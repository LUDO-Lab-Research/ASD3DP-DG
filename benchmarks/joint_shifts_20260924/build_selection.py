#!/usr/bin/env python3
"""Select the three approved joint printer/speed/microphone shifts from r4."""

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

SEED = 20260924
FAMILIES = (
    "belt_tension_abnormal",
    "extruder_cogging_or_no_extrusion",
    "cooling_fan_fault",
    "toolhead_collision",
)
SUBTYPE_QUOTAS = {
    "belt_tension_abnormal": {"belt_a": 9, "belt_b": 8, "belt_a_b": 8},
    "extruder_cogging_or_no_extrusion": {"extruder_cogging_or_no_extrusion": 25},
    "cooling_fan_fault": {"cooling_fan_fault": 25},
    "toolhead_collision": {f"collision_{direction}": 5 for direction in
                           ("x-min", "x-max", "y-max", "x-min-y-max", "x-max-y-max")},
}
FOLDS = {
    "j1_ab_slow_13_to_c_fast_24": (("A", "B"), "slow", (1, 3), ("C",), "fast", (2, 4)),
    "j2_ac_fast_24_to_b_slow_13": (("A", "C"), "fast", (2, 4), ("B",), "slow", (1, 3)),
    "j3_bc_slow_12_to_a_fast_34": (("B", "C"), "slow", (1, 2), ("A",), "fast", (3, 4)),
}
POSITIONS = {1: "rear", 2: "left", 3: "front", 4: "right"}


def read_csv(path):
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def rank(*parts):
    return hashlib.sha256(json.dumps((SEED, *parts), separators=(",", ":")).encode()).hexdigest()


def choose(pool, n, used_uids, fold, purpose):
    ordered = sorted(pool, key=lambda r: (rank(fold, purpose, r["clip_uid"], r["channel_id"]), r["clip_uid"], r["channel_id"]))
    selected = []
    for row in ordered:
        if row["clip_uid"] in used_uids:
            continue
        selected.append(row)
        used_uids.add(row["clip_uid"])
        if len(selected) == n:
            break
    if len(selected) != n:
        raise ValueError(f"Insufficient distinct temporal clips for {fold}/{purpose}: {len(selected)} < {n}")
    return selected


