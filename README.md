# BugCraft — the one gated bug-fixing skill for AI coding agents

**BugCraft** turns "fix this bug" into a **gated, evidence-checked run**: ten hard gates from symptom
contract to a live soak that keeps babysitting your script until no new bug appears. Built for
**Claude Code**, **opencode**, **Codex**, **Gemini CLI** and any agent that loads a `SKILL.md`.
Bundled with **DeepCraft**, the TDDAB software-engineering methodology it plugs into.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Gates](https://img.shields.io/badge/gates-10%20(B0%E2%80%93B9)-brightgreen)](skills/bugcraft/SKILL.md)
[![Tests](https://img.shields.io/badge/tests-18%20passing-success)](skills/bugcraft/tests/test_bug_gate_check.py)
[![Dependencies](https://img.shields.io/badge/dependencies-none-lightgrey)](skills/bugcraft/scripts/bug_gate_check.py)
[![Agents](https://img.shields.io/badge/works%20with-Claude%20Code%20%7C%20opencode%20%7C%20Codex%20%7C%20Gemini-blueviolet)](#compatibility)

> Debugging skills are usually advice. Advice gets skipped under pressure — exactly when it matters.
> BugCraft gives the agent a **file it must fill** and a **checker that fails the commit** until the
> evidence exists.

---

## Contents

- [Why this exists](#why-this-exists)
- [The 10 gates](#the-10-gates)
- [Install](#install)
- [Quickstart](#quickstart)
- [The gate is enforced, not advisory](#the-gate-is-enforced-not-advisory)
- [The soak gate: babysit the script until nothing new breaks](#the-soak-gate-babysit-the-script-until-nothing-new-breaks)
- [What the soak actually caught](#what-the-soak-actually-caught)
- [DeepCraft: the methodology underneath](#deepcraft-the-methodology-underneath)
- [Compatibility](#compatibility)
- [Provenance and credits](#provenance-and-credits)
- [FAQ](#faq)
- [License](#license)

---

## Why this exists

There are hundreds of "debugging" and "bug fixing" skills for AI agents. Most are three paragraphs
of advice with no enforcement, so an agent under time pressure skips straight to a guess-fix.

Worse: a lot of the popular link lists are **fiction**. Of the 50 "bug finding / bug fixing" skills
circulating in one such list, **45 do not exist** — several point at repositories that contain no
skills directory at all (`anthropics/claude-code`, `openai/codex`, `microsoft/vscode`,
`langchain-ai/langchain`, `vercel/ai`), and eight point at repositories that 404. The five that do
exist describe the same handful of methods with different wording.

BugCraft is that handful of methods, consolidated once, with the enforcement none of them had:

- **One skill, not fifty** — find, diagnose, repair, soak, close out.
- **Gated** — every gate writes required fields into `.swarm/bugs/BUG-<slug>.md`; a stdlib checker
  refuses `READY` until they exist.
- **Verified sources** — each method is attributed to a real, MIT-licensed skill (see
  [provenance](skills/bugcraft/references/provenance.md)).
- **Zero dependencies** — pure Python 3 stdlib for the checker; the rest is markdown.

## The 10 gates

| Gate | Name | What must exist before moving on |
|---|---|---|
| **B0** | Symptom contract | expected vs actual, acceptance criteria, baseline frequency, redaction |
| **B1** | Feedback loop | **one agent-runnable command, already run once**, red on *this* symptom |
| **B2** | Reproduce + minimise | the user's failure mode (not a neighbour), smallest load-bearing scenario, determinism |
| **B3** | Ranked hypotheses | 3–5 falsifiable, each with confidence + disconfirming evidence, red-teamed |
| **B4** | Isolate + instrument | one variable per probe, tagged `[DEBUG-xxxx]` logs, boundary instrumentation |
| **B5** | Minimal root-cause fix | one change at the source; recurrence risk addressed; no "probable root cause" dressed as fact |
| **B6** | Regression lock | correct seam, observed **red→green**, plus **revert-to-verify** |
| **B7** | Fresh-evidence verification | full suite exit 0 **this turn**, original symptom re-checked, proof matched to the surface |
| **B8** | **Soak & sweep** | live window with **0 new findings**, function-by-function matrix, edge-case discovery (conditional — see below) |
| **B9** | Close-out | debug artifacts removed, rollback path, attempt recorded, postmortem countermeasure |

Three iron laws run through all of them: **no fix without a root cause**, **no hypothesis without a
red-capable loop**, **no completion claim without fresh evidence from this turn**.

## Install

### Agent skill manager

```bash
npx skills add rastinder/bugcraft --skill bugcraft
npx skills add rastinder/bugcraft --skill deepcraft
```

### Manual (Claude Code, opencode, Gemini CLI, project-local)

```bash
git clone https://github.com/rastinder/bugcraft.git
cp -r bugcraft/skills/* ~/.claude/skills/     # Claude Code
cp -r bugcraft/skills/* ~/.opencode/skills/   # opencode
cp -r bugcraft/skills/* ~/.gemini/skills/     # Gemini CLI
cp -r bugcraft/skills/* .agents/skills/       # this project only
```

Then load it the way your harness loads skills (`skill bugcraft` in Claude Code / opencode), or let
`AGENTS.md` / `CLAUDE.md` auto-load it. **No configuration, no API keys, no build step.**

## Quickstart

```bash
# 1. create the evidence file for this bug
python3 skills/bugcraft/scripts/bug_gate_check.py --template > .swarm/bugs/BUG-checkout-total.md

# 2. fill the gates as you work (not at the end — that is fiction)

# 3. check
python3 skills/bugcraft/scripts/bug_gate_check.py .swarm/bugs/BUG-checkout-total.md
```

```
BugCraft gates — .swarm/bugs/BUG-checkout-total.md
  B0 Symptom contract             PASS
  B1 Feedback loop                PASS
  B2 Reproduce + minimise         MISSING (baseline_rate, minimized)
  ...
INCOMPLETE — do not claim the bug is fixed. Missing:
  - B2 Reproduce + minimise: missing baseline_rate, minimized
```

Exit `0` + `READY` means every gate is recorded. Exit `1` names exactly what is missing. Exit `2`
is bad usage. A **waiver** is allowed only with a written reason and stays printed in the output — the
one legitimate case is B6 when no correct regression seam exists, which is itself the finding.

## The gate is enforced, not advisory

Wire it into a pre-commit hook and the claim "the bug is fixed" stops being an opinion:

```bash
# .git/hooks/pre-commit — block a commit that skips the gates
for f in $(git diff --cached --name-only | grep '^\.swarm/bugs/.*\.md$'); do
  python3 skills/bugcraft/scripts/bug_gate_check.py "$f" || {
    echo "BugCraft gates incomplete in $f"; exit 1; }
done
```

The checker proves the gates were **recorded** — it cannot prove the evidence is true. That
distinction is stated in the tool's own output, because a green check you can fake is worth less
than an honest red one.

## The soak gate: babysit the script until nothing new breaks

A single green run is a snapshot, not a verdict. **B8** drives the real artifact with live tools for
a sustained window and only stops when a **full cycle passes with no new finding**.

It is **conditional** — it runs only when all four doability conditions hold:

1. the artifact can be driven without production credentials or destructive effects (or a safe
   sandbox exists);
2. one cycle completes in bounded time, or can be interrupted safely;
3. live observation is available (console, logs, network, DOM, exit codes);
4. failures are attributable to a function or step.

Otherwise it records `waived: not doable — <condition>` and moves on. A library with no runtime
surface is a legitimate skip; **an interactive script you never ran is not**, and re-running the unit
tests is not a soak.

**Function-by-function sweep** — every public function / endpoint / route / command, across five
dimensions, so "all scenarios covered" is a measured fact instead of a hope:

| dimension | run |
|---|---|
| happy path | valid representative input |
| boundary | empty / zero / one / max / oversized / unicode |
| invalid | wrong type, missing field, malformed, null |
| error path | dependency down, timeout, permission denied, disk full, offline |
| state | called twice, out of order, cancelled mid-flight, restarted, resumed |

Windows by artifact type (interactive ≥ 2 cycles + 10 min, batch ≥ 3 full runs, flaky ≥ 100
iterations, scheduler ≥ 1 real trigger), plus property/fuzz inputs, sequence permutations, locale and
timezone variation, adversarial input, threshold neighbours — and the **HICCUPS / FEW HICCUPS**
oracles (History, Image, Comparable, Claims, User expectations, Product, Standards, Familiarity,
Explainability, World) for finding bugs no spec mentions.

Each new finding resets the clean clock and goes back through B2→B6.

## What the soak actually caught

A deliberately trivial module, with green unit tests, soaked for four cycles:

| Cycle | Input | Result |
|---|---|---|
| 1 | `last_n([1,2,3,4], 2)` | ✅ `c,d` |
| 2 | `n=0` | 🐞 **returned the whole list** — `items[-0:]` is `items[0:]` |
| 3 | `n="x"` | 🐞 **raw `ValueError` traceback** leaked to the user |
| 4 | `n > len` | ✅ all items |

Both bugs were invisible to the unit tests and obvious to the soak. Both were fixed, locked with
regression tests, and the re-soak produced a clean window. That is the entire argument for B8.

## DeepCraft: the methodology underneath

**DeepCraft** is the TDDAB engineering method BugCraft plugs into:
`INTAKE → EXPLORE → TDDAB PLAN → EXECUTE → PROTOCOL D → FINALIZE`, with hard gates 0–5 for memory,
planning, evidence, false-green rejection, visual verification and multi-branch benchmarking.

Its **GATE 6** makes BugCraft mandatory for any defect: no first fix edit without B0+B1, no commit
until the checker exits 0, and no close-out without the B8 soak. Protocol D keeps its names, BugCraft
supplies the detail — the skill includes a D0–D6 → B0–B9 mapping table so neither document
contradicts the other.

Use DeepCraft alone for feature work; it pulls BugCraft in automatically when something breaks.

## Compatibility

| Harness | How it loads | Status |
|---|---|---|
| Claude Code | `~/.claude/skills/<name>/SKILL.md`, `skill <name>` | tested |
| opencode | `~/.opencode/skills/<name>/SKILL.md`, `skill <name>` | tested |
| Gemini CLI | `~/.gemini/skills/<name>/SKILL.md` | tested (skill root) |
| Codex / any `AGENTS.md` agent | reference the path from `AGENTS.md` | portable markdown |
| Project-local agents | `<repo>/.agents/skills/<name>/SKILL.md` | tested |

Requires Python 3.9+ for `scripts/bug_gate_check.py` (f-strings and `list[...]` annotations are the
only modern syntax). Everything else is plain markdown.

## Provenance and credits

BugCraft is a consolidation, not an invention. Every method traces to a real, MIT-licensed skill:

| Source | Contributed |
|---|---|
| [`obra/superpowers@systematic-debugging`](https://github.com/obra/superpowers) | iron law, four-phase order, multi-component boundary instrumentation |
| [`obra/superpowers@verification-before-completion`](https://github.com/obra/superpowers) | the fresh-evidence gate, claim/evidence table |
| [`khasky/awesome-agent-skills@awesome-bug-fix`](https://github.com/khasky/awesome-agent-skills) | feedback-loop ladder, loop tightening, signature triage, redaction, red-team pass |
| [`khasky/awesome-agent-skills@awesome-root-cause`](https://github.com/khasky/awesome-agent-skills) | Ishikawa sweep, why-chain to a systemic gap, Poka-Yoke countermeasures |
| [`wshobson/agents@debugging-strategies`](https://github.com/wshobson/agents) | flaky, performance and production debugging patterns |
| [`mattpocock/skills@diagnosing-bugs`](https://github.com/mattpocock/skills) | red-capable loop criteria, minimise-to-load-bearing, correct-seam rule, `[DEBUG-]` tagging |

Additional methods (bisect exit-code contract, determinism recipe, flaky-vs-environment-vs-data
triage, revert-to-verify, severity × priority matrix, HICCUPS oracles, risk-first ordering,
blameless postmortem) come from MIT-licensed QA skills, documented per-item in
[`skills/bugcraft/references/provenance.md`](skills/bugcraft/references/provenance.md) — including
the verification that 45 of the 50 advertised skills do not exist.

MIT licensed. See [LICENSE](LICENSE) and [CREDITS.md](CREDITS.md).

## FAQ

<details>
<summary><b>Is this just another prompt?</b></summary>

No. The prose is the smaller half. The enforcement is `scripts/bug_gate_check.py`: a bug is not
"fixed" until the evidence file passes, and the same command can fail a commit in CI.
</details>

<details>
<summary><b>Does it work without network access or an LLM call?</b></summary>

Yes. Nothing in BugCraft calls a model or the network. The checker is stdlib Python; the gates are
markdown instructions your agent follows.
</details>

<details>
<summary><b>Will it work for a project with no tests?</b></summary>

Yes, and it will say something uncomfortable: B6 requires a **correct seam**, and if the code has
none, that missing seam is recorded as an architectural finding instead of a fake test. That is
deliberate — a shallow test that can never fail is worse than an honest gap.
</details>

<details>
<summary><b>Does it only work for Python?</b></summary>

The method is language-agnostic (it has per-language failure notes for Python, Go, TypeScript and
Rust). Only the checker is Python, and it just parses your bug file.
</details>

<details>
<summary><b>How is this different from <code>systematic-debugging</code> or <code>diagnosing-bugs</code>?</b></summary>

Those are the sources for B1–B5 and they are excellent. BugCraft adds what they leave out: a fixed
evidence file, a checker that fails closed, fresh-evidence rules per surface (UI, persistence, race,
config, long-running), **revert-to-verify**, and the **B8 soak** with a function-by-function matrix.
</details>

<details>
<summary><b>Why "baby sit the script"?</b></summary>

Because a bug you found once is a bug you will meet again. The soak is the difference between "the
repro passed" and "I watched it run for a while and nothing new broke".
</details>

<details>
<summary><b>Can it run in CI?</b></summary>

Yes — run `bug_gate_check.py` on the committed bug files. It exits `0`/`1`/`2` and has a `--json`
mode for machine consumption.
</details>

## License

MIT © 2026 Rastinder — see [LICENSE](LICENSE).
Skills consolidated from MIT-licensed sources; attribution in [CREDITS.md](CREDITS.md).

---

**Topics:** agent skills · Claude Code skills · opencode skill · Codex skill · AI coding agent ·
bug fixing skill · debugging skill · root cause analysis · TDD · test-driven development · soak
testing · exploratory testing · code review · software quality
