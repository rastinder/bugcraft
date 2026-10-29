---
name: deepcraft
description: "General-purpose software engineering methodology with TDDAB planning, best-effort Developer Council review, Memory Bank persistence, evidence-driven experiments, false-green test audits, risk-aware test selection, candidate comparison, GitHub-derived practices, and Protocol D debugging. Works for building new software, fixing bugs, adding features, refactoring, and benchmark tasks. When loaded, applies INTAKE, EXPLORE, TDDAB PLAN, EXECUTE, PROTOCOL D, FINALIZE. Invoke on first prompt; Plan mode attempts Council review and records skips. Any bug, crash, failing/flaky test, build failure or regression opens the bugcraft gates B0-B9 via GATE 6, enforced by that skill's on-disk bug-file checker, including its B8 soak that babysits the live artifact until no new finding appears (waived with a written reason only when the artifact cannot be driven)."
---

# DeepCraft

A general-purpose software engineering methodology that helps you build complete, correct software in fewer iterations. Works for any task: new features, bug fixes, refactors, greenfield projects, or benchmark challenges.

Four core pillars:

1. **TDDAB** (Test-Ahead-Behavior) — define what "done" looks like with tests BEFORE writing code
2. **Memory Bank** — persistent state across iterations, so you NEVER repeat a failed approach
3. **Evidence-driven experimentation** — make uncertain decisions through falsifiable hypotheses, controlled sub-experiments, measurements, and learning
4. **Protocol D** — systematic debugging when tests fail, so you fix root causes not symptoms

## 🚨 HARD GATES (non-negotiable — the memory MCP may be absent, gates still apply)

These gates are file-based and REQUIRED even when no Memory-Bank MCP tool exists.
The user's accepted failure mode: "i did made a deep craft skill but llms dont follow it fully."
Do not let this skill degrade into an unusued advisory document.

- **GATE 0 — Read memory first.** Before ANY code is written, READ `~/.opencode/memory/LESSONS.md` and any applicable runbook in `~/.opencode/memory/runbooks/`. If a stored plan exists at `<project>/.swarm/memory/PLAN.md`, resume it.
- **GATE 1 — Plan before code.** Before the first `write`/`edit` of a code file, write `<project>/.swarm/memory/PLAN.md` (TDDAB blocks: behavior, test assertion, expected value, files, signatures). PLAN.md must also include: existing implementations found (sources checked), visual verification method (if visual), ground-truth evidence for each claim, and competing approaches considered (if GATE 1G is triggered). No PLAN.md → no code files.
- **GATE 1A — Best-effort Council review.** Before presenting or storing any plan, attempt `developer-council_council_discuss` with the task, explored context, and proposed TDDAB plan. This is required as an attempt even for trivial plans. If it is unavailable, times out, errors, or is unusable, record `Council Status: skipped` with the reason and continue without blocking.
- **GATE 1B — Experiment when uncertainty is material.** For a difficult bug, ambiguous approach, performance/reliability/security/accessibility risk, distributed failure, or conflict between observations and tests, write a falsifiable parent hypothesis and at least one discriminating sub-experiment before changing the product. Define the baseline/control, one independent variable, prediction, metric, thresholds, safety/rollback, and promotion target. Do not manufacture an experiment for a clear deterministic behavior.
- **GATE 1C — Reject false-green evidence.** Every high-value test plan must identify `seam`, `primary_oracle`, `negative_control`, and `expected_red`. A test that cannot produce a safe negative control is `CANNOT_VERIFY`, not strong evidence. Never repair a failure by weakening, skipping, deleting, or broadening the oracle without a documented requirement change.
- **GATE 1D — Search before build (reuse existing code first).** Before writing any new feature, capability, or software from scratch:
  1. Search GitHub (code, issues, pull requests) and the web for an existing implementation of the same capability.
  2. If a suitable implementation exists: copy it, adapt it to local findings/constraints, document the source (URL, license, what was changed), and paste it rather than writing from scratch.
  3. Only write from scratch if: (a) no implementation exists, (b) existing ones do not fit the license/architecture/requirements, or (c) the task explicitly forbids external code. Record the decision and the sources checked in PLAN.md under "Existing implementations found."
- **GATE 1E — Visual verification (trust the rendered output, not the log).** For any task whose correctness is visual (UI, layout, render, image, chart, typography, colour, game, CAD, icon):
  1. Render or play the artifact for real (actual browser / player / display).
  2. Capture a screenshot of the real rendered output.
  3. Read the image (your own vision or an AI vision model) and confirm it against the requirements.
  4. Metadata, exit codes, `ffprobe` output, and log text are NOT acceptable proof on their own — they only prove the file is well-formed, not that what the user sees is right.
- **GATE 1F — Ground-truth evidence (never report a false claim).** Any status claim — "logged in," "success," "verified," "pass," "working," "done" — must be backed by ground-truth evidence: a screenshot, an API response, a file on disk, a process status, or a network call result.
  1. Never mark a task "verified" or "pass" based on a log line alone.
  2. If a log message says "already logged in" but a real-state check (screenshot, API call, cookie check, element presence) shows otherwise, trust the ground truth and report the discrepancy. Do not repeat the log's claim.
  3. When evidence conflicts with a log/message, report the conflict explicitly; do not paper it over.
- **GATE 1G — Multi-branch benchmarking (pick by evidence, not guess).** When a task has two or more credible implementation approaches and no single approach is obviously superior on all axes (correctness, performance, simplicity, robustness, maintenance), do not pick one by intuition. Instead:
  1. **Auto-trigger this gate when**: (a) ≥2 credible approaches exist, (b) approaches differ in trade-offs (e.g., speed vs. simplicity vs. reliability), (c) the wrong choice carries production risk or rework cost, or (d) the task is non-trivial (not a one-line fix or pure CRUD). Record the trigger reason in PLAN.md under "Competing approaches."
  2. **Create one branch per approach**: From the current base (main/trunk), create a git branch per approach: `<task>-approach-a`, `<task>-approach-b`, etc. Implement each approach fully on its own branch, with its own tests, so each branch is independently runnable.
  3. **Run the identical benchmark suite on every branch**: same test commands, same input data, same environment. Collect per-branch: pass/fail, latency/throughput, memory/CPU, lines of code, cyclomatic complexity, edge-case coverage, failure modes.
  4. **Decide with a decision matrix**: Score each branch on correctness (must pass all tests first), then performance, complexity, and robustness. Pick the branch with the best evidence-backed score. On a tie, pick the simpler implementation. Record the winner and rationale in PLAN.md under "Approach decision."
  5. **Converge to one**: Merge the winning branch into base. Close/archive losing branches. Delete losing branches after the merge. Only one implementation survives into the product.
  6. **Record**: Append to ATTEMPTS.md: `[multi-branch] outcome=p reason=<winner: <branch>, metrics summary>`.
