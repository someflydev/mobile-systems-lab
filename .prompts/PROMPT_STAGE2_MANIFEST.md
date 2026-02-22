# PROMPT Stage-2 Manifest

## Stage-2 Goals
- Raise completeness from current 68/100 toward 90+ by closing key P1 execution gaps.
- Raise excellence from 7/10 toward 8-9 by improving determinism, behavioral validation, and release hygiene.
- Implement the report’s highest-leverage improvement: real benchmark parsing + regression gating.
- Prevent complexity creep by preferring minimal scripts/tests over broad refactors.

## Stage-2 Definition of Done (DoD-S2)
- [ ] `./cli-tools/mobile-systems-lab generate artifacts/spec-examples/LAB_01_SENSOR_TOGGLE_APP.spec.v2.json --dry-run` exits 0.
- [ ] Schema misuse check: `./cli-tools/mobile-systems-lab generate artifacts/contracts/LAB_SPEC.v2.json --dry-run` exits non-zero with an actionable hint to `artifacts/spec-examples/`.
- [ ] Deterministic workflow exists and is idempotent: `bash scripts/dev/doctor.sh`, `bash scripts/dev/bringup_lab01.sh`, `bash scripts/dev/teardown_lab01.sh` all exit 0.
- [ ] `python3 -m unittest discover -s tests -v` passes.
- [ ] CI workflow runs the same core local checks (`make validate`, CLI smoke).
- [ ] Benchmark parsers ingest fixtures and emit `BENCHMARK_RESULT` payloads with `provenance` field.
- [ ] `./cli-tools/mobile-systems-lab benchmark LAB_01_SENSOR_TOGGLE_APP` produces unified metrics from parser-derived inputs.
- [ ] Regression check exists and fails on threshold breach for core metrics.
- [ ] Generator fails on unresolved template placeholders.
- [ ] Release hygiene baseline exists (`LICENSE`, `CHANGELOG.md`, prompt-output manifest).

## Planned Prompt Sequence
1. `PROMPT_08.txt` - Deterministic bring-up/check/teardown + spec input clarity.
- Why first: establishes stable developer execution surface and removes immediate CLI confusion.

2. `PROMPT_09.txt` - Behavior-level tests + CI gates.
- Why second: locks in correctness for new deterministic workflow and prevents regressions.

3. `PROMPT_10.txt` - Benchmark real parsers + regression gate.
- Why third: highest leverage improvement from Post-Flight report.

4. `PROMPT_11.txt` - Generator quality upgrades (runnable-lite + placeholder validation).
- Why fourth: improves generated scaffold utility after quality gates are in place.

5. `PROMPT_12.txt` - Release hygiene + naming consistency + governance enforcement.
- Why fifth: final hardening and consistency pass once core behavior is stable.

## Issue Coverage Mapping
- PF-001 (Flutter bootstrap variance): `PROMPT_08`, `PROMPT_11`
- PF-002 (benchmark stub limits): `PROMPT_10`
- PF-003 (generator not runnable enough): `PROMPT_11`
- PF-004 (reproducibility gaps): `PROMPT_08`, `PROMPT_09`
- PF-005 (release metadata missing): `PROMPT_12`
- PF-006/PF-007/PF-008 naming and orchestration drift: `PROMPT_09`, `PROMPT_12`

## Stop Condition
- If any prompt fails its acceptance criteria, stop Stage-2 execution immediately.
- Record failure details (command, stderr/stdout excerpt, touched files) in `.prompts/improvements-before-finalization.txt` before proceeding.
- Do not start the next Stage-2 prompt until the failing prompt is corrected and re-validated.

## Explicit Exclusion
- Front-facing website/frontend packaging work is excluded from Stage-2.
