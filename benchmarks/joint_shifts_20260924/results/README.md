# Verified joint-shift results

These are the completed J1–J3 tests defined in the [frozen selection](../README.md).
Printer build, speed protocol, and microphone pair change together; no row
estimates an isolated factor effect. Each assignment trained one autoencoder
for 100 epochs on 990 source-normal and 10 target-normal mono files. The final
checkpoint was evaluated on 100 normal and 100 anomalous files in each domain.
Each domain's anomalies contain 25 files per Belt, Extruder, Fan, and Collision
family. No test score was used to choose a checkpoint or scoring method.

| Split | Score | Source AUC | Target AUC | Pooled pAUC | Belt target AUC | Extruder target AUC | Fan target AUC | Collision target AUC |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| J1 | MSE | 92.97 | 64.86 | 78.68 | 43.12 | 50.08 | 66.24 | 100.00 |
| J1 | Mahalanobis | 91.42 | 92.86 | 80.18 | 80.10 | 93.70 | 97.62 | 100.00 |
| J2 | MSE | 96.84 | 92.39 | 87.43 | 73.54 | 96.14 | 99.88 | 100.00 |
| J2 | Mahalanobis | 98.11 | 88.14 | 82.47 | 63.74 | 90.18 | 98.64 | 100.00 |
| J3 | MSE | 95.36 | 95.49 | 86.86 | 89.50 | 95.78 | 96.70 | 100.00 |
| J3 | Mahalanobis | 98.47 | 91.44 | 82.78 | 79.40 | 91.34 | 95.02 | 100.00 |

All values are percentages from **one trained model per split**. Source and
Target AUC compare normal files from the named domain against anomalies pooled
from both domains, following the DCASE evaluator. Family columns use the same
100 target-normal files against that family's 50 anomalies (25 per domain).
Pooled pAUC uses all 400 test files and maximum false-positive rate 0.1.
The Mahalanobis label denotes the pinned baseline's source/target residual-
covariance scoring rule; MSE and Mahalanobis score the same checkpoint.

The selected collision files score above every target-normal file for both
scoring methods in all three assignments. These command-linked impact events
are plausible strong acoustic cues, but the 100% values describe only this
selected test population. Belt and extruder results vary substantially by
assignment and scoring rule. Because the assignments share some audio files
and each was trained once, these six rows are neither independent replications
nor an estimate of seed or session-sampling uncertainty.

The [local verification receipt](LOCAL_RESULTS_VERIFIED.json) records a PASS
for every assignment: 400 score rows were joined to frozen selected-file IDs,
audio SHA-256, labels, printer domains, sessions and channels; AUC and pAUC
were independently recomputed from [`file_scores.csv`](j1_ab_slow_13_to_c_fast_24/seed13711/file_scores.csv).
Each fold directory also contains its original evaluation JSON, split audit,
family metrics, verification JSON, and epoch-100 checkpoint. [Model SHA-256
values](MODEL_SHA256.json) match the retained checkpoints on the training host.
Full audio remains outside Git; its selections and processing code are in this
repository.
