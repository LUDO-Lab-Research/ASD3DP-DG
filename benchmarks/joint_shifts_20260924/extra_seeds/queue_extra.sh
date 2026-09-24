#!/usr/bin/env bash
set -euo pipefail
RUN_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN=/home/dori/project/asd3dp-dg-3d-recon/.venv/bin/python
export PYTHONPATH="$RUN_DIR/deps${PYTHONPATH:+:$PYTHONPATH}"
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MPLBACKEND=Agg
trap 'printf "%s\n" "$?" > "$RUN_DIR/queue.exit"' EXIT
for fold in j1_ab_slow_13_to_c_fast_24 j2_ac_fast_24_to_b_slow_13 j3_bc_slow_12_to_a_fast_34; do
  dataset="/home/dori/datasets/asd3dp-dg-joint/$fold"
  mkdir -p "$RUN_DIR/evaluation/$fold" "$RUN_DIR/logs/$fold"
  if [[ ! -f "$RUN_DIR/evaluation/$fold/audit.json" ]]; then
    python3 "$RUN_DIR/audit_split.py" --fold "$fold" --dataset-root "$dataset" \
      --output "$RUN_DIR/evaluation/$fold/audit.json" \
      > "$RUN_DIR/logs/$fold/audit.log" 2>&1
  fi
  for seed in 13712 13713; do
    output="$RUN_DIR/evaluation/$fold/seed$seed"
    if [[ ! -f "$RUN_DIR/logs/$fold/train_seed$seed.exit" ]]; then
      echo "$(date -u +%FT%TZ) TRAIN $fold seed$seed" >&2
      "$RUN_DIR/train_extra.sh" "$fold" "$seed"
    fi
    [[ "$(cat "$RUN_DIR/logs/$fold/train_seed$seed.exit")" == 0 ]]
    if [[ ! -f "$output/result.json" ]]; then
      echo "$(date -u +%FT%TZ) EVALUATE $fold seed$seed" >&2
      "$PYTHON_BIN" "$RUN_DIR/evaluate_fold.py" --fold "$fold" --seed "$seed" \
        --output-dir "$output" --audit-json "$RUN_DIR/evaluation/$fold/audit.json" \
        > "$RUN_DIR/logs/$fold/evaluate_seed$seed.log" 2>&1
      "$PYTHON_BIN" "$RUN_DIR/summarize_faults.py" --output-dir "$output" \
        > "$RUN_DIR/logs/$fold/fault_seed$seed.log" 2>&1
    fi
    "$PYTHON_BIN" - "$output" <<'PY'
import json,sys
from pathlib import Path
out=Path(sys.argv[1])
assert json.loads((out/'result.json').read_text())['status']=='COMPLETED'
assert json.loads((out/'fault_verification.json').read_text())['status']=='PASS'
PY
    echo "$(date -u +%FT%TZ) COMPLETE $fold seed$seed" >&2
  done
done
