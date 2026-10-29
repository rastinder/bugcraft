#!/usr/bin/env python3
"""bugcraft gate checker — turns the BugCraft skill's B0-B9 gates into a hard, on-disk check.

Usage:
    bug_gate_check.py --template            # print a new bug file skeleton
    bug_gate_check.py <bug-file.md>         # check it
    bug_gate_check.py --json <bug-file.md>  # machine-readable result

Exit codes:
    0  READY      every gate has evidence (or an explicit, visible waiver)
    1  INCOMPLETE named gate fields are missing
    2  bad usage / unreadable file

What this proves, and what it does NOT: it proves every gate was *recorded* with the required
evidence fields. It cannot prove the evidence is true. Fabricating a field is lying, not gating.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# gate id -> (human title, required field names)
GATES: list[tuple[str, str, tuple[str, ...]]] = [
    ("B0", "Symptom contract", ("expected", "actual", "acceptance", "frequency", "redaction")),
    ("B1", "Feedback loop", ("command", "first_run", "red_confirmed")),
    ("B2", "Reproduce + minimise", ("baseline_rate", "minimized")),
    ("B3", "Ranked hypotheses", ("redteam",)),
    ("B4", "Isolate + instrument", ("variable", "probe", "result")),
    ("B5", "Minimal root-cause fix", ("root_cause", "change")),
    ("B6", "Regression lock", ("seam", "red_proof", "green_proof")),
    ("B7", "Fresh-evidence verification", ("suite_exit", "symptom_recheck", "evidence")),
    ("B8", "Soak & sweep", ("doable", "window", "cycles", "functions_total",
                            "functions_exercised", "new_bugs", "clean_window")),
    ("B9", "Close-out", ("debug_artifacts", "rollback", "record")),
]

MIN_HYPOTHESES = 3

TEMPLATE = """# BUG-<slug>

mode: fix          # hunt | fix | perf | postmortem
impact: P2         # P0 data loss / P1 broken / P2 degraded / P3 cosmetic
opened: <date>

## B0 Symptom contract
status: open
expected:
actual:
acceptance:
frequency:
redaction:

## B1 Feedback loop
status: open
command:
first_run:
red_confirmed:

## B2 Reproduce + minimise
status: open
baseline_rate:
minimized:

## B3 Ranked hypotheses
status: open
H1:
H2:
H3:
redteam:

## B4 Isolate + instrument
status: open
variable:
probe:
result:

## B5 Minimal root-cause fix
status: open
root_cause:
change:

## B6 Regression lock
status: open
seam:
red_proof:
green_proof:

## B7 Fresh-evidence verification
status: open
suite_exit:
symptom_recheck:
evidence:

## B8 Soak & sweep
status: open
# If the artifact cannot be live-driven, replace these fields with:
#   waived: not doable — <which condition failed and why>
doable:
window:            # e.g. "2 cycles + 10 min live observation"
cycles:
functions_total:
functions_exercised:   # e.g. "4/4 (happy, boundary, invalid, state)"
new_bugs:          # count + what happened to each (fixed / logged with owner)
clean_window:      # N consecutive cycles with 0 new findings

## B9 Close-out
status: open
debug_artifacts:
rollback:
record:
"""

FIELD_RE = re.compile(r"^\s*([A-Za-z][A-Za-z0-9_]*)\s*:\s*(.*)$")
SECTION_RE = re.compile(r"^##\s+B(\d)\b(.*)$")
HYPO_RE = re.compile(r"^\s*H(\d+)\s*:\s*(.+)$")


def parse(text: str) -> tuple[dict[str, dict[str, str]], dict[str, list[str]]]:
    """Return {gate_id: {field: value}} and {gate_id: [hypothesis bodies]}."""
    sections: dict[str, dict[str, str]] = {}
    hypotheses: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        m = SECTION_RE.match(line)
        if m:
            current = f"B{m.group(1)}"
            sections.setdefault(current, {})
            hypotheses.setdefault(current, [])
            continue
        if line.startswith("#"):  # another heading ends the section
            current = None
            continue
        if current is None:
            continue
        h = HYPO_RE.match(line)
        if h:
            body = h.group(2).strip()
            if body:
                hypotheses[current].append(body)
            continue
        f = FIELD_RE.match(line)
        if f:
            sections[current][f.group(1).lower()] = f.group(2).strip()
    return sections, hypotheses


def strip_comment(value: str) -> str:
    """Drop a trailing '# comment' note and surrounding whitespace/quotes."""
    value = re.sub(r"\s+#\s.*$", "", value)
    return value.strip().strip("\"'").strip()


def check(text: str) -> dict:
    sections, hypotheses = parse(text)
    result: dict = {"ready": True, "gates": [], "problems": [], "waived": []}

    for gid, title, fields in GATES:
        gate = {"gate": gid, "title": title, "status": "pass", "missing": [], "waived": None}
        if gid not in sections:
            gate["status"] = "missing_section"
            gate["missing"] = list(fields)
            result["problems"].append(f"{gid} {title}: section '## {gid} {title}' not found")
            result["ready"] = False
            result["gates"].append(gate)
            continue

        data = sections[gid]
        waiver = strip_comment(data.get("waived", ""))
        if waiver:
            gate["status"] = "waived"
            gate["waived"] = waiver
            result["waived"].append(f"{gid} waived: {waiver}")
            result["gates"].append(gate)
            continue

        for name in fields:
            if not strip_comment(data.get(name, "")):
                gate["missing"].append(name)
        if gid == "B3":
            got = len(hypotheses.get(gid, []))
            if got < MIN_HYPOTHESES:
                gate["missing"].append(f"hypotheses({got}/{MIN_HYPOTHESES})")

        if gate["missing"]:
            gate["status"] = "incomplete"
            result["ready"] = False
            result["problems"].append(f"{gid} {title}: missing {', '.join(gate['missing'])}")
        result["gates"].append(gate)

    return result


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:]]
    as_json = "--json" in args
    args = [a for a in args if a != "--json"]

    if not args:
        print(__doc__)
        return 2
    if args[0] in ("--template", "-t"):
        print(TEMPLATE)
        return 0

    path = Path(args[0])
    if not path.is_file():
        print(f"bug_gate_check: no such file: {path}", file=sys.stderr)
        return 2

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"bug_gate_check: cannot read {path}: {exc}", file=sys.stderr)
        return 2

    result = check(text)
    if as_json:
        print(json.dumps(result, indent=2))
        return 0 if result["ready"] else 1

    print(f"BugCraft gates — {path}")
    for gate in result["gates"]:
        mark = {"pass": "PASS", "waived": "WAIVED", "incomplete": "MISSING", "missing_section": "NO SECTION"}[gate["status"]]
        extra = ""
        if gate["status"] == "waived":
            extra = f" ({gate['waived']})"
        elif gate["missing"]:
            extra = f" ({', '.join(gate['missing'])})"
        print(f"  {gate['gate']} {gate['title']:<28} {mark}{extra}")

    if result["waived"]:
        print("\nWaivers (visible on purpose — a waiver is a claim, not a pass):")
        for w in result["waived"]:
            print(f"  - {w}")

    if result["ready"]:
        print("\nREADY — every gate recorded. This proves the gates were filled, NOT that the")
        print("evidence inside is true; verify the referenced command output before committing.")
        return 0

    print("\nINCOMPLETE — do not claim the bug is fixed. Missing:")
    for problem in result["problems"]:
        print(f"  - {problem}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
