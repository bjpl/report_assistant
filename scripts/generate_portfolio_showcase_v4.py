#!/usr/bin/env python3
"""
Portfolio Showcase Analysis v4 - Developer Versatility Report
Highlights breadth of capabilities and individual project excellence
"""

import os
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

BASE_DIR = Path("C:/Users/brand/Development/Project_Workspace/active-development")
RAW_DATA_DIR = BASE_DIR / "report_assistant/docs/git_raw_data_v4"
OUTPUT_DIR = BASE_DIR / "report_assistant/docs"


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

    except Exception as e:
        print(f"Error parsing {file_path}: {e}")

    return data


def generate_showcase_report():
    """Generate portfolio showcase report emphasizing versatility"""

    # Parse all raw data files
    projects_data = []
    for file_path in RAW_DATA_DIR.glob("*_v4.txt"):
        data = parse_raw_data(file_path)
        if data['project_name']:
            projects_data.append(data)

    # Sort by category then by commits
    projects_data.sort(key=lambda x: (x['category'], -x['recent_commits']))

    # Calculate totals
    total_commits = sum(p['recent_commits'] for p in projects_data)
    total_lines = sum(p['lines_added'] + p['lines_removed'] for p in projects_data)

    # Collect all unique technologies
    all_tech = set()
    for project in projects_data:
        all_tech.update([t.replace('✓ ', '').strip() for t in project['tech_stack']])

    # Group by category
    by_category = defaultdict(list)
    for project in projects_data:
        by_category[project['category']].append(project)

    # Generate showcase report
    report = f"""# Portfolio Showcase Analysis v4: Developer Versatility & Breadth

**Developer:** Brandon Lambert
**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Analysis Period:** August 1, 2024 - Present
**Portfolio Objective:** Demonstrate versatility across diverse domains and technology stacks

---

## 🎯 Executive Summary: Technical Versatility Demonstrated

This portfolio showcases **{len(projects_data)} distinct projects** across **{len(by_category)} different domains**, demonstrating proficiency with **{len(all_tech)} technologies and frameworks**. Each project represents a different challenge, domain, and technology choice, highlighting adaptability and breadth of capabilities.

### Portfolio Highlights

| Metric | Value | Significance |
|--------|-------|--------------|
| **Project Domains** | {len(by_category)} | Diverse problem-solving across education, e-commerce, research, visualization |
| **Technology Stack Breadth** | {len(all_tech)} technologies | Full-stack versatility from Python to TypeScript, React to Ruby |
| **Total Development Activity** | {total_commits:,} commits | Substantial hands-on experience across all projects |
| **Code Volume** | {total_lines:,} lines | Large-scale implementation experience |
| **Project Types** | Frontend, Backend, Full-Stack, CLI, Data Analysis | Complete software lifecycle capabilities |

---

## 🌟 Core Competencies Demonstrated

### 1. Full-Stack Web Development
**Projects:** describe_it, hablas, aves, california_puzzle_game, colombia_puzzle_game
- Modern React applications with TypeScript
- Next.js for server-side rendering
- Vite for optimized build performance
- State management and responsive design

### 2. Python Development & Data Processing
**Projects:** video_gen, corporate_intel
- Large-scale data processing (9M+ lines of code)
- API development with FastAPI
- Automated content generation
- Docker containerization

### 3. E-commerce & Business Applications
**Project:** fancy_monkey
- E-commerce platform development
- Product management systems
- Transaction handling

### 4. Developer Tools & Automation
**Projects:** report_assistant, brandonjplambert
- CLI tool development
- Automated reporting systems
- Development workflow optimization
- Portfolio management tools

### 5. Language Learning Technology
**Projects:** aves, describe_it, hablas, subjunctive_practice
- Educational technology applications
- Interactive learning interfaces
- Content management for education
- Image annotation and review tools

### 6. Data Visualization & Interactive Media
**Projects:** internet, california_puzzle_game, colombia_puzzle_game
- 3D visualization with Three.js
- Interactive puzzle game mechanics
- Animation systems
- Canvas-based graphics

### 7. Ruby & Static Site Development
**Projects:** letratos, brandonjplambert
- Jekyll-based static sites
- Ruby scripting and automation
- Photography portfolio management
- Content organization systems

---

## 📊 Technology Breadth: Skills Matrix

### Languages Demonstrated

| Language | Projects | Use Cases | Proficiency Indicators |
|----------|----------|-----------|------------------------|
| **TypeScript** | 4 | Type-safe React apps, build tooling | Production applications with complex state |
| **JavaScript** | 9 | Frontend & Node.js backends | Full-stack implementations |
| **Python** | 2 | Data processing, API servers | Large-scale data handling (9M+ lines) |
| **Ruby** | 2 | Static sites, scripting | Jekyll site generators |

### Frontend Technologies

| Technology | Projects | Demonstrates |
|------------|----------|--------------|
| **React 18+** | 4 | Modern component architecture, hooks, performance optimization |
| **Next.js** | 2 | SSR/SSG, API routes, full-stack React applications |
| **Vite** | 4 | Modern build tooling, fast development experience |
| **Tailwind CSS** | 4 | Utility-first CSS, responsive design, rapid prototyping |
| **Three.js** | 1 | 3D graphics programming, WebGL visualization |

### Backend & Infrastructure

| Technology | Projects | Demonstrates |
|------------|----------|--------------|
| **Node.js/Express** | Multiple | RESTful API design, middleware, authentication |
| **FastAPI** | 1 | Modern Python APIs, async programming |
| **Docker** | 2 | Containerization, deployment automation |
| **PostgreSQL** | Multiple | Database design, SQL, data modeling |

### Testing & Quality

| Technology | Projects | Demonstrates |
|------------|----------|--------------|
| **Vitest** | 4 | Modern testing, unit/integration tests |
| **Jest** | 2 | Traditional testing frameworks |
| **Playwright** | Present | E2E testing capabilities |

---

## 🎨 Project Showcase: Individual Excellence

"""

    # Detailed project breakdowns by category
    for category, projects in sorted(by_category.items()):
        report += f"### {category}\n\n"

        for project in projects:
            report += f"#### {project['project_name']}\n\n"
            report += f"**Development Effort:** {project['recent_commits']} commits, "
            report += f"{project['lines_added']:,} lines added\n\n"

            # Technology showcase
            report += "**Technologies:**\n"
            for tech in project['tech_stack']:
                clean_tech = tech.replace('✓ ', '')
                report += f"- {clean_tech}\n"

            if not project['tech_stack']:
                report += "- Custom implementation\n"

            # Determine project type and highlight
            if 'React' in ' '.join(project['tech_stack']):
                report += "\n**Demonstrates:** Modern frontend development with React ecosystem\n"
            elif 'Python' in ' '.join(project['tech_stack']):
                report += "\n**Demonstrates:** Backend/data processing with Python\n"
            elif 'Ruby' in ' '.join(project['tech_stack']):
                report += "\n**Demonstrates:** Static site generation and Ruby scripting\n"

            # Commit breakdown
            if project['conventional_commits']:
                top_types = sorted(project['conventional_commits'].items(), key=lambda x: x[1], reverse=True)[:3]
                report += f"\n**Primary Activities:** {', '.join([f'{t[0]} ({t[1]})' for t in top_types])}\n"

            report += "\n---\n\n"

    report += f"""## 💪 Demonstrated Capabilities Summary

### Technical Breadth
- **{len(all_tech)} Different Technologies Mastered**
- **Frontend:** React, Next.js, Vite, Tailwind, Three.js
- **Backend:** Node.js, Python, FastAPI, Express
- **Databases:** PostgreSQL, data modeling
- **DevOps:** Docker, Docker Compose, CI/CD readiness
- **Testing:** Vitest, Jest, Playwright

### Domain Expertise Across Industries

"""

    for category in sorted(by_category.keys()):
        project_count = len(by_category[category])
        commit_count = sum(p['recent_commits'] for p in by_category[category])
        report += f"- **{category}:** {project_count} project{'s' if project_count > 1 else ''} ({commit_count} commits)\n"

    # Technology adoption matrix
    report += f"""

### Complete Technology Stack

"""

    tech_by_project = defaultdict(list)
    for project in projects_data:
        for tech in project['tech_stack']:
            clean_tech = tech.replace('✓ ', '').strip()
            tech_by_project[clean_tech].append(project['project_name'])

    for tech, project_list in sorted(tech_by_project.items(), key=lambda x: len(x[1]), reverse=True):
        report += f"**{tech}**\n"
        report += f"- Used in: {', '.join(project_list)}\n"
        report += f"- Demonstrates: {'Core competency' if len(project_list) >= 3 else 'Applied expertise'}\n\n"

    report += f"""---

## 🎯 Portfolio Strengths: What This Demonstrates

### 1. **Versatility Over Specialization**
Rather than deep specialization in a single stack, this portfolio demonstrates the ability to:
- Learn and master new technologies quickly
- Choose appropriate tools for each problem domain
- Work effectively across the entire stack
- Adapt to different project requirements

### 2. **Full Project Lifecycle Experience**
Each project represents complete ownership:
- **Planning:** Architecture decisions, technology selection
- **Implementation:** {total_commits:,} commits show hands-on development
- **Scale:** Projects ranging from small utilities to large applications
- **Completion:** All projects show sustained development through completion

### 3. **Problem Domain Diversity**
Not limited to a single industry or use case:
- **Education Technology:** Interactive learning tools
- **E-commerce:** Business applications
- **Data Processing:** Large-scale automation
- **Visualization:** Graphics and interactive media
- **Developer Tools:** Productivity and workflow automation
- **Research Tools:** Open-source analysis platforms

### 4. **Modern Development Practices**
Evidence of contemporary software engineering:
- Conventional commits for clear change history
- Component-based architecture in React projects
- Containerization with Docker
- Modern build tools (Vite, Next.js)
- TypeScript for type safety
- Testing frameworks integration

### 5. **Scale Handling**
Comfortable working at different scales:
- **Small projects:** utilities, tools ({project['recent_commits']} for report_assistant)
- **Medium projects:** interactive applications (112-146 commits)
- **Large projects:** video_gen with 454 commits, 9M+ lines processed

---

## 🚀 Career Value Proposition

### What This Portfolio Proves

1. **Fast Learner:** Successfully worked with {len(all_tech)}+ technologies
2. **Self-Directed:** Conceived, planned, and executed {len(projects_data)} independent projects
3. **Full-Stack:** Comfortable from database to UI to deployment
4. **Practical:** All projects serve real purposes (education, commerce, tools)
5. **Sustained Effort:** {total_commits:,} commits show consistent development discipline

### Ideal Roles
- **Full-Stack Developer:** Proven across frontend and backend
- **Technical Lead:** Experience making technology choices for diverse needs
- **Startup Engineer:** Can build entire products independently
- **Consulting:** Breadth to work across client stacks and domains
- **Team Polyglot:** Can work in any part of a codebase

### Differentiators
- **Range:** Not locked into one framework or language
- **Independence:** Complete projects from conception to delivery
- **Modern Stack:** Up-to-date with current best practices (React 18+, Vite, TypeScript)
- **Volume:** Significant code volume shows real implementation experience
- **Quality:** Use of testing, conventional commits, modern tooling

---

## 📈 Portfolio Metrics

### Commit Activity Distribution

| Category | Projects | Commits | % of Total |
|----------|----------|---------|------------|
"""

    for category in sorted(by_category.keys(), key=lambda c: sum(p['recent_commits'] for p in by_category[c]), reverse=True):
        cat_commits = sum(p['recent_commits'] for p in by_category[category])
        pct = (cat_commits / total_commits * 100) if total_commits > 0 else 0
        report += f"| {category} | {len(by_category[category])} | {cat_commits} | {pct:.1f}% |\n"

    report += f"""

### Development Velocity by Project Type

**High-Intensity Projects (200+ commits):**
"""

    high_intensity = [p for p in projects_data if p['recent_commits'] >= 200]
    for project in sorted(high_intensity, key=lambda x: x['recent_commits'], reverse=True):
        report += f"- {project['project_name']}: {project['recent_commits']} commits\n"

    report += f"""

**Medium-Intensity Projects (50-199 commits):**
"""

    medium_intensity = [p for p in projects_data if 50 <= p['recent_commits'] < 200]
    for project in sorted(medium_intensity, key=lambda x: x['recent_commits'], reverse=True):
        report += f"- {project['project_name']}: {project['recent_commits']} commits\n"

    report += f"""

**Focused Projects (<50 commits):**
"""

    focused = [p for p in projects_data if p['recent_commits'] < 50]
    for project in sorted(focused, key=lambda x: x['recent_commits'], reverse=True):
        report += f"- {project['project_name']}: {project['recent_commits']} commits\n"

    report += f"""

---

## 🎓 Learning & Growth Evidence

### Technology Adoption Curve
This portfolio shows progressive adoption of modern technologies:
- **Build Tools:** Migration to Vite (modern, fast) in 4 projects
- **Type Safety:** TypeScript in 4 projects shows maturity
- **Testing:** Vitest adoption in newer projects
- **Containerization:** Docker in production-ready projects

### Conventional Commit Adoption
Evidence of professional development practices:
- Total conventional commits: {sum(sum(p['conventional_commits'].values()) for p in projects_data)}
- Shows understanding of team development workflows
- Clear change documentation for future maintainability

---

## 💼 Portfolio Summary for Recruiters

**Name:** Brandon Lambert
**Portfolio Size:** {len(projects_data)} Projects
**Total Commits:** {total_commits:,}
**Technology Breadth:** {len(all_tech)} Technologies
**Domains Covered:** {len(by_category)}

**Top Skills Demonstrated:**
1. React/TypeScript Frontend Development
2. Node.js Backend Development
3. Python Data Processing & APIs
4. Full-Stack Application Architecture
5. Modern Build Tooling (Vite, Next.js)
6. Database Design (PostgreSQL)
7. Docker & Containerization
8. Testing & Quality Assurance

**Unique Value:**
- Generalist with proven ability to work across any stack
- Self-motivated with complete project ownership experience
- Modern technology adoption (React 18, Vite, TypeScript)
- Practical focus (all projects serve real purposes)
- Sustained development discipline ({total_commits:,} commits)

---

*Portfolio Showcase Analysis v4*
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*Focus: Individual project excellence and developer versatility*
"""

    # Write showcase report
    output_file = OUTPUT_DIR / "portfolio_showcase_v4.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✓ Portfolio showcase report generated: {output_file}")

    return projects_data, all_tech, by_category


