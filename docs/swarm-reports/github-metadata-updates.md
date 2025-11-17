# GitHub Repository Metadata Updates

**Generated:** 2025-11-17
**Purpose:** Update GitHub repository descriptions and homepage URLs for all projects with live sites

---

## Repositories to Update (12 Total)

### 1. aves
**Homepage URL:** https://bjpl.github.io/aves/
**Description:** Visual Spanish bird learning platform with AI-powered annotations using GPT-4 Vision API and interactive workspace architecture

### 2. california_puzzle_game
**Homepage URL:** https://bjpl.github.io/california_puzzle_game/
**Description:** Interactive California geography learning game with D3.js visualization, PWA architecture, and comprehensive test coverage

### 3. colombia_department_puzzle
**Homepage URL:** https://bjpl.github.io/colombia_department_puzzle
**Description:** Educational Colombian geography puzzle game demonstrating SPARC methodology and D3-geo projection techniques

### 4. describe_it
**Homepage URL:** https://describe-it.vercel.app/
**Description:** Full-stack Spanish learning application with AI-powered image descriptions using Next.js 15.5, GPT-4 Vision, and multi-style generation

### 5. fancy_monkey
**Homepage URL:** https://fancymonkey.shop
**Description:** Zero-cost e-commerce platform with GitHub Pages frontend, Vercel serverless checkout, and Stripe payment integration including mobile wallets

### 6. Internet-Infrastructure-Map
**Homepage URL:** https://bjpl.github.io/Internet-Infrastructure-Map/
**Description:** 3D visualization of global internet infrastructure using Three.js with live data integration and intelligent fallback mechanisms

### 7. letratos
**Homepage URL:** https://bjpl.github.io/letratos/
**Description:** Bilingual poetry and photography portfolio with Jekyll static site generation and token-based design system

### 8. online_language_learning_resources
**Homepage URL:** https://bjpl.github.io/online_language_learning_resources/
**Description:** Modern web-based language learning resource platform built with Vite, featuring comprehensive testing and accessibility features

### 9. sinonimos_de_caminar
**Homepage URL:** https://bjpl.github.io/sinonimos_de_caminar/
**Description:** Spanish synonym learning tool for 'caminar' with 56 audio files featuring 8 Latin American voices and interactive exploration

### 10. sinonimos_de_comer
**Homepage URL:** https://bjpl.github.io/sinonimos_de_comer/
**Description:** Spanish synonym learning tool for 'comer' with literary narrative system and earth-tones design language

### 11. sinonimos_de_hablar
**Homepage URL:** https://bjpl.github.io/sinonimos_de_hablar/
**Description:** Spanish synonym learning tool for 'hablar' with interactive card interface and regional usage notes

### 12. sinonimos_de_ver
**Homepage URL:** https://bjpl.github.io/sinonimos_de_ver/
**Description:** Spanish synonym learning tool for 'ver' with full offline capability and curated photography from 15+ contributors

---

## Update Instructions

### Option 1: Using the Script (Recommended)

```bash
# Ensure GitHub CLI is authenticated
gh auth login

# Run the update script
bash scripts/update_github_metadata.sh
```

### Option 2: Manual Updates via GitHub Web Interface

For each repository:
1. Navigate to https://github.com/bjpl/[repo-name]/settings
2. Update "Description" field with the description above
3. Update "Website" field with the homepage URL above
4. Click "Save changes"

### Option 3: Individual Commands

```bash
gh repo edit bjpl/[repo-name] --description "[description]" --homepage "[url]"
```

---

## Description Guidelines

All descriptions follow these standards:

1. **Professional Neutral Tone:** Technical accuracy without casual language
2. **Key Technologies Highlighted:** Specific frameworks and tools mentioned
3. **Project Value Stated:** What the project demonstrates or achieves
4. **Concise Length:** 60-120 characters for optimal GitHub display
5. **Searchable Keywords:** Relevant technical terms included

---

## Benefits

### For Portfolio Presentation
- Clear project purpose visible on GitHub profile
- Live demo links directly accessible from repository page
- Professional, consistent descriptions across all projects

### For Technical Recruiters
- Immediate understanding of technical capabilities
- Quick access to live demonstrations
- Clear categorization of project types

### For SEO and Discoverability
- Relevant keywords improve GitHub search results
- Homepage URLs establish project credibility
- Consistent metadata improves profile professionalism

---

## Verification

After updates, verify at: https://github.com/bjpl

Check that:
- Repository descriptions are visible and accurate
- Homepage URLs are clickable and functional
- All 12 repositories show consistent professional presentation
