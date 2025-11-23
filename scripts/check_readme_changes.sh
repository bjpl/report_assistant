#!/bin/bash

# Git Operations Specialist - README Change Detection Script
# Purpose: Check git status for all 16 tracked projects
# Date: 2025-11-11

BASE_DIR="/mnt/c/Users/brand/Development/Project_Workspace/active-development"

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

echo "========================================="
echo "README Change Detection Report"
echo "Date: $(date)"
echo "========================================="
echo ""

TOTAL_PROJECTS=${#PROJECTS[@]}
CHANGED_PROJECTS=0
UNCHANGED_PROJECTS=0
ERROR_PROJECTS=0

declare -a PROJECTS_WITH_CHANGES
declare -a PROJECTS_WITHOUT_CHANGES
declare -a PROJECTS_WITH_ERRORS

for project in "${PROJECTS[@]}"; do
    PROJECT_PATH="$BASE_DIR/$project"

    echo "Checking: $project"
    echo "Path: $PROJECT_PATH"

    if [ ! -d "$PROJECT_PATH" ]; then
        echo "  ❌ ERROR: Directory does not exist"
        ((ERROR_PROJECTS++))
        PROJECTS_WITH_ERRORS+=("$project")
        echo ""
        continue
    fi

    if [ ! -d "$PROJECT_PATH/.git" ]; then
        echo "  ⚠️  WARNING: Not a git repository"
        ((ERROR_PROJECTS++))
        PROJECTS_WITH_ERRORS+=("$project")
        echo ""
        continue
    fi

    # Check git status for README.md changes
    cd "$PROJECT_PATH"
    README_STATUS=$(git status --porcelain README.md 2>/dev/null)

    if [ -n "$README_STATUS" ]; then
        echo "  ✅ README.md has changes"
        echo "  Status: $README_STATUS"
        ((CHANGED_PROJECTS++))
        PROJECTS_WITH_CHANGES+=("$project")
    else
        echo "  ℹ️  No README changes detected"
        ((UNCHANGED_PROJECTS++))
        PROJECTS_WITHOUT_CHANGES+=("$project")
    fi

    echo ""
done

echo "========================================="
echo "Summary"
echo "========================================="
echo "Total Projects Checked: $TOTAL_PROJECTS"
echo "Projects with README Changes: $CHANGED_PROJECTS"
echo "Projects without Changes: $UNCHANGED_PROJECTS"
echo "Projects with Errors: $ERROR_PROJECTS"
echo ""

if [ $CHANGED_PROJECTS -gt 0 ]; then
    echo "Projects with README changes:"
    for project in "${PROJECTS_WITH_CHANGES[@]}"; do
        echo "  - $project"
    done
    echo ""
fi

if [ $UNCHANGED_PROJECTS -gt 0 ]; then
    echo "Projects without changes:"
    for project in "${PROJECTS_WITHOUT_CHANGES[@]}"; do
        echo "  - $project"
    done
    echo ""
fi

if [ $ERROR_PROJECTS -gt 0 ]; then
    echo "Projects with errors:"
    for project in "${PROJECTS_WITH_ERRORS[@]}"; do
        echo "  - $project"
    done
    echo ""
fi

echo "========================================="
echo "Next Steps:"
echo "========================================="
if [ $CHANGED_PROJECTS -gt 0 ]; then
    echo "1. Review changes in projects listed above"
    echo "2. Run commit script to stage and commit README changes"
    echo "3. Review commit summary"
    echo "4. Execute push commands (manual approval required)"
else
    echo "No README changes detected. Waiting for README updates to complete."
fi
