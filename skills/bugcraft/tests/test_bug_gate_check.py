#!/usr/bin/env python3
"""Tests for the BugCraft gate checker.

The point of these tests is that the gate must be able to go RED: a template with empty fields
must be rejected, and removing any single piece of evidence must fail the check. A checker that
only ever says READY would be worse than no gate at all.

Run:  python3 -m pytest ~/.opencode/skills/bugcraft/tests/test_bug_gate_check.py -q
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "bug_gate_check.py"

spec = importlib.util.spec_from_file_location("bug_gate_check", SCRIPT)
bgc = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(bgc)


def filled() -> str:
    """A completely evidenced bug file (template with every field populated)."""
    values = {
        "B0": {
            "expected": "exit code 0 and one row printed",
            "actual": "exit code 1, no rows",
            "acceptance": "ticket #42: resume must reprint the last row",
            "frequency": "10/10 runs",
            "redaction": "no secrets in loop output; token via $TOKEN",
        },
        "B1": {
            "command": "python3 -m pytest tests/test_resume.py::test_reprints -x",
            "first_run": "1 failed, exit 1 — IndexError at resume.py:88",
            "red_confirmed": "output matches the reported symptom (no rows printed)",
        },
        "B2": {
            "baseline_rate": "10/10",
            "minimized": "single-row fixture, resume directly after write",
        },
        "B3": {
            "H1": "if offset is not rewound, resume starts past EOF",
            "H2": "if the reader is closed, read returns []",
            "H3": "if the flush is async, resume races the writer",
            "redteam": "H1 survives premise/path/consequence; H2 refuted (reader still open)",
        },
        "B4": {
            "variable": "rewound offset only",
            "probe": "log [DEBUG-a4f2] offset before and after flush",
            "result": "offset past EOF after flush; H1 supported",
        },
        "B5": {
            "root_cause": "seek(0) never called after the buffered write",
            "change": "add seek(0) before read (resume.py, 1 line)",
        },
        "B6": {
            "seam": "tests/test_resume.py::test_reprints (real call site)",
            "red_proof": "fails before fix: IndexError, observed",
            "green_proof": "passes after fix, observed",
        },
        "B7": {
            "suite_exit": "0 (full suite: 212 passed, 0 failed)",
            "symptom_recheck": "original 10/10 loop now 0/10 failures",
            "evidence": "pytest output captured this turn; grep [DEBUG-] = 0 hits",
        },
        "B8": {
            "doable": "yes — CLI script with a real fixture and live stdout",
            "window": "3 consecutive full runs",
            "cycles": "3 (10:02, 10:07, 10:11)",
            "functions_total": "4",
            "functions_exercised": "4/4 (happy, boundary, invalid, state)",
            "new_bugs": "1 found in cycle 1, fixed and locked; 0 in cycles 2-3",
            "clean_window": "2 consecutive cycles with 0 new findings",
        },
        "B9": {
            "debug_artifacts": "0 [DEBUG-] hits, temp fixture deleted",
            "rollback": "git revert <sha>",
            "record": "ATTEMPTS.md line appended",
        },
    }
    out = []
    for gid, title, fields in bgc.GATES:
        out.append(f"## {gid} {title}")
        out.append("status: pass")
        for name in fields:
            out.append(f"{name}: {values[gid][name]}")
        if gid == "B3":
            for n in (1, 2, 3):
                out.append(f"H{n}: {values['B3'][f'H{n}']}")
        out.append("")
    return "\n".join(out)


# --- negative control: the unfilled template must be rejected -------------------------------

def test_template_is_rejected():
    result = bgc.check(bgc.TEMPLATE)
    assert result["ready"] is False
    assert len(result["problems"]) == len(bgc.GATES)


def test_template_skips_kebab_comment_fields():
    # `mode: fix   # hunt | fix | perf` must not count as evidence for anything
    sections, _ = bgc.parse(bgc.TEMPLATE)
    assert sections["B0"].get("expected", "") == ""


# --- positive control ----------------------------------------------------------------------

def test_fully_filled_file_is_ready(tmp_path):
    path = tmp_path / "BUG-resume.md"
    path.write_text(filled(), encoding="utf-8")
    proc = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "READY" in proc.stdout


def test_three_hypothesis_lines_satisfy_b3():
    result = bgc.check(filled())
    assert result["ready"] is True, result["problems"]


# --- each gate must fail on its own when evidence is removed -------------------------------

def test_missing_single_field_fails_and_names_it():
    text = filled().replace("root_cause: seek(0) never called after the buffered write", "root_cause:")
    result = bgc.check(text)
    assert result["ready"] is False
    assert any("B5" in p and "root_cause" in p for p in result["problems"])


def test_missing_section_is_reported():
    text = filled().split("## B6 Regression lock")[0] + "\n"
    result = bgc.check(text)
    assert result["ready"] is False
    assert any("B6" in p for p in result["problems"])


def test_two_hypotheses_is_not_enough():
    text = filled()
    text = text.replace("H3: if the flush is async, resume races the writer\n", "")
    result = bgc.check(text)
    assert result["ready"] is False
    assert any("hypotheses(2/3)" in p for p in result["problems"])


def test_soak_gate_missing_window_is_incomplete():
    text = filled().replace("window: 3 consecutive full runs", "window:")
    result = bgc.check(text)
    assert result["ready"] is False
    assert any("B8" in p and "window" in p for p in result["problems"])


def test_soak_gate_missing_function_matrix_is_incomplete():
    text = filled().replace("functions_exercised: 4/4 (happy, boundary, invalid, state)", "functions_exercised:")
    result = bgc.check(text)
    assert result["ready"] is False
    assert any("functions_exercised" in p for p in result["problems"])


def test_soak_not_doable_needs_a_visible_waiver():
    # a soak that cannot be run must still be recorded, with the reason stated
    text = filled()
    text = text.replace(
        "## B8 Soak & sweep\nstatus: pass",
        "## B8 Soak & sweep\nwaived: not doable — library has no runtime surface to drive",
    )
    result = bgc.check(text)
    assert result["ready"] is True, result["problems"]
    assert any("B8" in w and "not doable" in w for w in result["waived"])


def test_empty_waiver_is_not_honoured():
    # an empty `waived:` must not count as a waiver; the gate passes only because its
    # evidence fields are still filled in.
    text = filled().replace("## B8 Soak & sweep\nstatus: pass", "## B8 Soak & sweep\nwaived:")
    result = bgc.check(text)
    assert not any("B8" in w for w in result["waived"])
    assert result["ready"] is True, result["problems"]


def test_empty_waiver_does_not_excuse_missing_evidence():
    text = (
        filled()
        .replace("## B8 Soak & sweep\nstatus: pass", "## B8 Soak & sweep\nwaived:")
        .replace("window: 3 consecutive full runs", "window:")
    )
    result = bgc.check(text)
    assert result["ready"] is False
    assert any("B8" in p and "window" in p for p in result["problems"])


def test_empty_waiver_does_not_waive():
    text = filled().replace(
        "green_proof: passes after fix, observed", "green_proof:\nwaived:"
    )
    result = bgc.check(text)
    assert result["ready"] is False
    assert any("green_proof" in p for p in result["problems"])


def test_waiver_with_reason_is_visible_not_silent():
    text = filled().replace(
        "seam: tests/test_resume.py::test_reprints (real call site)", "seam:"
    ).replace("## B6 Regression lock\nstatus: pass", "## B6 Regression lock\nwaived: no seam exists; documented as architectural finding")
    result = bgc.check(text)
    assert result["ready"] is True, result["problems"]
    assert result["waived"] and "B6" in result["waived"][0]
    assert result["gates"][6]["status"] == "waived"


# --- cli behaviour -------------------------------------------------------------------------

def test_missing_file_exits_2():
    proc = subprocess.run([sys.executable, str(SCRIPT), "/nonexistent/bug.md"], capture_output=True, text=True)
    assert proc.returncode == 2


def test_template_flag_exits_0_and_is_parseable():
    proc = subprocess.run([sys.executable, str(SCRIPT), "--template"], capture_output=True, text=True)
    assert proc.returncode == 0
    sections, _ = bgc.parse(proc.stdout)
    assert set(sections) == {g[0] for g in bgc.GATES}


def test_incomplete_exit_code_is_1(tmp_path):
    path = tmp_path / "BUG-empty.md"
    path.write_text(bgc.TEMPLATE, encoding="utf-8")
    proc = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
    assert proc.returncode == 1
    assert "INCOMPLETE" in proc.stdout


def test_json_mode_shape(tmp_path):
    path = tmp_path / "BUG-resume.md"
    path.write_text(filled(), encoding="utf-8")
    proc = subprocess.run([sys.executable, str(SCRIPT), "--json", str(path)], capture_output=True, text=True)
    assert proc.returncode == 0
    import json

    payload = json.loads(proc.stdout)
    assert payload["ready"] is True
    assert [g["gate"] for g in payload["gates"]] == [g[0] for g in bgc.GATES]
