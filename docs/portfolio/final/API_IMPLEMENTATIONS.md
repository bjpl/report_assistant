# API Implementations Report

**Date:** October 18, 2025
**Projects with External APIs:** 8 projects
**Projects with Internal APIs:** 6 projects
**Total API Integrations:** 25+ external APIs, 6 internal REST APIs
**Coverage:** AI services, financial data, government data, analytics

---

## Overview

This document details all API implementations across the portfolio, including both external third-party API integrations and internal REST API development. The projects demonstrate proficiency with modern API architectures, authentication patterns, rate limiting, and production-grade error handling.

---

## Table of Contents

1. [Projects with External API Usage](#projects-with-external-api-usage)
2. [Projects with Internal API Implementation](#projects-with-internal-api-implementation)
3. [API Integration Patterns](#api-integration-patterns)
4. [Security & Authentication](#security--authentication)
5. [Rate Limiting & Error Handling](#rate-limiting--error-handling)

---

## Projects with External API Usage

### 1. AVES - Multi-AI Language Learning Platform

**External APIs Used:**
- **Anthropic Claude API** (Primary AI provider as of October 2025)
- **Unsplash API** (Image search)
- **Legacy: OpenAI GPT-4 Vision** (Deprecated, migrated to Claude)

**API Configuration:**
```typescript
// .env.example
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_MODEL=claude-sonnet-4-5-20250629
ANTHROPIC_MAX_TOKENS=4096
ANTHROPIC_TEMPERATURE=0.7

UNSPLASH_ACCESS_KEY=your_unsplash_key_here
UNSPLASH_SECRET_KEY=your_unsplash_secret_here

// Feature flags
ENABLE_VISION_AI=true
VISION_PROVIDER=claude
ENABLE_IMAGE_ANALYSIS=true
ENABLE_EXERCISE_GENERATION=true
```

**Claude API Implementation:**
```typescript
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

async function analyzeImage(imageUrl: string, prompt: string) {
  const response = await anthropic.messages.create({
    model: 'claude-sonnet-4-5-20250629',
    max_tokens: 4096,
    messages: [{
      role: 'user',
      content: [
        {
          type: 'image',
          source: {
            type: 'url',
            url: imageUrl
          }
        },
        {
          type: 'text',
          text: prompt
        }
      ]
    }]
  });

  return response.content[0].text;
}
```

**Unsplash API Implementation:**
```typescript
import { createApi } from 'unsplash-js';

const unsplash = createApi({
  accessKey: process.env.UNSPLASH_ACCESS_KEY
});

async function searchImages(query: string, perPage: number = 20) {
  const result = await unsplash.search.getPhotos({
    query,
    perPage,
    orientation: 'landscape'
  });

  return result.response?.results.map(photo => ({
    id: photo.id,
    url: photo.urls.regular,
    thumb: photo.urls.thumb,
    author: photo.user.name,
    downloadLocation: photo.links.download_location
  }));
}
```

**Rate Limiting:**
```typescript
// Rate limiting configuration
VISION_API_TIMEOUT=30000
VISION_API_MAX_RETRIES=3
VISION_API_RETRY_DELAY=1000
VISION_RATE_LIMIT_PER_MINUTE=20
```

**Migration Notes:**
- Migrated from OpenAI GPT-4 Vision to Claude Sonnet 4.5 on October 5, 2025
- Reason: Better multilingual support, improved accuracy for Spanish/English translation
- Cost reduction: 30% lower per-token cost with Claude
- Maintained backward compatibility during migration

---

### 2. DESCRIBE_IT - AI-Powered Image Description Generator

**External APIs Used:**
- **Anthropic Claude API** (Primary, migrated from OpenAI)
- **Supabase API** (Database, Auth, Real-time)
- **Unsplash API** (Image search)
- **Vercel KV** (Redis caching)

**API Configuration:**
```env
# Anthropic Claude (Primary)
ANTHROPIC_API_KEY=sk-ant-your-key
CLAUDE_MODEL=claude-sonnet-4-5-20250629
CLAUDE_MAX_TOKENS=8192
CLAUDE_TEMPERATURE=0.7

# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...

# Unsplash
NEXT_PUBLIC_UNSPLASH_ACCESS_KEY=your-key
UNSPLASH_ACCESS_KEY=your-key

# Vercel KV (Redis)
KV_REST_API_URL=your-kv-rest-api-url
KV_REST_API_TOKEN=your-kv-rest-api-token
```

**Claude API Integration:**
```typescript
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

export async function generateDescriptions(
  imageUrl: string,
  styles: string[]
) {
  const descriptions = {};

  for (const style of styles) {
    const prompt = getPromptForStyle(style);

    const response = await anthropic.messages.create({
      model: process.env.CLAUDE_MODEL,
      max_tokens: parseInt(process.env.CLAUDE_MAX_TOKENS),
      temperature: parseFloat(process.env.CLAUDE_TEMPERATURE),
      messages: [{
        role: 'user',
        content: [
          {
            type: 'image',
            source: { type: 'url', url: imageUrl }
          },
          {
            type: 'text',
            text: prompt
          }
        ]
      }]
    });

    descriptions[style] = response.content[0].text;
  }

  return descriptions;
}
```

**Supabase Real-time Integration:**
```typescript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(/* config */);

// Subscribe to real-time changes
const subscription = supabase
  .channel('session-updates')
  .on('postgres_changes', {
    event: '*',
    schema: 'public',
    table: 'sessions'
  }, (payload) => {
    console.log('Session updated:', payload);
    updateUI(payload.new);
  })
  .subscribe();
```

**Caching with Vercel KV:**
```typescript
import { kv } from '@vercel/kv';

async function getCachedDescription(imageId: string) {
  const cached = await kv.get(`description:${imageId}`);
  if (cached) return cached;

  const fresh = await generateDescriptions(imageUrl, styles);
  await kv.set(`description:${imageId}`, fresh, { ex: 3600 }); // 1 hour

  return fresh;
}
```

---

### 3. HABLAS - English Learning for Spanish Speakers

**External APIs Used:**
- **Anthropic Claude API** (Content generation)
- **Supabase API** (Optional, planned for future)

**API Configuration:**
```env
# Anthropic API
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Optional settings
AI_MODEL=claude-sonnet-4-5-20250929
AI_MAX_TOKENS=8000
AI_TEMPERATURE=0.7
```

**Content Generation with Claude:**
```typescript
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

async function generateLearningResource(
  topic: string,
  difficulty: 'beginner' | 'intermediate' | 'advanced',
  category: string
) {
  const prompt = `Generate an English learning resource for Spanish speakers.
Topic: ${topic}
Difficulty: ${difficulty}
Category: ${category}

Include:
1. Vocabulary (English-Spanish)
2. Example sentences
3. Pronunciation guide
4. Common mistakes
5. Practice exercises`;

  const response = await anthropic.messages.create({
    model: 'claude-sonnet-4-5-20250929',
    max_tokens: 8000,
    messages: [{
      role: 'user',
      content: prompt
    }]
  });

  return parseResourceContent(response.content[0].text);
}
```

**CLI Tool Usage:**
```bash
# Generate learning resources
npm run ai:generate-all
npm run ai:generate-essentials
npm run ai:generate-topic -- "Work & Employment"
npm run ai:generate-level -- intermediate
```

---

### 4. VIDEO_GEN - AI-Powered Video Generation

**External APIs Used:**
- **Anthropic Claude API** (AI narration, translation)
- **OpenAI API** (Alternative AI provider)
- **YouTube Data API v3** (Video search)

**API Configuration:**
```env
# Claude API (Primary)
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here

# OpenAI API (Alternative)
OPENAI_API_KEY=sk-your-openai-key-here

# YouTube Data API v3
YOUTUBE_API_KEY=your-youtube-api-key-here

# Translation settings
TRANSLATION_METHOD=claude
TRANSLATION_METHOD_OPTIONS=claude,google,openai
```

**Claude Translation Implementation:**
```python
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

async def translate_script(
    text: str,
    source_lang: str,
    target_lang: str
) -> str:
    """Translate video script using Claude API."""

    prompt = f"""Translate the following video script from {source_lang} to {target_lang}.
Maintain:
- Natural speaking tone
- Technical accuracy
- Cultural appropriateness
- Timing markers [00:00]

Text: {text}"""

    message = client.messages.create(
        model="claude-sonnet-4-5-20250629",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )

    return message.content[0].text
```

**YouTube API Integration:**
```python
from googleapiclient.discovery import build

youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))

def search_videos(query: str, max_results: int = 10):
    """Search for videos on YouTube."""

    request = youtube.search().list(
        part='snippet',
        q=query,
        type='video',
        maxResults=max_results,
        order='relevance'
    )

    response = request.execute()

    return [{
        'id': item['id']['videoId'],
        'title': item['snippet']['title'],
        'description': item['snippet']['description'],
        'thumbnail': item['snippet']['thumbnails']['high']['url'],
        'channel': item['snippet']['channelTitle'],
        'published': item['snippet']['publishedAt']
    } for item in response['items']]
```

**AI Narration Enhancement:**
```python
async def enhance_narration(script: str) -> str:
    """Enhance video narration with AI."""

    prompt = f"""Improve this video narration script:
- Make it more engaging
- Add transitions
- Improve pacing
- Maintain educational value

Script: {script}"""

    message = client.messages.create(
        model="claude-sonnet-4-5-20250629",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text
```

---

### 5. CORPORATE_INTEL - Business Intelligence Platform

**External APIs Used:**
- **Alpha Vantage API** (Stock market data)
- **SEC EDGAR API** (SEC filings)
- **yfinance** (Yahoo Finance data)
- **NewsAPI** (Financial news)
- **Crunchbase API** (Company data, optional)
- **GitHub API** (Repository analysis)

**API Configuration:**
```env
# Alpha Vantage (Stock data)
ALPHA_VANTAGE_API_KEY=your_key_here

# SEC EDGAR
SEC_USER_AGENT=Corporate Intel Platform/1.0 (your-email@example.com)
SEC_RATE_LIMIT=10

# NewsAPI
NEWSAPI_KEY=your_newsapi_key

# Crunchbase
CRUNCHBASE_API_KEY=your_crunchbase_key

# GitHub
GITHUB_TOKEN=your_github_token
```

**Alpha Vantage Integration:**
```python
import aiohttp
from alpha_vantage.timeseries import TimeSeries

class AlphaVantageConnector:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.ts = TimeSeries(key=api_key, output_format='pandas')
        self.base_url = 'https://www.alphavantage.co/query'

    async def get_stock_data(
        self,
        symbol: str,
        function: str = 'TIME_SERIES_DAILY',
        outputsize: str = 'compact'
    ) -> dict:
        """Fetch stock data from Alpha Vantage."""

        params = {
            'function': function,
            'symbol': symbol,
            'apikey': self.api_key,
            'outputsize': outputsize,
            'datatype': 'json'
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise AlphaVantageError(f"API error: {response.status}")

    async def get_company_overview(self, symbol: str) -> dict:
        """Get company fundamental data."""

        params = {
            'function': 'OVERVIEW',
            'symbol': symbol,
            'apikey': self.api_key
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                return await response.json()
```

**SEC EDGAR Integration:**
```python
import asyncio
import aiohttp
from datetime import datetime

class SECEdgarConnector:
    def __init__(self, user_agent: str, rate_limit: int = 10):
        self.user_agent = user_agent
        self.rate_limit = rate_limit
        self.base_url = 'https://data.sec.gov'
        self.headers = {'User-Agent': user_agent}
        self.semaphore = asyncio.Semaphore(rate_limit)

    async def get_company_filings(
        self,
        cik: str,
        filing_type: str = '10-K',
        count: int = 10
    ) -> list:
        """Fetch company filings from SEC EDGAR."""

        # Pad CIK to 10 digits
        cik = str(cik).zfill(10)

        url = f"{self.base_url}/submissions/CIK{cik}.json"

        async with self.semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        filings = data.get('filings', {}).get('recent', {})

                        # Filter by filing type
                        results = []
                        for i in range(len(filings.get('accessionNumber', []))):
                            if filings['form'][i] == filing_type:
                                results.append({
                                    'accession_number': filings['accessionNumber'][i],
                                    'filing_date': filings['filingDate'][i],
                                    'report_date': filings['reportDate'][i],
                                    'form_type': filings['form'][i],
                                    'file_number': filings['fileNumber'][i]
                                })

                                if len(results) >= count:
                                    break

                        return results
                    else:
                        raise SECAPIError(f"SEC API error: {response.status}")

            # Rate limiting: 10 requests per second
            await asyncio.sleep(1.0 / self.rate_limit)

    async def get_filing_document(self, accession_number: str, cik: str) -> str:
        """Download full filing document."""

        cik = str(cik).zfill(10)
        accession = accession_number.replace('-', '')

        url = f"{self.base_url}/Archives/edgar/data/{int(cik)}/{accession}/{accession_number}.txt"

        async with self.semaphore:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        raise SECAPIError(f"Document fetch error: {response.status}")
```

**Yahoo Finance Integration:**
```python
import yfinance as yf
import pandas as pd

class YahooFinanceConnector:
    def __init__(self):
        self.cache_duration = timedelta(hours=1)

    async def get_stock_info(self, ticker: str) -> dict:
        """Fetch stock information."""

        stock = yf.Ticker(ticker)
        info = stock.info

        return {
            'symbol': ticker,
            'name': info.get('longName'),
            'sector': info.get('sector'),
            'industry': info.get('industry'),
            'market_cap': info.get('marketCap'),
            'pe_ratio': info.get('forwardPE'),
            'dividend_yield': info.get('dividendYield'),
            'beta': info.get('beta'),
            'fifty_two_week_high': info.get('fiftyTwoWeekHigh'),
            'fifty_two_week_low': info.get('fiftyTwoWeekLow')
        }

    async def get_historical_data(
        self,
        ticker: str,
        period: str = '1y',
        interval: str = '1d'
    ) -> pd.DataFrame:
        """Fetch historical price data."""

        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval=interval)

        return hist

    async def get_earnings(self, ticker: str) -> pd.DataFrame:
        """Fetch earnings data."""

        stock = yf.Ticker(ticker)
        return stock.earnings
```

**Rate Limiting Strategy:**
```python
from dataclasses import dataclass
from datetime import datetime, timedelta
import asyncio

@dataclass
class RateLimiter:
    """Rate limiter for external API calls."""

    max_calls: int
    time_period: timedelta
    calls: list = field(default_factory=list)

    async def acquire(self):
        """Wait until a call can be made within rate limits."""

        now = datetime.now()

        # Remove old calls outside the time window
        self.calls = [
            call_time for call_time in self.calls
            if now - call_time < self.time_period
        ]

        # Wait if at limit
        if len(self.calls) >= self.max_calls:
            oldest_call = min(self.calls)
            wait_time = (oldest_call + self.time_period - now).total_seconds()

            if wait_time > 0:
                await asyncio.sleep(wait_time)
                return await self.acquire()

        self.calls.append(now)

# Usage
alpha_vantage_limiter = RateLimiter(
    max_calls=5,
    time_period=timedelta(minutes=1)
)

async with alpha_vantage_limiter.acquire():
    data = await alpha_vantage.get_stock_data('AAPL')
```

---

### 6. OPEN_LEARN - Colombian Intelligence Platform

**External APIs Used:**
- **DANE API** (National Statistics Department)
- **Banco de la República API** (Central Bank data)
- **SECOP API** (Public procurement)
- **Datos Abiertos** (Open Data Portal)
- **DNP API** (National Planning)
- **IDEAM API** (Weather and climate)

**API Configuration:**
```env
# Colombian Government APIs

# DANE (National Statistics)
DANE_API_KEY=your_dane_api_key
DANE_BASE_URL=https://www.dane.gov.co/api

# Banco de la República (Central Bank)
BANREP_BASE_URL=https://www.banrep.gov.co/api

# SECOP (Public Procurement)
SECOP_API_TOKEN=your_secop_token
SECOP_BASE_URL=https://www.colombiacompra.gov.co/api

# Datos Abiertos (Open Data)
DATOS_GOV_BASE_URL=https://www.datos.gov.co/api

# DNP (National Planning)
DNP_BASE_URL=https://www.dnp.gov.co/api

# IDEAM (Weather)
IDEAM_BASE_URL=https://www.ideam.gov.co/api
```

**Government API Integration:**
```python
import aiohttp
from typing import Dict, List, Optional

class ColombianGovernmentAPI:
    """Connector for Colombian government APIs."""

    def __init__(self):
        self.dane_key = os.getenv('DANE_API_KEY')
        self.secop_token = os.getenv('SECOP_API_TOKEN')
        self.headers = {
            'User-Agent': 'OpenLearn/1.0',
            'Accept': 'application/json'
        }

    async def get_dane_statistics(
        self,
        dataset: str,
        filters: Optional[Dict] = None
    ) -> Dict:
        """Fetch statistics from DANE."""

        url = f"{os.getenv('DANE_BASE_URL')}/datasets/{dataset}"
        params = {'api_key': self.dane_key}

        if filters:
            params.update(filters)

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise DANEAPIError(f"DANE API error: {response.status}")

    async def get_banrep_indicators(
        self,
        indicator: str,
        start_date: str,
        end_date: str
    ) -> List[Dict]:
        """Fetch economic indicators from Banco de la República."""

        url = f"{os.getenv('BANREP_BASE_URL')}/indicators/{indicator}"
        params = {
            'start_date': start_date,
            'end_date': end_date,
            'format': 'json'
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=self.headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('observations', [])
                else:
                    raise BanRepAPIError(f"BanRep API error: {response.status}")

    async def get_secop_contracts(
        self,
        entity: Optional[str] = None,
        year: Optional[int] = None,
        min_amount: Optional[float] = None
    ) -> List[Dict]:
        """Fetch public procurement contracts from SECOP."""

        url = f"{os.getenv('SECOP_BASE_URL')}/contracts"
        params = {
            'token': self.secop_token,
            'format': 'json'
        }

        if entity:
            params['entity'] = entity
        if year:
            params['year'] = year
        if min_amount:
            params['min_amount'] = min_amount

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=self.headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('contracts', [])
                else:
                    raise SECOPAPIError(f"SECOP API error: {response.status}")
```

---

### 7. CALIFORNIA_PUZZLE_GAME - Optional Cloud Sync

**External APIs Used:**
- **Supabase API** (Optional - Auth, database, real-time)

**API Configuration:**
```env
# Optional Supabase configuration
VITE_SUPABASE_URL=https://project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
VITE_SUPABASE_SYNC_ENABLED=true
VITE_SUPABASE_SYNC_INTERVAL=30000
VITE_SUPABASE_REALTIME_ENABLED=false
```

**Implementation:**
```typescript
import { createClient } from '@supabase/supabase-js';

const supabase = import.meta.env.VITE_SUPABASE_URL
  ? createClient(
      import.meta.env.VITE_SUPABASE_URL,
      import.meta.env.VITE_SUPABASE_ANON_KEY
    )
  : null;

// Optional sync - game works without Supabase
async function syncGameProgress(gameState: GameState) {
  if (!supabase || !import.meta.env.VITE_SUPABASE_SYNC_ENABLED) {
    // Fall back to local storage
    localStorage.setItem('game_state', JSON.stringify(gameState));
    return;
  }

  const { data: { user } } = await supabase.auth.getUser();

  if (!user) {
    localStorage.setItem('game_state', JSON.stringify(gameState));
    return;
  }

  // Sync to Supabase
  await supabase
    .from('game_progress')
    .upsert({
      user_id: user.id,
      state: gameState,
      updated_at: new Date().toISOString()
    });
}
```

---

### 8. COLOMBIA_PUZZLE_GAME - Analytics & Error Tracking

**External APIs Used:**
- **Supabase API** (Auth, database)
- **Google Analytics 4** (Analytics)
- **Sentry** (Error tracking, performance monitoring)

**API Configuration:**
```env
# Google Analytics 4
VITE_GA_MEASUREMENT_ID=G-XXXXXXXXXX
VITE_GA_ENABLED=true

# Sentry
VITE_SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/xxx
VITE_SENTRY_ENABLED=true
VITE_SENTRY_ENVIRONMENT=production
VITE_SENTRY_TRACES_SAMPLE_RATE=0.1
VITE_SENTRY_REPLAYS_SESSION_SAMPLE_RATE=0.1
VITE_SENTRY_REPLAYS_ON_ERROR_SAMPLE_RATE=1.0

# Supabase
VITE_SUPABASE_URL=https://project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
```

**Google Analytics Integration:**
```typescript
import ReactGA from 'react-ga4';

// Initialize GA4
if (import.meta.env.VITE_GA_ENABLED === 'true') {
  ReactGA.initialize(import.meta.env.VITE_GA_MEASUREMENT_ID);
}

// Track page views
function trackPageView(path: string) {
  ReactGA.send({ hitType: 'pageview', page: path });
}

// Track events
function trackEvent(category: string, action: string, label?: string) {
  ReactGA.event({
    category,
    action,
    label
  });
}

// Track game events
trackEvent('Game', 'department_placed', 'Antioquia');
trackEvent('Game', 'puzzle_completed', `time:${completionTime}ms`);
```

**Sentry Integration:**
```typescript
import * as Sentry from '@sentry/react';
import { BrowserTracing } from '@sentry/tracing';

if (import.meta.env.VITE_SENTRY_ENABLED === 'true') {
  Sentry.init({
    dsn: import.meta.env.VITE_SENTRY_DSN,
    environment: import.meta.env.VITE_SENTRY_ENVIRONMENT,
    integrations: [
      new BrowserTracing(),
      new Sentry.Replay()
    ],
    tracesSampleRate: parseFloat(import.meta.env.VITE_SENTRY_TRACES_SAMPLE_RATE),
    replaysSessionSampleRate: parseFloat(import.meta.env.VITE_SENTRY_REPLAYS_SESSION_SAMPLE_RATE),
    replaysOnErrorSampleRate: parseFloat(import.meta.env.VITE_SENTRY_REPLAYS_ON_ERROR_SAMPLE_RATE)
  });
}

// Error handling
try {
  // Game logic
} catch (error) {
  Sentry.captureException(error);
  throw error;
}
```

---

## Projects with Internal API Implementation

### 1. AVES - Express.js REST API

**API Framework:** Express.js + TypeScript + Drizzle ORM

**API Routes (9 endpoints):**
```
POST   /api/auth/register          - User registration
POST   /api/auth/login             - User login
POST   /api/auth/logout            - User logout

GET    /api/vocabulary             - List vocabulary
POST   /api/vocabulary             - Create vocabulary
PUT    /api/vocabulary/:id         - Update vocabulary
DELETE /api/vocabulary/:id         - Delete vocabulary

GET    /api/exercises              - List exercises
POST   /api/exercises              - Create exercise
POST   /api/exercises/:id/submit   - Submit answer

GET    /api/annotations            - List annotations
POST   /api/annotations            - Create annotation
PUT    /api/annotations/:id        - Update annotation

POST   /api/ai/annotations         - Generate annotations (Claude)
POST   /api/ai/exercises           - Generate exercises (Claude)

GET    /api/images/search          - Search images (Unsplash)

GET    /api/species                - List bird species
GET    /api/species/:id            - Get species details

POST   /api/batch/process          - Batch operations
```

**API Implementation:**
```typescript
import express from 'express';
import { z } from 'zod';
import { db } from '../db';

const router = express.Router();

// Validation schema
const vocabularySchema = z.object({
  term: z.string().min(1).max(255),
  definition: z.string(),
  etymology: z.string().optional(),
  difficulty: z.number().int().min(1).max(5),
  category: z.string()
});

// Create vocabulary
router.post('/vocabulary', requireAuth, async (req, res) => {
  try {
    const validated = vocabularySchema.parse(req.body);

    const [newVocab] = await db
      .insert(vocabulary)
      .values({
        ...validated,
        user_id: req.session.userId
      })
      .returning();

    res.status(201).json(newVocab);
  } catch (error) {
    if (error instanceof z.ZodError) {
      res.status(400).json({ errors: error.errors });
    } else {
      res.status(500).json({ error: 'Internal server error' });
    }
  }
});

// Get vocabulary list
router.get('/vocabulary', requireAuth, async (req, res) => {
  const { category, difficulty, search } = req.query;

  let query = db
    .select()
    .from(vocabulary)
    .where(eq(vocabulary.user_id, req.session.userId));

  if (category) {
    query = query.where(eq(vocabulary.category, category));
  }

  if (difficulty) {
    query = query.where(eq(vocabulary.difficulty, parseInt(difficulty)));
  }

  if (search) {
    query = query.where(
      or(
        like(vocabulary.term, `%${search}%`),
        like(vocabulary.definition, `%${search}%`)
      )
    );
  }

  const results = await query.orderBy(vocabulary.created_at);
  res.json(results);
});
```

**API Error Handling:**
```typescript
// Global error handler
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error(err.stack);

  if (err instanceof z.ZodError) {
    return res.status(400).json({
      error: 'Validation failed',
      details: err.errors
    });
  }

  if (err.name === 'UnauthorizedError') {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  res.status(500).json({ error: 'Internal server error' });
});
```

---

### 2. DESCRIBE_IT - Next.js API Routes

**API Framework:** Next.js 14 App Router API Routes

**API Routes (20+ endpoints):**
```
POST   /api/descriptions          - Generate descriptions
GET    /api/descriptions/:id      - Get description
PUT    /api/descriptions/:id      - Update description
DELETE /api/descriptions/:id      - Delete description

POST   /api/sessions              - Create session
GET    /api/sessions              - List sessions
GET    /api/sessions/:id          - Get session
PUT    /api/sessions/:id          - Update session
DELETE /api/sessions/:id          - Delete session

POST   /api/qa                    - Submit question
GET    /api/qa/:sessionId         - Get Q&A history

POST   /api/phrases               - Extract phrases
GET    /api/phrases/:sessionId    - Get extracted phrases

GET    /api/search                - Search images (Unsplash)

POST   /api/export                - Export session data

GET    /api/health                - Health check
GET    /api/metrics               - API metrics
GET    /api/monitoring            - System monitoring

POST   /api/analytics             - Track analytics
GET    /api/progress              - User progress
PUT    /api/settings              - Update settings

GET    /api/admin/cache           - Cache management
POST   /api/admin/cache/clear     - Clear cache
```

**API Route Implementation:**
```typescript
// app/api/descriptions/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { createRouteHandlerClient } from '@supabase/auth-helpers-nextjs';
import { anthropic } from '@/lib/anthropic';

const descriptionSchema = z.object({
  imageUrl: z.string().url(),
  styles: z.array(z.enum([
    'concise',
    'detailed',
    'technical',
    'creative',
    'accessible'
  ])).min(1)
});

export async function POST(request: NextRequest) {
  try {
    // Authentication
    const supabase = createRouteHandlerClient({ cookies });
    const { data: { session } } = await supabase.auth.getSession();

    if (!session) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    // Validation
    const body = await request.json();
    const validated = descriptionSchema.parse(body);

    // Rate limiting check
    const rateLimitKey = `descriptions:${session.user.id}`;
    const requestCount = await checkRateLimit(rateLimitKey);

    if (requestCount > 50) {
      return NextResponse.json(
        { error: 'Rate limit exceeded' },
        { status: 429 }
      );
    }

    // Generate descriptions
    const descriptions = await generateDescriptions(
      validated.imageUrl,
      validated.styles
    );

    // Save to database
    const { data, error } = await supabase
      .from('descriptions')
      .insert({
        user_id: session.user.id,
        image_url: validated.imageUrl,
        descriptions,
        created_at: new Date().toISOString()
      })
      .select()
      .single();

    if (error) throw error;

    return NextResponse.json(data, { status: 201 });

  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Validation failed', details: error.errors },
        { status: 400 }
      );
    }

    console.error('Description generation error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function GET(request: NextRequest) {
  const supabase = createRouteHandlerClient({ cookies });
  const { data: { session } } = await supabase.auth.getSession();

  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const { searchParams } = new URL(request.url);
  const sessionId = searchParams.get('sessionId');

  const { data, error } = await supabase
    .from('descriptions')
    .select('*')
    .eq('user_id', session.user.id)
    .order('created_at', { ascending: false })
    .limit(50);

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }

  return NextResponse.json(data);
}
```

**Middleware for API Routes:**
```typescript
// middleware.ts
import { createMiddlewareClient } from '@supabase/auth-helpers-nextjs';
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function middleware(req: NextRequest) {
  const res = NextResponse.next();
  const supabase = createMiddlewareClient({ req, res });

  // Refresh session if expired
  await supabase.auth.getSession();

  // Protect API routes
  if (req.nextUrl.pathname.startsWith('/api/')) {
    const { data: { session } } = await supabase.auth.getSession();

    // Public endpoints
    const publicEndpoints = ['/api/health', '/api/auth'];
    const isPublic = publicEndpoints.some(endpoint =>
      req.nextUrl.pathname.startsWith(endpoint)
    );

    if (!session && !isPublic) {
      return NextResponse.json(
        { error: 'Authentication required' },
        { status: 401 }
      );
    }
  }

  return res;
}

export const config = {
  matcher: ['/api/:path*', '/dashboard/:path*']
};
```

---

### 3. HABLAS - Next.js API Routes

**API Framework:** Next.js 14 App Router

**API Routes:**
```
POST   /api/auth/[...nextauth]    - NextAuth.js authentication
POST   /api/analytics             - Track analytics
POST   /api/auth/signup           - User signup
POST   /api/auth/login            - User login
```

**NextAuth.js Configuration:**
```typescript
// app/api/auth/[...nextauth]/route.ts
import NextAuth, { NextAuthOptions } from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';

export const authOptions: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      name: 'Admin Credentials',
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" }
      },
      async authorize(credentials) {
        if (
          credentials?.email === process.env.ADMIN_EMAIL &&
          credentials?.password === process.env.ADMIN_PASSWORD
        ) {
          return {
            id: '1',
            email: process.env.ADMIN_EMAIL,
            name: 'Admin',
            role: 'admin'
          };
        }
        return null;
      }
    })
  ],
  pages: {
    signIn: '/admin/login',
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) token.role = user.role;
      return token;
    },
    async session({ session, token }) {
      if (session?.user) {
        session.user.role = token.role;
      }
      return session;
    }
  },
  session: {
    strategy: 'jwt',
    maxAge: 24 * 60 * 60
  }
};

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };
```

---

### 4. VIDEO_GEN - FastAPI REST API

**API Framework:** FastAPI + Python

**API Routes:**
```
POST   /api/generate              - Generate video
GET    /api/status/:job_id        - Check job status
GET    /api/jobs                  - List all jobs
DELETE /api/jobs/:job_id          - Cancel job

POST   /api/translate             - Translate script
POST   /api/narrate               - Generate narration

GET    /api/presets               - List presets
POST   /api/presets               - Create preset
PUT    /api/presets/:id           - Update preset
DELETE /api/presets/:id           - Delete preset

GET    /api/youtube/search        - Search YouTube videos

GET    /api/health                - Health check
GET    /api/metrics               - API metrics
```

**FastAPI Implementation:**
```python
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, validator
from typing import Optional, List
import uuid

app = FastAPI(
    title="Video Generation API",
    description="AI-powered video generation with multi-language support",
    version="2.0.0"
)

class VideoGenerationRequest(BaseModel):
    """Video generation request model."""

    title: str = Field(..., min_length=1, max_length=255)
    script: str = Field(..., min_length=1)
    language: str = Field(default="en", regex="^[a-z]{2}$")
    voice: str = Field(default="male")
    accent_color: str = Field(default="blue")
    resolution: tuple[int, int] = Field(default=(1920, 1080))

    @validator('voice')
    def validate_voice(cls, v):
        allowed_voices = ['male', 'male_warm', 'female', 'female_friendly']
        if v not in allowed_voices:
            raise ValueError(f'Voice must be one of: {allowed_voices}')
        return v

class JobResponse(BaseModel):
    """Job status response."""

    job_id: str
    status: str
    progress: float
    message: Optional[str] = None
    output_path: Optional[str] = None
    error: Optional[str] = None

# In-memory job storage (use Redis in production)
jobs: dict[str, JobResponse] = {}

@app.post("/api/generate", response_model=JobResponse, status_code=202)
async def generate_video(
    request: VideoGenerationRequest,
    background_tasks: BackgroundTasks
):
    """Generate a video asynchronously."""

    # Create job ID
    job_id = str(uuid.uuid4())

    # Initialize job status
    jobs[job_id] = JobResponse(
        job_id=job_id,
        status="queued",
        progress=0.0
    )

    # Add to background tasks
    background_tasks.add_task(
        process_video_generation,
        job_id,
        request
    )

    return jobs[job_id]

@app.get("/api/status/{job_id}", response_model=JobResponse)
async def get_job_status(job_id: str):
    """Get status of a video generation job."""

    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    return jobs[job_id]

@app.get("/api/jobs", response_model=List[JobResponse])
async def list_jobs(
    status: Optional[str] = None,
    limit: int = 50
):
    """List all jobs with optional filtering."""

    result = list(jobs.values())

    if status:
        result = [job for job in result if job.status == status]

    return result[:limit]

@app.delete("/api/jobs/{job_id}")
async def cancel_job(job_id: str):
    """Cancel a running job."""

    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = jobs[job_id]

    if job.status in ["completed", "failed", "cancelled"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel job in status: {job.status}"
        )

    job.status = "cancelled"
    return {"message": "Job cancelled successfully"}

@app.post("/api/translate")
async def translate_script(
    text: str,
    source_lang: str,
    target_lang: str,
    method: str = "claude"
):
    """Translate video script."""

    if method == "claude":
        translated = await translate_with_claude(text, source_lang, target_lang)
    elif method == "google":
        translated = await translate_with_google(text, source_lang, target_lang)
    else:
        raise HTTPException(status_code=400, detail="Invalid translation method")

    return {
        "original": text,
        "translated": translated,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "method": method
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""

    return {
        "status": "healthy",
        "version": "2.0.0",
        "services": {
            "ffmpeg": check_ffmpeg_available(),
            "anthropic": check_anthropic_api(),
            "storage": check_storage_available()
        }
    }

# Background task processor
async def process_video_generation(job_id: str, request: VideoGenerationRequest):
    """Process video generation in background."""

    try:
        # Update status
        jobs[job_id].status = "processing"
        jobs[job_id].progress = 0.1

        # Step 1: Generate audio (20% progress)
        audio_path = await generate_audio(request.script, request.voice, request.language)
        jobs[job_id].progress = 0.3

        # Step 2: Create visuals (40% progress)
        visual_path = await create_visuals(request, audio_path)
        jobs[job_id].progress = 0.7

        # Step 3: Render video (20% progress)
        output_path = await render_video(visual_path, audio_path, request)
        jobs[job_id].progress = 0.9

        # Complete
        jobs[job_id].status = "completed"
        jobs[job_id].progress = 1.0
        jobs[job_id].output_path = output_path
        jobs[job_id].message = "Video generated successfully"

    except Exception as e:
        jobs[job_id].status = "failed"
        jobs[job_id].error = str(e)
        logger.error(f"Video generation failed for job {job_id}: {e}")
```

---

### 5. CORPORATE_INTEL - FastAPI Enterprise API

**API Framework:** FastAPI + SQLAlchemy + PostgreSQL

**API Routes (7 major endpoints, 25+ sub-routes):**
```
# Authentication
POST   /api/auth/register         - User registration
POST   /api/auth/login            - User login
POST   /api/auth/refresh          - Refresh token
POST   /api/auth/logout           - User logout
POST   /api/auth/password-reset   - Password reset

# Companies
GET    /api/v1/companies          - List companies
POST   /api/v1/companies          - Create company
GET    /api/v1/companies/:id      - Get company
PUT    /api/v1/companies/:id      - Update company
DELETE /api/v1/companies/:id      - Delete company
GET    /api/v1/companies/:id/metrics - Get company metrics

# Filings
GET    /api/v1/filings            - List filings
POST   /api/v1/filings            - Create filing
GET    /api/v1/filings/:id        - Get filing
GET    /api/v1/filings/:id/document - Download document
POST   /api/v1/filings/:id/analyze - Analyze filing

# Metrics
GET    /api/v1/metrics            - Query metrics
POST   /api/v1/metrics/batch      - Batch insert metrics
GET    /api/v1/metrics/timeseries - Time-series data
GET    /api/v1/metrics/aggregate  - Aggregate metrics

# Intelligence
POST   /api/v1/intelligence/analyze - Run analysis
GET    /api/v1/intelligence/insights - Get insights
POST   /api/v1/intelligence/compare - Compare companies

# Reports
GET    /api/v1/reports            - List reports
POST   /api/v1/reports            - Generate report
GET    /api/v1/reports/:id        - Get report
DELETE /api/v1/reports/:id        - Delete report
GET    /api/v1/reports/:id/export - Export report

# Health & Monitoring
GET    /api/v1/health             - Health check
GET    /api/v1/metrics/system     - System metrics
```

**FastAPI Implementation:**
```python
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from src.auth.service import AuthService
from src.auth.models import User, UserCreate, TokenResponse
from src.core.dependencies import get_db, get_current_user
from src.api.v1.companies import router as companies_router
from src.api.v1.filings import router as filings_router
from src.api.v1.metrics import router as metrics_router
from src.api.v1.intelligence import router as intelligence_router
from src.api.v1.reports import router as reports_router

app = FastAPI(
    title="Corporate Intelligence Platform API",
    description="Enterprise-grade business intelligence and financial data analysis",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Include routers
app.include_router(companies_router, prefix="/api/v1", tags=["companies"])
app.include_router(filings_router, prefix="/api/v1", tags=["filings"])
app.include_router(metrics_router, prefix="/api/v1", tags=["metrics"])
app.include_router(intelligence_router, prefix="/api/v1", tags=["intelligence"])
app.include_router(reports_router, prefix="/api/v1", tags=["reports"])

# Authentication endpoints
@app.post("/api/auth/register", response_model=TokenResponse, status_code=201)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""

    auth_service = AuthService(db)

    try:
        user, tokens = await auth_service.register_user(user_data)
        return tokens
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/auth/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Authenticate user and return JWT tokens."""

    auth_service = AuthService(db)

    try:
        user, tokens = await auth_service.authenticate_user(
            form_data.username,
            form_data.password
        )
        return tokens
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

@app.post("/api/auth/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token."""

    auth_service = AuthService(db)

    try:
        tokens = await auth_service.refresh_access_token(refresh_token)
        return tokens
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

# Companies API
from src.core.models import CompanyCreate, CompanyResponse

@app.get("/api/v1/companies", response_model=List[CompanyResponse])
async def list_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    sector: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List companies with pagination and filtering."""

    query = db.query(Company)

    if sector:
        query = query.filter(Company.sector == sector)

    companies = query.offset(skip).limit(limit).all()
    return companies

@app.post("/api/v1/companies", response_model=CompanyResponse, status_code=201)
async def create_company(
    company_data: CompanyCreate,
    current_user: User = Depends(require_permission(PermissionScope.WRITE_COMPANIES)),
    db: Session = Depends(get_db)
):
    """Create a new company."""

    # Check if company already exists
    existing = db.query(Company).filter(
        Company.ticker == company_data.ticker
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Company with this ticker already exists"
        )

    company = Company(**company_data.dict())
    db.add(company)
    db.commit()
    db.refresh(company)

    return company

# Metrics API with TimescaleDB
@app.get("/api/v1/metrics/timeseries")
async def get_timeseries_metrics(
    company_id: int,
    metric_type: str,
    start_date: datetime,
    end_date: datetime,
    interval: str = Query("1h", regex="^(1h|1d|1w|1M)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get time-series metrics with TimescaleDB aggregation."""

    # Use TimescaleDB continuous aggregates
    if interval == "1h":
        query = f"""
        SELECT * FROM metrics_hourly
        WHERE company_id = :company_id
        AND metric_type = :metric_type
        AND hour BETWEEN :start_date AND :end_date
        ORDER BY hour
        """
    else:
        query = f"""
        SELECT
          time_bucket(:interval, time) AS bucket,
          company_id,
          metric_type,
          AVG(value) as avg_value,
          MAX(value) as max_value,
          MIN(value) as min_value
        FROM metrics
        WHERE company_id = :company_id
        AND metric_type = :metric_type
        AND time BETWEEN :start_date AND :end_date
        GROUP BY bucket, company_id, metric_type
        ORDER BY bucket
        """

    result = db.execute(
        query,
        {
            'company_id': company_id,
            'metric_type': metric_type,
            'start_date': start_date,
            'end_date': end_date,
            'interval': interval
        }
    )

    return [dict(row) for row in result]

# Health check
@app.get("/api/v1/health")
async def health_check(db: Session = Depends(get_db)):
    """Comprehensive health check."""

    try:
        # Check database
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    # Check Redis
    try:
        redis_client.ping()
        redis_status = "healthy"
    except Exception as e:
        redis_status = f"unhealthy: {str(e)}"

    return {
        "status": "healthy" if db_status == "healthy" and redis_status == "healthy" else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "database": db_status,
            "redis": redis_status,
            "ray": check_ray_status(),
            "prefect": check_prefect_status()
        }
    }
```

---

### 6. OPEN_LEARN - FastAPI Learning Platform API

**API Framework:** FastAPI + SQLAlchemy + AsyncPG

**API Routes (18 endpoints):**
```
# Authentication
POST   /api/auth/register         - User registration
POST   /api/auth/login            - User login
POST   /api/auth/logout           - User logout

# Language & Content
GET    /api/language              - Get language resources
POST   /api/language/analyze      - Analyze text
GET    /api/language/vocabulary   - Get vocabulary

# Scraping & Sources
GET    /api/scraping/sources      - List sources
POST   /api/scraping/scrape       - Trigger scrape
GET    /api/scraping/articles     - Get articles

# Analysis
POST   /api/analysis              - Analyze article
GET    /api/analysis/:id          - Get analysis
POST   /api/analysis/batch        - Batch analysis

# Search
GET    /api/search                - Full-text search
GET    /api/search/advanced       - Advanced search

# Export
POST   /api/export                - Export data
GET    /api/export/:id/download   - Download export

# Monitoring
GET    /api/health                - Health check
GET    /api/monitoring/metrics    - System metrics
GET    /api/monitoring/performance - Performance stats

# User Features
GET    /api/avatar/upload         - Upload avatar
GET    /api/preferences           - Get preferences
PUT    /api/preferences           - Update preferences
GET    /api/notifications         - Get notifications
PUT    /api/notifications/:id     - Mark as read

# Admin
GET    /api/cache/admin           - Cache admin
POST   /api/cache/admin/clear     - Clear cache
GET    /api/scheduler             - Scheduler status
```

**FastAPI Implementation:**
```python
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.connection import get_db
from app.services.scraper_service import ScraperService
from app.services.analysis_service import AnalysisService

app = FastAPI(
    title="Open Learn Colombia API",
    description="Colombian news and language learning platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Scraping endpoints
@app.post("/api/scraping/scrape")
async def trigger_scrape(
    source: str,
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Trigger scraping for a specific source."""

    scraper_service = ScraperService(db)

    # Validate source exists
    if not scraper_service.source_exists(source):
        raise HTTPException(status_code=404, detail="Source not found")

    # Add to background tasks
    background_tasks.add_task(
        scraper_service.scrape_source,
        source
    )

    return {
        "message": f"Scraping initiated for {source}",
        "status": "queued"
    }

@app.get("/api/scraping/articles")
async def get_articles(
    source: Optional[str] = None,
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get scraped articles with filtering."""

    query = db.query(Article)

    if source:
        query = query.filter(Article.source == source)

    if category:
        query = query.filter(Article.category == category)

    articles = query.order_by(
        Article.published_date.desc()
    ).offset(skip).limit(limit).all()

    return articles

# Analysis endpoints
@app.post("/api/analysis")
async def analyze_article(
    article_id: int,
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze an article for language learning."""

    article = db.query(Article).filter(Article.id == article_id).first()

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    analysis_service = AnalysisService(db)

    # Process in background
    background_tasks.add_task(
        analysis_service.analyze_article,
        article_id
    )

    return {
        "article_id": article_id,
        "status": "processing"
    }

# Full-text search with Elasticsearch
@app.get("/api/search")
async def search_articles(
    q: str,
    filters: Optional[dict] = None,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Full-text search across articles."""

    from app.search.elasticsearch_client import es_client

    # Build Elasticsearch query
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": q,
                            "fields": ["title^3", "content", "summary^2"],
                            "fuzziness": "AUTO"
                        }
                    }
                ]
            }
        },
        "from": skip,
        "size": limit,
        "highlight": {
            "fields": {
                "content": {},
                "title": {}
            }
        }
    }

    # Add filters
    if filters:
        query["query"]["bool"]["filter"] = []

        if "source" in filters:
            query["query"]["bool"]["filter"].append({
                "term": {"source": filters["source"]}
            })

        if "date_range" in filters:
            query["query"]["bool"]["filter"].append({
                "range": {
                    "published_date": filters["date_range"]
                }
            })

    # Execute search
    results = es_client.search(
        index="articles",
        body=query
    )

    return {
        "total": results["hits"]["total"]["value"],
        "results": [
            {
                "id": hit["_id"],
                "score": hit["_score"],
                **hit["_source"],
                "highlights": hit.get("highlight", {})
            }
            for hit in results["hits"]["hits"]
        ]
    }
```

---

## API Integration Patterns

### Error Handling Pattern

**Standardized Error Response:**
```typescript
interface APIError {
  error: string;
  message: string;
  details?: any;
  timestamp: string;
  path: string;
  statusCode: number;
}
```

**Implementation:**
```typescript
// Express/Node.js
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  const errorResponse: APIError = {
    error: err.name,
    message: err.message,
    timestamp: new Date().toISOString(),
    path: req.path,
    statusCode: err.statusCode || 500
  };

  if (process.env.NODE_ENV === 'development') {
    errorResponse.details = err.stack;
  }

  res.status(errorResponse.statusCode).json(errorResponse);
});
```

```python
# FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": type(exc).__name__,
            "message": str(exc),
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path
        }
    )
```

---

### Rate Limiting Pattern

**Implementation:**
```typescript
// Express rate limiting
import rateLimit from 'express-rate-limit';

const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  standardHeaders: true,
  legacyHeaders: false,
  handler: (req, res) => {
    res.status(429).json({
      error: 'Too Many Requests',
      message: 'Rate limit exceeded. Please try again later.',
      retryAfter: req.rateLimit.resetTime
    });
  }
});

app.use('/api/', apiLimiter);
```

```python
# FastAPI with SlowAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/api/data")
@limiter.limit("5/minute")
async def get_data(request: Request):
    return {"data": "value"}
```

---

### Caching Pattern

**Redis Caching:**
```typescript
import { createClient } from 'redis';

const redis = createClient({ url: process.env.REDIS_URL });

async function getCached<T>(
  key: string,
  fetcher: () => Promise<T>,
  ttl: number = 3600
): Promise<T> {
  // Try cache first
  const cached = await redis.get(key);

  if (cached) {
    return JSON.parse(cached);
  }

  // Fetch fresh data
  const fresh = await fetcher();

  // Cache it
  await redis.setEx(key, ttl, JSON.stringify(fresh));

  return fresh;
}

// Usage
const data = await getCached(
  `company:${id}`,
  () => fetchCompanyData(id),
  3600
);
```

---

### Pagination Pattern

**Cursor-based Pagination:**
```typescript
interface PaginatedResponse<T> {
  data: T[];
  pagination: {
    next_cursor: string | null;
    has_more: boolean;
    total?: number;
  };
}

async function paginateResults<T>(
  query: any,
  cursor?: string,
  limit: number = 20
): Promise<PaginatedResponse<T>> {
  const results = await query
    .where(cursor ? ['id', '>', cursor] : undefined)
    .limit(limit + 1)
    .execute();

  const hasMore = results.length > limit;
  const data = hasMore ? results.slice(0, limit) : results;
  const nextCursor = hasMore ? data[data.length - 1].id : null;

  return {
    data,
    pagination: {
      next_cursor: nextCursor,
      has_more: hasMore
    }
  };
}
```

---

## Security & Authentication

### JWT Implementation

**Token Generation:**
```typescript
import jwt from 'jsonwebtoken';

function generateAccessToken(userId: string): string {
  return jwt.sign(
    { sub: userId },
    process.env.JWT_SECRET,
    { expiresIn: '1h' }
  );
}

function generateRefreshToken(userId: string): string {
  return jwt.sign(
    { sub: userId },
    process.env.JWT_REFRESH_SECRET,
    { expiresIn: '7d' }
  );
}
```

**Token Verification:**
```typescript
import { verify } from 'jsonwebtoken';

async function verifyToken(token: string): Promise<JWTPayload> {
  try {
    const payload = verify(token, process.env.JWT_SECRET);
    return payload as JWTPayload;
  } catch (error) {
    throw new UnauthorizedError('Invalid token');
  }
}
```

---

### API Key Authentication

**API Key Middleware:**
```typescript
async function validateAPIKey(req: Request, res: Response, next: NextFunction) {
  const apiKey = req.headers['x-api-key'];

  if (!apiKey) {
    return res.status(401).json({ error: 'API key required' });
  }

  const isValid = await verifyAPIKey(apiKey);

  if (!isValid) {
    return res.status(401).json({ error: 'Invalid API key' });
  }

  next();
}
```

---

## Rate Limiting & Error Handling

### Exponential Backoff for External APIs

```typescript
async function fetchWithRetry<T>(
  fetcher: () => Promise<T>,
  maxRetries: number = 3,
  baseDelay: number = 1000
): Promise<T> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fetcher();
    } catch (error) {
      if (attempt === maxRetries - 1) throw error;

      const delay = baseDelay * Math.pow(2, attempt);
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }

  throw new Error('Max retries exceeded');
}

// Usage
const data = await fetchWithRetry(
  () => fetch('https://api.example.com/data'),
  3,
  1000
);
```

---

## Summary

This portfolio demonstrates comprehensive API proficiency across:

### External API Integration (8 projects, 25+ APIs):
1. **AI Services:** Anthropic Claude API (5 projects), OpenAI (legacy in 2 projects)
2. **Financial Data:** Alpha Vantage, SEC EDGAR, Yahoo Finance
3. **Government Data:** Colombian government APIs (DANE, Banco de la República, SECOP, DNP, IDEAM)
4. **Image Services:** Unsplash API (2 projects)
5. **Media:** YouTube Data API v3
6. **Analytics:** Google Analytics 4, Sentry
7. **Backend Services:** Supabase (4 projects), Vercel KV (Redis)

### Internal API Development (6 projects):
1. **AVES** - Express.js REST API (9 routes)
2. **Describe It** - Next.js API routes (20+ endpoints)
3. **Hablas** - Next.js API routes with NextAuth.js
4. **Video Gen** - FastAPI with background task processing
5. **Corporate Intel** - FastAPI enterprise API (25+ endpoints, TimescaleDB, RBAC)
6. **Open Learn** - FastAPI with Elasticsearch, async processing

### Key Technical Patterns Demonstrated:
- **Authentication:** JWT, OAuth2, API keys, session-based
- **Rate Limiting:** Per-user, per-IP, sliding window
- **Caching:** Redis, in-memory, CDN
- **Error Handling:** Standardized responses, retry logic, exponential backoff
- **Pagination:** Cursor-based, offset-based
- **Real-time:** WebSockets, server-sent events
- **Background Jobs:** Celery, FastAPI BackgroundTasks
- **Monitoring:** Health checks, metrics, performance tracking

---

*End of API Implementations Report*
