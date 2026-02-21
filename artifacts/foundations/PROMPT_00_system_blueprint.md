# Mobile Systems Lab: Complete Platform Blueprint

## Purpose
Build a minimalist, CLI-first system for learning and shipping real mobile apps in:
- Kotlin (Android native)
- Swift (iOS native)
- Flutter (Dart)
- React Native (TypeScript/JavaScript)

Baseline rule: avoid overengineering; keep apps small, fast, and testable on physical devices without store release.

---

## SECTION 1 - MINDSET & MENTAL MODELS

### 1A. What app making actually is

App making is composing layers that operate at different rates and constraints.

```text
[User Intent]
    |
    v
[UI Layer] <-> [State Layer] <-> [Persistence Layer]
    |              |                 |
    v              v                 v
[Device Capability Layer]      [Communication Layer]
    |
    v
[Packaging + Distribution Layer]
    |
    v
[Runtime Constraints: battery/memory/cpu/network/policy]
```

- UI layer: renders a view tree from state and user interaction.
- State layer: source of truth for what the UI should show now.
- Device capability layer: sensors, camera, location, background jobs, notifications.
- Persistence layer: preferences, files, databases, secure storage.
- Communication layer: HTTP/WebSocket/BLE/NFC and retries.
- Packaging layer: signing, manifests, provisioning, installable artifacts.
- Runtime constraints: execution is governed by OS lifecycle, power policy, permissions, and thermal pressure.

### 1B. Desktop vs Web vs Mobile

| Dimension | Desktop | Web | Mobile |
|---|---|---|---|
| Resource budget | Usually larger | Browser-managed | Strict CPU/memory/power limits |
| Deployment | Installer/binary | URL refresh | Signed package + device policy |
| Permissions | Broad OS access | Browser API grants | Explicit runtime permissions + entitlements |
| Lifecycle | Long-running windows | Tab/session-based | Frequent pause/stop/recreate |
| Offline behavior | Usually possible | Depends on PWA/service worker | Must be intentional for resilience |
| Background work | Flexible | Very limited | OS-gated and quota/policy constrained |

### 1C. Mobile constraints that define architecture

- Limited CPU: bursty work is okay; sustained heavy loops trigger thermal throttling.
- Limited memory: aggressive process death can happen in background.
- Background execution limits: tasks need allowed channels (work managers, background fetch, foreground service).
- Permissions model: deny-by-default, revocable at runtime, sometimes one-time grants.
- Sandboxing: app-private files by default; cross-app access is policy controlled.
- Battery: radio, GPS, camera, and wakeups dominate power usage.

Practical implication: design for interruption, resumption, and graceful degradation first.

### 1D. Minimalist Vim Maniac App Builder philosophy

- CLI-driven setup: generate scaffolds with commands, not wizards.
- Manual file control: know where manifests, build files, and entry points live.
- Avoid IDE lock-in: IDE is optional for signing/provisioning edge cases.
- Inspect generated trees: never trust scaffolds blindly.
- Version-control everything: configs, scripts, schema, sample data, benchmark logs.
- Exportable configs: app behavior should be serializable and reproducible.

### 1E. Core design values

- Fast launch: first frame quickly; delay non-critical work.
- Minimal screens: fewer surfaces reduce bugs and cognitive overhead.
- Clear state flow: one directional updates where possible.
- Config-driven behavior: toggles and thresholds in JSON.
- Deterministic behavior: same input/config should produce same output.
- Offline-first when possible: local persistence before network dependency.

### 1F. Mobile architecture patterns (how to choose)

- MVC: simple apps, quick starts; risk of controller bloat.
- MVVM: common for SwiftUI/Android; clear binding between state and view.
- Unidirectional data flow: predictable updates and debugging.
- Redux-style: centralized store; excellent for time-travel/testing, can feel verbose.
- Provider pattern (Flutter): practical scoped dependency + state distribution.
- Observable state: native reactivity; lightweight for small modules.
- Hooks-based systems (React Native): composable behavior, easy co-location, watch for rerender noise.

Rule: start with unidirectional flow + small feature stores; add complexity only when forced.

### 1G. Unified cross-platform abstraction

```text
Screen      = route + lifecycle boundary
Widget/View = render unit
State       = serializable model of current UI + domain
Effect      = side effect (IO, sensor subscription, timer, network)
Permission  = runtime capability gate
Sensor      = stream source (accel/gps/etc)
Storage     = durable local state
Config      = versioned external policy for behavior
```

