# Device Testing Checklist

## Scope
Checklist for local physical-device testing without App Store or Play Store release.

## Android checklist

- [ ] Enable developer options (tap Build number 7 times).
- [ ] Enable USB debugging.
- [ ] Accept RSA fingerprint prompt.
- [ ] Verify connection:
```bash
adb kill-server && adb start-server
adb devices -l
```
- [ ] Install debug build:
```bash
./gradlew :app:installDebug
```
- [ ] Verify runtime permissions (location/camera/mic where applicable).
- [ ] Verify sensor streams start/stop on app lifecycle transitions.
- [ ] Test wireless debugging (optional):
```bash
adb tcpip 5555
adb connect <device_ip>:5555
```

## iOS checklist

- [ ] Enable Developer Mode on device and reboot.
- [ ] Connect device and trust this Mac.
- [ ] Add Apple ID in Xcode (Personal Team allowed).
- [ ] Set unique bundle identifier.
- [ ] Ensure signing team/profile resolves.
- [ ] Build to device:
```bash
xcodebuild -scheme <SchemeName> -configuration Debug -destination 'id=<DEVICE_UDID>' build
```
- [ ] Accept on-device trust prompt if needed.
- [ ] Validate permissions for sensors/camera/mic/location.

## Flutter checklist

- [ ] Validate toolchain:
```bash
flutter doctor -v
```
- [ ] Detect device:
```bash
flutter devices
```
- [ ] Run on physical device:
```bash
flutter run -d <device_id>
```
- [ ] Validate release build on device:
```bash
flutter build apk --release
flutter build ios --release
```

## React Native checklist

- [ ] Start Metro:
```bash
npx react-native start
```
- [ ] Android device bridge:
```bash
adb reverse tcp:8081 tcp:8081
npx react-native run-android
```
- [ ] iOS connected device:
```bash
npx react-native run-ios --device "<Device Name>"
```
- [ ] Validate production bundle path:
```bash
npx react-native bundle --entry-file index.js --platform android --dev false --bundle-output android/app/src/main/assets/index.android.bundle --assets-dest android/app/src/main/res
```

## Provisioning and certificates (iOS)

- Certificate: who signs the app.
- Provisioning profile: binds app ID + certificate + device list + entitlements.
- Development profile: for debug install to registered devices.
- Ad hoc profile: direct distribution to specific UDIDs.
- App Store profile: for TestFlight/App Store pipeline.

## Common error map

| Error | Cause | Fix |
|---|---|---|
| `device unauthorized` (Android) | RSA trust not granted | reconnect and accept prompt |
| `INSTALL_FAILED_VERSION_DOWNGRADE` | app version lower than installed | uninstall or bump version |
| `No provisioning profile found` (iOS) | signing mismatch | select valid team + bundle id |
| App launches then exits | missing permission/config crash | inspect logs, add guarded initialization |
| Sensor reads on emulator but not device | permission or hardware assumptions | verify runtime permission + availability checks |

## Logs and diagnostics

```bash
# Android
adb logcat | rg "E/|FATAL|ANR|permission"

# iOS (macOS log stream)
log stream --predicate 'process == "<AppName>"'

# Flutter
flutter logs

# React Native
npx react-native log-android
```

## Exit criteria per lab

- [ ] App installs and launches on real Android + iOS hardware.
- [ ] Required permissions requested only when feature is used.
- [ ] Sensor subscriptions stop on background/inactive states.
- [ ] Config import/export tested with valid and invalid JSON.
- [ ] Release build sanity check completed at least once before lab sign-off.

