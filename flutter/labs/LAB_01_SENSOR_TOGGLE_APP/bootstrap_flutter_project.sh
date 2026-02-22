#!/usr/bin/env bash
set -euo pipefail

if ! command -v flutter >/dev/null 2>&1; then
  echo "flutter SDK not found in PATH. Install Flutter first." >&2
  exit 1
fi

# Generates missing iOS/Android platform scaffolding deterministically for this lab folder.
flutter create . --platforms=android,ios --org com.mobilelab --project-name lab_01_sensor_toggle_app

echo "Flutter platform scaffolding refreshed. Next: flutter pub get && flutter run -d <device_id>"
