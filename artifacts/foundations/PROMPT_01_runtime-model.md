# PROMPT 01 - Canonical Runtime Model (Intellectual Constitution)

## Scope
This document defines a shared conceptual runtime layer for:
- Kotlin (Android)
- Swift (iOS)
- Flutter (Dart)
- React Native (TypeScript)

It is the base contract for future automated lab generation, CLI scaffolding, sensor experiments, config-driven apps, and cross-stack performance comparison.

No full codebase definitions here. Only canonical abstractions and small illustrative snippets.

---

## SECTION 1 - Canonical Mobile Runtime Model

### 1.1 Unified lifecycle model

```text
┌──────────┐      user/app start       ┌────────────┐
│ Not Live │ ─────────────────────────> │  Launching │
└──────────┘                            └─────┬──────┘
                                              │ init complete
                                              v
                                        ┌────────────┐
                                        │ Foreground │
                                        └─────┬──────┘
                                app hidden    │ user focus
                                              v
                                        ┌────────────┐
                                        │ Background │
                                        └─────┬──────┘
                                      OS may suspend/kill
                                   ┌──────────┴──────────┐
                                   v                     v
                            ┌────────────┐        ┌─────────────┐
                            │ Suspension │        │ Termination │
                            └─────┬──────┘        └─────────────┘
                                  │ resume intent
                                  v
                            ┌────────────┐
                            │ Foreground │
                            └────────────┘
```

Canonical lifecycle rules:
- Launch: minimal boot path only (config load, essential state, root screen).
- Foreground: interactive, high-frequency UI updates allowed.
- Background: execute only approved low-cost work.
- Suspension: in-memory state is not guaranteed; persist critical deltas early.
- Termination: design for restart from durable state, not process continuity.

### 1.2 Screen model

Canonical definitions:
- Screen: user-visible stateful route boundary.
- Navigation: transition policy between screens (push, pop, replace, modal).
- Route: addressable destination + parameters.
- Stack: ordered route history enabling back behavior.

```text
[Route A] -> [Route B] -> [Route C]
   ^                         |
   +----------- pop ---------+
```

Rules for labs:
- Each lab has one primary root route and optional detail route.
- Route params must be serializable.
- Back behavior must be explicit and deterministic.

### 1.3 View composition model

- Declarative style: UI is a function of state; preferred for consistency.
- Imperative style: direct mutation commands; use only for edge integrations.
- Tree model: all stacks ultimately build a view tree/hierarchy.
- Layout model: constraints/flex/stack-based layouts resolved each frame pass.

```text
State -> View Description -> Diff/Apply -> Pixels
```

### 1.4 State model

State categories:
- Local state: one screen/widget/view scope.
- Shared state: multi-screen/session scope.
- Persistent state: survives process death/restart.
- Derived state: computed from canonical state.
- Side effects: external interactions (IO, sensors, timers, network).

Normalized flow:

```text
Event -> Reducer/Handler -> New State -> Render
                |
                +-> Effect Runner -> Effect Result Event -> Reducer/Handler
```

Constraints:
- Keep canonical state minimal and serializable.
- Derived values should be recomputed, not stored when avoidable.
- Side effects must be idempotent or safely retryable.

### 1.5 Event model

Event classes:
- User events: taps, text input, gestures.
- System events: lifecycle transitions, connectivity, low battery.
- Sensor events: accelerometer, GPS, camera frames.
- Timer events: scheduled ticks, debounced actions, retries.

Event handling principles:
- Normalize all events into one internal event envelope.
- Timestamp and source-tag events for replay and debugging.
- Throttle or sample high-rate sensor events before state updates.

### 1.6 Permission model

Permission layers:
- Build-time declarations: manifests/entitlements/capabilities.
- Runtime requests: user grant/deny path.
- Policy constraints: OS privacy mode, approximate location, one-time grants.

Permission contract:
- Request just-in-time when feature is triggered.
- Always provide denied-path behavior.
- Cache permission status with short TTL, then re-check before critical calls.