Canonical event loop:

```text
Intent -> Reducer/Handler -> New State -> Render
                      |
                      +-> Effect -> Result Event -> Reducer/Handler
```

---

## SECTION 2 - PHYSICAL DEVICE TESTING

Goal: install and test locally on real devices without store publishing.

### Android (Kotlin/Flutter/RN Android target)

1. Device setup
- On phone: Settings -> About phone -> tap Build number 7 times.
- Enable Developer options.
- Enable USB debugging.

2. Verify device + adb
```bash
adb kill-server && adb start-server
adb devices -l
```

3. Install debug build
```bash
# Native Android
./gradlew :app:installDebug

# Flutter
flutter devices
flutter run -d <device_id>

# React Native
adb reverse tcp:8081 tcp:8081
npx react-native run-android
```

4. Local signed builds (non-Play)
```bash
# Build release APK/AAB
./gradlew :app:assembleRelease

# Sign APK (example)
apksigner sign --ks ~/.keystores/mobilelab.jks app/build/outputs/apk/release/app-release-unsigned.apk
apksigner verify --verbose app/build/outputs/apk/release/app-release-unsigned.apk

# Install signed APK
adb install -r app/build/outputs/apk/release/app-release-unsigned.apk
```

5. Wireless debugging
```bash
adb tcpip 5555
adb connect <phone_ip>:5555
adb devices
```

Common Android issues:
- `device unauthorized`: accept RSA prompt on phone; reconnect cable.
- `INSTALL_FAILED_VERSION_DOWNGRADE`: uninstall existing or increment versionCode.
- `INSTALL_PARSE_FAILED_NO_CERTIFICATES`: APK unsigned or bad signature.
- `permission denied` on sensor/location: request runtime permission path in app.

### iOS (Swift/Flutter/RN iOS target)

1. Device setup
- iPhone: Settings -> Privacy & Security -> Developer Mode -> ON (reboot required).
- Trust Mac on first connection.

2. Provisioning with personal Apple ID
- Xcode -> Settings -> Accounts -> add Apple ID.
- Project -> Signing & Capabilities -> Team = Personal Team.
- Bundle identifier must be unique.

3. Install to device from CLI/Xcode toolchain
```bash
# List destinations
xcodebuild -scheme <SchemeName> -showdestinations

# Build for specific device
xcodebuild -scheme <SchemeName> -configuration Debug -destination 'id=<DEVICE_UDID>' build
```

4. Local IPA (ad hoc/internal)
```bash
# Archive
xcodebuild -scheme <SchemeName> -configuration Release -archivePath build/<App>.xcarchive archive

# Export IPA (requires ExportOptions.plist)
xcodebuild -exportArchive -archivePath build/<App>.xcarchive -exportPath build/ipa -exportOptionsPlist ios/ExportOptions.plist
```

5. TestFlight alternatives
- Direct install from Xcode to tethered devices.
- Ad hoc distribution (UDID-registered devices).
- Apple Configurator for supervised/local deployment.
- Internal MDM for organizations.

Common iOS issues:
- `No provisioning profile found`: team/signing mismatch.
- `Developer Mode required`: enable on device and reboot.
- `A signed resource has been added`: clean build folder and rebuild.
- `Untrusted Developer`: trust profile in device management settings.

### Flutter specifics

```bash
flutter doctor -v
flutter devices
flutter run -d <device_id>
flutter build apk --release
flutter build ios --release
```

Debug vs release:
- Debug: assertions, service protocol, hot reload.
- Release: optimized AOT/JIT-free path (platform dependent), realistic performance/battery testing.

### React Native specifics

```bash
# Start Metro
npx react-native start

# Android
adb reverse tcp:8081 tcp:8081
npx react-native run-android

# iOS (with connected device)
npx react-native run-ios --device "<Device Name>"

# Production JS bundle example
npx react-native bundle --entry-file index.js --platform ios --dev false --bundle-output ios/main.jsbundle --assets-dest ios
```

Debug server vs production bundle:
- Debug server (Metro): fast iteration, network dependency, slower runtime.
- Production bundle: local compiled assets, realistic startup and perf.

### Certificates and provisioning clarity

