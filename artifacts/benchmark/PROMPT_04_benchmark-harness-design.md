# PROMPT_04 - Cross-Platform Benchmark Harness Design

## Scope
Benchmark harness for `LAB_01_SENSOR_TOGGLE_APP` across:
- Kotlin Android
- Swift iOS
- Flutter
- React Native

Prerequisite applied: constraints from `.prompts/PROMPT_06_s.txt`.

Principles:
- measurable, reproducible, bounded complexity
- one unified protocol, platform-specific collectors
- no vanity metrics, no unbounded instrumentation scope

---

## SECTION 1 - What To Measure

| Metric | Measurement method | Sampling strategy | Normalization method | Tooling |
|---|---|---|---|---|
| Cold start time | launch from killed process to first interactive frame | 7 runs, discard top/bottom 1, use p50/p95 | normalize by device class and build type | Android `am start -W`, iOS Instruments launch metrics, Flutter `--trace-startup`, RN startup markers |
| Warm start time | relaunch from background/home to interactive frame | 7 runs, same filter | same as cold start | same tools as above |
| Memory footprint at idle | process memory after 120s idle | 1Hz samples for 120s | winsorize 5%, report p50/p95 MB | Android `dumpsys meminfo`, iOS Allocations/Memory report, Flutter DevTools memory, RN Flipper/Hermes heap |
| Memory during sensor streaming | memory under fixed sensor workload | 1Hz samples for 300s | same as idle | same tools |
| CPU usage idle | process CPU percentage at idle | 1Hz for 120s | percent normalized to one core equivalent | Android `top`, iOS Time Profiler, Flutter DevTools CPU timeline, RN profiler |
| CPU accel streaming | CPU with accelerometer ON | 1Hz for 300s | same as above | same tools |
| CPU GPS streaming | CPU with GPS ON | 1Hz for 300s | same as above | same tools |
| Frame rendering stability | jank frames + p95 frame time | collect framestats for entire scenario | jank rate = jank_frames/total_frames | Android `gfxinfo framestats`, iOS Core Animation instrument, Flutter frame timeline, RN perf monitor |
| Sensor throughput | delivered sensor events/time | count events from instrumented log tags | normalize to eps (accel) / epm (gps) | app-side counters + platform logs |
| Battery impact estimation | battery delta over fixed window + estimated per hour | per scenario start/end + OS energy trace | normalize to `%/hour` | Android batterystats/historian, iOS Energy Log, Flutter/RN via platform energy data |
| Background execution reliability | success rate of resume/background task cycle | 10 background-resume attempts | reliability_pct | app lifecycle markers + OS logs |
| Config load latency | config parse+validation time | capture at every startup run | p50/p95 in ms | app timer instrumentation + startup logs |

Notes:
- All metrics are kept because they directly map to runtime constraints in the canonical model.
- No additional secondary metrics unless required by a regression investigation.

---

## SECTION 2 - Platform-Specific Tooling

### Android (Kotlin / Flutter Android / RN Android)
- `adb shell am start -W`
- `adb shell dumpsys meminfo <package>`
- `adb shell dumpsys gfxinfo <package> framestats`
- `adb shell top -n 1 -o %CPU,%MEM,NAME`
- `adb shell atrace ...` (systrace/trace)
- `adb shell dumpsys batterystats --reset` + `dumpsys batterystats <package>`
- Battery Historian for post-analysis from batterystats bugreport

### iOS (Swift / Flutter iOS / RN iOS)
- Instruments (Time Profiler, Core Animation, Allocations, Energy Log)
- `xcrun xctrace record --template ...`
- Xcode profiler sessions
- `log stream --predicate ...`
- sysdiagnose for deep incident capture

### Flutter
- `flutter run --profile --trace-startup`
- Flutter DevTools (CPU, memory, timeline)
- Performance overlay for frame stability validation
- Timeline events exported from profile runs

### React Native
- Hermes profiling (if Hermes enabled)
- Flipper performance/memory plugins
- RN performance monitor for FPS
- Metro + device logs for startup and event counters

---

## SECTION 3 - Unified Benchmark Protocol

### Protocol steps
1. Prepare device/environment (same class, OS lock, no background apps).
2. Reboot device.
3. Install fresh debug/profile build and clear app data.
4. Execute cold-start runs.
5. Execute warm-start runs.
6. Run fixed sensor scenarios (idle, accel, GPS, combined).
7. Run background reliability cycle.
8. Export raw logs and metric capture.
9. Convert to `BENCHMARK_RESULT.json`.
10. Normalize into `UNIFIED_METRICS.json`.

Schema contracts:
- `artifacts/contracts/BENCHMARK_RESULT.schema.json`
- `artifacts/contracts/UNIFIED_METRICS.schema.json`

### Minimal benchmark runner pseudocode

```text
for platform in [kotlin_android, swift_ios, flutter, react_native]:
  prepare_device(platform)
  install_fresh_build(platform)
  raw = collect_metrics(platform, protocol)
  result = build_benchmark_result(raw)
  write_json(result)

unified = normalize_results(all_platform_results)
alerts = detect_regressions(unified, baseline)
write_unified(unified, alerts)
print_cli_summary(unified, alerts)
```

---

## SECTION 4 - Log Normalization