### 1.7 Sensor model

Access modes:
- Pull-based: request current value on demand.
- Stream-based: periodic event stream.
- Callback-based: OS pushes updates as availability changes.

Unified sensor lifecycle:

```text
Declare -> Check Permission -> Start -> Sample/Throttle -> Consume -> Stop -> Dispose
```

### 1.8 Storage model

Storage tiers:
- Key-value: fast preferences/flags.
- File system: config export/import and structured blobs.
- Database: indexed/query-heavy domain data.
- Secure storage: credentials/secrets only.

Durability strategy:
- Save user intent quickly (write-ahead or immediate save for critical toggles).
- Use atomic writes for config export/import.
- Keep migration functions explicit and versioned.

### 1.9 Rendering model

Canonical rendering rules:
- Frame updates target 60fps baseline (`~16.67ms/frame`).
- Rebuild trigger should be narrow (component/screen-level isolation).
- Prefer diff-based reconciliation where available.
- Avoid full-tree rebuild cascades caused by broad state invalidation.

---

### 1.10 Layer diagram (normalized)

```text
+----------------------------------------------------+
|                 App Composition Layer              |
|   Routes | Screens | View Tree | Input Handlers    |
+---------------------------+------------------------+
                            |
+---------------------------v------------------------+
|                  State + Effect Layer              |
|   Local/Shared/Persistent State | Reducers | IO    |
+---------------------------+------------------------+
                            |
+---------------------------v------------------------+
|             Device Capability Adapter Layer        |
|   Permissions | Sensors | Storage | Background API |
+---------------------------+------------------------+
                            |
+---------------------------v------------------------+
|                   OS Runtime + Policies            |
|   Lifecycle | Scheduler | Battery | Privacy Model  |
+----------------------------------------------------+
```

### 1.11 Normalized vocabulary glossary

| Canonical term | Meaning | Constraint |
|---|---|---|
| `AppRoot` | First runtime entry boundary | Must initialize minimal dependencies only |
| `Screen` | Route-bound user surface | Serializable route params |
| `Route` | Address + arguments | Deterministic parser |
| `StateStore` | Canonical mutable state owner | Single write protocol per feature |
| `Effect` | Non-pure action | Must report completion/failure event |
| `PermissionGate` | Precondition for capability | Deny path mandatory |
| `SensorHandle` | Active sensor subscription | Must be stoppable/disposable |
| `StoragePort` | Abstract storage interface | Explicit durability guarantees |
| `Config` | Versioned external behavior policy | Validated before apply |
| `RenderBudget` | Per-frame execution budget | p95 frame time under target |

---

## SECTION 2 - Cross-Platform Abstraction Table

