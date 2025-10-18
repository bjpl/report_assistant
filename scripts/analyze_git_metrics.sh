#!/bin/bash

# Git Metrics Extraction Script
# Analyzes all repositories in active-development workspace

BASE_DIR="/mnt/c/Users/brand/Development/Project_Workspace/active-development"
OUTPUT_FILE="/mnt/c/Users/brand/Development/Project_Workspace/active-development/report_assistant/docs/git_metrics_detailed.md"

# Top 10 repositories by commit count
TOP_REPOS=(
  "california_puzzle_game:278"
  "colombia_puzzle_game:250"
  "brandonjplambert:238"
  "online_language_learning_resources:198"
  "aves:146"
  "letratos:122"
  "describe_it:112"
  "corporate_intel:84"
  "hablas:71"
  "open_learn:41"
)

echo "# Git Metrics Analysis Report" > "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "**Generated:** $(date '+%Y-%m-%d %H:%M:%S')" >> "$OUTPUT_FILE"
echo "**Analysis Period:** Since 2024-08-01" >> "$OUTPUT_FILE"
echo "**Total Repositories Analyzed:** 24" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

echo "## Executive Summary" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Count total commits across all repos
total_commits=0
for entry in "${TOP_REPOS[@]}"; do
  count="${entry#*:}"
  total_commits=$((total_commits + count))
done

echo "- **Total Commits (Top 10 Repos):** $total_commits" >> "$OUTPUT_FILE"
echo "- **Analysis Date Range:** August 2024 - October 2025" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

echo "## 1. Repository Commit Overview" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "| Repository | Total Commits | Since Aug 2024 |" >> "$OUTPUT_FILE"
echo "|------------|---------------|----------------|" >> "$OUTPUT_FILE"

# Analyze each top repository
for entry in "${TOP_REPOS[@]}"; do
  repo="${entry%:*}"
  total="${entry#*:}"

  if [ -d "$BASE_DIR/$repo/.git" ]; then
    recent=$(cd "$BASE_DIR/$repo" && git log --since="2024-08-01" --oneline --all 2>/dev/null | wc -l)
    echo "| $repo | $total | $recent |" >> "$OUTPUT_FILE"
  fi
done

echo "" >> "$OUTPUT_FILE"

echo "## 2. Commit Message Pattern Analysis" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "### Conventional Commit Type Distribution" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

for entry in "${TOP_REPOS[@]}"; do
  repo="${entry%:*}"

  echo "#### $repo" >> "$OUTPUT_FILE"
  echo "" >> "$OUTPUT_FILE"
  echo "| Type | Count |" >> "$OUTPUT_FILE"
  echo "|------|-------|" >> "$OUTPUT_FILE"

  if [ -d "$BASE_DIR/$repo/.git" ]; then
    cd "$BASE_DIR/$repo"

    # Count conventional commit types
    for type in feat fix docs test refactor chore style perf build ci; do
      count=$(git log --since="2024-08-01" --format="%s" --all 2>/dev/null | grep -E "^$type[:(]" | wc -l)
      if [ "$count" -gt 0 ]; then
        echo "| $type | $count |" >> "$OUTPUT_FILE"
      fi
    done

    # Count non-conventional commits
    total_commits=$(git log --since="2024-08-01" --oneline --all 2>/dev/null | wc -l)
    conventional_commits=$(git log --since="2024-08-01" --format="%s" --all 2>/dev/null | grep -E "^(feat|fix|docs|test|refactor|chore|style|perf|build|ci)[:(]" | wc -l)
    other_commits=$((total_commits - conventional_commits))

    if [ "$other_commits" -gt 0 ]; then
      echo "| other | $other_commits |" >> "$OUTPUT_FILE"
    fi
  fi

  echo "" >> "$OUTPUT_FILE"
done

echo "## 3. Code Churn Analysis" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "| Repository | Lines Added | Lines Removed | Net Change | Churn Ratio |" >> "$OUTPUT_FILE"
echo "|------------|-------------|---------------|------------|-------------|" >> "$OUTPUT_FILE"

