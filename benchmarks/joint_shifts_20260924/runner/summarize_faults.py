"""Summarize fixed scores by fault family/subtype; no retraining or selection."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.stats import hmean
from sklearn.metrics import roc_auc_score

RUN = Path(__file__).resolve().parent
OUT = RUN / 'evaluation/seed13711'


def main():
    result = json.loads((OUT / 'result.json').read_text())
    audit_path = Path(result.get('audit_path', str(OUT / 'audit.json')))
    assert json.loads(audit_path.read_text())['status'] == 'VALIDATED'
    with (OUT / 'file_scores.csv').open() as stream:
        rows = list(csv.DictReader(stream))
    normal = [r for r in rows if r['label'] == 'normal']
    assert len(normal) * 2 == len(rows)
    output = []
    for scope, column in [('family', 'fault_family'), ('subtype', 'fault_subtype')]:
        for fault in sorted({r[column] for r in rows if r['label'] == 'anomaly'}):
            anomaly = [r for r in rows if r['label'] == 'anomaly' and r[column] == fault]
            selected = normal + anomaly
            labels = np.array([int(r['label'] == 'anomaly') for r in selected])
            domains = np.array([r['domain'] for r in selected])
            for method in ['MSE', 'MAHALA']:
                scores = np.array([float(r[method]) for r in selected])
                record = {'scope': scope, 'fault': fault, 'method': method, 'seed': result['seed'], 'normal_count': len(normal), 'anomaly_count': len(anomaly), 'anomaly_source': sum(r['domain'] == 'source' for r in anomaly), 'anomaly_target': sum(r['domain'] == 'target' for r in anomaly), 'AUC_pooled': roc_auc_score(labels, scores), 'pAUC_pooled': roc_auc_score(labels, scores, max_fpr=0.1)}
                for domain in ['source', 'target']:
                    mask = (domains == domain) | (labels == 1)
                    record[f'AUC_{domain}_dcase'] = roc_auc_score(labels[mask], scores[mask])
                    own = domains == domain
                    record[f'AUC_{domain}_within_domain'] = roc_auc_score(labels[own], scores[own])
                    pos, neg = scores[mask & (labels == 1)], scores[mask & (labels == 0)]
                    rank_auc = np.mean(pos[:, None] > neg[None, :]) + .5 * np.mean(pos[:, None] == neg[None, :])
                    assert abs(rank_auc - record[f'AUC_{domain}_dcase']) < 1e-12
                record['hmean_dcase'] = float(hmean([record['AUC_source_dcase'], record['AUC_target_dcase'], record['pAUC_pooled']]))
                output.append(record)
    assert len(output) == 28  # 4 fault families + 10 subtypes, for 2 score methods.
    for method in ['MSE', 'MAHALA']:
        pooled = [r for r in output if r['scope'] == 'family' and r['method'] == method]
        weighted = sum(r['AUC_pooled'] * r['anomaly_count'] for r in pooled) / sum(r['anomaly_count'] for r in pooled)
        reference = next(r for r in json.loads((OUT / 'result.json').read_text())['metrics'] if r['method'] == method)
        assert abs(weighted - reference['AUC_pooled']) < 1e-12
    with (OUT / 'fault_metrics.csv').open('w') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(output[0]))
        writer.writeheader(); writer.writerows(output)
    (OUT / 'fault_verification.json').write_text(json.dumps({'status': 'PASS', 'input_score_sha256': hashlib.sha256((OUT / 'file_scores.csv').read_bytes()).hexdigest(), 'normal_reference': f'same {len(normal)} test-normal files for every fault scope', 'family_count': 4, 'subtype_count': 10, 'metric_rows': 28, 'pairwise_auc_check': 'PASS', 'family_weighted_auc_equals_pooled_auc': True, 'model_or_threshold_selection': False}, indent=2) + '\n')
    for row in output:
        if row['scope'] == 'family':
            print(row['method'], row['fault'], row['anomaly_count'], f"AUC={row['AUC_pooled']:.4f}", f"pAUC={row['pAUC_pooled']:.4f}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=OUT)
    cli = parser.parse_args()
    OUT = cli.output_dir.resolve()
    main()
