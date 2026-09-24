"""Reread one joint-shift delivery before any H100 training or scoring."""

import argparse
import csv
import hashlib
import json
import wave
from collections import Counter
from pathlib import Path

FOLDS = {
    "j1_ab_slow_13_to_c_fast_24": (("A", "B"), "slow", ("1", "3"), ("C",), "fast", ("2", "4")),
    "j2_ac_fast_24_to_b_slow_13": (("A", "C"), "fast", ("2", "4"), ("B",), "slow", ("1", "3")),
    "j3_bc_slow_12_to_a_fast_34": (("B", "C"), "slow", ("1", "2"), ("A",), "fast", ("3", "4")),
}
FAMILIES = {"belt_tension_abnormal", "extruder_cogging_or_no_extrusion", "cooling_fan_fault", "toolhead_collision"}
SUBTYPES = {"belt_a": 9, "belt_b": 8, "belt_a_b": 8,
            "extruder_cogging_or_no_extrusion": 25, "cooling_fan_fault": 25,
            **{f"collision_{x}": 5 for x in ("x-min", "x-max", "y-max", "x-min-y-max", "x-max-y-max")}}


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def rows(path):
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream))


def check(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--fold", choices=FOLDS, required=True)
    p.add_argument("--dataset-root", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    root = a.dataset_root.resolve()
    ready = json.loads((root / "DATASET_READY.json").read_text())
    check(ready["status"] == "VERIFIED_JOINT_SHIFT_SUBSET" and ready["fold"] == a.fold, "Wrong dataset receipt")
    protocol = json.loads((Path(__file__).resolve().parent / "protocol.json").read_text())
    check(ready["source_annotation_revision"] == protocol["dataset_annotation_revision"], "Wrong annotation revision")
    check(ready["source_metadata_manifest_sha256"] == protocol["source_metadata_manifest_sha256"], "Wrong source metadata manifest")
    check(ready["source_annotation_sha256"] == protocol["source_annotation_sha256"], "Wrong source annotation hashes")
    recipe = json.loads((root / "metadata/selection/recipe.json").read_text())
    check(recipe["selection_sha256"] == ready["selection_sha256"], "Recipe/receipt mismatch")
    train_path, test_path = (root / f"metadata/{part}/selected_samples.csv" for part in ("train", "test"))
    train, test = rows(train_path), rows(test_path)
    all_rows = train + test
    check(len(train) == 1000 and len(test) == 400, "Wrong split size")
    check(Counter((r["domain"], r["label"]) for r in train) == {("source", "normal"): 990, ("target", "normal"): 10}, "Train balance")
    check(Counter((r["domain"], r["label"]) for r in test) == {(d, l): 100 for d in ("source", "target") for l in ("normal", "anomaly")}, "Test balance")
    check(all(r["collection_slot"].endswith(("-1", "-2")) for r in train), "Train normal repetition must be 1 or 2")
    check(all(r["collection_slot"].endswith("-3") for r in test if r["label"] == "normal"), "Test normal repetition must be 3")
    src_printers, src_speed, src_channels, tgt_printers, tgt_speed, tgt_channels = FOLDS[a.fold]
    for domain, printers, speed, channels in (("source", src_printers, src_speed, src_channels), ("target", tgt_printers, tgt_speed, tgt_channels)):
        domain_rows = [r for r in all_rows if r["domain"] == domain]
        check(all(r["printer_id"] in printers and r["speed_profile"] == speed and r["channel_id"] in channels for r in domain_rows), f"{domain} factor mismatch")
        check(Counter(r["channel_id"] for r in train if r["domain"] == domain) == {c: (495 if domain == "source" else 5) for c in channels}, f"{domain} train channel balance")
        for label in ("normal", "anomaly"):
            chosen = [r for r in test if r["domain"] == domain and r["label"] == label]
            check(Counter(r["channel_id"] for r in chosen) == {c: 50 for c in channels}, f"{domain}/{label} channel balance")
            if domain == "source":
                check(Counter(r["printer_id"] for r in chosen) == {pr: 50 for pr in printers}, f"{domain}/{label} printer balance")
        anomalies = [r for r in test if r["domain"] == domain and r["label"] == "anomaly"]
        check(Counter(r["fault_family"] for r in anomalies) == dict.fromkeys(FAMILIES, 25), f"{domain} family balance")
        check(Counter(r["fault_subtype"] for r in anomalies) == SUBTYPES, f"{domain} subtype balance")
    check(Counter(r["printer_id"] for r in train if r["domain"] == "source") == {pr: 495 for pr in src_printers}, "Source train printer balance")
    check(not ({r["session_id"] for r in train} & {r["session_id"] for r in test}), "Train/test session overlap")
    check(not ({r["clip_uid"] for r in train} & {r["clip_uid"] for r in test}), "Train/test temporal overlap")
    check(len({r["clip_uid"] for r in test}) == 400, "Test temporal clips not unique")
    for key in ("sample_id", "destination_audio_path", "mono_wav_sha256"):
        check(len({r[key] for r in all_rows}) == 1400, f"Repeated {key}")
    check(sha(root / "metadata/selection/selected_samples.csv") == ready["selection_sha256"], "Frozen selection mismatch")
    for row in all_rows:
        dest = root / row["destination_audio_path"]
        check(dest.is_file() and dest.stat().st_size == int(row["bytes"]), f"Missing/short WAV: {dest}")
        check(sha(dest) == row["mono_wav_sha256"], f"WAV hash mismatch: {dest}")
        with wave.open(str(dest)) as wav:
            check((wav.getframerate(), wav.getnchannels(), wav.getsampwidth(), wav.getnframes()) == (48000, 1, 2, 480000), f"WAV shape mismatch: {dest}")
    for part, selected in (("train", train), ("test", test)):
        sample_ids = {r["sample_id"] for r in selected}
        for filename in ("clip_gcode.csv", "clip_telemetry.csv", "clip_timeline.csv", "clip_annotations_range.csv"):
            check({r["sample_id"] for r in rows(root / "metadata" / part / filename)} == sample_ids, f"Annotation coverage: {part}/{filename}")
    for kind, field, value in (("data", "label", "anomaly"), ("domain", "domain", "target")):
        truth = dict(csv.reader((root / f"metadata/selection/evaluator/ground_truth_{kind}/ground_truth_3DPrinter_section_00_test.csv").open()))
        check(len(truth) == 400, f"Wrong {kind} truth size")
        check(all(int(truth[Path(r["destination_audio_path"]).name]) == int(r[field] == value) for r in test), f"Wrong {kind} truth")
    receipt = {"status": "VALIDATED", "fold": a.fold, "train_count": 1000, "test_count": 400,
               "train_selection_sha256": sha(train_path), "test_selection_sha256": sha(test_path),
               "selection_sha256": recipe["selection_sha256"], "audio_hashes_checked": 1400,
               "train_sessions": len({r["session_id"] for r in train}), "test_sessions": len({r["session_id"] for r in test}),
               "train_temporal_intervals": len({r["clip_uid"] for r in train}), "test_temporal_intervals": 400,
               "scope": "File, annotation, ratio and overlap audit; not independent acoustic ground-truth verification."}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
