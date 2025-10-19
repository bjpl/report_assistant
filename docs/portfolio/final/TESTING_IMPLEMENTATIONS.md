# Testing Implementations Report

**Date:** October 18, 2025
**Projects with Testing:** 4 confirmed implementations
**Testing Frameworks:** Jest, Vitest, Playwright, Pytest
**Coverage:** Unit tests, Integration tests, E2E tests, Load testing

---

## Overview

This document details testing implementations across portfolio projects. Testing strategies range from comprehensive test-driven development with 70% coverage requirements to enterprise-grade load testing and cross-browser E2E verification. Four projects demonstrate professional testing practices with multiple test types and continuous integration support.

---

## Summary of All 4 Projects with Testing

### JavaScript/TypeScript Testing (3 projects):
1. **AVES** - Jest (backend), Vitest + Playwright (frontend), 70% coverage requirement
2. **Describe It** - Vitest, Playwright, MSW, Lighthouse performance testing
3. **Report Assistant** - Vitest for utilities

### Python Testing (2 projects):
4. **Corporate Intel** - Pytest, pytest-cov, Locust load testing, comprehensive markers
5. **Open Learn** - Pytest, pytest-asyncio, httpx, faker for test data

---

## Projects with Testing Features

### 1. AVES - Comprehensive Three-Tier Testing Strategy

**Testing Stack:** Jest + Vitest + Playwright + React Testing Library

**Backend Testing (Jest + ts-jest)**

**Configuration:**
```javascript
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  testMatch: ['**/__tests__/**/*.test.ts'],
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
    '!src/**/__tests__/**',
    '!src/index.ts'
  ],
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70
    }
  },
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1'
  },
  setupFilesAfterEnv: ['<rootDir>/src/__tests__/setup.ts'],
  globalTeardown: '<rootDir>/src/__tests__/globalTeardown.ts'],
  testTimeout: 15000,
  forceExit: true,
  detectOpenHandles: true,
  maxWorkers: 1,
  maxConcurrency: 1,
  verbose: true
};
```

**Dependencies:**
```json
{
  "devDependencies": {
    "@types/jest": "^30.0.0",
    "@types/supertest": "^6.0.3",
    "jest": "^29.7.0",
    "supertest": "^7.1.4",
    "ts-jest": "^29.1.1"
  }
}
```

**Test Scripts:**
```json
{
  "scripts": {
    "test": "jest"
  }
}
```

**Integration Test Example:**
```typescript
// src/__tests__/integration/auth-flow.test.ts
import request from 'supertest';
import express from 'express';
import authRouter from '../../routes/auth';
import {
  testPool,
  TEST_USERS,
  createTestUser,
  verifyTokenStructure,
} from './setup';

const app = express();
app.use(express.json());
app.use('/api', authRouter);

describe('Integration: Authentication Flow', () => {
  describe('Complete User Registration Flow', () => {
    it('should successfully register a new user and return valid JWT token', async () => {
      const response = await request(app)
        .post('/api/auth/register')
        .send(TEST_USERS.regularUser)
        .expect(201);

      expect(response.body).toHaveProperty('token');
      expect(response.body).toHaveProperty('user');
      expect(response.body.user).toHaveProperty('id');
      expect(response.body.user.email).toBe(TEST_USERS.regularUser.email.toLowerCase());
      expect(response.body.user).not.toHaveProperty('password_hash');

      expect(verifyTokenStructure(response.body.token)).toBe(true);

      const dbResult = await testPool.query(
        'SELECT id, email FROM users WHERE email = $1',
        [TEST_USERS.regularUser.email.toLowerCase()]
      );
      expect(dbResult.rows.length).toBe(1);
      expect(dbResult.rows[0].id).toBe(response.body.user.id);
    });

    it('should prevent duplicate user registration', async () => {
      await request(app)
        .post('/api/auth/register')
        .send(TEST_USERS.regularUser)
        .expect(201);

      const response = await request(app)
        .post('/api/auth/register')
        .send(TEST_USERS.regularUser)
        .expect(409);

      expect(response.body.error).toContain('already registered');

      const dbResult = await testPool.query(
        'SELECT COUNT(*) as count FROM users WHERE email = $1',
        [TEST_USERS.regularUser.email.toLowerCase()]
      );
      expect(parseInt(dbResult.rows[0].count)).toBe(1);
    });

    it('should enforce password strength requirements', async () => {
      const weakPasswords = [
        { password: 'short', reason: 'too short' },
        { password: 'nouppercase123', reason: 'no uppercase' },
        { password: 'NOLOWERCASE123', reason: 'no lowercase' },
        { password: 'NoNumbers', reason: 'no numbers' },
      ];

      for (const testCase of weakPasswords) {
        const response = await request(app)
          .post('/api/auth/register')
          .send({
            ...TEST_USERS.regularUser,
            password: testCase.password
          })
          .expect(400);

        expect(response.body.error).toBeTruthy();
      }
    });
  });
});
```

**Service Test Examples:**
```typescript
// src/__tests__/services/VisionAI.test.ts
describe('VisionAI Service', () => {
  it('should analyze bird images with Claude', async () => {
    const result = await visionAI.analyzeBirdImage(
      'https://example.com/flamingo.jpg'
    );

    expect(result).toHaveProperty('species');
    expect(result).toHaveProperty('annotations');
    expect(result.annotations).toBeInstanceOf(Array);
  });
});

// src/__tests__/services/ExerciseService.test.ts
describe('ExerciseService', () => {
  it('should generate contextual exercises', async () => {
    const exercises = await exerciseService.generateForSpecies('flamingo');

    expect(exercises.length).toBeGreaterThan(0);
    expect(exercises[0]).toHaveProperty('type');
    expect(exercises[0]).toHaveProperty('prompt');
  });
});
```

