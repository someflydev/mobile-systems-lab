# Swift Template Set

Purpose: scaffold minimal SwiftUI lab from `LAB_SPEC.v2`.

Primary placeholders:
- `{{LAB_ID}}`
- `{{APP_TITLE}}`
- `{{STATE_MODEL}}`
- `{{SENSOR_SUBSCRIPTION}}`
- `{{PERMISSION_REQUEST}}`
- `{{CONFIG_LOAD}}`
- `{{CONFIG_SAVE}}`
- `{{UI_COMPONENTS}}`
- `{{BACKGROUND_BLOCK}}`

Generation rule:
- Single `ObservableObject` view model for baseline labs.
- Sensor and permission logic isolated in small services.
