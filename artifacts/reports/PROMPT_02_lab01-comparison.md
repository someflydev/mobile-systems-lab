# PROMPT_02 - LAB_01_SENSOR_TOGGLE_APP Cross-Platform Reference

## Scope
Implemented one canonical lab (`LAB_01_SENSOR_TOGGLE_APP`) in four ecosystems with minimal architecture and shared behavior:
- load `config.json` at startup
- toggles for accelerometer + GPS
- live sensor values when enabled
- config export/import
- persistent last toggle state
- lifecycle-aware sensor start/stop

## Shared Config Contract

Schema version: `v1`

Feature flags in all implementations:
- `accelerometer_enabled`
- `gps_enabled`
- `dark_mode`
- `log_sensor_data`

Primary schema examples:
- `kotlin-android/labs/LAB_01_SENSOR_TOGGLE_APP/app/src/main/assets/config.schema.v1.json`
- `swift-ios/labs/LAB_01_SENSOR_TOGGLE_APP/LAB01SensorToggleApp/Resources/config.schema.v1.json`
- `flutter/labs/LAB_01_SENSOR_TOGGLE_APP/assets/config.schema.v1.json`
- `react-native/labs/LAB_01_SENSOR_TOGGLE_APP/assets/config.schema.v1.json`

Default config examples:
- `kotlin-android/labs/LAB_01_SENSOR_TOGGLE_APP/app/src/main/assets/config.json`
- `swift-ios/labs/LAB_01_SENSOR_TOGGLE_APP/LAB01SensorToggleApp/Resources/config.json`
- `flutter/labs/LAB_01_SENSOR_TOGGLE_APP/assets/config.json`
- `react-native/labs/LAB_01_SENSOR_TOGGLE_APP/assets/config.json`

---

## Kotlin Android (ViewModel + Flow)

### Repo Tree (example)

```text
kotlin-android/labs/LAB_01_SENSOR_TOGGLE_APP/
  settings.gradle.kts
  app/
    build.gradle.kts
    src/main/AndroidManifest.xml
    src/main/assets/config.json
    src/main/assets/config.schema.v1.json
    src/main/java/com/mobilelab/lab01/
      MainActivity.kt
      MainViewModel.kt
      SensorRepository.kt
      PermissionManager.kt
      ConfigRepository.kt
      LabConfig.kt
```

### Key design snippet

```kotlin
// MainViewModel.kt
fun onForegroundChanged(isForeground: Boolean) {
    this.isForeground = isForeground
    if (isForeground) syncSensors() else stopSensors()
}
```

```kotlin
// SensorRepository.kt
fun accelerometerFlow(): Flow<AccelReading> = callbackFlow { ... }.sample(300L)
```

### Physical device testing

```bash
adb devices -l
gradle :app:installDebug
adb logcat | rg "lab01|FATAL|E/"
```

GPS simulation:
```bash
adb emu geo fix -122.084 37.422
```

Verify sensor output:
- toggle accelerometer on and move device
- toggle GPS on and grant permission
- background app and confirm paused status text

### Performance contract notes
- Rebuild triggers: `UiState` Flow updates only on relevant state changes.
- Frame budget awareness: sampled accelerometer (`300ms`) + GPS (`1000ms`) updates.
- Throttling: `Flow.sample(...)` in sensor repository.
- Battery note: sensors stop on `onStop`, avoiding background drain.

---

## Swift iOS (ObservableObject + SwiftUI)

### Repo Tree (example)

```text
swift-ios/labs/LAB_01_SENSOR_TOGGLE_APP/
  LAB01SensorToggleApp.xcodeproj/
  LAB01SensorToggleApp/
    LAB01SensorToggleAppApp.swift
    ContentView.swift
    AppViewModel.swift
    SensorService.swift
    ConfigStore.swift
    LabConfig.swift
    Info.plist
    Resources/config.json
    Resources/config.schema.v1.json
```

### Key design snippet

```swift
// AppViewModel.swift
func onSceneActive(_ active: Bool) {
    isForeground = active
    syncSensors()
}
```

```swift
// SensorService.swift
motionManager.accelerometerUpdateInterval = 0.3
locationManager.startUpdatingLocation()
```

### Physical device testing

```bash
open LAB01SensorToggleApp.xcodeproj
xcodebuild -project LAB01SensorToggleApp.xcodeproj -scheme LAB01SensorToggleApp -configuration Debug -destination 'id=<DEVICE_UDID>' build
log stream --predicate 'process == "LAB01SensorToggleApp"'
```

GPS simulation:
- Xcode debug location simulation (simulator)
- physical device movement for real GPS updates

Verify sensor output:
- toggle accelerometer and move device
- toggle GPS and grant when-in-use permission
- move app to background and confirm paused status

### Performance contract notes
- Rebuild triggers: `@Published` changes in `AppViewModel`.
- Frame budget awareness: update interval `0.3s` for accelerometer.
- Throttling: sensor service controls update frequencies at source.
- Battery note: explicit stop of both sensors when scene not active.

---

## Flutter (ChangeNotifier)

### Repo Tree (example)

```text
flutter/labs/LAB_01_SENSOR_TOGGLE_APP/
  pubspec.yaml
  lib/
    main.dart
    models/lab_config.dart
    services/config_service.dart
    services/permission_service.dart
    services/sensor_service.dart
    viewmodels/lab01_view_model.dart
  assets/config.json
  assets/config.schema.v1.json
  android/app/src/main/AndroidManifest.xml
  ios/Runner/Info.plist
```

### Key design snippet

```dart
// lab01_view_model.dart
void onLifecycleForeground(bool foreground) {
  _isForeground = foreground;
  _syncSensors();
  notifyListeners();
}
```

```dart
// sensor_service.dart
accelerometerEventStream(samplingPeriod: SensorInterval.uiInterval)
```