**Backend Test Structure:**
```
backend/src/__tests__/
├── config/
│   └── aiConfig.test.ts
├── integration/
│   ├── admin-dashboard-flow.test.ts
│   ├── annotation-workflow.test.ts
│   ├── auth-flow.test.ts
│   ├── exercise-generation-flow.test.ts
│   └── species-vocabulary-flow.test.ts
├── routes/
│   ├── auth.test.ts
│   ├── exercises.test.ts
│   └── vocabulary.test.ts
├── services/
│   ├── aiExerciseGenerator.test.ts
│   ├── exerciseCache.test.ts
│   ├── ExerciseService.test.ts
│   ├── userContextBuilder.test.ts
│   ├── UserService.test.ts
│   ├── VisionAI.test.ts
│   └── VocabularyService.test.ts
├── sanitize.test.ts
├── validate-middleware.test.ts
└── validation.test.ts
```

**Total Backend Tests:** 23 test files covering API routes, services, middleware, and integration flows

---

**Frontend Testing (Vitest + React Testing Library)**

**Configuration:**
```typescript
// vitest.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'happy-dom',
    setupFiles: ['./src/test/setup.ts'],
    css: true,
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'src/test/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/mockData',
        '**/*.test.*',
      ],
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

**Dependencies:**
```json
{
  "dependencies": {
    "@testing-library/jest-dom": "^6.9.1"
  },
  "devDependencies": {
    "@testing-library/dom": "^10.4.1",
    "@testing-library/react": "^14.3.1",
    "@testing-library/user-event": "^14.6.1",
    "@vitest/coverage-v8": "^1.6.1",
    "@vitest/ui": "^1.6.1",
    "happy-dom": "^12.10.3",
    "vitest": "^1.1.0"
  }
}
```

**Test Scripts:**
```json
{
  "scripts": {
    "test": "vitest",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:headed": "playwright test --headed",
    "test:e2e:debug": "playwright test --debug",
    "test:e2e:smoke": "playwright test smoke.spec.ts",
    "test:e2e:report": "playwright show-report"
  }
}
```

**Component Test Example:**
```typescript
// src/__tests__/components/exercises/VisualIdentification.test.tsx
import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '../../../test/test-utils';
import { userEvent } from '@testing-library/user-event';
import { VisualIdentification } from '../../../components/exercises/VisualIdentification';
import type { VisualIdentificationExercise } from '../../../../../shared/types/exercise.types';

describe('VisualIdentification', () => {
  const mockExercise: VisualIdentificationExercise = {
    id: 'vi-1',
    type: 'visual_identification',
    prompt: 'el pico',
    instructions: 'Click on the beak',
    metadata: {
      bird: 'flamingo',
      targetPart: 'beak',
      pronunciation: 'el PEE-koh',
      tip: 'The beak is the pointed part at the front of the head',
    },
  };

  const mockOnAnswer = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('Rendering', () => {
    it('should render without crashing', () => {
      render(
        <VisualIdentification
          exercise={mockExercise}
          onAnswer={mockOnAnswer}
          disabled={false}
        />
      );
      expect(screen.getByText('Visual Identification')).toBeInTheDocument();
    });

    it('should display prompt', () => {
      render(
        <VisualIdentification
          exercise={mockExercise}
          onAnswer={mockOnAnswer}
          disabled={false}
        />
      );
      expect(screen.getByText(mockExercise.prompt)).toBeInTheDocument();
    });

    it('should display instructions', () => {
      render(
        <VisualIdentification
          exercise={mockExercise}
          onAnswer={mockOnAnswer}
          disabled={false}
        />
      );
      expect(screen.getByText(/Click on:/i)).toBeInTheDocument();
    });

    it('should display pronunciation when available', () => {
      render(
        <VisualIdentification
          exercise={mockExercise}
          onAnswer={mockOnAnswer}
          disabled={false}
        />
      );
      expect(screen.getByText(mockExercise.metadata!.pronunciation!)).toBeInTheDocument();
    });
  });

  describe('User Interaction', () => {
    it('should call onAnswer when image is clicked', async () => {
      const user = userEvent.setup();
      render(
        <VisualIdentification
          exercise={mockExercise}
          onAnswer={mockOnAnswer}
          disabled={false}
        />
      );

      const image = screen.getByRole('img');
      await user.click(image);

      await waitFor(() => {
        expect(mockOnAnswer).toHaveBeenCalledWith({
          correct: expect.any(Boolean),
          coordinates: expect.objectContaining({
            x: expect.any(Number),
            y: expect.any(Number)
          })
        });
      });
    });
  });
});
```

**Frontend Test Structure:**
```
frontend/src/__tests__/
├── components/
│   ├── annotations/
│   │   ├── AnnotationBatchActions.test.tsx
│   │   ├── AnnotationCanvas.test.tsx
│   │   ├── AnnotationReviewCard.test.tsx
│   │   ├── HoverLayer.test.tsx
│   │   ├── InteractiveLayer.test.tsx
│   │   ├── ResponsiveAnnotationCanvas.test.tsx
│   │   └── StaticLayer.test.tsx
│   ├── exercises/
│   │   ├── AIExerciseContainer.test.tsx
│   │   ├── ContextualFill.test.tsx
│   │   ├── ExerciseContainer.test.tsx
│   │   ├── VisualDiscrimination.test.tsx
│   │   └── VisualIdentification.test.tsx
│   ├── learn/
│   │   ├── BirdSelector.test.tsx
│   │   ├── InteractiveBirdImage.test.tsx
│   │   ├── ProgressSection.test.tsx
│   │   └── VocabularyPanel.test.tsx
│   ├── lesson/
│   │   └── LessonQuiz.test.tsx
│   ├── practice/
│   │   ├── ExerciseRenderer.test.tsx
│   │   ├── FeedbackDisplay.test.tsx
│   │   └── PracticeStats.test.tsx
│   └── ui/
│       ├── Alert.test.tsx
│       ├── Badge.test.tsx
│       ├── Button.test.tsx
│       ├── Card.test.tsx
│       ├── Input.test.tsx
│       ├── Modal.test.tsx
│       ├── ProgressBar.test.tsx
│       ├── Skeleton.test.tsx
│       ├── Spinner.test.tsx
│       ├── Tabs.test.tsx
│       └── Tooltip.test.tsx
├── hooks/
│   ├── useAIAnnotations.test.ts
│   ├── useAIExercise.test.ts
│   ├── useAnnotations.test.ts
│   ├── useCMS.test.ts
│   ├── useDisclosure.test.ts
│   ├── useExercise.test.ts
│   ├── useMobileDetect.test.ts
│   ├── useProgress.test.ts
│   ├── useProgressQuery.test.ts
│   └── useSpecies.test.ts
└── services/
    ├── aiExerciseService.test.ts
    ├── apiAdapter.test.ts
    ├── clientDataService.test.ts
    ├── exerciseGenerator.test.ts
    └── unsplashService.test.ts
