# Report Assistant

A comprehensive, standardized daily report management system built with GMS (Goal-Milestone-Status) methodology for tracking development progress across multiple projects.

## Overview

Report Assistant provides automated tools for managing, validating, and analyzing daily development reports. It integrates git commit history with structured reporting to maintain accurate project documentation and progress tracking across an entire portfolio of projects.

## Features

### 📊 Automated Report Management
- **Daily Reports**: Auto-generate reports from git commit history
- **GMS Reports**: Goal-Milestone-Status methodology for progress tracking
- **Progress Reports**: Comprehensive project progress documentation
- **Validation**: Ensure reports align with actual git commits

### 🔍 Analysis & Insights
- **Cross-Project Analysis**: Analyze activity across multiple projects
- **Search Capabilities**: Full-text search across all reports
- **Statistics**: Commit counts, file changes, activity patterns
- **Time-Series Analysis**: Track development velocity over time

### 🤖 Swarm Orchestration
- **Claude-Flow Integration**: AI-powered report generation and analysis
- **Parallel Processing**: Process multiple projects concurrently
- **Memory Coordination**: Persistent state across agent sessions
- **Automated Workflows**: Batch operations for efficiency

### 📁 Multi-Project Support
- Track 15+ projects with daily reports
- Support for 10+ projects with startup reports
- Nested project support (e.g., language-learning/subjunctive_practice)
- Automatic project discovery and configuration

## Tech Stack

- **Core**: Node.js, Python 3.x
- **Orchestration**: Claude-Flow v2.0.0 (SPARC methodology)
- **Validation**: Python scripts with git integration
- **Generation**: Template-based report creation
- **Analysis**: Text processing, regex, statistics

## Installation

```bash
# Clone repository
git clone https://github.com/bjpl/report_assistant.git
cd report_assistant

# Install dependencies
npm run setup:deps

# Create required directories
npm run setup:dirs
```

## Quick Start

```bash
# Generate today's GMS report
npm run gms

# Generate progress report
npm run progress

# Full workflow (GMS + Progress)
npm run today

# Validate all reports
npm run audit

# Generate missing reports
npm run generate:missing
```

## Usage

### Daily Operations

```bash
# Morning workflow
npm run morning  # Generate GMS report for the day

# Evening workflow
npm run evening  # Generate progress report and commit

# Quick aliases
npm run t  # Today (GMS + Progress)
npm run g  # GMS only
npm run p  # Progress only
npm run c  # Commit reports
```

### Report Management

```bash
# Validate reports against git history
npm run audit

# Validate specific project
npm run audit:project -- --project video_gen

# Generate missing reports for all projects
npm run generate:missing

# Backfill historical reports
npm run backfill
```

### Analysis & Search

```bash
# Search across all reports
python scripts/report_management/analyze_reports.py search "authentication"

# Project statistics (last 30 days)
python scripts/report_management/analyze_reports.py stats --project aves

# Cross-project analysis
python scripts/report_management/analyze_reports.py cross --days 90
```

### Swarm Operations

```bash
# Initialize swarm for parallel processing
npm run swarm:init

# Run comprehensive audit across all projects
npm run swarm:audit

# Align reports across projects
npm run swarm:align

# Execute GMS audit workflow
npm run swarm:gms
```

## Configuration

Projects are configured in `scripts/report_management/config.py`:

```python
PROJECTS = [
    'aves',
    'hablas',
    'describe_it',
    # ... add more projects
]

# Report templates
DAILY_REPORT_TEMPLATE = """
# Daily Development Report
## Date: {date}
## Project: {project}
...
"""
```

## Report Types

### Daily Reports (`daily_reports/`)
- Automatically generated from git commits
- Include commit messages, files changed, statistics
- Naming: `YYYY-MM-DD.md`
- Location: `{project}/daily_reports/`

### Startup Reports (`daily_dev_startup_reports/`)
- Manual planning documents created at session start
- Goals, blockers, priorities, notes
- Custom naming with timestamps
- Location: `{project}/daily_dev_startup_reports/`