```text
Certificate: identity used to sign binaries.
Provisioning profile: policy document that binds
  - App ID (bundle id)
  - Certificate(s)
  - Device UDID list (dev/ad hoc)
  - Entitlements (capabilities)

Without this binding, iOS install/run fails.
```

### Device testing troubleshooting quick map

| Symptom | Likely cause | Fix |
|---|---|---|
| Device not listed | cable/driver/trust issue | reconnect, trust prompt, restart adb/Xcode |
| App installs but crashes on launch | missing runtime permission or fatal init | inspect logs and add guarded init |
| Works on emulator not device | sensor/hardware path differs | test real permission and hardware availability checks |
| Background task not running | OS policy restriction | use sanctioned APIs (WorkManager/BGTaskScheduler) |

---

## SECTION 3 - SYSTEM DESIGN FOR THE PLATFORM (MONOREPO)

### High-level monorepo shape

```text
/mobile-systems-lab/
  mindset/
  shared-concepts/
  kotlin-android/
  swift-ios/
  flutter/
  react-native/
  sensor-labs/
  config-patterns/
  device-testing/
  artifacts/
  cli-tools/
```

### Module intent

- `mindset/`: conceptual docs and architecture diagrams before code.
- `shared-concepts/`: platform-neutral definitions (state/effects/config schema).
- `kotlin-android/`, `swift-ios/`, `flutter/`, `react-native/`: ecosystem implementations.
- `sensor-labs/`: reusable sensor scenarios and expected behavior specs.
- `config-patterns/`: JSON schemas, migrations, sample configs.
- `device-testing/`: setup instructions, commands, troubleshooting runbooks.
- `artifacts/`: generated docs, benchmark records, review snapshots.
- `cli-tools/`: bootstrap scripts, common Make targets, log helpers.

### README philosophy structure

1. Why this repo exists (minimal mobile systems literacy).
2. Working style (CLI-first, Vim-friendly, deterministic configs).
3. Safety rails (small labs, measurable perf, physical-device checks).
4. How to run each ecosystem quickly.
5. Progress rules (no advanced extensions before baseline gates).

### Progressive lab structure in repo

Every ecosystem has identical lab folder names:

```text
labs/
  lab00_hello/
  lab01_sensor_toggle/
  ...
  lab15_unique_capability/
```

This allows direct comparison across stacks.

---

## SECTION 4 - PROGRESSIVE LAB STRUCTURE

## Canonical lab sequence (identical in all ecosystems)

| Lab | Objective | Required outputs | Gate |
|---|---|---|---|
| LAB 00 | Hello World Minimal Screen | single screen app, one action | app launches on physical device |
| LAB 01 | Sensor Toggle App | config load, accelerometer + GPS, import/export | sensor + config round trip works |
| LAB 02 | Stateful Counter | deterministic state updates | unit tests for reducer/state |
| LAB 03 | Form + Validation | input model, synchronous validation | invalid states blocked |
| LAB 04 | Persistent Storage | save/load local settings | survives restart |
| LAB 05 | Config-driven UI toggle | UI switches from JSON | no code change for toggle |
| LAB 06 | Accelerometer discipline | sampling + throttling | controlled event rate |
| LAB 07 | GPS discipline | accuracy mode + lifecycle stop/start | battery-aware updates |
| LAB 08 | Camera preview | permission + preview lifecycle | safe open/close |
| LAB 09 | Background timer | sanctioned background pattern | bounded behavior |
| LAB 10 | Export config JSON | file write + share/open | exported file valid |
| LAB 11 | Import config file | parse + schema validate + apply | invalid config rejected |
| LAB 12 | Performance tuning | rerender/rebuild minimization | measured improvement |
| LAB 13 | Battery awareness | high/low power mode behavior | reduced sampling under low power |
| LAB 14 | Offline-first example | local queue + sync later | works without network |
| LAB 15 | Unique capability demo | stack-specific feature | documented tradeoff |

### State diagram for labs 01/10/11

```text
[Default Config]
      |
      v
[Load Config] --invalid--> [Fallback + Error Banner]
      |
    valid
      v
[Active Config] --> [Sensor Manager Running]
      |                    |
  export json          emits events
      |                    v
      +--------------> [State Update] -> [UI Render]
```

### Small illustrative snippets (not full apps)

Kotlin (Android) - config read sketch:
```kotlin
val json = File(filesDir, "app-config.json").readText()
val cfg = json.decodeFromString<AppConfig>(json)
viewModel.applyConfig(cfg)
```

