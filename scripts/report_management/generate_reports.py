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
    # Check if directory exists
    if not project_path.exists():
        return []

    try:
        # Try to get commits - works whether .git is local or in parent directory
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
    # Check if directory exists
    if not project_path.exists():
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


def generate_work_completed_section(commits: List[Dict], files_changed: List[str]) -> str:
    """Generate Work Completed section from commits"""
    if not commits:
        return "<!-- No commits found for this date -->"

    work_items = []
    for i, commit in enumerate(commits[:5], 1):  # Limit to first 5 commits
        work_item = f"""### {i}. {commit['message']}

**Status**: Completed
**Commit**: `{commit['hash'][:8]}`
**Author**: {commit['author']}

**Changes Made**:
- {commit['message']}

<!-- Add additional details about this work item manually -->
"""
        work_items.append(work_item)

    if len(commits) > 5:
        work_items.append(f"\n<!-- {len(commits) - 5} additional commits not shown in detail -->")

    return "\n---\n\n".join(work_items)


def generate_documentation_updates(files_changed: List[str]) -> str:
    """Detect documentation file changes"""
    doc_files = [f for f in files_changed if any(ext in f.lower() for ext in ['.md', 'readme', 'docs/'])]

    if not doc_files:
        return "<!-- No documentation files were modified -->"

    updates = []
    for doc_file in doc_files[:10]:  # Limit to first 10
        updates.append(f"- [x] `{doc_file}` - Updated")

    if len(doc_files) > 10:
        updates.append(f"\n<!-- {len(doc_files) - 10} additional documentation files updated -->")

    return "\n".join(updates)


def generate_report_content(project: str, date: str) -> str:
    """Generate report content for a specific date using comprehensive template"""
    project_path = BASE_DIR / project if "/" not in project else BASE_DIR / project

    commits = get_commits_for_date(project_path, date)
    files_changed = get_files_changed_for_date(project_path, date)

    # Generate auto-filled sections
    work_completed = generate_work_completed_section(commits, files_changed)
    doc_updates = generate_documentation_updates(files_changed)

    # Format files changed list
    files_list = ""
    if files_changed:
        for file in files_changed[:30]:  # Show more files in comprehensive template
            files_list += f"- `{file}`\n"
        if len(files_changed) > 30:
            files_list += f"\n<!-- {len(files_changed) - 30} additional files changed -->\n"
    else:
        files_list = "<!-- No files changed -->"

    # Generate executive summary
    exec_summary = f"Completed {len(commits)} commit(s) affecting {len(files_changed)} file(s) in {project}."
    if commits:
        exec_summary += f" Primary focus: {commits[0]['message']}"

    # Use comprehensive template with auto-filled sections
    content = DAILY_REPORT_TEMPLATE

    # Replace template placeholders with actual data
    content = content.replace("[Project Name]", project)
    content = content.replace("[YYYY-MM-DD]", date)
    content = content.replace("[HH:MM]", "[Auto-generated - fill in manually]")
    content = content.replace("[Brief 1-line description of main work]",
                            commits[0]['message'] if commits else "[Fill in manually]")
    content = content.replace("[Write your executive summary here]", exec_summary)

    # Add auto-generated work completed section
    # Find and replace the work completed section
    work_section_start = content.find("## Work Completed")
    work_section_end = content.find("## Technical Decisions")
    if work_section_start != -1 and work_section_end != -1:
        content = (content[:work_section_start] +
                  f"## Work Completed\n\n{work_completed}\n\n" +
                  content[work_section_end:])

    # Add auto-generated documentation updates
    doc_section_start = content.find("## Documentation Updates")
    doc_section_end = content.find("## Next Session Planning")
    if doc_section_start != -1 and doc_section_end != -1:
        content = (content[:doc_section_start] +
                  f"## Documentation Updates\n\n{doc_updates}\n\n---\n\n" +
                  content[doc_section_end:])

    # Add files changed as appendix
    content += f"\n\n---\n\n## Auto-Generated Appendix\n\n### All Files Changed ({len(files_changed)} files)\n\n{files_list}\n"

    # Add commit details
    commits_detail = ""
    for commit in commits:
        commits_detail += f"- **{commit['hash'][:8]}** {commit['message']}\n"
        commits_detail += f"  *{commit['author']} ({commit['email']}) - {commit['date']}*\n\n"

    content += f"\n### All Commits ({len(commits)} commits)\n\n{commits_detail}\n"
    content += f"---\n\n**Auto-Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"

    return content


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
    parser.add_argument(
        "--missing",
        action="store_true",
        help="Generate reports only for dates with commits but missing reports (default behavior)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Generate reports for all dates with commits"
    )
    parser.add_argument(
        "--backfill",
        action="store_true",
        help="Backfill all missing reports (same as --missing, for backwards compatibility)"
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
        # Default behavior: generate missing reports
        # --missing, --backfill, and --all flags are all supported but do the same thing
        results = generate_all_missing_reports(args.overwrite)
        print_generation_results(results)


if __name__ == "__main__":
    main()
