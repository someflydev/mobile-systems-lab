# Stage-2 Pre-Flight

## 1. Stage-2 Goal Alignment (mapped to report P0/P1)

### Inputs verified
- `POST_FLIGHT_REPORT.md` exists and defines current priorities (completeness `68/100`, excellence `7/10`).
- Stage-2 prompts exist: `.prompts/PROMPT_08.txt` ... `.prompts/PROMPT_12.txt`.
- `.prompts/PROMPT_STAGE2_MANIFEST.md` exists and remains aligned with the prompt sequence.
- `.prompts/PROMPT_MANIFEST.md` exists and lists Stage-1 + Stage-2 prompts.

### P0/P1 alignment summary
- Current report lists no P0 issues.
- Stage-2 prompt set directly targets P1 issues and the report’s highest-leverage improvement:
  - `PF-001` (Flutter/bootstrap/reproducibility variance): `PROMPT_08`, `PROMPT_11`
  - `PF-002` (benchmark parser maturity): `PROMPT_10`
  - `PF-003` (generator scaffold usefulness): `PROMPT_11`
  - `PF-004` (reproducibility / deterministic workflows): `PROMPT_08`, `PROMPT_09`
  - `PF-005` (release hygiene): `PROMPT_12`

### Alignment verdict
- **Strong alignment** to Stage-2 objectives (completeness and excellence uplift without frontend scope).
- Front-facing/frontend work remains explicitly excluded.

## 2. Prompt Dependency Graph

### Ordered Stage-2 prompts
1. `PROMPT_08.txt` - deterministic bring-up/check/teardown + spec input clarity
2. `PROMPT_09.txt` - behavior-level tests + CI gates
3. `PROMPT_10.txt` - benchmark parsers + regression gate
4. `PROMPT_11.txt` - generator quality + render validation (scratch output)
5. `PROMPT_12.txt` - release hygiene + naming consistency + governance enforcement

### Dependency graph (logical)
```text
POST_FLIGHT_REPORT.md
        |
        v
   PROMPT_08  --> spec examples + dev scripts + CLI schema-misuse error handling
        |
        v
   PROMPT_09  --> tests/CI lock in PROMPT_08 behaviors + manifest consistency
       / \
      v   v
PROMPT_10  PROMPT_11
  |          |
  |          +--> generator contracts + scratch-output validation + placeholder checks
  +--> parser fixtures + provenance + regression gate
       \   /
        v v
     PROMPT_12 --> release metadata + naming normalization + governance/hygiene enforcement
```

### Sequencing verdict
- **Safe and minimal**.
- No hidden circular dependencies detected.

## 3. Prompt-by-Prompt QA (issues + fixes)

### `PROMPT_08.txt`
Status: **Pass (ready)**

Verified improvements
- Added explicit `scripts/dev/check_lab01.sh` artifact and acceptance criterion.
- `doctor` requirement now permits `grep` fallback if `rg` is unavailable.
- Teardown safety is constrained to a dedicated temp root (`.tmp/stage2/`) with path guards.

Notes
- Good balance of determinism and minimalism.
- No front-facing scope leakage.

### `PROMPT_09.txt`
Status: **Pass (ready)**

Verified improvements
- Acceptance commands now use more portable `unittest` module invocation form.
- CI wording clarified from “fail on first failing suite” to “fail clearly on any failing suite.”

Notes
- Scope remains appropriately filesystem/CLI-only.

### `PROMPT_10.txt`
Status: **Pass (ready)**

Verified improvements
- Added parser package `__init__.py` artifact.
- Explicit fixture-to-results path wiring requirement added (`artifacts/benchmark/results/<platform>/<lab_id>/`).
- Added explicit requirement that parser tests cover all four platforms.
- Acceptance commands updated to `unittest` module form.

Notes
- `mktemp` usage is clearly labeled as Unix-shell oriented, which is acceptable for current repo CI assumptions.

### `PROMPT_11.txt`
Status: **Pass (ready)**

Verified improvements
- High-risk overwrite path removed: acceptance now uses scratch generation (`LAB_99_GENERATOR_SMOKE`) and `--out-root .tmp/stage2/generated`.
- Placeholder no-match check now uses correct shell semantics: `! rg -n ...`.
- Placeholder scan scope is restricted to scratch generated output.
- Generator contract naming aligned to schema style (`GENERATOR_OUTPUT.schema.v1.json`).

