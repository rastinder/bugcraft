# Provenance — what in that 50-skill list actually exists

The user supplied 50 install commands for "bug-finding" and "bug-fixing" skills. Before
consolidating, each repository was checked directly (GitHub API tree listing for `SKILL.md`
paths, 2026-10-29). **Most of the list does not exist as described.** This file records the
check so nobody rebuilds the same list believing it was verified.

Verdict key: **REAL** = the named skill exists at that path · **RENAMED** = the repo has an
equivalent skill under a different name · **ABSENT** = the repo exists but has no such skill ·
**NO REPO** = the repository itself 404s.

## Summary

| Verdict | Count of the 50 entries |
|---|---|
| REAL (exact name + repo) | 3 |
| RENAMED / close equivalent | 2 |
| ABSENT in an existing repo | 37 |
| NO REPO (404) | 8 |

Only 5 of the 50 point at a skill that can actually be installed. The combined `bugcraft` skill
is therefore built from the 4 real entries plus 2 real skills that were *not* on the list but are
the strongest sources for this method.

## Per-repository evidence

| Repo | `SKILL.md` count | Bug/debug/fix skills actually present |
|---|---|---|
| `obra/superpowers` | 15 | `systematic-debugging`, `verification-before-completion` |
| `khasky/awesome-agent-skills` | 49 | `awesome-bug-fix`, `awesome-root-cause` |
| `wshobson/agents` | 185 | `debugging-strategies`, `parallel-debugging` (under `plugins/*/skills/`) |
| `mattpocock/skills` | — | `diagnosing-bugs` (**not on the list**, best-in-class) |
| `mcp-use/mcp-use` | 6 | none (only `mcp-builder`, `chatgpt-app-builder`, `mcp-apps-builder`) |
| `vercel/ai` | 15 | none bug-related |
| `boshu2/agentops` | 70 | none (`bug-hunt` absent) |
| `ComposioHQ/awesome-claude-skills` | 864 | none — these are vendor integrations (`bugsnag-automation`, `bugherd-automation`), not debugging skills |
| `anthropics/claude-code` | 0 | none (no skills directory at all) |
| `openai/codex` | 0 | none |
| `microsoft/vscode` | 0 | none |
| `langchain-ai/langchain` | 0 | none |
| `opencode-ai/opencode` | 0 | none |
| `gurbaxani/ai-skills` | — | repository not found |
| `danielfernandez/claude-code-skills` | — | repository not found |
| `elie222/instructor` | — | repository not found at that path |
| `codeium/windsurf` | — | repository not found at that path |
| `google/gemini` | — | repository not found at that path |

## Mapping: list entry → reality

| # | Claimed skill | Verdict |
|---|---|---|
| 1 | `khasky/awesome-agent-skills@awesome-bug-fix` | **REAL** |
| 6 | `obra/superpowers@systematic-debugging` | **REAL** |
| 12, 13 | `wshobson/agents@debugging` / `@find-bugs` | **RENAMED** → `debugging-strategies` |
| 18 | `anthropics/claude-code@root-cause-analysis` | **RENAMED** → `khasky/awesome-agent-skills@awesome-root-cause` |
| 2, 3, 4, 5, 7–11, 14–17, 19–25 | bug-hunt, bug-hunter, auto-bug-fixer, debugging, bug-report, reproduce-bug, crash-analysis, find-bugs, bug-finder, crash-dump-analysis, error-analysis | **ABSENT** (repo exists, skill does not) or **NO REPO** |
| 26–50 | every `bug-fix` / `fix-bug` / `patch-bug` / `fix-issue` / `bug-resolution` / `bug-patch` / `patch` entry | **ABSENT** or **NO REPO** — all 25 |

Note `anthropics/claude-code` accounts for 12 of the list's entries and contains **zero** skills;
its `.claude/` directory holds agent configuration, not loadable skills.

## Why consolidation was still correct

The 50 entries, where real, all describe the same small set of methods: build a red-capable
feedback loop, reproduce and minimise, rank falsifiable hypotheses, instrument one variable at a
time, fix at the source, lock with a regression test, verify with fresh evidence, close out with
root-cause countermeasures. `bugcraft` keeps every one of those methods once, in one gated run,
and adds the missing enforcement (an on-disk gate file plus a checker) that none of the source
skills had. Installing the real four separately would duplicate the same method with different
wording and no shared gate, which is exactly the fragmentation this consolidation removes.

## Licences

All sources used are MIT:

- `obra/superpowers` — MIT
- `khasky/awesome-agent-skills` — MIT (declared in its SKILL.md frontmatter)
- `wshobson/agents` — MIT
- `mattpocock/skills` — MIT

Content was rewritten and consolidated for this skill rather than copied verbatim; the method
attribution above records where each step came from.

## Second source set — the gemini QA skills (folded 2026-10-29)

`~/.gemini/skills` carried seven skills overlapping BugCraft. All were read, the unique methods
were folded in, then they were removed (backup: `/tmp/gemini-qa-skills-20261029.tgz`).

| Skill | Lines | Verdict | Destination / what was deliberately NOT taken |
|---|---|---|---|
| `systematic-debugging` | 283 | already fully absorbed (it is a primary source) | Iron Laws, B1-B4 ordering |
| `verification-before-completion` | 120 | already fully absorbed (primary source) | B7 gate function, claim/evidence table |
| `bug-reproduction` | 410 | 4 new items folded | bisect exit-code contract + untestable/skip trap, determinism recipe, flaky-vs-environment-vs-data table, revert-to-verify (B1/B2/B6) |
| `ai-bug-triage` | 417 | only the severity x priority matrix folded | hunt ranking. Not taken: fingerprint/cluster/ticket-generation pipeline (CI ops, not bug repair) |
| `exploratory-testing` | 313 | HICCUPS / FEW HICCUPS oracles folded | B8 soak sweep. Not taken: SBTM charter management and team session logistics |
| `quality-postmortem` | 383 | core rules folded | B9 blameless/systemic rule, owned+dated action items, two-metric improvement, escaped-defect classes. Not taken: suite-health dashboards, retro templates |
| `risk-based-testing` | 337 | impact x probability + churn folded | hunt ordering and B8 targeting. Not taken: the 6-phase risk-matrix deliverable workflow |

Dangling "Related skills" mentions of the retired names remain in ~25 other gemini skills. They
are informational links and were left alone; a CI triage pipeline is not replaced by BugCraft, so
repointing them would be a lie. `~/.gemini/skills/RETIRED-SKILLS.md` records the mapping.
