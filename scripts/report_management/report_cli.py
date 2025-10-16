#!/usr/bin/env python3
"""
Report CLI - Consolidated Python command-line tool for report management
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# Import existing modules
from audit_reports import audit_project, audit_all_projects
from generate_reports import generate_daily_report, generate_reports_from_commits
from sync_reports import sync_reports_across_projects
from update_format import update_report_format
from validate_reports import validate_report_structure

class ReportCLI:
    """Unified CLI for report management operations"""

    def __init__(self):
        self.project_root = Path("/mnt/c/Users/brand/Development/Project_Workspace/active-development")
        self.report_assistant = self.project_root / "report_assistant"
        self.today = datetime.now().strftime("%Y-%m-%d")

    def setup_parser(self) -> argparse.ArgumentParser:
        """Setup argument parser with all commands"""
        parser = argparse.ArgumentParser(
            description="Report Assistant CLI - Unified report management",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  report-cli today                    # Generate today's reports
  report-cli audit --project video_gen # Audit specific project
  report-cli generate --all            # Generate all missing reports
  report-cli stats                     # Show statistics
            """
        )

        subparsers = parser.add_subparsers(dest='command', help='Commands')

        # Today command
        today_parser = subparsers.add_parser('today', help='Generate today\'s reports')
        today_parser.add_argument('--force', action='store_true', help='Overwrite existing')

        # GMS command
        gms_parser = subparsers.add_parser('gms', help='Generate GMS startup report')
        gms_parser.add_argument('--date', default=self.today, help='Report date')
        gms_parser.add_argument('--auto-fill', action='store_true', help='Auto-fill with swarm')

        # Progress command
        progress_parser = subparsers.add_parser('progress', help='Generate progress report')
        progress_parser.add_argument('--date', default=self.today, help='Report date')

        # Audit command
        audit_parser = subparsers.add_parser('audit', help='Audit reports')
        audit_parser.add_argument('--project', help='Specific project to audit')
        audit_parser.add_argument('--output', help='Output file for results')

        # Generate command
        gen_parser = subparsers.add_parser('generate', help='Generate reports')
        gen_parser.add_argument('--all', action='store_true', help='Generate all missing')
        gen_parser.add_argument('--project', help='Specific project')
        gen_parser.add_argument('--backfill', action='store_true', help='Backfill from git')
        gen_parser.add_argument('--days', type=int, default=30, help='Days to backfill')

        # Sync command
        sync_parser = subparsers.add_parser('sync', help='Sync reports')
        sync_parser.add_argument('--dry-run', action='store_true', help='Preview changes')
        sync_parser.add_argument('--force', action='store_true', help='Force sync')

        # Validate command
        val_parser = subparsers.add_parser('validate', help='Validate reports')
        val_parser.add_argument('--project', help='Specific project')
        val_parser.add_argument('--fix', action='store_true', help='Auto-fix issues')

        # Stats command
        stats_parser = subparsers.add_parser('stats', help='Show statistics')
        stats_parser.add_argument('--json', action='store_true', help='JSON output')
        stats_parser.add_argument('--detailed', action='store_true', help='Detailed stats')

        # Init command
        init_parser = subparsers.add_parser('init', help='Initialize project')
        init_parser.add_argument('project', help='Project name')
        init_parser.add_argument('--templates', action='store_true', help='Copy templates')

        # Backup command
        backup_parser = subparsers.add_parser('backup', help='Backup reports')
        backup_parser.add_argument('--compress', action='store_true', help='Compress backup')

        # Clean command
        clean_parser = subparsers.add_parser('clean', help='Clean temp files')
        clean_parser.add_argument('--deep', action='store_true', help='Deep clean')

        # Swarm command
        swarm_parser = subparsers.add_parser('swarm', help='Swarm operations')
        swarm_parser.add_argument('action', choices=['audit', 'align', 'deploy'])
        swarm_parser.add_argument('--agents', type=int, default=5, help='Number of agents')

        return parser

    def cmd_today(self, args):
        """Generate today's reports"""
        print(f"📊 Generating reports for {self.today}...")

        # Generate GMS
        gms_path = self.report_assistant / "daily_dev_startup_reports" / f"{self.today}_startup_report.md"
        if gms_path.exists() and not args.force:
            print("⚠️  GMS report already exists (use --force to overwrite)")
        else:
            self._copy_template("gms_startup_report", gms_path)
            print(f"✅ GMS report created: {gms_path}")

        # Generate Progress
        progress_path = self.report_assistant / "daily_reports" / f"{self.today}.md"
        if progress_path.exists() and not args.force:
            print("⚠️  Progress report already exists (use --force to overwrite)")
        else:
            self._copy_template("daily_report", progress_path)
            print(f"✅ Progress report created: {progress_path}")

    def cmd_audit(self, args):
        """Audit reports"""
        if args.project:
            print(f"🔍 Auditing project: {args.project}")
            results = audit_project(self.project_root / args.project)
        else:
            print("🔍 Auditing all projects...")
            results = audit_all_projects(self.project_root)

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"✅ Results saved to {args.output}")
        else:
            self._display_audit_results(results)

    def cmd_stats(self, args):
        """Show statistics"""
        stats = self._collect_statistics()

        if args.json:
            print(json.dumps(stats, indent=2))
        else:
            self._display_statistics(stats, detailed=args.detailed)

    def cmd_init(self, args):
        """Initialize project"""
        project_dir = self.project_root / args.project

        print(f"🎯 Initializing project: {args.project}")

        # Create directories
        (project_dir / "daily_reports").mkdir(parents=True, exist_ok=True)
        (project_dir / "daily_dev_startup_reports").mkdir(parents=True, exist_ok=True)

        if args.templates:
            templates_dir = project_dir / "docs" / "templates"
            templates_dir.mkdir(parents=True, exist_ok=True)

            # Copy templates
            for template in ["daily_report", "gms_startup_report", "strategic_audit"]:
                src = self.report_assistant / "docs" / "templates" / f"{template}_template.md"
                dst = templates_dir / f"{template}_template.md"
                if src.exists():
                    dst.write_text(src.read_text())

        print(f"✅ Project {args.project} initialized")

    def cmd_swarm(self, args):
        """Swarm operations"""
        print(f"🤖 Executing swarm {args.action}...")

        commands = {
            'audit': [
                "npx", "claude-flow@alpha", "swarm", "deploy", "audit-all",
                "Comprehensive report audit across all projects"
            ],
            'align': [
                "npx", "claude-flow@alpha", "swarm", "deploy", "align-reports",
                "Align all reports to standard format"
            ],
            'deploy': [
                "npx", "claude-flow@alpha", "swarm", "init", "mesh",
                "--max-agents", str(args.agents)
            ]
        }

        try:
            subprocess.run(commands[args.action], check=True)
            print(f"✅ Swarm {args.action} complete")
        except subprocess.CalledProcessError as e:
            print(f"❌ Swarm operation failed: {e}")
            sys.exit(1)

    def _copy_template(self, template_name: str, destination: Path):
        """Copy template to destination"""
        template_path = self.report_assistant / "docs" / "templates" / f"{template_name}_template.md"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(template_path.read_text())

    def _collect_statistics(self) -> Dict:
        """Collect report statistics"""
        stats = {
            'total_projects': 0,
            'total_daily_reports': 0,
            'total_gms_reports': 0,
            'projects_with_reports': [],
            'recent_activity': [],
            'compliance': {
                'fully_compliant': 0,
                'partial': 0,
                'non_compliant': 0
            }
        }

        for project_dir in self.project_root.iterdir():
            if not project_dir.is_dir():
                continue

            stats['total_projects'] += 1

            daily_reports = list((project_dir / "daily_reports").glob("*.md")) if (project_dir / "daily_reports").exists() else []
            gms_reports = list((project_dir / "daily_dev_startup_reports").glob("*.md")) if (project_dir / "daily_dev_startup_reports").exists() else []

            if daily_reports or gms_reports:
                stats['projects_with_reports'].append({
                    'name': project_dir.name,
                    'daily_count': len(daily_reports),
                    'gms_count': len(gms_reports)
                })

                stats['total_daily_reports'] += len(daily_reports)
                stats['total_gms_reports'] += len(gms_reports)

                # Determine compliance
                if daily_reports and gms_reports:
                    stats['compliance']['fully_compliant'] += 1
                elif daily_reports or gms_reports:
                    stats['compliance']['partial'] += 1
                else:
                    stats['compliance']['non_compliant'] += 1

            # Recent activity
            for report in daily_reports[-5:]:
                stats['recent_activity'].append({
                    'project': project_dir.name,
                    'file': report.name,
                    'modified': report.stat().st_mtime
                })

        return stats

    def _display_statistics(self, stats: Dict, detailed: bool = False):
        """Display statistics in readable format"""
        print("\n📊 Report Statistics")
        print("=" * 50)
        print(f"Total Projects:        {stats['total_projects']}")
        print(f"Daily Reports:         {stats['total_daily_reports']}")
        print(f"GMS Reports:           {stats['total_gms_reports']}")
        print(f"Fully Compliant:       {stats['compliance']['fully_compliant']}")
        print(f"Partially Compliant:   {stats['compliance']['partial']}")
        print(f"Non-Compliant:         {stats['compliance']['non_compliant']}")

        if detailed:
            print("\n📁 Projects with Reports:")
            for project in sorted(stats['projects_with_reports'], key=lambda x: x['daily_count'] + x['gms_count'], reverse=True):
                print(f"  {project['name']:30} Daily: {project['daily_count']:3}  GMS: {project['gms_count']:3}")

            print("\n🕐 Recent Activity:")
            for activity in sorted(stats['recent_activity'], key=lambda x: x['modified'], reverse=True)[:10]:
                print(f"  {activity['project']}: {activity['file']}")

    def _display_audit_results(self, results: Dict):
        """Display audit results"""
        print("\n🔍 Audit Results")
        print("=" * 50)
        for project, data in results.items():
            status = "✅" if data.get('compliant') else "❌"
            print(f"{status} {project}")
            if data.get('issues'):
                for issue in data['issues']:
                    print(f"    ⚠️  {issue}")

    def run(self):
        """Main entry point"""
        parser = self.setup_parser()
        args = parser.parse_args()

        if not args.command:
            parser.print_help()
            return

        # Route to appropriate command
        command_map = {
            'today': self.cmd_today,
            'gms': lambda a: self._generate_report('gms', a),
            'progress': lambda a: self._generate_report('progress', a),
            'audit': self.cmd_audit,
            'stats': self.cmd_stats,
            'init': self.cmd_init,
            'swarm': self.cmd_swarm,
            # Add other commands as needed
        }

        handler = command_map.get(args.command)
        if handler:
            handler(args)
        else:
            print(f"❌ Command not implemented: {args.command}")
            sys.exit(1)

    def _generate_report(self, report_type: str, args):
        """Generic report generation"""
        if report_type == 'gms':
            path = self.report_assistant / "daily_dev_startup_reports" / f"{args.date}_startup_report.md"
            template = "gms_startup_report"
        else:
            path = self.report_assistant / "daily_reports" / f"{args.date}.md"
            template = "daily_report"

        self._copy_template(template, path)
        print(f"✅ {report_type.upper()} report created: {path}")

        if hasattr(args, 'auto_fill') and args.auto_fill:
            print("🤖 Auto-filling with swarm...")
            subprocess.run(["npx", "claude-flow@alpha", "sparc", "run", "gms-audit", f"Fill report for {args.date}"])


if __name__ == "__main__":
    cli = ReportCLI()
    cli.run()