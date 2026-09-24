#!/usr/bin/env bash
set -euo pipefail
RUN_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN=/home/dori/project/asd3dp-dg-3d-recon/.venv/bin/python
export PYTHONPATH="$RUN_DIR/deps${PYTHONPATH:+:$PYTHONPATH}"
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MPLBACKEND=Agg
for fold in j1_ab_slow_13_to_c_fast_24 j2_ac_fast_24_to_b_slow_13 j3_bc_slow_12_to_a_fast_34; do
  exit_file="$RUN_DIR/logs/$fold/train_seed13711.exit"
  while [[ ! -f "$exit_file" ]]; do sleep 20; done
  [[ "$(cat "$exit_file")" == 0 ]] || { echo "Training failed: $fold" >&2; exit 1; }
  out="$RUN_DIR/evaluation/$fold/seed13711"
  [[ ! -e "$out/result.json" ]] || { echo "Result already exists: $fold" >&2; exit 1; }
  echo "$(date -u +%FT%TZ) EVALUATE $fold" >&2
  "$PYTHON_BIN" "$RUN_DIR/evaluate_fold.py" --fold "$fold" \
    > "$RUN_DIR/evaluation/$fold/evaluation.log" 2>&1
  "$PYTHON_BIN" "$RUN_DIR/summarize_faults.py" --output-dir "$out" \
    > "$RUN_DIR/evaluation/$fold/fault_summary.log" 2>&1
  echo "$(date -u +%FT%TZ) VERIFIED_FAULT_SUMMARY $fold" >&2
done
