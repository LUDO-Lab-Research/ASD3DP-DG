# Three-factor joint-shift benchmark

The current ASD3DP-DG benchmark fixes three **joint** changes in printer build,
speed protocol, and microphone position. These factors change together, so a
score difference cannot be attributed to one factor alone.

Printer labels A, B, and C denote distinct builds. Slow/Fast are G-code
program families, not fixed attained head speeds; ordinary commanded feedrates
reach 12,000/30,000 mm/min, respectively. CH1/CH2/CH3/CH4 are rear/left/front/right
microphones, as defined in [Collection](collection.md).

| Split | Factor | Source | Target |
|---|---|---|---|
| J1 | Printer | A+B | C |
|  | Speed program | Slow | Fast |
|  | Microphones | CH1+CH3 | CH2+CH4 |
| J2 | Printer | A+C | B |
|  | Speed program | Fast | Slow |
|  | Microphones | CH2+CH4 | CH1+CH3 |
| J3 | Printer | B+C | A |
|  | Speed program | Slow | Fast |
|  | Microphones | CH1+CH2 | CH3+CH4 |
| All splits | Train normal files | 990 | 10 |
|  | Test normal files | 100 | 100 |
|  | Test anomaly files | 100 | 100 |

In **each** split, training has 990 source-normal and 10 target-normal mono
files. The two source printers contribute 495 files each. Evaluation has 100
normal and 100 anomaly files in each domain. Each domain's 100 anomalies
contain 25 belt, 25 extruder, 25 fan, and 25 collision files. The source
test's two printers contribute 50 files each for normal and anomaly labels;
the permitted channel pair is balanced within each partition/domain.

Normal repetitions 1 and 2 supply training; repetition 3 supplies normal
evaluation. Fault sessions supply anomaly evaluation. Thus train/test sessions
are disjoint. Two microphones can provide two **training files** from the same
ten-second source interval; they are correlated views, not independent events.
No source interval crosses training and evaluation. The benchmark uses the
unchanged r4 clip boundaries and original mono PCM files.

The [frozen recipes, selected-sample CSVs, and builder](../../benchmarks/joint_shifts_20260924/README.md)
record exact file membership and source hashes. The earlier printer-only
rotations are separate historical experiments and are not evidence for these
joint shifts. The completed baseline uses 100 epochs and one fixed seed per
split; [file scores, checkpoints, and verification receipts](../../benchmarks/joint_shifts_20260924/results/README.md)
are available with the frozen selection.

| Split | Score | Source AUC | Target AUC | Pooled pAUC | Belt | Extruder | Fan | Collision |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| J1 | MSE | 92.97 | 64.86 | 78.68 | 43.12 | 50.08 | 66.24 | 100.00 |
| J1 | Mahalanobis | 91.42 | 92.86 | 80.18 | 80.10 | 93.70 | 97.62 | 100.00 |
| J2 | MSE | 96.84 | 92.39 | 87.43 | 73.54 | 96.14 | 99.88 | 100.00 |
| J2 | Mahalanobis | 98.11 | 88.14 | 82.47 | 63.74 | 90.18 | 98.64 | 100.00 |
| J3 | MSE | 95.36 | 95.49 | 86.86 | 89.50 | 95.78 | 96.70 | 100.00 |
| J3 | Mahalanobis | 98.47 | 91.44 | 82.78 | 79.40 | 91.34 | 95.02 | 100.00 |

Values are percentages from one completed training run per split. Source and
Target AUC use normal files from the named domain against anomalies pooled
across domains; fault-family columns are Target AUC against 50 anomalies per
family. Pooled pAUC uses all 400 test files and maximum false-positive rate
0.1. The 100% collision values describe these selected command-linked impacts,
not unseen collisions or an independent factor effect.
