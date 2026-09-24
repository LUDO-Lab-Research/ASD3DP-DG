#!/usr/bin/env python3
"""Copy and rehash one frozen joint-shift selection, including r4 annotations."""

import argparse
import csv
import hashlib
import json
import os
import shutil
import wave
from collections import Counter, defaultdict
from pathlib import Path

ANNOTATIONS = ("clip_gcode.csv", "clip_telemetry.csv", "clip_timeline.csv", "clip_annotations_range.csv")


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def rows(path):
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream))


def safe(root, relative):
    path = root / relative
    if not relative or Path(relative).is_absolute() or ".." in Path(relative).parts or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"Unsafe relative path: {relative}")
    return path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source", type=Path, required=True)
    p.add_argument("--selection", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    source, selection, output = (x.resolve() for x in (args.source, args.selection, args.output))
    if output.exists():
        raise ValueError(f"Output exists: {output}")
    recipe = json.loads((selection / "recipe.json").read_text())
    selected = rows(selection / "selected_samples.csv")
    if sha(selection / "selected_samples.csv") != recipe["selection_sha256"]:
        raise ValueError("Selection SHA-256 changed")
    for name, digest in recipe["source_input_sha256"].items():
        if sha(source / name) != digest:
            raise ValueError(f"Source metadata changed: {name}")
    manifest = {}
    with (source / "METADATA_SHA256SUMS").open() as stream:
        for line in stream:
            digest, relative = line.rstrip("\n").split("  ", 1)
            manifest[relative] = digest
    source_annotation_hashes = {}
    for filename in ANNOTATIONS:
        relative = f"annotations/clip/{filename}"
        actual = sha(source / relative)
        if manifest.get(relative) != actual:
            raise ValueError(f"r4 annotation differs from its release manifest: {relative}")
        source_annotation_hashes[relative] = actual
    if len(selected) != 1400:
        raise ValueError("Expected 1,400 WAV files")
    need_bytes = sum(int(r["bytes"]) for r in selected)
    if shutil.disk_usage(output.parent).free < need_bytes + 500_000_000:
        raise ValueError("Insufficient free space for dataset and reserve")
    stage = output.with_name(output.name + ".staging")
    stage.mkdir(parents=True, exist_ok=True)
    owner = stage / ".selection-owner.json"
    identity = {"selection_sha256": recipe["selection_sha256"], "source": str(source)}
    if owner.exists() and json.loads(owner.read_text()) != identity:
        raise ValueError("Staging belongs to another selection")
    owner.write_text(json.dumps(identity, indent=2) + "\n")
    copies = 0
    for r in selected:
        original = safe(source, r["audio_path"])
        dest = safe(stage, r["destination_audio_path"])
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not original.is_file() or original.stat().st_size != int(r["bytes"]) or sha(original) != r["mono_wav_sha256"]:
            raise ValueError(f"Missing or corrupt source WAV: {original}")
        if not dest.exists():
            partial = dest.with_suffix(".wav.partial")
            shutil.copyfile(original, partial)
            os.replace(partial, dest)
        if dest.stat().st_size != int(r["bytes"]) or sha(dest) != r["mono_wav_sha256"]:
            raise ValueError(f"Copied WAV differs: {dest}")
        with wave.open(str(dest), "rb") as wav:
            if (wav.getframerate(), wav.getnchannels(), wav.getsampwidth(), wav.getnframes()) != (48000, 1, 2, 480000):
                raise ValueError(f"Wrong WAV shape: {dest}")
        copies += 1
        if copies % 100 == 0:
            print(f"{selection.name}: verified {copies}/{len(selected)} WAVs", flush=True)
    for partition in ("train", "test"):
        part = stage / "metadata" / partition
        part.mkdir(parents=True, exist_ok=True)
        with (part / "selected_samples.csv").open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(selected[0]))
            writer.writeheader()
            writer.writerows(r for r in selected if r["partition"] == partition)
    by_uid = defaultdict(list)
    for r in selected:
        by_uid[r["clip_uid"]].append(r)
    for filename in ANNOTATIONS:
        src = source / "annotations/clip" / filename
        with src.open(newline="") as stream:
            reader = csv.DictReader(stream)
            handles = {part: (stage / "metadata" / part / filename).open("w", newline="") for part in ("train", "test")}
            writers = {part: csv.DictWriter(handle, fieldnames=["sample_id", "destination_audio_path", *reader.fieldnames]) for part, handle in handles.items()}
            for writer in writers.values():
                writer.writeheader()
            seen = set()
            for original in reader:
                for selected_row in by_uid.get(original["clip_uid"], ()):
                    if original["session_id"] != selected_row["session_id"] or original["printer_id"] != selected_row["printer_id"]:
                        raise ValueError(f"Annotation join mismatch: {filename}")
                    writers[selected_row["partition"]].writerow({"sample_id": selected_row["sample_id"], "destination_audio_path": selected_row["destination_audio_path"], **original})
                    seen.add(selected_row["sample_id"])
            for handle in handles.values():
                handle.close()
            if len(seen) != len(selected):
                raise ValueError(f"Annotation coverage mismatch: {filename}, {len(seen)}")
    (stage / "metadata/selection").mkdir(parents=True, exist_ok=True)
    with (stage / "metadata/selection/selected_samples.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(selected[0]))
        writer.writeheader()
        writer.writerows(selected)
    shutil.copy2(selection / "recipe.json", stage / "metadata/selection/recipe.json")
    for kind, field in (("data", "label"), ("domain", "domain")):
        out = stage / f"metadata/selection/evaluator/ground_truth_{kind}/ground_truth_3DPrinter_section_00_test.csv"
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", newline="") as handle:
            writer = csv.writer(handle)
            for r in selected:
                if r["partition"] == "test":
                    writer.writerow((Path(r["destination_audio_path"]).name, int(r[field] == ("anomaly" if kind == "data" else "target"))))
    output_hashes = {str(p.relative_to(stage)): sha(p) for p in stage.rglob("*") if p.is_file() and p.name not in ("SHA256SUMS", "DATASET_READY.json")}
    (stage / "SHA256SUMS").write_text("".join(f"{digest}  {name}\n" for name, digest in sorted(output_hashes.items())))
    receipt = {"status": "VERIFIED_JOINT_SHIFT_SUBSET", "fold": selection.name,
               "selection_sha256": recipe["selection_sha256"], "source_annotation_revision": recipe["annotation_revision"],
               "train_count": 1000, "test_count": 400, "audio_hashes_checked": copies,
               "annotation_tables_checked": list(ANNOTATIONS),
               "source_metadata_manifest_sha256": sha(source / "METADATA_SHA256SUMS"),
               "source_annotation_sha256": source_annotation_hashes,
               "source_retained": True}
    (stage / "DATASET_READY.json").write_text(json.dumps(receipt, indent=2) + "\n")
    os.rename(stage, output)
    print(json.dumps(receipt, indent=2), flush=True)


if __name__ == "__main__":
    main()