| Canonical Concept | Kotlin Android | Swift iOS | Flutter | React Native | Unique Quirks | Performance Implications |
|---|---|---|---|---|---|---|
| App root | `Application` + `Activity` entry | `@main App` / app delegate lifecycle | `main()` + `runApp()` | JS entry (`index.js/tsx`) + native host | RN has JS runtime boot gap; Android has activity recreation | Startup path depth strongly affects cold start |
| Screen | `Activity` / `Fragment` / Compose destination | SwiftUI view route / UIKit VC | Widget route/screen | Navigator screen component | UIKit/Activity lifecycle differs from declarative paradigms | Over-large screen state increases rebuild work |
| Navigation | Jetpack Navigation / intents | NavigationStack / UINavigationController | Navigator 1/2, Router | React Navigation/native stack | Deep-link handling differs by framework | Stack churn can trigger expensive re-init if not cached |
| State container | ViewModel + state holder (`StateFlow`, etc.) | `@State`, `@StateObject`, observable models | `StatefulWidget`, Provider/Riverpod/BLoC | Hooks/context/Redux/Zustand etc. | Ownership semantics vary widely | Incorrect ownership causes rerender storms |
| Async execution | Coroutines/dispatchers | Swift Concurrency (`async/await`, actors) | Futures/Streams/isolates | JS event loop + native modules/threads | RN single JS thread pressure is common bottleneck | Blocking main/JS thread drops frames |
| Sensor subscription | SensorManager/FusedLocation callbacks | CoreMotion/CoreLocation delegates | Plugin streams + platform channels | Native modules/events/plugins | Background sensor policies differ by OS/OEM | High-frequency streams must be sampled |
| File storage | App internal files + scoped storage | App sandbox/documents | `path_provider` + Dart IO | FS libs/native modules | External/shared file access policy differs | Sync IO on UI thread harms responsiveness |
| Permission request | Manifest + runtime permission APIs | Info.plist keys + runtime request APIs | plugin-level wrappers calling native | package APIs/native bridge | iOS requires usage strings; Android versions differ by API level | Permission retries/loops can degrade UX and funnel metrics |
| Background work | WorkManager/foreground service | BGTaskScheduler/background modes | plugin/channel to native schedulers | headless JS + native schedulers | iOS stricter scheduled windows; Android OEM kill behavior | Unbounded background work drains battery and may be throttled |
| Configuration injection | assets/raw JSON + DI + startup parse | bundled JSON + decode + environment injection | asset bundle JSON + provider injection | bundled JSON/remote config + context store | RN/Flutter can patch config quickly; native may use build variants | Parse and apply early but avoid heavy startup blocking |

Mapping rule for labs: canonical concept names in specs remain stable even when stack-specific implementation differs.

---

## SECTION 3 - LAB Spec Contract (`LAB_SPEC.v1.json`)

Contract file:
- `artifacts/contracts/LAB_SPEC.v1.json`

Required fields:
- `lab_id`
- `title`
- `canonical_features_used`
- `sensors_used`
- `storage_used`
- `state_complexity_level`
- `expected_runtime_constraints`
- `config_schema_version`
- `performance_goal`

Illustrative instance snippet:

```json
{
  "lab_id": "LAB_01",
  "title": "Sensor Toggle App",
  "canonical_features_used": ["lifecycle", "sensors", "config_import_export"],
  "sensors_used": ["accelerometer", "gps"],
  "storage_used": ["file_system", "key_value"],
  "state_complexity_level": "S4_streaming_effects",
  "expected_runtime_constraints": ["frame_budget_16ms", "battery_budget"],
  "config_schema_version": "config.v1",
  "performance_goal": {
    "startup_ms_p95_max": 1500,
    "frame_time_ms_p95_max": 16.67,
    "memory_mb_peak_max": 220,
    "battery_drain_percent_10min_max": 4.5
  }
}
```

Compatibility rule:
- `v1` is canonical base.
- Future `v2+` contracts may extend via additive fields or broader enums.
- Future versions must keep `v1` required keys and semantics stable unless a migration note explicitly defines a compatible transform.

CLI scaffolding implication:
- `lab_id` and `canonical_features_used` are enough to choose templates.
- `state_complexity_level` and `sensors_used` select default architecture wiring.

---

## SECTION 4 - Config-First App Blueprint

### 4.1 Blueprint runtime sequence

```text
Boot -> Load config.json -> Validate against config.schema.v1 -> Migrate if needed
     -> Build AppRoot with injected Config -> Enable declared sensors/features
     -> Run
```

### 4.2 Minimal blueprint components

- `ConfigLoader`: reads local config file or bundled default.
- `ConfigValidator`: validates against `config.schema.v1.json`.
- `ConfigMigrator`: applies deterministic version transforms.
- `FeatureRegistry`: enables/disables runtime features from config.
- `ConfigIO`: import/export with atomic file writes.

### 4.3 Schema artifact

Contract file:
- `artifacts/contracts/config.schema.v1.json`

### 4.4 Example default config

