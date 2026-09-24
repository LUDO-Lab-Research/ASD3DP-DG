# Annotation layers

Annotations distinguish collection intent, setup, observed operation, review decisions, clip quality, and released intervals. A planned fault describes the experiment; it does not by itself label every moment of a session.

| Layer | Example artifact | Meaning |
|---|---|---|
| Collection intent | `planned_annotation.json` | Condition and protocol chosen before recording |
| Setup | `setup_measurement_snapshot.json` | Applied belt, fan, or collision settings |
| Runtime | G-code and telemetry | Commands and recorded state observations |
| Session review | `human_annotation.json` | Reviewer decisions and corrections |
| Clip quality | Channel review record | Quality decision for a particular channel clip |
| Release projection | Clip and interval CSVs | Admitted evidence in clip coordinates |

`condition` and `fault_mode` describe different properties. The condition categories are `normal`, `soft-anomaly`, and `hard-anomaly`; these are collection categories, not measured damage severity. Fault modes include belt tension, cooling fan, extruder cogging, and toolhead collision. A print can complete while a fault is present.

`clip_annotations_range.csv` contains within-clip interval projections. `clip_timeline.csv` preserves original command observations alongside corrected command ranges. `clip_gcode.csv` and `clip_telemetry.csv` connect clips to command and state context. Original G-code `;TYPE:` text and normalized labels remain distinguishable. Several operation, belt, and fault ranges may overlap in one clip; aggregate occupancy by interval union within a layer.

The current annotation contract allows unknown or null values where evidence is incomplete. Preserve them instead of converting them to zero or a normal decision. Field names, CSV column order, and schema keys remain as defined in the supplied tables. Printer build labels appear as A, B, and C in public annotation values.

See [Schema and field names](schemas.md) for interpretation and [Time coordinates](timebase.md) for interval origins.
