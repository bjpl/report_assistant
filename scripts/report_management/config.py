#!/usr/bin/env python3
"""
Report Management Configuration
Defines paths and settings for daily reports system
"""

import os
from pathlib import Path
from typing import List, Dict

# Base directory for all projects
BASE_DIR = Path("/mnt/c/Users/brand/Development/Project_Workspace/active-development")

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

# Report template
DAILY_REPORT_TEMPLATE = """# Daily Development Report - {date}

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