Swift (iOS) - config decode sketch:
```swift
let data = try Data(contentsOf: url)
let cfg = try JSONDecoder().decode(AppConfig.self, from: data)
store.apply(cfg)
```

Flutter (Dart) - stream discipline sketch:
```dart
accelSub = accelerometerEvents
  .sampleTime(const Duration(milliseconds: 200))
  .listen((e) => controller.onAccel(e));
```

React Native (TypeScript) - permission gate sketch:
```ts
const granted = await PermissionsAndroid.request(
  PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION
);
if (granted === PermissionsAndroid.RESULTS.GRANTED) startGps();
```

---

## SECTION 5 - UNIQUE LANGUAGE + DEVICE CAPABILITIES

### Kotlin + Android

Strengths:
- Deep system integration (intents, services, receivers).
- Foreground services for persistent user-visible work.
- Broadcast receivers for system event reactions.
- Custom launchers and intent filters for advanced flows.

Tradeoffs:
- Broad device fragmentation.
- OEM behavior differences in background policy.

Performance implication:
- High native performance; risk is lifecycle complexity, not runtime overhead.

Choose when:
- You need deep Android OS features, hardware access, or custom system interactions.

### Swift + iOS

Strengths:
- SwiftUI animation and rendering ergonomics.
- CoreMotion, ARKit, WidgetKit, Shortcuts integration.
- Tight hardware/software integration.

Tradeoffs:
- Apple signing/provisioning friction.
- Platform-specific APIs can reduce portability.

Performance implication:
- Excellent performance with predictable hardware targets.

Choose when:
- iOS-first product, premium UX, Apple ecosystem integrations.

### Flutter

Strengths:
- Skia-based rendering consistency across platforms.
- Single codebase UI with strong composition model.
- Platform channels for native escapes.

Tradeoffs:
- Larger binary sizes.
- Need careful bridge design for deep native features.

Performance implication:
- Strong UI throughput when widget rebuild scope is controlled.

Choose when:
- Shared product logic/UI across Android + iOS with consistent look.

### React Native

Strengths:
- JS ecosystem velocity.
- Excellent iteration speed and OTA-style conceptual workflows.
- Reanimated and native module bridges for advanced interactions.

Tradeoffs:
- Bridge complexity and dependency churn.
- Performance can degrade with heavy JS-thread work.

Performance implication:
- Great for many apps; needs disciplined render boundaries and native escapes for hotspots.

Choose when:
- Team has strong JS expertise and needs cross-platform speed with broad library access.

---

## SECTION 6 - SENSOR CAPABILITIES MATRIX

| Capability | Kotlin Android | Swift iOS | Flutter | React Native | Unique constraints | Permission model | Testing difficulty |
|---|---|---|---|---|---|---|---|
| Accelerometer | Native SensorManager | CoreMotion | plugin bridge/native | plugin bridge/native module | sampling rate must be throttled | usually no explicit runtime dialog for basic motion, platform rules apply | Medium |
| Gyroscope | SensorManager | CoreMotion | plugin/native | plugin/native | high-frequency streams can drain battery | similar to accelerometer | Medium |
| GPS | FusedLocationProvider | CoreLocation | geolocator-like plugin | community/native location libs | background location heavily restricted | explicit runtime + background declarations | High |
| Magnetometer | SensorManager | CoreMotion | plugin/native | plugin/native | noisy indoors, calibration needed | platform-specific | Medium |
| Camera | CameraX/Camera2 | AVFoundation | camera plugin | vision/camera libs | lifecycle + threading critical | runtime camera permission | High |
| Microphone | MediaRecorder/AudioRecord | AVAudioSession | audio plugins | audio libs/native modules | privacy-sensitive and background limits | runtime mic permission | High |
| NFC | Android NFC APIs | Core NFC | limited plugin support | limited plugin support | iOS feature scope narrower by use case | entitlement + runtime flow | High |
| Bluetooth | Android BLE stack | CoreBluetooth | flutter_blue-like plugins | BLE libs | scan throttling + background policy | runtime + sometimes location dependencies | High |
| Battery state | BatteryManager | ProcessInfo/UIDevice | battery plugin | native module/plugin | low-power mode semantics differ | generally no dialog | Low |
| File system | Scoped storage model | sandbox containers | path_provider etc | FS libraries/native | user-visible docs access differs | document picker/sandbox rules | Medium |
| Background processing | WorkManager/ForegroundService | BGTaskScheduler/background modes | via platform channels/plugins | headless JS/native services | strict quotas and kill policies | manifest/capability declarations | Very High |

