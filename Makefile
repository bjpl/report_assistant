# Report Assistant Makefile
# Standard commands for report management and maintenance
# Usage: make [command]

.PHONY: help audit generate sync validate clean init test deploy backup restore

# Default target - show help
help:
	@echo "Report Assistant - Standardized Commands"
	@echo "========================================"
	@echo ""
	@echo "Daily Operations:"
	@echo "  make today              - Generate today's reports (GMS + progress)"
	@echo "  make gms                - Generate GMS startup report for today"
	@echo "  make progress           - Generate daily progress report"
	@echo "  make commit             - Commit all report changes"
	@echo ""
	@echo "Bulk Operations:"
	@echo "  make audit              - Audit all projects for report compliance"
	@echo "  make generate-all       - Generate missing reports for all projects"
	@echo "  make sync               - Sync reports across all projects"
	@echo "  make validate           - Validate all reports against templates"
	@echo ""
	@echo "Project Management:"
	@echo "  make init-project P=name - Initialize reports for new project"
	@echo "  make backfill P=name    - Backfill reports from git history"
	@echo "  make update P=name      - Update project to latest format"
	@echo "  make status P=name      - Check project report status"
	@echo ""
	@echo "Template Operations:"
	@echo "  make list-templates     - List available templates"
	@echo "  make apply-template T=gms P=proj - Apply template to project"
	@echo "  make update-templates   - Update all templates to latest"
	@echo "  make validate-templates - Check template consistency"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean              - Clean temporary files"
	@echo "  make backup             - Backup all reports"
	@echo "  make restore DATE=YYYY-MM-DD - Restore from backup"
	@echo "  make stats              - Show report statistics"
	@echo ""
	@echo "Development:"
	@echo "  make test               - Run all tests"
	@echo "  make lint               - Lint Python scripts"
	@echo "  make format             - Format all code"
	@echo "  make install            - Install dependencies"

# Configuration
PYTHON := python3
PROJECT_ROOT := /mnt/c/Users/brand/Development/Project_Workspace/active-development
REPORT_ASSISTANT := $(PROJECT_ROOT)/report_assistant
SCRIPTS_DIR := $(REPORT_ASSISTANT)/scripts/report_management
TODAY := $(shell date +%Y-%m-%d)

# Daily Operations
today: gms progress
	@echo "✅ Today's reports generated"

gms:
	@echo "📊 Generating GMS startup report for $(TODAY)..."
	@cp $(REPORT_ASSISTANT)/docs/templates/gms_startup_report_template.md \
		$(REPORT_ASSISTANT)/daily_dev_startup_reports/$(TODAY)_startup_report.md
	@echo "✅ GMS report created: daily_dev_startup_reports/$(TODAY)_startup_report.md"
	@echo "📝 Please edit the report with today's analysis"

progress:
	@echo "📈 Generating daily progress report for $(TODAY)..."
	@cp $(REPORT_ASSISTANT)/docs/templates/daily_report_template.md \
		$(REPORT_ASSISTANT)/daily_reports/$(TODAY).md
	@echo "✅ Progress report created: daily_reports/$(TODAY).md"
	@echo "📝 Please edit the report with today's progress"

commit:
	@echo "💾 Committing all report changes..."
	@cd $(REPORT_ASSISTANT) && git add daily_reports/ daily_dev_startup_reports/
	@cd $(REPORT_ASSISTANT) && git commit -m "docs: Add reports for $(TODAY)" || echo "No changes to commit"
	@echo "✅ Reports committed"

# Bulk Operations
audit:
	@echo "🔍 Auditing all projects for report compliance..."
	@$(PYTHON) $(SCRIPTS_DIR)/audit_reports.py
	@echo "✅ Audit complete - see report_type_audit_matrix.md"

generate-all:
	@echo "🚀 Generating missing reports for all projects..."
	@$(PYTHON) $(SCRIPTS_DIR)/generate_reports.py --all
	@echo "✅ All missing reports generated"

sync:
	@echo "🔄 Syncing reports across all projects..."
	@$(PYTHON) $(SCRIPTS_DIR)/sync_reports.py
	@echo "✅ Report sync complete"

validate:
	@echo "✔️ Validating all reports against templates..."
	@$(PYTHON) $(SCRIPTS_DIR)/validate_reports.py
	@echo "✅ Validation complete"

