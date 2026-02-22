# Prompt Manifest

## Conventions
- Authoritative prompt files currently include `_s` prompts for Stage-1 foundations and `.txt` prompts for Stage-2 execution.
- Prompt IDs are ordered lexically and executed in dependency order listed below.

## Stage-1 (Completed)
| Order | Prompt ID | File | Scope |
|---|---|---|---|
| 1 | PROMPT_00_s | `.prompts/PROMPT_00_s.txt` | System blueprint + roadmap |
| 2 | PROMPT_01_s | `.prompts/PROMPT_01_s.txt` | Canonical runtime model + LAB_SPEC v1 |
| 3 | PROMPT_02_s | `.prompts/PROMPT_02_s.txt` | LAB_01 implementation across 4 ecosystems |
| 4 | PROMPT_03_s | `.prompts/PROMPT_03_s.txt` | Generation engine design + LAB_SPEC v2 |
| 5 | PROMPT_04_s | `.prompts/PROMPT_04_s.txt` | Benchmark harness design |
| 6 | PROMPT_05_s | `.prompts/PROMPT_05_s.txt` | North Star app design |
| 7 | PROMPT_06_s | `.prompts/PROMPT_06_s.txt` | Complexity constitution |

## Stage-2 (Planned)
| Order | Prompt ID | File | Depends on | Primary focus |
|---|---|---|---|---|
| 8 | PROMPT_08 | `.prompts/PROMPT_08.txt` | Stage-1 complete | deterministic bring-up/check/teardown + spec input clarity |
| 9 | PROMPT_09 | `.prompts/PROMPT_09.txt` | PROMPT_08 | behavior-level tests + CI gates |
| 10 | PROMPT_10 | `.prompts/PROMPT_10.txt` | PROMPT_09 | benchmark real parsers + regression gate |
| 11 | PROMPT_11 | `.prompts/PROMPT_11.txt` | PROMPT_09 | generator quality + output contract |
| 12 | PROMPT_12 | `.prompts/PROMPT_12.txt` | PROMPT_10, PROMPT_11 | release hygiene + consistency + governance enforcement |

## Related Manifest
- Stage-2 execution detail and DoD: `.prompts/PROMPT_STAGE2_MANIFEST.md`
