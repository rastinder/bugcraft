# Evidence-Driven Experiments and Adaptive Testing

Use this reference when a task is uncertain, difficult to diagnose, performance-sensitive, distributed, or user-facing. It complements DeepCraft's TDDAB and Protocol D; it does not replace either.

## 1. The core distinction

A test measures a system under a declared condition and compares the result with an oracle. An experiment deliberately changes one relevant aspect of the system or its environment to learn whether a falsifiable prediction is supported.

| Activity | Typical subject change | Purpose | Keep as a permanent test? |
|---|---|---|---|
| Unit, component, integration, contract, acceptance, property, metamorphic, accessibility, or security test | No product change; inputs, fixtures, time, or test doubles may vary | Check known behavior against an oracle | Usually yes, when the behavior is important |
| Trace collection, metric collection, minimized reproduction, differential observation | No deliberate product change | Gather diagnostic evidence | Usually no; preserve the useful regression separately |
| Feature-flag, algorithm, dependency, configuration, or deployment comparison | Product or deployment changes | Compare outcomes and learn | Keep only stable checks and findings |
| Load, stress, soak, or fault-injection run | Workload, resource, dependency, or failure state changes | Measure performance or resilience | Keep a stable benchmark, guardrail, or recovery test |
| Mutation testing | Code is deliberately changed | Measure whether tests detect plausible faults | No; use surviving mutants to improve permanent tests |
| Observational incident or natural rollout analysis | No planned intervention | Learn from naturally occurring variation | Keep evidence and any discovered regression |

A test can be broad or narrow; an experiment can be local or end-to-end. Classify the activity by what it changes and what uncertainty it reduces, not by tool or test size.

## 2. When to run an experiment

Run a parent experiment when at least one of these is true:

- the cause is not yet identified;
- several plausible causes or designs remain;
- the result depends on timing, load, concurrency, state, data, deployment, or external services;
- the user/business outcome is uncertain, not just the implementation;
- a previous green suite conflicts with observed behavior;
- the proposed change has meaningful performance, reliability, security, accessibility, or migration risk;
- the cost of being wrong is high and a cheap, reversible experiment can reduce uncertainty.

Do not create an experiment for a known deterministic behavior that a focused regression test can answer directly. Do not change production or shared infrastructure merely to satisfy curiosity; use a safe environment and explicit authorization.

## 3. Parent experiment and sub-experiment loop

Use one parent hypothesis and decompose it into sub-experiments only when more than one factor is uncertain. Each sub-experiment must have one discriminating prediction, a control or baseline, a metric, and a decision that changes the next action.

### Loop

1. **Baseline:** reproduce the current observation and record the decision threshold.
2. **Map uncertainty:** list candidate causes, assumptions, dependencies, and unknowns.
3. **Choose the cheapest discriminating sub-experiment:** prefer observation, a reduced input, a boundary condition, or a reversible switch over a rewrite.
4. **Change one major factor:** keep all other relevant conditions as comparable as possible.
5. **Predict before execution:** write the expected observation and the result that would refute the hypothesis.
6. **Run and capture evidence:** retain commands, seeds, environment, logs, traces, metrics, and artifacts.
7. **Classify:** `supported`, `refuted`, `inconclusive`, or `invalid`.
8. **Decide:** accept, refine, pivot, abandon, or investigate further. An inconclusive run is not proof.
9. **Promote:** turn the discovered defect into the narrowest durable regression test; add journey or acceptance coverage when the user/business risk warrants it.

### Example

Parent hypothesis: “A new cache path caused the checkout p95 regression.”

- **E0 — observation:** trace the request and establish a repeatable baseline.
- **E1 — controlled comparison:** replay the same workload against the old and new builds.
- **E2 — reversible intervention:** toggle only the suspect cache path.
- **E3 — boundary comparison:** compare cold/warm cache and serialization behavior.
- **E4 — realistic workload:** run the smallest load or soak experiment that can test the suspected threshold.
- **E5 — user validation:** execute the critical checkout journey and its acceptance criteria.
- **Promotion:** add a regression test for the actual root cause, plus a focused journey test for the user-visible promise.