```json
{
  "schema_version": "config.v1",
  "ui": {
    "theme": "system",
    "density": "comfortable",
    "show_debug_panel": false
  },
  "features": {
    "import_export_enabled": true,
    "offline_mode_enabled": true,
    "background_timer_enabled": false
  },
  "sensors": {
    "accelerometer": { "enabled": true, "frequency_hz": 10 },
    "gps": { "enabled": false, "accuracy_mode": "balanced", "interval_seconds": 5 },
    "camera": { "enabled": false },
    "microphone": { "enabled": false },
    "battery_state": { "enabled": true }
  },
  "storage": {
    "mode": "key_value",
    "retention_days": 30
  },
  "runtime": {
    "target_fps": 60,
    "max_bg_work_minutes_per_hour": 5,
    "log_level": "info"
  }
}
```

### 4.5 Migration strategy concept

Migration contract:
- Each config has explicit `schema_version`.
- Migrations are pure, forward transforms: `vN -> vN+1`.
- Invalid migration leaves active config unchanged and emits a user-visible error.

Suggested migration steps:
1. Parse old version permissively.
2. Normalize defaults for missing fields.
3. Transform renamed or split fields.
4. Validate against target schema.
5. Persist migrated config atomically with backup.

---

## SECTION 5 - Sensor Capability Normalization

### 5.1 Canonical sensor interface

```text
Sensor {
  id: string
  permission_required: boolean
  event_frequency: "on_demand" | "low" | "medium" | "high"
  battery_cost_level: "low" | "medium" | "high"
  data_shape: object
}
```

### 5.2 Sensor mapping table

| Sensor | Canonical data_shape | Kotlin Android | Swift iOS | Flutter | React Native | Notes |
|---|---|---|---|---|---|---|
| Accelerometer | `{x: f32, y: f32, z: f32, ts_ms: i64}` | SensorManager events | CoreMotion updates | plugin stream via channels | plugin/native event emitter | Usually stream-based; sample to 5-20Hz for baseline labs |
| GPS | `{lat: f64, lon: f64, acc_m: f32, speed_mps?: f32, ts_ms: i64}` | FusedLocation callbacks | CoreLocation delegate | geolocation plugin | location plugin/native | High battery impact; respect foreground/background rules |
| Camera | `{session: string, frame?: bytes, ts_ms: i64}` | CameraX/Camera2 session callbacks | AVFoundation capture session | camera plugin | camera libs/native modules | Treat preview as lifecycle-heavy capability, not passive sensor |
| Microphone | `{level_db?: f32, chunk?: bytes, ts_ms: i64}` | AudioRecord/MediaRecorder callbacks | AVAudioEngine/session | audio plugin | audio libs/native | Privacy-sensitive; explicit user intent required |
| Battery state | `{level_pct: i32, charging: bool, saver_mode?: bool, ts_ms: i64}` | BatteryManager + broadcasts | UIDevice/ProcessInfo notifications | battery plugin | native module/plugin | Event frequency low; cheap signal for adaptive behavior |

### 5.3 Permission normalization

| Sensor | Permission required | Foreground/background caveat |
|---|---|---|
| Accelerometer | Usually implicit (platform dependent) | Continuous high frequency may still be constrained |
| GPS | Yes | Background location has stricter policy on both OSes |
| Camera | Yes | Background use is generally restricted |
| Microphone | Yes | Background recording has strict policy and disclosure requirements |
| Battery state | Usually no explicit prompt | API availability differs by platform version |

---

## SECTION 6 - Performance Contract (Snappy UX)

### 6.1 Contract values

- Max frame budget: `16.67ms` at 60fps baseline.
- Preferred p95 frame time: `<= 16.67ms`; stretch bound p99 `<= 24ms`.
- Cold start p95 target for baseline labs: `<= 1.5s` on reference mid-tier device.
- Sensor processing budget: no unthrottled high-frequency UI-bound updates.

### 6.2 Rebuild isolation strategy

- Keep fast-changing sensor state outside broad UI roots.
- Render from derived view models/selectors at component granularity.
- Preserve immutable update discipline to improve diff/reconciliation accuracy.

