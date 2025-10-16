#!/usr/bin/env python3
"""Check which projects had commits yesterday and need reports"""

import os
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

workspace = Path("C:/Users/brand/Development/Project_Workspace/active-development")
yesterday = "2025-10-11"

# All projects with daily_reports folders
projects = [
    "agentic_learning",
    "ai_stack_analysis",
    "algorithms_and_data_structures",
    "aves",
    "brandonjplambert",
    "california_puzzle_game",
    "colombia_puzzle_game",
    "corporate_intel",
    "deployment_sprint",
    "describe_it",
    "fancy_monkey",
    "hablas",
    "health_agent",
    "learning_voice_agent",
    "letratos",
    "llms_on_my_system",
    "online_language_learning_resources",
    "open_learn",
    "report_assistant",
    "thematic_outline_gen",
    "video_gen",
    "language-learning/hablas",
    "language-learning/subjunctive_practice",
    "internet/docs",
    "colombia_puzzle_game/deployment_sprint",
    "brandonjplambert/_site",
    "letratos/_site"
]

results = []

for project in projects:
    project_path = workspace / project
    if not (project_path / ".git").exists():
        continue

    try:
        # Check for commits on yesterday
        cmd = [
            "git", "-C", str(project_path), "log",
            f"--since={yesterday} 00:00",
            f"--until={yesterday} 23:59",
            "--oneline"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)

        if result.returncode == 0:
            commits = result.stdout.strip().split('\n') if result.stdout.strip() else []
            commit_count = len(commits)

            if commit_count > 0:
                # Check if report exists
                daily_reports_dir = project_path / "daily_reports"
                report_file = daily_reports_dir / f"{yesterday}.md"
                has_report = report_file.exists()

                results.append({
                    'project': project,
                    'commits': commit_count,
                    'has_report': has_report,
                    'report_path': str(report_file)
                })

    except Exception as e:
        print(f"Error checking {project}: {e}")

# Print results
print(f"\n{'='*80}")
print(f"Projects with commits on {yesterday}")
print(f"{'='*80}\n")

for r in results:
    status = "✓ HAS REPORT" if r['has_report'] else "✗ MISSING REPORT"
    print(f"{r['project']:50} {r['commits']:2} commits  {status}")

print(f"\n{'='*80}")
print(f"Summary: {len(results)} projects with commits, {sum(1 for r in results if not r['has_report'])} missing reports")
print(f"{'='*80}\n")

# Output projects needing reports
needs_reports = [r for r in results if not r['has_report']]
if needs_reports:
    print("\nProjects needing reports:")
    for r in needs_reports:
        print(f"  - {r['project']}")