for entry in "${TOP_REPOS[@]}"; do
  repo="${entry%:*}"

  if [ -d "$BASE_DIR/$repo/.git" ]; then
    cd "$BASE_DIR/$repo"

    # Calculate code churn
    stats=$(git log --since="2024-08-01" --numstat --format="" --all 2>/dev/null | \
            awk '{added+=$1; removed+=$2} END {print added"|"removed"|"(added-removed)"|"(removed>0?added/removed:0)}')

    if [ -n "$stats" ]; then
      added=$(echo "$stats" | cut -d'|' -f1)
      removed=$(echo "$stats" | cut -d'|' -f2)
      net=$(echo "$stats" | cut -d'|' -f3)
      ratio=$(echo "$stats" | cut -d'|' -f4)

      # Handle empty values
      added=${added:-0}
      removed=${removed:-0}
      net=${net:-0}
      ratio=${ratio:-0}

      echo "| $repo | $added | $removed | $net | $ratio |" >> "$OUTPUT_FILE"
    fi
  fi
done

echo "" >> "$OUTPUT_FILE"

echo "## 4. Temporal Commit Distribution" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Analyze temporal patterns for top 3 repos
for i in 0 1 2; do
  entry="${TOP_REPOS[$i]}"
  repo="${entry%:*}"

  echo "### $repo" >> "$OUTPUT_FILE"
  echo "" >> "$OUTPUT_FILE"

  if [ -d "$BASE_DIR/$repo/.git" ]; then
    cd "$BASE_DIR/$repo"

    # Hourly distribution
    echo "#### Hourly Distribution" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "| Hour | Commits |" >> "$OUTPUT_FILE"
    echo "|------|---------|" >> "$OUTPUT_FILE"

    git log --since="2024-08-01" --format="%ad" --date=format:'%H' --all 2>/dev/null | \
      sort | uniq -c | awk '{printf "| %s:00 | %s |\n", $2, $1}' >> "$OUTPUT_FILE"

    echo "" >> "$OUTPUT_FILE"

    # Day of week distribution
    echo "#### Day of Week Distribution" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "| Day | Commits |" >> "$OUTPUT_FILE"
    echo "|-----|---------|" >> "$OUTPUT_FILE"

    git log --since="2024-08-01" --format="%ad" --date=format:'%u' --all 2>/dev/null | \
      sort | uniq -c | awk '{
        day=$2;
        days[1]="Monday"; days[2]="Tuesday"; days[3]="Wednesday";
        days[4]="Thursday"; days[5]="Friday"; days[6]="Saturday"; days[7]="Sunday";
        printf "| %s | %s |\n", days[day], $1
      }' >> "$OUTPUT_FILE"

    echo "" >> "$OUTPUT_FILE"
  fi
done

echo "## 5. File Change Frequency (Hotspots)" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Top 3 repos
for i in 0 1 2; do
  entry="${TOP_REPOS[$i]}"
  repo="${entry%:*}"

  echo "### $repo - Top 20 Most Changed Files" >> "$OUTPUT_FILE"
  echo "" >> "$OUTPUT_FILE"
  echo "| Changes | File |" >> "$OUTPUT_FILE"
  echo "|---------|------|" >> "$OUTPUT_FILE"

  if [ -d "$BASE_DIR/$repo/.git" ]; then
    cd "$BASE_DIR/$repo"
    git log --since="2024-08-01" --name-only --format="" --all 2>/dev/null | \
      grep -v '^$' | sort | uniq -c | sort -rn | head -20 | \
      awk '{printf "| %s | %s |\n", $1, $2}' >> "$OUTPUT_FILE"
  fi

  echo "" >> "$OUTPUT_FILE"
done

echo "## 6. Author Contribution Analysis" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

for i in 0 1 2; do
  entry="${TOP_REPOS[$i]}"
  repo="${entry%:*}"

  echo "### $repo" >> "$OUTPUT_FILE"
  echo "" >> "$OUTPUT_FILE"
  echo "| Author | Commits | Percentage |" >> "$OUTPUT_FILE"
  echo "|--------|---------|------------|" >> "$OUTPUT_FILE"

  if [ -d "$BASE_DIR/$repo/.git" ]; then
    cd "$BASE_DIR/$repo"
    total=$(git log --since="2024-08-01" --oneline --all 2>/dev/null | wc -l)

    git log --since="2024-08-01" --format="%an" --all 2>/dev/null | \
      sort | uniq -c | sort -rn | \
      awk -v total="$total" '{
        percentage = (total > 0) ? ($1 / total * 100) : 0;
        printf "| %s | %s | %.1f%% |\n", substr($0, index($0,$2)), $1, percentage
      }' >> "$OUTPUT_FILE"
  fi

  echo "" >> "$OUTPUT_FILE"
