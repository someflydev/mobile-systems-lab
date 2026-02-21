# Simplicity Score Rubric

Purpose:
- Rate proposed changes for labs, features, config schemas, and benchmark harness updates.
- Prevent complexity creep with a single comparable score.

Scoring scale:
- Lower is better.
- Total score range: 0 to 25.

## Dimensions (0-5 each)

1. Cognitive Load
- 0: immediately understandable in one read
- 1: minor new concept
- 2: moderate concept load
- 3: multiple interacting concepts
- 4: difficult to reason about without diagrams
- 5: high mental overhead / fragile understanding

2. File Count Impact
- 0: 0-1 file changed
- 1: 2-3 files
- 2: 4-6 files
- 3: 7-10 files
- 4: 11-15 files
- 5: >15 files

3. State Complexity Impact
- 0: stateless or local only
- 1: local with trivial persistence
- 2: shared state added
- 3: persistent + derived state interactions
- 4: multi-stream async state orchestration
- 5: background + recovery + multi-source state

4. Sensor Complexity Impact
- 0: no sensors
- 1: one sensor, low rate
- 2: one sensor with permission complexity
- 3: two sensors with throttling
- 4: multi-sensor concurrency near budget
- 5: background sensor orchestration

5. Runtime Impact
- 0: no measurable perf/battery effect
- 1: negligible impact
- 2: small measurable impact
- 3: moderate impact requiring tuning
- 4: high impact with regression risk
- 5: severe impact or threshold breach likely

## Total Score Bands

| Total | Classification | Policy |
|---:|---|---|
| 0-6 | Minimal | auto-approve if tests pass |
| 7-11 | Controlled | reviewer sign-off required |
| 12-16 | Elevated | requires written justification |
| 17-20 | High Risk | requires architecture review + rollback plan |
| 21-25 | Excessive | reject unless emergency fix |

## Object-Specific Guidance

## Lab
- Use full five dimensions.
- Must include drift checklist pass.

## Feature
- Weight cognitive and runtime dimensions most heavily in review notes.

## Config Schema change
- Emphasize branching and cognitive impacts.
- Any score >= 12 requires migration plan.

## Benchmark harness change
- Emphasize runtime and cognitive dimensions.
- Reject if it adds vanity metrics with no decision utility.

## Score Template

```text
Change ID:
Object Type: lab | feature | config | benchmark
Cognitive Load: X/5
File Count Impact: X/5
State Complexity Impact: X/5
Sensor Complexity Impact: X/5
Runtime Impact: X/5
Total: XX/25
Classification:
Decision:
Justification (if required):
```

