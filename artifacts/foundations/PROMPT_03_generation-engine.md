# PROMPT_03 - LAB Generation Engine (Spec -> Multi-Platform Scaffold)

## Scope
Design a minimal, extensible lab generation engine for `mobile-systems-lab`.

Input:
- `LAB_SPEC.v2.json` instance

Outputs:
- Kotlin Android scaffold
- Swift iOS scaffold
- Flutter scaffold
- React Native scaffold
- Cross-platform comparison report

Constraints applied from `.prompts/PROMPT_06_s.txt`:
- keep dependency count bounded
- keep abstraction depth shallow
- keep generated file count bounded
- avoid heavy frameworks/DI/state mega-layers
- enforce parity and drift checks across ecosystems

---

## SECTION 1 - LAB_SPEC Contract (v2)

Canonical schema:
- `artifacts/contracts/LAB_SPEC.v2.json`

### Required fields (v2)
- `lab_id`
- `difficulty_level` (1-5)
- `canonical_features_used`
- `sensors_used`
- `storage_used`
- `state_model_type`
- `async_complexity`
- `config_schema_version`
- `ui_components_required`
- `background_processing_required`
- `performance_budget`
- `expected_permissions`
- `device_constraints`

Backward-compatible retained v1 fields:
- `title`
- `state_complexity_level`
- `expected_runtime_constraints`
- `performance_goal`

### Example LAB_SPECs (v2)

`LAB_02_STATEFUL_COUNTER`
```json
{
  "schema_version": "lab_spec.v2",
  "lab_id": "LAB_02_STATEFUL_COUNTER",
  "title": "Stateful Counter",
  "difficulty_level": 1,
  "canonical_features_used": ["local_state", "view_composition", "persistent_state"],
  "sensors_used": ["none"],
  "storage_used": ["key_value"],
  "state_complexity_level": "S1_local_state",
  "state_model_type": "local_mutable",
  "async_complexity": "A1_single_async_call",
  "expected_runtime_constraints": ["cold_start_budget", "frame_budget_16ms"],
  "config_schema_version": "config.v1",
  "ui_components_required": ["title_text", "numeric_display", "primary_button", "secondary_button"],
  "background_processing_required": false,
  "performance_goal": {
    "startup_ms_p95_max": 1200,
    "frame_time_ms_p95_max": 16.67,
    "memory_mb_peak_max": 180,
    "battery_drain_percent_10min_max": 1
  },
  "performance_budget": {
    "max_dependencies_per_platform": 8,
    "max_third_party_libraries": 2,
    "max_files_generated": 18,
    "max_sensor_concurrency": 0,
    "max_background_tasks": 0,
    "max_config_branches": 2
  },
  "expected_permissions": ["none"],
  "device_constraints": {
    "physical_device_required": false,
    "android_min_api": 26,
    "ios_min_version": "16.0",
    "network_required": false,
    "battery_sensitive": false,
    "emulator_supported": true
  }
}
```

`LAB_03_BACKGROUND_GPS_LOGGER`
```json
{
  "schema_version": "lab_spec.v2",
  "lab_id": "LAB_03_BACKGROUND_GPS_LOGGER",
  "title": "Background GPS Logger",
  "difficulty_level": 4,
  "canonical_features_used": ["lifecycle", "sensors", "permissions", "storage", "background_work", "performance_tuning"],
  "sensors_used": ["gps", "battery_state"],
  "storage_used": ["file_system", "database"],
  "state_complexity_level": "S4_streaming_effects",
  "state_model_type": "unidirectional_store",
  "async_complexity": "A4_background_orchestrated",
  "expected_runtime_constraints": ["battery_budget", "background_execution_limits", "permission_denied_path", "process_recreation"],
  "config_schema_version": "config.v1",
  "ui_components_required": ["title_text", "status_text", "toggle_switch", "list_view"],
  "background_processing_required": true,
  "performance_goal": {
    "startup_ms_p95_max": 1700,
    "frame_time_ms_p95_max": 16.67,
    "memory_mb_peak_max": 260,
    "battery_drain_percent_10min_max": 4
  },
  "performance_budget": {
    "max_dependencies_per_platform": 12,
    "max_third_party_libraries": 3,
    "max_files_generated": 34,
    "max_sensor_concurrency": 2,
    "max_background_tasks": 1,
    "max_config_branches": 3
  },
  "expected_permissions": ["location_when_in_use", "location_always", "file_read_write"],
  "device_constraints": {
    "physical_device_required": true,
    "android_min_api": 29,
    "ios_min_version": "16.0",
    "network_required": false,
    "battery_sensitive": true,
    "emulator_supported": false
  }
}
```

