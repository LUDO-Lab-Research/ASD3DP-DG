# ASD3DP-DG field dictionary

Current stored annotations, executable review contracts, setup/G-code keys observed across 78 sessions, conditional/automatic candidates and final output specifications are distinguished below. Dotted names denote JSON object paths; `[]` denotes one array item. Arbitrary printer-configuration values and free-form notes are not fixed annotation sub-schemas.

**28 schemas · 393 schema-field occurrences**. Identical names may have different time origins or row grain; read the applicable table. See the [Schema map](schemas.md).

## audio_clip_manifest

File/API: `bundle/clips/audio_clip_manifest.csv` · Row grain: **clip × channel** · Status: **current**

Resolve path relative to bundle/clips/. frame_count is 480000 frames in the channel WAV.

**Join:** clip_uid → clip_plan; four rows, channels 1–4, per temporal clip. Paths are relative to bundle/clips.

**Time:** Decisions/settings without time fields inherit the linked session/clip coordinates. Updated/completed Unix times describe revision history, not audio onset.

**Missing values:** Missing keys and empty values follow the source contract. Do not convert unknown/needs_review to a normal decision or zero.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `clip_uid` | string / source-defined | identifier | Identifier of a shared temporal clip, common to all channels. |
| `channel` | DG: integer 1–4; legacy: ch1–ch4 | channel | Microphone channel: legacy uses values such as ch1; DG uses 1–4. |
| `path` | string / source-defined | path | Relative artifact path interpreted from the applicable manifest. |
| `frame_count` | integer (CSV: text) | frames | Number of frames in the target audio. |
| `sha256` | string / source-defined | SHA-256 | SHA-256 of the artifact referenced by this manifest. |

## clip_event_annotations

File/API: `bundle/clips/clip_event_annotations.csv` · Row grain: **clip** · Status: **current**

Preserve planned values, unknown anomaly_state, needs_review and an empty fault_interval_id.

**Join:** clip_uid → the shared temporal clip in clip_plan. Shared provisional annotation without a channel column.

**Time:** Decisions/settings without time fields inherit the linked session/clip coordinates. Updated/completed Unix times describe revision history, not audio onset.

**Missing values:** Missing keys and empty values follow the source contract. Do not convert unknown/needs_review to a normal decision or zero.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `clip_uid` | string / source-defined | identifier | Identifier of a shared temporal clip, common to all channels. |
| `condition` | string / source-defined | category | Collection or reviewed condition: normal/soft-anomaly/hard-anomaly; distinguish planned from human authority. |
| `fault_mode` | string / source-defined | category | Fault family: none or a belt/fan/extruder/collision value defined by the contract. |
| `anomaly_state` | string / source-defined | category | Automatic clip-annotation anomaly state; unknown in the collection output. |
| `annotation_authority` | string / source-defined | category | Kind of evidence used to determine or generate this value or interval. |
| `review_state` | string / source-defined | category | Review state for this schema; session, clip and legacy vocabularies differ. |
| `fault_interval_id` | string / source-defined | identifier | Original fault interval linked to this clip; empty in automatic collection tables. |

## clip_gcode

File/API: `bundle/clips/clip_gcode.csv` · Row grain: **clip × source observation** · Status: **current**

Observation-bracket/command join, not the command's actual execution interval.

**Join:** clip_uid → clip_plan; multiple source/marker brackets may join one clip. evidence_type distinguishes row kinds.

**Time:** source_frame_lower/upper are host-observed brackets. Do not directly use sample_index, line or Moonraker eventtime as WAV seconds. Units follow the registry/parent source.

**Missing values:** Missing keys and empty values follow the source contract. Do not convert unknown/needs_review to a normal decision or zero.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `clip_uid` | string / source-defined | identifier | Identifier of a shared temporal clip, common to all channels. |
| `evidence_type` | string / source-defined | category | Kind of G-code/marker evidence linked to the clip. |
| `command_order` | integer (CSV: text) | index | Linked command order; the current writer retains the source-line value. |
| `line` | integer (CSV: text) | index | Observed source line number. |
| `byte_start` | integer (CSV: text) | bytes | Starting byte offset of the original source line. |
| `byte_end_exclusive` | integer (CSV: text) | bytes | Exclusive ending byte offset of the original source line. |
| `command` | string / source-defined | text | Retained source line or command string. |
| `kind` | string / source-defined | category | Marker/event kind. |
| `phase_event` | string / source-defined | category | Typed phase marker, such as PRINTING_MOTION_BEGIN/END. |
| `anchor_id` | string / source-defined | identifier | Instrumentation anchor identifier. |
| `source_frame_lower` | integer (CSV: text) | frames | Lower host-observed source-frame bracket bound. |
| `source_frame_upper` | integer (CSV: text) | frames | Upper host-observed source-frame bracket bound. |
| `host_observed_frame_lower` | integer (CSV: text) | frames | Lower bound of the host-observed source-frame bracket. |
| `host_observed_frame_upper` | integer (CSV: text) | frames | Upper bound of the host-observed source-frame bracket. |
| `width_frames` | integer (CSV: text) | frames | Observation bracket upper minus lower; not a physical acoustic-error bound. |
| `result` | string / source-defined | category | Original marker/G-code observation result. |

## clip_plan

File/API: `bundle/clips/clip_plan.csv` · Row grain: **clip** · Status: **current**

start_seconds/end_seconds are recording-boundary-relative seconds. end_source_frame_exclusive is the half-open interval end.

**Join:** session_id+run_id link recorder/run evidence. clip_uid is the parent key for channel files and range tables.

**Time:** Source frames use the shared recorder coordinates. start_seconds/end_seconds are relative to recording start_boundary_frame and may differ from WAV-relative seconds by pre-roll.

**Missing values:** Missing keys and empty values follow the source contract. Do not convert unknown/needs_review to a normal decision or zero.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `clip_uid` | string / source-defined | identifier | Identifier of a shared temporal clip, common to all channels. |
| `session_id` | string / source-defined | identifier | Current collector session identifier. |
| `run_id` | string / source-defined | identifier | Execution-envelope identifier linked to the session. |
| `grid_index` | integer (CSV: text) | index | Integer index on the original fixed grid; excluded indices are not renumbered. |
| `start_source_frame` | integer (CSV: text) | frames | Starting source frame of the interval. |
| `end_source_frame_exclusive` | integer (CSV: text) | frames | End of the source interval; this frame is excluded. |
| `start_seconds` | number (CSV: text) | s | Start of the interval. Interpret time origins using this file's timing_basis and session timing table. |
| `end_seconds` | number (CSV: text) | s | End of the interval. Interpret time origins using this file's timing_basis and session timing table. |
| `duration_seconds` | number (CSV: text) | s | Duration of the row interval. Interpret time origins using this file's timing_basis and session timing table. |
| `selection_rule` | string / source-defined | text | Identifier/description of the clip-selection rule. |

## clip_telemetry

File/API: `bundle/clips/clip_telemetry.csv` · Row grain: **clip × telemetry sample** · Status: **current**

values_json contains the registry's 14 selected values. sample_index joins raw cursor evidence.

**Join:** clip_uid → clip_plan; sample_index → raw telemetry/cursor within the same session. Never directly join sample_index across sessions.

**Time:** source_frame_lower/upper are host-observed brackets. Do not directly use sample_index, line or Moonraker eventtime as WAV seconds. Units follow the registry/parent source.

