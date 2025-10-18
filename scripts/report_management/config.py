#!/usr/bin/env python3
"""
Report Management Configuration
Defines paths and settings for daily reports system
"""

import os
from pathlib import Path
from typing import List, Dict

# Base directory for all projects
# Use parent directory of report_assistant (go up 2 levels from scripts/report_management)
BASE_DIR = Path(__file__).parent.parent.parent.parent

# Template file path
REPORT_ASSISTANT_DIR = Path(__file__).parent.parent.parent
TEMPLATE_FILE = REPORT_ASSISTANT_DIR / "docs" / "templates" / "daily_report_template.md"

# Projects with daily_reports folders
DAILY_REPORTS_PROJECTS = [
    "agentic_learning",
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
    "letratos",
    "online_language_learning_resources",
    "open_learn",
    "video_gen",
]

# Projects with daily_dev_startup_reports folders
STARTUP_REPORTS_PROJECTS = [
    "algorithms_and_data_structures",
    "aves",
    "california_puzzle_game",
    "colombia_puzzle_game",
    "corporate_intel",
    "describe_it",
    "fancy_monkey",
    "hablas",
    "letratos",
    "video_gen",
]

# Nested projects (e.g., subjunctive_practice inside language-learning)
NESTED_PROJECTS = {
    "language-learning/subjunctive_practice": {
        "daily_reports": True,
        "daily_dev_startup_reports": True,
    }
}

# Load comprehensive template from file
def get_daily_report_template() -> str:
    """Load the comprehensive daily report template"""
    if TEMPLATE_FILE.exists():
        return TEMPLATE_FILE.read_text()
    else:
        # Fallback to simple template if file not found
        return """# Daily Development Report - {date}

## Project: {project_name}

## Commits
{commits}

## Files Changed
{files_changed}

## Summary
{summary}

## Next Steps
{next_steps}
"""

DAILY_REPORT_TEMPLATE = get_daily_report_template()

# Startup report template
STARTUP_REPORT_TEMPLATE = """# Development Startup Report - {timestamp}

## Project: {project_name}

## Current Status
{status}

## Today's Goals
{goals}

## Blockers/Issues
{blockers}

## Notes
{notes}
"""

def get_daily_reports_path(project: str) -> Path:
    """Get path to daily_reports folder for a project"""
    if "/" in project:  # Nested project
        return BASE_DIR / project / "daily_reports"
    return BASE_DIR / project / "daily_reports"

def get_startup_reports_path(project: str) -> Path:
    """Get path to daily_dev_startup_reports folder for a project"""
    if "/" in project:  # Nested project
        return BASE_DIR / project / "daily_dev_startup_reports"
    return BASE_DIR / project / "daily_dev_startup_reports"

def get_all_projects_with_daily_reports() -> List[str]:
    """Get list of all projects with daily_reports"""
    projects = DAILY_REPORTS_PROJECTS.copy()
    projects.extend([k for k, v in NESTED_PROJECTS.items() if v.get("daily_reports")])
    return projects

def get_all_projects_with_startup_reports() -> List[str]:
    """Get list of all projects with startup reports"""
    projects = STARTUP_REPORTS_PROJECTS.copy()
    projects.extend([k for k, v in NESTED_PROJECTS.items() if v.get("daily_dev_startup_reports")])
    return projects