### GMS Reports
- Goal-Milestone-Status methodology
- High-level progress tracking
- Generated via `npm run gms`

## Architecture

```
report_assistant/
├── daily_reports/          # Daily reports for this project
├── daily_dev_startup_reports/  # Startup reports for this project
├── docs/                   # Documentation and analysis
│   ├── templates/          # Report templates
│   └── portfolio/          # Portfolio analysis
├── scripts/
│   ├── generate-gms.js     # GMS report generation
│   ├── generate-progress.js  # Progress report generation
│   └── report_management/  # Python validation/analysis tools
├── memory/                 # Agent memory and state
│   ├── agents/             # Per-agent memory storage
│   └── sessions/           # Session persistence
└── coordination/           # Swarm coordination configs
```

## Workflows

### Weekly Maintenance

```bash
# 1. Validate all reports
npm run audit -- --verbose

# 2. Delete invalid reports
python scripts/report_management/validate_reports.py --delete

# 3. Generate missing reports
npm run generate:missing

# 4. Weekly summary
npm run weekly
```

### New Project Setup

```bash
# Create project directories
npm run init:project -- --project=new_project

# Add to config.py
# Edit scripts/report_management/config.py and add 'new_project' to PROJECTS

# Validate setup
npm run audit:project -- --project new_project
```

## Testing

```bash
# Run Python tests
npm run test

# Watch mode
npm run test:watch

# Linting
npm run lint

# Format code
npm run format
```

## Tracked Projects

The system currently tracks and manages reports for:

**Language Learning** (10 projects): aves, hablas, describe_it, letratos, online_language_learning_resources, sinonimos series

**Development Tools** (5 projects): report_assistant, deployment_sprint, learn_claude_flow, algorithms_and_data_structures

**Web Applications** (4 projects): fancy_monkey, corporate_intel, video_gen, open_learn

**Geographic & Data Viz** (3 projects): california_puzzle_game, colombia_puzzle_game, internet

**Portfolio & Professional** (2 projects): brandonjplambert, agentic_learning

**AI & Voice** (1 project): learning_voice_agent

## API Reference

### Python Scripts

```python
# Validate reports
from scripts.report_management.validate_reports import validate_project
validate_project('aves')

# Generate reports
from scripts.report_management.generate_reports import generate_missing
generate_missing('hablas', overwrite=False)

# Analyze reports
from scripts.report_management.analyze_reports import search_reports
results = search_reports('authentication', case_sensitive=False)
```

### Node.js Scripts

```javascript
// Generate GMS report
const generateGMS = require('./scripts/generate-gms.js');
generateGMS();

// Generate progress report
const generateProgress = require('./scripts/generate-progress.js');
generateProgress();
```

## Performance

- **Report Validation**: ~500ms per project
- **Report Generation**: ~2-5 seconds per report
- **Cross-Project Analysis**: ~3 seconds for 15 projects
- **Swarm Operations**: 2.8-4.4x faster than sequential

## Best Practices

1. **Daily Workflow**: Run `npm run today` at day start and `npm run evening` at day end
2. **Weekly Audit**: Run `npm run weekly` every Sunday
3. **Commit Reports**: Always commit reports after generation
4. **Validate First**: Run validation before bulk operations
5. **Use Swarms**: Leverage swarm operations for multi-project tasks

## Troubleshooting

**Reports not generating?**
- Ensure git repository exists in project directory
- Verify commits exist for the target date
- Check write permissions on daily_reports/

**Validation failures?**
- Check git repository status: `git status`
- Verify date format: YYYY-MM-DD
- Check config.py has correct project paths

**Search not working?**
- Try case-insensitive search: `--case-sensitive false`
- Check date ranges: `--days 30`
- Verify reports exist for the time period

## Contributing

This is a personal project management tool. Contributions welcome via issues and pull requests.

## License

MIT

## Author

Brandon Lambert

## Support

- Repository: https://github.com/bjpl/report_assistant
- Issues: https://github.com/bjpl/report_assistant/issues

---

**Part of the Brandon Lambert Development Portfolio** - Systematic project management and progress tracking across 26+ active development projects.