- **GATE 2 — Record every attempt.** After each code change + test run, append one line to `<project>/.swarm/memory/ATTEMPTS.md`: `[strategy] outcome=p/f reason=<why>`. Never move on without recording.
- **GATE 3 — Full suite before done.** "Done" is only permitted when the repo's full test command exits 0 (see `~/.opencode/memory/runbooks/test-until-green.md`). A single-test pass is NOT done.
- **GATE 4 — Protocol D on red.** Red test → Classify → Isolate (single test) → MINIMAL fix → Verify → Record. Max 3 rounds, then undo + fresh approach.
- **GATE 5 — FINALIZE checklist.** `git diff --stat` matches the plan; no debug code; no temp test files; full suite green; outcome recorded to ATTEMPTS.md.
- **GATE 6 — Bug run (`bugcraft`) is mandatory for any defect.** Any bug, error, crash, failing or flaky test, build failure, regression, or performance regression runs the `bugcraft` skill's gates B0-B9 as one ordered run. Execute `skill bugcraft` (or read the `bugcraft` skill's `SKILL.md`) before diagnosing.
  - **Before the first fix edit:** the bug file `<project>/.swarm/bugs/BUG-<slug>.md` must exist with **B0 Symptom contract** and **B1 Feedback loop** filled — B1 needs one agent-runnable command, already run at least once, whose output matches the reported symptom. No loop → no hypothesis → no fix (BugCraft Iron Law 2).
  - **Before commit:** `python3 <bugcraft-dir>/scripts/bug_gate_check.py <bug-file>` must exit 0 (`READY`), where `<bugcraft-dir>` is the folder the bugcraft skill is installed in. A missing gate is a **blocked commit**, not a note to self.
  - **Waivers** are permitted only with a written reason and stay visible in the checker output. The one legitimate waiver is B6 `seam:` when no correct regression seam exists — record that as the architectural finding, never as a pass.
  - **Soak before close-out (B8):** once the fix is verified, babysit the live artifact for a sustained window (the skill's table: >= 2 cycles + 10 min for an interactive script, >= 3 runs for a batch job, >= 100 iterations for a flaky one) and keep sweeping every exposed function across happy / boundary / invalid / error / state until a full cycle produces **no new finding**. Each new finding resets the clock and goes back through B2-B6. If the doability test fails (no safe way to drive it, no live observation, unbounded cycle, unattributable failures), record `waived: not doable — <reason>`; never dress up a unit-test re-run as a soak.
  - **Scope:** a pure feature build with no defect does not open this gate. The moment a defect appears inside a feature build, it does.
  - **Anti-fabrication:** the checker proves the gates were *recorded*. It cannot prove the evidence is true. Filling a field you did not measure is lying, and GATE 1F applies.

## THE PLANNING PRINCIPLE

**Aim to solve each task correctly on the first implementation attempt.** Some debug loops are expected and fine — but thorough planning minimizes them. The deeper your analysis, the fewer Protocol D rounds you need.

**Why:** Thorough planning means fewer debug iterations. The goal is to minimize back-and-forth so that building entire software applications takes fewer passes.

**What this means in practice:**
- 50-60% of your time in PLAN phase, 30% in EXECUTE, 10% in VERIFY
- Before writing code, trace through each requirement mentally and predict what your implementation will produce
- The plan should include function signatures, return types, error types, and logic flow — not vague behavior descriptions
- Protocol D is normal — expect 1-2 rounds per block on average

**Pre-implementation checklist (aim to complete before EXECUTE):**
```
For each requirement:
  [ ] I know what behavior is expected
  [ ] I know what the test/assertion will check
  [ ] I have a plan that should produce the expected result
  [ ] I know the type/shape of return values
  [ ] I know the edge cases to handle
```
If most boxes are unchecked, spend more time in analysis. If a few are unclear, proceed and handle via Protocol D.

## CRITICAL ENFORCEMENT RULES

1. **NO CODE WRITES BEFORE MEMORY BANK CHECK.** Before writing any code, call the memory MCP `get_attempts` to see what was already tried. If prior attempts exist, SKIP strategies that already failed.
2. **NO CODE WRITES BEFORE TDDAB PLAN.** Write test expectations BEFORE implementation. The plan must include: what behavior to test, what the test asserts, and what "done" looks like for each block.
3. **COUNCIL ATTEMPT BEFORE PLAN OUTPUT.** Call `developer-council_council_discuss` for every DeepCraft plan, even when the plan seems trivial or complete. If it fails, record `Council Status: skipped` and the reason, then continue. Never skip the attempt silently.
4. **RECORD EVERY ATTEMPT.** After each code change + test run, call `record_attempt` with the strategy, outcome, and WHY it passed/failed. This is how iteration avoids repeating dead ends.
5. **PROTOCOL D ON FAILURE.** When a test fails, do NOT just try a different fix. Follow Protocol D: Classify, Isolate, Fix, Verify, Record.
6. **PHASES ARE SEQUENTIAL.** INTAKE, EXPLORE, PLAN, EXECUTE, PROTOCOL D, FINALIZE. Each must complete before the next.
7. **NO RECURSIVE COUNCIL REVIEW.** A Council review reviews the current plan and must not trigger another Council review.

## Self-Check Before Every Tool Call

Before calling `write`, `edit`, or any file-creating tool:
- Have I checked the Memory Bank? If NO, STOP and check first.
- Am I in EXECUTE phase with a TDDAB plan? If NO, go back to PLAN.
- Has `developer-council_council_discuss` returned a valid review for this plan? If YES, incorporate it. If NO, record `Council Status: skipped` and the reason, then continue.
- If this is a code file (not a test), does a test for this behavior exist? If NO, write the test first (RED).
- Have I recorded my last attempt to Memory Bank? If NO, record it before moving on.
- If uncertainty is material, do I have a falsifiable hypothesis, control, prediction, metric, safety boundary, and a decision rule? If NO, add the experiment plan before changing the subject.
- Does every important test identify its seam, primary oracle, negative control, and expected-red behavior? If NO, mark it `CANNOT_VERIFY` and strengthen it before claiming confidence.
- Have I classified the testing purpose as investigative/diagnostic, user journey/use-case/acceptance, or both, with a reason tied to risk? If NO, select the track before choosing test scope.

## Workflow Overview

```
INTAKE -> EXPLORE -> TDDAB PLAN -> EXECUTE -> PROTOCOL D -> FINALIZE
   |        |          |           |          |            |
 Memory  Codebase   Test-first   RED->GREEN  Debug      Diff+Test
 Bank    analysis   Plan + Gate  per block  Loop       + Outcome
 check              self-review  COMMIT     record     to Memory
```

When uncertainty is material, EXECUTE may invoke a side loop without replacing the phases:

```
HYPOTHESIS -> SUB-EXPERIMENT -> MEASURE -> LEARN -> REVISE/ACCEPT/ABANDON
                         -> PROMOTE FINDING TO REGRESSION/JOURNEY/ACCEPTANCE TEST
```

The full method and source bibliography are in `references/experimentation-and-testing.md`.

## Skill composition

DeepCraft is the orchestration layer; an invoked skill supplies a domain-specific method. Every invoked skill inherits Gates 0–5, the experiment classification, the testing-purpose selection, and attempt recording unless the invoked skill explicitly documents a safe specialization. A specialized skill may add browser journeys, property tests, contract tests, load tests, security checks, or other techniques, but it must not bypass root-cause evidence, adaptive selection, or the full-suite gate.

Before invoking a specialist, state:
- the uncertainty or risk that makes it relevant;
- whether the task needs investigative/diagnostic testing, user journey/use-case/acceptance testing, or both;
- which experiment or test will discriminate the result;
- what evidence will be promoted to permanent coverage.

**Registered specialist: `bugcraft`.** It is the single consolidated bug skill (find, diagnose, repair) and the mandatory method for GATE 6. Protocol D keeps its phase names and gates; BugCraft supplies the detailed run and the on-disk evidence file. Invoke it rather than treating this document's D0-D7 summary as the whole method.


## Phase 0: INTAKE

**ALWAYS start here. This is what makes iterative loops work.**

### Step 1: Identify the task
- Read the instruction, issue, ticket, or user request
- Identify the project path (the directory containing the code)
- Classify the task type: `build` (new feature) | `update` (modify existing) | `fix` (bug fix) | `refactor` (restructure)

### Step 2: Load Memory Bank
Call the memory MCP:
```
get_attempts(project_path="<project-path>")
get_dead_ends(project_path="<project-path>")
get_plan(project_path="<project-path>")
get_repo_map(project_path="<project-path>")
```

### Step 3: Decide what to skip
- If Memory Bank has a cached repo_map, skip Phase 1 re-exploration (use cached map)
- If Memory Bank has dead_ends, DO NOT try those strategies
- If Memory Bank has a stored plan, resume from where it left off
- If Memory Bank has a completed outcome, check if the task is already done

### Step 4: Record task start
```
init_memory(project_path="<project-path>", task_type="<type>", instruction="<task summary>")
```

## Phase 1: EXPLORE

**Goal: Understand the codebase FAST. Do not re-explore if Memory Bank has a cached map.**

### If Memory Bank has repo_map:
1. Read the cached map
2. Verify it's still accurate (quick `ls` + `git log --oneline -3`)
3. Skip to Phase 2

### If no cached repo_map:
1. **Structure**: `find . -type f \( -name "*.py" -o -name "*.ts" -o -name "*.go" -o -name "*.rs" -o -name "*.js" \) -not -path "*/node_modules/*" -not -path "*/vendor/*" -not -path "*/target/*" | head -50`
2. **Test setup**: `find . -name "test_*" -o -name "*_test.*" -o -name "conftest.py" -o -name "pytest.ini" -o -name "package.json" -o -name "Makefile" | head -20`
3. **Config**: `ls setup.py setup.cfg pyproject.toml pytest.ini tox.ini package.json tsconfig.json Makefile go.mod Cargo.toml 2>/dev/null`
4. **Git state**: `git status --short && git log --oneline -5`
5. **Relevant code**: `grep -rn "keyword_from_task" --include="*.py" --include="*.ts" --include="*.go" . | head -20`

### Record to Memory Bank:
```
store_repo_map(project_path="<path>", repo_map=<structure>)
```

### Web research (if needed)

**Research = one command, two sources, one merged answer.** When the user says "research" (or the
web-research step below needs current, sourced facts), run:

```bash
copilot-research "<the specific question>"
```

It sends the question to M365 Copilot's **Deep Researcher** agent, runs its **own** independent
web search, and merges both — printing **A** Copilot · **B** own search · **C** merged
conclusion · **D** agreement · **E** divergence.

Carry sections **A–E (with citations)** into the plan or experiment record; never collapse it to
one source or relabel Copilot's answer as your own web finding. You may append your own extra
tool-based search after **B**. If a section prints `UNAVAILABLE`, record that verbatim and mark
the finding **single-source**. Do not select `copilot-researcher` as the driving model — a harness
system prompt overrides the agent's behaviour; always call the helper.
If the task involves a library, framework, unfamiliar failure mode, or testing technique, search for authoritative guidance before choosing an approach. Prefer primary documentation, standards bodies, original research, and respected practitioners; compare claims instead of copying one skill blindly. For uncertain or difficult work, use 1-2 targeted searches first, then broaden only if the evidence changes the plan. Record the source, the method it supports, and how it applies to this task in the plan or experiment record. Do not treat a web search as proof of correctness: verify the approach in the local codebase or a controlled experiment.

## Phase 2: TDDAB PLAN

**TDDAB = Test-Ahead-Behavior. Write what the test should assert BEFORE writing code.**

### Step 1: Parse the task description — extract structured requirements

Task descriptions come in many forms: dense paragraphs, bullet lists, issue tickets, spec documents. Whatever the format, extract every testable behavior.

**Step 1a: Read the FULL task description before touching anything.**

**Step 1b: Split into sentences and classify each:**
```
  - "must" / "cannot" / "never" / "always" -> REQUIREMENT (high priority)
  - "should" / "when X" / "if X" / "unless" -> CONDITION (high priority)
  - "add" / "create" / "implement" / "support" / "extend" -> ACTION (high priority)
  - "default" / "defaults to" / "fallback" -> DEFAULT (medium priority)
  - "throw" / "error" / "raise" / "reject" / "invalid" -> ERROR_BEHAVIOR (high priority)
  - Other sentences -> CONTEXT (low priority)
```

**Step 1c: Extract behavioral triples (entity, action, detail):**
```
Pattern: "The Command class gains a config method accepting ConfigOptions"
  -> Entity: Command class, Action: gains/config, Detail: method with fields name, searchPaths, formats, mergeConfigs, parser

Pattern: "Boolean false and numeric zero are valid config values"
  -> Entity: Boolean false / numeric zero, Action: are valid, Detail: edge case - falsy values are NOT invalid
```

**Step 1d: Extract edge cases explicitly:**
Scan for: `none`, `empty`, `null`, `undefined`, `zero`, `negative`, `missing`, `malformed`, `invalid`, `unknown`, `case-insensitive`, `boundary`, `overflow`, `default`.

**Step 1e: Extract API surfaces:**
- New classes, methods, types, interfaces, enums mentioned in the task
- Method names following camelCase patterns (getX*, parse*, create*, is*, has*)
- Public API that must remain stable (backwards compatibility)

**Step 1f: Build the requirement checklist:**
```
REQ-1: <behavior description> | Type: <type> | Priority: <high/medium/low>
       Edge cases: <list>
       API surfaces: <new/modified methods>
```

**CRITICAL: Do NOT skip sentences.** A single sentence like "Unknown config keys are ignored" is a testable requirement. Missing one = one failing test.

### Step 2: Check for existing tests or test specs

**If tests already exist:** Read them — they are the ground truth for what "done" means.
```bash
find . -name "*_test.*" -o -name "test_*.*" | head -20
grep -E "def test_|func Test|test\(|it\(" <test_file>
grep -E "assert|require|expect|attest" <test_file> | head -30
grep -E "import |require |use " <test_file> | head -20
```
Map each test function to a requirement. Any requirement with no direct test still must be implemented.

**If NO tests exist:** Derive test cases from the requirements:
```
REQ: "Config values follow strict precedence where CLI args override env vars"
  -> Test: set config value, set env var, pass CLI arg -> verify CLI arg wins
  -> Test: set config value, set env var, no CLI arg -> verify env var wins
  -> Test: set config value only -> verify config value used
```
Write a temporary test file matching the repo's test framework pattern.

### Step 3: Define behaviors
For each requirement: Behavior, Test assertion, Input, Expected output, Edge cases.

### Step 4: Write the TDDAB plan
Each plan block must include EXACT signatures, return types, and logic.
```
Block 1:
  Requirement: REQ-N
  Test function: <name>
  Seam: <exact boundary under test>
  Primary oracle: <observable postcondition>
  Negative control: <safe fault/mutation/invalid input>
  Expected red: <why the control must fail>
  Test assertion: <exact assert statement>
  Expected value: <literal value the test expects>
  Files to modify: <list with exact paths>
  Implementation spec:
    Function signature: <exact signature matching existing patterns>
    Parameters: <name: type> (match existing conventions)
    Return type: <exact type>
    Error types: <exact exception/error class names>
    Logic flow: 1. <steps> 2. <edge case handling> 3. <type coercion>
    Edge cases: None/empty -> <what happens>, Zero/false -> <what happens>, Invalid -> <what error>
    Imports needed: <exact import statements>
    Exports needed: <what to add to __init__.py/mod.ts/etc>
```

### Step 4a: Experiment and test-selection plan

For every block with material uncertainty, add a compact experiment record before implementation:

```
Experiment: EXP-<id>
Trigger: <why a normal test is insufficient>
Subject change: none | test-input/fixture | code | config | dependency | deployment | load | fault | data
Intent: <decision this work should enable>
Parent hypothesis: <falsifiable claim>
Mechanism: <why it might be true>
Baseline/control: <comparison condition>
Primary metric: <measurement>
Success/failure threshold: <precommitted rule>
Guardrails: <quality, cost, latency, safety, or user constraints>
Invalid if: <fixture, environment, instrumentation, or detector failure>
Sub-experiments:
  E1: <prediction> | variable: <one factor> | control: <baseline> | metric: <measurement> | decision: <accept/refute/pivot>
  E2: <prediction> | variable: <one factor> | control: <baseline> | metric: <measurement> | decision: <accept/refute/pivot>
Bundle (when justified):
  base_sha: <same starting revision>
  arms: main | control | ablation | robustness | candidate-fix
  shared_verification_matrix: <commands and expected exits>
safety_stop_and_rollback: <scope, stop condition, rollback, authorization>
promote_to: <regression | acceptance | contract | property | model | none>
```

Use the experiment loop: baseline -> uncertainty map -> cheapest discriminating sub-experiment -> predict -> run -> classify (`supported`, `refuted`, `inconclusive`, `invalid`) -> decide -> promote. For multiple credible causes/fixes or high-risk changes, use a conditional bundle with a `main` arm plus only the `control`, `ablation`, `robustness`, or `candidate-fix` arms that can change the decision. Run fail-closed preflight (base revision, build/import, baseline, RED signal, treatment path) before interpreting any arm. For competing fixes, use same-base isolated worktrees and a shared verification matrix; if every candidate fails hard eligibility, report `no winner`. Keep the full template in `references/experimentation-and-testing.md` and the evidence in `<project>/.swarm/memory/EXPERIMENTS.md` when the file fallback is used.

Then classify testing purpose before choosing scope:

- **Investigative/diagnostic:** use when the question is why, where, or under what condition; start with reproduction, traces, metrics, reduced inputs, and controlled comparisons.
- **User journey/use-case/acceptance:** use when the question is whether an actor can achieve the intended outcome; include the main flow, important alternatives, dangerous exceptions, preconditions, and postconditions.
- **Both:** use when technical uncertainty and user/business risk coexist, or when a component-level fix may affect an externally visible workflow. Do not use a broad E2E suite as a substitute for root-cause diagnosis.

If no experiment is warranted, record `Experiment: not needed; reason: <clear deterministic behavior already covered by a focused test>`.

### Step 5: Completeness gate
Before writing code, verify:
- [ ] Most testable behaviors have a plan block
- [ ] Key test cases traced mentally with predicted output
- [ ] Major expected values accounted for
- [ ] Edge cases from the task have handling
- [ ] Key function signatures specified
- [ ] New classes/types defined with fields
- [ ] Error/exception classes named with throw conditions
- [ ] Imports and exports identified
- [ ] File dependency order established (leaf modules first)
- [ ] Material uncertainty has a parent hypothesis and discriminating sub-experiments, or an explicit reason no experiment is needed
- [ ] Each experiment has a control/baseline, one independent variable, prediction, metric, thresholds, safety/rollback, and promotion target
- [ ] Each important test has a seam, primary oracle, negative control, and expected-red behavior (or `CANNOT_VERIFY` with a reason)
- [ ] Testing purpose and risk justify diagnostic, journey/acceptance, or both
- [ ] Signatures match existing codebase conventions (checked via grep)
If most checked, proceed. Gaps caught by Protocol D. Max 2 plan revision rounds.

### Step 6: Check for a previously stored plan
```
get_task_state(project_path="<path>")
```
If a prior plan exists, resume. Do not rewrite completed blocks.

### Step 7: Store plan to Memory Bank
```
store_plan(project_path="<path>", plan=<TDDAB plan JSON>)
```

### Step 8: Best-effort Developer Council review
Call `developer-council_council_discuss` with:
- `problem`: The TDDAB plan summary
- `context`: Codebase context from EXPLORE
- `models`: `["copilot", "glm", "qwen3.8-max"]`
- `mode`: `"collaborative"`

Seats: `copilot` = GPT 5.6 via the Copilot proxy, `glm` = LiteLLM `auto` failover, `qwen3.8-max` = Qwen3.8-Max with Thinking mode through the shared CloakBrowser profile. `qwen3.8-max` needs a one-time qwen.ai login in the shared browser (`cloakbrowser-login https://chat.qwen.ai/`); if its answer starts with `[Qwen3.8-Max Web Chat] Login required`, tell the user that one command is needed and proceed with the other two seats only if they return usable output. Use `developer-council_check_council_seats` first if a seat returns an error string.

Validate that the response is non-empty and usable. If valid, incorporate the findings into the plan and record `Council Findings`, `Council Risks`, and `Council Recommendations`. If the tool is unavailable, times out, errors, or returns an unusable response, record `Council Status: skipped` with the reason and continue. Do not recursively invoke the Council.

## Phase 3: EXECUTE

**Vertical slices only. One block at a time. RED -> GREEN -> VERIFY -> COMMIT per block.**

### Pre-execute: Check current state
```
get_task_state(project_path="<path>")
```
Check: completed_blocks (skip), failed_blocks (review before retrying), current_block (where to resume).

#### EXPERIMENT: when uncertainty is material
Before implementing a fix or architecture change, run the smallest reversible experiment that can distinguish the leading hypotheses:

1. Establish a baseline and record the current metric/observation.
2. Write the parent hypothesis and a falsifiable prediction.
3. Split the question into sub-experiments; each changes one major factor and has a control.
4. Run the cheapest discriminating sub-experiment first.
5. Classify the result as supported, refuted, inconclusive, or invalid.
6. Record evidence, confounders, decision, and the next action.
7. Promote the finding to a stable regression, acceptance, contract, property, or model test where appropriate.

Never use an experiment to hide a symptom, change production without authorization, or declare success because a flaky run passed. If the experiment changes code, configuration, dependencies, deployment, load, data, or fault state, record that as `subject_change` and restore the baseline before the full verification suite.

Before interpreting an experiment, run a fail-closed preflight: record `base_sha` and dirty state, verify build/import, run the baseline, prove the RED signal detects the exact symptom, and prove the treatment changes the exercised path. If preflight fails, classify the run `invalid`; do not call it a refutation.

For a difficult bug or high-risk change, generate 3–5 ranked root-cause hypotheses and give each a cheap discriminating test. Test the most discriminating hypothesis first. For competing repairs, use same-base isolated worktrees, a shared verification matrix, hard eligibility gates, and an explicit `no winner` outcome when none is safe.

#### TEST AUDIT: before trusting green
For every new or repaired high-value test, record `seam`, `primary_oracle`, `negative_control`, and `expected_red`. Run the negative control and apply O1–O6. A static test-smell scan produces candidates only; a fresh semantic reviewer must attempt refutation and return `CONFIRMED`, `FALSE-POSITIVE`, or `NEEDS-CONTEXT`. Never turn a red suite green by weakening the oracle, hiding a race with a timeout, skipping a test, or editing production under a test-healing role.


#### RED: Write the test
1. **If tests already exist:** confirm your planned implementation will make them pass.
2. **If writing your own:** Write the test function that asserts the behavior.
3. Run the test to confirm it FAILS for the RIGHT reason:
   ```bash
   python -m pytest <test_file>::<test_function> -xvs 2>&1 | tail -15
   go test -run <TestFunc> -v ./... 2>&1 | tail -15
   deno test <test_file> --filter "<test name>" 2>&1 | tail -15
   cargo test <test_name> -- --nocapture 2>&1 | tail -15
   ```
4. If it fails for the wrong reason, fix the test, not the code.

#### GREEN: Write minimal code
1. Write the MINIMAL code to make the test pass
2. Run the test, confirm it PASSES
3. If it doesn't pass, go to Protocol D

#### VERIFY: Run broader tests
1. Run the specific test again: confirm it still passes.
2. Apply the generic verification contract:
   - **O1 — primary outcome:** assert the intended outcome, not merely execution.
   - **O2 — oracle falsification:** invalidate/invert the oracle and verify the test turns red.
   - **O3 — fault sensitivity:** inject a relevant safe fault and verify detection.
   - **O4 — seam/write contract:** prove the real boundary and failure path are exercised.
   - **O5 — repeat/isolation:** bound repeats, seeds, state, ordering, and concurrency.
   - **O6 — independent review:** a fresh read-only actor attempts to refute the result.
3. Run the diagnostic audit: mechanical candidates are not verdicts. Classify each as `CONFIRMED`, `FALSE-POSITIVE`, or `NEEDS-CONTEXT` with mechanism, causal evidence, and context.
4. Select the verification track by purpose and risk:
   - **Diagnostic/investigative:** confirm the root cause with a minimized reproducer, trace, metric, or controlled comparison; do not rely on a green retry.
   - **Journey/use-case/acceptance:** exercise the actor's main flow, important alternative, dangerous exception, preconditions, and postconditions.
   - **Both:** run the diagnostic experiment first, then validate the user/business outcome and the critical integration path.
   - Add property-based, metamorphic, model/state, contract, mutation, performance, security, accessibility, or fault-injection checks only when the risk or uncertainty justifies their cost.
5. Select tests by change impact and risk, recording `must-run`, `should-run`, and `optional` with a reason for every omission. A selected subset is for iteration speed only; the full suite remains mandatory before done.
6. Run existing repo tests to check for regressions:
   ```bash
   deno test --allow-all              # Deno
   python -m pytest tests/ -x         # Python
   go test ./...                      # Go
   npm test                            # Node
   ```
7. If existing tests fail, you broke something. Undo and fix. Classify the failure as `test_defect`, `product_regression`, `environment_failure`, or `ambiguous_specification`; do not edit production to make a test defect disappear.
8. If all selected checks, the independent audit, and the full suite pass, record the evidence envelope and move to the next block.

#### COMMIT: Record progress
1. `git add <files> && git commit -m "<block description>"`
2. Record to Memory Bank:
```
record_attempt(project_path="<path>", block="<block number>",
  strategy="<approach used>", outcome="passed",
  test_output="<test output summary>", reason="<why it passed/failed>")
```
3. Move to the next block (or FINALIZE if all done)

## Phase 4: PROTOCOL D (When Tests Fail)

**Debug loops are normal — expect 1-2 per block. Follow Protocol D systematically.**

> **Deep hangs / non-test runtime issues:** For hangs, stalls, or failures that don't surface as test assertions (e.g. a frozen TUI, silent process death, queue saturation), stay inside `bugcraft`: its B1 covers non-assertion failures (replay a captured trace, throwaway harness, correlate stack traces with runtime state, read exit status / `dmesg` / journal) and its B4 instruments component boundaries until one layer is named. There is no separate `debugger` skill any more — it was folded into `bugcraft` (method in B1/B3/B5/B7, read-only delegated variant in Appendix A).

> **GATE 6 applies to every Protocol D round.** Open `skill bugcraft` and work its gates in order. Protocol D's step names map onto BugCraft's gates; neither overrides the other:
>
> | Protocol D | BugCraft gate | What must exist before moving on |
> |---|---|---|
> | D0 Classify | B0 Symptom contract | expected / actual / acceptance / frequency / redaction |
> | D1 Classify failure | B2 Reproduce | the reported failure mode, not a nearby one |
> | D2 Isolate | B1 Feedback loop, B2 minimise | one command, run once, red on *this* symptom; smallest load-bearing scenario |
> | D3 Hypothesise | B3 Ranked hypotheses | 3-5 falsifiable, red-teamed |
> | D3 experiment | B4 Isolate + instrument | one variable per probe, `[DEBUG-xxxx]` tagged |
> | D4 Fix | B5 Minimal fix | one change, at the source, no drive-bys |
> | D5 Verify | B6 Regression lock, B7 Fresh evidence | observed red→green, full suite exit 0 in this turn |
> | D5 Verify (live) | B8 Soak & sweep | sustained window with 0 new findings; function matrix exercised; else a written not-doable waiver |
> | D6 Record | B9 Close-out | ATTEMPTS.md line + cleanup + rollback |
>
> Before commit: `python3 <bugcraft-dir>/scripts/bug_gate_check.py <project>/.swarm/bugs/BUG-<slug>.md` exits 0. Exit 1 names the missing gate — fix the evidence, not the check.

### D0. Classify failure and purpose
Before fixing, decide whether this is:
- **Diagnostic/investigative:** the symptom is known but the cause is not; build a red-capable feedback loop first, then minimize, rank 3–5 hypotheses, and run a discriminating experiment.
- **User journey/use-case/acceptance:** the question is whether the intended actor can achieve the promised outcome; test the main, alternative, and dangerous exception flows.
- **Both:** technical cause and user/business impact are both uncertain or high risk; investigate first, then validate the journey.
- **Regression:** known behavior is broken; preserve a minimal failing test and prevent duplicate broad E2E coverage.

Also classify the failure as `test_defect`, `product_regression`, `environment_failure`, or `ambiguous_specification`. A test healer may change only approved test mechanics; it must not weaken the oracle or edit production to obtain green.

### D1: Classify the failure
| Classification | Symptom | Fix Direction |
|---|---|---|
| Import error | ModuleNotFoundError, ImportError, cannot find module | Missing export, wrong import path, new file not created |
| Type error | TypeError, AttributeError, cannot read property | Wrong type returned, missing method, wrong parameter type |
| Value mismatch | assertEqual(X, Y) where X!=Y | Logic error — trace expected vs actual |
| Missing method | has no attribute, not a function | Method not implemented or wrong name |
| Wrong error type | assertRaises(X) but got Y | Throwing wrong exception class |
| Environment | Missing dep, wrong version | Fix environment |

### D2: Isolate (THE MOST IMPORTANT STEP)
First build a tight, red-capable feedback loop: one agent-runnable command that drives the exact bug path and can turn red on the reported symptom. Make it deterministic, fast, isolated, and repeatable. If the symptom is intermittent, raise the reproduction rate with bounded loops, seeds, or controlled stress before hypothesizing.

1. Read the traceback. Which EXACT line in YOUR code failed?
2. What was the expected vs actual value?
3. Run ONLY the failing test:
   ```bash
   python -m pytest <test_file>::<test_function> -xvs 2>&1 | tail -30
   go test -run TestSpecificFunc -v ./... 2>&1 | tail -30
   deno test <test_file> --filter "test name" 2>&1 | tail -30
   ```
4. Add a temporary debug print RIGHT BEFORE the failing assertion
5. Re-run the SINGLE test. Read the debug output.
6. Identify the EXACT point where your code diverges from expected.

### D3: Hypothesize (rank by likelihood)

Before instrumenting, write 3–5 ranked hypotheses. Each row must name a cheap discriminating test, predicted observation, and what result would refute it:

```text
rank | hypothesis | mechanism | prediction | cheap test | refutation result
1 | <most likely> | <why> | <what should happen> | <command/probe> | <what would disprove it>
2 | <alternative> | <why> | <what should happen> | <command/probe> | <what would disprove it>
```

For each material hypothesis, write the prediction, baseline/control, one independent variable, metric, threshold, safety/rollback, and expected decision. Run the cheapest discriminating sub-experiment before making a broad fix. Record `supported`, `refuted`, `inconclusive`, or `invalid`; an inconclusive run requires a better experiment, not a hopeful code change. Separate a valid wrong prediction (`direction`, `magnitude`, `regime`, `shape`, or `tradeoff`) from an apparatus failure.

### D4: Fix (MINIMAL change — one thing at a time)
Apply the SMALLEST fix for the most likely cause. Do NOT fix multiple things at once.

### D5: Verify
1. Remove temporary instrumentation and verify no debug artifacts remain.
2. Run the minimized red-capable regression test: old code must fail, fixed code must pass.
3. Re-run the original, unminimized reproduction to confirm the user-visible symptom is gone.
4. Run the full test file and existing tests: baseline must still pass.
5. If no correct regression seam exists, record that architectural finding instead of claiming a strong test.
6. Preserve the full log/evidence path, not only the display tail, and record `source_unchanged` and `temporary_artifacts_remaining`.

### D6: Record to Memory Bank
Record the attempt as an evidence envelope, not only a pass/fail word:
```text
[attempt-id] strategy=<approach> command=<exact command> exit=<code>
result=pass|fail|invalid|inconclusive evidence=<log/report path + digest>
source_unchanged=<true|false> temporary_artifacts_remaining=<count>
next=<action>
```
When the memory MCP is available, use `record_attempt`; when it is not, append the same fields to `<project>/.swarm/memory/ATTEMPTS.md`.

### D7: Common failure patterns per language

**Python:** None != expected (check return statement), dict != object (use dataclass), module has no attribute (forgot __init__.py export)

**Go:** nil pointer dereference (add nil check), wrong type assertion (check pointer vs value), undefined X (missing import or unexported symbol, check capitalization)

**TypeScript:** Values not equal (type coercion, check === vs ==), X is not a function (not exported or wrong this binding), assertRejects fails (doesn't throw or wrong error type)

**Rust:** panicked at (unwrap on None/Err, use ? or match), wrong return type (check trait impl), cannot find function (forgot pub or wrong use)

### Max iterations: 3 Protocol D rounds per block
If after 3 rounds still failing:
1. Undo all changes: `git checkout -- .`
2. Re-read the task description for this behavior
3. Try a COMPLETELY different approach
4. If still failing after 1 fresh start, record dead-end and move to next block
5. Come back to failed blocks after completing all others

## Phase 5: FINALIZE

### Step 1: Cross-check
- [ ] Diff matches the TDDAB plan? `git diff`
- [ ] Every block in the plan was implemented?
- [ ] Every material experiment has a record, result classification, decision, and evidence artifacts?
- [ ] Every important test has a seam, primary oracle, negative control, and expected-red result or `CANNOT_VERIFY`?
- [ ] Diagnostic findings were promoted to focused regression tests, and user/business findings were covered by the appropriate journey/acceptance tests?
- [ ] Mechanical audit candidates received an independent semantic verdict: `CONFIRMED`, `FALSE-POSITIVE`, or `NEEDS-CONTEXT`?
- [ ] Any candidate comparison recorded `base_sha`, shared verification matrix, hard eligibility, and `no winner` when applicable?
- [ ] Evidence envelope records exact command, exit code, full log path/digest, `source_unchanged`, and temporary artifact count?
- [ ] No extra changes beyond the plan?
- [ ] No debug code (print, pdb, console.log)?
- [ ] No test modifications (unless the test itself was wrong)?
- [ ] GATE 6: `bug_gate_check.py <bug-file>` exits 0 (`READY`), and every waiver is a real documented one (B6 no-seam only)?
- [ ] GATE 6: the winning hypothesis is stated in the commit message, and the original un-minimised repro was re-run green (B7)?
- [ ] No temporary test files left in the diff?

### Step 2: Full test suite
```bash
python -m pytest tests/ -xvs --timeout=120
# or: npm test / go test ./... / cargo test
```

### Step 3: Record outcome
```text
record_outcome(project_path="<path>", status="passed",
  tests_passed=<count>, tests_failed=<count>, tests_skipped=<count>,
  infrastructure_errors=<count>, full_suite_exit=<code>,
  selected_test_scope=<must-run/should-run/optional + reasons>,
  base_sha=<revision>, source_unchanged=<true|false>,
  temporary_artifacts_remaining=<count>, evidence=<log/report paths>,
  diff_summary="<git diff --stat output>", notes="<key insight>")
```

### Step 4: Output
Show: git diff, full-suite results, selected diagnostic/journey evidence, test-quality audit verdicts, experiment records and decisions, candidate comparison or `no winner`, and a brief explanation. State which testing track was used and why.

## Codebase Navigation Patterns

**Strategy: Top-down then bottom-up. Find the PATTERN, don't invent one.**

**Step 1: Map the file tree:**
```bash
find . -type f \( -name "*.go" -o -name "*.py" -o -name "*.ts" -o -name "*.rs" -o -name "*.js" \) \
  -not -path "*/vendor/*" -not -path "*/node_modules/*" -not -path "*/target/*" \
  -not -path "*/.git/*" -not -path "*/dist/*" -not -path "*/build/*" | sort
```

**Step 2: Identify the module structure:**
```bash
ls */__init__.py */package.json */go.mod */Cargo.toml */mod.ts */index.ts 2>/dev/null
ls main.go main.py index.ts lib.rs app.py 2>/dev/null
find . -name "test_*" -o -name "*_test.*" -o -name "*.test.*" | head -20
```

**Step 3: Find the EXACT files to modify:**
Map test files to source files: `config_test.ts` -> `command.ts` or `config.ts`, `test_api.py` -> `api.py`, `foo_test.go` -> `foo.go`

**Step 4: Find existing SIMILAR patterns to copy (THE KEY STEP):**
```bash
grep -rn "similar_keyword" --include="*.go" --include="*.py" --include="*.ts" --include="*.rs" . | head -15
grep -n "def similar_method\|func similarFunc\|similarMethod(" <relevant_file>
grep -rn "interface\|type\|class\|struct\|enum" <relevant_dir>/ | head -20
head -30 <file_to_modify>
```

**Step 5: Read ONLY the relevant section (token-efficient):**
```bash
grep -n "class Command\|export class\|func.*Command\|type Command" <file> | head -5
sed -n '50,200p' <file>
```

**Step 6: Verify existing tests pass BEFORE you start:**
```bash
python -m pytest tests/ -x --timeout=60 2>&1 | tail -5
go test ./... 2>&1 | tail -5
```

## Multi-File Change Tracking

Changes across multiple files must be coherent. Getting the dependency order wrong causes cascading failures.

**Step 1: List ALL files that will be modified or created.**

**Step 2: For each file, note what changes and its dependencies.**

**Step 3: Write changes in DEPENDENCY ORDER (leaf modules first):**
1. Types/interfaces (no dependencies)
2. Implementation logic (depends on types)
3. Integration points (depends on implementation)
4. Re-exports (depends on everything)

**Step 4: After all changes, verify:**
```bash
git diff --stat  # Check no unexpected files changed
deno check <main_file>     # TypeScript
python -c "import <module>" # Python
go build ./...              # Go
cargo check                 # Rust
```

## New File Creation

**When to create new files:**
- The task mentions a "submodule", "module", or "directory"
- The feature is substantial enough to warrant its own module (>100 lines)
- The task names multiple related classes/types that belong together

**File creation patterns by language:**
- **TypeScript/JavaScript**: Create `mod.ts` or `index.ts` as module entry. Re-export from parent.
- **Python**: Create `__init__.py` in new directories. Export public API from it.
- **Go**: Create new `.go` files in the appropriate package directory. Package name matches directory.
- **Rust**: Create new `.rs` files and declare them in `mod.rs` or `lib.rs`.

**Naming conventions (match the repo!):**
```bash
find . -name "*.ts" -not -path "*/node_modules/*" | head -10
find . -name "*.py" -not -path "*/venv/*" | head -10
find . -name "*.go" | head -10
```

## Language-Specific Patterns

**Go:** init() for registration, interfaces for extensibility, receiver methods (pointer vs value matters), capitalized = exported, errors.Is()/errors.As() for wrapping, context.Context first param, opts ...Option functional options. Testing: `go test -run TestName -v ./pkg/...`

**Python:** pyproject.toml + pytest, conftest.py for fixtures, __init__.py exports, @dataclass/NamedTuple, exception hierarchy. Testing: `python -m pytest tests/test_file.py::TestClass::test_method -xvs`

**TypeScript/JavaScript:** tsconfig.json for module resolution, package.json exports field, assertEquals(actual, expected) - actual FIRST in Deno, re-exports via mod.ts/index.ts. Testing: `deno test <file> --filter "name"` or `npx jest <file> -t "name"`

**Rust:** Cargo.toml + cargo test, #[derive(Debug, Clone, PartialEq)], pub visibility, Option<T>/Result<T,E>. Testing: `cargo test test_name -- --nocapture`

**General cross-language patterns:** Registry/plugin (register()), Builder (builder().build()), Visitor (accept/visit_*), Factory (create_*/from_*), Iterator (next() returning Option/null)

## What NOT to Do

1. Don't change files not mentioned in the task
2. Don't ignore existing test patterns — match the repo's assertion style
3. Don't write 1000 lines without testing — test every 100-200 lines
4. Don't guess API signatures — grep the codebase for similar functions
5. Don't forget imports — new functions need imports in every file that uses them
6. Don't change public APIs that aren't in scope — existing tests will fail
7. Don't skip baseline tests — if existing tests fail, nothing else matters
8. Don't try to install dependencies if offline — use what's already available
9. Don't leave temporary test files in the diff — remove them before finishing
10. Don't modify existing test files — your changes may be overwritten
11. Don't call a random retry, a coverage number, or a green flaky run an experiment
12. Don't change more than one major experimental factor without recording the confound
13. Don't use broad E2E tests to replace root-cause diagnosis
14. Don't run load, security, mutation, or fault-injection interventions without scope, stop conditions, rollback, and authorization
15. Don't treat a static test-smell match as a confirmed defect; require semantic refutation/review
16. Don't auto-heal by broadening assertions, increasing timeouts, skipping tests, or editing production to obtain green
17. Don't select a candidate fix without same-base evidence, hard eligibility gates, and an explicit no-winner option
18. Don't trust a log line as proof of state — verify against ground truth (screenshot, API response, file on disk, process status).
19. Don't write code from scratch when an existing implementation can be found on GitHub or the web — copy it, adapt it to local findings, document the source, and paste it instead.
20. Don't pick an implementation approach by intuition when multiple credible options exist — create a branch per approach, benchmark them identically, and let the decision matrix pick the winner.

## Token Efficiency Rules

1. Don't read entire files — use `grep -n` then read +/-50 lines around it
2. Don't re-explore — Memory Bank cache is your friend
3. Don't run full test suite until the specific test passes
4. Don't explain what you're about to do — just do it, record to Memory Bank
5. Don't describe the diff — show it with `git diff`
6. Chunk your work — don't write more than 150-200 lines between test runs
7. Use grep to extract patterns, not reading — `grep -n "export class\|export function" file.ts`
8. Cache your analysis — store to Memory Bank immediately
9. Prioritize by requirement count — focus on unimplemented requirements
10. Use `git diff --stat` not `git diff` when you just need file scope

## Quick Decision Guide

| Situation | Action |
|-----------|--------|
| Starting a new feature | INTAKE -> EXPLORE -> TDDAB PLAN -> EXECUTE |
| Fixing a bug | GATE 6: `skill bugcraft` -> B0 symptom contract -> B1 red-capable loop -> B2 minimise -> B3 hypotheses -> B4 isolate -> B5 minimal fix -> B6 regression -> B7 fresh evidence -> B8 close-out -> `bug_gate_check.py` exits 0 |
| "Find bugs" / audit, no known symptom | `bugcraft` hunt mode: taxonomy sweep -> reachability proof -> severity x reachability x blast radius ranking (no suspicions presented as findings) |
| Bug returned after an earlier fix | `bugcraft` B1 recent-changes check (`git log -S <symbol>`) -> treat the old fix as a symptom fix -> root-cause route |
| Same fix attempted 3× without success | Stop: `git checkout -- .`, re-read B0, re-EXPLORE, new plan, or escalate with what was ruled out |
| Fixed but it "still feels buggy" / keeps failing later | B8 Soak & sweep: drive the live artifact for the window, sweep every function (happy/boundary/invalid/error/state), reset the clock on each new finding until a clean cycle |
| Artifact cannot be driven live (library, prod-only job) | B8 records `waived: not doable — <condition>`; state the missing observation surface as a testability finding |
| Updating existing code | INTAKE -> check Memory Bank -> EXPLORE -> TDDAB PLAN -> EXECUTE |
| Iterative loop re-entry | INTAKE -> get_task_state -> skip dead_ends -> resume plan |
| Tests fail | Protocol D -> Classify -> Isolate -> Fix -> Verify -> Record |
| Difficult, ambiguous, distributed, or high-risk problem | Add a parent hypothesis and discriminating sub-experiments before changing the product; record control, prediction, metric, safety, and decision |
| Reproducible symptom with unknown cause | Investigative/diagnostic track -> minimize and experiment -> promote root-cause regression |
| New or changed user-facing workflow | User journey/use-case/acceptance track -> main, alternative, exception, preconditions, postconditions |
| Technical uncertainty plus user/business risk | Both: investigate first, then validate the critical journey and integration path |
| Green test may be false-green | Test audit -> seam/oracle/negative control -> refute-first review -> `CONFIRMED`, `FALSE-POSITIVE`, or `NEEDS-CONTEXT` |
| Multiple credible fixes / competing approaches | GATE 1G: one git branch per approach → identical benchmark suite on all branches → decision matrix (correctness, performance, complexity, robustness) → merge winner, delete losers → record in PLAN.md "Approach decision" and ATTEMPTS.md |
| Flaky/intermittent result | Classify test defect, product regression, environment failure, or ambiguous spec; bounded repeats; quarantine with owner/deadline |
| No experiment needed | State the clear deterministic behavior and focused test that already answers the question |
| Stuck after 3 attempts | Undo all -> re-read task -> fresh EXPLORE -> new PLAN |
| No MCP available | REQUIRED file fallback: Gate 0−5 apply with `<project>/.swarm/memory/` + `~/.opencode/memory/` files — never skip memory |
| Tests already exist | Read them as ground truth; map to requirements |
| No tests exist | Write your own derived from requirements; match repo test framework |
| Need new files | Follow existing module structure; create in dependency order |
| Offline/no internet | Use only what's installed; find alternatives |

## Memory Bank MCP Reference

| Tool | When to call | Returns |
|------|-------------|---------|
| `init_memory` | Start of Phase 0 | Creates memory bank directory |
| `analyze_task` | Phase 2 (PLAN) | Structured requirements from task description |
| `get_task_state` | End of Phase 0, start of Phase 3, after each commit | Full state |
| `get_attempts` | Phase 0, before planning | Previous strategies for this project |
| `get_dead_ends` | Phase 0, before planning | Failed approaches to skip |
| `get_plan` | Phase 2 (PLAN), resume scenario | Stored TDDAB plan |
| `get_repo_map` | Phase 0, resume scenario | Cached repo structure |
| `store_repo_map` | End of Phase 1 (EXPLORE) | Saves repo structure to disk |
| `store_plan` | End of Phase 2 (PLAN) | Saves TDDAB plan to disk |
| `EXPERIMENTS.md` | Gate 1B, after each experiment | File fallback for hypothesis, control, prediction, metric, result, decision, and evidence |
| `record_attempt` | End of each EXECUTE block | Records outcome, adds to dead_ends if failed |
| `record_outcome` | Phase 5 (FINALIZE) | Final task result |

### The memory-driven loop
```
Phase 0: init_memory -> get_attempts -> get_dead_ends -> get_task_state
Phase 1: store_repo_map
Phase 2: get_task_state (resume?) -> analyze_task -> store_plan -> experiment_plan
Phase 3: get_task_state -> execute blocks -> test_audit/O1-O6 -> experiment/learn -> record_attempt -> get_task_state
Phase 5: record_outcome -> get_task_state (verify completion)
```

## Compatibility

This skill works with:
- **opencode**: Load via `skill deepcraft` or auto-load via AGENTS.md
- **Claude Code**: Load via `skill deepcraft`
- **Any iterative loop**: Designed as the primary skill for autonomous iteration
- **Any language**: Python, Go, TypeScript, Rust, JavaScript
- **Any task type**: New features, bug fixes, refactors, greenfield projects

### Memory Bank MCP

The memory MCP is the core of DeepCraft. If not available, the gates still apply via the FILE fallback (mandatory, not optional):
- Read lessons/runbooks: `~/.opencode/memory/LESSONS.md`, `~/.opencode/memory/runbooks/`
- Plain text memory in `<project>/.swarm/memory/PLAN.md` + `ATTEMPTS.md` (create the dir)
- `get_task_state` / `get_attempts` are satisfied by re-reading PLAN.md / ATTEMPTS.md

### DeepSWE Benchmark Quick-Start

When working on DeepSWE benchmark tasks (instruction.md + repo in Docker, no test.patch visible):

```
1. Read instruction.md FULLY (every word)
2. Call analyze_task MCP -> get requirements, behaviors, edge cases
3. Explore the repo:
   - find . -type f -name "*.go" (or .py, .ts, .rs) | grep -v vendor/node_modules
   - grep -rn "keyword_from_instruction" --include="*.<ext>" .
   - Read 50-100 lines around relevant code
4. Check what test runner the repo uses (deno test, pytest, go test, npm test)
5. Write a TDDAB plan with exact signatures, return types, error types
6. For each plan block:
   a. Write the implementation
   b. Write a temp test based on the instruction
   c. Run your temp test
   d. Run existing repo tests (regression check)
   e. If both pass -> next block; if fail -> Protocol D
7. Remove temp test files
8. git diff --stat -> verify only intended files changed
9. Record outcome to Memory Bank
```

**Time budget:** 50% planning, 30% implementing, 10% testing, 10% debugging
