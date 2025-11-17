# Report Assistant

A comprehensive daily report management system employing GMS (Goal-Milestone-Status) methodology for tracking development progress across multiple projects.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Development](#development)
- [Configuration](#configuration)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Overview

Report Assistant provides automated tools for managing, validating, and analyzing daily development reports. The system integrates git commit history with structured reporting to maintain accurate project documentation and progress tracking across an entire portfolio of projects.

The platform supports tracking for 15 active projects with automated report generation, validation against actual commits, and comprehensive analysis capabilities.

## Features

### Automated Report Management

- Daily report auto-generation from git commit history
- GMS (Goal-Milestone-Status) methodology for progress tracking
- Comprehensive project progress documentation
- Report validation ensuring alignment with git commits

### Analysis and Insights

- Cross-project activity analysis across multiple repositories
- Full-text search capabilities across all reports
- Statistics tracking for commits, file changes, and activity patterns
- Time-series analysis for development velocity tracking

### Multi-Project Support

- Tracking for 15 projects with daily reports
- Support for 10+ projects with startup reports
- Nested project support for related repositories
- Automatic project discovery and configuration

## Tech Stack

- **Core**: Python 3.12.3 (primary), Makefile workflows
- **Validation**: Python scripts with git integration
- **Generation**: Template-based report creation
- **Analysis**: Text processing, regex, statistics
- **Testing**: pytest 8.4.2 with coverage tools

## Technical Overview

This project demonstrates **automated report management and validation systems** for software development progress tracking. The implementation showcases Python automation, git integration, GMS (Goal-Milestone-Status) methodology, and comprehensive cross-project analysis capabilities.

**Key Technologies:**
- Python 3.12.3 for report automation
- Git integration for commit history analysis
- Makefile-based workflow orchestration
- pytest 8.4.2 for testing infrastructure

**Implementation Highlights:**
- Automated daily report generation from git commits
- Cross-project analysis across 15 active projects
- Report validation against actual commit history
- Full-text search capabilities across all reports
- GMS methodology for progress tracking
- Template-based report generation system

## Exploring the Code

The project structure demonstrates **Python-based automation workflow**:

```
report_assistant/
├── daily_reports/          # Daily reports for this project
├── daily_dev_startup_reports/  # Startup reports
├── docs/                   # Documentation and analysis
│   ├── templates/          # Report templates
│   └── portfolio/          # Portfolio analysis
├── scripts/
│   └── report_management/  # Python validation/analysis tools
│       ├── analyze_reports.py    # Report analysis
│       ├── config.py             # Project configuration
│       ├── generate_reports.py   # Report generation
│       ├── report_cli.py         # CLI interface
│       └── validate_reports.py   # Report validation
├── Makefile                # Primary workflow tool
└── package.json            # Node.js metadata (minimal)
```

**For Technical Review:**

Those interested in the implementation details can explore:
- `scripts/report_management/` directory for Python automation
- `validate_reports.py` for git integration patterns
- `generate_reports.py` for template-based generation
- `analyze_reports.py` for text processing and search
- `Makefile` for workflow orchestration
- `docs/` directory for documentation and analysis

**Local Development** _(Optional for developers)_

<details>
<summary>Click to expand setup instructions</summary>

**Prerequisites:**
- Python 3.12.3 or higher
- Git (for commit history integration)
- pytest 8.4.2 (for testing)

**Setup:**

```bash
# Clone repository
git clone https://github.com/bjpl/report_assistant.git
cd report_assistant

# Install Python dependencies
pip install pytest pytest-asyncio pytest-cov pytest-mock

# Create required directories
mkdir -p tests backups
```

**Usage:**

Daily Operations:
```bash
# Validate all reports
make validate
# Or directly:
python scripts/report_management/validate_reports.py

# Generate missing reports
make generate
# Or directly:
python scripts/report_management/generate_reports.py

# Analyze reports
make analyze
# Or directly:
python scripts/report_management/analyze_reports.py

# Create backup
make backup
```

Report Management:
```bash
# Validate reports against git history
python scripts/report_management/validate_reports.py

# Validate specific project
python scripts/report_management/validate_reports.py --project aves

# Generate missing reports
python scripts/report_management/generate_reports.py

# Delete invalid reports
python scripts/report_management/validate_reports.py --delete
```

Analysis and Search:
```bash
# Search across all reports
python scripts/report_management/analyze_reports.py search "authentication"

# Analyze reports via CLI
python scripts/report_management/report_cli.py
```

</details>

## Project Structure

```
report_assistant/
├── daily_reports/              # Daily reports for this project
├── daily_dev_startup_reports/  # Startup reports for this project
├── docs/                       # Documentation and analysis
│   ├── templates/              # Report templates
│   └── portfolio/              # Portfolio analysis
├── scripts/
│   └── report_management/      # Python validation and analysis tools
│       ├── analyze_reports.py  # Report analysis
│       ├── config.py           # Project configuration
│       ├── generate_reports.py # Report generation
│       ├── report_cli.py       # CLI interface
│       └── validate_reports.py # Report validation
├── memory/                     # Agent memory and state (optional)
│   ├── agents/                 # Per-agent memory storage
│   └── sessions/               # Session persistence
├── coordination/               # Swarm coordination configs (optional)
├── Makefile                    # Primary workflow tool
└── package.json                # Node.js metadata (minimal)
```

## Development

### Report Types

**Daily Reports** (`daily_reports/`):
- Automatically generated from git commits
- Include commit messages, files changed, and statistics
- Naming convention: `YYYY-MM-DD.md`
- Location: `{project}/daily_reports/`

**Startup Reports** (`daily_dev_startup_reports/`):
- Manual planning documents created at session start
- Include goals, blockers, priorities, and notes
- Custom naming with timestamps
- Location: `{project}/daily_dev_startup_reports/`

**GMS Reports**:
- Goal-Milestone-Status methodology
- High-level progress tracking

### Weekly Maintenance Workflow

Validate all reports:
```bash
python scripts/report_management/validate_reports.py --verbose
```

Delete invalid reports:
```bash
python scripts/report_management/validate_reports.py --delete
```

Generate missing reports:
```bash
python scripts/report_management/generate_reports.py
```

Create backup:
```bash
make backup
```

### New Project Setup

Add project to configuration:
```bash
# Edit scripts/report_management/config.py
# Add project name to DAILY_REPORTS_PROJECTS
```

Create project directories:
```bash
mkdir -p ../new_project/daily_reports
mkdir -p ../new_project/daily_dev_startup_reports
```

Validate setup:
```bash
python scripts/report_management/validate_reports.py --project new_project
```

## Configuration

Projects are configured in `scripts/report_management/config.py`:

```python
PROJECTS = [
    'aves',
    'hablas',
    'describe_it',
    # Add additional projects here
]

# Report templates
DAILY_REPORT_TEMPLATE = """
# Daily Development Report
## Date: {date}
## Project: {project}
"""
```

## Testing

Test infrastructure is planned but not yet implemented. Testing dependencies are installed and ready for test development:

```bash
# Install testing dependencies
pip install pytest pytest-asyncio pytest-cov pytest-mock

# Run tests (when implemented)
pytest

# Coverage report (when implemented)
pytest --cov=scripts/report_management
```

## Contributing

Contributions are welcome. Submit issues and pull requests with clear descriptions of proposed changes.

## License

MIT License - See LICENSE file for details
