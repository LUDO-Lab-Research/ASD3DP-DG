#!/usr/bin/env bash
set -euo pipefail
RUN_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN=/home/dori/project/asd3dp-dg-3d-recon/.venv/bin/python
export PYTHONPATH="$RUN_DIR/deps${PYTHONPATH:+:$PYTHONPATH}"
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MPLBACKEND=Agg
trap 'printf "%s\n" "$?" > "$RUN_DIR/helper.exit"' EXIT
for fold in j2_ac_fast_24_to_b_slow_13 j3_bc_slow_12_to_a_fast_34; do
  seed=13712
  dataset="/home/dori/datasets/asd3dp-dg-joint/$fold"
  output="$RUN_DIR/evaluation/$fold/seed$seed"
  mkdir -p "$RUN_DIR/evaluation/$fold" "$RUN_DIR/logs/$fold"
  if [[ ! -f "$RUN_DIR/evaluation/$fold/audit.json" ]]; then
    python3 "$RUN_DIR/audit_split.py" --fold "$fold" --dataset-root "$dataset" \
      --output "$RUN_DIR/evaluation/$fold/audit.json" \
      > "$RUN_DIR/logs/$fold/audit.log" 2>&1
  fi
  echo "$(date -u +%FT%TZ) HELPER TRAIN $fold seed$seed" >&2
  "$RUN_DIR/train_extra.sh" "$fold" "$seed"
  [[ "$(cat "$RUN_DIR/logs/$fold/train_seed$seed.exit")" == 0 ]]
  echo "$(date -u +%FT%TZ) HELPER EVALUATE $fold seed$seed" >&2
  "$PYTHON_BIN" "$RUN_DIR/evaluate_fold.py" --fold "$fold" --seed "$seed" \
    --output-dir "$output" --audit-json "$RUN_DIR/evaluation/$fold/audit.json" \
    > "$RUN_DIR/logs/$fold/evaluate_seed$seed.log" 2>&1
  "$PYTHON_BIN" "$RUN_DIR/summarize_faults.py" --output-dir "$output" \
    > "$RUN_DIR/logs/$fold/fault_seed$seed.log" 2>&1
  "$PYTHON_BIN" - "$output" <<'PY'
import json,sys
from pathlib import Path
out=Path(sys.argv[1])
assert json.loads((out/'result.json').read_text())['status']=='COMPLETED'
assert json.loads((out/'fault_verification.json').read_text())['status']=='PASS'
PY
  echo "$(date -u +%FT%TZ) HELPER COMPLETE $fold seed$seed" >&2
done
