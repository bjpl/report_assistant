#!/bin/bash

# GitHub Repository Description Update Script
# Generated: 2025-11-11
# Purpose: Update GitHub repository descriptions for all 25 projects (excluding close_reading)
# Requires: gh CLI authenticated (run: gh auth login)

set -e  # Exit on error

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================"
echo "GitHub Description Update Script"
echo "========================================"
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}Error: GitHub CLI (gh) is not installed${NC}"
    echo "Install: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${YELLOW}Warning: Not authenticated with GitHub CLI${NC}"
    echo "Please run: gh auth login"
    exit 1
fi

echo -e "${GREEN}GitHub CLI is authenticated and ready${NC}"
echo ""

# Counter for success/failure
SUCCESS_COUNT=0
FAIL_COUNT=0

# Function to update a repository description
update_repo() {
    local repo=$1
    local description=$2

    echo "Updating: $repo"
    if gh repo edit "$repo" --description "$description" 2>&1; then
        echo -e "${GREEN}✓ Success${NC}"
        ((SUCCESS_COUNT++))
    else
        echo -e "${RED}✗ Failed${NC}"
        ((FAIL_COUNT++))
    fi
    echo ""
}

# ==============================================
# PROJECTS WITH DESCRIPTIONS (19 projects)
# ==============================================

update_repo "bjpl/agentic_learning" \
    "Revolutionary autodidactic learning system powered by AI agent orchestration and consciousness evolution paradigms."

update_repo "bjpl/algorithms_and_data_structures" \
    "Interactive learning platform teaching algorithms through intuitive everyday analogies and interactive CLI experiences."

update_repo "bjpl/aves" \
    "AI-powered inductive learning platform for Spanish ornithological vocabulary acquisition through interactive photography."

update_repo "bjpl/brandonjplambert" \
    "Sophisticated academic portfolio and educational resource platform built with Jekyll 4.3+, featuring bilingual support and Sveltia CMS."

update_repo "bjpl/california_puzzle_game" \
    "Interactive educational puzzle game for learning California geography with D3.js visualizations and React."

update_repo "bjpl/colombia_department_puzzle" \
    "Interactive educational puzzle game to learn all 33 departments of Colombia through engaging drag-and-drop gameplay."

update_repo "bjpl/corporate_intel" \
    "Production-hardened business intelligence platform that aggregates corporate financial data through automated API integrations for EdTech ecosystem analysis."

update_repo "bjpl/deployment_sprint" \
    "Strategic deployment planning and progress tracking for 6 concurrent projects with comprehensive documentation."

update_repo "bjpl/describe_it" \
    "Comprehensive Next.js 14 app combining visual learning with AI-powered language education for learning Spanish through interactive image descriptions."

update_repo "bjpl/fancy_monkey" \
    "People Clothes e-commerce platform with zero hosting costs using GitHub Pages, Stripe, and Vercel serverless functions."

update_repo "bjpl/hablas" \
    "English Learning Hub for Colombian workers - mobile-first web app connecting delivery drivers and rideshare workers to practical English resources through WhatsApp."

update_repo "bjpl/Internet-Infrastructure-Map" \
    "Educational 3D visualization of global internet infrastructure with live data, intelligent fallbacks, and integrated knowledge base."

update_repo "bjpl/learn_claude_flow" \
    "Interactive React-based learning tool for Claude Flow documentation with integrated PDF viewer, advanced search, and bookmark features."

update_repo "bjpl/learn_comptia_network_plus" \
    "Interactive web-based learning platform for mastering CompTIA Network+ N10-009 certification through hands-on practice and scenario-based learning."

update_repo "bjpl/learn_my_system" \
    "ThinkPad P16v system documentation with automated hardware data collection, comprehensive dashboard, and real-time monitoring."

update_repo "bjpl/learning_voice_agent" \
    "AI-powered voice conversation system for capturing and developing learning insights. Built with FastAPI, Claude Haiku, and modern web technologies."

update_repo "bjpl/letratos" \
    "Static-generated bilingual poetry and photography portfolio built with Jekyll 4.3.0, featuring Spanish/English collections with responsive galleries."

update_repo "bjpl/online_language_learning_resources" \
    "Beautifully crafted modern website curating the best language learning resources from around the web for polyglots and language enthusiasts worldwide."

update_repo "bjpl/open_learn_co" \
    "Colombian Open Data Intelligence Platform aggregating, analyzing, and providing insights from Colombian open data sources, news media, and government APIs."

update_repo "bjpl/sinonimos_de_caminar" \
    "Elegant and interactive collection of Spanish synonyms for the verb 'caminar' with multi-voice LATAM audio, contextual images, and cultural notes."

update_repo "bjpl/sinonimos_de_hablar" \
    "Interactive educational web app exploring Spanish synonyms of 'hablar' with cultural notes, audio pronunciation, and example sentences for LATAM learners."

# ==============================================
# PROJECTS PENDING README GENERATION (4 projects)
# These will be updated once READMEs are generated
# ==============================================

# TODO: Uncomment and update once README is generated
# update_repo "bjpl/ai_stack_analysis" \
#     "[PLACEHOLDER - Waiting for README generation]"

# TODO: Uncomment and update once README is generated
# update_repo "bjpl/drive_reset" \
#     "[PLACEHOLDER - Waiting for README generation]"

# TODO: Uncomment and update once README is generated
# update_repo "bjpl/llms_on_my_system" \
#     "[PLACEHOLDER - Waiting for README generation]"

# TODO: Uncomment and update once README is generated
# update_repo "bjpl/report_assistant" \
#     "[PLACEHOLDER - Waiting for README generation]"

# TODO: Uncomment and update once README is generated
# update_repo "bjpl/learn_strudel" \
#     "[PLACEHOLDER - Waiting for README generation]"

# TODO: Uncomment and update once README is generated
# update_repo "bjpl/learning_agentic_engineering" \
#     "[PLACEHOLDER - Waiting for README generation]"

# ==============================================
# SUMMARY
# ==============================================

echo "========================================"
echo "Update Summary"
echo "========================================"
echo -e "${GREEN}Successful updates: $SUCCESS_COUNT${NC}"
echo -e "${RED}Failed updates: $FAIL_COUNT${NC}"
echo ""

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}All repository descriptions updated successfully!${NC}"
    exit 0
else
    echo -e "${YELLOW}Some updates failed. Please check the errors above.${NC}"
    exit 1
fi
