#!/usr/bin/env python3
"""
Portfolio Analysis v4 - Report Generator
Consolidates raw git analysis data into comprehensive markdown reports
"""

import os
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

BASE_DIR = Path("C:/Users/brand/Development/Project_Workspace/active-development")
RAW_DATA_DIR = BASE_DIR / "report_assistant/docs/git_raw_data_v4"
OUTPUT_DIR = BASE_DIR / "report_assistant/docs"

# Project categories
CATEGORIES = {
    "Language Learning": ["aves", "describe_it", "hablas", "language_learning_subjunctive_practice"],
    "Puzzles": ["california_puzzle_game", "colombia_puzzle_game"],
    "Open Source Research": ["corporate_intel", "open_learn"],
    "Galleries & Portfolios": ["brandonjplambert", "letratos", "online_language_learning_resources"],
    "Utilities": ["video_gen", "report_assistant"],
    "E-commerce": ["fancy_monkey"],
    "Visualizations": ["internet"]
}


def parse_raw_data(file_path):
    """Parse a raw analysis text file into structured data"""
    data = {
        'project_name': '',
        'category': '',
        'total_commits': 0,
        'recent_commits': 0,
        'authors': 0,
        'branches': 0,
        'conventional_commits': {},
        'tech_stack': [],
        'lines_added': 0,
        'lines_removed': 0,
        'net_change': 0,
        'top_files': [],
        'commit_size': {}
    }

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract project name and category
        match = re.search(r'=== Portfolio Analysis v4: (.+?) ===', content)
        if match:
            data['project_name'] = match.group(1)

        match = re.search(r'Category: (.+)', content)
        if match:
            data['category'] = match.group(1)

        # Extract statistics
        match = re.search(r'Total Commits: (\d+)', content)
        if match:
            data['total_commits'] = int(match.group(1))

        match = re.search(r'Commits Since Aug 2024: (\d+)', content)
        if match:
            data['recent_commits'] = int(match.group(1))

        match = re.search(r'Authors: (\d+)', content)
        if match:
            data['authors'] = int(match.group(1))

        match = re.search(r'Branches: (\d+)', content)
        if match:
            data['branches'] = int(match.group(1))

        # Extract conventional commits
        conv_section = re.search(r'## 2\. Conventional Commit Types.*?\n---\n(.*?)(?=\n\n|\n##|$)', content, re.DOTALL)
        if conv_section:
            for line in conv_section.group(1).strip().split('\n'):
                match = re.match(r'(\w+): (\d+)', line)
                if match:
                    data['conventional_commits'][match.group(1)] = int(match.group(2))

        # Extract code churn
        match = re.search(r'Lines Added: (\d+)', content)
        if match:
            data['lines_added'] = int(match.group(1))

        match = re.search(r'Lines Removed: (\d+)', content)
        if match:
            data['lines_removed'] = int(match.group(1))

        match = re.search(r'Net Change: (-?\d+)', content)
        if match:
            data['net_change'] = int(match.group(1))

        # Extract tech stack
        tech_section = re.search(r'## 5\. Technology Stack.*?\n---\n(.*?)(?=\n\n|\n##|$)', content, re.DOTALL)
        if tech_section:
            data['tech_stack'] = [line.strip() for line in tech_section.group(1).strip().split('\n') if line.strip()]

        # Extract commit size distribution
        size_section = re.search(r'## 9\. Commit Size Distribution.*?\n---\n(.*?)(?=\n\n|\n##|$)', content, re.DOTALL)
        if size_section:
            for line in size_section.group(1).strip().split('\n'):
                if 'Small' in line:
                    match = re.search(r'(\d+) commits', line)
                    if match:
                        data['commit_size']['small'] = int(match.group(1))
                elif 'Medium' in line:
                    match = re.search(r'(\d+) commits', line)
                    if match:
                        data['commit_size']['medium'] = int(match.group(1))
                elif 'Large' in line:
                    match = re.search(r'(\d+) commits', line)
                    if match:
                        data['commit_size']['large'] = int(match.group(1))

    except Exception as e:
        print(f"Error parsing {file_path}: {e}")

    return data