Notes
- Adds `--out-root`, which is a justified and minimal non-destructive enhancement.
- No overengineering signals beyond prompt scope.

### `PROMPT_12.txt`
Status: **Pass (ready)**

Verified improvements
- Stale-reference acceptance check is now enforcing (`! rg -n ...`).
- Prompt-output manifest minimum keys are explicitly defined.
- CI modification is now explicitly additive to `PROMPT_09` changes.
- Acceptance command updated to portable `unittest` module form.

Notes
- Scope remains release hygiene and governance enforcement only.

## 4. Acceptance Criteria Feasibility (CI-safe?)

### Overall assessment
- **CI-safe: Yes**, with the repository’s current constraints (no native device/emulator requirements in Stage-2).
- Commands are predominantly shell + Python + repo CLI.

### Feasibility summary by prompt
- `PROMPT_08`: CI-safe after `rg` fallback clarification and dedicated temp-root teardown rule.
- `PROMPT_09`: CI-safe; pure `unittest` + Makefile + CLI checks.
- `PROMPT_10`: CI-safe; fixture-driven parser tests and normalization only.
- `PROMPT_11`: CI-safe after scratch generation and `--out-root` requirement.
- `PROMPT_12`: CI-safe after enforcing `rg` no-match check.

### Remaining caveats (acceptable)
- Unix shell assumptions remain present (`bash`, `mktemp`, `rg`/`grep`), which is consistent with the repo’s current CLI-first workflow and CI (Ubuntu runners).

## 5. Naming / Path / Convention Alignment

### Verified alignment
- Stage-2 prompts target existing repo roots and conventions:
  - `.prompts/`, `artifacts/`, `cli-tools/`, `tests/`, `.github/workflows/`, `templates/`
- No frontend/site directories are introduced.
- `PROMPT_11` contract file naming now better matches schema conventions (`*.schema.v1.json`).

### Constraint note
- `docs/03` (referenced by this pre-flight task text) does not exist in current repo.
- Validation was performed against actual repo layout and `artifacts/foundations/repo-tree.monorepo.txt` conventions instead.

### Minor consistency suggestion (optional)
- `PROMPT_STAGE2_MANIFEST.md` DoD bullet for deterministic workflow currently lists `doctor`, `bringup`, `teardown` but not `check_lab01.sh`.
- This is not blocking (the prompt itself includes the check script), but adding it would improve symmetry.

## 6. Overengineering Risks + Guardrails Verification

### Guardrails verified
- Every Stage-2 prompt includes explicit anti-scope and overengineering guardrails.
- Frontend/front-facing work is excluded from all Stage-2 prompts and the Stage-2 manifest.
- New dependencies are not requested except optional fixture/parser code using stdlib/local scripts.
- Heavy refactors and meta-systems are explicitly avoided.

### Risk review
- `PROMPT_10` remains the heaviest prompt, but this is justified by the post-flight report’s highest-leverage improvement.
- `PROMPT_11` introduces `--out-root`, which is a minimal addition to prevent destructive generation and is therefore a net simplification/safety improvement.
- `PROMPT_12` governance enforcement remains path/JSON-parse based, not policy-engine based.

Verdict: **Overengineering risk is controlled.**

## 7. Recommended Edits (patch list) + Priority

### P3 (optional polish only)
1. Add `bash scripts/dev/check_lab01.sh` to DoD-S2 deterministic workflow bullet in `.prompts/PROMPT_STAGE2_MANIFEST.md` for symmetry with `PROMPT_08`.
- Impact: documentation consistency only.
- Blocking: No.

No additional P1/P2 prompt-text fixes are required before Stage-2 execution.

## 8. Go/No-Go Decision

### Decision
- **GO**

### Why
- Previously identified prompt-text blockers (destructive overwrite risk and non-enforcing acceptance checks) have been resolved.
- Acceptance criteria are now executable and materially aligned with current repo constraints.
- Sequencing is safe and minimal, and anti-scope/guardrails remain strong.

### Execution recommendation
- Execute Stage-2 strictly in order (`PROMPT_08` -> `PROMPT_12`) using the stop condition in `.prompts/PROMPT_STAGE2_MANIFEST.md`.