**Missing values:** Missing keys and empty values follow the source contract. Do not convert unknown/needs_review to a normal decision or zero.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `clip_uid` | string / source-defined | identifier | Identifier of a shared temporal clip, common to all channels. |
| `sample_index` | integer (CSV: text) | index | Index joining corresponding telemetry and recorder-cursor samples. |
| `source_frame_lower` | integer (CSV: text) | frames | Lower host-observed source-frame bracket bound. |
| `source_frame_upper` | integer (CSV: text) | frames | Upper host-observed source-frame bracket bound. |
| `moonraker_eventtime` | number (CSV: text) | s, source clock | Original Moonraker observation clock; do not use directly as WAV-relative seconds. |
| `values_json` | JSON object/string as specified | JSON | Telemetry values by registry path serialized as JSON in a CSV cell. |

## human_annotation_input

File/API: `human_annotation.json: annotation` · Row grain: **session revision** · Status: **current**

schema_version is asd3dp-dg-annotation-v1. All three nullable extension keys remain mandatory. Required strings other than summary/note cannot be empty.

**Join:** The stored envelope's annotation object. expected_revision belongs to the POST wrapper, not this object.

**Time:** Decisions/settings without time fields inherit the linked session/clip coordinates. Updated/completed Unix times describe revision history, not audio onset.

**Missing values:** All 21 keys are required. annotation_confidence/environment_change/operator_intervention may be null. Required strings other than summary/note cannot be empty.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `schema_version` | schema-specific string or integer | version | File/input format version; string or numeric representation depends on the schema. |
| `condition` | string / source-defined | category | Collection or reviewed condition: normal/soft-anomaly/hard-anomaly; distinguish planned from human authority. Allowed values: hard-anomaly, normal, soft-anomaly |
| `fault_mode` | string / source-defined | category | Fault family: none or a belt/fan/extruder/collision value defined by the contract. Allowed values: belt_tension_abnormal, cooling_fan_fault, extruder_cogging_or_no_extrusion, none, toolhead_collision |
| `affected_part` | string / source-defined | category | Component targeted by this condition. |
| `fault_origin` | string / source-defined | category | How the fault arose or was applied; preserve original values such as controlled, simulated or none. |
| `protocol_axis` | string / source-defined | category | Collection-protocol identifier. |
| `filament_state` | string / source-defined | category | Filament loading/use state; do not arbitrarily replace unknown. |
| `speed_profile` | string / source-defined | category | Session-level protocol such as slow/fast, not instantaneous velocity. |
| `print_outcome` | string / source-defined | category | Run outcome: completed/cancelled/error/unknown. Allowed values: cancelled, completed, error, unknown |
| `process_state` | string / source-defined | category | Operation phase/state, on a different axis from fault state. Allowed values: homing, idle, paused, printing_motion, terminal |
| `anomaly_progress_state` | string / source-defined | category | Anomaly progression: none/candidate/active/resolved/unknown. Allowed values: active, candidate, none, resolved, unknown |
| `condition_source_type` | string / source-defined | category | Source category for the condition decision. |
| `condition_summary` | string / source-defined | text | Human-readable description of the condition. |
| `material_family` | string / source-defined | category | Material family; preserve unknown where information is absent. |
| `reviewer_id` | string / source-defined | identifier | Value identifying the reviewer. |
| `review_state` | string / source-defined | category | Review state for this schema; session, clip and legacy vocabularies differ. Allowed values: accepted, rejected, reviewed, unreviewed |
| `operator_note` | string / source-defined | text | Reviewer's explanation; empty-value rules depend on the contract. |
| `annotation_authority` | string / source-defined | category | Kind of evidence used to determine or generate this value or interval. |
| `annotation_confidence` | null / JSON scalar / object / array | nullable JSON | Nullable confidence with its scale and meaning recorded; no universal score is imposed. |
| `environment_change` | null / JSON scalar / object / array | nullable JSON | Nullable free-form environmental-change record; no source-interval structure is implied. |
| `operator_intervention` | null / JSON scalar / object / array | nullable JSON | Nullable free-form operator-intervention record; retain evidence for the intervention time. |

## human_annotation_envelope

File/API: `annotations/<session>/human_annotation.json` · Row grain: **session revision** · Status: **current**

schema_version is 1 for legacy notes and 2 for structured records; interpret with annotation_contract.

**Join:** session_id and run_id/hash link the source. revision/previous_revision track edits; annotation contains decision input.

**Time:** Decisions/settings without time fields inherit the linked session/clip coordinates. Updated/completed Unix times describe revision history, not audio onset.

**Missing values:** Missing keys and empty values follow the source contract. Do not convert unknown/needs_review to a normal decision or zero.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `schema_version` | schema-specific string or integer | version | File/input format version; string or numeric representation depends on the schema. |
| `annotation_contract` | string / source-defined | version | Annotation contract name used by the stored envelope. |
| `session_id` | string / source-defined | identifier | Current collector session identifier. |
| `human_note` | string / source-defined | text | Human note retained in a legacy or structured annotation. |
| `note_state` | string / source-defined | category | Whether the human note is present or empty. |
| `review_state` | string / source-defined | category | Review state for this schema; session, clip and legacy vocabularies differ. |
| `annotation` | JSON object/string as specified | JSON | Structured session-annotation object; null for a legacy note-only record. |
| `run_id` | string / source-defined | identifier | Execution-envelope identifier linked to the session. |
| `run_manifest_sha256` | string / source-defined | SHA-256 | SHA-256 of the run manifest. |
| `annotation_preset_id` | string / source-defined | identifier | Preset identifier used for the recording plan. |
| `annotation_preset_revision` | schema-specific string or integer | version | Revision number of that preset. |
| `planned_annotation_sha256` | string / source-defined | SHA-256 | SHA-256 of the planned annotation. |
| `planned_to_actual_corrections` | JSON object/string as specified | JSON | Differences between planned values and actual values saved by a person. |
| `planning_provenance` | string / source-defined | category | Planning provenance state, such as PRESET_STAMPED/LEGACY_NO_PRESET. |
| `updated_unix_ns` | integer (CSV: text) | ns since Unix epoch | Unix-epoch timestamp of the revision save, not audio onset. |
| `revision` | string / source-defined | version | Revision identifier/hash binding the current saved values and their provenance. |
| `previous_revision` | string / source-defined | version | Previous saved revision identifier; may be null on first save. |
| `recorder_manifest_sha256` | string / source-defined | SHA-256 | SHA-256 of the recorder manifest. |

## clip_quality_review

File/API: `clip-reviews/<clip>/chN.json` · Row grain: **clip × channel revision** · Status: **current**

Verdict/issue vocabulary differs from session review_state. The decision is bound to this channel's bytes.

**Join:** clip_uid+channel_id identify the audio; clip_audio_sha256 binds its bytes. Also retain bundle_manifest_sha256.

**Time:** Decisions/settings without time fields inherit the linked session/clip coordinates. Updated/completed Unix times describe revision history, not audio onset.

