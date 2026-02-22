# mobile-systems-lab

Prompt-driven cross-platform mobile systems lab for Kotlin Android, Swift iOS, Flutter, and React Native.

## Current Status

- Foundations and runtime contracts: complete under `artifacts/foundations/` and `artifacts/contracts/`.
- Canonical implementation: `LAB_01_SENSOR_TOGGLE_APP` exists in all 4 ecosystems.
- Generation engine: minimal executable CLI added (`cli-tools/mobile-systems-lab`) using `templates/*` + `LAB_SPEC.v2`.
- Benchmark harness: schemas + checklist + minimal result collect/normalize tooling.

## Quickstart

```bash
# 1) Validate contracts and basic repo checks
make validate

# 2) CLI help
./cli-tools/mobile-systems-lab --help

# 3) Generate scaffold from a v2 spec (dry run)
./cli-tools/mobile-systems-lab generate artifacts/contracts/LAB_SPEC.v2.json --dry-run

# 4) Compare multi-platform presence for LAB_01
./cli-tools/mobile-systems-lab compare LAB_01_SENSOR_TOGGLE_APP
```

## Platform Run Commands (LAB_01)

### Kotlin Android
```bash
cd kotlin-android/labs/LAB_01_SENSOR_TOGGLE_APP
./gradlew :app:installDebug
```

### Swift iOS
```bash
cd swift-ios/labs/LAB_01_SENSOR_TOGGLE_APP
xcodebuild -project LAB01SensorToggleApp.xcodeproj -scheme LAB01SensorToggleApp -configuration Debug -destination 'id=<DEVICE_UDID>' build
```

### Flutter
```bash
cd flutter/labs/LAB_01_SENSOR_TOGGLE_APP
./bootstrap_flutter_project.sh
flutter pub get
flutter run -d <device_id>
```

### React Native
```bash
cd react-native/labs/LAB_01_SENSOR_TOGGLE_APP
npm install
npm run android  # or npm run ios
```

## Benchmark Tooling

Create per-platform stubs:

```bash
python3 cli-tools/benchmark_collect_stub.py --lab-id LAB_01_SENSOR_TOGGLE_APP --platform kotlin_android --out artifacts/benchmark/results/kotlin_android/LAB_01_SENSOR_TOGGLE_APP/run1.json
```

Normalize into unified metrics:

```bash
./cli-tools/mobile-systems-lab benchmark LAB_01_SENSOR_TOGGLE_APP
```

## Repo Index

- Prompt lineage: `.prompts/`
- Foundations: `artifacts/foundations/`
- Contracts: `artifacts/contracts/`
- Benchmark docs/results: `artifacts/benchmark/`
- Governance: `artifacts/governance/`
- North Star product: `artifacts/product/`
- Templates: `templates/`

