# LAB_01_SENSOR_TOGGLE_APP (Kotlin Android)

Minimal Android native implementation using `ViewModel + Flow`.

## Run (physical device)

```bash
# 1) Connect Android phone with USB debugging enabled
adb devices -l

# 2) Build + install debug
gradle :app:installDebug

# 3) View logs
adb logcat | rg "lab01|FATAL|E/"
```

## GPS simulation

```bash
# For emulator only (replace coordinates)
adb emu geo fix -122.084 37.422
```

## Verify sensor output

- Toggle Accelerometer ON and move device; values should update.
- Toggle GPS ON (grant permission); location text should update.
- Put app in background; sensor rows show paused state.

## Config files

- Default config: `app/src/main/assets/config.json`
- Schema: `app/src/main/assets/config.schema.v1.json`