**Missing values:** Missing keys and empty values follow the source contract. Do not convert unknown/needs_review to a normal decision or zero.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `schema_version` | schema-specific string or integer | version | File/input format version; string or numeric representation depends on the schema. |
| `clip_uid` | string / source-defined | identifier | Identifier of a shared temporal clip, common to all channels. |
| `session_id` | string / source-defined | identifier | Current collector session identifier. |
| `channel_id` | DG: integer 1–4; legacy: ch1–ch4 | channel | Channel identifier; its format follows the file schema. |
| `reviewer_id` | string / source-defined | identifier | Value identifying the reviewer. |
| `verdict` | string / source-defined | category | Channel-quality decision: accepted/flagged. |
| `issues` | string / source-defined | categories | Channel-quality issues: clipping/sync/truncation/background_noise/other. |
| `note` | string / source-defined | text | Note value retained from the original record. |
| `authority` | string / source-defined | category | Evidence-record kind, such as planned/setup/human. |
| `clip_audio_sha256` | string / source-defined | SHA-256 | SHA-256 of this channel's clip WAV. |
| `bundle_manifest_sha256` | string / source-defined | SHA-256 | SHA-256 of the bundle manifest. |
| `start_source_frame` | integer (CSV: text) | frames | Starting source frame of the interval. |
| `end_source_frame_exclusive` | integer (CSV: text) | frames | End of the source interval; this frame is excluded. |
| `previous_revision` | string / source-defined | version | Previous saved revision identifier; may be null on first save. |
| `updated_unix_ns` | integer (CSV: text) | ns since Unix epoch | Unix-epoch timestamp of the revision save, not audio onset. |
| `revision` | string / source-defined | version | Revision identifier/hash binding the current saved values and their provenance. |

## clip_quality_request

File/API: `clip quality API request` · Row grain: **clip × channel revision** · Status: **current**

expected_revision must match. Accepted clips must have no issues.

**Join:** The URL's clip/channel and expected_revision identify the target. Do not infer the source session from the request body alone.

**Time:** Decisions/settings without time fields inherit the linked session/clip coordinates. Updated/completed Unix times describe revision history, not audio onset.

**Missing values:** Missing keys and empty values follow the source contract. Do not convert unknown/needs_review to a normal decision or zero.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `expected_revision` | string / source-defined | version | Current revision on which the edit request is based; a mismatch causes a conflict. |
| `reviewer_id` | string / source-defined | identifier | Value identifying the reviewer. |
| `verdict` | string / source-defined | category | Channel-quality decision: accepted/flagged. |
| `issues` | string / source-defined | categories | Channel-quality issues: clipping/sync/truncation/background_noise/other. |
| `note` | string / source-defined | text | Note value retained from the original record. |

## planned_annotation

File/API: `bundle/run/planned_annotation.json` · Row grain: **session planned snapshot** · Status: **current**

Defaults carry planned authority and are separate from review input.

**Join:** Frozen run snapshot. Defaults record conditions; preset/BOM/capture-hardware hashes retain planning evidence.

**Time:** Decisions/settings without time fields inherit the linked session/clip coordinates. Updated/completed Unix times describe revision history, not audio onset.

**Missing values:** Missing keys and empty values follow the source contract. Do not convert unknown/needs_review to a normal decision or zero.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `annotation_preset_id` | string / source-defined | identifier | Preset identifier used for the recording plan. |
| `annotation_preset_revision` | schema-specific string or integer | version | Revision number of that preset. |
| `authority` | string / source-defined | category | Evidence-record kind, such as planned/setup/human. |
| `bom_sha256` | string / source-defined | SHA-256 | SHA-256 of the BOM snapshot. |
| `capture_hardware_sha256` | string / source-defined | SHA-256 | SHA-256 of the capture-hardware profile. |
| `defaults` | JSON object/string as specified | JSON | Planned annotation values copied from the preset. |
| `preset_sha256` | string / source-defined | SHA-256 | SHA-256 of the preset content. |
| `review_state` | string / source-defined | category | Review state for this schema; session, clip and legacy vocabularies differ. |
| `schema_version` | schema-specific string or integer | version | File/input format version; string or numeric representation depends on the schema. |

## planned_defaults

File/API: `bundle/run/planned_annotation.json: defaults` · Row grain: **session planned snapshot** · Status: **current**

Compare expected_anomaly_progress_state with the subsequent actual anomaly_progress_state.

**Join:** The planned_annotation.defaults object. Compare with human actual values; do not use directly as benchmark labels.

**Time:** Decisions/settings without time fields inherit the linked session/clip coordinates. Updated/completed Unix times describe revision history, not audio onset.

**Missing values:** Missing keys and empty values follow the source contract. Do not convert unknown/needs_review to a normal decision or zero.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `affected_part` | string / source-defined | category | Component targeted by this condition. |
| `condition` | string / source-defined | category | Collection or reviewed condition: normal/soft-anomaly/hard-anomaly; distinguish planned from human authority. |
| `condition_summary` | string / source-defined | text | Human-readable description of the condition. |
| `expected_anomaly_progress_state` | string / source-defined | category | Anomaly progression expected by the planned preset, distinct from actual judgment. |
| `fault_mode` | string / source-defined | category | Fault family: none or a belt/fan/extruder/collision value defined by the contract. |
| `fault_origin` | string / source-defined | category | How the fault arose or was applied; preserve original values such as controlled, simulated or none. |
| `filament_state` | string / source-defined | category | Filament loading/use state; do not arbitrarily replace unknown. |
| `material_family` | string / source-defined | category | Material family; preserve unknown where information is absent. |
| `protocol_axis` | string / source-defined | category | Collection-protocol identifier. |
| `speed_profile` | string / source-defined | category | Session-level protocol such as slow/fast, not instantaneous velocity. |

## telemetry_values

File/API: `telemetry_samples.jsonl: values` · Row grain: **sample** · Status: **current**

Fourteen paths read from the actual registry. Missing values are not zero.

**Join:** Dotted path keys in telemetry_sample.values; join exactly to metadata registry paths.

**Time:** source_frame_lower/upper are host-observed brackets. Do not directly use sample_index, line or Moonraker eventtime as WAV seconds. Units follow the registry/parent source.

**Missing values:** Missing keys and empty values follow the source contract. Do not convert unknown/needs_review to a normal decision or zero.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `toolhead.position` | number array | mm[3] | Reported toolhead XYZ coordinates. |
| `toolhead.homed_axes` | string / source-defined | state | String of homed axes. |
| `motion_report.live_position` | number array | mm[4] | Reported live XYZE coordinates. |
| `motion_report.live_velocity` | number (CSV: text) | mm/s | Reported live head velocity. |
| `motion_report.live_extruder_velocity` | number (CSV: text) | mm/s | Reported live extruder velocity. |
| `extruder.temperature` | number (CSV: text) | °C | Extruder/nozzle temperature. |
| `extruder.target` | number (CSV: text) | °C | Extruder target temperature. |
| `extruder.power` | number (CSV: text) | ratio | Reported extruder-heater power. |
| `heater_bed.temperature` | number (CSV: text) | °C | Bed temperature reported through telemetry. |
| `heater_bed.target` | number (CSV: text) | °C | Bed target temperature. |
| `heater_bed.power` | number (CSV: text) | ratio | Reported bed-heater power. |
| `fan.speed` | number (CSV: text) | ratio | Reported fan-control ratio, not measured RPM. |
| `print_stats.state` | string / source-defined | state | Reported job state. |
| `virtual_sdcard.file_position` | integer (CSV: text) | bytes | Observed source byte cursor. |

## telemetry_sample

File/API: `bundle/gcode/telemetry_samples.jsonl` · Row grain: **sample** · Status: **current**

Per-field units for values are defined in telemetry_values.

**Join:** Join cursor samples by sample_index within the same session. Interpret the values object with its registry.

**Time:** source_frame_lower/upper are host-observed brackets. Do not directly use sample_index, line or Moonraker eventtime as WAV seconds. Units follow the registry/parent source.

**Missing values:** Missing keys and empty values follow the source contract. Do not convert unknown/needs_review to a normal decision or zero.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `schema_version` | schema-specific string or integer | version | File/input format version; string or numeric representation depends on the schema. |
| `sample_index` | integer (CSV: text) | index | Index joining corresponding telemetry and recorder-cursor samples. |
| `moonraker_eventtime` | number (CSV: text) | s, source clock | Original Moonraker observation clock; do not use directly as WAV-relative seconds. |
| `values` | JSON object/string as specified | JSON | Telemetry sample values keyed by registry path. |

