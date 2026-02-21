# LAB_01_SENSOR_TOGGLE_APP (Flutter)

Minimal Flutter implementation using `ChangeNotifier`.

## Run (physical device)

```bash
# 1) Ensure Flutter SDK is installed and doctor is clean
flutter doctor -v

# 2) Fetch deps
flutter pub get

# 3) Connect device and run
flutter devices
flutter run -d <device_id>

# 4) Logs
flutter logs
```

## GPS simulation

```bash
# Android emulator example
adb emu geo fix -122.084 37.422
```

- iOS simulator: Xcode -> Debug -> Simulate Location.

## Verify sensor output

- Toggle Accelerometer ON and move device.
- Toggle GPS ON, grant permission, and verify coordinates update.
- Background app to verify paused state text.

## Config files

- Default config: `assets/config.json`
- Schema: `assets/config.schema.v1.json`
- Export path: app documents directory `lab01-config-export.json`

## Note

If this folder was not created by `flutter create`, generate platform folders once:

```bash
flutter create .
```

