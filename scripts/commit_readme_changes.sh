#!/bin/bash

# Git Operations Specialist - README Commit Script
# Purpose: Stage and commit README changes across all tracked projects
# Date: 2025-11-11

BASE_DIR="/mnt/c/Users/brand/Development/Project_Workspace/active-development"
SUMMARY_FILE="$BASE_DIR/report_assistant/docs/readme_commit_summary.md"

# Array of all 16 unique projects
PROJECTS=(
    "agentic_learning"
    "algorithms_and_data_structures"
    "aves"
    "brandonjplambert"
    "california_puzzle_game"
    "colombia_puzzle_game"
    "corporate_intel"
    "deployment_sprint"
    "describe_it"
    "fancy_monkey"
    "hablas"
    "language-learning/subjunctive_practice"
    "letratos"
    "online_language_learning_resources"
    "open_learn"
    "video_gen"
)

# Commit message template
COMMIT_MESSAGE="docs: Update README with current project status and accurate information

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

echo "========================================="
echo "README Commit Script"
echo "Date: $(date)"
echo "========================================="
echo ""

TOTAL_COMMITS=0
FAILED_COMMITS=0
SKIPPED_PROJECTS=0

declare -a COMMITTED_PROJECTS
declare -a FAILED_PROJECTS
declare -a SKIPPED_PROJECTS_LIST

# Initialize summary file
cat > "$SUMMARY_FILE" << 'EOL'
# README Commit Summary

**Date:** $(date)
**Git Operations Specialist**

---

## Overview

This document summarizes all README commits made across tracked projects.

---

## Commits Created

EOL

for project in "${PROJECTS[@]}"; do
    PROJECT_PATH="$BASE_DIR/$project"

    echo "Processing: $project"
    echo "Path: $PROJECT_PATH"

    if [ ! -d "$PROJECT_PATH" ]; then
        echo "  ⏭️  SKIPPED: Directory does not exist"
        ((SKIPPED_PROJECTS++))
        SKIPPED_PROJECTS_LIST+=("$project - directory not found")
        echo ""
        continue
    fi

    if [ ! -d "$PROJECT_PATH/.git" ]; then
        echo "  ⏭️  SKIPPED: Not a git repository"
        ((SKIPPED_PROJECTS++))
        SKIPPED_PROJECTS_LIST+=("$project - not a git repo")
        echo ""
        continue
    fi

    cd "$PROJECT_PATH"

    # Check if README.md has changes
    README_STATUS=$(git status --porcelain README.md 2>/dev/null)

    if [ -z "$README_STATUS" ]; then
        echo "  ⏭️  SKIPPED: No changes to commit"
        ((SKIPPED_PROJECTS++))
        SKIPPED_PROJECTS_LIST+=("$project - no changes")
        echo ""
        continue
    fi

    echo "  📝 Changes detected: $README_STATUS"

    # Stage README.md
    git add README.md
    if [ $? -ne 0 ]; then
        echo "  ❌ FAILED: Could not stage README.md"
        ((FAILED_COMMITS++))
        FAILED_PROJECTS+=("$project - staging failed")
        echo ""
        continue
    fi

    # Create commit
    git commit -m "$COMMIT_MESSAGE"
    if [ $? -ne 0 ]; then
        echo "  ❌ FAILED: Could not create commit"
        ((FAILED_COMMITS++))
        FAILED_PROJECTS+=("$project - commit failed")
        echo ""
        continue
    fi

    # Get commit hash
    COMMIT_HASH=$(git log -1 --format="%H")
    COMMIT_SHORT=$(git log -1 --format="%h")

    echo "  ✅ SUCCESS: Commit created ($COMMIT_SHORT)"
    ((TOTAL_COMMITS++))
    COMMITTED_PROJECTS+=("$project|$COMMIT_SHORT|$COMMIT_HASH")

    # Add to summary file
    echo "" >> "$SUMMARY_FILE"
    echo "### $project" >> "$SUMMARY_FILE"
    echo "" >> "$SUMMARY_FILE"
    echo "- **Commit Hash:** $COMMIT_HASH" >> "$SUMMARY_FILE"
    echo "- **Short Hash:** $COMMIT_SHORT" >> "$SUMMARY_FILE"
    echo "- **Date:** $(date)" >> "$SUMMARY_FILE"
    echo "- **Status:** Committed (not pushed)" >> "$SUMMARY_FILE"
    echo "" >> "$SUMMARY_FILE"

    echo ""
