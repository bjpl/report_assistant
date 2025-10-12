# Report Template Clarification Summary

**Date:** October 11, 2025
**Issue:** Confusion between different types of reports and their purposes
**Resolution:** Created 3 distinct templates with clear purposes

---

## The Problem

The report_assistant project had confusing template naming and unclear purposes:
- `startup_report_template.md` was overly complex for daily startup audits
- No dedicated template for GMS (8-checkpoint) methodology
- Unclear distinction between post-session progress reports and pre-session audits

---

## The Solution: 3 Distinct Report Types

### 1. Daily Progress Reports (`/daily_reports/`)

**Template:** `daily_report_template.md`
**Purpose:** Post-session progress tracking
**When:** AFTER completing work
**Directory:** `/daily_reports/YYYY-MM-DD.md`

**Use Case:**
```
You spent 4 hours building a new feature.
At the end of the session, you write:
- What features were completed
- What bugs were fixed
- What technical decisions were made
- What commits were pushed
```

**Key Sections:**
- Executive Summary
- Work Completed
- Technical Decisions
- Metrics & Performance
- Issues & Blockers
- Next Session Planning

---

### 2. GMS Startup Reports (`/daily_dev_startup_reports/`)

**Template:** `gms_startup_report_template.md` ✅ NEW
**Purpose:** Pre-session strategic audit
**When:** BEFORE starting work
**Directory:** `/daily_dev_startup_reports/YYYY-MM-DD_startup_report.md`

**Use Case:**
```
You're about to start a development session.
Before writing any code, you audit:
- Are daily reports up to date?
- What TODOs/FIXMEs exist?
- What's uncommitted?
- What issues are open?
- What's the technical debt?
- What should I work on?
- Generate 5 alternative plans (A/B/C/D/E)
- Choose the best plan
```

**Key Sections (8 Mandatory GMS Checkpoints):**
1. Daily Report Audit
2. Code Annotation Scan (TODO/FIXME/HACK)
3. Uncommitted Work Analysis
4. Issue Tracker Review
5. Technical Debt Assessment
6. Project Status Reflection
7. Alternative Plans Proposal (A/B/C/D/E)
8. Recommendation with Rationale

---

### 3. Strategic Audits (`/docs/audits/`)

**Template:** `strategic_audit_template.md` (renamed from `startup_report_template.md`)
**Purpose:** Deep strategic review
**When:** Quarterly, major milestones, or incidents
**Directory:** `/docs/audits/` or `/daily_dev_startup_reports/` (for major reviews)

**Use Case:**
```
You're planning a quarterly review, starting a new phase,
or conducting a post-incident analysis.
This is a comprehensive audit including:
- Architecture assessment
- Security posture
- Performance analysis
- Resource planning
- Budget implications
- Risk analysis
```

**Key Sections:**
- Executive Summary
- Audit Scope & Objectives
- Strategic Assessment (10 dimensions)
- Architecture Assessment
- Code Quality Analysis
- Testing & QA
- Performance & Scalability
- Security Posture
- Technical Debt Inventory
- Team & Process Assessment
- Risk Analysis
- Strategic Recommendations
- Resource & Budget Implications
- Success Metrics & KPIs

---

## File Changes Made

### Created Files
1. `/docs/templates/gms_startup_report_template.md` - NEW GMS template

### Renamed Files
2. `/docs/templates/startup_report_template.md` → `/docs/templates/strategic_audit_template.md`

### Updated Files
3. `/docs/DAILY_REPORTS_ALIGNMENT_SUMMARY.md` - Added clarification section

---

## Template Comparison Table

| Aspect | Daily Progress Report | GMS Startup Report | Strategic Audit |
|--------|----------------------|-------------------|-----------------|
| **Template** | `daily_report_template.md` | `gms_startup_report_template.md` | `strategic_audit_template.md` |
| **Directory** | `/daily_reports/` | `/daily_dev_startup_reports/` | `/docs/audits/` |
| **Timing** | After work (post-session) | Before work (pre-session) | Quarterly/milestones |
| **Frequency** | Every session (daily) | Daily or weekly | Quarterly/as-needed |
| **Length** | 200-300 lines | 300-500 lines | 500-800 lines |
| **Focus** | What was built | What should be built | Strategic planning |
| **Audience** | Team, future self | Developer (decision-making) | Stakeholders, leadership |
| **Sections** | 8 sections | 8 GMS checkpoints | 10+ strategic dimensions |
| **Output** | Progress documentation | Actionable plan (A/B/C/D/E) | Strategic recommendations |

---

## Usage Examples

### Scenario 1: Normal Daily Development

**Morning (9:00 AM):**
```bash
# Generate GMS startup report
cp docs/templates/gms_startup_report_template.md \
   daily_dev_startup_reports/2025-10-11_startup_report.md

# Fill in 8 checkpoints, choose Plan B
# Start work based on Plan B
```

**Evening (5:00 PM):**
```bash
# Generate daily progress report
cp docs/templates/daily_report_template.md \
   daily_reports/2025-10-11.md

# Document what was accomplished from Plan B
# Note any deviations or discoveries
```

---

### Scenario 2: Weekly Development (Smaller Projects)

**Monday Morning:**
```bash
# Generate GMS startup report for the week
cp docs/templates/gms_startup_report_template.md \
   daily_dev_startup_reports/2025-10-11_startup_report.md

# Plan entire week's work (Plan A/B/C/D/E)
```

**Daily (Tue-Fri):**
```bash
# Generate daily progress reports
cp docs/templates/daily_report_template.md \
   daily_reports/2025-10-XX.md

# Document daily progress toward weekly plan
```

---

### Scenario 3: Quarterly Planning

**Quarter End:**
```bash
# Generate strategic audit
cp docs/templates/strategic_audit_template.md \
   docs/audits/Q4-2025-strategic-audit.md

# Conduct comprehensive review
# Interview stakeholders
# Analyze architecture, security, performance
# Plan next quarter
```

---

## Memory Storage

All clarification updates stored in swarm memory:

```bash
# Coordination memory keys
swarm/fix/template-clarification-docs
swarm/fix/template-clarification-gms
```

---

## Benefits of This Clarification

1. **Clear Purpose:** Each template has a distinct purpose
2. **Correct Timing:** Know when to use each template (before/after/quarterly)
3. **Right Tool for Job:** GMS for planning, Daily for tracking, Strategic for audits
4. **Reduced Confusion:** Template names match their purposes
5. **Better Planning:** GMS methodology ensures thoughtful plan selection

---

## Next Steps for Users

1. **Start using GMS template** for pre-session planning
2. **Continue using daily template** for post-session tracking
3. **Use strategic template** only for major reviews
4. **Reference this document** when unsure which template to use

---

**Document Version:** 1.0.0
**Last Updated:** October 11, 2025
**Author:** Report Assistant Project
**Status:** Complete