### Physical device testing

```bash
flutter doctor -v
flutter pub get
flutter devices
flutter run -d <device_id>
flutter logs
```

GPS simulation:
```bash
adb emu geo fix -122.084 37.422
```

Verify sensor output:
- toggles update values in live UI
- GPS permission denial path shows explicit status
- app background pauses sensor updates

### Performance contract notes
- Rebuild triggers: `AnimatedBuilder` bound to one `ChangeNotifier`.
- Frame budget awareness: sensor values are string-updated with source throttling.
- Throttling: accelerometer via UI interval; GPS by distance/accuracy settings.
- Battery note: `stopAll()` called on lifecycle background transitions.

---

## React Native TypeScript (useState/useEffect)

### Repo Tree (example)

```text
react-native/labs/LAB_01_SENSOR_TOGGLE_APP/
  App.tsx
  src/
    config.ts
    permissions.ts
    sensors.ts
  assets/config.json
  assets/config.schema.v1.json
  package.json
  app.json
```

### Key design snippet

```tsx
// App.tsx
useEffect(() => {
  void syncSensors();
  return () => {
    stopAccelRef.current?.();
    stopGpsRef.current?.();
  };
}, [config.feature_flags.accelerometer_enabled, config.feature_flags.gps_enabled, foreground]);
```

```ts
// sensors.ts
Accelerometer.setUpdateInterval(300);
await Location.watchPositionAsync({ accuracy: Location.Accuracy.High, timeInterval: 1000 }, ...)
```

### Physical device testing

```bash
npm install
npm run start
npm run android
npm run ios
adb logcat | rg "ReactNative|Expo|FATAL"
```

GPS simulation:
```bash
adb emu geo fix -122.084 37.422
```

Verify sensor output:
- accelerometer text updates while moving device
- GPS text updates after permission grant
- app state inactive/background forces paused labels

### Performance contract notes
- Rebuild triggers: `useState` updates for config/status/sensor text.
- Frame budget awareness: updates throttled at sensor source and effect dependencies.
- Throttling: `Accelerometer.setUpdateInterval(300)` + GPS watch interval.
- Battery note: subscriptions disposed on dependency/lifecycle changes.

---

## Comparison Tables

### Code size comparison

| Ecosystem | Approx source LOC | Notes |
|---|---:|---|
| Kotlin Android | 440 | ViewModel + repositories + Compose UI |
| Swift iOS | 372 | SwiftUI + ObservableObject + delegates |
| Flutter | 433 | ChangeNotifier + services + single UI entry |
| React Native TS | 340 | Hooks + Expo sensor/location modules |

### Sensor subscription differences

| Ecosystem | Accelerometer | GPS |
|---|---|---|
| Kotlin Android | `SensorManager` listener + Flow | `LocationManager` listener + Flow |
| Swift iOS | `CMMotionManager` callback | `CLLocationManager` delegate |
| Flutter | `sensors_plus` stream | `geolocator` stream |
| React Native TS | Expo accelerometer listener | Expo location watch subscription |

### Permission handling differences

| Ecosystem | Permission strategy |
|---|---|
| Kotlin Android | runtime request via `ActivityResultContracts.RequestPermission` |
| Swift iOS | `requestWhenInUseAuthorization` + Info.plist usage key |
| Flutter | `Geolocator.checkPermission/requestPermission` |
| React Native TS | `expo-location` foreground permission request |

### Config storage differences

| Ecosystem | Startup config source | Persistent toggle storage | Export/import |
|---|---|---|---|
| Kotlin Android | assets fallback + local file override | SharedPreferences + local json file | Android document picker URI read/write |
| Swift iOS | bundled resource + documents override | UserDefaults + local json file | SwiftUI fileImporter/fileExporter |
| Flutter | asset + documents override | SharedPreferences + local json file | documents file write/read |
| React Native TS | bundled json + documentDirectory override | AsyncStorage + local json file | Expo document picker + file system |

### Performance implications

| Ecosystem | Primary risk | Mitigation in implementation |
|---|---|---|
| Kotlin Android | frequent Flow emissions driving recomposition | `sample(...)` on sensor streams |
| Swift iOS | delegate callbacks causing frequent `@Published` updates | fixed update intervals + sensor stop on inactive |
| Flutter | broad `notifyListeners()` refresh | single-screen baseline + source throttling |
| React Native TS | JS thread pressure from high-frequency events | 300ms accelerometer interval + controlled effect deps |

### Development friction score (1 = lowest friction, 10 = highest)

| Ecosystem | Score | Why |
|---|---:|---|
| Flutter | 4 | consistent APIs and fast iteration once SDK is installed |
| React Native TS (Expo) | 5 | quick setup, but dependency version matching matters |
| Kotlin Android | 6 | native APIs are clear but permission + lifecycle details are verbose |
| Swift iOS | 7 | signing/provisioning adds non-code friction |

---

## Critical Reflection

- Cleanest implementation: **SwiftUI** and **Flutter** were the most concise for UI + state readability.
- Most boilerplate: **Kotlin Android** due to explicit manifest/build/lifecycle/permission wiring.
- Performance differences: **Kotlin/Swift native** have most direct runtime control; **React Native** is most sensitive to event frequency on JS thread.
- Easiest sensor access: **Kotlin** and **Swift** provide first-party APIs with deep control; **Flutter/RN** are easier initially but rely on plugin/runtime abstraction layers.
- Architectural lessons:
  - keep sensor logic outside UI and throttle at subscription source
  - persist only what must survive restart (toggle state + config)
  - treat lifecycle transitions as first-class runtime events
  - config-first boot path enables deterministic labs and cross-platform parity

This LAB_01 is the canonical baseline for future labs in `mobile-systems-lab`.
