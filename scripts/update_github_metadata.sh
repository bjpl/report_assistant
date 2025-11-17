#!/bin/bash

# GitHub Repository Metadata Update Script
# Updates repository descriptions and homepage URLs for all projects with live sites
# Run this script after authenticating with: gh auth login

set -e

echo "Updating GitHub repository metadata for 12 repositories with live sites..."
echo ""

# 1. aves
echo "Updating aves..."
gh repo edit bjpl/aves \
  --description "Visual Spanish bird learning platform with AI-powered annotations using GPT-4 Vision API and interactive workspace architecture" \
  --homepage "https://bjpl.github.io/aves/"

# 2. california_puzzle_game
echo "Updating california_puzzle_game..."
gh repo edit bjpl/california_puzzle_game \
  --description "Interactive California geography learning game with D3.js visualization, PWA architecture, and comprehensive test coverage" \
  --homepage "https://bjpl.github.io/california_puzzle_game/"

# 3. colombia_department_puzzle
echo "Updating colombia_department_puzzle..."
gh repo edit bjpl/colombia_department_puzzle \
  --description "Educational Colombian geography puzzle game demonstrating SPARC methodology and D3-geo projection techniques" \
  --homepage "https://bjpl.github.io/colombia_department_puzzle"

# 4. describe_it
echo "Updating describe_it..."
gh repo edit bjpl/describe_it \
  --description "Full-stack Spanish learning application with AI-powered image descriptions using Next.js 15.5, GPT-4 Vision, and multi-style generation" \
  --homepage "https://describe-it.vercel.app/"

# 5. fancy_monkey
echo "Updating fancy_monkey..."
gh repo edit bjpl/fancy_monkey \
  --description "Zero-cost e-commerce platform with GitHub Pages frontend, Vercel serverless checkout, and Stripe payment integration including mobile wallets" \
  --homepage "https://fancymonkey.shop"

# 6. Internet-Infrastructure-Map
echo "Updating Internet-Infrastructure-Map..."
gh repo edit bjpl/Internet-Infrastructure-Map \
  --description "3D visualization of global internet infrastructure using Three.js with live data integration and intelligent fallback mechanisms" \
  --homepage "https://bjpl.github.io/Internet-Infrastructure-Map/"

# 7. letratos
echo "Updating letratos..."
gh repo edit bjpl/letratos \
  --description "Bilingual poetry and photography portfolio with Jekyll static site generation and token-based design system" \
  --homepage "https://bjpl.github.io/letratos/"

# 8. online_language_learning_resources
echo "Updating online_language_learning_resources..."
gh repo edit bjpl/online_language_learning_resources \
  --description "Modern web-based language learning resource platform built with Vite, featuring comprehensive testing and accessibility features" \
  --homepage "https://bjpl.github.io/online_language_learning_resources/"

# 9. sinonimos_de_caminar
echo "Updating sinonimos_de_caminar..."
gh repo edit bjpl/sinonimos_de_caminar \
  --description "Spanish synonym learning tool for 'caminar' with 56 audio files featuring 8 Latin American voices and interactive exploration" \
  --homepage "https://bjpl.github.io/sinonimos_de_caminar/"

# 10. sinonimos_de_comer
echo "Updating sinonimos_de_comer..."
gh repo edit bjpl/sinonimos_de_comer \
  --description "Spanish synonym learning tool for 'comer' with literary narrative system and earth-tones design language" \
  --homepage "https://bjpl.github.io/sinonimos_de_comer/"

# 11. sinonimos_de_hablar
echo "Updating sinonimos_de_hablar..."
gh repo edit bjpl/sinonimos_de_hablar \
  --description "Spanish synonym learning tool for 'hablar' with interactive card interface and regional usage notes" \
  --homepage "https://bjpl.github.io/sinonimos_de_hablar/"

# 12. sinonimos_de_ver
echo "Updating sinonimos_de_ver..."
gh repo edit bjpl/sinonimos_de_ver \
  --description "Spanish synonym learning tool for 'ver' with full offline capability and curated photography from 15+ contributors" \
  --homepage "https://bjpl.github.io/sinonimos_de_ver/"

echo ""
echo "✅ All repository metadata updated successfully!"
