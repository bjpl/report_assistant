#!/bin/bash

# Portfolio Analysis v4 - Comprehensive Git Metrics for Curated Projects
# Focus on Language Learning, Puzzles, Research, Galleries, Utilities, E-commerce, Visualizations

BASE_DIR="/c/Users/brand/Development/Project_Workspace/active-development"
OUTPUT_DIR="$BASE_DIR/report_assistant/docs"
RAW_DATA_DIR="$OUTPUT_DIR/git_raw_data_v4"
REPORT_FILE="$OUTPUT_DIR/portfolio_analysis_v4.md"
EXEC_SUMMARY_FILE="$OUTPUT_DIR/portfolio_executive_summary_v4.md"

# Create output directories
mkdir -p "$RAW_DATA_DIR"

# Define portfolio projects by category
declare -A PROJECTS

# Language Learning
PROJECTS[aves]="Language Learning"
PROJECTS[describe_it]="Language Learning"
PROJECTS[hablas]="Language Learning"
PROJECTS[language-learning/subjunctive_practice]="Language Learning"

# Puzzles
PROJECTS[california_puzzle_game]="Puzzles"
PROJECTS[colombia_puzzle_game]="Puzzles"

# Open Source Research
PROJECTS[corporate_intel]="Open Source Research"
PROJECTS[open_learn]="Open Source Research"

# Galleries and Portfolios
PROJECTS[brandonjplambert]="Galleries & Portfolios"
PROJECTS[letratos]="Galleries & Portfolios"
PROJECTS[online_language_learning_resources]="Galleries & Portfolios"

# Utilities
PROJECTS[video_gen]="Utilities"
PROJECTS[report_assistant]="Utilities"

# E-commerce
PROJECTS[fancy_monkey]="E-commerce"

# Visualizations
PROJECTS[internet]="Visualizations"

echo "Portfolio Analysis v4 - Starting $(date '+%Y-%m-%d %H:%M:%S')"
echo "Total Projects: ${#PROJECTS[@]}"
echo ""

