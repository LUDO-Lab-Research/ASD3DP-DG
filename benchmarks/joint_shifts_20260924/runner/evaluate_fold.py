"""Evaluate a frozen epoch-100 model using the pinned upstream score functions."""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import pickle
import sys
from types import SimpleNamespace

RUN = Path(__file__).resolve().parent
preparser = argparse.ArgumentParser(add_help=False)
FOLDS = ['j1_ab_slow_13_to_c_fast_24', 'j2_ac_fast_24_to_b_slow_13', 'j3_bc_slow_12_to_a_fast_34']
preparser.add_argument('--fold', required=True, choices=FOLDS)
precli, _ = preparser.parse_known_args()
FOLD = precli.fold
BASE = RUN / 'folds' / FOLD / 'baseline'
OUT = RUN / 'evaluation' / FOLD / 'seed13711'
DATA = Path('/home/dori/datasets/asd3dp-dg-joint') / FOLD
for key in ['OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS']:
    os.environ[key] = '1'
os.environ['MPLBACKEND'] = 'Agg'
sys.path.insert(0, str(BASE))

import numpy as np
import scipy.stats
import torch
from sklearn import metrics
from datasets.loader_common import file_to_vectors
from networks.dcase2023t2_ae.network import AENet
from networks.dcase2023t2_ae.dcase2023t2_ae import DCASE2023T2AE
from networks.criterion.mahala import calc_inv_cov


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(seed=13711, audit_path=None):
    OUT.mkdir(parents=True, exist_ok=True)
    os.chdir(OUT)
    audit_path = audit_path or OUT.parent / 'audit.json'
    audit = json.loads(audit_path.read_text())
    assert audit['status'] == 'VALIDATED'
    assert sha(DATA / 'metadata/test/selected_samples.csv') == audit['test_selection_sha256']
    plan = json.loads((RUN / 'protocol.json').read_text())
    assert seed in plan['seeds'] and FOLD in plan['folds']
    assert all(sha(BASE / path) == digest for path, digest in plan['expected_source_hashes'].items())
    assert sha(DATA / 'metadata/train/selected_samples.csv') == plan['folds'][FOLD]['train_selection_sha256']
    model_name = f'DCASE2023T2-AE_DCASE2023T23DPrinter_seed{seed}'
    model_dir = BASE / 'models/saved_model' / f'asd3dp_dg_joint_{FOLD}'
    model_path = model_dir / f'{model_name}.pth'
    checkpoint_dir = BASE / 'models/checkpoint' / f'asd3dp_dg_joint_{FOLD}' / model_name
    args_path = checkpoint_dir / 'args.json'
    args_hash = sha(args_path)
    model_hash = sha(model_path)
    args = json.loads(args_path.read_text())
    assert args['seed'] == seed and args['epochs'] == 100
    exit_file = RUN / 'logs' / FOLD / f'train_seed{seed}.exit'
    assert exit_file.read_text().strip() == '0'
    checkpoint = torch.load(checkpoint_dir / 'checkpoint.tar', map_location='cpu', weights_only=True)
    assert checkpoint['epoch'] == 100
    model = AENet(input_dim=args['n_mels'] * args['frames'], block_size=args['n_mels'])
    weights = torch.load(model_path, map_location='cpu', weights_only=True)
    assert all(torch.isfinite(value).all() for value in weights.values())
    model.load_state_dict(weights, strict=True)
    model.eval()
    torch.set_num_threads(1)
    # Avoid BaseModel.__init__: it writes args.json and loads the training cache.
    # Call the actual pinned upstream eval method on one complete file at a time.
    evaluator = object.__new__(DCASE2023T2AE)
    evaluator.model = model
    evaluator.device = torch.device('cpu')
    evaluator.block_size = args['n_mels']
    evaluator.args = SimpleNamespace(score='MSE')
    inv_source, inv_target = calc_inv_cov(model=model, device=evaluator.device)
    thresholds = {}
    for method in ['MSE', 'MAHALA']:
        distribution = model_dir / f'score_distr_{model_name}_{method.lower()}.pickle'
        with distribution.open('rb') as stream:
            shape, loc, scale = pickle.load(stream)
        thresholds[method] = float(scipy.stats.gamma.ppf(args['decision_threshold'], shape, loc=loc, scale=scale))
    with (DATA / 'metadata/test/selected_samples.csv').open() as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == audit['test_count']
    assert len({row['mono_wav_sha256'] for row in rows}) == len(rows)
    scored = []
    with torch.inference_mode():
        for index, row in enumerate(rows, 1):
            path = DATA / row['destination_audio_path']
            assert sha(path) == row['mono_wav_sha256']
            vectors = file_to_vectors(str(path), n_mels=args['n_mels'], n_frames=args['frames'], n_fft=args['n_fft'], hop_length=args['hop_length'], power=args['power'], fmin=args['fmin'], fmax=args['fmax'], win_length=args['win_length'], mono=args['mono'])
            vectors = vectors[::args['frame_hop_length']]
            assert vectors.shape == (934, 640) and np.isfinite(vectors).all()
            batch = (torch.from_numpy(vectors), torch.tensor([int(row['label'] == 'anomaly')]), None, [path.name])
            result = {'filename': path.name, 'clip_uid': row['clip_uid'], 'audio_sha256': row['mono_wav_sha256'], 'domain': row['domain'], 'label': row['label'], 'fault_family': row['fault_family'], 'fault_subtype': row['fault_subtype'], 'session_id': row['session_id'], 'channel_id': row['channel_id'], 'vectors': len(vectors)}
            for method in ['MSE', 'MAHALA']:
                evaluator.args.score = method
                predictions, _, decisions, _ = evaluator.eval(test_loader=[batch], y_pred=[], anomaly_score_list=[], decision_result_list=[], domain_list=None, y_true=[], decision_threshold=thresholds[method], mode=False, inv_cov_source=inv_source, inv_cov_target=inv_target)
                result[method] = predictions[0]
                result[f'{method}_decision'] = decisions[0][1]
                assert np.isfinite(predictions[0])
            scored.append(result)
            if index % 50 == 0:
                print(f'Scored {index}/{len(rows)} files', flush=True)
    with (OUT / 'file_scores.csv').open('w') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(scored[0]))
        writer.writeheader(); writer.writerows(scored)
    labels = np.array([int(row['label'] == 'anomaly') for row in scored])
    domains = np.array([row['domain'] for row in scored])
    summaries = []
    for method in ['MSE', 'MAHALA']:
        scores = np.array([row[method] for row in scored])
        # Match the upstream DCASE2023 source/target AUC definition exactly:
        # normals from the named domain versus anomalies from BOTH domains.
        values = {'method': method, 'seed': seed, 'epoch': 100, 'test_files': len(scored), 'AUC_pooled': metrics.roc_auc_score(labels, scores), 'pAUC_pooled_max_fpr_0_1': metrics.roc_auc_score(labels, scores, max_fpr=0.1), 'threshold_train_gamma_q90': thresholds[method]}
        for domain in ['source', 'target']:
            mask = (domains == domain) | (labels == 1)
            values[f'AUC_{domain}_dcase'] = metrics.roc_auc_score(labels[mask], scores[mask])
            pos, neg = scores[mask & (labels == 1)], scores[mask & (labels == 0)]
            pairwise_auc = ((pos[:, None] > neg[None, :]).mean() + 0.5 * (pos[:, None] == neg[None, :]).mean())
            assert abs(values[f'AUC_{domain}_dcase'] - pairwise_auc) < 1e-12
            own = domains == domain
            values[f'AUC_{domain}_within_domain'] = metrics.roc_auc_score(labels[own], scores[own])
            values[f'pAUC_{domain}_within_domain'] = metrics.roc_auc_score(labels[own], scores[own], max_fpr=0.1)
            values[f'F1_{domain}'] = metrics.f1_score(labels[own], scores[own] > thresholds[method], zero_division=0)
        values['hmean_source_target_pAUC'] = float(scipy.stats.hmean([values['AUC_source_dcase'], values['AUC_target_dcase'], values['pAUC_pooled_max_fpr_0_1']]))
        summaries.append(values)
    with (OUT / 'metrics.csv').open('w') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(summaries[0]))
        writer.writeheader(); writer.writerows(summaries)
    assert sha(args_path) == args_hash, 'Training args were modified'
    assert sha(model_path) == model_hash
    receipt = {'status': 'COMPLETED', 'seed': seed, 'checkpoint_epoch': 100, 'device': 'cpu', 'dataset_root': str(DATA), 'audit_path': str(audit_path), 'audit_sha256': sha(audit_path), 'model_sha256': model_hash, 'training_args_sha256': args_hash, 'test_selection_sha256': audit['test_selection_sha256'], 'file_scores_sha256': sha(OUT / 'file_scores.csv'), 'evaluation_script_sha256': sha(Path(__file__)), 'score_implementation': 'pinned upstream DCASE2023T2AE.eval, with source file_to_vectors and calc_inv_cov', 'test_files': len(scored), 'thresholds': thresholds, 'training_or_model_selection_performed': False, 'metric_independent_pairwise_auc_check': 'PASS', 'metrics': summaries}
    (OUT / 'result.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(summaries, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fold', required=True, choices=FOLDS)
    parser.add_argument('--seed', type=int, choices=[13711], default=13711)
    parser.add_argument('--dataset-root', type=Path, default=DATA)
    parser.add_argument('--output-dir', type=Path)
    parser.add_argument('--audit-json', type=Path)
    cli = parser.parse_args()
    DATA = cli.dataset_root.resolve()
    OUT = (cli.output_dir or RUN / 'evaluation' / FOLD / f'seed{cli.seed}').resolve()
    main(cli.seed, cli.audit_json.resolve() if cli.audit_json else None)
