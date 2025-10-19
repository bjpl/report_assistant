# PostgreSQL Direct Implementation Report

**Date:** October 18, 2025
**Projects Using PostgreSQL (Non-Supabase):** 2-3 confirmed implementations
**Primary Use Cases:** Time-series data, business intelligence, educational content

---

## Overview

This document details direct PostgreSQL implementations across portfolio projects, excluding those using Supabase as the database provider. These implementations use self-hosted or cloud-hosted PostgreSQL instances with direct database connections.

---

## Projects with Direct PostgreSQL Implementation

### 1. CORPORATE_INTEL - Business Intelligence Platform

**Database Configuration:** PostgreSQL with TimescaleDB extension

**Database Architecture:**
```
PostgreSQL 14+ with TimescaleDB 2.x
├── Core PostgreSQL
├── TimescaleDB extension (time-series optimization)
├── pgvector extension (semantic search)
└── pg_stat_statements (performance monitoring)
```

**Schema Design:**
```sql
-- Companies table
companies (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  ticker VARCHAR(10),
  sector VARCHAR(100),
  created_at TIMESTAMPTZ
)

-- Time-series metrics (hypertable)
metrics (
  time TIMESTAMPTZ NOT NULL,
  company_id INTEGER,
  metric_type VARCHAR(50),
  value NUMERIC,
  metadata JSONB
)
-- TimescaleDB hypertable conversion
SELECT create_hypertable('metrics', 'time');

-- Vector embeddings for semantic search
company_embeddings (
  id SERIAL PRIMARY KEY,
  company_id INTEGER,
  embedding vector(1536),
  created_at TIMESTAMPTZ
)
```

**Connection Management:**
```python
# Database connection configuration
DATABASE_URL = "postgresql://user:password@localhost:5432/corporate_intel"

# Connection pooling with SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,
    pool_recycle=3600
)
```

**TimescaleDB Features Used:**
- Hypertables for time-series data
- Continuous aggregates for performance
- Data retention policies
- Compression (10x reduction achieved)
- Time-based partitioning

**Performance Optimizations:**
```sql
-- Continuous aggregate for hourly metrics
CREATE MATERIALIZED VIEW metrics_hourly
WITH (timescaledb.continuous) AS
SELECT
  time_bucket('1 hour', time) AS hour,
  company_id,
  metric_type,
  AVG(value) as avg_value,
  MAX(value) as max_value,
  MIN(value) as min_value
FROM metrics
GROUP BY hour, company_id, metric_type;

-- Compression policy
ALTER TABLE metrics SET (
  timescaledb.compress,
  timescaledb.compress_segmentby = 'company_id'
);
```

**Database Operations:**
- Batch inserts for efficiency
- Partitioned queries by time range
- Vector similarity searches
- JSONB queries for metadata
- Window functions for analytics

**Backup and Maintenance:**
```bash
# Backup strategy
pg_dump -Fc corporate_intel > backup.dump

# Vacuum and analyze
VACUUM ANALYZE metrics;

# Reindex for performance
REINDEX INDEX CONCURRENTLY idx_metrics_time;
```

---

### 2. AVES - Educational Content Database

**Database Configuration:** PostgreSQL with Drizzle ORM

**Database Stack:**
```
PostgreSQL 14+
├── Drizzle ORM (TypeScript)
├── Migration management
├── Connection pooling
└── Type-safe queries
```

**Schema Structure:**
```typescript
// Drizzle schema definition
export const species = pgTable('species', {
  id: serial('id').primaryKey(),
  scientificName: varchar('scientific_name', { length: 255 }),
  commonNameEn: varchar('common_name_en', { length: 255 }),
  commonNameEs: varchar('common_name_es', { length: 255 }),
  family: varchar('family', { length: 100 }),
  order: varchar('order', { length: 100 }),
  conservationStatus: varchar('conservation_status', { length: 50 }),
  createdAt: timestamp('created_at').defaultNow()
});

export const vocabulary = pgTable('vocabulary', {
  id: serial('id').primaryKey(),
  term: varchar('term', { length: 255 }),
  definition: text('definition'),
  etymology: text('etymology'),
  difficulty: integer('difficulty'),
  category: varchar('category', { length: 100 })
});

export const annotations = pgTable('annotations', {
  id: serial('id').primaryKey(),
  speciesId: integer('species_id').references(() => species.id),
  imageUrl: text('image_url'),
  annotations: jsonb('annotations'),
  generatedBy: varchar('generated_by', { length: 50 }),
  createdAt: timestamp('created_at').defaultNow()
});

export const userProgress = pgTable('user_progress', {
  id: serial('id').primaryKey(),
  userId: varchar('user_id', { length: 255 }),
  vocabularyId: integer('vocabulary_id').references(() => vocabulary.id),
  masteryLevel: integer('mastery_level'),
  lastReviewed: timestamp('last_reviewed'),
  reviewCount: integer('review_count').default(0)
});
```

**Drizzle ORM Configuration:**
```typescript
import { drizzle } from 'drizzle-orm/node-postgres';
import { Pool } from 'pg';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

export const db = drizzle(pool);
```

**Type-Safe Queries:**
```typescript
// Type-safe query examples
const birdSpecies = await db
  .select()
  .from(species)
  .where(eq(species.family, 'Trochilidae'))
  .orderBy(species.commonNameEn);

const userVocabulary = await db
  .select({
    term: vocabulary.term,
    mastery: userProgress.masteryLevel
  })
  .from(vocabulary)
  .leftJoin(userProgress, eq(vocabulary.id, userProgress.vocabularyId))
  .where(eq(userProgress.userId, userId));
```

