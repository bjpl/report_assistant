#!/usr/bin/env python3
"""
Report Validation Utility
Validates that daily reports align with git commits
Identifies and optionally removes reports without commits
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set, Tuple
import argparse

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from config import BASE_DIR, get_all_projects_with_daily_reports, get_daily_reports_path


def get_git_commit_dates(project_path: Path) -> Set[str]:
    """Get all dates with git commits that touched files in this project"""
    try:
        # Use git log with path filter to only get commits for this project
        # Use --all to check all branches, and "." to filter by current directory
        result = subprocess.run(
            ["git", "log", "--all", "--format=%cs", "--", "."],
            cwd=project_path,
            capture_output=True,
            text=True,
            check=True
        )
        # Convert to set of unique dates in YYYY-MM-DD format
        # Filter out empty strings from the split
        dates = result.stdout.strip().split("\n") if result.stdout.strip() else []
        return set(d for d in dates if d)
    except subprocess.CalledProcessError:
        return set()


def get_report_dates(reports_path: Path) -> List[Tuple[str, Path]]:
    """Get all dates with reports in YYYY-MM-DD format"""
    if not reports_path.exists():
        return []

    report_dates = []
    for report_file in reports_path.glob("*.md"):
        # Extract date from filename (YYYY-MM-DD.md)
        try:
            date_str = report_file.stem  # Removes .md extension
            # Validate date format
            datetime.strptime(date_str, "%Y-%m-%d")
            report_dates.append((date_str, report_file))
        except ValueError:
            # Skip files that don't match date format
            continue

    return report_dates


def validate_project_reports(project: str, delete: bool = False) -> Dict:
    """
    Validate reports for a single project
    Returns dict with validation results
    """
    project_path = BASE_DIR / project if "/" not in project else BASE_DIR / project
    reports_path = get_daily_reports_path(project)

    if not project_path.exists():
        return {
            "project": project,
            "status": "error",
            "message": "Project path not found"
        }

    # Get commit dates and report dates
    commit_dates = get_git_commit_dates(project_path)
    report_dates = get_report_dates(reports_path)

    # Find reports without commits
    reports_without_commits = []
    for date_str, report_path in report_dates:
        if date_str not in commit_dates:
            reports_without_commits.append((date_str, report_path))

    # Find commits without reports
    report_date_strs = {d for d, _ in report_dates}
    commits_without_reports = commit_dates - report_date_strs

    result = {
        "project": project,
        "status": "ok" if not reports_without_commits else "invalid",
        "total_reports": len(report_dates),
        "total_commits": len(commit_dates),
        "reports_without_commits": len(reports_without_commits),
        "commits_without_reports": len(commits_without_reports),
        "invalid_reports": reports_without_commits,
        "missing_report_dates": sorted(list(commits_without_reports))
    }

    # Delete invalid reports if requested
    if delete and reports_without_commits:
        deleted = []
        for date_str, report_path in reports_without_commits:
            try:
                report_path.unlink()
                deleted.append(date_str)
            except Exception as e:
                print(f"Error deleting {report_path}: {e}")
        result["deleted"] = deleted

    return result


def validate_all_projects(delete: bool = False) -> List[Dict]:
    """Validate reports for all projects"""
    projects = get_all_projects_with_daily_reports()
    results = []

    for project in sorted(projects):
        result = validate_project_reports(project, delete)
        results.append(result)

    return results


def print_validation_results(results: List[Dict], verbose: bool = False):
    """Print validation results in readable format"""
    print("\n" + "=" * 80)
    print("DAILY REPORTS VALIDATION RESULTS")
    print("=" * 80 + "\n")

    total_projects = len(results)
    invalid_projects = sum(1 for r in results if r["status"] == "invalid")
    total_invalid_reports = sum(r.get("reports_without_commits", 0) for r in results)
    total_missing_reports = sum(r.get("commits_without_reports", 0) for r in results)

    print(f"Total Projects: {total_projects}")
    print(f"Projects with Invalid Reports: {invalid_projects}")
    print(f"Total Invalid Reports (no commits): {total_invalid_reports}")
    print(f"Total Missing Reports (commits without reports): {total_missing_reports}")
    print("\n" + "-" * 80 + "\n")

    for result in results:
        if result["status"] == "error":
            print(f"❌ {result['project']}: {result['message']}")
            continue

        status_icon = "✅" if result["status"] == "ok" else "⚠️"
        print(f"{status_icon} {result['project']}")
        print(f"   Reports: {result['total_reports']} | Commits: {result['total_commits']}")

        if result["reports_without_commits"] > 0:
            print(f"   Invalid Reports (no commits): {result['reports_without_commits']}")
            if verbose:
                for date_str, _ in result["invalid_reports"]:
                    print(f"      - {date_str}")

        if result["commits_without_reports"] > 0:
            print(f"   Missing Reports: {result['commits_without_reports']}")
            if verbose and len(result["missing_report_dates"]) <= 10:
                for date_str in result["missing_report_dates"][:10]:
                    print(f"      - {date_str}")
                if len(result["missing_report_dates"]) > 10:
                    print(f"      ... and {len(result['missing_report_dates']) - 10} more")

        if result.get("deleted"):
            print(f"   🗑️  Deleted: {len(result['deleted'])} invalid reports")

        print()


def main():
    parser = argparse.ArgumentParser(
        description="Validate daily reports against git commits"
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Delete reports without corresponding git commits"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed information about invalid reports"
    )
    parser.add_argument(
        "--project", "-p",
        help="Validate specific project only"
    )

    args = parser.parse_args()

    if args.delete:
        confirm = input(
            "⚠️  This will DELETE reports without git commits. Continue? (yes/no): "
        )
        if confirm.lower() != "yes":
            print("Aborted.")
            return

    if args.project:
        results = [validate_project_reports(args.project, args.delete)]
    else:
        results = validate_all_projects(args.delete)

    print_validation_results(results, args.verbose)


if __name__ == "__main__":
    main()
