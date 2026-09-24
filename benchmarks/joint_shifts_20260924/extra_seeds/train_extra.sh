#!/usr/bin/env bash
set -euo pipefail
RUN_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
FOLD="${1:?fold required}"
SEED="${2:?seed required}"
case "$FOLD" in j1_ab_slow_13_to_c_fast_24|j2_ac_fast_24_to_b_slow_13|j3_bc_slow_12_to_a_fast_34) ;; *) echo "invalid fold" >&2; exit 2;; esac
case "$SEED" in 13712|13713) ;; *) echo "invalid additional seed" >&2; exit 2;; esac
BASE="$RUN_DIR/folds/$FOLD/baseline"
DATA="/home/dori/datasets/asd3dp-dg-joint/$FOLD"
PYTHON_BIN=/home/dori/project/asd3dp-dg-3d-recon/.venv/bin/python
EXPORT="asd3dp_dg_joint_${FOLD}"
MODEL="DCASE2023T2-AE_DCASE2023T23DPrinter_seed${SEED}"
[[ -f "$RUN_DIR/evaluation/$FOLD/audit.json" ]] || { echo "split audit missing" >&2; exit 1; }
if [[ -e "$BASE/models/checkpoint/$EXPORT/$MODEL/checkpoint.tar" ]]; then
  echo "checkpoint exists; refusing overwrite" >&2; exit 1
fi
mkdir -p "$RUN_DIR/logs/$FOLD"
export PYTHONPATH="$RUN_DIR/deps${PYTHONPATH:+:$PYTHONPATH}"
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
export MPLBACKEND=Agg PYTHONUNBUFFERED=1 CUBLAS_WORKSPACE_CONFIG=:4096:8
cd "$BASE"
set +e
"$PYTHON_BIN" "$RUN_DIR/train_no_anomaly_debug.py" \
  --dataset DCASE2023T23DPrinter --dev --train_only \
  --dataset_directory ./data --export_dir "$EXPORT" \
  --result_directory ./results --mono True --is_auto_download False \
  --use_ids 0 --seed "$SEED" --epochs 100 --batch_size 256 \
  --n_mels 128 --frames 5 --n_fft 1024 --hop_length 512 \
  --learning_rate 0.001 --validation_split 0.1 \
  > "$RUN_DIR/logs/$FOLD/train_seed${SEED}.log" 2>&1
STATUS=$?
set -e
printf '%s\n' "$STATUS" > "$RUN_DIR/logs/$FOLD/train_seed${SEED}.exit"
exit "$STATUS"
