# Front-Facing Ideas
## 1. Audience Positioning Options (2–3)

### Option A - Builder-first Runtime Lab
- Audience: senior builders comparing native and cross-platform mobile stacks.
- Positioning: "Spec-driven mobile systems repo with runnable baseline apps and measurable constraints."

### Option B - Platform Governance Kit
- Audience: platform leads, staff engineers, architecture councils.
- Positioning: "Cross-platform mobile architecture with explicit contracts, drift checks, and complexity budgets."

### Option C - Curriculum + Portfolio Track
- Audience: advanced learners and educators.
- Positioning: "A guided path from mental model to runnable multi-stack implementation, benchmarking, and product design."

## 2. README Final-Copy Directions (2–3 variants)

### A) Hacker/Builder Version
- Target audience: engineers who want immediate proof.
- One-liner value prop: "Build one mobile concept in four ecosystems, then measure and compare."
- Why this is different:
  - prompt lineage is explicit (`.prompts/`)
  - contracts are versioned (`LAB_SPEC.v1/v2`, benchmark schemas)
  - LAB_01 exists in Kotlin, Swift, Flutter, RN
  - CLI exists for generate/compare/benchmark/mutate
  - governance constraints prevent complexity drift
  - benchmark protocol is standardized and schema-backed
- Demo story:
  1. `make validate`
  2. `./cli-tools/mobile-systems-lab compare LAB_01_SENSOR_TOGGLE_APP`
  3. inspect `artifacts/reports/PROMPT_02_lab01-comparison.md`
  4. generate from v2 spec in dry-run
  5. emit unified benchmark metrics from stubs
- Proof points to include:
  - passing unit checks
  - CI workflow file
  - schema inventory count
- What NOT to promise yet:
  - full production-grade benchmark ingestion from native profilers

### B) Enterprise/Platform Version
- Target audience: teams needing governance and reliability.
- One-liner value prop: "A disciplined mobile systems platform that couples architecture intent to measurable outputs."
- Why this is different:
  - complexity constitution with explicit budgets
  - drift detection checklist and simplicity rubric
  - contract-first generation and benchmark schemas
  - cross-platform comparability as a hard constraint
  - product roadmap gated by benchmarks and parity
  - anti-feature doctrine reduces framework creep
- Demo story:
  1. review governance docs
  2. inspect v1->v2 migration notes
  3. inspect generation templates + mapping
  4. inspect benchmark protocol + normalized schema
- Proof points to include:
  - governance docs in `artifacts/governance/`
  - benchmark schemas and protocol checklist
- What NOT to promise yet:
  - release pipeline/compliance readiness (license/changelog still missing)

### C) Educator/Community Version
- Target audience: advanced bootcamp/internals training cohorts.
- One-liner value prop: "Learn mobile systems by building and evaluating one canonical app across four runtimes."
- Why this is different:
  - starts with mindset/runtime model before implementation
  - one canonical lab repeated across ecosystems
  - includes product and benchmark evolution layers
  - CLI-first/Vim-friendly artifact flow
  - explicit guardrails and escalation rules
- Demo story:
  1. read foundations docs
  2. run one platform of LAB_01
  3. compare architecture/perf implications
  4. explore North Star evolution plan
- Proof points to include:
  - structured prompt-to-artifact progression
  - generated contracts/templates and reports
- What NOT to promise yet:
  - beginner one-click setup across all platform toolchains

## 3. Productized Demo Flows (how someone experiences value fast)

### Flow 1 - 10-minute confidence check
1. `make validate`
2. `./cli-tools/mobile-systems-lab --help`
3. `./cli-tools/mobile-systems-lab compare LAB_01_SENSOR_TOGGLE_APP`
4. Open `artifacts/reports/PROMPT_02_lab01-comparison.md`

### Flow 2 - Spec-to-scaffold demo
1. Inspect `artifacts/contracts/LAB_SPEC.v2.json` example.
2. `./cli-tools/mobile-systems-lab generate <spec.json> --dry-run`
3. Review templates under `templates/*`.

### Flow 3 - Benchmark contract demo
1. Create four stub benchmark results via `cli-tools/benchmark_collect_stub.py`.
2. Run `./cli-tools/mobile-systems-lab benchmark LAB_01_SENSOR_TOGGLE_APP`.
3. Open unified output under `artifacts/benchmark/results/unified/...`.

## 4. Frontend Vision (MVP + v2 + anti-scope)

### MVP (1-2 weeks)
- Static-first Artifact Explorer site:
  - prompt lineage page (`PROMPT_00` -> `PROMPT_06`)
  - contract explorer cards for JSON schemas
  - LAB_01 per-platform runbook cards
  - governance summary panel (budget + escalation + anti-features)

