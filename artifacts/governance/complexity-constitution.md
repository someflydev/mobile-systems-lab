# Complexity Constitution - mobile-systems-lab

## Purpose
This document is the governing doctrine that protects the repository from overengineering while allowing controlled, evidence-based growth.

---

## Section 1 - Core Philosophy

## What this repo is
- A disciplined cross-platform mobile systems learning and implementation lab.
- A comparative runtime engineering workspace across Kotlin, Swift, Flutter, and React Native.
- A config-driven, CLI-first, physical-device-tested development environment.

## What this repo is not
- Not a startup MVP codebase.
- Not a feature velocity race.
- Not a framework collection or plugin marketplace.
- Not a vanity benchmark dashboard.

## Surface boundaries
- Learning surface:
  - Purpose: teach core mobile runtime principles and tradeoffs.
  - Output: minimal runnable labs and explicit architecture notes.
- Research surface:
  - Purpose: evaluate hypotheses with repeatable measurements.
  - Output: benchmark artifacts and comparative analysis.
- Product surface:
  - Purpose: evolve the North Star app under strict constraints.
  - Output: practical, offline-first, sensor-driven app increments.
- Automation surface:
  - Purpose: reduce repetitive setup while preserving understanding.
  - Output: scaffold generation, parity checks, drift detection.

---

## Section 2 - Complexity Budget

Budgets are hard limits unless escalation is approved.

| Budget Item | Limit | Scope |
|---|---:|---|
| Max dependency count per ecosystem lab | 12 total | includes first-party + third-party package declarations |
| Max third-party libraries per lab | 3 | excludes core SDK/framework packages |
| Max abstraction layers | 3 | UI -> state/effect -> adapter/storage |
| Max files per lab | 30 | excludes generated platform build metadata |
| Max architectural indirection depth | 2 hops | caller -> interface -> implementation; no chains |
| Max config branching factor | 6 flags/branches | per lab schema version |
| Max sensor concurrency | 2 active sensors | V1 baseline |
| Max background tasks | 1 bounded task | explicit lifecycle policy required |

## Changes that require written justification
- Any dependency beyond budget.
- Any new abstraction layer.
- Any file count over budget.
- Any additional sensor beyond allowed concurrency.
- Any background worker beyond one task.
- Any config schema expansion that increases branch count > 6.

Required justification payload:
- problem statement
- alternatives considered
- measured cost impact (startup/memory/battery)
- rollback plan

---

## Section 3 - Abstraction Rules

## Abstraction is allowed when
- The same logic is duplicated in 3+ places and semantic equivalence is proven.
- The abstraction reduces cognitive load and keeps call graph shallow.
- A single abstraction removes platform risk without hiding platform constraints.

## Duplication is preferable when
- Code is small, clear, and platform behavior differs.
- Shared abstraction would hide lifecycle/permission differences.
- Change frequency is low and readability is higher with explicit copies.

## Platform-specific code is embraced when
- OS capability is unique (background policy, sensors, permission UX).
- Native APIs are materially more reliable/performant.
- Cross-platform wrapper would reduce correctness or debuggability.

## Cross-platform uniformity is required when
- Canonical lab behavior, data contract, config schema, and measurement protocol must match.
- Result comparability would break if behavior diverges.

## Lab divergence rules
- A lab may diverge only at implementation details required by OS/runtime.
- A lab must stay canonical for feature intent, config contract, output semantics, and benchmark protocol.

---

## Section 4 - Performance Non-Negotiables

| Constraint | Baseline Target |
|---|---|
| Cold start p95 | <= 1500 ms |
| Warm start p95 | <= 700 ms |
| Idle memory p95 | <= 220 MB (debug baseline) |
| Streaming memory p95 | <= 300 MB |
| Frame time p95 | <= 16.67 ms |
| Jank rate | <= 2.0% |
| Config load p95 | <= 40 ms |
| Debug overhead ceiling | <= 25% delta vs profile mode |

## Sensor sampling discipline
- Accelerometer default 5-15 Hz.
- GPS default 1 update per 3-10 sec (balanced mode).
- Throttle at source before state updates.

## Battery thresholds
- <= 4% battery drain per 10 minutes for combined baseline sensor scenario.
- If threshold exceeded, reduce sampling before adding optimization complexity.

## Logging discipline
- Structured logs only for lifecycle, permissions, sensors, config, performance.
- No verbose continuous raw sensor logs in default mode.
- Log sampling required for high-frequency streams.

---

## Section 5 - North Star App Guardrails

## Must remain minimal
- Two core screens in V1.
- One primary action path per screen.
- No hidden multi-step setup flows.

## Must remain config-driven
- Runtime behavior controlled by versioned JSON config.
- Import/export paths mandatory.
- Safe fallback config required.

## Must not be abstracted away
- Lifecycle transitions.
- Permission denial paths.
- Sensor start/stop boundaries.
- Persistence boundaries.

## Must remain directly understandable
- Feature data flow must fit in one diagram.
- State ownership must be explicit and singular per concern.
- Any new module must justify why it cannot live in existing structure.

---

## Section 6 - Anti-Feature List

Prohibited by default:
- Mega state frameworks.
- Unnecessary DI frameworks.
- GraphQL layer.
- Plugin explosion.
- Premature sync engine.
- Backend coupling before explicit local-first limits are reached.
- Cross-platform forced UI uniformity at the expense of native quality.
- Benchmark vanity metrics without actionable decisions.

---

## Section 7 - Escalation Rules

Escalation is acceptable only with evidence and rollback path.

## Increase complexity
Allowed when:
- current budget prevents correctness, reliability, or measurably important UX/perf target.
- benchmark or bug data proves necessity.

## Add abstraction
Allowed when:
- repeated patterns across 3+ implementations are stable.
- abstraction reduces net complexity score (Section 9 rubric).

## Introduce new sensor types
Allowed when:
- user value is explicit.
- permission and battery impact are documented.
- benchmark profile updated.

## Introduce background tasks
Allowed when:
- foreground model demonstrably fails user requirement.
- task is bounded, cancellable, and policy-compliant.

## Introduce encryption
Allowed when:
- sensitive local data exists and threat model is documented.
- performance and key-management strategy are defined.

## Introduce sync
Allowed when:
- offline-first local model is stable.
- conflict model, privacy policy, and failure recovery are specified.
- deferred until North Star V1 parity and benchmark baseline are complete.