# Project Management
init-project:
	@if [ -z "$(P)" ]; then echo "❌ Error: Project name required (P=name)"; exit 1; fi
	@echo "🎯 Initializing reports for project: $(P)"
	@mkdir -p $(PROJECT_ROOT)/$(P)/daily_reports
	@mkdir -p $(PROJECT_ROOT)/$(P)/daily_dev_startup_reports
	@cp $(REPORT_ASSISTANT)/docs/templates/*.md $(PROJECT_ROOT)/$(P)/docs/templates/ 2>/dev/null || true
	@echo "✅ Project $(P) initialized with report structure"

backfill:
	@if [ -z "$(P)" ]; then echo "❌ Error: Project name required (P=name)"; exit 1; fi
	@echo "📚 Backfilling reports for project: $(P)"
	@$(PYTHON) $(SCRIPTS_DIR)/generate_reports.py --project $(P) --backfill
	@echo "✅ Backfill complete for $(P)"

update:
	@if [ -z "$(P)" ]; then echo "❌ Error: Project name required (P=name)"; exit 1; fi
	@echo "🔄 Updating project $(P) to latest format..."
	@$(PYTHON) $(SCRIPTS_DIR)/update_format.py --project $(P)
	@echo "✅ Project $(P) updated"

status:
	@if [ -z "$(P)" ]; then echo "❌ Error: Project name required (P=name)"; exit 1; fi
	@echo "📊 Checking status for project: $(P)"
	@$(PYTHON) $(SCRIPTS_DIR)/check_status.py --project $(P)

# Template Operations
list-templates:
	@echo "📄 Available templates:"
	@echo "  - daily_report_template.md      : Post-session progress tracking"
	@echo "  - gms_startup_report_template.md: Pre-session 8-checkpoint audit"
	@echo "  - strategic_audit_template.md   : Quarterly/milestone review"

apply-template:
	@if [ -z "$(T)" ] || [ -z "$(P)" ]; then echo "❌ Error: Template (T=) and Project (P=) required"; exit 1; fi
	@echo "📝 Applying template $(T) to project $(P)..."
	@cp $(REPORT_ASSISTANT)/docs/templates/$(T)_template.md $(PROJECT_ROOT)/$(P)/
	@echo "✅ Template applied"

update-templates:
	@echo "🔄 Updating all templates to latest version..."
	@cd $(REPORT_ASSISTANT) && git pull origin main 2>/dev/null || true
	@echo "✅ Templates updated"

validate-templates:
	@echo "✔️ Validating template consistency..."
	@$(PYTHON) $(SCRIPTS_DIR)/validate_templates.py
	@echo "✅ Templates valid"

# Maintenance
clean:
	@echo "🧹 Cleaning temporary files..."
	@find $(REPORT_ASSISTANT) -name "*.pyc" -delete
	@find $(REPORT_ASSISTANT) -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@find $(REPORT_ASSISTANT) -name ".DS_Store" -delete 2>/dev/null || true
	@echo "✅ Cleanup complete"

backup:
	@echo "💾 Backing up all reports..."
	@tar -czf $(REPORT_ASSISTANT)/backups/reports_backup_$(TODAY).tar.gz \
		$(REPORT_ASSISTANT)/daily_reports \
		$(REPORT_ASSISTANT)/daily_dev_startup_reports
	@echo "✅ Backup created: backups/reports_backup_$(TODAY).tar.gz"

restore:
	@if [ -z "$(DATE)" ]; then echo "❌ Error: Backup date required (DATE=YYYY-MM-DD)"; exit 1; fi
	@echo "📥 Restoring reports from $(DATE)..."
	@tar -xzf $(REPORT_ASSISTANT)/backups/reports_backup_$(DATE).tar.gz -C $(REPORT_ASSISTANT)
	@echo "✅ Reports restored from $(DATE)"

stats:
	@echo "📊 Report Statistics"
	@echo "===================="
	@echo "Daily Reports: $$(find $(PROJECT_ROOT)/*/daily_reports -name "*.md" 2>/dev/null | wc -l)"
	@echo "GMS Reports:   $$(find $(PROJECT_ROOT)/*/daily_dev_startup_reports -name "*.md" 2>/dev/null | wc -l)"
	@echo "Projects:      $$(ls -d $(PROJECT_ROOT)/*/ | wc -l)"
	@echo ""
	@echo "Recent Activity:"
	@find $(PROJECT_ROOT)/*/daily_reports -name "*.md" -mtime -7 2>/dev/null | head -5

# Development
test:
	@echo "🧪 Running tests..."
	@cd $(REPORT_ASSISTANT) && python -m pytest tests/
	@echo "✅ All tests passed"

lint:
	@echo "🔍 Linting Python scripts..."
	@cd $(REPORT_ASSISTANT) && python -m pylint scripts/
	@echo "✅ Linting complete"

format:
	@echo "🎨 Formatting code..."
	@cd $(REPORT_ASSISTANT) && python -m black scripts/
	@echo "✅ Code formatted"

install:
	@echo "📦 Installing dependencies..."
	@pip install -r $(REPORT_ASSISTANT)/requirements.txt
	@npm install -g claude-flow@alpha
	@echo "✅ Dependencies installed"

# Quick aliases for common operations
.PHONY: t g s a
t: today      # Shorthand for make today
g: gms        # Shorthand for make gms
s: sync       # Shorthand for make sync
a: audit      # Shorthand for make audit