`LAB_04_CONFIG_MUTATION_TEST`
```json
{
  "schema_version": "lab_spec.v2",
  "lab_id": "LAB_04_CONFIG_MUTATION_TEST",
  "title": "Config Mutation Test",
  "difficulty_level": 3,
  "canonical_features_used": ["config_import_export", "storage", "config_mutation_testing", "derived_state"],
  "sensors_used": ["none"],
  "storage_used": ["file_system", "key_value"],
  "state_complexity_level": "S3_persistent_state",
  "state_model_type": "provider_notifier",
  "async_complexity": "A2_stream_subscription",
  "expected_runtime_constraints": ["storage_quota", "process_recreation"],
  "config_schema_version": "config.v1",
  "ui_components_required": ["title_text", "status_text", "primary_button", "secondary_button", "text_input", "list_view"],
  "background_processing_required": false,
  "performance_goal": {
    "startup_ms_p95_max": 1400,
    "frame_time_ms_p95_max": 16.67,
    "memory_mb_peak_max": 220,
    "battery_drain_percent_10min_max": 1.5
  },
  "performance_budget": {
    "max_dependencies_per_platform": 10,
    "max_third_party_libraries": 2,
    "max_files_generated": 26,
    "max_sensor_concurrency": 0,
    "max_background_tasks": 0,
    "max_config_branches": 5
  },
  "expected_permissions": ["file_read_write"],
  "device_constraints": {
    "physical_device_required": false,
    "android_min_api": 26,
    "ios_min_version": "16.0",
    "network_required": false,
    "battery_sensitive": false,
    "emulator_supported": true
  }
}
```

Compatibility and migration:
- `artifacts/contracts/LAB_SPEC.v2.migration-notes.md`

---

## SECTION 2 - Mapping Layer

Canonical mapping contract:
- `artifacts/contracts/CANONICAL_MAPPING.json`

Purpose:
- map canonical concepts and feature tokens to each ecosystem
- map template placeholders to resolver tables
- guarantee parity between generated implementations

Key mapping buckets:
- `concept_mappings`
- `state_model_type_mapping`
- `sensor_subscription_mapping`
- `permission_mapping`
- `template_placeholders`

---

## SECTION 3 - Template Structure

Template roots:

```text
templates/
  kotlin/
  swift/
  flutter/
  react-native/
```

Each root includes a minimal template set with placeholders:
- `{{STATE_MODEL}}`
- `{{SENSOR_SUBSCRIPTION}}`
- `{{PERMISSION_REQUEST}}`
- `{{CONFIG_LOAD}}`
- `{{CONFIG_SAVE}}`

Population rules:
- `{{STATE_MODEL}}` <- `state_model_type` via `state_model_type_mapping`
- `{{SENSOR_SUBSCRIPTION}}` <- `sensors_used` via `sensor_subscription_mapping`
- `{{PERMISSION_REQUEST}}` <- `expected_permissions` via `permission_mapping`
- `{{CONFIG_LOAD}}` <- `config_schema_version` + platform config loader template
- `{{CONFIG_SAVE}}` <- `storage_used` + platform storage template
- `{{UI_COMPONENTS}}` <- `ui_components_required`
- `{{BACKGROUND_BLOCK}}` <- `background_processing_required` + `async_complexity`

Minimal policy:
- do not generate extra framework layers beyond template core
- only generate files required by selected features and UI components

---

## SECTION 4 - Generation Flow

### ASCII pipeline

```text
              +-------------------------+
LAB_SPEC.v2 ->| 1) Parse + Validate     |
              +-----------+-------------+
                          |
                          v
              +-------------------------+
              | 2) Resolve features     |
              |    + complexity budget  |
              +-----------+-------------+
                          |
                          v
              +-------------------------+
              | 3) Map canonical tokens |
              |    via mapping contract |
              +-----------+-------------+
                          |
                          v
              +-------------------------+
              | 4) Populate templates   |
              |    for 4 ecosystems     |
              +-----------+-------------+
                          |
                          v
              +-------------------------+
              | 5) Inject config schema |
              | 6) Inject permissions   |
              | 7) Inject minimal UI    |
              +-----------+-------------+
                          |
                          v
              +-------------------------+
              | 8) Emit scaffolds       |
              | 9) Emit compare report  |
              +-------------------------+
```

### Pseudocode

```text
function generate(specPath):
  spec = readJson(specPath)
  validate(spec, LAB_SPEC.v2)

  enforceConstraintBudget(spec.performance_budget)
  mapping = readJson(CANONICAL_MAPPING)

  resolved = resolveCanonical(spec, mapping)
  for platform in [kotlin, swift, flutter, react-native]:
    files = loadTemplates(platform)
    rendered = renderTemplates(files, resolved[platform])
    writeScaffold(platformOutputPath(spec.lab_id, platform), rendered)
    injectConfigSchema(spec.config_schema_version, platformOutputPath)

  report = buildComparisonReport(spec, resolved)
  write(reportPath(spec.lab_id), report)
```