def choose_train(pool, n, fold, purpose):
    # Both microphone views are valid training files. Reuse of a temporal
    # interval is confined to this partition; evaluation sessions are separate.
    selected = sorted(pool, key=lambda r: (rank(fold, purpose, r["clip_uid"], r["channel_id"]), r["clip_uid"], r["channel_id"]))[:n]
    if len(selected) != n:
        raise ValueError(f"Insufficient training files for {fold}/{purpose}: {len(selected)} < {n}")
    return selected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source, output = args.source.resolve(), args.output.resolve()
    ready = json.loads((source / "DATASET_READY.json").read_text())
    if ready.get("status") != "VERIFIED_AUDIO_AND_ANNOTATIONS" or ready.get("annotation_revision") != "r4-20260924":
        raise ValueError("Expected verified r4 source release")
    paths = ["DATASET_READY.json", "annotations/clip/clip_plan.csv", "annotations/clip/clip_audio_manifest.csv", "annotations/session/session_context.csv", "annotations/session/end_anchors.csv"]
    inputs = {name: sha(source / name) for name in paths}
    contexts = {r["session_id"]: r for r in read_csv(source / paths[3])}
    anchors = {r["session_id"]: r for r in read_csv(source / paths[4])}
    clips = {r["clip_uid"]: r for r in read_csv(source / paths[1])}
    audio = read_csv(source / paths[2])
    if len(clips) != 11861 or len(audio) != 47444:
        raise ValueError("Unexpected r4 population")
    candidates = []
    seen = set()
    for wav in audio:
        key = wav["clip_uid"], wav["channel_id"]
        if key in seen:
            raise ValueError(f"Duplicate audio view: {key}")
        seen.add(key)
        clip = clips[wav["clip_uid"]]
        ctx = contexts[clip["session_id"]]
        anchor = anchors[clip["session_id"]]
        if clip["selected"] != "true" or clip["status"] != "selected" or clip["blocking_reasons"]:
            raise ValueError("Unselected clip in audio manifest")
        if any(wav[k] != clip[k] for k in ("session_id", "printer_id", "label", "start_source_frame", "end_source_frame_exclusive")):
            raise ValueError("Audio/clip identity mismatch")
        if wav["audio_delivery_state"] != "verified_loose_and_archived_clip_wav" or int(wav["bytes"]) != 960044:
            raise ValueError("Unverified audio file")
        if int(clip["end_source_frame_exclusive"]) - int(clip["start_source_frame"]) != 480000:
            raise ValueError("Not a 10-second window")
        if ctx["selected_condition"] != clip["condition"] or ctx["selected_speed_profile"] != clip["speed_profile"]:
            raise ValueError("Context/clip contradiction")
        if anchor["source_wav_sha256"] != wav["source_interleaved_wav_sha256"]:
            raise ValueError("Anchor/source WAV contradiction")
        family = clip["fault_family"]
        subtype = (ctx["belt_target"] if family == "belt_tension_abnormal" else
                   f"collision_{ctx['collision_direction']}" if family == "toolhead_collision" else family)
        if clip["label"] == "anomaly" and subtype not in SUBTYPE_QUOTAS[family]:
            raise ValueError("Unknown fault subtype")
        candidates.append({**wav, "fault_family": clip["fault_family"], "speed_profile": clip["speed_profile"],
                           "fault_subtype": subtype,
                           "collection_slot": ctx["collection_slot"], "condition": clip["condition"],
                           "microphone_position": POSITIONS[int(wav["channel_id"])],
                           "fault_overlap_sec": clip["fault_overlap_sec"], "fault_overlap_ratio": clip["fault_overlap_ratio"],
                           "anchor_revision": anchor["anchor_revision"], "anchor_source": anchor["anchor_source"],
                           "delta_seconds": anchor["delta_seconds"]})
    if len(seen) != len(candidates):
        raise ValueError("Audio identity count mismatch")
    output.mkdir(parents=True, exist_ok=True)
    for fold, (source_printers, source_speed, source_channels, target_printers, target_speed, target_channels) in FOLDS.items():
        rows = []
        for domain, printers, speed, channels in (("source", source_printers, source_speed, source_channels), ("target", target_printers, target_speed, target_channels)):
            for pi, printer in enumerate(printers):
                used_normal_test = set()
                for ci, channel in enumerate(channels):
                    pool = [r for r in candidates if r["printer_id"] == printer and r["speed_profile"] == speed and int(r["channel_id"]) == channel]
                    normal_train = [r for r in pool if r["label"] == "normal" and r["collection_slot"] in (f"normal-{speed}-1", f"normal-{speed}-2")]
                    normal_test = [r for r in pool if r["label"] == "normal" and r["collection_slot"] == f"normal-{speed}-3"]
                    if domain == "source":
                        train_n = 248 if pi == ci else 247
                        test_n = 25
                    else:
                        train_n = 5
                        test_n = 50
                    rows += [dict(r, partition="train", domain=domain) for r in choose_train(normal_train, train_n, fold, f"{domain}/{printer}/ch{channel}/train")]
                    rows += [dict(r, partition="test", domain=domain) for r in choose(normal_test, test_n, used_normal_test, fold, f"{domain}/{printer}/ch{channel}/normal-test")]
            # Allocate each family equally; alternate the odd source sample
            # between the two printers and the two microphone positions.
            for fi, family in enumerate(FAMILIES):
                cells = []
                for pi, printer in enumerate(printers):
                    for ci, channel in enumerate(channels):
                        if domain == "source":
                            n = 7 if pi == fi % 2 and ci == (0 if fi < 2 else 1) else 6
                        else:
                            n = 13 if (fi < 2 and ci == 0) or (fi >= 2 and ci == 1) else 12
                        cells.append((printer, channel, n))
                left = {(printer, channel): n for printer, channel, n in cells}
                allocations = defaultdict(Counter)
                for subtype, needed in SUBTYPE_QUOTAS[family].items():
                    for item in range(needed):
                        printer, channel, _ = max(cells, key=lambda cell: (left[(cell[0], cell[1])], rank(fold, domain, family, subtype, item, cell[0], cell[1])))
                        if left[(printer, channel)] <= 0:
                            raise ValueError("Fault subtype allocation exhausted")
                        left[(printer, channel)] -= 1
                        allocations[(printer, channel)][subtype] += 1
                if any(left.values()):
                    raise ValueError("Fault subtype allocation incomplete")
                used_anomaly = set()
                for printer, channel, _ in cells:
                    for subtype, n in allocations[(printer, channel)].items():
                        pool = [r for r in candidates if r["printer_id"] == printer and r["speed_profile"] == speed and int(r["channel_id"]) == channel and r["label"] == "anomaly" and r["fault_subtype"] == subtype]
                        rows += [dict(r, partition="test", domain=domain) for r in choose(pool, n, used_anomaly, fold, f"{domain}/{printer}/ch{channel}/{subtype}")]
        # A temporal clip may have both microphone views inside the same
        # partition. Its views must never straddle train and test.
        by_uid = defaultdict(set)
        for row in rows:
            by_uid[row["clip_uid"]].add(row["partition"])
        if any(len(parts) > 1 for parts in by_uid.values()):
            raise ValueError(f"Train/test temporal overlap in {fold}")
        if len({r["audio_path"] for r in rows}) != len(rows) or len({r["mono_wav_sha256"] for r in rows}) != len(rows):
            raise ValueError(f"Repeated WAV in {fold}")
        for domain, printers, speed, channels in (("source", source_printers, source_speed, source_channels), ("target", target_printers, target_speed, target_channels)):
            actual = [r for r in rows if r["domain"] == domain]
            if any(r["printer_id"] not in printers or r["speed_profile"] != speed or int(r["channel_id"]) not in channels for r in actual):
                raise ValueError(f"Domain assignment mismatch in {fold}")
        counts = Counter((r["partition"], r["domain"], r["label"]) for r in rows)
        wanted = {("train", "source", "normal"): 990, ("train", "target", "normal"): 10,
                  ("test", "source", "normal"): 100, ("test", "target", "normal"): 100,
                  ("test", "source", "anomaly"): 100, ("test", "target", "anomaly"): 100}
        if counts != wanted:
            raise ValueError(f"Budget mismatch in {fold}: {counts}")
        for domain in ("source", "target"):
            family_counts = Counter(r["fault_family"] for r in rows if r["partition"] == "test" and r["domain"] == domain and r["label"] == "anomaly")
            if family_counts != dict.fromkeys(FAMILIES, 25):
                raise ValueError(f"Fault balance mismatch in {fold}: {family_counts}")
            for family in FAMILIES:
                subtype_counts = Counter(r["fault_subtype"] for r in rows if r["partition"] == "test" and r["domain"] == domain and r["fault_family"] == family)
                if subtype_counts != SUBTYPE_QUOTAS[family]:
                    raise ValueError(f"Fault subtype mismatch in {fold}: {family}, {subtype_counts}")
            channel_counts = Counter(r["channel_id"] for r in rows if r["partition"] == "test" and r["domain"] == domain)
            if channel_counts != {str(c): 100 for c in (source_channels if domain == "source" else target_channels)}:
                raise ValueError(f"Channel balance mismatch in {fold}: {channel_counts}")
        if {r["session_id"] for r in rows if r["partition"] == "train"} & {r["session_id"] for r in rows if r["partition"] == "test"}:
            raise ValueError(f"Session overlap in {fold}")
        rows.sort(key=lambda r: (r["partition"], r["domain"], r["label"], r["printer_id"], r["channel_id"], r["clip_uid"]))
        index = Counter()
        for row in rows:
            key = (row["partition"], row["domain"])
            i = index[key]
            index[key] += 1
            prefix = f"section_00_{row['domain']}_train_normal" if row["partition"] == "train" else "section_00_test"
            # Test needs a single global sequence, including both domains.
            if row["partition"] == "test":
                i = index[("test", "all")]
                index[("test", "all")] += 1
            row["sample_id"] = f"{prefix}_{i:06d}"
            row["destination_audio_path"] = f"3DPrinter/{row['partition']}/{row['sample_id']}.wav"
        path = output / fold
        path.mkdir(parents=True, exist_ok=True)
        fields = ("sample_id", "partition", "domain", "label", "printer_id", "session_id", "clip_uid", "channel_id", "fault_family", "fault_subtype", "speed_profile", "collection_slot", "microphone_position", "condition", "audio_path", "destination_audio_path", "mono_wav_sha256", "bytes", "start_source_frame", "end_source_frame_exclusive", "source_interleaved_wav_sha256", "fault_overlap_sec", "fault_overlap_ratio", "anchor_revision", "anchor_source", "delta_seconds")
        with (path / "selected_samples.csv").open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows({key: row[key] for key in fields} for row in rows)
        recipe = {"name": fold, "selection_seed": SEED, "annotation_revision": ready["annotation_revision"],
                  "source": {"printers": source_printers, "speed": source_speed, "channels": source_channels},
                  "target": {"printers": target_printers, "speed": target_speed, "channels": target_channels},
                  "train": {"source_normal": 990, "target_normal": 10},
                  "test_per_domain": {"normal": 100, "anomaly": 100, "each_fault_family": 25},
                  "test_subtype_quotas_per_domain": SUBTYPE_QUOTAS,
                  "normal_session_roles": {"train": [1, 2], "test": [3]},
                  "audio_views": "Both microphone views may train on the same temporal clip; no temporal clip crosses train/test.",
                  "source_input_sha256": inputs, "selection_sha256": sha(path / "selected_samples.csv")}
        (path / "recipe.json").write_text(json.dumps(recipe, indent=2) + "\n")
        print(fold, len(rows), recipe["selection_sha256"])


if __name__ == "__main__":
    main()