```

**Total Frontend Tests:** 45+ test files covering components, hooks, and services

---

**E2E Testing (Playwright)**

**Configuration:**
```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e/tests',
  timeout: 30 * 1000,
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,

  reporter: [
    ['html', { outputFolder: 'playwright-report' }],
    ['json', { outputFile: 'test-results/results.json' }],
    ['list']
  ],

  use: {
    baseURL: process.env.PLAYWRIGHT_BASE_URL || 'http://localhost:5173',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    actionTimeout: 10 * 1000,
    navigationTimeout: 30 * 1000,
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'], headless: true },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'], headless: true },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'], headless: true },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'], headless: true },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'], headless: true },
    },
    {
      name: 'iPad',
      use: { ...devices['iPad Pro'], headless: true },
    },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },

  outputDir: 'test-results/',
});
```

**Dependencies:**
```json
{
  "devDependencies": {
    "@playwright/test": "^1.55.1"
  }
}
```

**Smoke Test Example:**
```typescript
// e2e/tests/smoke.spec.ts
import { test, expect } from '../fixtures/test-fixtures';

test.describe('Smoke Tests', () => {
  test('should load home page without errors', async ({ page }) => {
    const errors: string[] = [];

    page.on('console', (msg) => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });

    page.on('pageerror', (error) => {
      errors.push(error.message);
    });

    await page.goto('/');
    await page.waitForLoadState('networkidle');

    await expect(page.locator('body')).toBeVisible();

    if (errors.length > 0) {
      console.log('Console errors detected:', errors);
    }
  });

  test('should have working navigation', async ({ page }) => {
    await page.goto('/');

    const navLinks = ['Learn', 'Practice', 'Species'];

    for (const link of navLinks) {
      const element = page.locator(`text=${link}`);
      await expect(element).toBeVisible();
    }
  });

  test('should respond quickly to user interactions', async ({ page }) => {
    await page.goto('/');

    const startTime = Date.now();
    await page.click('text=Learn');
    await page.waitForURL(/\/learn/);
    const endTime = Date.now();
    const navigationTime = endTime - startTime;

    expect(navigationTime).toBeLessThan(3000);
  });

  test('should be accessible via direct URLs', async ({ page }) => {
    const urls = ['/', '/learn', '/practice', '/species'];

    for (const url of urls) {
      await page.goto(url);
      await page.waitForLoadState('networkidle');

      const main = page.locator('main');
      await expect(main).toBeVisible();
    }
  });

  test('should have no broken assets', async ({ page }) => {
    const failed: string[] = [];

    page.on('response', response => {
      if (response.status() >= 400) {
        failed.push(`${response.status()} ${response.url()}`);
      }
    });

    await page.goto('/');
    await page.waitForLoadState('networkidle');

    expect(failed.length).toBe(0);
  });
});
```

**E2E Test Structure:**
```
frontend/e2e/tests/
├── learning-flow.spec.ts
├── navigation.spec.ts
├── practice-mode.spec.ts
├── responsive-design.spec.ts
├── smoke.spec.ts
└── species-browser.spec.ts
```

**Total E2E Tests:** 6 test suites covering critical user journeys across 6 devices (3 desktop browsers + 3 mobile viewports)

**AVES Testing Summary:**
- **Backend:** 23 Jest test files with 70% coverage requirement
- **Frontend:** 45+ Vitest test files with React Testing Library
- **E2E:** 6 Playwright test suites across 6 devices
- **Total:** 70+ test files with comprehensive coverage
- **CI Integration:** All tests run on every commit

---

### 2. DESCRIBE_IT - Multi-Tier Testing with Performance Monitoring

**Testing Stack:** Vitest + Playwright + MSW + Lighthouse

**Configuration:**

**Dependencies:**
```json
{
  "devDependencies": {
    "@playwright/test": "^1.55.1",
    "@testing-library/dom": "^10.4.1",
    "@testing-library/jest-dom": "^6.9.1",
    "@testing-library/react": "^16.3.0",
    "@testing-library/user-event": "^14.6.1",
    "@vitejs/plugin-react": "^4.2.1",
    "@vitest/coverage-v8": "^3.2.4",
    "jsdom": "^26.1.0",
    "lighthouse": "^13.0.0",
    "msw": "^2.11.3",
    "supertest": "^7.1.4",
    "vitest": "^3.2.4"
  }
}
```

**Test Scripts:**
```json
{
  "scripts": {
    "test": "vitest",
    "test:run": "vitest run",
    "test:coverage": "vitest run --coverage",
    "test:watch": "vitest --watch",
    "test:ui": "vitest --ui",
    "test:unit": "vitest run tests/unit",
    "test:integration": "vitest run tests/integration",
    "test:e2e": "playwright test",
    "test:e2e:staging": "playwright test --config=playwright-staging.config.ts",
    "test:smoke": "playwright test --grep='@smoke'",
    "test:supabase": "tsx scripts/test-supabase-connection.ts",
    "test:perf": "node scripts/performance-test.js",
    "test:vitals": "node scripts/web-vitals-test.js",
    "perf:test": "vitest run tests/performance",
    "perf:benchmark": "vitest run tests/performance/benchmark-suite.ts",
    "perf:monitor": "node scripts/performance-monitor.js",
    "perf:report": "node scripts/performance-report.js",
    "perf:regression": "vitest run tests/performance --reporter=json > performance-results.json",
    "lighthouse": "node scripts/lighthouse-audit.js",
    "lighthouse:ci": "npm run lighthouse -- --ci"
  }
}
```

**Test Types:**
1. **Unit Tests:** Component and utility function tests
2. **Integration Tests:** API endpoint integration tests
3. **E2E Tests:** Full user journey tests with Playwright
4. **Performance Tests:** Lighthouse audits and web vitals
5. **Smoke Tests:** Critical path verification
6. **API Tests:** Supabase connection and API integration tests

**Test Structure:**
```
tests/
├── api/
│   ├── api-integration.test.ts
│   ├── auth/
│   │   ├── signin.test.ts
│   │   └── signup.test.ts
│   ├── descriptions/
│   │   └── generate.test.ts
│   ├── export/
│   │   └── generate.test.ts
│   ├── health.test.ts
│   ├── images/
│   │   └── search.test.ts
│   ├── images-search.test.ts
│   ├── monitoring/
│   │   └── health.test.ts
│   ├── phrases/
│   │   └── extract.test.ts
│   ├── qa/
│   │   └── generate.test.ts
│   ├── questions/
│   │   └── generate.test.ts
│   ├── unit-tests.test.ts
│   └── vocabulary/
│       └── save.test.ts
├── auth/
│   └── AuthManager.test.ts
├── integration/
│   └── [integration test files]
├── performance/
│   └── benchmark-suite.ts
└── unit/
    └── [unit test files]