A sub-experiment is not a random retry. If its result cannot change the next decision, stop spending time on it.

## 4. Experiment record

Use one record per parent experiment and keep the sub-experiment identifier on every evidence artifact.

```text
EXP-<id>
parent_task: <task or issue>
status: proposed | running | complete | abandoned

mode: observation | intervention | quasi-experiment
subject_change: none | test-input/fixture | code | config | dependency |
                deployment | load | fault | data
instrumentation: none | external | test-only | production

intent: <observable decision this work should enable>
uncertainty: <what is not known>
hypothesis: <falsifiable claim>
mechanism: <why the claim might be true>
prediction: <expected result if true>
baseline_or_control: <comparison condition>
independent_variable: <single manipulated factor>
metric: <measurement>
success_threshold: <precommitted threshold>
failure_threshold: <precommitted threshold>
scope_and_environment: <component, service, staging, production-like, production>
data_seed_and_repetitions: <inputs, random seed, repeat count>
procedure: <ordered actions>
safety_stop_and_rollback: <limits, kill switch, cleanup, abort conditions>

sub_experiment: <E-id>
observations: <actual results and artifacts>
result: supported | refuted | inconclusive | invalid
information_gain: <what uncertainty was reduced>
confounders: <known weaknesses or alternative explanations>
decision: accept | revise | abandon | investigate further
promote_to: none | regression | acceptance | contract | property | model
artifacts: <logs, traces, metrics, reports, links>
```

### Required interpretation

- **Supported:** the prediction was observed; confidence increased, but alternative explanations may remain.
- **Refuted:** the prediction contradicted the hypothesis; revise or replace it.
- **Inconclusive:** the run did not discriminate; do not report it as evidence for or against the hypothesis.
- **Invalid:** the environment, fixture, instrumentation, or procedure invalidated the run; fix the procedure before drawing conclusions.

## 5. Testing tracks

### Track A — Investigative/diagnostic testing

Primary question: **What is happening, why, and where is the cause?**

Use it for reproducible failures with unknown causes, intermittent or distributed failures, unexpected performance, regressions that evade assertions, and unfamiliar runtime behavior. Start with observation, reproduction, a minimized case, traces, logs, metrics, controlled input changes, and comparison. Keep instrumentation reversible. End by fixing the root cause and adding a focused regression test.

This track is a purpose, not a formal test level. Its closest formal practice is exploratory/experience-based testing, but a diagnostic test can be component, integration, or end-to-end.

### Track B — User journey/use-case/acceptance testing

Primary question: **Can the intended user or business actor reach the intended outcome, with the expected postconditions and acceptable quality?**

Use it for new user-facing features, critical workflows, changed business rules, release qualification, and high-impact integrations. Cover the main success flow, important alternative flows, dangerous exception flows, preconditions, and postconditions. Prefer behavior-focused examples over implementation-coupled UI steps. Keep a small set of critical journeys; use lower-level tests for business-rule permutations and edge cases.

Usability testing is related but different: it asks whether target users can understand, operate, and complete the task comfortably. Use automated accessibility checks plus manual assistive-technology or real-user checks where needed.

### Track C — Exploratory testing

Exploratory testing learns about the system while designing and executing focused probes. Use a time-boxed charter naming the target, risk, setup, and time limit. Record discoveries, turn high-value discoveries into stable regression or acceptance tests, and do not confuse exploratory freedom with random clicking.

## 6. Additional methods and when to use them