---

## SECTION 5 - Drift Prevention System

Drift checks run after scaffold generation and during CI.

### Drift detectors

1. Feature parity detector
- Compare `canonical_features_used` to generated feature manifest per platform.
- Fail if any required canonical feature is missing.

2. Sensor mapping detector
- For each sensor in `sensors_used`, verify generated sensor adapter exists in all platforms.

3. Permission divergence detector
- Verify expected permissions map to build-time + runtime declarations in each platform scaffold.

4. Config parity detector
- Verify each platform includes same config keys and version.

5. Performance guard detector
- Verify generated benchmark config and thresholds match `performance_goal` and `performance_budget`.

### Drift manifest file (generated)

```text
artifacts/reports/drift/<LAB_ID>.drift.json
```

Fields:
- `missing_features`
- `missing_sensors`
- `permission_mismatch`
- `config_mismatch`
- `budget_violations`

---

## SECTION 6 - Difficulty Scaling Engine

| difficulty_level | Sensor count | Async complexity | State depth | Background | UI complexity | Config branching |
|---:|---|---|---|---|---|---|
| 1 | 0-1 | A0-A1 | local only | none | 2-4 components | 1-2 branches |
| 2 | 1 | A1-A2 | local + shared | optional timer only | 3-6 components | 2-3 branches |
| 3 | 1-2 | A2-A3 | shared + persistent | optional bounded worker | 4-8 components | 3-5 branches |
| 4 | 2-3 | A3-A4 | persistent + derived + streams | required bounded background | 5-10 components | 4-6 branches |
| 5 | 3-4 | A4 | multi-stream + failure recovery | required + lifecycle resilience | 6-12 components | 5-8 branches |

Scaling rules:
- increase only one major axis at a time where possible
- do not exceed budgets in `performance_budget`
- require explicit justification for level 4/5 background tasks and extra dependencies

---

## SECTION 7 - CLI Interface

Command surface:

```bash
mobile-systems-lab generate LAB_SPEC.v2.json
mobile-systems-lab compare LAB_ID
mobile-systems-lab benchmark LAB_ID
mobile-systems-lab mutate LAB_ID --sensor-add=gyro
```

### CLI behavior

`generate`
- validates spec
- generates platform scaffolds
- writes report and drift manifest

`compare`
- reads generated manifests and code metadata
- reports parity and divergence

`benchmark`
- runs per-platform benchmark scripts
- compares against `performance_goal`

`mutate`
- applies declarative mutation to existing spec
- re-generates scaffold and drift report

Minimal options:
- `--out-dir`
- `--dry-run`
- `--strict-budget`
- `--platforms=kotlin,swift,flutter,react-native`

---

## SECTION 8 - Mutation Engine

Mutation operations (deterministic and reversible):
- sensor-expanded: `--sensor-add=<sensor>` / `--sensor-remove=<sensor>`
- config-expanded: add/remove feature flags and branch cases
- async stress: escalate `async_complexity`
- background stress: toggle `background_processing_required`
- performance stress: tighten `performance_goal`

Mutation workflow:

```text
Read current spec -> apply mutation patch -> validate v2 -> regenerate -> run drift checks -> emit mutation report
```

Output:
- `artifacts/reports/mutations/<LAB_ID>.<timestamp>.md`

Safety limits:
- reject mutation if it violates `performance_budget`
- reject mutation if required permissions are absent for added sensors

---

## SECTION 9 - Output Structure

```text
artifacts/
  contracts/
    LAB_SPEC.v2.json
    LAB_SPEC.v2.migration-notes.md
    CANONICAL_MAPPING.json
  foundations/
    PROMPT_03_generation-engine.md
templates/
  kotlin/
  swift/
  flutter/
  react-native/
```

Monorepo integration targets (generated by engine, not manual):

```text
kotlin-android/labs/<LAB_ID>/
swift-ios/labs/<LAB_ID>/
flutter/labs/<LAB_ID>/
react-native/labs/<LAB_ID>/
artifacts/reports/<LAB_ID>-comparison.md
```

---

## Minimal Design Decisions
- one schema + one mapping contract + one template set per ecosystem
- no plugin marketplace, no dynamic runtime codegen, no heavy orchestration service
- strict parity/drift checks before accepting generated output
- keep each generated lab directly readable and editable in Vim/CLI

This is the compounding layer: **Spec -> Multi-Platform Implementation at scale**.
