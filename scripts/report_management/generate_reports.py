#!/usr/bin/env python3
"""
Report Generation Utility
Automatically generates daily reports for dates with git commits
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set
import argparse

sys.path.insert(0, str(Path(__file__).parent))
from config import (
    BASE_DIR,
    get_all_projects_with_daily_reports,
    get_daily_reports_path,
    DAILY_REPORT_TEMPLATE
)


def get_commits_for_date(project_path: Path, date: str) -> List[Dict]:
    """Get all commits for a specific date"""
    if not (project_path / ".git").exists():
        return []

    try:
        # Get commits for the date
        result = subprocess.run(
            [
                "git", "log",
                "--all",
                f"--since={date} 00:00:00",
                f"--until={date} 23:59:59",
                "--format=%H|||%s|||%an|||%ae|||%cd",
                "--date=iso"
            ],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True
        )

        commits = []
        for line in result.stdout.strip().split("\n"):
            if line:
                parts = line.split("|||")
                if len(parts) >= 5:
                    commits.append({
                        "hash": parts[0],
                        "message": parts[1],
                        "author": parts[2],
                        "email": parts[3],
                        "date": parts[4]
                    })

        return commits
    except subprocess.CalledProcessError:
        return []


def get_files_changed_for_date(project_path: Path, date: str) -> List[str]:
    """Get list of files changed on a specific date"""
    if not (project_path / ".git").exists():
        return []

    try:
        result = subprocess.run(
            [
                "git", "log",
                "--all",
                f"--since={date} 00:00:00",
                f"--until={date} 23:59:59",
                "--name-only",
                "--format="
            ],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True
        )

        files = [f for f in result.stdout.strip().split("\n") if f]
        return sorted(set(files))
    except subprocess.CalledProcessError:
        return []


def generate_report_content(project: str, date: str) -> str:
    """Generate report content for a specific date"""
    project_path = BASE_DIR / project if "/" not in project else BASE_DIR / project

    commits = get_commits_for_date(project_path, date)
    files_changed = get_files_changed_for_date(project_path, date)

    # Format commits
    commits_text = ""
    if commits:
        for commit in commits:
            commits_text += f"- **{commit['hash'][:8]}** {commit['message']}\n"
            commits_text += f"  *{commit['author']} - {commit['date']}*\n\n"
    else:
        commits_text = "No commits on this date.\n"

    # Format files
    files_text = ""
    if files_changed:
        for file in files_changed[:20]:  # Limit to first 20 files
            files_text += f"- {file}\n"
        if len(files_changed) > 20:
            files_text += f"\n... and {len(files_changed) - 20} more files\n"
    else:
        files_text = "No files changed.\n"

    # Generate summary
    summary = f"Made {len(commits)} commit(s) affecting {len(files_changed)} file(s)."

    return DAILY_REPORT_TEMPLATE.format(
        date=date,
        project_name=project,
        commits=commits_text.strip(),
        files_changed=files_text.strip(),
        summary=summary,
        next_steps="[To be filled in]"
    )


def generate_report_for_date(project: str, date: str, overwrite: bool = False) -> bool:
    """Generate a report for a specific date"""
    reports_path = get_daily_reports_path(project)
    reports_path.mkdir(parents=True, exist_ok=True)

    report_file = reports_path / f"{date}.md"

    if report_file.exists() and not overwrite:
        print(f"   Report already exists for {date} (use --overwrite to replace)")
        return False

    content = generate_report_content(project, date)

    try:
        report_file.write_text(content)
        print(f"   ✅ Generated report for {date}")
        return True
    except Exception as e:
        print(f"   ❌ Error generating report for {date}: {e}")
        return False


def generate_missing_reports(project: str, overwrite: bool = False) -> Dict:
    """Generate reports for all dates with commits but no reports"""
    from validate_reports import validate_project_reports

    validation = validate_project_reports(project)

    if validation["status"] == "error":
        return {
            "project": project,
            "status": "error",
            "message": validation["message"]
        }

    missing_dates = validation["missing_report_dates"]

    if not missing_dates:
        return {
            "project": project,
            "status": "complete",
            "generated": 0,
            "message": "All reports up to date"
        }

    print(f"\n📝 Generating {len(missing_dates)} missing reports for {project}...")

    generated = 0
    for date in missing_dates:
        if generate_report_for_date(project, date, overwrite):
            generated += 1

    return {
        "project": project,
        "status": "ok",
        "generated": generated,
        "total_missing": len(missing_dates)
    }


def generate_all_missing_reports(overwrite: bool = False) -> List[Dict]:
    """Generate missing reports for all projects"""
    projects = get_all_projects_with_daily_reports()
    results = []

    for project in sorted(projects):
        result = generate_missing_reports(project, overwrite)
        results.append(result)

    return results


def print_generation_results(results: List[Dict]):
    """Print generation results"""
    print("\n" + "=" * 80)
    print("REPORT GENERATION RESULTS")
    print("=" * 80 + "\n")

    total_generated = sum(r.get("generated", 0) for r in results)

    print(f"Total Reports Generated: {total_generated}\n")
    print("-" * 80 + "\n")

    for result in results:
        if result["status"] == "error":
            print(f"❌ {result['project']}: {result['message']}")
        elif result["status"] == "complete":
            print(f"✅ {result['project']}: {result['message']}")
        else:
            print(f"📝 {result['project']}: Generated {result['generated']}/{result['total_missing']} reports")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Generate daily reports for dates with git commits"
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing reports"
    )
    parser.add_argument(
        "--project", "-p",
        help="Generate reports for specific project only"
    )
    parser.add_argument(
        "--date", "-d",
        help="Generate report for specific date (YYYY-MM-DD)"
    )

    args = parser.parse_args()

    if args.date:
        # Validate date format
        try:
            datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            print("Error: Date must be in YYYY-MM-DD format")
            return

        if not args.project:
            print("Error: --project required when using --date")
            return

        generate_report_for_date(args.project, args.date, args.overwrite)
    elif args.project:
        results = [generate_missing_reports(args.project, args.overwrite)]
        print_generation_results(results)
    else:
        results = generate_all_missing_reports(args.overwrite)
        print_generation_results(results)


if __name__ == "__main__":
    main()
