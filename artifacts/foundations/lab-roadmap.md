# Lab Roadmap

## Objective
Deliver identical progressive labs across Kotlin Android, Swift iOS, Flutter, and React Native with strict baseline gates.

## Baseline gates
- Gate A: LAB 00 runs on physical device in all 4 ecosystems.
- Gate B: LAB 01 runs on physical device in all 4 ecosystems with config import/export.
- Gate C: First benchmark protocol recorded once (startup, memory, battery over 10 minutes).
- Gate D: Advanced extensions unlocked only after Gate B + Gate C.

## Timeline (6 weeks)

```text
W1: Foundations + LAB00 everywhere
W2: Device setup hardening + LAB01 everywhere
W3: LAB02 LAB03 LAB04 LAB05
W4: LAB06 LAB07 LAB08 LAB09
W5: LAB10 LAB11 LAB12 LAB13
W6: LAB14 LAB15 + comparative report + baseline freeze
```

## Weekly plan

### Week 1
- Finalize monorepo skeleton and CLI scripts.
- Implement LAB 00 in all stacks.
- Verify install/run on one Android and one iOS physical device.

### Week 2
- Implement LAB 01 in all stacks.
- Add config schema v1 and import/export path.
- Record first cross-stack sensor reliability notes.

### Week 3
- Implement LAB 02-05.
- Add unit tests for state transitions and validation.
- Verify persistent storage restart behavior on devices.

### Week 4
- Implement LAB 06-09.
- Add sampling/throttling defaults and lifecycle stop/resume checks.
- Validate camera permissions and background timer behavior.

### Week 5
- Implement LAB 10-13.
- Add schema migration hook and invalid config fallback UX.
- Run first performance and battery benchmarks (same scenario across stacks).

### Week 6
- Implement LAB 14-15.
- Produce per-stack unique capability demo and tradeoff report.
- Freeze baseline; document known limitations and next extensions.

## Progressive milestone checklist

| Milestone | Android | iOS | Flutter | React Native |
|---|---|---|---|---|
| M1 LAB00 done | [ ] | [ ] | [ ] | [ ] |
| M2 LAB01 done | [ ] | [ ] | [ ] | [ ] |
| M3 LAB02-05 done | [ ] | [ ] | [ ] | [ ] |
| M4 LAB06-09 done | [ ] | [ ] | [ ] | [ ] |
| M5 LAB10-13 done | [ ] | [ ] | [ ] | [ ] |
| M6 LAB14-15 done | [ ] | [ ] | [ ] | [ ] |

## Benchmark protocol (minimum)
- Startup: cold launch to interactive screen.
- Memory: average + peak during 10-minute LAB 01 session.
- Battery: delta over 10-minute LAB 01 session with same sampling settings.
- Stability: crash count and permission failure count.

## 12-month mastery trajectory

### Quarter 1 (Months 1-3)
- Complete all labs once in all stacks.
- Achieve repeatable device install/debug routines.

### Quarter 2 (Months 4-6)
- Re-implement labs with stricter architecture discipline.
- Improve test coverage and benchmark automation.

### Quarter 3 (Months 7-9)
- Add secure storage, privacy prompts, and offline conflict handling.
- Start comparative maintenance-cost tracking.

### Quarter 4 (Months 10-12)
- Build one production-grade mini app per stack.
- Publish final capability/performance matrix and architectural recommendations.