### 6.3 Async isolation strategy

- Keep CPU-heavy work off main/UI thread.
- Use structured concurrency primitives (coroutines, Swift concurrency, isolates, native modules/workers).
- Avoid synchronous disk/network on render-critical paths.

### 6.4 Background work limits

- Background jobs must be bounded, cancellable, and policy-compliant.
- Never assume continuous background execution.
- Backoff and coalesce periodic work to reduce wakeups.

### 6.5 Logging strategy

Log classes:
- `runtime.lifecycle`
- `runtime.permission`
- `runtime.sensor`
- `runtime.storage`
- `runtime.performance`

Log rules:
- Structured logs with timestamp, lab_id, route, event_type.
- Sample noisy streams (e.g., 1 in N sensor events).
- Strip sensitive fields before persistence/export.

### 6.6 Crash recovery pattern

```text
Crash/kill detected -> reload last durable state + config -> show recovery banner
                  -> replay safe queued intents if idempotent -> continue
```

Recovery requirements:
- Persist critical state deltas before background transition.
- Maintain small crash-safe checkpoint file.
- Guard startup with schema/version validation before state replay.

---

## SECTION 7 - Architectural Decision Flow

### 7.1 Decision tree

```text
Start
 |
 +-- Need deep platform-specific capabilities (services, intents, widgets, ARKit, Shortcuts)?
 |      |
 |      +-- Android-heavy -> Choose Kotlin native
 |      |
 |      +-- iOS-heavy -> Choose Swift native
 |
 +-- Need one shared codebase with near-native rendering consistency?
 |      |
 |      +-- High UI/animation consistency required across platforms -> Choose Flutter
 |
 +-- Team strongest in JS/TS and high release velocity needed?
 |      |
 |      +-- Yes -> Choose React Native
 |
 +-- Sensor intensity very high + strict frame budgets + complex background policies?
 |      |
 |      +-- Prefer native (Kotlin/Swift) unless strong prior Flutter/RN native-bridge expertise
 |
 End
```

### 7.2 Weighted selection guide

| Decision factor | Kotlin native | Swift native | Flutter | React Native |
|---|---|---|---|---|
| Sensor intensity (high) | Strong | Strong | Medium-Strong (with channels) | Medium (bridge pressure) |
| UI complexity (custom) | Strong | Strong | Strong | Medium-Strong |
| Animation depth | Strong | Very strong on iOS | Strong | Medium-Strong with Reanimated/native |
| Raw performance need | Strong | Strong | Strong | Medium-Strong |
| Small team shared stack | Weak | Weak | Strong | Strong |
| Release velocity (cross-platform) | Weak-Medium | Weak-Medium | Strong | Strong |
| Native ecosystem leverage | Very strong Android | Very strong iOS | Medium | Medium |

Decision policy for this repo:
- Build all four to learn runtime tradeoffs.
- Use canonical spec contracts so each lab remains comparable.
- Keep features minimal and measurable before adding abstraction layers.

---

## Foundation for Automation and CLI Scaffolding

How this constitution feeds automation:
- `LAB_SPEC.v1.json` drives lab template selection and required features.
- `config.schema.v1.json` guarantees cross-platform config parity.
- Canonical vocabulary maps spec terms to stack-specific implementations.
- Performance contract provides common benchmark assertions.

Minimal CLI scaffolding inputs (conceptual):
- `lab_id`
- `target_stack`
- `state_complexity_level`
- `sensors_used`
- `config_schema_version`

Expected outputs:
- Folder skeleton.
- Route/state/effect stubs.
- Sensor adapter stubs.
- Config loader/validator stubs.

---

## Closing Canonical Statement

This document plus the two contract schemas form the baseline constitution of `mobile-systems-lab`.
Future prompts should treat these as normative references when generating:
- Progressive labs
- Runnable examples
- Sensor experiments
- Config-driven apps
- Comparative performance tests

