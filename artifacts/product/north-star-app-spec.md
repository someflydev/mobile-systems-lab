# North Star App Spec

## Constraint Baseline
This design applies `PROMPT_06_s` rules:
- minimal screen count and file count
- bounded sensor concurrency (max 2 in V1)
- bounded background tasks (0 in V1)
- config-first behavior
- no heavy frameworks or speculative backend

---

## SECTION 1 - App Identity

## Candidate Concepts

1. **Motion-Tagged Focus Sessions**
- User starts/stops focus blocks.
- Accelerometer estimates movement intensity.
- GPS attaches coarse location context.
- Useful for understanding where focus quality drops.

2. **Geo-Motion Field Notes**
- Quick note capture with automatic movement and place metadata.
- Sensors enrich notes with context.
- Strong for journaling and field inspection workflows.

3. **Local Mobility Logbook**
- Passive local timeline of motion + location states.
- Designed for self-observation and habit feedback.
- Strong analytics potential but higher privacy sensitivity.

## Canonical Selection
**Motion-Tagged Focus Sessions** (canonical North Star)

Why:
- real daily utility
- two sensors used meaningfully (accelerometer + GPS)
- simple but expandable data model
- offline-first by default
- clear config import/export surface
- easy to compare across ecosystems without synthetic complexity

---

## SECTION 2 - Core Features (V1)

## Primary Screen: `Session`
- session timer status (idle/running)
- Start/Stop button
- current movement intensity (low/medium/high)
- current place snapshot (lat/lon coarse or named zone)
- instant status banner (permission/config/sensor state)

## Secondary Screen: `History`
- list of completed sessions (start, end, duration, intensity summary, place summary)
- export data JSON button
- import config JSON button

## Data Model (V1)
- `SessionRecord`
  - `id`
  - `started_at`
  - `ended_at`
  - `duration_sec`
  - `movement_score_avg`
  - `movement_level`
  - `location_anchor`
  - `sample_count`
- `RuntimeStatus`
  - `sensor_state`
  - `permission_state`
  - `last_config_version`
- `AppConfig`
  - feature flags
  - sampling intervals
  - storage limits

## Config Schema
- canonical file: `artifacts/contracts/north-star-config.schema.v1.json`
- loaded on startup, validated, fallback to defaults when invalid

## Sensor Interactions
- accelerometer: periodic movement score updates
- GPS: coarse location anchor updates while session active

## Permission Model
- location when-in-use required for GPS feature
- motion permission where platform requires it
- denied path: session runs with reduced context (movement-only or manual place)

## Export/Import Flow
- export config JSON and session data JSON from secondary screen
- import config JSON from file picker
- validate schema version before apply

## Background Behavior (V1)
- no persistent background logging
- if app backgrounds during active session:
  - suspend sensor streams
  - mark session as interrupted
  - resume only when app foregrounds

## Performance Targets (V1)
- cold start p95 <= 1500ms
- frame time p95 <= 16.67ms
- idle memory p95 <= 220MB (debug baseline cross-platform)
- battery drain <= 4% per 10 min in combined sensor mode

---

## SECTION 3 - Sensor Intelligence Design

## Accelerometer Use
- derive `movement_score` from magnitude deltas
- convert score into bands:
  - `low`
  - `medium`
  - `high`

## GPS Use
- capture coarse location anchor every configured interval during active session
- avoid high-frequency route tracking in V1

## Sampling Rates (default)
- accelerometer: 5 Hz
- GPS: every 5 sec (balanced accuracy)

## Battery Safety
- only sample while session is active and foregrounded
- auto-throttle accelerometer to 2 Hz when battery low
- pause GPS when battery saver mode detected (if available)

## Throttling Strategy
- source-level throttling (before state updates)
- render updates max every 500ms
- aggregate raw samples into short windows

## Event Storage Strategy
- store aggregated samples, not raw continuous stream
- per-session rolling aggregates:
  - average movement
  - max movement
  - sample count
  - first/last known location anchor

