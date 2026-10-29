#!/usr/bin/env python3
"""DeepSWE Benchmark Runner for DeepCraft skill evaluation.

Analyzes all DeepSWE tasks and produces metrics on how well the deepcraft
methodology covers each task's requirements.

Usage:
    python3 deepswe_benchmark.py                    # Analyze all tasks
    python3 deepswe_benchmark.py --task cliffy-config-file-parsing  # Single task
    python3 deepswe_benchmark.py --lang python       # Filter by language
    python3 deepswe_benchmark.py --report            # Generate markdown report
"""

import json
import sys
import os
import re
import argparse
from pathlib import Path
from datetime import datetime

TASKS_DIR = Path("/home/ras/deep-swe/deep-swe/tasks")
OUTPUT_DIR = Path("/home/ras/.opencode/skills/deepcraft/scripts/results")


def parse_task(task_dir: Path) -> dict:
    """Parse a single DeepSWE task and extract metrics."""
    task_id = task_dir.name
    
    # Read task.toml
    toml_path = task_dir / "task.toml"
    repo_url = ""
    language = ""
    category = ""
    base_commit = ""
    if toml_path.exists():
        content = toml_path.read_text()
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("repository_url"):
                repo_url = line.split("=", 1)[1].strip().strip('"')
            elif line.startswith("language"):
                language = line.split("=", 1)[1].strip().strip('"')
            elif line.startswith("category"):
                category = line.split("=", 1)[1].strip().strip('"')
            elif line.startswith("base_commit_hash"):
                base_commit = line.split("=", 1)[1].strip().strip('"')
    
    # Read instruction.md
    inst_path = task_dir / "instruction.md"
    inst_content = ""
    inst_words = 0
    inst_sentences = 0
    if inst_path.exists():
        inst_content = inst_path.read_text()
        inst_words = len(inst_content.split())
        # Count sentences (rough)
        inst_sentences = len([s for s in re.split(r'[.!?]+', inst_content) if s.strip()])
    
    # Analyze test.patch (training mode only)
    test_patch_path = task_dir / "tests" / "test.patch"
    test_fns = []
    assertion_count = 0
    test_patch_lines = 0
    test_files = []
    if test_patch_path.exists():
        tpc = test_patch_path.read_text()
        test_patch_lines = tpc.count("\n")
        
        # Extract test files
        test_files = re.findall(r'^diff --git a/.+ b/(.+)$', tpc, re.M)
        
        # Extract test functions
        # Python
        test_fns.extend(re.findall(r'^\+\s*def\s+(test_\w+)', tpc, re.M))
        # Go
        test_fns.extend(re.findall(r'^\+\s*func\s+(Test\w+)', tpc, re.M))
        # TypeScript/JS
        test_fns.extend(re.findall(r'^\+\s*test\(\s*["\']([^"\']+)', tpc, re.M))
        test_fns.extend(re.findall(r'^\+\s*it\(\s*["\']([^"\']+)', tpc, re.M))
        test_fns.extend(re.findall(r'^\+\s*describe\(\s*["\']([^"\']+)', tpc, re.M))
        # Rust
        test_fns.extend(re.findall(r'^\+\s*fn\s+(test_\w+)', tpc, re.M))
        
        # Count assertions
        assertion_count = len(re.findall(r'^\+.*(?:self\.)?(?:assert|require|expect|attest)\w*\s*[\(.]', tpc, re.M))
    
    # Analyze solution.patch
    sol_path = task_dir / "solution" / "solution.patch"
    sol_lines_added = 0
    sol_files = []
    sol_new_files = 0
    if sol_path.exists():
        spc = sol_path.read_text()
        sol_lines_added = len([l for l in spc.split("\n") if l.startswith("+") and not l.startswith("+++")])
        sol_files = re.findall(r'^diff --git a/.+ b/(.+)$', spc, re.M)
        sol_new_files = spc.count("new file mode")
    
    # Extract requirements from instruction (simplified DSA-1)
    requirements = []
    if inst_content:
        raw_sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', inst_content.strip())
        for sent in raw_sentences:
            sent = sent.strip()
            if len(sent) < 10:
                continue
            s_lower = sent.lower()
            rtype = "context"
            priority = "low"
            if any(k in s_lower for k in ["must", "cannot", "never", "always"]):
                rtype = "requirement"; priority = "high"
            elif any(k in s_lower for k in ["should", "when ", " if ", "unless"]):
                rtype = "condition"; priority = "high"
            elif any(k in s_lower for k in ["add ", "create ", "implement ", "support ", "extend "]):
                rtype = "action"; priority = "high"
            elif any(k in s_lower for k in ["default", "defaults to", "fallback"]):
                rtype = "default"; priority = "medium"
            elif any(k in s_lower for k in ["throw", "error", "raise", "reject"]):
                rtype = "error_behavior"; priority = "high"
            requirements.append({"type": rtype, "priority": priority, "text": sent[:150]})
    
    high_priority = [r for r in requirements if r["priority"] == "high"]
    
    return {
        "task_id": task_id,
        "language": language,
        "category": category,
        "repo_url": repo_url,
        "base_commit": base_commit[:12] if base_commit else "",
        "instruction_words": inst_words,
        "instruction_sentences": inst_sentences,
        "requirement_count": len(requirements),
        "high_priority_count": len(high_priority),
        "test_function_count": len(set(test_fns)),
        "assertion_count": assertion_count,
        "test_patch_lines": test_patch_lines,
        "test_files": test_files,
        "solution_lines_added": sol_lines_added,
        "solution_files_modified": len(sol_files),
        "solution_new_files": sol_new_files,
        "creates_new_files": sol_new_files > 0,
    }


