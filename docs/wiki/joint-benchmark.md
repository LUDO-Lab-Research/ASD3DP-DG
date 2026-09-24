# Three-factor joint-shift benchmark

The current ASD3DP-DG benchmark fixes three **joint** changes in printer build,
speed protocol, and microphone position. These factors change together, so a
score difference cannot be attributed to one factor alone.

| Split | Source | Target |
|---|---|---|
| J1 | A+B, Slow, CH1 rear + CH3 front | C, Fast, CH2 left + CH4 right |
| J2 | A+C, Fast, CH2 left + CH4 right | B, Slow, CH1 rear + CH3 front |
| J3 | B+C, Slow, CH1 rear + CH2 left | A, Fast, CH3 front + CH4 right |

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
joint shifts. The planned baseline uses 100 epochs and one fixed seed per split;
results will appear here only after file and run verification.