done

echo "## 7. Commit Size Distribution" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "| Repository | Small (<10 lines) | Medium (10-100) | Large (>100) | Avg Lines/Commit |" >> "$OUTPUT_FILE"
echo "|------------|-------------------|-----------------|--------------|------------------|" >> "$OUTPUT_FILE"

for entry in "${TOP_REPOS[@]}"; do
  repo="${entry%:*}"

  if [ -d "$BASE_DIR/$repo/.git" ]; then
    cd "$BASE_DIR/$repo"

    # Analyze commit sizes
    git log --since="2024-08-01" --shortstat --format="%H" --all 2>/dev/null | \
      awk '
        /^[0-9a-f]{40}/ { commits++ }
        /files? changed/ {
          split($0, a, ",");
          for(i in a) {
            if(a[i] ~ /insertion/) { gsub(/[^0-9]/, "", a[i]); insertions += a[i] }
            if(a[i] ~ /deletion/) { gsub(/[^0-9]/, "", a[i]); deletions += a[i] }
          }
          total = insertions + deletions;
          if(total < 10) small++;
          else if(total <= 100) medium++;
          else large++;
          total_lines += total;
        }
        END {
          avg = (commits > 0) ? total_lines / commits : 0;
          printf "| '"$repo"' | %d | %d | %d | %.1f |\n", small, medium, large, avg
        }
      ' >> "$OUTPUT_FILE"
  fi
done

echo "" >> "$OUTPUT_FILE"

echo "## 8. Branch and Merge Activity" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "| Repository | Total Branches | Merge Commits | Active Branches |" >> "$OUTPUT_FILE"
echo "|------------|----------------|---------------|-----------------|" >> "$OUTPUT_FILE"

for entry in "${TOP_REPOS[@]}"; do
  repo="${entry%:*}"

  if [ -d "$BASE_DIR/$repo/.git" ]; then
    cd "$BASE_DIR/$repo"

    total_branches=$(git branch -a 2>/dev/null | wc -l)
    merge_commits=$(git log --since="2024-08-01" --merges --oneline --all 2>/dev/null | wc -l)
    active_branches=$(git branch -a 2>/dev/null | grep -v "HEAD" | wc -l)

    echo "| $repo | $total_branches | $merge_commits | $active_branches |" >> "$OUTPUT_FILE"
  fi
done

echo "" >> "$OUTPUT_FILE"

echo "## Commands Used for Verification" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo '```bash' >> "$OUTPUT_FILE"
echo "# Commit count" >> "$OUTPUT_FILE"
echo 'git rev-list --all --count' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "# Conventional commits by type" >> "$OUTPUT_FILE"
echo 'git log --since="2024-08-01" --format="%s" --all | grep -E "^(feat|fix|docs):" | cut -d: -f1 | sort | uniq -c' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "# Code churn" >> "$OUTPUT_FILE"
echo 'git log --since="2024-08-01" --numstat --format="" --all | awk '\''{added+=$1; removed+=$2} END {print added, removed}'\''' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "# Temporal distribution" >> "$OUTPUT_FILE"
echo 'git log --since="2024-08-01" --format="%ad" --date=format:'\''%H'\'' --all | sort | uniq -c' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "# File hotspots" >> "$OUTPUT_FILE"
echo 'git log --since="2024-08-01" --name-only --format="" --all | sort | uniq -c | sort -rn | head -20' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "# Author stats" >> "$OUTPUT_FILE"
echo 'git log --since="2024-08-01" --format="%an" --all | sort | uniq -c | sort -rn' >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "# Branch and merge activity" >> "$OUTPUT_FILE"
echo 'git branch -a | wc -l' >> "$OUTPUT_FILE"
echo 'git log --since="2024-08-01" --merges --oneline --all | wc -l' >> "$OUTPUT_FILE"
echo '```' >> "$OUTPUT_FILE"

echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "*Report generated by Git Metrics Extraction System*" >> "$OUTPUT_FILE"

chmod +x "$0"
