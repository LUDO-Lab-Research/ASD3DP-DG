# Clip selection

The selected pool contains 11,861 temporal intervals and four mono channel WAVs for each interval. The source recordings also retain preparation, shutdown, pre-roll, and post-roll.

Clips lie on one fixed, non-overlapping grid beginning at recording boundary frame `B`. Each complete grid window contains 480,000 frames, or ten seconds at 48,000 Hz. All four microphones use the same window. Incomplete final windows are excluded. Audio is extracted without recentering, padding, concatenation, resampling, or gain adjustment.

For ordinary printing sessions, a selected clip must lie wholly inside the admitted operation interval. Collision sessions use their protocol's printing-motion phase. The operation interval is based on observed boundaries and conservative corrected command timing; [Time coordinates](timebase.md) explains the latter. A slicer `Custom` label by itself does not mean an interval is excluded.

| Session family | Additional admission rule |
|---|---|
| Normal | Admitted operation interval; exported fault overlap is zero |
| Belt A, Belt B, or both | At least three seconds of relevant belt activity within the clip |
| Fan blade damage | At least three seconds of observed fan activity |
| Extruder cogging | At least three seconds of observed extruder activity |
| Toolhead collision | An audio RMS event overlaps by at least 0.1 second, or a shorter event lies wholly inside the clip |

For sustained faults, eligible activity is an interval union, so overlap need not be continuous and overlapping intervals are not double-counted. Inactive regions of an anomaly session are not automatically relabeled normal. Collision event cores use four-channel RMS; display padding does not extend the admission interval.

The clip candidate table contains 14,142 complete grid windows. Of these, 354 were outside admitted operation and 1,927 did not meet fault-overlap policy, leaving 11,861 selected windows. The source grid index is retained across exclusions.
