#!/bin/bash
# Report Assistant - Bash Aliases for Quick Commands
# Add to your ~/.bashrc or ~/.zshrc:
# source /path/to/report_assistant/report_aliases.sh

# Base paths
export REPORT_ASSISTANT="/mnt/c/Users/brand/Development/Project_Workspace/active-development/report_assistant"
export PROJECT_ROOT="/mnt/c/Users/brand/Development/Project_Workspace/active-development"

# === CORE ALIASES ===

# Quick daily operations
alias rt="cd $REPORT_ASSISTANT && make today"          # Report Today
alias rg="cd $REPORT_ASSISTANT && make gms"            # Report GMS
alias rp="cd $REPORT_ASSISTANT && make progress"       # Report Progress
alias rc="cd $REPORT_ASSISTANT && make commit"         # Report Commit
alias rs="cd $REPORT_ASSISTANT && ./report status"     # Report Status

# === PROJECT NAVIGATION ===

# Quick CD to report directories
alias cdr="cd $REPORT_ASSISTANT"
alias cdrd="cd $REPORT_ASSISTANT/daily_reports"
alias cdrg="cd $REPORT_ASSISTANT/daily_dev_startup_reports"

# === AUDIT & VALIDATION ===

alias ra="cd $REPORT_ASSISTANT && make audit"          # Report Audit
alias raa="cd $REPORT_ASSISTANT && make audit-all"     # Report Audit All
alias rv="cd $REPORT_ASSISTANT && make validate"       # Report Validate

# === GENERATION ===

alias rgen="cd $REPORT_ASSISTANT && make generate-all"  # Generate all missing
alias rbf="cd $REPORT_ASSISTANT && make backfill"      # Backfill from git

# === SWARM OPERATIONS ===

alias rswarm="npx claude-flow@alpha swarm init mesh --max-agents 5"
alias rswarm-audit="npx claude-flow@alpha swarm deploy audit-all"
alias rswarm-align="npx claude-flow@alpha swarm deploy align-reports"
alias rswarm-gms="npx claude-flow@alpha sparc run gms-audit"

# === FUNCTIONS FOR ADVANCED OPERATIONS ===

# Initialize new project with reports
rinit() {
    local project="${1:-$(basename $(pwd))}"
    echo "🎯 Initializing reports for: $project"
    cd "$PROJECT_ROOT/$project" 2>/dev/null || cd "$PROJECT_ROOT"
    mkdir -p daily_reports daily_dev_startup_reports docs/templates
    cp "$REPORT_ASSISTANT/docs/templates/"*.md docs/templates/ 2>/dev/null || true
    echo "✅ Project initialized: $project"
}

# Quick report for specific project
rproject() {
    local project="$1"
    if [[ -z "$project" ]]; then
        echo "Usage: rproject <project_name>"
        return 1
    fi
    cd "$PROJECT_ROOT/$project" && ls -la daily_reports/ daily_dev_startup_reports/ 2>/dev/null
}

# Show report stats for current directory or project
rstats() {
    local dir="${1:-$(pwd)}"
    echo "📊 Report Statistics for: $(basename $dir)"
    echo "Daily Reports: $(find $dir/daily_reports -name "*.md" 2>/dev/null | wc -l)"
    echo "GMS Reports:   $(find $dir/daily_dev_startup_reports -name "*.md" 2>/dev/null | wc -l)"
}

# Quick edit today's reports
redit() {
    local today=$(date +%Y-%m-%d)
    local editor="${EDITOR:-vi}"

    case "$1" in
        gms|g)
            $editor "$REPORT_ASSISTANT/daily_dev_startup_reports/${today}_startup_report.md"
            ;;
        progress|p)
            $editor "$REPORT_ASSISTANT/daily_reports/${today}.md"
            ;;
        both|b|"")
            $editor "$REPORT_ASSISTANT/daily_dev_startup_reports/${today}_startup_report.md" \
                    "$REPORT_ASSISTANT/daily_reports/${today}.md"
            ;;
        *)
            echo "Usage: redit [gms|progress|both]"
            ;;
    esac
}

# Quick backup
rbackup() {
    local date=$(date +%Y%m%d_%H%M%S)
    local backup_file="$REPORT_ASSISTANT/backups/reports_backup_${date}.tar.gz"
    mkdir -p "$REPORT_ASSISTANT/backups"
    tar -czf "$backup_file" -C "$REPORT_ASSISTANT" daily_reports daily_dev_startup_reports
    echo "✅ Backup created: $backup_file"
}

# List recent reports
rrecent() {
    local days="${1:-7}"
    echo "📅 Reports from last $days days:"
    find "$PROJECT_ROOT" \( -path "*/daily_reports/*.md" -o -path "*/daily_dev_startup_reports/*.md" \) \
         -mtime -"$days" -type f 2>/dev/null | \
         while read -r file; do
             echo "  $(basename $(dirname $(dirname "$file")))/$(basename $(dirname "$file"))/$(basename "$file")"
         done | sort -r | head -20
}