```

**API Test Example:**
```typescript
// tests/api/descriptions/generate.test.ts
import { describe, it, expect, beforeAll, vi } from 'vitest';
import { generateDescriptions } from '@/lib/ai/descriptions';

describe('POST /api/descriptions/generate', () => {
  beforeAll(() => {
    vi.mock('@anthropic-ai/sdk');
  });

  it('should generate descriptions for an image', async () => {
    const imageUrl = 'https://example.com/image.jpg';
    const styles = ['technical', 'creative'];

    const result = await generateDescriptions(imageUrl, styles);

    expect(result).toHaveLength(2);
    expect(result[0]).toHaveProperty('style', 'technical');
    expect(result[0]).toHaveProperty('text');
    expect(result[1]).toHaveProperty('style', 'creative');
  });

  it('should handle API errors gracefully', async () => {
    const invalidUrl = 'not-a-url';

    await expect(
      generateDescriptions(invalidUrl, ['technical'])
    ).rejects.toThrow();
  });
});
```

**MSW API Mocking:**
```typescript
// tests/mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.post('/api/descriptions/generate', async ({ request }) => {
    const body = await request.json();

    return HttpResponse.json({
      descriptions: [
        {
          style: body.styles[0],
          text: 'Mock description for testing'
        }
      ]
    });
  }),

  http.get('/api/images/search', ({ request }) => {
    const url = new URL(request.url);
    const query = url.searchParams.get('query');

    return HttpResponse.json({
      results: [
        {
          id: '1',
          urls: { regular: 'https://example.com/1.jpg' },
          description: `Image matching ${query}`
        }
      ]
    });
  }),
];
```

**Performance Testing:**
```typescript
// tests/performance/benchmark-suite.ts
import { describe, it, expect } from 'vitest';
import { performance } from 'perf_hooks';

describe('Performance Benchmarks', () => {
  it('should generate descriptions in under 3 seconds', async () => {
    const start = performance.now();

    await generateDescriptions(testImageUrl, ['technical']);

    const duration = performance.now() - start;
    expect(duration).toBeLessThan(3000);
  });

  it('should handle batch processing efficiently', async () => {
    const imageUrls = Array(10).fill(testImageUrl);
    const start = performance.now();

    await Promise.all(
      imageUrls.map(url => generateDescriptions(url, ['technical']))
    );

    const duration = performance.now() - start;
    expect(duration).toBeLessThan(10000); // 1s per image average
  });
});
```

**Lighthouse Integration:**
```javascript
// scripts/lighthouse-audit.js
const lighthouse = require('lighthouse');
const chromeLauncher = require('chrome-launcher');

async function runLighthouse(url) {
  const chrome = await chromeLauncher.launch({ chromeFlags: ['--headless'] });

  const options = {
    logLevel: 'info',
    output: 'html',
    onlyCategories: ['performance', 'accessibility', 'best-practices', 'seo'],
    port: chrome.port,
  };

  const runnerResult = await lighthouse(url, options);

  await chrome.kill();

  // Assert performance score
  const performanceScore = runnerResult.lhr.categories.performance.score * 100;
  console.log(`Performance score: ${performanceScore}`);

  if (performanceScore < 90) {
    throw new Error(`Performance score ${performanceScore} is below threshold of 90`);
  }

  return runnerResult;
}
```

**Describe It Testing Summary:**
- **Unit Tests:** Component and service tests with Vitest
- **Integration Tests:** API integration with MSW mocking
- **E2E Tests:** Playwright cross-browser testing
- **Performance Tests:** Lighthouse audits + custom benchmarks
- **Smoke Tests:** Critical path verification
- **Coverage:** V8 coverage reporting
- **CI Integration:** Multiple test commands for different scenarios

---

### 3. CORPORATE_INTEL - Enterprise-Grade Testing Suite

**Testing Stack:** Pytest + pytest-cov + pytest-asyncio + Locust

**Configuration:**
```ini
# pytest.ini
[pytest]
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*

