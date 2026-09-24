# One-seed execution source

These are the scripts used for the fixed J1–J3 experiment. They are copied
unchanged from the run directory before training. `../training_protocol.json`
pins seed 13711, 100 epochs, final-checkpoint scoring, the selected-file
hashes, r4 annotation hashes, and the DCASE2023 Task 2 autoencoder source
hashes. The training/scoring core is the cited upstream DCASE baseline; it is
not duplicated here.

The operational scripts expect the run directory at
`/home/dori/study/asd3dp-dg/runs/24_asd3dp_dg_joint_shifts_h100_20260924`
with a separate baseline copy under `folds/<assignment>/baseline`, a `deps`
environment, and verified datasets under `/home/dori/datasets/asd3dp-dg-joint`.
Copy `../training_protocol.json` to that run directory as `protocol.json`.
Machine-specific paths in the scripts record the actual H100 execution
environment; adapt them when reproducing elsewhere.

`audit_split.py` rereads selected WAVs, labels, annotations and session
membership before training. `train_fold.sh` runs the autoencoder at the fixed
seed and epoch count. `evaluate_fold.py` scores the final checkpoint, and
`summarize_faults.py` reports family/subtype metrics. `verify_results.py`
independently recalculates area-under-curve values from per-file scores after
the run artifacts are returned. The queues only sequence these steps; they
do not select a checkpoint or change the frozen split.
