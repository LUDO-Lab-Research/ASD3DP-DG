#!/usr/bin/env bash
set -euo pipefail
RUN_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
for fold in j1_ab_slow_13_to_c_fast_24 j2_ac_fast_24_to_b_slow_13 j3_bc_slow_12_to_a_fast_34; do
  dataset="/home/dori/datasets/asd3dp-dg-joint/$fold"
  while [[ ! -f "$dataset/DATASET_READY.json" ]]; do sleep 20; done
  echo "$(date -u +%FT%TZ) START $fold" >&2
  "$RUN_DIR/train_fold.sh" "$fold"
  echo "$(date -u +%FT%TZ) FINISHED $fold" >&2
done
