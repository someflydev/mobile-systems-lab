# LAB_01_SENSOR_TOGGLE_APP (React Native TypeScript)

Minimal React Native TS implementation using `useState/useEffect` (Expo runtime).

## Run (physical device)

```bash
# 1) Install deps
npm install

# 2) Start Metro (Expo)
npm run start

# 3) Android debug install (requires Android SDK)
npm run android

# 4) iOS debug install (requires Xcode full install)
npm run ios
```

## Logs

```bash
# Metro logs
npm run start

# Android logs
adb logcat | rg "ReactNative|Expo|FATAL"

# iOS process logs
log stream --predicate 'process CONTAINS "LAB_01_SENSOR_TOGGLE_APP"'
```

## GPS simulation

```bash
# Android emulator example
adb emu geo fix -122.084 37.422
```

- iOS simulator: Xcode -> Debug -> Simulate Location.

## Verify sensor output

- Toggle Accelerometer ON and move device.
- Toggle GPS ON and grant permission.
- Background app and verify paused status.

## Config files

- Default config: `assets/config.json`
- Schema: `assets/config.schema.v1.json`
- Export file path: app document directory `lab01-config-export.json`

