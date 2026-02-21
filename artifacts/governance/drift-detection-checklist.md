# Drift Detection Checklist

Apply this checklist before:
- merging a new lab
- adding a new dependency
- adding abstraction
- increasing config schema size
- adding new CLI commands

## A. New Lab Merge Checklist

- [ ] Canonical behavior matches lab spec across all four ecosystems.
- [ ] Config schema version and required keys are identical across ecosystems.
- [ ] Permission behavior includes explicit denied-path UX.
- [ ] Sensor start/stop rules are lifecycle-safe.
- [ ] File count and dependency count stay within complexity budget.
- [ ] Benchmark protocol eligibility is preserved (metrics can still be captured).

## B. Dependency Addition Checklist

- [ ] New dependency is strictly required for missing capability.
- [ ] Existing dependency or platform API cannot reasonably satisfy need.
- [ ] Third-party budget remains <= 3 per lab.
- [ ] Security/licensing risk reviewed.
- [ ] Performance impact measured on startup and memory.
- [ ] Removal fallback plan is documented.

## C. Abstraction Addition Checklist

- [ ] Repetition exists in 3+ locations.
- [ ] Proposed abstraction reduces total cognitive load.
- [ ] Indirection depth remains <= 2 hops.
- [ ] Platform-specific behavior is still visible where required.
- [ ] Debuggability is improved or unchanged.

## D. Config Schema Expansion Checklist

- [ ] Change is additive when possible.
- [ ] Branching factor remains <= 6 for current version.
- [ ] Defaults are deterministic.
- [ ] Migration path documented.
- [ ] Backward compatibility behavior specified.
- [ ] Invalid config path tested.

## E. CLI Command Addition Checklist

- [ ] Command solves repetitive high-value workflow.
- [ ] Existing commands cannot cover use case.
- [ ] Command output is deterministic and scriptable.
- [ ] Command complexity is bounded and documented.
- [ ] Drift/parity checks updated if needed.

## F. Performance Drift Gate

Fail merge if any are true without approved waiver:
- [ ] Cold start p95 regression > 15% from baseline.
- [ ] Idle memory p95 regression > 20%.
- [ ] Jank rate increases by > 1.5 percentage points.
- [ ] Battery drain exceeds threshold for baseline scenario.
- [ ] Sensor throughput drops > 20% unexpectedly.

## G. Decision Record Requirement

For any failed item that is accepted with waiver:
- [ ] Create a short decision note with owner and expiry date.
- [ ] Include mitigation plan and rollback trigger.