| Method | Best question | Use when |
|---|---|---|
| Unit/component | Does a focused unit behave correctly? | Known local behavior, fast feedback, edge cases |
| Integration | Do real boundaries collaborate? | Database, filesystem, queue, process, or service seams |
| Contract | Does a consumer/provider interaction remain compatible? | Separate deploys, API/message boundaries, test doubles |
| End-to-end | Does a critical whole-system journey work near production conditions? | Release confidence for high-value journeys; keep few and stable |
| Property-based | Do invariants hold across a defined input domain? | Large input spaces, parsers, transformations, round trips, state machines |
| Metamorphic | When input A changes to B, how should the output relation change? | Exact output oracles are weak, expensive, or unavailable |
| Mutation | Would the suite detect plausible small faults? | Suspiciously green suites or high-risk logic |
| Model/state-transition | Are important states and valid/invalid transitions correct? | Stateful workflows, protocols, queues, workflows |
| Performance/load/capacity | Does the system meet latency, throughput, resource, or capacity targets? | Performance SLOs, bottlenecks, capacity planning |
| Fault injection/chaos | Does the system preserve steady state and recover under failure? | Resilience, failover, retry, timeout, and recovery mechanisms |
| Security/threat | Can an attacker bypass controls or abuse business logic? | Authentication, authorization, input, secrets, privacy, dependencies |
| Accessibility | Can people perceive, operate, understand, and use it? | UI changes, keyboard, screen reader, WCAG, localization |

### Layer and quality selection

Use the smallest test that can reliably answer the question, then add fidelity where the risk is real. Unit tests are usually fast and precise; integration and contract tests expose boundary defects; end-to-end tests provide user/system confidence but are slower, more expensive, and more brittle. Balance these using risk, speed, maintainability, utilization, reliability, and fidelity rather than relying on a fixed percentage.

Coverage is useful for finding unexercised code, but it does not prove that assertions are strong. A small mutation or property-based check can expose a weak oracle more clearly than line coverage alone.

## 7. Adaptive selection guide

| Situation | Start with | Add next | Avoid |
|---|---|---|---|
| Clear acceptance criterion and deterministic bug | Focused regression/unit test | Critical journey only if user-visible | Duplicating every case as E2E |
| Reproducible failure, cause unknown | Diagnostic/reproduction experiment | Root-cause regression and, if needed, journey | Declaring victory after a retry or a symptom patch |
| Unclear workflow or unfamiliar UX | Exploratory charter | Acceptance examples and stable journey | Scripting every exploratory observation |
| Large input domain or invariant | Property-based test | Explicit examples plus shrunk counterexample | Hand-picked examples only |
| Weak or unavailable output oracle | Metamorphic or model-based check | Diagnostic comparison | Treating a plausible relation as proof |
| Stateful workflow | State/model testing | Critical happy path and exception journey | Only isolated state assertions |
| API or service boundary | Contract test | Narrow integration and one critical journey | Full production-like integration for every case |
| Suspiciously green suite | Mutation on changed/high-risk logic | Strengthen tests for surviving mutants | Vanity mutation-score targets |
| Dependency, process, or recovery behavior | Controlled fault injection in staging | SLO/recovery validation | Uncontrolled production disruption |
| Latency, throughput, or capacity target | Performance baseline | Load/soak/stress experiment | Treating a lab score as field truth |
| UI or accessibility concern | Automated checks | Manual assistive-technology or real-user journey | Treating automated pass as full conformance |

Use both diagnostic and user-use testing when the technical cause is uncertain and the affected workflow is business-critical, when a bug may be invisible at the component level but harmful to the user, or when the fix changes an externally visible contract. For a clear, local, deterministic change, one focused test track is usually enough.

## 8. Guardrails

- Precommit predictions, thresholds, and stop conditions; changing them after seeing results creates false learning.
- Change one major factor at a time and retain a control, seed, repeat count, and environment record.
- Do not treat retries, one green run, coverage, or a mutation score as proof of correctness.
- Do not promote an experiment as a permanent test unless it expresses a stable oracle and important behavior.
- Do not run destructive fault injection, security attacks, load tests, or production experiments without explicit authorization, safe scope, observability, and rollback.
- Keep permanent regression tests narrow and stable; keep exploratory sessions focused and recorded.
- Validate property generators, models, metamorphic relations, and external oracles independently.
- Promote production discoveries into requirements, acceptance criteria, or regression tests so the same gap is not rediscovered.

## 9. GitHub-derived practices

