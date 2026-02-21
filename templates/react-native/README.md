# React Native Template Set

Purpose: scaffold minimal React Native TypeScript lab from `LAB_SPEC.v2`.

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
- Use `useState/useEffect` baseline unless spec explicitly asks for reducer model.
- Keep platform-specific branches isolated in small adapter modules.
