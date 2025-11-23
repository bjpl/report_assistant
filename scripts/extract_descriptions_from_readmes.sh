#!/bin/bash

# Helper script to extract descriptions from README files
# This can be used to update the main script once the remaining READMEs are generated

BASE_PATH="/mnt/c/Users/brand/Development/Project_Workspace/active-development"

echo "========================================"
echo "README Description Extractor"
echo "========================================"
echo ""

# Projects that need README generation
PENDING_PROJECTS=(
    "ai_stack_analysis"
    "drive_reset"
    "llms_on_my_system"
    "report_assistant"
    "learn_strudel"
    "learning_agentic_engineering"
)

echo "Checking for newly generated READMEs..."
echo ""

for project in "${PENDING_PROJECTS[@]}"; do
    README_PATH="$BASE_PATH/$project/README.md"

    if [ -f "$README_PATH" ]; then
        echo "✓ Found: $project/README.md"
        echo "  First 3 lines:"
        head -n 3 "$README_PATH" | sed 's/^/    /'
        echo ""
    else
        echo "✗ Missing: $project/README.md"
        echo ""
    fi
done

echo "========================================"
echo "Instructions for updating main script:"
echo "========================================"
echo ""
echo "1. Read the first 1-2 sentences from each README"
echo "2. Extract a concise description (max 350 characters)"
echo "3. Update update_github_descriptions.sh by uncommenting the relevant sections"
echo "4. Replace [PLACEHOLDER] with the actual description"
echo "5. Run the updated script to update GitHub descriptions"
echo ""