# Git operations for reports
rgit() {
    cd "$REPORT_ASSISTANT"
    case "$1" in
        status|s)
            git status daily_reports/ daily_dev_startup_reports/
            ;;
        diff|d)
            git diff daily_reports/ daily_dev_startup_reports/
            ;;
        add|a)
            git add daily_reports/ daily_dev_startup_reports/
            ;;
        commit|c)
            git add daily_reports/ daily_dev_startup_reports/
            git commit -m "docs: Add reports for $(date +%Y-%m-%d)"
            ;;
        push|p)
            git push
            ;;
        *)
            echo "Usage: rgit [status|diff|add|commit|push]"
            ;;
    esac
}

# Search reports
rsearch() {
    local pattern="$1"
    if [[ -z "$pattern" ]]; then
        echo "Usage: rsearch <pattern>"
        return 1
    fi
    echo "🔍 Searching for: $pattern"
    grep -r "$pattern" "$PROJECT_ROOT"/*/daily_reports "$PROJECT_ROOT"/*/daily_dev_startup_reports 2>/dev/null | head -20
}

# Quick compliance check
rcheck() {
    local project="${1:-$(basename $(pwd))}"
    local daily_exists="❌"
    local gms_exists="❌"

    [[ -d "$PROJECT_ROOT/$project/daily_reports" ]] && daily_exists="✅"
    [[ -d "$PROJECT_ROOT/$project/daily_dev_startup_reports" ]] && gms_exists="✅"

    echo "📋 Compliance Check: $project"
    echo "  Daily Reports Dir:   $daily_exists"
    echo "  GMS Reports Dir:     $gms_exists"

    if [[ "$daily_exists" == "✅" ]]; then
        echo "  Daily Report Count:  $(ls "$PROJECT_ROOT/$project/daily_reports/"*.md 2>/dev/null | wc -l)"
    fi

    if [[ "$gms_exists" == "✅" ]]; then
        echo "  GMS Report Count:    $(ls "$PROJECT_ROOT/$project/daily_dev_startup_reports/"*.md 2>/dev/null | wc -l)"
    fi
}

# Morning routine
rmorning() {
    echo "☀️ Good morning! Starting your day..."
    cd "$REPORT_ASSISTANT"
    make gms
    echo ""
    echo "📝 GMS report created. Please review and fill in the 8 checkpoints."
    echo "📁 Opening in editor..."
    redit gms
}

# Evening routine
revening() {
    echo "🌙 Wrapping up your day..."
    cd "$REPORT_ASSISTANT"
    make progress
    echo ""
    echo "📝 Progress report created. Document today's achievements."
    echo "📁 Opening in editor..."
    redit progress
    echo ""
    read -p "Commit reports? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        make commit
        echo "✅ Reports committed. Great work today!"
    fi
}

# Help function
rhelp() {
    cat << EOF
Report Assistant - Quick Commands
=================================

DAILY OPERATIONS:
  rt              - Generate today's reports (GMS + progress)
  rg              - Generate GMS startup report
  rp              - Generate daily progress report
  rc              - Commit today's reports
  rs              - Show current status
  redit [type]    - Edit today's reports (gms/progress/both)

PROJECT MANAGEMENT:
  rinit [project] - Initialize project with report structure
  rproject <name> - Show reports for specific project
  rcheck [project]- Check compliance for project

AUDIT & VALIDATION:
  ra              - Audit all projects
  rv              - Validate all reports
  rstats [dir]    - Show statistics

UTILITIES:
  rbackup         - Create backup of all reports
  rrecent [days]  - List recent reports
  rsearch <text>  - Search in all reports
  rgit <command>  - Git operations for reports

SWARM OPERATIONS:
  rswarm          - Initialize swarm
  rswarm-audit    - Deploy audit swarm
  rswarm-align    - Deploy alignment swarm
  rswarm-gms      - Run GMS audit with swarm

ROUTINES:
  rmorning        - Morning routine (create & edit GMS)
  revening        - Evening routine (create progress & commit)

NAVIGATION:
  cdr             - CD to report_assistant
  cdrd            - CD to daily_reports
  cdrg            - CD to daily_dev_startup_reports

Type 'rhelp' to see this help again.
EOF
}

# === AUTO-COMPLETION (for bash) ===

if [[ -n "$BASH_VERSION" ]]; then
    # Completion for rproject
    _rproject_complete() {
        local cur="${COMP_WORDS[COMP_CWORD]}"
        local projects=$(ls -d "$PROJECT_ROOT"/*/ 2>/dev/null | xargs -n1 basename)
        COMPREPLY=($(compgen -W "$projects" -- "$cur"))
    }
    complete -F _rproject_complete rproject

    # Completion for redit
    complete -W "gms progress both g p b" redit

    # Completion for rgit
    complete -W "status diff add commit push s d a c p" rgit
fi

# Show available commands on load
echo "📚 Report Assistant loaded! Type 'rhelp' for available commands."