---

## SECTION 7 - CONFIG EXPORT SYSTEM DESIGN

### Unified config contract

- Single JSON config controls feature toggles, sensor policy, UI behavior.
- Config is versioned and validated before apply.
- Invalid config never mutates live state; fallback defaults remain active.

### JSON schema (illustrative)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://mobile-systems-lab.local/schemas/app-config.v1.json",
  "type": "object",
  "required": ["version", "ui", "sensors", "sync"],
  "properties": {
    "version": { "type": "integer", "minimum": 1 },
    "ui": {
      "type": "object",
      "required": ["showAdvanced", "theme"],
      "properties": {
        "showAdvanced": { "type": "boolean" },
        "theme": { "type": "string", "enum": ["light", "dark", "system"] }
      }
    },
    "sensors": {
      "type": "object",
      "required": ["accelerometerHz", "gpsMode"],
      "properties": {
        "accelerometerHz": { "type": "integer", "minimum": 1, "maximum": 50 },
        "gpsMode": { "type": "string", "enum": ["off", "balanced", "high_accuracy"] }
      }
    },
    "sync": {
      "type": "object",
      "required": ["offlineQueueLimit"],
      "properties": {
        "offlineQueueLimit": { "type": "integer", "minimum": 10, "maximum": 10000 }
      }
    }
  }
}
```

### Example config

```json
{
  "version": 1,
  "ui": {
    "showAdvanced": false,
    "theme": "system"
  },
  "sensors": {
    "accelerometerHz": 10,
    "gpsMode": "balanced"
  },
  "sync": {
    "offlineQueueLimit": 500
  }
}
```

### Import/export flow

```text
Import file -> Parse JSON -> Validate schema -> Migrate if needed -> Dry-run apply -> Commit active config -> Persist backup
Export file <- Read active config <- Stamp metadata/date/schema id <- Write atomically
```

### Migration strategy

- Keep migrators as pure functions `vN -> vN+1`.
- Never mutate original file; write migrated copy.
- Track `sourceVersion`, `targetVersion`, `migratedAt` in metadata.
- Reject unknown major versions with explicit error.

Future-proofing rules:
- Additive changes preferred (new optional keys).
- Avoid semantic overload of existing fields.
- Preserve backward parser compatibility for at least 2 versions.

---

## SECTION 8 - PERFORMANCE & SNAPPY UX

### Principles

- Rebuild minimization: scope state updates to smallest subtree/component.
- State isolation: split volatile sensor data from stable UI config.
- Lazy loading: defer non-critical modules, camera init, heavy parsing.
- Render discipline: throttle sensor streams and batch updates.
- 60fps budget: ~16.6ms/frame end-to-end.
- Battery awareness: adapt sampling rates under low battery/thermal pressure.

### Profiling commands by ecosystem

Android/Kotlin:
```bash
./gradlew :app:assembleDebug
adb shell dumpsys gfxinfo <package_name>
adb shell top -o %CPU,%MEM,ARGS
adb logcat | rg "Choreographer|Skipped"
```

iOS/Swift:
```bash
xcodebuild -scheme <SchemeName> -configuration Release -destination 'id=<DEVICE_UDID>' build
xcrun xctrace list devices
xcrun xctrace record --template 'Time Profiler' --target-stdout -o build/trace.trace --launch -- <app_binary>
```

Flutter:
```bash
flutter run --profile -d <device_id>
flutter pub global run devtools
flutter build apk --analyze-size
```

React Native:
```bash
npx react-native start
npx react-native run-android --variant release
adb logcat | rg "ReactNative|Choreographer"
```

### Rebuild minimization checklist

- Use memoization/selectors for derived values.
- Keep sensor streams off main render path where possible.
- Avoid global state invalidating whole tree.
- Prefer immutable updates for predictable diffing.

---

## SECTION 9 - CLI-DRIVEN WORKFLOW

### Bootstrap scripts

- `cli-tools/bootstrap-all.sh`: verifies toolchains, clones templates, runs smoke checks.
- `cli-tools/new-lab.sh <stack> <lab>`: scaffolds consistent lab folder and README.
- `cli-tools/run-device.sh <stack>`: one command to run on first connected device.

### Makefile targets (top-level)

```make
bootstrap:
	./cli-tools/bootstrap-all.sh