### v2 (4-8 weeks)
- Interactive comparative UX:
  - prompt-to-artifact traceability table from machine-readable manifest
  - benchmark result viewer (UNIFIED_METRICS charts/tables)
  - generation preview panel (template placeholder resolution preview)
  - North Star roadmap gate tracker (V1..V6)

### Don't build yet (anti-scope)
- Cloud auth/multi-tenant management
- server-heavy dashboard backend
- full online mobile build farm UI
- plugin marketplace or extension store
- AI assistant embedded in docs as default UI

## 5. 5 Frontend Languages Considered (why + 2+ frameworks each)

### 1) TypeScript
- Fit: strongest docs/productization ecosystem and JSON tooling.
- Frameworks:
  - Astro
  - Next.js
  - SvelteKit
- Strength for this repo: fastest path from markdown/contracts to polished explorer.

### 2) Elm
- Fit: deterministic architecture aligns with repo discipline.
- Frameworks:
  - elm-pages
  - Lamdera
  - Browser + elm-ui SPA architecture
- Strength: very reliable state model for traceability UI.

### 3) Dart (Flutter Web)
- Fit: narrative continuity with Flutter track.
- Frameworks:
  - Flutter Web
  - Jaspr
- Strength: shared language story for mobile + web demos.

### 4) Kotlin (Kotlin/JS or Compose Multiplatform Web)
- Fit: strong for Kotlin-oriented platform teams.
- Frameworks:
  - Compose Multiplatform Web
  - KVision
  - fritz2
- Strength: coherent Kotlin-centric architecture narrative.

### 5) Rust
- Fit: robust and performant for heavy data visualizations.
- Frameworks:
  - Leptos
  - Yew
  - Dioxus
- Strength: excellent for high-integrity, schema-heavy UIs.

## 6. Recommended Frontend Stack (one clear pick) + Integration Plan

Recommended stack:
- **TypeScript + Astro (Starlight) + optional thin Node API layer for local CLI bridging**

Why:
- Best fit for current repo shape (many markdown + JSON artifacts).
- Minimal complexity for MVP static site.
- Easy incremental enhancement for v2 visualizations.

Integration plan:
- MVP:
  - static generation from `artifacts/**` and `.prompts/**`
  - no auth, no backend required
- v2:
  - optional local API wrapper to call `cli-tools/mobile-systems-lab`
  - render benchmark JSON files from `artifacts/benchmark/results/`
- deployment:
  - static on Vercel/Netlify
  - optional wrapper service on Fly.io/Render only if needed

## 7. Assets/Artifacts to Showcase (what the repo already has)

- Prompt lineage:
  - `.prompts/PROMPT_00_s.txt` ... `.prompts/PROMPT_06_s.txt`
- Runtime/architecture docs:
  - `artifacts/foundations/PROMPT_00_system_blueprint.md`
  - `artifacts/foundations/PROMPT_01_runtime-model.md`
  - `artifacts/foundations/PROMPT_03_generation-engine.md`
- Implemented baseline:
  - `kotlin-android/labs/LAB_01_SENSOR_TOGGLE_APP/`
  - `swift-ios/labs/LAB_01_SENSOR_TOGGLE_APP/`
  - `flutter/labs/LAB_01_SENSOR_TOGGLE_APP/`
  - `react-native/labs/LAB_01_SENSOR_TOGGLE_APP/`
- Contracts:
  - `artifacts/contracts/LAB_SPEC.v1.json`
  - `artifacts/contracts/LAB_SPEC.v2.json`
  - `artifacts/contracts/CANONICAL_MAPPING.json`
  - `artifacts/contracts/BENCHMARK_RESULT.schema.json`
  - `artifacts/contracts/UNIFIED_METRICS.schema.json`
- Product/Governance:
  - `artifacts/product/north-star-app-spec.md`
  - `artifacts/governance/complexity-constitution.md`

## 8. Packaging Polish Checklist (screenshots, gifs, examples, site deploy)

- [ ] Add one screenshot per ecosystem for LAB_01 running on device.
- [ ] Add short GIF showing sensor toggle + config import/export.
- [ ] Add schema explorer screenshots.
- [ ] Add benchmark visualization screenshot from unified metrics sample.
- [ ] Add explicit "what is real now" vs "planned next" matrix in README.
- [ ] Add LICENSE + CHANGELOG before public announcement.
- [ ] Publish static docs explorer MVP to Netlify/Vercel.

