# Interpretation limits

The three printer domains differ in builds and assembly. A difference between domains cannot be attributed to one component without a separate controlled experiment.

The slow and fast categories name source G-code program families. Commanded feedrates are not direct measurements of attained toolhead speed. Microphone direction labels do not provide microphone distance or angle measurements.

Belt displacement readings describe a manual intervention, not calibrated belt tension. Fan damage is recorded as an applied setup, not a measured acoustic severity. The extruder condition also changes filament loading relative to the no-filament normal protocol, so a model-score difference does not isolate cogging alone.

Command-to-sound correction uses one timing offset per session. It helps align command context with audio but is not a direct timestamp for every physical action. Overlapping within-clip ranges can sum to more than a clip duration; use interval unions for occupancy. Unknown or unreviewed values must remain distinguishable from normal labels.

The dataset is a research release for DCASE Task 2-style evaluation. It is not an official DCASE-organized dataset or benchmark.