check:
	./cli-tools/check-all.sh

run-android:
	./cli-tools/run-device.sh kotlin-android

run-ios:
	./cli-tools/run-device.sh swift-ios

labs:
	./cli-tools/list-labs.sh
```

### Vim-friendly navigation

```bash
rg --files | rg 'lab0[0-9]|lab1[0-5]'
rg "TODO|FIXME|permission|sensor" -n
rg "AppConfig|State|Reducer|ViewModel|Store" -n
```

### Grep-based debugging and logs

```bash
# Android
adb logcat | rg "E/|FATAL|ANR|permission"

# iOS (sim/device logs via mac tooling)
log stream --predicate 'process == "<AppName>"'

# Flutter / RN
flutter logs
npx react-native log-android
```

### Hot reload vs cold restart

- Hot reload: UI iteration and small logic edits.
- Hot restart: state reset with faster app relaunch.
- Cold restart: required for native module changes, manifest/entitlements, signing and permission declaration changes.

---

## SECTION 10 - ADVANCED EXTENSIONS (POST-BASELINE ONLY)

Do not implement before:
1. LAB 01 runnable on physical devices in all four ecosystems.
2. Benchmark protocol defined and recorded once (startup time, memory, battery for 10-minute sensor session).

Post-baseline candidates:
- Local-first sync engine.
- Multi-device merge/conflict strategy.
- Background sensor logging with retention policies.
- Privacy-first data minimization and explicit consent UX.
- Encrypted local storage with key rotation.
- Plugin-based mini app engine.
- Config-driven UI engine.
- Sensor-triggered automation rules.

---

## SECTION 11 - MILESTONES, DIAGRAMS, AND DELIVERABLE MAP

### Milestones

| Milestone | Completion criteria |
|---|---|
| M1 Foundations | Section docs + repo skeleton + LAB 00 all stacks |
| M2 Sensor baseline | LAB 01 all stacks on physical devices |
| M3 Persistence/config | LAB 04/05/10/11 complete with schema validation |
| M4 Runtime discipline | LAB 12/13 benchmarked and logged |
| M5 Comparative mastery | LAB 15 complete with tradeoff report |

### Cross-platform runtime diagram

```text
+---------------------- App Shell ----------------------+
| Screen Router | State Store | Effect Dispatcher       |
+----------------------+-------------------------------+
                       |
                       v
      +----------------+----------------+
      | Sensors | Storage | Network | BG |
      +----------------+----------------+
                       |
                       v
                OS Runtime Policies
         (permissions, battery, lifecycle)
```

### Lab roadmap timeline (summary)

```text
Week 1: Mindset + LAB00 (all stacks)
Week 2: LAB01 + device testing hardening
Week 3: LAB02-05 (state, forms, persistence, config UI)
Week 4: LAB06-09 (sensor/camera/background discipline)
Week 5: LAB10-13 (import/export + perf + battery)
Week 6: LAB14-15 + comparative review + baseline benchmark
```

### Proposed repo name

`mobile-systems-lab`

Alternative if you want stronger intent naming:
`lean-mobile-systems-lab`

### 6-week build schedule

1. Week 1: Create monorepo skeleton, write shared concepts, ship LAB 00 in all four stacks.
2. Week 2: Ship LAB 01 in all stacks on physical devices; establish permissions checklist.
3. Week 3: Ship LAB 02-05 with config schema v1 and validation tests.
4. Week 4: Ship LAB 06-09 with stream discipline and background constraints documented.
5. Week 5: Ship LAB 10-13 with export/import hardening and first perf+battery benchmark.
6. Week 6: Ship LAB 14-15, publish capability comparison, freeze baseline v1.0.

### 12-month mastery trajectory

- Months 1-2: Repeat LAB 00-05 until implementation speed and confidence are high.
- Months 3-4: Deep sensor lifecycle and permission edge cases; improve test stability on real devices.
- Months 5-6: Build offline-first queue + deterministic replay harness.
- Months 7-8: Add secure storage and privacy controls; threat-model data flows.
- Months 9-10: Build advanced background automation within OS policy limits.
- Months 11-12: Produce ecosystem comparison reports with measured benchmarks and maintenance cost analysis.