done

# Add summary statistics to file
cat >> "$SUMMARY_FILE" << EOL

---

## Summary Statistics

- **Total Projects Checked:** ${#PROJECTS[@]}
- **Commits Created:** $TOTAL_COMMITS
- **Projects Skipped:** $SKIPPED_PROJECTS
- **Failed Commits:** $FAILED_COMMITS

---

## Committed Projects

EOL

if [ $TOTAL_COMMITS -gt 0 ]; then
    for item in "${COMMITTED_PROJECTS[@]}"; do
        IFS='|' read -r proj short_hash full_hash <<< "$item"
        echo "- **$proj** - $short_hash" >> "$SUMMARY_FILE"
    done
else
    echo "No commits were created." >> "$SUMMARY_FILE"
fi

cat >> "$SUMMARY_FILE" << EOL

---

## Skipped Projects

EOL

if [ $SKIPPED_PROJECTS -gt 0 ]; then
    for item in "${SKIPPED_PROJECTS_LIST[@]}"; do
        echo "- $item" >> "$SUMMARY_FILE"
    done
else
    echo "No projects were skipped." >> "$SUMMARY_FILE"
fi

cat >> "$SUMMARY_FILE" << EOL

---

## Failed Commits

EOL

if [ $FAILED_COMMITS -gt 0 ]; then
    for item in "${FAILED_PROJECTS[@]}"; do
        echo "- $item" >> "$SUMMARY_FILE"
    done
else
    echo "No failures occurred." >> "$SUMMARY_FILE"
fi

cat >> "$SUMMARY_FILE" << 'EOL'

---

## Push Commands (Manual Review Required)

**⚠️ DO NOT EXECUTE AUTOMATICALLY**

Review the commits above, then execute push commands manually:

```bash
# For each committed project:
EOL

if [ $TOTAL_COMMITS -gt 0 ]; then
    for item in "${COMMITTED_PROJECTS[@]}"; do
        IFS='|' read -r proj short_hash full_hash <<< "$item"
        PROJECT_PATH="$BASE_DIR/$proj"
        echo "cd $PROJECT_PATH && git push origin HEAD" >> "$SUMMARY_FILE"
    done
else
    echo "# No commits to push" >> "$SUMMARY_FILE"
fi

cat >> "$SUMMARY_FILE" << 'EOL'
```

---

## Verification Steps

1. Review each commit in the projects listed above
2. Verify commit messages are accurate
3. Check that Claude Code attribution is present
4. Manually execute push commands after approval

---

*Generated by Git Operations Specialist*
EOL

echo "========================================="
echo "Final Summary"
echo "========================================="
echo "Total Projects Checked: ${#PROJECTS[@]}"
echo "Commits Created: $TOTAL_COMMITS"
echo "Projects Skipped: $SKIPPED_PROJECTS"
echo "Failed Commits: $FAILED_COMMITS"
echo ""

if [ $TOTAL_COMMITS -gt 0 ]; then
    echo "Committed projects:"
    for item in "${COMMITTED_PROJECTS[@]}"; do
        IFS='|' read -r proj short_hash full_hash <<< "$item"
        echo "  ✅ $proj ($short_hash)"
    done
    echo ""
fi

if [ $SKIPPED_PROJECTS -gt 0 ]; then
    echo "Skipped projects:"
    for item in "${SKIPPED_PROJECTS_LIST[@]}"; do
        echo "  ⏭️  $item"
    done
    echo ""
fi

if [ $FAILED_COMMITS -gt 0 ]; then
    echo "Failed projects:"
    for item in "${FAILED_PROJECTS[@]}"; do
        echo "  ❌ $item"
    done
    echo ""
fi

echo "========================================="
echo "Commit summary saved to:"
echo "$SUMMARY_FILE"
echo "========================================="
echo ""
echo "⚠️  IMPORTANT: Review commits before pushing!"
echo "See summary file for push commands."