**Migration Management:**
```bash
# Drizzle migrations
npm run db:generate  # Generate migration from schema
npm run db:migrate   # Apply migrations
npm run db:drop      # Drop all tables
```

**Database Features:**
- JSONB storage for annotations
- Full-text search on definitions
- Foreign key constraints
- Indexes on frequently queried columns
- Materialized views for statistics

---

### 3. Other Potential PostgreSQL Uses

**Common Patterns Across Projects:**

**Connection Pooling:**
```javascript
// Node.js pg pool configuration
const pool = new Pool({
  user: process.env.DB_USER,
  host: process.env.DB_HOST,
  database: process.env.DB_NAME,
  password: process.env.DB_PASSWORD,
  port: 5432,
  max: 20,                    // Maximum pool size
  idleTimeoutMillis: 30000,   // Close idle clients after 30s
  connectionTimeoutMillis: 2000 // Timeout connection after 2s
});
```

**Transaction Management:**
```javascript
// Transaction example
const client = await pool.connect();
try {
  await client.query('BEGIN');
  await client.query('INSERT INTO ...');
  await client.query('UPDATE ...');
  await client.query('COMMIT');
} catch (e) {
  await client.query('ROLLBACK');
  throw e;
} finally {
  client.release();
}
```

---

## Database Performance Patterns

### Indexing Strategies
```sql
-- B-tree indexes for equality and range queries
CREATE INDEX idx_metrics_time ON metrics(time DESC);
CREATE INDEX idx_companies_ticker ON companies(ticker);

-- GIN indexes for JSONB
CREATE INDEX idx_annotations_data ON annotations USING GIN(annotations);

-- GiST indexes for full-text search
CREATE INDEX idx_vocabulary_search ON vocabulary USING GiST(to_tsvector('english', definition));

-- Partial indexes for filtered queries
CREATE INDEX idx_active_users ON user_progress(user_id) WHERE mastery_level > 0;
```

### Query Optimization
```sql
-- Use EXPLAIN ANALYZE for query planning
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM metrics
WHERE time > NOW() - INTERVAL '7 days';

-- Optimize JOIN order
-- Good: smaller table first
SELECT * FROM vocabulary v
JOIN user_progress up ON v.id = up.vocabulary_id
WHERE up.user_id = '123';

-- Use CTEs for complex queries
WITH recent_progress AS (
  SELECT * FROM user_progress
  WHERE last_reviewed > NOW() - INTERVAL '30 days'
)
SELECT * FROM recent_progress WHERE mastery_level > 3;
```

---

## Database Monitoring

### Performance Monitoring Queries
```sql
-- Slow queries
SELECT query, calls, mean_exec_time, max_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Table sizes
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Index usage
SELECT
  schemaname,
  tablename,
  indexname,
  idx_scan,
  idx_tup_read,
  idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan;
```

---

## Backup and Recovery

### Backup Strategies
```bash
# Logical backup (pg_dump)
pg_dump -Fc -f backup.dump dbname

# Parallel backup for large databases
pg_dump -Fc -j 4 -f backup.dump dbname

# Continuous archiving with WAL
archive_mode = on
archive_command = 'cp %p /backup/wal/%f'
```

### Recovery Procedures
```bash
# Restore from dump
pg_restore -d dbname backup.dump

# Point-in-time recovery
recovery_target_time = '2024-10-18 14:00:00'
```

---

## Security Configurations

### Connection Security
```sql
-- SSL enforcement
ALTER SYSTEM SET ssl = on;

-- Row Level Security example
ALTER TABLE user_progress ENABLE ROW LEVEL SECURITY;

CREATE POLICY user_own_data ON user_progress
  FOR ALL
  USING (user_id = current_user_id());
```

### User Management
```sql
-- Read-only user for reporting
CREATE ROLE readonly_user WITH LOGIN PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE dbname TO readonly_user;
GRANT USAGE ON SCHEMA public TO readonly_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly_user;
```

---

## Migration from Other Databases

### From SQLite to PostgreSQL
```bash
# Using pgloader
pgloader sqlite://source.db postgresql://user:pass@localhost/target
```

### Schema Migrations
```sql
-- Alembic for Python projects
alembic init migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

-- Drizzle for TypeScript projects
drizzle-kit generate:pg
drizzle-kit push:pg
```

---

## Cost Optimization

### Self-Hosted Considerations
- Hardware requirements: 4GB RAM minimum, SSD storage
- Backup storage costs
- Monitoring infrastructure
- Maintenance time

### Cloud Hosting Options
- AWS RDS PostgreSQL
- Google Cloud SQL
- Azure Database for PostgreSQL
- DigitalOcean Managed Databases

### Performance Tuning
```sql
-- Configuration tuning
shared_buffers = 256MB          # 25% of RAM
effective_cache_size = 1GB      # 50-75% of RAM
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
```

---

## Summary

Direct PostgreSQL implementations in the portfolio demonstrate:

1. **Advanced Features:** TimescaleDB for time-series, pgvector for embeddings
2. **ORM Integration:** Drizzle for type-safe queries
3. **Performance Optimization:** Indexing, partitioning, connection pooling
4. **Production Practices:** Migrations, backups, monitoring
5. **Security:** SSL, RLS, user management

Key differences from Supabase implementations:
- Direct database access and control
- Custom extension management
- Self-managed backups and security
- Greater flexibility in configuration
- Lower-level optimization capabilities

---

*End of PostgreSQL Direct Implementation Report*