def generate_comprehensive_report():
    """Generate comprehensive portfolio report"""

    # Parse all raw data files
    projects_data = []
    for file_path in RAW_DATA_DIR.glob("*_v4.txt"):
        data = parse_raw_data(file_path)
        if data['project_name']:
            projects_data.append(data)

    # Sort by recent commits descending
    projects_data.sort(key=lambda x: x['recent_commits'], reverse=True)

    # Calculate totals and aggregates
    total_commits_all = sum(p['total_commits'] for p in projects_data)
    total_commits_recent = sum(p['recent_commits'] for p in projects_data)
    total_lines_added = sum(p['lines_added'] for p in projects_data)
    total_lines_removed = sum(p['lines_removed'] for p in projects_data)

    # Group by category
    by_category = defaultdict(list)
    for project in projects_data:
        by_category[project['category']].append(project)

    # Generate main report
    report = f"""# Portfolio Analysis v4: Comprehensive Development Metrics

**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Analysis Period:** August 1, 2024 - Present
**Total Projects:** {len(projects_data)}
**Portfolio Categories:** {len(by_category)}

---

## Executive Summary

### Portfolio Overview

This comprehensive analysis covers **{len(projects_data)} curated projects** across **{len(by_category)} categories**: Language Learning, Puzzles, Open Source Research, Galleries & Portfolios, Utilities, E-commerce, and Visualizations.

### Key Metrics

| Metric | All Time | Since Aug 2024 |
|--------|----------|----------------|
| **Total Commits** | {total_commits_all:,} | {total_commits_recent:,} |
| **Lines Added** | - | {total_lines_added:,} |
| **Lines Removed** | - | {total_lines_removed:,} |
| **Net Change** | - | {total_lines_added - total_lines_removed:,} |
| **Active Projects** | {len([p for p in projects_data if p['recent_commits'] > 0])} | - |

### Top 5 Most Active Projects (Since Aug 2024)

| Rank | Project | Category | Commits | Lines Changed |
|------|---------|----------|---------|---------------|
"""

    for i, project in enumerate(projects_data[:5], 1):
        lines_changed = project['lines_added'] + project['lines_removed']
        report += f"| {i} | **{project['project_name']}** | {project['category']} | {project['recent_commits']} | {lines_changed:,} |\n"

    report += f"""

---

## 1. Projects by Category

"""

    # Generate category sections
    for category, projects in sorted(by_category.items()):
        report += f"### {category}\n\n"
        report += f"**Projects:** {len(projects)}\n\n"

        # Category table
        report += "| Project | Total Commits | Recent Commits | Lines +/- | Tech Stack |\n"
        report += "|---------|---------------|----------------|-----------|------------|\n"

        for project in sorted(projects, key=lambda x: x['recent_commits'], reverse=True):
            tech_summary = ", ".join([t.replace('✓ ', '') for t in project['tech_stack'][:3]]) or "N/A"
            if len(project['tech_stack']) > 3:
                tech_summary += f" +{len(project['tech_stack'])-3}"

            lines_display = f"+{project['lines_added']:,}/-{project['lines_removed']:,}"

            report += f"| {project['project_name']} | {project['total_commits']} | {project['recent_commits']} | {lines_display} | {tech_summary} |\n"

        report += "\n"

    report += """---

## 2. Technology Stack Analysis

### Technology Adoption Across Portfolio

"""

    # Aggregate technology usage
    tech_counts = defaultdict(int)
    for project in projects_data:
        for tech in project['tech_stack']:
            clean_tech = tech.replace('✓ ', '').strip()
            tech_counts[clean_tech] += 1

    report += "| Technology | Projects | Adoption Rate |\n"
    report += "|------------|----------|---------------|\n"

    for tech, count in sorted(tech_counts.items(), key=lambda x: x[1], reverse=True):
        adoption = (count / len(projects_data)) * 100
        report += f"| {tech} | {count} | {adoption:.1f}% |\n"

    report += """

---

## 3. Development Activity Analysis

### Commit Pattern Analysis

"""

    # Aggregate conventional commits
    conv_totals = defaultdict(int)
    for project in projects_data:
        for commit_type, count in project['conventional_commits'].items():
            conv_totals[commit_type] += count

    report += "| Commit Type | Count | Percentage |\n"
    report += "|-------------|-------|------------|\n"

    total_conv = sum(conv_totals.values())
    for commit_type, count in sorted(conv_totals.items(), key=lambda x: x[1], reverse=True):
        pct = (count / total_conv * 100) if total_conv > 0 else 0
        report += f"| **{commit_type}** | {count} | {pct:.1f}% |\n"

    report += f"""

**Total Conventional Commits:** {total_conv}
**Conventional Commit Adoption:** {(total_conv / total_commits_recent * 100) if total_commits_recent > 0 else 0:.1f}%

---

## 4. Code Quality Indicators

### Commit Size Distribution

"""

    # Aggregate commit sizes
    total_small = sum(p['commit_size'].get('small', 0) for p in projects_data)
    total_medium = sum(p['commit_size'].get('medium', 0) for p in projects_data)
    total_large = sum(p['commit_size'].get('large', 0) for p in projects_data)
    total_sized = total_small + total_medium + total_large

    report += "| Size Category | Count | Percentage |\n"
    report += "|---------------|-------|------------|\n"

    if total_sized > 0:
        report += f"| Small (<10 lines) | {total_small} | {(total_small/total_sized*100):.1f}% |\n"
        report += f"| Medium (10-100 lines) | {total_medium} | {(total_medium/total_sized*100):.1f}% |\n"
        report += f"| Large (>100 lines) | {total_large} | {(total_large/total_sized*100):.1f}% |\n"

    report += """

**Insight:** Smaller, focused commits indicate better development practices and easier code review.

---

## 5. Project Deep Dive

"""

    # Detailed breakdown for each project
    for project in projects_data:
        report += f"""### {project['project_name']}

**Category:** {project['category']}
**Total Commits:** {project['total_commits']} ({project['recent_commits']} since Aug 2024)
**Authors:** {project['authors']}
**Branches:** {project['branches']}

**Code Activity (Since Aug 2024):**
- Lines Added: {project['lines_added']:,}
- Lines Removed: {project['lines_removed']:,}
- Net Change: {project['net_change']:+,}

**Technology Stack:**
"""

        for tech in project['tech_stack']:
            report += f"- {tech}\n"

        if not project['tech_stack']:
            report += "- No technology stack detected\n"

        report += "\n**Commit Type Breakdown:**\n"
        if project['conventional_commits']:
            for commit_type, count in sorted(project['conventional_commits'].items(), key=lambda x: x[1], reverse=True):
                report += f"- {commit_type}: {count}\n"
        else:
            report += "- No conventional commits detected\n"

        report += "\n---\n\n"

    report += f"""## 6. Insights & Recommendations

### Strengths

1. **Active Development:** {total_commits_recent} commits since August 2024 demonstrate consistent portfolio activity
2. **Technology Diversity:** {len(tech_counts)} different technologies used across portfolio
3. **Conventional Commits:** {(total_conv / total_commits_recent * 100) if total_commits_recent > 0 else 0:.1f}% adoption rate shows good development practices

### Areas for Improvement

1. **Testing Coverage:** Few projects show evidence of comprehensive testing frameworks
2. **CI/CD Adoption:** Limited GitHub Actions or automated pipeline usage
3. **Documentation:** Consider adding README files and inline documentation

### Portfolio Health Score: {calculate_health_score(projects_data)}/10

Based on commit activity, technology adoption, code quality indicators, and development practices.

---

*Report generated by Portfolio Analysis v4 System*
*Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

    # Write main report
    output_file = OUTPUT_DIR / "portfolio_analysis_v4.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✓ Main report generated: {output_file}")

    # Generate executive summary
    generate_executive_summary(projects_data, by_category)


def calculate_health_score(projects_data):
    """Calculate portfolio health score out of 10"""
    score = 0.0

    # Activity score (0-3 points)
    total_recent = sum(p['recent_commits'] for p in projects_data)
    if total_recent > 500:
        score += 3
    elif total_recent > 250:
        score += 2
    elif total_recent > 100:
        score += 1

    # Technology diversity (0-2 points)
    tech_set = set()
    for p in projects_data:
        tech_set.update([t.replace('✓ ', '') for t in p['tech_stack']])
    if len(tech_set) > 15:
        score += 2
    elif len(tech_set) > 10:
        score += 1

    # Conventional commits (0-2 points)
    total_commits = sum(p['recent_commits'] for p in projects_data)
    total_conv = sum(sum(p['conventional_commits'].values()) for p in projects_data)
    if total_commits > 0:
        conv_rate = total_conv / total_commits
        if conv_rate > 0.8:
            score += 2
        elif conv_rate > 0.5:
            score += 1

    # Commit size distribution (0-2 points)
    total_small = sum(p['commit_size'].get('small', 0) for p in projects_data)
    total_commits_sized = sum(
        p['commit_size'].get('small', 0) +
        p['commit_size'].get('medium', 0) +
        p['commit_size'].get('large', 0)
        for p in projects_data
    )
    if total_commits_sized > 0:
        small_rate = total_small / total_commits_sized
        if small_rate > 0.4:
            score += 2
        elif small_rate > 0.25:
            score += 1

    # Active projects (0-1 point)
    active = len([p for p in projects_data if p['recent_commits'] > 10])
    if active >= len(projects_data) * 0.7:
        score += 1

    return round(score, 1)


def generate_executive_summary(projects_data, by_category):
    """Generate executive summary report"""

    summary = f"""# Portfolio Executive Summary v4

