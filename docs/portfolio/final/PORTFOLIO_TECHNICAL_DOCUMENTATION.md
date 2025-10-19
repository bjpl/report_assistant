# Brandon Lambert - Technical Portfolio Documentation

**Date:** October 18, 2025
**Projects:** 13 Production Applications
**Primary Technologies:** TypeScript, JavaScript, Python, Ruby
**Development Period:** August 2024 - October 2025

---

## Portfolio Overview

This document provides technical documentation for 13 completed projects spanning web applications, data processing systems, educational software, and developer tools. Each project was developed independently with full ownership from conception through deployment.

### Development Statistics

- Total Commits: 2,137
- Lines of Code Modified: ~28.5 million
- Test Coverage Range: 79-95% where applicable
- Total Tests Written: ~3,000
- Documentation: ~27,000 words

---

## Project Descriptions

### 1. AVES - Spanish Learning Platform

**Technology Stack:** React 18, TypeScript, Express, PostgreSQL, GPT-4 Vision API

**Architecture:**
- Monorepo structure using npm workspaces
- Backend API with Express and TypeScript
- React frontend with TanStack Query for server state
- PostgreSQL database with Drizzle ORM
- GPT-4 Vision integration for image annotation

**Key Features:**
- Automatic bird feature annotation using computer vision
- Progressive vocabulary disclosure system (5 levels)
- Canvas-based interactive rendering
- Exercise generation using GPT-4
- Species taxonomy browser with filtering

**Testing:** 264 frontend tests, 57 E2E tests, 95% backend coverage

**Performance:** 2.8-4.4x improvement in development velocity using automated tools

---

### 2. VIDEO_GEN - Video Generation Pipeline

**Technology Stack:** Python 3.10+, FastAPI, FFmpeg, Edge-TTS, Claude API

**Architecture:**
- 7-stage processing pipeline
- Modular renderer system
- FastAPI web interface
- Command-line interface

**Input Methods:**
- Document processing
- YouTube transcript extraction
- Wizard-guided creation
- Programmatic API

**Capabilities:**
- 12 scene types (6 general, 6 educational)
- 4 voice options with Edge-TTS
- 28 language support
- GPU acceleration via NVIDIA NVENC

**Testing:** 474 passing tests, 79% code coverage

**Performance:** 2.25x speedup with parallel processing

---

### 3. CALIFORNIA_PUZZLE_GAME - Geography Learning Application

**Technology Stack:** React 18, TypeScript, Vite, D3.js, Tailwind CSS, Zustand, Supabase

**Features:**
- Interactive county map using D3.js
- Drag-and-drop interface with touch support
- Progressive Web App with offline functionality
- Dark mode with OLED optimization
- Authentication and data persistence via Supabase
- 4 difficulty levels

**Testing:** 1,792 tests with 100% pass rate

**Performance:** Lighthouse score 95+, WCAG AA compliant

**Bundle Size:** Optimized for mobile deployment

---

### 4. COLOMBIA_PUZZLE_GAME - Department Learning Application

**Technology Stack:** React 18, TypeScript, Vite, D3-geo, Tailwind CSS

**Features:**
- GeoJSON-based map of 33 departments
- Multiple game modes (complete, regional, timed)
- Progressive hint system
- Achievement tracking
- Educational content integration

**Testing:** 895 passing tests (89.9% pass rate)

**Performance:** ~137KB gzipped bundle, WCAG AAA compliant

---

### 5. CORPORATE_INTEL - Business Intelligence Platform

**Technology Stack:** Python 3.11+, FastAPI, PostgreSQL, TimescaleDB, Ray, Prefect, dbt

**Data Sources:**
- SEC EDGAR filings
- Yahoo Finance
- Alpha Vantage
- NewsAPI
- Crunchbase
- GitHub API

**Architecture:**
- Pluggable analysis engine using Strategy pattern
- Distributed processing with Ray
- Workflow orchestration via Prefect
- Time-series optimization with TimescaleDB
- Redis caching layer

**Testing:** 391 tests with 85% coverage

**Performance:** p99 latency <100ms with caching

**Monitoring:** OpenTelemetry, Prometheus, Grafana

---

### 6. OPEN_LEARN - Open Source Learning Platform

**Technology Stack:** Docker, Docker Compose, Node.js

**Development:** 41 commits, 253,257 lines modified

**Features:**
- Containerized deployment architecture
- Multi-service orchestration
- Educational content management
- Open source learning resources

**Infrastructure:**
- Docker Compose for service orchestration
- Scalable microservices architecture
- Environment-based configuration

---

### 7. DESCRIBE_IT - Visual Content Description System