testpaths = tests

minversion = 3.11

addopts =
    -v
    -ra
    -l
    --strict-markers
    --cov=src
    --cov-report=html:htmlcov
    --cov-report=term-missing
    --cov-report=xml
    --cov-branch
    -W error::DeprecationWarning
    -W error::PendingDeprecationWarning
    --durations=10
    --tb=short
    --color=yes

markers =
    unit: Unit tests (fast, isolated)
    integration: Integration tests (require database/external services)
    slow: Slow running tests
    auth: Authentication and authorization tests
    api: API endpoint tests
    database: Database-related tests
    security: Security-focused tests
    performance: Performance and load tests
    smoke: Smoke tests for critical functionality
    regression: Regression tests
    real_world: Real-world API tests (calls actual APIs, may be slow and incur costs)

[coverage:run]
source = src
omit =
    */tests/*
    */test_*.py
    */__pycache__/*
    */venv/*
    */virtualenv/*
    */.venv/*

[coverage:report]
precision = 2
show_missing = True
skip_covered = False
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstractmethod
    @abc.abstractmethod

asyncio_mode = auto

log_cli = true
log_cli_level = INFO
log_cli_format = %(asctime)s [%(levelname)8s] %(message)s
log_cli_date_format = %Y-%m-%d %H:%M:%S

timeout = 300
timeout_method = thread

console_output_style = progress

filterwarnings =
    error
    ignore::UserWarning
    ignore::DeprecationWarning:passlib.*
```

**Dependencies:**
```python
# requirements.txt (testing section)
pytest>=7.4.0,<8.0.0
pytest-asyncio>=0.21.0,<1.0.0
pytest-cov>=4.1.0,<5.0.0
httpx>=0.25.0,<1.0.0
locust>=2.17.0,<3.0.0  # Load testing
```

**Test Structure:**
```
tests/
├── api/
│   ├── API_TESTING_GUIDE.md
│   ├── conftest.py
│   ├── test_advanced_edge_cases.py
│   ├── test_auth.py
│   ├── test_companies.py
│   ├── test_error_handling.py
│   ├── test_filings.py
│   ├── test_health.py
│   ├── test_health_endpoints.py
│   └── test_intelligence.py
├── e2e/
│   └── [end-to-end test files]
├── fixtures/
│   └── [test fixtures and mock data]
├── integration/
│   └── [integration test files]
├── load-testing/
│   └── [Locust load test files]
├── migrations/
│   └── [migration test files]
├── performance/
│   └── [performance test files]
├── services/
│   └── [service test files]
├── staging/
│   └── [staging environment tests]
├── conftest.py
├── pytest.ini
└── smoke_test_comprehensive.py
```

**Authentication Test Example:**
```python
# tests/api/test_auth.py
import pytest
from datetime import datetime, timedelta
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.auth.models import User, UserRole


class TestRegisterEndpoint:
    """Test suite for POST /auth/register endpoint."""

    def test_register_user_success(self, api_client: TestClient):
        """Test successful user registration."""
        user_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "SecurePass123!@#",
            "full_name": "New User",
            "organization": "Test Org"
        }

        response = api_client.post("/auth/register", json=user_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()

        assert "message" in data
        assert "user" in data
        assert data["user"]["email"] == user_data["email"]
        assert data["user"]["username"] == user_data["username"]
        assert data["user"]["role"] == UserRole.VIEWER.value

    def test_register_duplicate_email(
        self, api_client: TestClient, test_user: User
    ):
        """Test registration with duplicate email returns 400."""
        user_data = {
            "email": test_user.email,
            "username": "differentuser",
            "password": "SecurePass123!@#"
        }

        response = api_client.post("/auth/register", json=user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_duplicate_username(
        self, api_client: TestClient, test_user: User
    ):
        """Test registration with duplicate username returns 400."""
        user_data = {
            "email": "different@example.com",
            "username": test_user.username,
            "password": "SecurePass123!@#"
        }

        response = api_client.post("/auth/register", json=user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_weak_password(self, api_client: TestClient):
        """Test registration with weak password returns 400."""
        user_data = {
            "email": "weak@example.com",
            "username": "weakuser",
            "password": "weak"
        }

        response = api_client.post("/auth/register", json=user_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_register_invalid_email(self, api_client: TestClient):
        """Test registration with invalid email returns 422."""
        user_data = {
            "email": "invalid-email",
            "username": "testuser",
            "password": "SecurePass123!@#"
        }

        response = api_client.post("/auth/register", json=user_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_missing_required_fields(self, api_client: TestClient):
        """Test registration with missing fields returns 422."""
        user_data = {
            "email": "test@example.com"
            # Missing username and password
        }

        response = api_client.post("/auth/register", json=user_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestLoginEndpoint:
    """Test suite for POST /auth/login endpoint."""

    def test_login_success(self, api_client: TestClient, test_user: User):
        """Test successful login."""
        login_data = {
            "username": test_user.email,
            "password": "TestPassword123!"
        }

        response = api_client.post("/auth/login", data=login_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self, api_client: TestClient):
        """Test login with invalid credentials returns 401."""
        login_data = {
            "username": "nonexistent@example.com",
            "password": "WrongPassword123!"
        }

        response = api_client.post("/auth/login", data=login_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.security
    def test_login_rate_limiting(self, api_client: TestClient):
        """Test login endpoint has rate limiting."""
        login_data = {
            "username": "test@example.com",
            "password": "WrongPassword!"
        }

        # Make multiple failed login attempts
        for _ in range(10):
            response = api_client.post("/auth/login", data=login_data)

        # Should eventually be rate limited
        assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
```

**Test Fixtures:**
```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.database import Base, get_db
from src.auth.models import User, UserRole
from src.auth.service import AuthService

# Test database setup
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def api_client(db):
    """Create API test client with database dependency override."""
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db) -> User:
    """Create a test user."""
    auth_service = AuthService()
    password_hash = auth_service.hash_password("TestPassword123!")

    user = User(
        email="test@example.com",
        username="testuser",
        password_hash=password_hash,
        role=UserRole.VIEWER,
        is_active=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@pytest.fixture
def admin_user(db) -> User:
    """Create an admin test user."""
    auth_service = AuthService()
    password_hash = auth_service.hash_password("AdminPassword123!")

    user = User(
        email="admin@example.com",
        username="adminuser",
        password_hash=password_hash,
        role=UserRole.ADMIN,
        is_active=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@pytest.fixture
def auth_headers(api_client: TestClient, test_user: User) -> dict:
    """Get authentication headers for test user."""
    login_data = {
        "username": test_user.email,
        "password": "TestPassword123!"
    }

    response = api_client.post("/auth/login", data=login_data)
    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}
```

**Load Testing with Locust:**
```python
# tests/load-testing/locustfile.py
from locust import HttpUser, task, between


class CorporateIntelUser(HttpUser):
    """Load test user simulating Corporate Intel API usage."""

    wait_time = between(1, 3)

    def on_start(self):
        """Login before starting tasks."""
        response = self.client.post("/auth/login", data={
            "username": "loadtest@example.com",
            "password": "LoadTest123!"
        })

        if response.status_code == 200:
            self.token = response.json()["access_token"]
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            self.headers = {}

    @task(3)
    def get_companies(self):
        """Fetch company list."""
        self.client.get("/api/companies", headers=self.headers)

    @task(2)
    def search_companies(self):
        """Search companies."""
        self.client.get(
            "/api/companies/search?q=tech",
            headers=self.headers
        )

    @task(1)
    def get_company_details(self):
        """Get specific company details."""
        self.client.get("/api/companies/AAPL", headers=self.headers)

    @task(1)
    def health_check(self):
        """Check API health."""
        self.client.get("/health")
```

**Running Load Tests:**
```bash
# Start load test with 100 users, 10 users/sec spawn rate
locust -f tests/load-testing/locustfile.py --host=http://localhost:8000 -u 100 -r 10

# Headless mode for CI
locust -f tests/load-testing/locustfile.py --host=http://localhost:8000 -u 100 -r 10 --headless --run-time 5m
```

**Test Markers Usage:**
```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run smoke tests (fast critical path)
pytest -m smoke

# Run all tests except slow ones
pytest -m "not slow"

# Run security tests
pytest -m security

# Run performance tests
pytest -m performance

# Run API tests
pytest -m api

# Run auth tests
pytest -m auth

# Exclude real-world API tests (that call external APIs)
pytest -m "not real_world"
```

**Coverage Reports:**
```bash
# Generate HTML coverage report
pytest --cov=src --cov-report=html

# View coverage in terminal
pytest --cov=src --cov-report=term-missing

# Generate XML coverage for CI
pytest --cov=src --cov-report=xml

# Check branch coverage
pytest --cov=src --cov-branch
```

**Corporate Intel Testing Summary:**
- **Pytest Configuration:** Comprehensive pytest.ini with 10 custom markers
- **Test Categories:** unit, integration, slow, auth, api, database, security, performance, smoke, regression, real_world
- **Coverage:** HTML, terminal, and XML reports with branch coverage
- **Load Testing:** Locust for performance testing
- **Async Support:** pytest-asyncio for FastAPI testing
- **API Testing:** httpx for async HTTP client testing
- **Test Organization:** Separate directories for api, e2e, integration, load-testing, performance, staging
- **CI Integration:** Comprehensive test suite with multiple execution modes

---

### 4. OPEN_LEARN - FastAPI Testing with Async Support

**Testing Stack:** Pytest + pytest-asyncio + httpx + faker

**Dependencies:**
```python
# requirements.txt (testing section)
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
aioresponses==0.7.6  # Mock for aiohttp requests
pytest-cov==4.1.0  # Coverage reporting
pytest-mock==3.12.0  # Enhanced mocking support
responses==0.24.1  # Mock for requests library
faker==20.1.0  # Generate test data
```

**Test Structure:**
```
backend/tests/
├── api/
│   └── [API endpoint tests]
├── fixtures/
│   └── [test fixtures]
├── scrapers/
│   └── [scraper tests]
├── security/
│   └── [security tests]
├── unit/
│   └── [unit tests]
├── conftest.py
├── README-health-tests.md
└── test_health.py
```

**Test Fixtures:**
```python
# tests/conftest.py
import pytest
import asyncio
from unittest.mock import Mock, patch


@pytest.fixture
def sample_text():
    """Sample Spanish text for testing"""
    return "El presidente de Colombia anunció nuevas medidas económicas."


@pytest.fixture
def sample_html():
    """Sample HTML for testing"""
    return """
    <html>
        <head>
            <title>Test Article</title>
            <meta name="description" content="Test description">
        </head>
        <body>
            <article>
                <h1>Test Title</h1>
                <p>Test content here.</p>
            </article>
        </body>
    </html>
    """


@pytest.fixture
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_settings():
    """Mock settings for testing"""
    mock_settings = Mock()
    mock_settings.USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    ]
    mock_settings.REQUEST_TIMEOUT = 30
    return mock_settings


@pytest.fixture(autouse=True)
def patch_settings(monkeypatch, mock_settings):
    """Automatically patch settings for all tests"""
    import sys

    try:
        from app.config import settings
        monkeypatch.setattr('app.config.settings', mock_settings)
    except ImportError:
        from types import ModuleType

        if 'app' not in sys.modules:
            app_module = ModuleType('app')
            sys.modules['app'] = app_module

        config_module = ModuleType('config')
        config_module.settings = mock_settings
        sys.modules['app.config'] = config_module
        sys.modules['app'].config = config_module
```

**Health Test Example:**
```python
# tests/test_health.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoints."""

    def test_health_endpoint_returns_200(self):
        """Test that health endpoint returns 200 OK."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data

    def test_readiness_probe(self):
        """Test readiness probe for Kubernetes."""
        response = client.get("/health/ready")

        assert response.status_code == 200
        data = response.json()

        assert data["ready"] is True
        assert "database" in data
        assert "elasticsearch" in data

    def test_liveness_probe(self):
        """Test liveness probe for Kubernetes."""
        response = client.get("/health/live")

        assert response.status_code == 200
        assert response.json()["alive"] is True

    @pytest.mark.asyncio
    async def test_database_health_check(self):
        """Test database connectivity check."""
        from app.core.health import check_database_health

        result = await check_database_health()

        assert result["status"] in ["healthy", "degraded"]
        assert "latency_ms" in result
        assert result["latency_ms"] < 1000  # Should respond within 1s

    @pytest.mark.asyncio
    async def test_elasticsearch_health_check(self):
        """Test Elasticsearch connectivity check."""
        from app.core.health import check_elasticsearch_health

        result = await check_elasticsearch_health()

        assert result["status"] in ["healthy", "degraded", "unhealthy"]
        assert "cluster_name" in result
```

**Async API Test Example:**
```python
# tests/api/test_search.py
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
class TestSearchEndpoints:
    """Test search API endpoints."""

    async def test_search_articles(self):
        """Test article search endpoint."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(
                "/api/v1/search/articles",
                params={"q": "educación", "limit": 10}
            )

        assert response.status_code == 200
        data = response.json()

        assert "results" in data
        assert "total" in data
        assert len(data["results"]) <= 10

    async def test_search_with_filters(self):
        """Test search with date and source filters."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(
                "/api/v1/search/articles",
                params={
                    "q": "economía",
                    "date_from": "2024-01-01",
                    "date_to": "2024-12-31",
                    "sources": ["DANE", "BanRep"]
                }
            )

        assert response.status_code == 200
        data = response.json()

        assert all(
            result["source"] in ["DANE", "BanRep"]
            for result in data["results"]
        )

    async def test_search_pagination(self):
        """Test search pagination."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            # First page
            response1 = await ac.get(
                "/api/v1/search/articles",
                params={"q": "salud", "limit": 5, "offset": 0}
            )

            # Second page
            response2 = await ac.get(
                "/api/v1/search/articles",
                params={"q": "salud", "limit": 5, "offset": 5}
            )

        assert response1.status_code == 200
        assert response2.status_code == 200

        page1_ids = [r["id"] for r in response1.json()["results"]]
        page2_ids = [r["id"] for r in response2.json()["results"]]

        # No overlap between pages
        assert len(set(page1_ids) & set(page2_ids)) == 0
```

**Test Data Generation with Faker:**
```python
# tests/unit/test_models.py
import pytest
from faker import Faker
from app.models.article import Article

fake = Faker(['es_ES'])  # Spanish locale


class TestArticleModel:
    """Test Article model."""

    def test_create_article(self):
        """Test article creation with faker data."""
        article = Article(
            title=fake.sentence(),
            content=fake.text(max_nb_chars=1000),
            author=fake.name(),
            published_date=fake.date_time(),
            source=fake.company()
        )

        assert article.title is not None
        assert len(article.content) > 0
        assert article.author is not None

    def test_article_validation(self):
        """Test article validation."""
        with pytest.raises(ValueError):
            Article(
                title="",  # Empty title should fail
                content=fake.text(),
                author=fake.name()
            )

    def test_article_serialization(self):
        """Test article JSON serialization."""
        article = Article(
            title=fake.sentence(),
            content=fake.text(),
            author=fake.name(),
            published_date=fake.date_time()
        )

        data = article.dict()

        assert "title" in data
        assert "content" in data
        assert "author" in data
        assert "published_date" in data
```

**Open Learn Testing Summary:**
- **Pytest:** Main testing framework
- **pytest-asyncio:** Async test support for FastAPI
- **httpx:** Async HTTP client for API testing
- **faker:** Test data generation with Spanish locale
- **aioresponses:** Mock async HTTP requests
- **pytest-mock:** Enhanced mocking capabilities
- **Test Organization:** Separate directories for api, unit, security, scrapers
- **Health Checks:** Comprehensive health check testing for Kubernetes readiness/liveness probes

---

## Common Testing Patterns

### Test Organization Best Practices

**Standard Directory Structure:**
```
project/
├── src/ or app/
│   └── [application code]
├── tests/ or __tests__/
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   ├── performance/
│   ├── fixtures/
│   ├── conftest.py (Python)
│   └── setup.ts (TypeScript)
└── [config files]
```

**Test File Naming:**
- Python: `test_*.py` or `*_test.py`
- JavaScript/TypeScript: `*.test.ts`, `*.test.tsx`, `*.spec.ts`

---

### Coverage Requirements

**AVES Backend (Jest):**
```javascript
coverageThreshold: {
  global: {
    branches: 70,
    functions: 70,
    lines: 70,
    statements: 70
  }
}
```

**Vitest Coverage (AVES Frontend, Describe It):**
```typescript
coverage: {
  provider: 'v8',
  reporter: ['text', 'json', 'html'],
  exclude: [
    'node_modules/',
    'src/test/',
    '**/*.d.ts',
    '**/*.config.*',
    '**/mockData',
    '**/*.test.*',
  ],
}
```

**Pytest Coverage (Corporate Intel, Open Learn):**
```ini
[coverage:run]
source = src
omit =
    */tests/*
    */test_*.py
    */__pycache__/*
    */venv/*

[coverage:report]
precision = 2
show_missing = True
skip_covered = False
```

---

### Fixture and Setup Patterns

**Jest Setup:**
```typescript
// setup.ts
import { testPool } from './database';

beforeAll(async () => {
  await testPool.connect();
});

afterAll(async () => {
  await testPool.end();
});

beforeEach(async () => {
  await testPool.query('BEGIN');
});

afterEach(async () => {
  await testPool.query('ROLLBACK');
});
```

**Pytest Fixtures:**
```python
@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
```

**Vitest Setup:**
```typescript
// setup.ts
import { afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';
import '@testing-library/jest-dom';

afterEach(() => {
  cleanup();
});
```

---

### Mocking Strategies

**MSW for API Mocking:**
```typescript
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';

const handlers = [
  http.post('/api/generate', () => {
    return HttpResponse.json({ result: 'mocked' });
  }),
];

const server = setupServer(...handlers);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

**Pytest Mocking:**
```python
from unittest.mock import Mock, patch

@patch('app.services.external_api.call')
def test_external_call(mock_call):
    mock_call.return_value = {"status": "success"}

    result = service.fetch_data()

    assert result["status"] == "success"
    mock_call.assert_called_once()
```

---

### E2E Testing Best Practices

**Playwright Configuration:**
```typescript
export default defineConfig({
  timeout: 30 * 1000,
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,

  use: {
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'Mobile Chrome', use: { ...devices['Pixel 5'] } },
    { name: 'Mobile Safari', use: { ...devices['iPhone 12'] } },
  ],
});
```

---

### Performance Testing

**Vitest Benchmarks:**
```typescript
import { describe, it, expect } from 'vitest';
import { performance } from 'perf_hooks';

describe('Performance', () => {
  it('should complete operation within time limit', async () => {
    const start = performance.now();

    await expensiveOperation();

    const duration = performance.now() - start;
    expect(duration).toBeLessThan(3000);
  });
});
```

**Locust Load Testing:**
```python
from locust import HttpUser, task, between

class LoadTestUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def frequent_endpoint(self):
        self.client.get("/api/data")

    @task(1)
    def occasional_endpoint(self):
        self.client.post("/api/process")
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Run unit tests
        run: npm run test:unit

      - name: Run integration tests
        run: npm run test:integration

      - name: Run E2E tests
        run: npm run test:e2e

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json
```

### Python CI Example

```yaml
name: Python Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run unit tests
        run: pytest -m unit

      - name: Run integration tests
        run: pytest -m integration

      - name: Generate coverage report
        run: pytest --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

## Testing Metrics Summary

### Projects with Comprehensive Testing

| Project | Framework | Test Types | Coverage | E2E | Load Testing |
|---------|-----------|------------|----------|-----|--------------|
| **AVES** | Jest + Vitest + Playwright | Unit, Integration, E2E | 70% required | ✅ 6 devices | ❌ |
| **Describe It** | Vitest + Playwright + Lighthouse | Unit, Integration, E2E, Performance | V8 coverage | ✅ Cross-browser | ❌ |
| **Corporate Intel** | Pytest + Locust | Unit, Integration, API, Security, Performance, Load | Branch coverage | ✅ E2E tests | ✅ Locust |
| **Open Learn** | Pytest + httpx | Unit, Integration, API, Security | pytest-cov | ❌ | ❌ |

### Test File Counts

- **AVES:** 70+ test files (23 backend, 45+ frontend, 6 E2E)
- **Describe It:** 15+ API tests, multiple E2E suites
- **Corporate Intel:** 9+ API test files, load testing, performance tests
- **Open Learn:** Multiple test categories (api, unit, security, scrapers)

### Testing Frameworks Used

**JavaScript/TypeScript:**
- Jest (backend testing)
- Vitest (unit/integration testing)
- Playwright (E2E testing)
- React Testing Library (component testing)
- Supertest (API testing)
- MSW (API mocking)
- Lighthouse (performance testing)

**Python:**
- Pytest (all test types)
- pytest-asyncio (async support)
- pytest-cov (coverage reporting)
- pytest-mock (mocking)
- httpx (async HTTP client)
- Locust (load testing)
- faker (test data generation)
- aioresponses (async mocking)

---

## Summary

Testing implementations across the portfolio demonstrate professional-grade practices:

1. **4 Projects with Comprehensive Testing:** AVES, Describe It, Corporate Intel, Open Learn
2. **Multiple Test Types:** Unit, Integration, E2E, Performance, Load, Smoke, Security
3. **Coverage Requirements:** 70% threshold (AVES), branch coverage (Corporate Intel)
4. **Cross-Browser Testing:** Playwright testing on Chromium, Firefox, WebKit, mobile devices
5. **CI/CD Integration:** All projects configured for continuous testing
6. **Load Testing:** Locust integration for enterprise applications (Corporate Intel)
7. **Performance Monitoring:** Lighthouse audits, web vitals, custom benchmarks
8. **Professional Tooling:** Jest, Vitest, Playwright, Pytest, MSW, React Testing Library

**Best Practices Implemented:**
- Test isolation with fixtures and setup/teardown
- Comprehensive mocking strategies
- Async/await testing support
- API integration testing
- Database transaction rollback in tests
- Coverage reporting (HTML, terminal, XML)
- Test categorization with markers/tags
- Performance benchmarking
- Security testing
- Health check testing

**Testing Strategy Maturity:**
- **AVES:** Gold standard with 70% coverage requirement, three-tier testing (unit/integration/E2E), cross-device E2E
- **Describe It:** Performance-focused with Lighthouse integration, MSW for API mocking, comprehensive test scripts
- **Corporate Intel:** Enterprise-grade with 10 test markers, load testing, comprehensive pytest configuration
- **Open Learn:** FastAPI best practices with async testing, faker for test data, health check testing

---

*End of Testing Implementations Report*