# Function to analyze a single project
analyze_project() {
    local project_path="$1"
    local project_name="$2"
    local category="$3"
    local output_file="$RAW_DATA_DIR/${project_name}_v4.txt"

    echo "Analyzing: $project_name ($category)"

    if [ ! -d "$project_path" ]; then
        echo "  ⚠ Project directory not found: $project_path"
        return 1
    fi

    # Initialize output file
    echo "=== Portfolio Analysis v4: $project_name ===" > "$output_file"
    echo "Category: $category" >> "$output_file"
    echo "Generated: $(date '+%Y-%m-%d %H:%M:%S')" >> "$output_file"
    echo "" >> "$output_file"

    cd "$project_path" 2>/dev/null || {
        echo "  ⚠ Cannot access directory"
        return 1
    }

    # Check for git repository
    if [ ! -d ".git" ]; then
        # Try to find .git in parent directories (for subdirectories)
        if ! git rev-parse --git-dir > /dev/null 2>&1; then
            echo "  ⚠ Not a git repository"
            echo "ERROR: Not a git repository" >> "$output_file"
            return 1
        fi
    fi

    # 1. Basic Stats
    echo "## 1. Repository Statistics" >> "$output_file"
    echo "---" >> "$output_file"
    total_commits=$(git rev-list --all --count 2>/dev/null || echo "0")
    recent_commits=$(git log --since="2024-08-01" --oneline --all 2>/dev/null | wc -l)
    first_commit=$(git log --reverse --format="%ai" --all 2>/dev/null | head -1)
    last_commit=$(git log --format="%ai" --all 2>/dev/null | head -1)
    authors=$(git log --format="%an" --all 2>/dev/null | sort -u | wc -l)
    branches=$(git branch -a 2>/dev/null | wc -l)

    echo "Total Commits: $total_commits" >> "$output_file"
    echo "Commits Since Aug 2024: $recent_commits" >> "$output_file"
    echo "First Commit: $first_commit" >> "$output_file"
    echo "Last Commit: $last_commit" >> "$output_file"
    echo "Authors: $authors" >> "$output_file"
    echo "Branches: $branches" >> "$output_file"
    echo "" >> "$output_file"

    # 2. Conventional Commits Analysis
    echo "## 2. Conventional Commit Types (Since Aug 2024)" >> "$output_file"
    echo "---" >> "$output_file"
    for type in feat fix docs test refactor chore style perf build ci; do
        count=$(git log --since="2024-08-01" --format="%s" --all 2>/dev/null | grep -E "^$type[:(]" | wc -l)
        if [ "$count" -gt 0 ]; then
            echo "$type: $count" >> "$output_file"
        fi
    done
    conventional_total=$(git log --since="2024-08-01" --format="%s" --all 2>/dev/null | grep -E "^(feat|fix|docs|test|refactor|chore|style|perf|build|ci)[:(]" | wc -l)
    other=$((recent_commits - conventional_total))
    [ "$other" -gt 0 ] && echo "other: $other" >> "$output_file"
    echo "" >> "$output_file"

    # 3. Code Churn
    echo "## 3. Code Churn Analysis (Since Aug 2024)" >> "$output_file"
    echo "---" >> "$output_file"
    churn_stats=$(git log --since="2024-08-01" --numstat --format="" --all 2>/dev/null | \
                  awk '{added+=$1; removed+=$2} END {printf "Lines Added: %d\nLines Removed: %d\nNet Change: %d\n", added, removed, added-removed}')
    echo "$churn_stats" >> "$output_file"
    echo "" >> "$output_file"

    # 4. File Analysis
    echo "## 4. Most Changed Files (Top 15)" >> "$output_file"
    echo "---" >> "$output_file"
    git log --since="2024-08-01" --name-only --format="" --all 2>/dev/null | \
        grep -v '^$' | sort | uniq -c | sort -rn | head -15 | \
        awk '{printf "%5d  %s\n", $1, $2}' >> "$output_file"
    echo "" >> "$output_file"

    # 5. Technology Stack Detection
    echo "## 5. Technology Stack" >> "$output_file"
    echo "---" >> "$output_file"

    [ -f "package.json" ] && echo "✓ Node.js/npm project" >> "$output_file"
    [ -f "tsconfig.json" ] && echo "✓ TypeScript" >> "$output_file"
    [ -f "vite.config.ts" ] || [ -f "vite.config.js" ] && echo "✓ Vite" >> "$output_file"
    [ -f "next.config.js" ] || [ -f "next.config.mjs" ] && echo "✓ Next.js" >> "$output_file"
    [ -f "requirements.txt" ] || [ -f "pyproject.toml" ] && echo "✓ Python" >> "$output_file"
    [ -f "Gemfile" ] && echo "✓ Ruby" >> "$output_file"
    [ -f "tailwind.config.js" ] || [ -f "tailwind.config.ts" ] && echo "✓ Tailwind CSS" >> "$output_file"
    [ -f ".github/workflows" ] && [ -d ".github/workflows" ] && echo "✓ GitHub Actions CI/CD" >> "$output_file"
    [ -f "Dockerfile" ] && echo "✓ Docker" >> "$output_file"
    [ -f "docker-compose.yml" ] && echo "✓ Docker Compose" >> "$output_file"

    # Check package.json for frameworks
    if [ -f "package.json" ]; then
        grep -q '"react"' package.json && echo "✓ React" >> "$output_file"
        grep -q '"vue"' package.json && echo "✓ Vue" >> "$output_file"
        grep -q '"express"' package.json && echo "✓ Express" >> "$output_file"
        grep -q '"vitest"' package.json && echo "✓ Vitest" >> "$output_file"
        grep -q '"jest"' package.json && echo "✓ Jest" >> "$output_file"
        grep -q '"playwright"' package.json && echo "✓ Playwright" >> "$output_file"
    fi
    echo "" >> "$output_file"

    # 6. Temporal Patterns
    echo "## 6. Day of Week Distribution (Since Aug 2024)" >> "$output_file"
    echo "---" >> "$output_file"
    git log --since="2024-08-01" --format="%ad" --date=format:'%u' --all 2>/dev/null | \
        sort | uniq -c | awk '{
            day=$2;
            days[1]="Monday"; days[2]="Tuesday"; days[3]="Wednesday";
            days[4]="Thursday"; days[5]="Friday"; days[6]="Saturday"; days[7]="Sunday";
            printf "%-10s: %3d commits\n", days[day], $1
        }' >> "$output_file"
    echo "" >> "$output_file"

    # 7. Author Contributions
    echo "## 7. Author Contributions (Since Aug 2024)" >> "$output_file"
    echo "---" >> "$output_file"
    git log --since="2024-08-01" --format="%an" --all 2>/dev/null | \
        sort | uniq -c | sort -rn | head -10 | \
        awk '{printf "%5d commits  %s\n", $1, substr($0, index($0,$2))}' >> "$output_file"
    echo "" >> "$output_file"

    # 8. Recent Activity
    echo "## 8. Recent Commits (Last 10)" >> "$output_file"
    echo "---" >> "$output_file"
    git log --format="%h | %ai | %an | %s" --all 2>/dev/null | head -10 | \
        awk -F'|' '{printf "%s | %s | %-20s | %s\n", $1, $2, $3, $4}' >> "$output_file"
    echo "" >> "$output_file"

    # 9. Commit Size Analysis
    echo "## 9. Commit Size Distribution (Since Aug 2024)" >> "$output_file"
    echo "---" >> "$output_file"
    git log --since="2024-08-01" --shortstat --format="%H" --all 2>/dev/null | \
        awk '
            /^[0-9a-f]{40}/ { commits++ }
            /files? changed/ {
                split($0, a, ",");
                insertions=0; deletions=0;
                for(i in a) {
                    if(a[i] ~ /insertion/) { gsub(/[^0-9]/, "", a[i]); insertions = a[i] }
                    if(a[i] ~ /deletion/) { gsub(/[^0-9]/, "", a[i]); deletions = a[i] }
                }
                total = insertions + deletions;
                if(total < 10) small++;
                else if(total <= 100) medium++;
                else large++;
                total_lines += total;
            }
            END {
                avg = (commits > 0) ? total_lines / commits : 0;
                printf "Small (<10 lines):   %d commits\n", small
                printf "Medium (10-100):     %d commits\n", medium
                printf "Large (>100 lines):  %d commits\n", large
                printf "Average lines/commit: %.1f\n", avg
            }
        ' >> "$output_file"
    echo "" >> "$output_file"

    echo "  ✓ Analysis complete"
}

# Main execution
echo "Starting Portfolio Analysis v4..."
echo ""

# Analyze each project
for project in "${!PROJECTS[@]}"; do
    category="${PROJECTS[$project]}"
    project_path="$BASE_DIR/$project"

    # Clean project name for file
    project_name=$(echo "$project" | tr '/' '_' | tr '-' '_')

    analyze_project "$project_path" "$project_name" "$category"
    echo ""
done

echo ""
echo "✓ All project analyses complete"
echo "Raw data saved to: $RAW_DATA_DIR"
echo ""
echo "Generating consolidated reports..."

# Generate consolidated markdown report
python3 "$BASE_DIR/report_assistant/scripts/generate_portfolio_report_v4.py"

echo ""
echo "✓ Portfolio Analysis v4 Complete!"
echo "Reports generated:"
echo "  - Main Report: $REPORT_FILE"
echo "  - Executive Summary: $EXEC_SUMMARY_FILE"
echo "  - Raw Data: $RAW_DATA_DIR/*.txt"

exit 0
