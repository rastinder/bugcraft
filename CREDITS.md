# Credits

BugCraft is a **consolidation**, not an original invention. The methods it enforces come from
MIT-licensed agent skills, rewritten and merged into a single gated run. DeepCraft is the TDDAB
methodology by Rastinder that BugCraft plugs into.

## Upstream skills (all MIT)

| Skill | Author / repo | What BugCraft took |
|---|---|---|
| `systematic-debugging` | [obra/superpowers](https://github.com/obra/superpowers) | iron law ("no fixes without root cause"), four-phase ordering, multi-component boundary instrumentation, data-flow tracing |
| `verification-before-completion` | [obra/superpowers](https://github.com/obra/superpowers) | fresh-evidence gate function, claim/evidence table, rationalization prevention |
| `awesome-bug-fix` | [khasky/awesome-agent-skills](https://github.com/khasky/awesome-agent-skills) (MIT, author Khasky) | ten-rung feedback-loop ladder and tightening, signature triage table, redaction rules, acceptance pinning, one-variable probe discipline, red-team pass, surface-specific proof |
| `awesome-root-cause` | [khasky/awesome-agent-skills](https://github.com/khasky/awesome-agent-skills) (MIT, author Khasky) | Ishikawa sweep, why-chain to a systemic gap, Poka-Yoke countermeasures, A3-style close-out |
| `debugging-strategies` | [wshobson/agents](https://github.com/wshobson/agents) | flaky-bug, performance-regression and production debugging patterns |
| `diagnosing-bugs` | [mattpocock/skills](https://github.com/mattpocock/skills) | red-capable loop completion criteria, minimise-to-load-bearing, correct-seam rule, `[DEBUG-....]` log tagging |

## Additional methods

Gathered from MIT-licensed QA skills and folded into the gates:

- **bisect exit-code contract** (0 = good, 1–124 = bad, 125 = skip), the untestable-commit trap and
  the determinism recipe — from `bug-reproduction`.
- **flaky vs environment-specific vs data-dependent vs genuinely unreproducible** triage table, and
  **revert-to-verify** — from `bug-reproduction`.
- **severity × priority matrix** (impact vs urgency, kept independent) — from `ai-bug-triage`.
- **HICCUPS / FEW HICCUPS oracle lenses** — from `exploratory-testing`.
- **risk-first ordering** (impact × probability, code churn as a probability signal, near-misses as
  evidence) — from `risk-based-testing`.
- **blameless-is-systemic postmortem rules**, owned+dated action items, two-metric improvement,
  escaped-defect classes — from `quality-postmortem`.

Per-item verification, and the reasons some upstream workflows were **deliberately not** copied
(CI fingerprinting/deduplication pipelines, risk-heatmap deliverables, SBTM session management,
suite-health dashboards), are recorded in
[`skills/bugcraft/references/provenance.md`](skills/bugcraft/references/provenance.md).

## Note on the "50 bug skills" list

A widely circulated list claims 50 installable bug-finding and bug-fixing skills. Checking every
entry against the actual repositories (2026-10-29) found **3 exact matches, 2 renamed equivalents,
37 absent and 8 pointing at repositories that do not exist**. `anthropics/claude-code` alone accounts
for 12 of the list's entries and contains zero `SKILL.md` files. BugCraft was built from the entries
that are real, plus two strong sources that were not on the list at all.

## DeepCraft

`skills/deepcraft` is the TDDAB methodology (Test-Ahead-Behavior, Memory Bank, evidence-driven
experiments, Protocol D debugging) maintained by Rastinder, extended here with **GATE 6**, which
makes BugCraft the mandatory method for any defect.

## License

MIT. If you reuse a technique from BugCraft, credit the upstream authors above rather than this repo
alone — that is where the thinking came from.