## clip_annotations_range

File/API: `annotations/clip/clip_annotations_range.csv` · Row grain: **clip × original interval** · Status: **specified**

Specified final schema, absent from current collection archives. The example is documentation-only.

**Join:** session_id+clip_uid+range_kind+range_id identify an intersection row. clip_uid joins clip_plan; range_id joins the original interval.

**Time:** Retain intersection source/WAV frames and clip-relative seconds. Distinguish original observation boundaries from clipped intersections.

**Missing values:** An empty core leaves both core cells empty. Non-G-code evidence may leave source-line cells empty. Admitted human ranges require revision/hash.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `clip_uid` | string | identifier | Identifier of a shared temporal clip, common to all channels. |
| `session_id` | string | identifier | Current collector session identifier. |
| `printer_id` | string | identifier | Physical printer/build identifier, not a fault label. |
| `range_id` | string | identifier | Original session-interval ID, retained across all intersecting clips. |
| `range_kind` | string | category | Layer: phase/process_feature/operation/belt_activity/fault/unknown. Allowed values: phase, process_feature, operation, belt_activity, fault, unknown |
| `label` | string | category | Operation, phase or event label; may be distinct from a feature. |
| `label_original` | string | text | TYPE or annotation string before normalization. |
| `clip_relative_start_seconds` | finite number (CSV: decimal text) | s | Intersection-start frame minus clip-start frame, divided by sample_rate. The origin is this clip's start. |
| `clip_relative_end_seconds` | finite number (CSV: decimal text) | s | Intersection-end frame minus clip-start frame, divided by sample_rate. The ending frame is excluded. |
| `overlap_duration_seconds` | finite number (CSV: decimal text) | s | This row's intersection-frame count divided by sample_rate. Distinct from a time position or directly measured physical-fault duration. |
| `overlap_ratio` | finite number (CSV: decimal text) | ratio | Row overlap frames divided by clip frames; do not simply sum overlapping rows. |
| `start_source_frame` | integer (CSV: decimal text) | frames | Starting source frame of the intersection between the original range and this clip. |
| `end_source_frame_exclusive` | integer (CSV: decimal text) | frames | Exclusive ending source frame of the intersection between the original range and this clip. |
| `start_wav_frame` | integer (CSV: decimal text) | frames | Interval start relative to WAV frame zero. |
| `end_wav_frame_exclusive` | integer (CSV: decimal text) | frames | Exclusive interval end relative to WAV frame zero. |
| `start_boundary_lower_frame` | integer (CSV: decimal text) | frames | Lower observation bound at the source range's start. |
| `start_boundary_upper_frame` | integer (CSV: decimal text) | frames | Upper observation bound at the source range's start. |
| `end_boundary_lower_frame` | integer (CSV: decimal text) | frames | Lower observation bound at the source range's end. |
| `end_boundary_upper_frame` | integer (CSV: decimal text) | frames | Upper observation bound at the source range's end. |
| `core_start_source_frame` | integer (CSV: decimal text) or empty cell | frames | Starting frame of the clip/core intersection. |
| `core_end_source_frame_exclusive` | integer (CSV: decimal text) or empty cell | frames | Ending frame of the clip/core intersection; empty when there is no core. |
| `left_clipped` | boolean encoded as true/false | boolean | Whether the original interval was clipped at the clip's left boundary. |
| `right_clipped` | boolean encoded as true/false | boolean | Whether the original interval was clipped at the clip's right boundary. |
| `source_line_start` | integer (CSV: decimal text) or empty cell | index | Source line initiating the original interval. |
| `source_line_end` | integer (CSV: decimal text) or empty cell | index | Evidence source line for the next TYPE/end transition. |
| `source_artifact` | string | path | Evidence-artifact path relative to the release root; examples use the restored root. |
| `source_artifact_sha256` | string | SHA-256 | SHA-256 of the source evidence artifact. |
| `annotation_authority` | string | category | Kind of evidence used to determine or generate this value or interval. |
| `review_state` | string | category | Review state for this schema; session, clip and legacy vocabularies differ. |
| `range_policy_version` | string | version | Version of range definition, normalization and intersection policy. |
| `annotation_revision` | string or empty cell | version | Admitted annotation revision linked to the final range; empty in automatic examples. |
| `annotation_sha256` | string or empty cell | SHA-256 | SHA-256 of the admitted annotation content. |

## gcode_review_row

File/API: `bundle/gcode/gcode_review.json: rows[]` · Row grain: **source line** · Status: **current**

Union of keys observed in all gcode_review rows of the 78 selected sessions. Keys depend on observation status. UNMAPPED rows have unmapped_reason instead of bracket coordinates. Both code branches and all actual rows are checked; the reason field is included.

**Join:** The parent gcode_review_envelope supplies session/source identity for all rows. Line/byte coordinates are valid only within that source.

**Time:** source_frame_lower/upper are host-observed brackets. Do not directly use sample_index, line or Moonraker eventtime as WAV seconds. Units follow the registry/parent source.

**Missing values:** UNMAPPED rows contain unmapped_reason and omit unjoined bracket fields. Do not fill them with frame zero.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `acceptance_status` | string / source-defined | category | Source-row review/admission state, distinct from observation status such as OBSERVED_BRACKET. |
| `byte_end_exclusive` | integer (CSV: text) | bytes | Exclusive ending byte offset of the original source line. |
| `byte_start` | integer (CSV: text) | bytes | Starting byte offset of the original source line. |
| `command` | string / source-defined | text | Retained source line or command string. |
| `evidence_status` | string / source-defined | category | Original source-row observation status, such as OBSERVED_BRACKET/UNMAPPED. Allowed values: OBSERVED_BRACKET, UNMAPPED |
| `left_sample_index` | integer (CSV: text) | index | Left cursor-sample index of the source-boundary crossing. |
| `line` | integer (CSV: text) | index | Observed source line number. |
| `right_sample_index` | integer (CSV: text) | index | Right cursor-sample index of the source-boundary crossing. |
| `source_boundary_byte` | integer (CSV: text) | bytes | Boundary byte offset of the observed source line. |
| `source_frame_lower` | integer (CSV: text) | frames | Lower host-observed source-frame bracket bound. |
| `source_frame_upper` | integer (CSV: text) | frames | Upper host-observed source-frame bracket bound. |
| `unmapped_reason` | string / source-defined | category | Original reason why no bracket could be constructed for the source row. Allowed values: NO_ADJACENT_CURSOR_CROSSING, OUTSIDE_CANONICAL_AUDIO |
| `wav_frame_lower` | integer (CSV: text) | frames | Observed lower bound relative to the first WAV frame. |
| `wav_frame_upper` | integer (CSV: text) | frames | Observed upper bound relative to the first WAV frame. |
| `width_frames` | integer (CSV: text) | frames | Observation bracket upper minus lower; not a physical acoustic-error bound. |

## recorder_timebase

File/API: `bundle/session/manifest.json (timebase fields)` · Row grain: **session timebase** · Status: **current**

Time-coordinate fields used for clip reconstruction, not the complete raw-recorder manifest schema.

**Join:** Session-manifest origin/boundary fields. Subtract first_source_frame from a source frame to obtain a WAV frame.

**Time:** Decisions/settings without time fields inherit the linked session/clip coordinates. Updated/completed Unix times describe revision history, not audio onset.