## Derived State
- `focus_stability_index` (0-100) from movement variance + session continuity
- `session_quality` label from duration + movement band

---

## SECTION 4 - Config-First Architecture

## Config Schema v1
- versioned JSON
- strict field validation
- additive evolution policy

## Feature Flags
- `accelerometer_enabled`
- `gps_enabled`
- `dark_mode`
- `log_sensor_data`
- `show_focus_stability_index`

## Sampling Controls
- `accelerometer_hz`
- `gps_interval_sec`
- `ui_update_interval_ms`

## UI Customization
- theme mode (`system/light/dark`)
- compact mode toggle

## Storage Strategy
- local-first store for session records
- local config file for behavior policy
- export/import file-based, no server dependency in V1

## Versioning Strategy
- `schema_version = north_star_config.v1`
- future versions only additive or explicitly migrated
- preserve backward parsing for one major version window

## JSON Schema Example (illustrative)

```json
{
  "schema_version": "north_star_config.v1",
  "feature_flags": {
    "accelerometer_enabled": true,
    "gps_enabled": true,
    "dark_mode": false,
    "log_sensor_data": true,
    "show_focus_stability_index": true
  },
  "sampling": {
    "accelerometer_hz": 5,
    "gps_interval_sec": 5,
    "ui_update_interval_ms": 500
  }
}
```

---

## SECTION 5 - UX Principles

## Screen Minimalism Rules
- max 2 core screens in V1
- one primary action per screen
- no nested menus for critical session actions

## Rebuild Isolation
- separate volatile sensor state from stable UI config state
- only update sensor subcomponents when sensor values change

## State Ownership Rules
- single feature owner per concern:
  - session state owner
  - sensor adapter
  - config store
- no global mutable bag

## Motion/Animation Policy
- no decorative animations
- only functional transitions (screen push/pop)

## Instant Feedback Policy
- toggle or action responses visible within one frame
- permission denial always surfaced with explicit status message

---

## SECTION 6 - Cross-Platform Implementation Strategy

## Kotlin (Android)
- native lifecycle-aware sensor subscriptions
- ViewModel + Flow for predictable updates
- keep foreground-only sampling in V1

## Swift (iOS)
- SwiftUI + ObservableObject with strict scene lifecycle handling
- CoreMotion + CoreLocation for native quality sensor integration

## Flutter
- ChangeNotifier/ValueNotifier and plugin streams
- isolate rebuild boundaries to keep frame stability

## React Native
- useState/useEffect with source-throttled listeners
- keep sensor processing lightweight to avoid JS thread pressure
- offload heavy calculations to native side only if proven necessary

---

## SECTION 7 - Evolution Roadmap

- **V1**: Minimal smart sensor logging (sessions + movement + location anchor + config import/export)
- **V2**: Derived analytics (weekly stability trends, context summaries)
- **V3**: Background resilience (bounded resume-safe background behavior)
- **V4**: Secure local storage (encrypted session/config data)
- **V5**: Multi-device sync
- **V6**: Plugin extension system

Gating rule:
- V5 and V6 are deferred until V1 is runnable in all four ecosystems **and** benchmarked with `PROMPT_04` protocol.

Evolution ladder:

```text
V1 -> V2 -> V3 -> V4 -> V5 -> V6
 |     |     |     |     |
 |     |     |     |     +-- only after benchmarked parity
 |     |     |     +-------- security hardening after stable runtime
 |     |     +-------------- background only after V1 reliability baseline
 |     +-------------------- analytics after clean V1 data quality
 +-------------------------- minimal cross-platform parity baseline
```

---

## SECTION 8 - Why This App Matters

- aligned with repo purpose: demonstrates core mobile systems constraints through real utility
- demonstrates depth: lifecycle, permissions, sensors, persistence, config, performance
- strong portfolio piece: practical, measurable, privacy-conscious local-first tool
- expandable: clean path from V1 baseline to advanced capabilities
- avoids tutorial-ware trap: solves a real user task, not synthetic feature demos

