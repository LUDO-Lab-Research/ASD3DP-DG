# Schema and field names

The public labeling change affects printer identity values. It does not rename `printer_id`, other CSV columns, JSON keys, tables, or schema definitions. Printer A/B/C identify builds; Belt A/B identify components in each build.

| Field or table | Read it as |
|---|---|
| `printer_id` | Public printer build label A, B, or C |
| `session_id` | Session identifier; join with the supplied session mapping where needed |
| `clip_uid` | Temporal clip identifier shared by its four channel files |
| `channel` | One microphone view, CH1 through CH4 |
| `start_source_frame`, `end_source_frame_exclusive` | Half-open interval in recorder frames |
| `clip_annotations_range.csv` | Intersections of clip windows and source ranges |
| `clip_timeline.csv` | Original and corrected command-time views |

Interpret a field using its table, row grain, units, and time origin. An identically named `start_seconds` value can have a different origin in a session table and a clip table. Source observation brackets are not exact acoustic onset times.

Missing keys, empty CSV cells, the string `unknown`, and numeric zero have different meanings. Do not infer a reviewed label from a planned condition, or infer a fixed interval from a free-form note. Use the schema files and headers shipped with the verified dataset for exact field sets and enums.

For the detailed 28-schema, 393-field dictionary, see [Complete field dictionary](fields.md). Its status labels distinguish stored formats, implemented conditional outputs, and specifications.
