# Report Assistant - Quick Reference Card

## 🚀 Installation

```bash
# Add to ~/.bashrc or ~/.zshrc:
source /path/to/report_assistant/report_aliases.sh

# Or use directly:
cd report_assistant
make help               # See all make commands
./report help           # See all CLI commands
```

---

## ⚡ Quick Commands (3 Ways)

### Method 1: Make Commands
```bash
make today              # Generate both reports
make gms                # GMS startup report
make progress           # Daily progress report
make commit             # Commit reports
make audit              # Audit all projects
```

### Method 2: NPM Scripts
```bash
npm run today           # Generate both reports
npm run gms             # GMS startup report
npm run progress        # Daily progress report
npm run commit          # Commit reports
npm run audit           # Audit all projects
```

### Method 3: Shell Aliases
```bash
rt                      # Report Today (both)
rg                      # Report GMS
rp                      # Report Progress
rc                      # Report Commit
rs                      # Report Status
```

---

## 📊 Daily Workflow

### Morning Routine
```bash
rmorning                # Create GMS report & open editor
# OR
make gms && redit gms
# OR
npm run morning
```

### Evening Routine
```bash
revening                # Create progress report, edit, commit
# OR
make progress && redit progress && make commit
# OR
npm run evening
```

---

## 🎯 Common Tasks

### Initialize New Project
```bash
# Method 1: Make
make init-project P=my-project

# Method 2: Shell function
rinit my-project

# Method 3: CLI
./report init my-project
```

### Audit Projects
```bash
# All projects
make audit
ra                      # Shell alias

# Specific project
make status P=video_gen
rcheck video_gen        # Shell alias
```

### Generate Missing Reports
```bash
# All missing
make generate-all
npm run generate:all

# Backfill from git
make backfill P=project
rbf                     # Shell alias
```

---

## 🤖 Swarm Operations

```bash
# Initialize swarm
rswarm
npx claude-flow swarm init mesh

# Deploy audit swarm
rswarm-audit
npm run swarm:audit

# Deploy alignment swarm
rswarm-align
npm run swarm:align

# GMS audit with AI
rswarm-gms
npm run swarm:gms
```

---

## 📁 Directory Structure

```
report_assistant/
├── daily_reports/              # Post-session progress
├── daily_dev_startup_reports/  # Pre-session GMS audits
├── docs/
│   └── templates/             # Report templates
├── scripts/
│   └── report_management/     # Python automation
├── backups/                   # Report backups
├── Makefile                   # Make commands
├── package.json               # NPM scripts
├── report                     # Shell CLI
└── report_aliases.sh          # Bash aliases
```

---

## 📋 Template Types

| Template | Purpose | When to Use | Directory |
|----------|---------|-------------|-----------|
| **GMS Startup** | 8-checkpoint audit | Before work (AM) | `daily_dev_startup_reports/` |
| **Daily Progress** | Session tracking | After work (PM) | `daily_reports/` |
| **Strategic Audit** | Deep review | Quarterly | `docs/audits/` |

---

## ⚡ Speed Commands (Aliases)

```bash
# Navigation
cdr                     # CD report_assistant
cdrd                    # CD daily_reports
cdrg                    # CD daily_dev_startup_reports

# Quick edits
redit gms               # Edit today's GMS
redit progress          # Edit today's progress
redit both              # Edit both reports

# Git operations
rgit status             # Git status for reports
rgit commit             # Commit with message
rgit push               # Push to remote

# Utilities
rbackup                 # Create backup
rrecent 7               # Last 7 days reports
rsearch "TODO"          # Search in reports
rstats                  # Show statistics
```

---

## 📊 Compliance Check

```bash
# Check project compliance
rcheck my-project

# Output:
# ✅ Daily Reports Dir
# ✅ GMS Reports Dir
# Daily Report Count: 15
# GMS Report Count: 3
```

---

## 🔧 Maintenance

```bash
# Backup
make backup
rbackup                 # Shell function

# Clean
make clean              # Remove temp files
npm run clean

# Validate
make validate           # Check all reports
npm run validate

# Stats
make stats              # Show statistics
rstats                  # Shell function
```

---

## 💡 Pro Tips

1. **Batch Operations**: Use make for bulk operations
   ```bash
   make audit generate-all validate
   ```

2. **Project-Specific**: Add project name to commands
   ```bash
   make status P=video_gen
   make backfill P=my-project
   ```

3. **Dry Run**: Preview changes before applying
   ```bash
   ./report sync --dry-run
   ```

4. **Auto-complete**: Tab completion works with aliases
   ```bash
   rproject <TAB>        # Shows all projects
   redit <TAB>           # Shows gms/progress/both
   ```

5. **Quick Status**: Check everything at once
   ```bash
   rs && rstats && rrecent 3
   ```

---

## 🚨 Troubleshooting

```bash
# Missing reports?
make audit              # Find what's missing
make generate-all       # Generate them

# Wrong format?
make validate           # Check format
make update P=project   # Update to latest

# Git issues?
rgit status             # Check git status
rgit diff               # See changes
make commit             # Commit with standard message

# Need help?
make help               # Make commands
./report help           # CLI help
rhelp                   # Alias help
```

---

## 📞 Quick Support

```bash
# View templates
cat docs/templates/gms_startup_report_template.md
cat docs/templates/daily_report_template.md

# Check logs
tail -f daily_reports/$(date +%Y-%m-%d).md

# Run tests
make test
npm test
```

---

## 🎯 One-Liner Cheatsheet

```bash
# Today's complete workflow
make today && redit both && make commit

# Weekly maintenance
make audit stats backup

# Project setup
make init-project P=new-proj && cd ../new-proj

# Emergency backup & clean
make backup clean validate
```

---

**Version**: 2.0.0 | **Updated**: 2025-10-11 | **Standards**: GMS 8-Checkpoint