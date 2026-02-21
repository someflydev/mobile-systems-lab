# LAB_01_SENSOR_TOGGLE_APP (Swift iOS)

Minimal SwiftUI implementation using `ObservableObject`.

## Run (physical device)

```bash
# 1) Open in Xcode and set Team/Signing once
open LAB01SensorToggleApp.xcodeproj

# 2) Optional CLI build to connected device (replace scheme and device id)
xcodebuild -project LAB01SensorToggleApp.xcodeproj -scheme LAB01SensorToggleApp -configuration Debug -destination 'id=<DEVICE_UDID>' build

# 3) Stream logs
log stream --predicate 'process == "LAB01SensorToggleApp"'
```

## GPS simulation

- Physical device: move device outdoors or use Xcode location simulation while debugging.
- Simulator: Xcode -> Debug -> Simulate Location.

## Verify sensor output

- Toggle Accelerometer ON and move the device.
- Toggle GPS ON and grant location permission.
- Move app to background; values switch to paused state.

## Config files

- Default config: `LAB01SensorToggleApp/Resources/config.json`
- Schema: `LAB01SensorToggleApp/Resources/config.schema.v1.json`