These practices were found by inspecting the actual `SKILL.md`, reference, script, or schema files in public GitHub repositories. They are reimplemented as generic DeepCraft rules; no third-party prose or code is copied.

| Source | Useful practice | DeepCraft adaptation |
|---|---|---|
| [adewale/testing-best-practices](https://github.com/adewale/testing-best-practices/tree/82c6eccc0f6e1feeb82221b331b6f308209e7e20) | Test modes, negative controls, anti-patterns, eval health | Require a primary oracle, a negative control, and an expected-red check; audit false-green patterns |
| [voidmatcha/e2e-skills](https://github.com/voidmatcha/e2e-skills/tree/16463a426fa98e64ae62bfb1d9e24052dc20bb71) | Mechanical candidate scan followed by semantic refutation; protected oracle | Static findings are candidates only; a fresh verifier must attempt refutation before confirming |
| [gtapps/claude-code-hermit](https://github.com/gtapps/claude-code-hermit/tree/f4b4c7712b1aba587a8d52725a463b69636f6d11) | Red-capable feedback loop, prediction-targeted instrumentation, cleanup and full logs | Do not hypothesize without a runnable reproducer; retain complete evidence and remove instrumentation |
| [AI-native-Systems-Research/agentic-strategy-evolution](https://github.com/AI-native-Systems-Research/agentic-strategy-evolution/tree/34193512f9aecca8244c3a99c67873e578193319) | Hypothesis bundles with main/control/ablation/robustness arms and prediction-error taxonomy | Use conditional experiment bundles for uncertain, multi-factor work |
| [edwardyap90/counterfactual-engineering-skill](https://github.com/edwardyap90/counterfactual-engineering-skill/tree/26ff26d21ff5accb18a7d4ac67e25b9271c6c10d) | Same-base candidate worktrees and shared verification matrix | Compare credible fixes on isolated branches; never declare a winner when every candidate is ineligible |
| [HermeticOrmus/hypothesis-debugging-skills](https://github.com/HermeticOrmus/hypothesis-debugging-skills/tree/13f391c6b0e1627b8eccee188b5a681ccbc7ea40) | Reproduce, isolate, rank hypotheses, minimal fix, regression | Make Protocol D's hypothesis table and old-red/new-green proof explicit |
| [KadenMc/agentic-experiments](https://github.com/KadenMc/agentic-experiments/tree/a7ee8f0aa58d9b388d4337c8e77848d41bfa8e51) | Hypothesis -> Experiment -> Finding chain and provenance | Link every experiment and finding to a command, revision, seed, and evidence artifact |
| [aks-builds/quality-skills](https://github.com/aks-builds/quality-skills) | Context-first risk strategy, test impact selection, flake policy | Select must-run/should-run/optional tests from change impact and risk while retaining the full-suite gate |
| [jalyper/claude-code-tester-skill](https://github.com/jalyper/claude-code-tester-skill) | Plan -> validate -> execute -> debug artifact handoffs | Validate the test plan before execution and preserve structured failure artifacts |
| [AZANIR/qa-skills](https://github.com/AZANIR/qa-skills) | Lifecycle handoffs, risk traceability, test healing/review distinctions | Ideas only; GPL-3.0 source, so do not copy its prose or code into this skill |

### License and provenance boundary

- Apache-2.0 sources (`voidmatcha/e2e-skills`, `AI-native-Systems-Research/agentic-strategy-evolution`) and MIT sources (`gtapps/claude-code-hermit`, `edwardyap90/counterfactual-engineering-skill`, `HermeticOrmus/hypothesis-debugging-skills`, `KadenMc/agentic-experiments`, `aks-builds/quality-skills`, `jalyper/claude-code-tester-skill`) may be adapted with attribution and license preservation.
- `AZANIR/qa-skills` is GPL-3.0; use only independently reimplemented abstract ideas unless a separate license review approves more.
- The `adewale/testing-best-practices` license file was not found in the reviewed tree; do not copy its text or code without confirming terms.
- Repository README claims, star counts, vendor claims, and benchmark scores are not proof of correctness. Verify the actual files and run the relevant local gates.

## 10. False-green audit and generic verification contract

### 10.1 Test contract

For every high-value behavior, record:

```text
seam: <exact boundary under test>
primary_oracle: <observable postcondition>
negative_control: <safe fault, mutation, invalid input, or broken dependency>
expected_red: <why the unchanged test must fail under the negative control>
evidence: <command, exit code, log/report path>
```

If a safe negative control cannot be built, record `CANNOT_VERIFY`; do not upgrade a plausible green test into a strong test.

### 10.2 O1–O6 verification contract

| Contract | Requirement |
|---|---|
| **O1 — primary outcome** | Assert the intended user/business/system outcome, not merely that code ran |
| **O2 — oracle falsification** | Temporarily invalidate or invert the oracle and verify the test turns red |
| **O3 — fault sensitivity** | Inject a relevant dependency/product fault and verify the test detects it |
| **O4 — seam/write contract** | Prove the real boundary, input, output, and failure behavior are exercised |
| **O5 — repeat/isolation** | Bound repeats, seeds, state, ordering, and concurrency where relevant |
| **O6 — independent review** | A fresh read-only reviewer attempts to refute the result without relying on the author's conclusion |

O1–O6 are language- and framework-neutral. Playwright, pytest, Go, or other framework checks are adapters, not substitutes for the contract.

### 10.3 Audit flow

A test-quality or false-green audit has two stages:

1. **Mechanical candidates:** scan for skips, missing assertions, conditional assertions, swallowed errors, retries, sleeps, tautological checks, mock-echo assertions, fault-masking, weak selectors, environment coupling, and source changes made by a test healer.
2. **Semantic refutation:** a fresh reviewer reads the surrounding code and evidence, constructs the strongest alternative explanation, and returns exactly one of:
   - `CONFIRMED`: evidence proves the candidate;
   - `FALSE-POSITIVE`: the candidate is not a defect in context;
   - `NEEDS-CONTEXT`: evidence is insufficient.

Record `file:line`, mechanism, causal evidence, negative control, source-unchanged state, temporary artifacts remaining, and the next action. A static match is never a P0/P1 verdict by itself.

### 10.4 Repair boundary

The primary behavior, expected value, assertion target, scenario count, and evidence contract are immutable during a repair. A healer may change test mechanics such as locators, waits, setup, fixtures, or navigation only when those changes do not weaken the oracle. If the only way to pass is to broaden an assertion, skip/delete a test, increase a timeout to hide a race, or edit expected values without a requirement, return `NOFIX` and report the defect.

## 11. Experiment bundles, candidate comparison, and evidence provenance

### 11.1 When a bundle is warranted

Use a bundle when multiple credible causes or fixes exist, the change is high risk, the test suite is suspiciously green, or a single intervention would be expensive to undo. Keep ordinary deterministic fixes on the normal TDD path.

```text
bundle_id:
base_sha:
base_dirty: true|false
shared_verification_matrix:
arms:
  - id: main
    role: main
    hypothesis: <primary claim>
    independent_variable: <one factor>
    prediction: <expected result>
    metric: <measurement>
    threshold: <pass/fail rule>
  - id: control
    role: control
    hypothesis: <where the effect should not appear>
  - id: ablation
    role: ablation
    hypothesis: <which component is necessary>
  - id: robustness
    role: robustness
    hypothesis: <which boundary/workload changes the result>
  - id: candidate-fix
    role: candidate-fix
    hypothesis: <which repair strategy is credible>
preflight: <base, build/import, baseline, RED signal, treatment path>
```

Require the main arm and a baseline/control. Add ablation for multi-component changes, robustness when a real boundary can change the conclusion, and candidate-fix arms only when credible repairs differ materially.

### 11.2 Fail-closed preflight

Before interpreting any arm, record and verify: base revision and dirty state, build/import success, baseline command and output, RED regression signal, and that the treatment actually changes the exercised path. If preflight fails, mark the run `invalid`; a broken apparatus cannot refute a hypothesis.

### 11.3 Candidate worktrees

For high-risk or genuinely competing fixes, create two or three isolated worktrees from the same `base_sha`, record a manifest, run the identical shared verification matrix, and capture each candidate's patch, logs, diff, and revision. Never rank a candidate by diff size alone.

Hard eligibility gates are: correctness, types/build, regression, required domain checks, no deleted/weakened tests, root-cause fit, acceptable blast radius, rollback safety, and user-constraint fit. If every candidate is ineligible, the result is **no winner**; do not merge the least-bad candidate.

### 11.4 Verdict and error taxonomy

Keep the scientific verdict separate from why the prediction was wrong:

```text
verdict: supported | refuted | inconclusive | invalid
error_cause: direction | magnitude | regime | shape | tradeoff |
             implementation_failure | insufficient_signal | apparatus_invalid
```

Only a method-valid run can be `refuted`. Direction errors reopen root-cause analysis; magnitude/regime errors refine the mechanism; setup or detector failures are `invalid`; weak signal is `inconclusive`.

### 11.5 Evidence and flake envelope

Every material run records:

```text
run_id:
commit_sha: <base and candidate revision>
dirty_state: <clean or diff digest>
command:
exit_code:
full_log_path:
output_digest:
source_unchanged: true|false
temporary_artifacts_remaining: <count>
infrastructure_error: true|false
selected_tests:
selection_reason: must-run | should-run | optional
result:
next_action:
```

Use bounded repeats for flaky behavior, preserve logs/traces/screenshots/seeds, and classify a failure as `test_defect`, `product_regression`, `environment_failure`, or `ambiguous_specification`. Quarantine only with an owner, issue, and expiry; never turn retries, skips, or `fixme` into green evidence.

## 12. Research basis

1. [MIT Lincoln Laboratory — Hypothesis-Driven Development](https://www.ll.mit.edu/doc/hypothesis-driven-development) — hypotheses, predictions, measurements, iteration, and prioritizing uncertainty.
2. [MIT Lincoln Laboratory — Hypothesis-Driven Development PDF](https://www.ll.mit.edu/sites/default/files/project/doc/2020-07/Hypothesis-Driven%20Development_v4.pdf) — experiment intent, measurable outcomes, controls, and repeatability.
3. [Google Testing Blog — How Much Testing is Enough?](https://testing.googleblog.com/2021/06/how-much-testing-is-enough.html) — unit/integration/E2E balance, critical user journeys, quality attributes, and feedback loops.
4. [Google Testing Blog — SMURF: Beyond the Test Pyramid](https://testing.googleblog.com/2024/10/smurf-beyond-test-pyramid.html) — speed, maintainability, utilization, reliability, and fidelity tradeoffs.
5. [Martin Fowler — Exploratory Testing](https://martinfowler.com/bliki/ExploratoryTesting.html) — time-boxed learning, test design, execution, and interpretation.
6. [Martin Fowler — Test Pyramid](https://martinfowler.com/bliki/TestPyramid.html) — focused tests, intermediate integration tests, and few broad-stack tests.
7. [ISTQB Acceptance Testing Syllabus](https://istqb.org/wp-content/uploads/2024/11/ISTQB-CT-AcT_Syllabus_v1.0_2019.pdf) — acceptance criteria, user flows, risk-based selection, and exploratory testing.
8. [Cucumber — Behaviour-Driven Development](https://cucumber.io/docs/bdd/) — discovery, executable examples, rapid feedback, and living documentation.
9. [Hypothesis — property-based testing](https://hypothesis.readthedocs.io/en/latest/) — generated inputs, invariants, examples, and shrinking.
10. [Pact — contract testing](https://docs.pact.io/) — consumer/provider contracts and isolated verification.
11. [Google Cloud — Fault Injection Testing](https://docs.cloud.google.com/fault-injection-testing/overview) — controlled failure experiments, steady-state probes, and safety controls.
12. [Google Cloud — Chaos Engineering](https://cloud.google.com/blog/products/devops-sre/getting-started-with-chaos-engineering) — controlled disruption, steady state, measurement, and recovery.