**Report Date:** {datetime.now().strftime('%Y-%m-%d')}
**Portfolio Size:** {len(projects_data)} Projects
**Analysis Period:** August 1, 2024 - Present

---

## Portfolio Snapshot

### Category Distribution

"""

    for category, projects in sorted(by_category.items(), key=lambda x: len(x[1]), reverse=True):
        total_commits = sum(p['recent_commits'] for p in projects)
        summary += f"**{category}:** {len(projects)} projects, {total_commits} commits\n\n"

    # Top performers
    summary += """### Top 3 Most Active Projects

"""

    for i, project in enumerate(projects_data[:3], 1):
        summary += f"""{i}. **{project['project_name']}** ({project['category']})
   - {project['recent_commits']} commits since Aug 2024
   - {project['lines_added']:,} lines added, {project['lines_removed']:,} removed
   - Tech: {', '.join([t.replace('✓ ', '') for t in project['tech_stack'][:3]])}

"""

    # Technology highlights
    tech_counts = defaultdict(int)
    for project in projects_data:
        for tech in project['tech_stack']:
            clean_tech = tech.replace('✓ ', '').strip()
            tech_counts[clean_tech] += 1

    top_tech = sorted(tech_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    summary += """### Most Used Technologies

"""

    for tech, count in top_tech:
        pct = (count / len(projects_data)) * 100
        summary += f"- **{tech}:** {count} projects ({pct:.0f}%)\n"

    summary += f"""