**Missing values:** Missing keys and empty values follow the source contract. Do not convert unknown/needs_review to a normal decision or zero.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `first_source_frame` | integer (CSV: text) | frames | Source frame corresponding to the first canonical-WAV frame. |
| `start_boundary_frame` | integer (CSV: text) | frames | Recording-start boundary and current clip-grid origin. |
| `frame_count` | integer (CSV: text) | frames | Number of frames in the target audio. |
| `sample_rate` | number (CSV: text) | Hz | Source PCM sampling rate. |
| `audio_sha256` | string / source-defined | SHA-256 | SHA-256 of canonical WAV bytes. |

## package_sessions

File/API: `package/sessions.csv` · Row grain: **session** · Status: **implemented-finalizer**

Dataset-wide session aggregate generated by the finalizer.

**Join:** session_id → source WAV/archive/clip count. printer_id and domain_id identify physical printers in the current collection.

**Time:** Decisions/settings without time fields inherit the linked session/clip coordinates. Updated/completed Unix times describe revision history, not audio onset.

**Missing values:** Missing keys and empty values follow the source contract. Do not convert unknown/needs_review to a normal decision or zero.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `printer_id` | string / source-defined | identifier | Physical printer/build identifier, not a fault label. |
| `domain_id` | string / source-defined | identifier | Domain identifier; currently equal to printer_id in the package. |
| `session_id` | string / source-defined | identifier | Current collector session identifier. |
| `run_id` | string / source-defined | identifier | Execution-envelope identifier linked to the session. |
| `slot_id` | string / source-defined | identifier | Collection-matrix slot identifier, distinct from actual fault truth. |
| `planned_condition` | string / source-defined | category | Planned collection condition, not an admitted clip class. |
| `planned_fault_family` | string / source-defined | category | Package column representing the planned fault_mode. |
| `speed_protocol` | string / source-defined | category | Package collection-protocol value, such as slow/fast. |
| `canonical_duration_s` | number (CSV: text) | s | Original session-WAV duration, shared by all four channels. |
| `clip_count` | integer (CSV: text) | count | Temporal clip count, distinct from the number of four-channel files. |
| `channel_count` | integer (CSV: text) | count | Number of simultaneously retained channels. |
| `source_wav_sha256` | string / source-defined | SHA-256 | SHA-256 of original WAV bytes. |
| `archive_path` | string / source-defined | path | Session-archive path relative to the package root. |
| `archive_bytes` | integer (CSV: text) | bytes | Complete compressed-file size. |
| `archive_sha256` | string / source-defined | SHA-256 | SHA-256 of the compressed archive bytes. |
| `split` | string / source-defined | category | Dataset split name; current collection aggregates use unassigned. |

## package_clips

File/API: `package/clips.csv` · Row grain: **clip** · Status: **implemented-finalizer**

start_time_s/end_time_s are WAV-relative; recording_relative_* are recording-boundary-relative.

**Join:** clip_id retains the original clip_uid value. session_id joins package_sessions; clip_id joins package_clip_files.

**Time:** start_time_s/end_time_s are WAV-relative; recording_relative_* are recording-boundary-relative. end_source_frame_exclusive excludes the final frame.

**Missing values:** Missing keys and empty values follow the source contract. Do not convert unknown/needs_review to a normal decision or zero.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `printer_id` | string / source-defined | identifier | Physical printer/build identifier, not a fault label. |
| `domain_id` | string / source-defined | identifier | Domain identifier; currently equal to printer_id in the package. |
| `session_id` | string / source-defined | identifier | Current collector session identifier. |
| `clip_id` | string / source-defined | identifier | Column name used for clip_uid in package aggregates. |
| `grid_index` | integer (CSV: text) | index | Integer index on the original fixed grid; excluded indices are not renumbered. |
| `start_source_frame` | integer (CSV: text) | frames | Starting source frame of the interval. |
| `end_source_frame_exclusive` | integer (CSV: text) | frames | End of the source interval; this frame is excluded. |
| `start_wav_frame` | integer (CSV: text) | frames | Interval start relative to WAV frame zero. |
| `end_wav_frame_exclusive` | integer (CSV: text) | frames | Exclusive interval end relative to WAV frame zero. |
| `start_time_s` | number (CSV: text) | s | WAV-relative starting time of the package clip. |
| `end_time_s` | number (CSV: text) | s | WAV-relative ending time of the package clip. |
| `recording_relative_start_s` | number (CSV: text) | s | Clip start relative to the recording-start boundary. |
| `recording_relative_end_s` | number (CSV: text) | s | Clip end relative to the recording-start boundary. |
| `sample_rate` | number (CSV: text) | Hz | Source PCM sampling rate. |
| `planned_condition` | string / source-defined | category | Planned collection condition, not an admitted clip class. |
| `planned_fault_family` | string / source-defined | category | Package column representing the planned fault_mode. |
| `selection_rule` | string / source-defined | text | Identifier/description of the clip-selection rule. |
| `clip_policy_version` | string / source-defined | version | Version of the clip-generation/selection policy. |
| `source_wav_sha256` | string / source-defined | SHA-256 | SHA-256 of original WAV bytes. |
| `split` | string / source-defined | category | Dataset split name; current collection aggregates use unassigned. |

## package_clip_files

File/API: `package/clip_files.csv` · Row grain: **clip × channel** · Status: **implemented-finalizer**

archive_path+member_path locate one channel file.

**Join:** clip_id+channel_id distinguish file rows. archive_path+member_path locate the actual file inside its archive.

**Time:** Decisions/settings without time fields inherit the linked session/clip coordinates. Updated/completed Unix times describe revision history, not audio onset.

**Missing values:** Missing keys and empty values follow the source contract. Do not convert unknown/needs_review to a normal decision or zero.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `printer_id` | string / source-defined | identifier | Physical printer/build identifier, not a fault label. |
| `session_id` | string / source-defined | identifier | Current collector session identifier. |
| `clip_id` | string / source-defined | identifier | Column name used for clip_uid in package aggregates. |
| `channel_id` | DG: integer 1–4; legacy: ch1–ch4 | channel | Channel identifier; its format follows the file schema. |
| `archive_path` | string / source-defined | path | Session-archive path relative to the package root. |
| `member_path` | string / source-defined | path | Internal path of this channel WAV relative to the transport-archive root. |
| `size_bytes` | integer (CSV: text) | bytes | Artifact size. |
| `sha256` | string / source-defined | SHA-256 | SHA-256 of the artifact referenced by this manifest. |

## setup_measurement_snapshot

File/API: `bundle/run/setup_measurement_snapshot.json` · Row grain: **session setup snapshot; [] is one event** · Status: **current-observed-78**

Recursive union of all setup-object keys in 78 production sessions; not every branch key is required in every session. Numeric arrays, such as XY pairs, are single values; [] denotes one event-array item. Fan notes are declarations, belt deltas are displacements and collision-event timing is command-based setup.

**Join:** Join through the run's session/printer identity. collision events[].event_index and belt target do not replace session-wide labels.

**Time:** Decisions/settings without time fields inherit the linked session/clip coordinates. Updated/completed Unix times describe revision history, not audio onset.

