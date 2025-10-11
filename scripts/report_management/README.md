# Daily Report Management System

A comprehensive toolkit for managing, validating, generating, and analyzing daily development reports across multiple projects.

## Directory Structure

```
report_assistant/
├── scripts/
│   └── report_management/
│       ├── config.py              # Configuration and project definitions
│       ├── validate_reports.py    # Validate reports against git commits
│       ├── generate_reports.py    # Auto-generate missing reports
│       ├── analyze_reports.py     # Flexible report analysis
│       └── README.md              # This file
```

## Quick Start

### 1. Validate Reports

Check that all daily reports correspond to git commits:

```bash
# Validate all projects
python3 scripts/report_management/validate_reports.py

# Validate specific project
python3 scripts/report_management/validate_reports.py --project video_gen

# Show detailed information
python3 scripts/report_management/validate_reports.py --verbose

# Delete invalid reports (reports without commits)
python3 scripts/report_management/validate_reports.py --delete
```

### 2. Generate Missing Reports

Auto-generate reports for dates with commits but no reports:

```bash
# Generate missing reports for all projects
python3 scripts/report_management/generate_reports.py

# Generate for specific project
python3 scripts/report_management/generate_reports.py --project video_gen

# Generate for specific date
python3 scripts/report_management/generate_reports.py --project video_gen --date 2025-10-11

# Overwrite existing reports
python3 scripts/report_management/generate_reports.py --overwrite
```

### 3. Analyze Reports

Search and analyze reports with flexible queries:

```bash
# Search for text across all reports
python3 scripts/report_management/analyze_reports.py search "authentication"

# Search in specific project
python3 scripts/report_management/analyze_reports.py search "bug fix" --project aves

# Case-sensitive search
python3 scripts/report_management/analyze_reports.py search "API" --case-sensitive

# Get project statistics (last 30 days)
python3 scripts/report_management/analyze_reports.py stats --project video_gen

# Get stats for all projects
python3 scripts/report_management/analyze_reports.py stats

# Cross-project analysis
python3 scripts/report_management/analyze_reports.py cross

# Analyze last 90 days
python3 scripts/report_management/analyze_reports.py cross --days 90
```

## Features

### Report Validation
- ✅ Validates that daily reports exist only for dates with git commits
- ✅ Identifies reports without commits (should be deleted)
- ✅ Identifies commits without reports (should be generated)
- ✅ Optional automatic deletion of invalid reports
- ✅ Per-project or all-projects validation

### Report Generation
- ✅ Auto-generates reports from git commit history
- ✅ Includes commit messages, authors, timestamps
- ✅ Lists files changed
- ✅ Generates summary statistics
- ✅ Uses configurable templates
- ✅ Batch generation for all missing reports

### Report Analysis
- ✅ Full-text search across all reports
- ✅ Case-sensitive or case-insensitive search
- ✅ Context-aware search results (shows surrounding lines)
- ✅ Project-level statistics (commits, files, activity)
- ✅ Cross-project analysis
- ✅ Customizable time periods
- ✅ Most active projects ranking

## Configuration

Edit `config.py` to:
- Add/remove projects
- Modify report templates
- Change directory paths
- Add nested projects (e.g., language-learning/subjunctive_practice)

## Report Types

### Daily Reports (`daily_reports/`)
- **Purpose**: Automatically generated summary of daily work
- **Trigger**: Created for every day with git commits
- **Content**: Commit messages, files changed, summary
- **Naming**: `YYYY-MM-DD.md`

### Startup Reports (`daily_dev_startup_reports/`)
- **Purpose**: Ad-hoc planning before development sessions
- **Trigger**: Manually created when starting work
- **Content**: Goals, status, blockers, notes
- **Naming**: Custom timestamps or descriptions

## Workflow Examples

### Daily Maintenance

```bash
# 1. Validate all reports
python3 scripts/report_management/validate_reports.py --verbose

# 2. Delete invalid reports
python3 scripts/report_management/validate_reports.py --delete

# 3. Generate missing reports
python3 scripts/report_management/generate_reports.py

# 4. Review weekly stats
python3 scripts/report_management/analyze_reports.py stats --days 7
```

### Project Review

```bash
# Check specific project
python3 scripts/report_management/validate_reports.py --project video_gen

# Generate missing reports
python3 scripts/report_management/generate_reports.py --project video_gen

# View project stats
python3 scripts/report_management/analyze_reports.py stats --project video_gen --days 30
```

### Cross-Project Analysis

```bash
# Monthly overview
python3 scripts/report_management/analyze_reports.py cross --days 30

# Search for feature across all projects
python3 scripts/report_management/analyze_reports.py search "authentication"

# Find all API-related work
python3 scripts/report_management/analyze_reports.py search "API" --case-sensitive
```

## Projects with Reports

### Daily Reports (15 projects)
- agentic_learning
- algorithms_and_data_structures
- aves
- brandonjplambert
- california_puzzle_game
- colombia_puzzle_game
- corporate_intel
- deployment_sprint
- describe_it
- fancy_monkey
- hablas
- letratos
- online_language_learning_resources
- open_learn
- video_gen

### Startup Reports (10 projects)
- algorithms_and_data_structures
- aves
- california_puzzle_game
- colombia_puzzle_game
- corporate_intel
- describe_it
- fancy_monkey
- hablas
- letratos
- video_gen

### Nested Projects
- language-learning/subjunctive_practice (both types)

## Future Enhancements

Potential additions:
- 📊 Export reports to CSV/JSON
- 📈 Generate charts and visualizations
- 🔄 Sync reports with GitHub issues
- 📧 Email summaries
- 🎯 Goal tracking across reports
- 🏷️ Tag-based categorization
- 📝 Template customization per project
- 🔍 Advanced search with regex
- 📅 Calendar view of activity
- 🤖 AI-powered insights

## Troubleshooting

**Reports not found:**
- Check project path in `config.py`
- Ensure git repository exists
- Verify folder naming (daily_reports vs daily_dev_startup_reports)

**Generation fails:**
- Check git repository is valid
- Ensure write permissions
- Verify date format (YYYY-MM-DD)

**Analysis returns no results:**
- Try case-insensitive search
- Check date ranges
- Verify reports exist for the period

## Support

For issues or questions:
1. Check this README
2. Review `config.py` settings
3. Verify git repository status
4. Check file permissions