**Technology Stack:** Next.js 14, TypeScript, React 19, Supabase, GPT-4, Vercel KV

**Features:**
- 5 description styles using GPT-4
- Real-time collaboration via WebSockets
- Interactive Q&A system
- Smart phrase extraction
- Session management with progress tracking
- Unsplash API integration

**Caching:** Multi-layer strategy with Vercel KV (Redis)

**Security:** JWT authentication, OAuth, Row Level Security

---

### 8. HABLAS.CO - Language Learning for Gig Workers

**Technology Stack:** Next.js 15, TypeScript, React 18, Claude API, Upstash Redis

**Target Audience:** Colombian gig economy workers

**Features:**
- WhatsApp community integration
- Offline-first architecture
- Job-specific vocabulary
- Data conservation features
- Mobile-optimized interface

**Content:** 50+ resources generated using Claude API

**Performance:** Optimized for 3G networks and budget devices

---

### 9. ONLINE_LANGUAGE_LEARNING_RESOURCES - Resource Aggregation Platform

**Technology Stack:** Vite, JavaScript, Tailwind CSS, HTML5, Vitest

**Coverage:** 67 languages

**Resource Types:**
- Applications
- Books
- Podcasts
- Courses
- Communities

**Features:**
- Search and filter system
- Mobile-first responsive design
- Accessibility features (WCAG 2.1 AAA)
- Performance optimization (98% load time improvement)

**Testing:** 50 tests with 100% pass rate

**Development:** 198 commits, 402,547 lines modified

---

### 10. BRANDONJPLAMBERT - Portfolio Website

**Technology Stack:** Jekyll 4.3, Ruby, Liquid, Sveltia CMS

**Features:**
- Git-based CMS
- Bilingual support (English/Spanish)
- 8px grid design system
- SEO optimization
- Academic content focus

**Performance:** Lighthouse score 95+, WCAG AAA compliant

**Development:** 238 commits

---

### 11. INTERNET - Infrastructure Visualization

**Technology Stack:** Three.js, Globe.GL, React, TypeScript, Vite

**Data Sources:**
- TeleGeography
- PeeringDB
- Cloudflare Radar

**Visualization:**
- 100+ submarine cables
- 500+ data centers
- Real-time data updates
- 60 FPS WebGL rendering

**Features:**
- Educational content integration
- Fallback data strategies
- Interactive navigation

**Development:** 8 commits focused on core functionality

---

### 12. LETRATOS - Creative Portfolio

**Technology Stack:** Jekyll 4.3, Ruby, SASS/SCSS

**Content:**
- Poetry collections (bilingual)
- 8 photography galleries

**Design:**
- 38 design tokens
- Responsive 320px-1920px
- WCAG 2.1 AA compliance

**Development:** 122 commits

---

### 13. REPORT_ASSISTANT - Documentation Automation

**Technology Stack:** Python, Node.js

**Purpose:** Automated report generation and portfolio analysis

**Features:**
- Git metrics extraction
- Daily report generation
- Multiple output formats
- Cross-platform compatibility

**Development:** 7 commits (tool recently created)

---

## Technology Summary

### Languages
- TypeScript: 8 projects
- JavaScript: 9 projects
- Python: 3 projects
- Ruby: 2 projects

### Frontend Frameworks
- React 18/19: 6 projects
- Next.js 14/15: 2 projects
- Vite: 5 projects
- Jekyll: 2 projects

### Backend Technologies
- Node.js/Express: 5 projects
- FastAPI: 2 projects
- PostgreSQL: 6 projects
- Docker: 3 projects

### AI/ML Integration
- GPT-4: 3 projects
- Claude API: 2 projects
- GPT-4 Vision: 1 project

### Testing Frameworks
- Vitest: 4 projects
- Jest: 2 projects
- Playwright: 2 projects
- pytest: 3 projects

---

## Quality Metrics

### Code Coverage
- Range: 79-95% where measured
- Total tests: ~3,000
- Largest test suite: 1,792 tests (California Puzzle)

### Performance
- Web applications: Lighthouse scores 95+
- API response times: p99 <100ms where measured
- Bundle sizes: Optimized for mobile (e.g., 137KB for Colombia Puzzle)

### Accessibility
- WCAG compliance levels achieved: AA to AAA
- Mobile optimization in all web projects
- Offline functionality where applicable

---

## Deployment Platforms

- GitHub Pages: 4 projects
- Vercel: 2 projects
- Docker: 3 projects
- Local/Self-hosted: Various

---

## Documentation

Total documentation across projects: ~27,000 words including:
- API documentation
- Setup guides
- Architecture decisions
- User guides
- Technical specifications

---

*End of Technical Documentation*