**Missing values:** Missing keys and empty values follow the source contract. Do not convert unknown/needs_review to a normal decision or zero.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `belt_measurements` | object | JSON | Rear-tensioner displacement measurements by target belt. |
| `belt_measurements.belt_a` | object | JSON | Displacement record for the belt physically named A at the site. |
| `belt_measurements.belt_a.current_mm` | number | mm | Current rear-tensioner length entered using the same reference surface. |
| `belt_measurements.belt_a.delta_mm` | number | mm | current_mm − normal_mm; input lengths are rounded to three decimal places. |
| `belt_measurements.belt_a.normal_mm` | number | mm | Normal-state rear-tensioner length entered using the same reference surface. |
| `belt_measurements.belt_b` | object | JSON | Displacement record for the belt physically named B at the site. |
| `belt_measurements.belt_b.current_mm` | number | mm | Current rear-tensioner length entered using the same reference surface. |
| `belt_measurements.belt_b.delta_mm` | number | mm | current_mm − normal_mm; input lengths are rounded to three decimal places. |
| `belt_measurements.belt_b.normal_mm` | number | mm | Normal-state rear-tensioner length entered using the same reference surface. |
| `collection_mode` | string | category | Selected collection scope: production/debug/qualification. |
| `collision_artifact_manifest` | object | JSON | Registered collision-path generation manifest for this session. |
| `collision_artifact_manifest.annotation_padding_frames` | integer | frames | Annotation padding declared by the collision artifact; not a measured onset error. |
| `collision_artifact_manifest.audio_sample_rate` | integer | Hz | Audio sample rate used for artifact timing calculations. |
| `collision_artifact_manifest.collision_boundaries_mm` | object | JSON | Object containing retained X/Y collision-boundary coordinates. |
| `collision_artifact_manifest.collision_boundaries_mm.x_max` | number | mm | Retained maximum-X collision-boundary coordinate. |
| `collision_artifact_manifest.collision_boundaries_mm.x_min` | number | mm | Retained minimum-X collision-boundary coordinate. |
| `collision_artifact_manifest.collision_boundaries_mm.y_max` | number | mm | Retained maximum-Y collision-boundary coordinate. |
| `collision_artifact_manifest.collision_range_contract` | object | JSON | Interval-construction rules in the collision-path manifest. |
| `collision_artifact_manifest.collision_range_contract.end` | string | text | Collision-interval end rule declared in the original manifest. |
| `collision_artifact_manifest.collision_range_contract.padding_seconds` | number | s | Annotation-padding duration in the original manifest. |
| `collision_artifact_manifest.collision_range_contract.physical_onset_claim` | boolean | boolean | Whether measured physical-contact onset is claimed; false in the candidate code. |
| `collision_artifact_manifest.collision_range_contract.start` | string | text | Collision-interval start rule declared in the original manifest. |
| `collision_artifact_manifest.direction` | string | category | Collision target direction: a single-axis or corner direction. |
| `collision_artifact_manifest.estimated_duration_seconds` | number | s | Builder-estimated path duration, distinct from measured audio duration. |
| `collision_artifact_manifest.event_count` | integer | count | Number of collision events registered in the path manifest. |
| `collision_artifact_manifest.events` | array | JSON array | List of collision-event or candidate objects; each item follows its schema. |
| `collision_artifact_manifest.events[].annotation_padding_seconds` | number | s | Annotation-padding duration declared for this event. |
| `collision_artifact_manifest.events[].approach_xy_mm` | array | mm[2] | X/Y coordinate pair of the collision approach position. |
| `collision_artifact_manifest.events[].axis_component_velocity_mm_s` | number | mm/s | Axis-component velocity of the approach path. |
| `collision_artifact_manifest.events[].collision_range_end_marker` | string | identifier | Marker name registered for the interval end. |
| `collision_artifact_manifest.events[].collision_range_start` | string | text | Artifact rule string defining the interval start. |
| `collision_artifact_manifest.events[].commanded_contact_seconds` | number | s | Contact duration designed into the command path, not measured contact duration. |
| `collision_artifact_manifest.events[].contact_class` | string | category | Protocol category for the commanded contact duration. |
| `collision_artifact_manifest.events[].corner` | string | category | Event corner name; preserve it separately from single-axis direction. |
| `collision_artifact_manifest.events[].direction` | string | category | Collision target direction: a single-axis or corner direction. |
| `collision_artifact_manifest.events[].estimated_contact_offset_seconds` | number | s | Command-derived estimated travel time from the approach marker to the boundary. |
| `collision_artifact_manifest.events[].event_index` | integer | index | Collision-event sequence number within the session path. |
| `collision_artifact_manifest.events[].marker_prefix` | string | identifier | Prefix identifier joining multiple markers of one collision event. |
| `collision_artifact_manifest.events[].tangent_coordinate_mm` | number | mm | Tangential coordinate for this single-boundary event. |
| `collision_artifact_manifest.events[].target_xy_mm` | array | mm[2] | X/Y target coordinate pair commanded by the collision path. |
| `collision_artifact_manifest.events[].velocity_mm_s` | number | mm/s | Commanded path velocity for this collision event. |
| `collision_artifact_manifest.gcode_sha256` | string | SHA-256 | SHA-256 of registered collision G-code bytes. |
| `collision_artifact_manifest.requested_duration_seconds` | integer | s | Path duration requested during artifact generation. |
| `collision_artifact_manifest.schema_version` | string | version | File/input format version; string or numeric representation depends on the schema. |
| `collision_artifact_manifest.seed` | string | integer | Random seed used to generate the collision path. |
| `collision_artifact_manifest.speed` | string | category | Artifact speed family: slow/fast. |
| `completed_unix_ns` | integer | ns, Unix epoch | Unix-epoch time when measurement or confirmation completed. |
| `evidence_sha256` | string | SHA-256 | SHA-256 of the canonically serialized measurement object, excluding evidence_sha256 itself. |
| `fan_damage` | object | JSON | Operator-declaration object describing physical fan damage. |
| `fan_damage.authority` | string | category | Evidence-record kind, such as planned/setup/human. |
| `fan_damage.machine_id` | string | identifier | Machine identifier of the printer whose setup was recorded. |
| `fan_damage.note` | string | text | Note value retained from the original record. |
| `fan_damage.recorded_unix_ns` | integer | ns, Unix epoch | Unix-epoch time when the declaration was saved; not an audio coordinate. |
| `fan_damage.schema_version` | string | version | File/input format version; string or numeric representation depends on the schema. |
| `input_source` | string | category | Source of this setup input, such as operator_measurement. |
| `interpretation` | string | text | Scope and limitations of the measurement supported by this setup evidence. |
| `machine_id` | string | identifier | Machine identifier of the printer whose setup was recorded. |
| `measurement_id` | string | identifier | Original setup measurement/confirmation record identifier. |
| `measurement_type` | string | category | Applied measurement method, such as rear_tensioner_displacement. |
| `operator_confirmed` | boolean | boolean | Whether the operator confirmed this measurement. |
| `production_credit` | boolean | boolean | Recorded eligibility for counting as a production session. |
| `recording_tag` | string | text | Original tag assigned to the recording workflow. |
| `schema_version` | string | version | File/input format version; string or numeric representation depends on the schema. |
| `target` | string | category | Displacement-measurement target: belt_a/belt_b/belt_a_b. |

## collision_rms_response

For clip selection, see [Clip selection](selection.md). The stored gap parameter is 0.750 s; conversion to 20 ms bins uses round(37.5)=38, so the executed maximum inactive gap is 0.760 s. The 50 ms padding is display-only; admission uses event cores.

File/API: `GET /debug/review/<session_id>/collision-rms.json` · Row grain: **session response; events[] is one automatic candidate** · Status: **implemented-review-only**

Response computed on demand by the review API, not a stored CSV in the 78 archives. Core spans include gaps joined by the maximum-gap rule and may differ from active_bin_count × bin_seconds. physical_onset_claim=false; this is an automatic candidate rather than a final fault label.

