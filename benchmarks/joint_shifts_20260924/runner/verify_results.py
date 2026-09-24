"""Independently verify score tables against frozen selections and source hashes."""

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

RUN = Path(__file__).resolve().parent
SELECTIONS = RUN.parents[1] / "benchmarks/joint_shifts_20260924/selections"
FAMILIES = ("belt_tension_abnormal", "extruder_cogging_or_no_extrusion", "cooling_fan_fault", "toolhead_collision")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def csv_rows(path):
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream))


def area(rows, method, max_fpr=None):
    scores = sorted(((float(r[method]), r["label"] == "anomaly") for r in rows), reverse=True)
    p = sum(label for _, label in scores)
    n = len(scores) - p
    assert p and n
    tp = fp = 0
    x0 = y0 = raw = 0.0
    for score in sorted({score for score, _ in scores}, reverse=True):
        group = [label for s, label in scores if s == score]
        tp += sum(group)
        fp += len(group) - sum(group)
        x1, y1 = fp / n, tp / p
        if max_fpr is None:
            raw += (x1 - x0) * (y0 + y1) / 2
        elif x0 < max_fpr:
            x = min(x1, max_fpr)
            y = y0 + (y1 - y0) * (x - x0) / (x1 - x0) if x1 != x0 else y1
            raw += (x - x0) * (y0 + y) / 2
        x0, y0 = x1, y1
    if max_fpr is None:
        return raw
    minimum = max_fpr**2 / 2
    return 0.5 * (1 + (raw - minimum) / (max_fpr - minimum))


def close(actual, expected, name):
    if abs(actual - float(expected)) > 1e-10:
        raise ValueError(f"{name}: recomputed {actual}, reported {expected}")


def verify_fold(fold, protocol):
    location = RUN / "evaluation" / fold
    folder = location / "seed13711"
    audit = json.loads((location / "audit.json").read_text())
    result = json.loads((folder / "result.json").read_text())
    fault_receipt = json.loads((folder / "fault_verification.json").read_text())
    assert audit["status"] == "VALIDATED" and fault_receipt["status"] == "PASS"
    assert result["status"] == "COMPLETED" and result["seed"] == 13711 and result["checkpoint_epoch"] == 100
    assert sha(location / "audit.json") == result["audit_sha256"]
    assert sha(folder / "file_scores.csv") == result["file_scores_sha256"] == fault_receipt["input_score_sha256"]
    assert audit["selection_sha256"] == protocol["folds"][fold]["selection_sha256"]
    assert audit["train_selection_sha256"] == protocol["folds"][fold]["train_selection_sha256"]
    assert audit["test_selection_sha256"] == protocol["folds"][fold]["test_selection_sha256"]
    assert (RUN / "logs" / fold / "train_seed13711.exit").read_text().strip() == "0"
    selected = [r for r in csv_rows(SELECTIONS / fold / "selected_samples.csv") if r["partition"] == "test"]
    scores = csv_rows(folder / "file_scores.csv")
    assert len(scores) == len(selected) == 400
    assert Counter((r["domain"], r["label"]) for r in scores) == {(d, label): 100 for d in ("source", "target") for label in ("normal", "anomaly")}
    assert len({r["clip_uid"] for r in scores}) == 400
    expected = {Path(r["destination_audio_path"]).name: r for r in selected}
    assert set(expected) == {r["filename"] for r in scores}
    for r in scores:
        source = expected[r["filename"]]
        for score_field, selection_field in (("audio_sha256", "mono_wav_sha256"), ("clip_uid", "clip_uid"), ("domain", "domain"), ("label", "label"), ("fault_family", "fault_family"), ("fault_subtype", "fault_subtype"), ("session_id", "session_id"), ("channel_id", "channel_id")):
            assert r[score_field] == source[selection_field], (fold, r["filename"], score_field)
    family_rows = [r for r in csv_rows(folder / "fault_metrics.csv") if r["scope"] == "family"]
    assert len(family_rows) == 8
    assert {r["fault"] for r in family_rows} == set(FAMILIES)
    for reported in result["metrics"]:
        method = reported["method"]
        assert method in ("MSE", "MAHALA") and reported["epoch"] == 100 and reported["test_files"] == 400
        close(area(scores, method), reported["AUC_pooled"], f"{fold}/{method}/pooled")
        close(area(scores, method, 0.1), reported["pAUC_pooled_max_fpr_0_1"], f"{fold}/{method}/pAUC")
        for domain in ("source", "target"):
            subset = [r for r in scores if r["domain"] == domain or r["label"] == "anomaly"]
            close(area(subset, method), reported[f"AUC_{domain}_dcase"], f"{fold}/{method}/{domain}")
        for family in FAMILIES:
            faults = [r for r in scores if r["label"] == "normal" or r["fault_family"] == family]
            record = next(r for r in family_rows if r["method"] == method and r["fault"] == family)
            assert int(record["anomaly_count"]) == 50
            for domain in ("source", "target"):
                subset = [r for r in faults if r["domain"] == domain or r["label"] == "anomaly"]
                close(area(subset, method), record[f"AUC_{domain}_dcase"], f"{fold}/{method}/{family}/{domain}")
    return {"selection_sha256": audit["selection_sha256"], "result_sha256": sha(folder / "result.json"), "fault_metrics_sha256": sha(folder / "fault_metrics.csv"), "file_scores_sha256": sha(folder / "file_scores.csv"), "test_files": 400, "independent_auc_recalculation": "PASS"}


def main():
    protocol = json.loads((RUN / "protocol.json").read_text())
    assert protocol["seeds"] == [13711] and protocol["epochs_per_seed"] == 100
    folds = {fold: verify_fold(fold, protocol) for fold in protocol["folds"]}
    receipt = {"status": "PASS", "protocol_sha256": sha(RUN / "protocol.json"), "folds": folds}
    (RUN / "LOCAL_RESULTS_VERIFIED.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
