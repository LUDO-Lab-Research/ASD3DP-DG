# Approved three-factor joint shifts (annotation r4)

This protocol fixes **three joint shifts**. Printer build, printing-speed protocol,
and microphone position all change together. The experiment does not estimate
the separate causal effect of any one factor. The earlier printer-only rotations
are retained as historical runs and are not the results for this protocol.

| Assignment | Source training/evaluation domain | Target training/evaluation domain |
|---|---|---|
| J1 | Printers A+B, Slow, CH1 rear + CH3 front | Printer C, Fast, CH2 left + CH4 right |
| J2 | Printers A+C, Fast, CH2 left + CH4 right | Printer B, Slow, CH1 rear + CH3 front |
| J3 | Printers B+C, Slow, CH1 rear + CH2 left | Printer A, Fast, CH3 front + CH4 right |

Each assignment uses 990 source-normal and 10 target-normal **mono files** for
training. The two source printers contribute 495 files each. The test has 100
normal and 100 anomaly files in **each** domain. Each domain has 25 belt, 25
extruder, 25 fan, and 25 collision anomalies; belt A/B/A+B contribute 9/8/8
and each of the five collision directions contributes 5. Source test files are
balanced 50:50 between its two printers. Within each partition/domain, the two
permitted channels have equal file counts.

Normal training files come from normal repetitions 1 and 2; normal test files
come from repetition 3. Anomaly test files come from separate fault sessions.
This keeps training and test sessions disjoint. Two channel views of one ten-second
interval may both appear **within training**, so 990 files are not 990 independent
temporal events. No temporal interval or audio hash crosses train and test.
All selected files retain the original 10-second r4 frame boundaries; there is
no new clipping, resampling, recentering, or noise synthesis.

`build_selection.py` uses the fixed selection seed 20260924 and source metadata
hashes. Each `selections/<assignment>/recipe.json` records the exact selection
SHA-256 and domain rule; `selected_samples.csv` records every file and its
original WAV SHA-256. `materialize.py` copies selected WAVs, re-reads their
hashes and PCM shape, and exports their r4 G-code, telemetry, timeline, and
range annotations. The four source annotation tables are rehashed against
the r4 metadata manifest, whose digest is frozen in the training protocol.
A completed dataset has `DATASET_READY.json` with status
`VERIFIED_JOINT_SHIFT_SUBSET` and `SHA256SUMS`.

[`training_protocol.json`](training_protocol.json) freezes the three selection
hashes, 100-epoch final-checkpoint rule, seed 13711, and the source-code hashes
of the training/scoring baseline. The completed [results and independently
verified file scores](results/README.md) are published separately from this
selection protocol.
[The run scripts](runner/README.md) record the split audit, one-seed training,
final-checkpoint scoring, fault-family summary, and independent result check.

Training and test use the same DCASE2023 Task 2 autoencoder/scoring code and
hyperparameters as the historical baseline, with **100 epochs and one fixed
seed (13711) per assignment**. The final epoch is scored; no test set chooses a
checkpoint or hyperparameter. Report source/target AUC and pooled pAUC for
MSE and Mahalanobis, with fault-family breakdowns. One seed gives a
single-run result, not a variability estimate. File membership may recur
across assignments; assignments are analyzed separately.

Source release: ASD3DP-DG annotation `r4-20260924`, 11,861 ten-second temporal
clips and 47,444 channel files. The source release and its selected WAV hashes
remain authoritative. See [clip selection](../../docs/wiki/selection.md) and
[time coordinates](../../docs/wiki/timebase.md).
