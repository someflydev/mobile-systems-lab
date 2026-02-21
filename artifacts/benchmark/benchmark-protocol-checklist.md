# Benchmark Protocol Checklist

## Scope
Canonical benchmark protocol for `LAB_01_SENSOR_TOGGLE_APP` across:
- Kotlin Android
- Swift iOS
- Flutter
- React Native

Constraint alignment (`PROMPT_06_s`):
- no vanity metrics
- fixed protocol
- bounded tooling complexity
- explicit drift/regression gates

## A. Environment Lock

- [ ] Use same device class for all runs (`mid` recommended).
- [ ] Lock OS version per platform for full benchmark cycle.
- [ ] Disable auto-updates and adaptive battery modes.
- [ ] Close all non-essential background apps.
- [ ] Keep battery between 60% and 90% at start.
- [ ] Keep ambient temperature stable.
- [ ] Use identical test duration and sample interval for all platforms.

## B. Run Profile (default)

- [ ] `cold_start_runs = 7`
- [ ] `warm_start_runs = 7`
- [ ] `idle_window_sec = 120`
- [ ] `sensor_stream_duration_sec = 300`
- [ ] `background_window_sec = 120`
- [ ] `sample_interval_ms = 1000`

## C. Device Preparation

### Android

```bash
adb devices -l
adb reboot
adb wait-for-device
adb shell settings put global window_animation_scale 0
adb shell settings put global transition_animation_scale 0
adb shell settings put global animator_duration_scale 0
```

### iOS (physical)

```bash
xcrun devicectl list devices
# Reboot device manually or via Xcode device window before run
```

### Flutter runner setup

```bash
flutter doctor -v
flutter devices
```

### React Native runner setup

```bash
node -v
npm -v
```

## D. Fresh Install

### Kotlin Android

```bash
cd kotlin-android/labs/LAB_01_SENSOR_TOGGLE_APP
gradle :app:installDebug
adb shell pm clear com.mobilelab.lab01
```

### Swift iOS

```bash
cd swift-ios/labs/LAB_01_SENSOR_TOGGLE_APP
xcodebuild -project LAB01SensorToggleApp.xcodeproj -scheme LAB01SensorToggleApp -configuration Debug -destination 'id=<DEVICE_UDID>' build
```

### Flutter

```bash
cd flutter/labs/LAB_01_SENSOR_TOGGLE_APP
flutter pub get
flutter run -d <device_id>
```

### React Native

```bash
cd react-native/labs/LAB_01_SENSOR_TOGGLE_APP
npm install
npm run android   # or npm run ios
```

## E. Measurement Commands by Metric

### Android native / Flutter Android / RN Android

Cold start:
```bash
adb shell am force-stop <package>
adb shell am start -W <package>/<activity>
```

Warm start:
```bash
adb shell input keyevent KEYCODE_HOME
adb shell am start -W <package>/<activity>
```

Memory:
```bash
adb shell dumpsys meminfo <package>
```

CPU:
```bash
adb shell top -n 1 -o %CPU,%MEM,NAME | rg <package>
```

Frame stability:
```bash
adb shell dumpsys gfxinfo <package> framestats
```

Battery estimate:
```bash
adb shell dumpsys batterystats --reset
# run scenario
adb shell dumpsys batterystats <package>
```

Trace/profiler:
```bash
adb shell atrace --async_start gfx view sched freq idle am wm
# run scenario
adb shell atrace --async_stop > trace.txt
```

### iOS native / Flutter iOS / RN iOS

Build/run and profiling:
```bash
xcodebuild -scheme <Scheme> -configuration Debug -destination 'id=<DEVICE_UDID>' build
xcrun xctrace record --template 'Time Profiler' --output artifacts/benchmark/traces/<run>.trace --time-limit 60s --launch -- <app_binary_or_bundle>
xcrun xctrace record --template 'Energy Log' --output artifacts/benchmark/traces/<run>-energy.trace --time-limit 120s --launch -- <app_binary_or_bundle>
```

Logs:
```bash
log stream --predicate 'process CONTAINS "LAB01"'
```

sysdiagnose (manual capture when needed):
- Trigger sysdiagnose on-device immediately after anomaly and archive capture with run id.

### Flutter-specific

```bash
flutter run --profile -d <device_id> --trace-startup
flutter attach --debug-port <port>
```

Use DevTools for timeline/memory snapshots during fixed windows.

### React Native-specific

```bash
# Metro + app run
npm run start
npm run android   # or npm run ios

# Hermes profiling (if Hermes enabled)
# capture profile via Dev Menu / tooling and export with run id
```

Use Flipper + RN performance monitor for frame and memory snapshots.

## F. Scenario Execution Order (fixed)

- [ ] Scenario 1: Idle baseline (120s)
- [ ] Scenario 2: Accelerometer ON only (300s)
- [ ] Scenario 3: GPS ON only (300s)
- [ ] Scenario 4: Accelerometer + GPS ON (300s)
- [ ] Scenario 5: Background/foreground reliability cycle (120s)

## G. Export Artifacts

- [ ] Raw tool logs saved under `artifacts/benchmark/raw/<platform>/<run_id>/`
- [ ] Per-run JSON saved as:
  `artifacts/benchmark/results/<platform>/<LAB_ID>/<run_id>.BENCHMARK_RESULT.json`
- [ ] Unified normalized output saved as:
  `artifacts/benchmark/results/unified/<LAB_ID>/<benchmark_id>.UNIFIED_METRICS.json`

## H. Acceptance / Sanity

- [ ] At least 5 valid runs per platform after outlier filtering.
- [ ] Device context fields complete in each result file.
- [ ] No missing required metric arrays.
- [ ] Regression detector executed and alerts emitted.

