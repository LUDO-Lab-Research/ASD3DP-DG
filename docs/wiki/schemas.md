# Schema and field names

Use the headers and schemas in the [Zenodo release](https://doi.org/10.5281/zenodo.23068430) for exact field names and allowed values.

| Field concept | Interpretation |
|---|---|
| Printer build | A, B, or C |
| Session identifier | Groups material from one recording session |
| Clip identifier | Identifies one temporal interval shared by the four channel files |
| Channel | One microphone view, CH1 through CH4 |
| Source frame interval | Includes the start frame and excludes the end frame |

Check what one row represents, the field's units, and its time origin before joining tables. For example, seconds measured from the session start and seconds measured from the clip start use different origins. Timing brackets describe when an observation was made.

An empty cell, an explicit unknown value, and numeric zero carry different meanings. Use the reviewed activity ranges when interpreting a planned fault. See [Reading the released tables](fields.md) for examples.
