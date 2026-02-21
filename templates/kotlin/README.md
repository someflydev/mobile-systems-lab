# Kotlin Template Set

Purpose: scaffold minimal Android native lab structure from `LAB_SPEC.v2`.

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
- Keep one ViewModel, one sensor adapter, one permission adapter, one config adapter.
- Do not add additional architectural layers unless spec budget explicitly allows it.