Input sources:
- Android logcat + dumpsys + trace
- iOS xctrace exports + system logs
- Flutter DevTools timeline/memory exports
- React Native profiler/Flipper exports

Normalization pipeline:

```text
Raw Logs -> Parse adapters -> Canonical metric events -> Outlier filter -> Units normalization -> Aggregation (p50/p95) -> Unified JSON
```

Normalization rules:
- Time in `ms`
- Memory in `MB`
- CPU in `%`
- Accel throughput in `events/sec`
- GPS throughput in `events/min`
- Battery in `%/hour`
- Winsorize extremes at 5% unless run count < 5

Output:
- `UNIFIED_METRICS.json` with exactly 4 platform entries

---

## SECTION 5 - Visualization Strategy

### CLI table output

```text
LAB_01_SENSOR_TOGGLE_APP  (scenario: combined_sensors)
platform         cold_p95  mem_idle_p95  cpu_gps_p95  jank%  battery%/h  score
kotlin_android   1420      164           18.2         1.3    3.8         89.1
swift_ios        1310      152           16.4         0.9    3.5         91.4
flutter          1560      188           21.1         1.7    4.2         84.0
react_native     1710      206           24.3         2.4    4.8         78.3
```

### ASCII performance bar chart (lower is better)

```text
Cold Start p95 (ms)
swift_ios      | ########### 1310
kotlin_android | ############ 1420
flutter        | ############## 1560
react_native   | ################ 1710
```

### Comparative summary report
- Top performer by metric
- Biggest regression from baseline
- Metrics requiring investigation

### Regression alerts
- CLI prints `WARNING` or `CRITICAL` with metric + delta.

---

## SECTION 6 - Drift & Regression Detection

Regression thresholds (default):
- cold start p95: warning `> +8%`, critical `> +15%`
- warm start p95: warning `> +10%`, critical `> +18%`
- idle memory p95: warning `> +10%`, critical `> +20%`
- sensor memory p95: warning `> +12%`, critical `> +22%`
- CPU p95 (idle/sensor): warning `> +10%`, critical `> +20%`
- jank rate: warning `> +0.8pp`, critical `> +1.5pp`
- accel throughput: warning `< -10%`, critical `< -20%`
- GPS throughput: warning `< -12%`, critical `< -25%`
- config load p95: warning `> +12%`, critical `> +25%`
- background reliability: warning `< -3pp`, critical `< -8pp`

Drift checks:
- metric missing from any platform result
- inconsistent unit conversion
- protocol mismatch (duration/sample interval differs)
- device class/OS mismatch

---

## SECTION 7 - Battery Reality Check

Battery scenarios (fixed 10-minute windows):
1. Accelerometer only
2. GPS only
3. Accelerometer + GPS

Estimation method:
- use OS battery/energy tooling deltas over window
- compute normalized `%/hour = delta_pct * (60 / test_minutes)`
- cross-check with CPU/memory spikes to identify confounders

Sampling interval tuning:
- default accelerometer sampling target: 5-15 Hz for lab baseline
- GPS interval target: 1-5 sec updates (balanced mode first)

Throttling strategy:
- enforce source-level throttling in sensor subscriptions
- pause sensor streams on background unless lab explicitly tests background streaming
- adaptive reduction under low battery/thermal warnings

---

## SECTION 8 - Scientific Discipline Rules

Hard rules:
- same device class per comparison set
- same OS version per comparison set
- same test duration and scenario order
- no foreground competing apps
- fixed sampling window and intervals
- fixed build type across platforms for a given report
- rerun if thermal state escalates beyond nominal/fair

Documentation requirements:
- record device model, OS, battery start/end, thermal state
- archive raw logs with run ID
- store protocol values with each result

---

## SECTION 9 - Output Artifacts

### Schemas
- `artifacts/contracts/BENCHMARK_RESULT.schema.json`
- `artifacts/contracts/UNIFIED_METRICS.schema.json`

### Checklist
- `artifacts/benchmark/benchmark-protocol-checklist.md`

### Sample BENCHMARK_RESULT snippet

```json
{
  "schema_version": "benchmark_result.v1",
  "benchmark_id": "bench_2026_02_21_001",
  "lab_id": "LAB_01_SENSOR_TOGGLE_APP",
  "platform": "kotlin_android",
  "summary": {
    "cold_start_ms_p50": 1280,
    "cold_start_ms_p95": 1420,
    "warm_start_ms_p50": 520,
    "memory_idle_mb_p50": 150,
    "memory_streaming_mb_p50": 168,
    "cpu_idle_pct_p50": 4.8,
    "cpu_accel_pct_p50": 8.9,
    "cpu_gps_pct_p50": 12.4,
    "config_load_ms_p50": 14
  }
}
```

### Sample UNIFIED_METRICS snippet

```json
{
  "schema_version": "unified_metrics.v1",
  "lab_id": "LAB_01_SENSOR_TOGGLE_APP",
  "scenario": "combined_sensors",
  "regression_alerts": [
    {
      "platform": "react_native",
      "metric": "cold_start_ms_p95",
      "baseline_value": 1550,
      "current_value": 1710,
      "delta_pct": 10.32,
      "severity": "warning"
    }
  ]
}
```

This harness turns the repo into a measurable comparative system while staying disciplined and minimal.
