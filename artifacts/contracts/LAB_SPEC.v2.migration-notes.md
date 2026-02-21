# LAB_SPEC v1 -> v2 Migration Notes

## Purpose
`LAB_SPEC.v2.json` extends `LAB_SPEC.v1.json` for automated scaffold generation at scale while preserving v1 semantics.

## Compatibility Summary
- v1 fields are retained in v2:
  - `lab_id`
  - `title`
  - `canonical_features_used`
  - `sensors_used`
  - `storage_used`
  - `state_complexity_level`
  - `expected_runtime_constraints`
  - `config_schema_version`
  - `performance_goal`
- v2 adds generation and governance fields:
  - `schema_version`
  - `difficulty_level`
  - `state_model_type`
  - `async_complexity`
  - `ui_components_required`
  - `background_processing_required`
  - `performance_budget`
  - `expected_permissions`
  - `device_constraints`

## Breaking vs Non-Breaking
- Schema validation is stricter in v2 because new fields are required.
- Generator behavior remains backward-compatible by supporting **auto-upgrade** from v1 input.

## Recommended Auto-Upgrade Rules (v1 to v2)

1. `schema_version`
- Set to `lab_spec.v2`.

2. `difficulty_level`
- Derive from v1 complexity:
  - `S0_stateless` -> `1`
  - `S1_local_state` -> `1`
  - `S2_shared_state` -> `2`
  - `S3_persistent_state` -> `3`
  - `S4_streaming_effects` -> `4`

3. `state_model_type`
- Derive from complexity/features:
  - if includes `shared_state` or `derived_state` -> `unidirectional_store`
  - else if includes `persistent_state` -> `observable_mvvm`
  - else -> `local_mutable`

4. `async_complexity`
- Derive from sensors/background:
  - sensors `none` + no background -> `A1_single_async_call`
  - one active stream -> `A2_stream_subscription`
  - multi-stream -> `A3_multi_stream_orchestrated`
  - with `background_work` -> `A4_background_orchestrated`

5. `ui_components_required`
- Minimum default: `["title_text", "status_text", "primary_button"]`.
- Add `toggle_switch` if sensors are used.

6. `background_processing_required`
- `true` if `canonical_features_used` contains `background_work`, else `false`.

7. `performance_budget`
- Default baseline:
  - `max_dependencies_per_platform`: `10`
  - `max_third_party_libraries`: `2`
  - `max_files_generated`: `24`
  - `max_sensor_concurrency`: `2`
  - `max_background_tasks`: `1`
  - `max_config_branches`: `3`

8. `expected_permissions`
- Default `["none"]`.
- Add `location_when_in_use` when `gps` appears.
- Add `motion` when accelerometer/gyroscope appears.
- Add `camera`/`microphone` for corresponding sensors.

9. `device_constraints`
- Default:
  - `physical_device_required`: `false`
  - `android_min_api`: `26`
  - `ios_min_version`: `16.0`
  - `network_required`: `false`
  - `battery_sensitive`: `false`
  - `emulator_supported`: `true`

## Minimal Migration Pseudocode

```text
read v1 json
copy v1 fields unchanged
inject missing v2 fields via defaults/derivations
validate against LAB_SPEC.v2.json
emit LAB_SPEC.v2.json
```

## Guardrails (from PROMPT_06_s constraints)
- Do not exceed `max_third_party_libraries` without explicit justification.
- Keep generated file count and abstraction depth within budget.
- Keep sensor concurrency and background tasks bounded by spec budget.