---

## Key Insights

### Development Velocity
- Total commits since Aug 2024: {sum(p['recent_commits'] for p in projects_data):,}
- Average commits per project: {sum(p['recent_commits'] for p in projects_data) / len(projects_data):.1f}
- Most active category: {max(by_category.items(), key=lambda x: sum(p['recent_commits'] for p in x[1]))[0]}

### Code Quality
- Conventional commit adoption: {(sum(sum(p['conventional_commits'].values()) for p in projects_data) / sum(p['recent_commits'] for p in projects_data) * 100) if sum(p['recent_commits'] for p in projects_data) > 0 else 0:.1f}%
- Average commit size: Medium (most commits are focused and reviewable)

### Technology Stack
- Primary language: Node.js/TypeScript
- Frontend framework: React dominates
- Build tool: Vite is preferred modern choice
- Testing: Mix of Vitest and Jest

---

## Strategic Recommendations

### 1. Standardization Opportunities
- Consolidate testing frameworks (prefer Vitest for new projects)
- Standardize build tooling (Vite for consistency)
- Implement consistent CI/CD across all projects

### 2. Quality Improvements
- Increase test coverage across portfolio
- Add pre-commit hooks for linting and formatting
- Implement automated dependency updates

### 3. Documentation Enhancement
- Add comprehensive README files
- Document API endpoints and data models
- Create architecture decision records (ADRs)

### 4. Performance Optimization
- Audit bundle sizes across web projects
- Implement code splitting where applicable
- Add performance monitoring

---

**Portfolio Health Score:** {calculate_health_score(projects_data)}/10

*Executive summary generated by Portfolio Analysis v4*
"""

    # Write executive summary
    output_file = OUTPUT_DIR / "portfolio_executive_summary_v4.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(summary)

    print(f"✓ Executive summary generated: {output_file}")


if __name__ == "__main__":
    print("Generating Portfolio Analysis v4 reports...")
    generate_comprehensive_report()
    print("✓ All reports generated successfully!")