def analyze_all_tasks(lang_filter=None, single_task=None):
    """Analyze all tasks and return results."""
    tasks = []
    
    if single_task:
        task_dir = TASKS_DIR / single_task
        if task_dir.exists():
            tasks.append(parse_task(task_dir))
    else:
        for task_dir in sorted(TASKS_DIR.iterdir()):
            if not task_dir.is_dir() or task_dir.name == "README.md":
                continue
            result = parse_task(task_dir)
            if lang_filter and result["language"] != lang_filter:
                continue
            tasks.append(result)
    
    return tasks


def generate_report(tasks):
    """Generate a markdown report."""
    lines = []
    lines.append("# DeepSWE Benchmark Analysis Report")
    lines.append(f"Generated: {datetime.now().isoformat()}")
    lines.append(f"Total tasks analyzed: {len(tasks)}")
    lines.append("")
    
    # Summary stats
    lines.append("## Summary Statistics")
    lines.append("")
    lines.append("| Metric | Min | Median | Mean | Max |")
    lines.append("|--------|-----|--------|------|-----|")
    
    metrics = [
        ("Instruction words", "instruction_words"),
        ("Instruction sentences", "instruction_sentences"),
        ("Requirements extracted", "requirement_count"),
        ("High-priority requirements", "high_priority_count"),
        ("Test functions", "test_function_count"),
        ("Assertions", "assertion_count"),
        ("Solution lines added", "solution_lines_added"),
        ("Files modified", "solution_files_modified"),
    ]
    
    for name, key in metrics:
        values = sorted([t[key] for t in tasks if t[key] is not None])
        if not values:
            continue
        n = len(values)
        median = values[n // 2]
        mean = int(sum(values) / n)
        lines.append(f"| {name} | {values[0]} | {median} | {mean} | {values[-1]} |")
    
    lines.append("")
    
    # Language distribution
    lines.append("## Language Distribution")
    lines.append("")
    lang_counts = {}
    for t in tasks:
        lang = t["language"] or "unknown"
        lang_counts[lang] = lang_counts.get(lang, 0) + 1
    for lang, count in sorted(lang_counts.items(), key=lambda x: -x[1]):
        lines.append(f"- {lang}: {count}")
    
    lines.append("")
    
    # New file creation
    new_file_tasks = [t for t in tasks if t["creates_new_files"]]
    lines.append(f"## New File Creation")
    lines.append(f"- {len(new_file_tasks)}/{len(tasks)} tasks create new files ({100*len(new_file_tasks)//len(tasks) if tasks else 0}%)")
    lines.append(f"- Total new files across all tasks: {sum(t['solution_new_files'] for t in tasks)}")
    lines.append("")
    
    # Per-task details
    lines.append("## Per-Task Details")
    lines.append("")
    lines.append("| Task | Lang | Reqs | Tests | Asserts | Sol Lines | Files | New Files |")
    lines.append("|------|------|------|-------|---------|-----------|-------|-----------|")
    
    for t in sorted(tasks, key=lambda x: -x["assertion_count"]):
        lines.append(
            f"| {t['task_id'][:30]} | {t['language']} | {t['requirement_count']} | "
            f"{t['test_function_count']} | {t['assertion_count']} | "
            f"{t['solution_lines_added']} | {t['solution_files_modified']} | "
            f"{t['solution_new_files']} |"
        )
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="DeepSWE Benchmark Runner for DeepCraft")
    parser.add_argument("--task", help="Analyze a single task")
    parser.add_argument("--lang", help="Filter by language (typescript, python, go, rust, javascript)")
    parser.add_argument("--report", action="store_true", help="Generate markdown report")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of text")
    args = parser.parse_args()
    
    tasks = analyze_all_tasks(lang_filter=args.lang, single_task=args.task)
    
    if args.json:
        print(json.dumps(tasks, indent=2))
    elif args.report:
        report = generate_report(tasks)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        report_path = OUTPUT_DIR / f"benchmark_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_path.write_text(report)
        print(f"Report written to: {report_path}")
        print(f"\n{report}")
    else:
        print(f"Analyzed {len(tasks)} tasks")
        print(f"\n{'Task':<40} {'Lang':<5} {'Reqs':>5} {'Tests':>6} {'Asserts':>8} {'Sol Lines':>10} {'Files':>6} {'New':>4}")
        print("-" * 90)
        for t in sorted(tasks, key=lambda x: -x["assertion_count"]):
            print(
                f"{t['task_id'][:38]:<40} {t['language']:<5} {t['requirement_count']:>5} "
                f"{t['test_function_count']:>6} {t['assertion_count']:>8} "
                f"{t['solution_lines_added']:>10} {t['solution_files_modified']:>6} "
                f"{t['solution_new_files']:>4}"
            )


if __name__ == "__main__":
    main()
