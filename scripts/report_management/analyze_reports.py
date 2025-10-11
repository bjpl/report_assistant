#!/usr/bin/env python3
"""
Report Analysis Utility
Provides flexible analysis of daily reports across projects
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Set
from collections import defaultdict
import argparse

sys.path.insert(0, str(Path(__file__).parent))
from config import (
    BASE_DIR,
    get_all_projects_with_daily_reports,
    get_daily_reports_path
)


class ReportAnalyzer:
    """Analyzer for project reports"""

    def __init__(self):
        self.projects = get_all_projects_with_daily_reports()

    def get_report_content(self, project: str, date: str) -> Optional[str]:
        """Get content of a specific report"""
        reports_path = get_daily_reports_path(project)
        report_file = reports_path / f"{date}.md"

        if report_file.exists():
            return report_file.read_text()
        return None

    def get_all_reports(self, project: str) -> List[Dict]:
        """Get all reports for a project"""
        reports_path = get_daily_reports_path(project)

        if not reports_path.exists():
            return []

        reports = []
        for report_file in sorted(reports_path.glob("*.md")):
            try:
                date = report_file.stem
                datetime.strptime(date, "%Y-%m-%d")
                reports.append({
                    "date": date,
                    "path": report_file,
                    "content": report_file.read_text()
                })
            except (ValueError, IOError):
                continue

        return reports

    def get_date_range_reports(self, project: str, start_date: str, end_date: str) -> List[Dict]:
        """Get reports within a date range"""
        all_reports = self.get_all_reports(project)

        return [
            r for r in all_reports
            if start_date <= r["date"] <= end_date
        ]

    def search_reports(self, project: str, query: str, case_sensitive: bool = False) -> List[Dict]:
        """Search for text in reports"""
        all_reports = self.get_all_reports(project)

        if not case_sensitive:
            query = query.lower()

        matches = []
        for report in all_reports:
            content = report["content"]
            if not case_sensitive:
                content = content.lower()

            if query in content:
                # Extract matching lines with context
                lines = report["content"].split("\n")
                matching_lines = []
                for i, line in enumerate(lines):
                    check_line = line if case_sensitive else line.lower()
                    if query in check_line:
                        # Add context (line before and after)
                        context_start = max(0, i - 1)
                        context_end = min(len(lines), i + 2)
                        matching_lines.append({
                            "line_number": i + 1,
                            "line": line,
                            "context": lines[context_start:context_end]
                        })

                matches.append({
                    "date": report["date"],
                    "path": report["path"],
                    "matches": matching_lines
                })

        return matches

    def get_commit_statistics(self, project: str, days: int = 30) -> Dict:
        """Get commit statistics for recent days"""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        reports = self.get_date_range_reports(project, start_date, end_date)

        total_commits = 0
        total_files = 0
        commit_messages = []

        for report in reports:
            content = report["content"]
            # Count commits (lines starting with "- **")
            commits = re.findall(r'^- \*\*[a-f0-9]{8}\*\* (.+)$', content, re.MULTILINE)
            total_commits += len(commits)
            commit_messages.extend(commits)

            # Count files in "Files Changed" section
            files_section = re.search(r'## Files Changed\n(.+?)(?=\n##|\Z)', content, re.DOTALL)
            if files_section:
                files = re.findall(r'^- (.+)$', files_section.group(1), re.MULTILINE)
                total_files += len(files)

        return {
            "project": project,
            "period": f"{start_date} to {end_date}",
            "days_with_reports": len(reports),
            "total_commits": total_commits,
            "total_files_changed": total_files,
            "avg_commits_per_day": total_commits / max(len(reports), 1),
            "recent_commit_messages": commit_messages[-10:]  # Last 10
        }

    def cross_project_analysis(self, days: int = 30) -> Dict:
        """Analyze activity across all projects"""
        stats_by_project = {}

        for project in self.projects:
            stats = self.get_commit_statistics(project, days)
            if stats["total_commits"] > 0:
                stats_by_project[project] = stats

        # Calculate totals
        total_commits = sum(s["total_commits"] for s in stats_by_project.values())
        total_files = sum(s["total_files_changed"] for s in stats_by_project.values())
        total_days = sum(s["days_with_reports"] for s in stats_by_project.values())

        # Most active projects
        most_active = sorted(
            stats_by_project.items(),
            key=lambda x: x[1]["total_commits"],
            reverse=True
        )

        return {
            "period_days": days,
            "active_projects": len(stats_by_project),
            "total_projects": len(self.projects),
            "total_commits": total_commits,
            "total_files_changed": total_files,
            "total_active_days": total_days,
            "most_active_projects": [p[0] for p in most_active[:5]],
            "project_stats": stats_by_project
        }


def print_search_results(results: List[Dict], query: str):
    """Print search results"""
    print(f"\n{'=' * 80}")
    print(f"SEARCH RESULTS FOR: '{query}'")
    print(f"{'=' * 80}\n")

    if not results:
        print("No matches found.\n")
        return

    print(f"Found {len(results)} report(s) with matches:\n")

    for result in results:
        print(f"📅 {result['date']}")
        print(f"   {result['path']}")
        for match in result["matches"]:
            print(f"\n   Line {match['line_number']}: {match['line']}")
        print()


def print_project_stats(stats: Dict):
    """Print project statistics"""
    print(f"\n{'=' * 80}")
    print(f"PROJECT STATISTICS: {stats['project']}")
    print(f"{'=' * 80}\n")

    print(f"Period: {stats['period']}")
    print(f"Days with Reports: {stats['days_with_reports']}")
    print(f"Total Commits: {stats['total_commits']}")
    print(f"Total Files Changed: {stats['total_files_changed']}")
    print(f"Average Commits/Day: {stats['avg_commits_per_day']:.1f}")

    if stats["recent_commit_messages"]:
        print(f"\nRecent Commit Messages:")
        for msg in stats["recent_commit_messages"]:
            print(f"  - {msg}")
    print()


def print_cross_project_stats(analysis: Dict):
    """Print cross-project analysis"""
    print(f"\n{'=' * 80}")
    print(f"CROSS-PROJECT ANALYSIS ({analysis['period_days']} days)")
    print(f"{'=' * 80}\n")

    print(f"Active Projects: {analysis['active_projects']}/{analysis['total_projects']}")
    print(f"Total Commits: {analysis['total_commits']}")
    print(f"Total Files Changed: {analysis['total_files_changed']}")
    print(f"Total Active Days: {analysis['total_active_days']}")

    print(f"\nMost Active Projects:")
    for i, project in enumerate(analysis["most_active_projects"], 1):
        stats = analysis["project_stats"][project]
        print(f"  {i}. {project}: {stats['total_commits']} commits, {stats['days_with_reports']} days")

    print()


def main():
    parser = argparse.ArgumentParser(
        description="Analyze daily reports with flexible queries"
    )

    subparsers = parser.add_subparsers(dest="command", help="Analysis commands")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search for text in reports")
    search_parser.add_argument("query", help="Text to search for")
    search_parser.add_argument("--project", "-p", help="Search in specific project only")
    search_parser.add_argument("--case-sensitive", action="store_true", help="Case-sensitive search")

    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Get project statistics")
    stats_parser.add_argument("--project", "-p", help="Get stats for specific project")
    stats_parser.add_argument("--days", "-d", type=int, default=30, help="Number of days to analyze")

    # Cross-project command
    cross_parser = subparsers.add_parser("cross", help="Cross-project analysis")
    cross_parser.add_argument("--days", "-d", type=int, default=30, help="Number of days to analyze")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    analyzer = ReportAnalyzer()

    if args.command == "search":
        if args.project:
            results = analyzer.search_reports(args.project, args.query, args.case_sensitive)
        else:
            # Search all projects
            results = []
            for project in analyzer.projects:
                project_results = analyzer.search_reports(project, args.query, args.case_sensitive)
                if project_results:
                    results.extend([{**r, "project": project} for r in project_results])

        print_search_results(results, args.query)

    elif args.command == "stats":
        if args.project:
            stats = analyzer.get_commit_statistics(args.project, args.days)
            print_project_stats(stats)
        else:
            # Stats for all projects
            for project in sorted(analyzer.projects):
                stats = analyzer.get_commit_statistics(project, args.days)
                if stats["total_commits"] > 0:
                    print_project_stats(stats)

    elif args.command == "cross":
        analysis = analyzer.cross_project_analysis(args.days)
        print_cross_project_stats(analysis)


if __name__ == "__main__":
    main()