**Join:** Response session_id links the source. events[].marker_prefix/event_index identify automatic search events.

**Time:** Source frames use the shared recorder coordinates. start_seconds/end_seconds are relative to recording start_boundary_frame and may differ from WAV-relative seconds by pre-roll.

**Missing values:** Missing keys and empty values follow the source contract. Do not convert unknown/needs_review to a normal decision or zero.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `schema_version` | schema-specific string or integer | version | File/input format version; string or numeric representation depends on the schema. |
| `session_id` | string / source-defined | identifier | Current collector session identifier. |
| `sample_rate` | number (CSV: text) | Hz | Source PCM sampling rate. |
| `time_axis` | string | category | Coordinate system used by RMS candidates: recorder_source_frames. |
| `authority` | string / source-defined | category | Evidence-record kind, such as planned/setup/human. |
| `review_state` | string / source-defined | category | Review state for this schema; session, clip and legacy vocabularies differ. |
| `physical_onset_claim` | boolean | boolean | Whether measured physical-contact onset is claimed; false in the candidate code. |
| `source_audio_location` | string | category | Storage-location kind of the canonical audio read for collision candidates. |
| `source_manifest_location` | string | category | Storage-location kind of the recorder manifest read for candidates. |
| `method` | string / source-defined | text | Calculation/mapping method. |
| `method.bin_seconds` | number | s | RMS bin duration; currently 0.020 seconds. |
| `method.channel_aggregation` | string | category | Median aggregation of four-channel RMS dBFS for each bin. |
| `method.threshold` | string | category | Threshold construction: a fixed dB rise above the search-gate median. |
| `method.threshold_rise_db` | number | dB | RMS threshold rise above the gate median; currently 12 dB. |
| `method.maximum_join_gap_seconds` | number | s | Declared join parameter 0.750 s; executed as round(0.750/0.020)=38 bins, allowing 0.760 s of inactive bins. |
| `method.minimum_active_seconds` | number | s | Total active-bin duration required in a candidate group; currently 0.080 seconds. |
| `method.display_padding_seconds` | number | s | Time added before/after the candidate core for display; currently 0.050 seconds. |
| `method.search_gate` | string | text | Construction of candidate search gates from G-code markers. |
| `source_event_count` | integer | count | Number of searchable G-code gates. |
| `candidate_count` | integer | count | Number of returned candidates satisfying RMS criteria. |
| `rejected_event_count` | integer | count | Search-gate count minus candidate count; not a human rejection decision. |
| `events` | array | JSON array | List of collision-event or candidate objects; each item follows its schema. |
| `events[].marker_prefix` | string | identifier | Prefix identifier joining multiple markers of one collision event. |
| `events[].direction` | string | category | Collision target direction: a single-axis or corner direction. |
| `events[].event_index` | integer | index | Collision-event sequence number within the session path. |
| `events[].line` | integer | index | Observed source line number. |
| `events[].estimated_contact_source_frame_lower` | integer | frames | Lower contact-frame estimate from commanded velocity and approach distance. |
| `events[].estimated_contact_source_frame_upper` | integer | frames | Upper contact-frame estimate from commanded velocity and approach distance. |
| `events[].search_source_frame_lower` | integer | frames | Original G-code search-gate start frame; RMS reads are constrained by WAV/recording bounds. |
| `events[].search_source_frame_upper` | integer | frames | Original G-code search-gate end frame; RMS reads are constrained by WAV/recording bounds. |
| `events[].command` | string / source-defined | text | Retained source line or command string. |
| `events[].range_kind` | string | category | collision-rms-candidate, distinct from an admitted fault interval. |
| `events[].source_frame_lower` | integer | frames | Display interval start after 50 ms padding, clamped to the RMS search gate; not the unpadded event core. |
| `events[].source_frame_upper` | integer | frames | Display interval exclusive end after 50 ms padding, clamped to the RMS search gate. |
| `events[].core_source_frame_lower` | integer | frames | Start frame of the selected group's first active bin. |
| `events[].core_source_frame_upper` | integer | frames | End frame of the selected group's last active bin; internal gaps may be included. |
| `events[].start_seconds` | number | s, recording-relative | Padded RMS-candidate start in recording-boundary-relative seconds. |
| `events[].end_seconds` | number | s, recording-relative | Padded RMS-candidate end in recording-boundary-relative seconds. |
| `events[].core_start_seconds` | number | s, recording-relative | Core start in seconds relative to recording start_boundary_frame. |
| `events[].core_end_seconds` | number | s, recording-relative | Core end in seconds relative to recording start_boundary_frame. |
| `events[].search_start_seconds` | number | s, recording-relative | Actual clipped search start in recording-relative seconds. |
| `events[].search_end_seconds` | number | s, recording-relative | Actual clipped search upper bound in recording-relative seconds; the final incomplete bin is excluded. |
| `events[].baseline_dbfs` | number | dBFS | Median bin score within the gate; based on dBFS, not calibrated SPL. |
| `events[].threshold_dbfs` | number | dBFS | baseline_dbfs + threshold_rise_db. |
| `events[].peak_dbfs` | number | dBFS | Maximum bin score of the selected group, not the waveform sample peak. |
| `events[].active_bin_count` | integer | count | Number of selected-group bins at or above threshold; gap bins are excluded. |
| `events[].qualified_group_count` | integer | count | Number of groups satisfying the minimum active-bin count. |
| `events[].annotation_authority` | string / source-defined | category | Kind of evidence used to determine or generate this value or interval. |
| `events[].review_state` | string / source-defined | category | Review state for this schema; session, clip and legacy vocabularies differ. |
| `events[].physical_onset_claim` | boolean | boolean | Whether measured physical-contact onset is claimed; false in the candidate code. |

## fan_pwm_ranges

File/API: `bundle/clips/fan_pwm_ranges.csv` · Row grain: **clip × affected source fan command** · Status: **implemented-conditional**

Conditional output for fan-control paths, absent from the current 78 member inventories. Physical blade damage is not a PWM transformation. Source coordinates describe original command ranges intersecting clips, rather than already clipped coordinates.

**Join:** clip_uid → clip_plan; source_line identifies the original fan-source command. Multiple clips may reference the same original range.

**Time:** Decisions/settings without time fields inherit the linked session/clip coordinates. Updated/completed Unix times describe revision history, not audio onset.

**Missing values:** Missing keys and empty values follow the source contract. Do not convert unknown/needs_review to a normal decision or zero.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `clip_uid` | string / source-defined | identifier | Identifier of a shared temporal clip, common to all channels. |
| `mode` | string | category | Original fan-control transformation mode, distinct from physical damage in this collection. |
| `source_line` | string | line number | Original G-code line number projected into a fan interval. |
| `command` | string / source-defined | text | Retained source line or command string. |
| `start_source_frame` | integer (CSV: text) | frames | Starting source frame of the interval. |
| `end_source_frame_exclusive` | integer (CSV: text) | frames | End of the source interval; this frame is excluded. |
| `mapping` | string | category | Host-observed interval mapping from a fan-source command to the next fan command. |

## fan_pwm_range_manifest

File/API: `bundle/clips/fan_pwm_range_manifest.json` · Row grain: **session fan command projection** · Status: **implemented-conditional**

Conditional output for fan-control paths, absent from the current 78 member inventories. Physical blade damage is not a PWM transformation. Source coordinates describe original command ranges intersecting clips, rather than already clipped coordinates.

**Join:** Mode and mapping-coverage summary for this session's fan_pwm_ranges.csv.

**Time:** Decisions/settings without time fields inherit the linked session/clip coordinates. Updated/completed Unix times describe revision history, not audio onset.