def generate_executive_showcase():
    """Generate executive summary for portfolio showcase"""

    projects_data, all_tech, by_category = generate_showcase_report()

    total_commits = sum(p['recent_commits'] for p in projects_data)

    summary = f"""# Portfolio Executive Summary: Brandon Lambert

**Developer Profile:** Full-Stack Engineer with Breadth-First Expertise
**Report Date:** {datetime.now().strftime('%Y-%m-%d')}
**Portfolio URL:** [Your Portfolio URL]

---

## 🎯 At a Glance

A portfolio of **{len(projects_data)} independent projects** demonstrating versatility across **{len(all_tech)} technologies** and **{len(by_category)} domains**. Rather than specializing in a single stack, this portfolio showcases the ability to learn quickly, choose appropriate technologies, and deliver complete solutions across diverse problem spaces.

---

## 💼 What Makes This Portfolio Unique

### 1. Breadth Over Depth
Most developers specialize. This portfolio demonstrates:
- **{len(all_tech)} different technologies** mastered
- **{len(by_category)} distinct domains** (education, e-commerce, visualization, research)
- **Multiple languages:** TypeScript, JavaScript, Python, Ruby
- **Full-stack capabilities:** Frontend, backend, databases, DevOps

### 2. Complete Project Ownership
Each project shows end-to-end responsibility:
- Architecture decisions and technology selection
- Implementation from scratch
- {total_commits:,} total commits showing sustained effort
- Real-world applications, not tutorials

### 3. Modern Technology Stack
Up-to-date with current best practices:
- React 18+ for frontend
- TypeScript for type safety
- Vite for blazing-fast builds
- Next.js for production apps
- Docker for containerization
- Modern testing frameworks (Vitest, Jest)

---

## 🛠️ Technical Capabilities

### Frontend Development
**Projects:** describe_it, hablas, aves, california_puzzle_game, colombia_puzzle_game, internet

**Demonstrated Skills:**
- React with hooks and modern patterns
- TypeScript for type-safe applications
- Responsive design with Tailwind CSS
- State management
- 3D graphics with Three.js
- Performance optimization

### Backend Development
**Projects:** video_gen, corporate_intel, aves

**Demonstrated Skills:**
- Node.js/Express APIs
- Python with FastAPI
- RESTful API design
- Database design (PostgreSQL)
- Authentication systems
- Docker containerization

### Data Processing & Automation
**Projects:** video_gen, report_assistant, corporate_intel

**Demonstrated Skills:**
- Large-scale data processing (9M+ lines)
- Automated content generation
- CLI tool development
- Report generation systems
- Process automation

---

## 📊 Portfolio Statistics

| Metric | Value |
|--------|-------|
| **Total Projects** | {len(projects_data)} |
| **Project Domains** | {len(by_category)} |
| **Technologies Used** | {len(all_tech)} |
| **Total Commits** | {total_commits:,} |
| **Languages** | TypeScript, JavaScript, Python, Ruby |
| **Frameworks** | React, Next.js, Express, FastAPI |

---

## 🌟 Standout Projects

### 1. video_gen (Python Utility)
- **454 commits** - Highest activity project
- **9M+ lines processed** - Large-scale data handling
- Automated video content generation
- Demonstrates: Python mastery, automation, scale handling

### 2. california_puzzle_game (React/TypeScript)
- **278 commits** - Sustained development effort
- Interactive puzzle game with animations
- Vite + React + TypeScript stack
- Demonstrates: Frontend expertise, game mechanics, UX design

### 3. colombia_puzzle_game (React/TypeScript)
- **250 commits** - Complex implementation
- 13M+ lines changed - Major development effort
- Similar tech stack, different problem domain
- Demonstrates: Consistency, pattern application, scalability

### 4. brandonjplambert (Full-Stack)
- **238 commits** - Personal portfolio/tools
- Mix of Ruby and JavaScript
- Developer tools and automation
- Demonstrates: Meta-development, tool building

### 5. describe_it & hablas (Next.js)
- Language learning applications
- Full-stack Next.js implementations
- TypeScript + React + PostgreSQL
- Demonstrates: Educational tech, full-stack capability

---

## 🎯 Ideal Career Opportunities

### Best Fit Roles
1. **Full-Stack Engineer** - Proven across entire stack
2. **Technical Lead** - Experience making architecture decisions
3. **Startup Engineer** - Can build complete products independently
4. **Consulting Developer** - Breadth to work across client stacks
5. **Platform Engineer** - Experience with diverse systems

### Work Environments
- **Startups:** Versatility to wear multiple hats
- **Agencies:** Ability to work across client technologies
- **Product Companies:** Full-stack development capability
- **Consulting:** Breadth to work across projects

---

## 💪 Key Differentiators

### 1. Rapid Technology Adoption
- Successfully worked with {len(all_tech)} different technologies
- Comfortable learning new stacks as needed
- Modern technology choices (React 18+, Vite, TypeScript)

### 2. Independent Execution
- {len(projects_data)} complete projects from concept to code
- Self-directed architecture and technology decisions
- Sustained effort (avg {total_commits // len(projects_data)} commits per project)

### 3. Domain Versatility
- Not locked into single industry or use case
- {len(by_category)} different domains mastered
- Practical applications: education, commerce, visualization, tools

### 4. Production-Ready Code
- Testing frameworks integrated
- Conventional commits for maintainability
- Docker containerization
- Modern build tooling

---

## 🚀 What Employers Get

When hiring a developer with this portfolio, you get:

✅ **Versatility:** Can work in any part of your stack
✅ **Self-Sufficiency:** Proven ability to own projects end-to-end
✅ **Modern Skills:** Up-to-date with current best practices
✅ **Fast Learning:** Track record of mastering new technologies
✅ **Full-Stack:** Frontend, backend, database, deployment
✅ **Practical Focus:** All projects serve real purposes
✅ **Volume:** {total_commits:,} commits show serious development experience

---

## 📫 Contact & Links

**Portfolio:** [Your Portfolio URL]
**GitHub:** [Your GitHub]
**LinkedIn:** [Your LinkedIn]
**Email:** [Your Email]

---

*This portfolio represents {total_commits:,} commits across {len(projects_data)} projects, demonstrating sustained development capability and technical versatility.*

*Updated: {datetime.now().strftime('%Y-%m-%d')}*
"""

    # Write executive showcase
    output_file = OUTPUT_DIR / "portfolio_executive_showcase_v4.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(summary)

    print(f"✓ Executive showcase generated: {output_file}")


if __name__ == "__main__":
    print("Generating Portfolio Showcase v4 reports...")
    generate_executive_showcase()
    print("✓ All showcase reports generated successfully!")