**Missing values:** Missing keys and empty values follow the source contract. Do not convert unknown/needs_review to a normal decision or zero.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `schema_version` | schema-specific string or integer | version | File/input format version; string or numeric representation depends on the schema. |
| `mode` | string | category | Original fan-control transformation mode, distinct from physical damage in this collection. |
| `affected_command_count` | string | count | Number of source commands affected by the fan transformation. |
| `mapped_command_count` | string | count | Number of fan commands with observation brackets suitable for range construction. |
| `unmapped_command_count` | string | count | affected_command_count − mapped_command_count. |
| `range_rule` | string | text | Annotation interval rule declared in fan-control settings. |

## human_annotation_request

File/API: `POST session annotation: structured request` · Row grain: **session revision request** · Status: **current**

expected_revision is null on first save and the existing revision string on edit. Mixing or adding keys from the two request forms is rejected by the current API.

**Join:** URL session + expected_revision fix the edit target; annotation follows human_annotation_input.

**Time:** Decisions/settings without time fields inherit the linked session/clip coordinates. Updated/completed Unix times describe revision history, not audio onset.

**Missing values:** Missing keys and empty values follow the source contract. Do not convert unknown/needs_review to a normal decision or zero.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `annotation` | JSON object/string as specified | JSON | Structured session-annotation object; null for a legacy note-only record. |
| `expected_revision` | string / source-defined | version | Current revision on which the edit request is based; a mismatch causes a conflict. |

## human_note_request

File/API: `POST session annotation: legacy request` · Row grain: **session note revision request** · Status: **current**

expected_revision is null on first save and the existing revision string on edit. Mixing or adding keys from the two request forms is rejected by the current API.

**Join:** URL session + expected_revision fix the edit target; distinguish note-only history from structured decisions.

**Time:** Decisions/settings without time fields inherit the linked session/clip coordinates. Updated/completed Unix times describe revision history, not audio onset.

**Missing values:** Missing keys and empty values follow the source contract. Do not convert unknown/needs_review to a normal decision or zero.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `human_note` | string / source-defined | text | Human note retained in a legacy or structured annotation. |
| `expected_revision` | string / source-defined | version | Current revision on which the edit request is based; a mismatch causes a conflict. |

## gcode_review_envelope

File/API: `bundle/gcode/gcode_review.json` · Row grain: **session G-code observation artifact** · Status: **current**

Rows contain per-line evidence; this wrapper fixes exact source bytes and audio coordinates. The display-range start is distinct from the first WAV frame. Anchor finalization adds anchor_ranges/anchor_event_count. All 78 inputs have empty anchor_ranges, so mapping_claim alone does not establish individual G1 anchor evidence.

**Join:** session_id joins the recorder manifest; source_sha256 joins retained source bytes; rows follow gcode_review_row.

**Time:** source_frame_lower/upper are host-observed brackets. Do not directly use sample_index, line or Moonraker eventtime as WAV seconds. Units follow the registry/parent source.

**Missing values:** Missing keys and empty values follow the source contract. Do not convert unknown/needs_review to a normal decision or zero.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `schema_version` | schema-specific string or integer | version | File/input format version; string or numeric representation depends on the schema. |
| `session_id` | string / source-defined | identifier | Current collector session identifier. |
| `source_sha256` | string | SHA-256 | SHA-256 of the exact instrumented source bytes referenced by the G-code review. |
| `source_size` | integer | bytes | Complete byte count of the retained instrumented G-code source. |
| `sample_rate` | number (CSV: text) | Hz | Source PCM sampling rate. |
| `audio_first_source_frame` | integer | frames | First source frame of the canonical WAV referenced by this G-code review. |
| `audio_last_source_frame_exclusive` | integer | frames | Exclusive source-frame end of the canonical WAV referenced by this G-code review. |
| `mapping_claim` | string | category | Claim describing source observation: HOST_OBSERVED_SOURCE_CURSOR_FRAME_BRACKETS_ONLY or MOONRAKER_G1_START_END_AUDIO_FRAME_BRACKETS; verify actual rows/anchor_ranges separately. Allowed values: HOST_OBSERVED_SOURCE_CURSOR_FRAME_BRACKETS_ONLY, MOONRAKER_G1_START_END_AUDIO_FRAME_BRACKETS |
| `point_interpolation` | boolean | boolean | False: the current G-code review does not interpolate a single point time. |
| `rows` | array | JSON array | Per-source-line G-code observation records, each following gcode_review_row. |
| `anchor_ranges` | array | JSON array | Ranges between START/END markers of original G1 commands; observed empty in all 78 current inputs. |
| `anchor_event_count` | integer | count | Number of marker events supplied to range construction, distinct from the count of nonempty anchor ranges. |

## planned_to_actual_correction

File/API: `human_annotation.json: planned_to_actual_corrections.<field>` · Row grain: **changed annotation field in one session revision** · Status: **current**

Value structure in a map keyed by changed field names. Compare expected_anomaly_progress_state with actual anomaly_progress_state. Unchanged fields are absent; source planned values are not overwritten.

**Join:** Entry in the parent envelope's changed-field map: the key identifies the field, and the value pairs planned and actual.

**Time:** Decisions/settings without time fields inherit the linked session/clip coordinates. Updated/completed Unix times describe revision history, not audio onset.

**Missing values:** Missing keys and empty values follow the source contract. Do not convert unknown/needs_review to a normal decision or zero.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `planned` | JSON value | JSON value | Original planned-defaults value for the corrected field. |
| `actual` | JSON value | JSON value | Value saved in the new human annotation for that field. |

## gcode_anchor_range

File/API: `bundle/gcode/gcode_review.json: anchor_ranges[]` · Row grain: **original G1 × START/END anchor pair** · Status: **implemented; no nonempty rows in observed 78**

Eleven keys that build_anchor_ranges can generate. Nonempty anchor ranges are not observed in the current 78 sessions. These differ from TYPE-derived process_feature ranges.

**Join:** Join the parent session and original source line/command. anchor_id connects the instrumented START/END pair.

**Time:** possible=[START.lower,END.upper), core=[START.upper,END.lower). WAV coordinates subtract the parent's audio_first_source_frame from source frames.

**Missing values:** The generator rejects incomplete marker pairs or reversed frame order. Empty anchor_ranges means there are no individual anchor rows.

| Field | Type | Unit | Meaning |
|---|---|---|---|
| `line` | integer (CSV: text) | index | Observed source line number. |
| `command` | string / source-defined | text | Retained source line or command string. |
| `anchor_id` | string / source-defined | identifier | Instrumentation anchor identifier. |
| `evidence_status` | string / source-defined | category | Original source-row observation status, such as OBSERVED_BRACKET/UNMAPPED. Allowed values: ANCHOR_BRACKET |
| `source_frame_lower` | integer (CSV: text) | frames | Lower host-observed source-frame bracket bound. |
| `source_frame_upper` | integer (CSV: text) | frames | Upper host-observed source-frame bracket bound. |
| `core_source_frame_lower` | integer | frames | Upper observation bound of the START marker; inner start of the anchor range. |
| `core_source_frame_upper` | integer | frames | Lower observation bound of the END marker; inner end of the anchor range. |
| `wav_frame_lower` | integer (CSV: text) | frames | Observed lower bound relative to the first WAV frame. |
| `wav_frame_upper` | integer (CSV: text) | frames | Observed upper bound relative to the first WAV frame. |
| `width_frames` | integer (CSV: text) | frames | Observation bracket upper minus lower; not a physical acoustic-error bound. |
