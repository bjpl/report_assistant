# Authentication Implementation Report

**Date:** October 18, 2025
**Projects with Authentication:** 3+ confirmed implementations
**Authentication Providers:** Supabase Auth, JWT, OAuth, Custom

---

## Overview

This document details authentication and authorization implementations across portfolio projects. Authentication methods range from OAuth integration to custom JWT implementations, with varying levels of security and user management features.

---

## Projects with Authentication Features

### 1. DESCRIBE_IT - Multi-Provider Authentication

**Authentication Stack:** Supabase Auth with OAuth integration

**Supported Authentication Methods:**
- Email/password authentication
- OAuth providers (Google, GitHub)
- Magic link email authentication
- JWT token-based sessions

**Implementation Details:**

**Supabase Client Setup:**
```typescript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
  {
    auth: {
      autoRefreshToken: true,
      persistSession: true,
      detectSessionInUrl: true
    }
  }
);
```

**Authentication Flow:**

1. **Email/Password Registration:**
```typescript
async function signUp(email: string, password: string) {
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
    options: {
      emailRedirectTo: `${window.location.origin}/auth/callback`
    }
  });

  if (error) throw error;
  return data;
}
```

2. **OAuth Sign-In:**
```typescript
async function signInWithProvider(provider: 'google' | 'github') {
  const { data, error } = await supabase.auth.signInWithOAuth({
    provider,
    options: {
      redirectTo: `${window.location.origin}/auth/callback`,
      scopes: 'email profile'
    }
  });

  if (error) throw error;
  return data;
}
```

3. **Magic Link:**
```typescript
async function signInWithMagicLink(email: string) {
  const { error } = await supabase.auth.signInWithOtp({
    email,
    options: {
      emailRedirectTo: `${window.location.origin}/auth/callback`
    }
  });

  if (error) throw error;
}
```

**Session Management:**
```typescript
// Session persistence in Next.js
export async function getServerSession() {
  const supabase = createServerClient();
  const { data: { session } } = await supabase.auth.getSession();
  return session;
}

// Client-side session hook
export function useAuth() {
  const [session, setSession] = useState(null);

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        setSession(session);
      }
    );

    return () => subscription.unsubscribe();
  }, []);

  return session;
}
```

**Protected Routes:**
```typescript
// Middleware for protected routes
export async function middleware(request: NextRequest) {
  const session = await getServerSession();

  if (!session) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/sessions/:path*']
};
```

**JWT Token Handling:**
```typescript
// Access JWT from session
const token = session?.access_token;

// Refresh token handling
async function refreshSession() {
  const { data, error } = await supabase.auth.refreshSession();
  return data.session;
}

// Token expiry check
function isTokenExpired(token: string): boolean {
  const decoded = jwt.decode(token);
  return decoded.exp < Date.now() / 1000;
}
```

**Row Level Security Integration:**
```sql
-- RLS policies for user data
CREATE POLICY "Users can view own sessions"
  ON sessions
  FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own sessions"
  ON sessions
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);
```

**Security Features:**
- Password strength requirements
- Email verification required
- Rate limiting on login attempts
- CSRF protection
- Secure cookie settings (httpOnly, secure, sameSite)

---

### 2. CALIFORNIA_PUZZLE_GAME - User Progress Authentication

**Authentication Stack:** Supabase Auth

**Authentication Purpose:**
- User registration for progress tracking
- Leaderboard identity verification
- Achievement system
- Cross-device progress synchronization

**Implementation:**

**User Registration Flow:**
```typescript
async function createAccount(email: string, username: string, password: string) {
  // Create auth user
  const { data: authData, error: authError } = await supabase.auth.signUp({
    email,
    password,
    options: {
      data: {
        username,
        display_name: username
      }
    }
  });

  if (authError) throw authError;

  // Create user profile
  const { error: profileError } = await supabase
    .from('profiles')
    .insert({
      id: authData.user.id,
      username,
      created_at: new Date().toISOString()
    });

  if (profileError) throw profileError;
}
```

**Session-Based Progress Tracking:**
```typescript
async function saveGameProgress(gameData: GameProgress) {
  const session = await supabase.auth.getSession();

  if (!session) {
    // Save to local storage for guest users
    localStorage.setItem('game_progress', JSON.stringify(gameData));
    return;
  }

  // Save to database for authenticated users
  await supabase
    .from('game_progress')
    .upsert({
      user_id: session.user.id,
      level_completed: gameData.level,
      score: gameData.score,
      time: gameData.time,
      updated_at: new Date().toISOString()
    });
}
```

**Guest vs Authenticated Features:**
```typescript
interface UserFeatures {
  canSaveProgress: boolean;
  canViewLeaderboard: boolean;
  canEarnAchievements: boolean;
  canSyncAcrossDevices: boolean;
}

function getUserFeatures(isAuthenticated: boolean): UserFeatures {
  if (isAuthenticated) {
    return {
      canSaveProgress: true,
      canViewLeaderboard: true,
      canEarnAchievements: true,
      canSyncAcrossDevices: true
    };
  }

  return {
    canSaveProgress: true,  // Local storage only
    canViewLeaderboard: false,
    canEarnAchievements: false,
    canSyncAcrossDevices: false
  };
}
```

**Anonymous to Authenticated Conversion:**
```typescript
async function migrateGuestData() {
  const guestProgress = localStorage.getItem('game_progress');

  if (!guestProgress) return;

  const session = await supabase.auth.getSession();
  if (!session) return;

  // Migrate local progress to user account
  const progress = JSON.parse(guestProgress);
  await saveGameProgress(progress);

  // Clear local storage
  localStorage.removeItem('game_progress');
}
```

---

### 3. AVES - Learning Platform Authentication

**Authentication Stack:** Express sessions with PostgreSQL storage

**Implementation Type:** Custom session-based authentication

**Database Schema:**
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  username VARCHAR(100),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  last_login TIMESTAMPTZ,
  email_verified BOOLEAN DEFAULT FALSE
);

CREATE TABLE sessions (
  sid VARCHAR(255) PRIMARY KEY,
  sess JSON NOT NULL,
  expire TIMESTAMPTZ NOT NULL
);

CREATE INDEX idx_sessions_expire ON sessions(expire);
```

**Express Session Configuration:**
```typescript
import session from 'express-session';
import connectPg from 'connect-pg-simple';

const PgSession = connectPg(session);

app.use(session({
  store: new PgSession({
    pool: pgPool,
    tableName: 'sessions',
    createTableIfMissing: true
  }),
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: {
    maxAge: 30 * 24 * 60 * 60 * 1000, // 30 days
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax'
  }
}));
```

**Password Hashing:**
```typescript
import bcrypt from 'bcrypt';

const SALT_ROUNDS = 10;

async function hashPassword(password: string): Promise<string> {
  return bcrypt.hash(password, SALT_ROUNDS);
}

async function verifyPassword(password: string, hash: string): Promise<boolean> {
  return bcrypt.compare(password, hash);
}
```

**Registration Endpoint:**
```typescript
app.post('/api/auth/register', async (req, res) => {
  const { email, password, username } = req.body;

  // Validate input
  if (!email || !password) {
    return res.status(400).json({ error: 'Email and password required' });
  }

  // Check if user exists
  const existingUser = await db
    .select()
    .from(users)
    .where(eq(users.email, email))
    .limit(1);

  if (existingUser.length > 0) {
    return res.status(409).json({ error: 'User already exists' });
  }

  // Hash password and create user
  const passwordHash = await hashPassword(password);
  const [newUser] = await db
    .insert(users)
    .values({
      email,
      password_hash: passwordHash,
      username
    })
    .returning();

  // Create session
  req.session.userId = newUser.id;

  res.status(201).json({
    user: {
      id: newUser.id,
      email: newUser.email,
      username: newUser.username
    }
  });
});
```

**Login Endpoint:**
```typescript
app.post('/api/auth/login', async (req, res) => {
  const { email, password } = req.body;

  // Find user
  const [user] = await db
    .select()
    .from(users)
    .where(eq(users.email, email))
    .limit(1);

  if (!user) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  // Verify password
  const isValid = await verifyPassword(password, user.password_hash);

  if (!isValid) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  // Update last login
  await db
    .update(users)
    .set({ last_login: new Date() })
    .where(eq(users.id, user.id));

  // Create session
  req.session.userId = user.id;

  res.json({
    user: {
      id: user.id,
      email: user.email,
      username: user.username
    }
  });
});
```

**Authentication Middleware:**
```typescript
function requireAuth(req: Request, res: Response, next: NextFunction) {
  if (!req.session.userId) {
    return res.status(401).json({ error: 'Authentication required' });
  }
  next();
}

// Protected route example
app.get('/api/user/progress', requireAuth, async (req, res) => {
  const progress = await getUserProgress(req.session.userId);
  res.json(progress);
});
```

**Logout:**
```typescript
app.post('/api/auth/logout', (req, res) => {
  req.session.destroy((err) => {
    if (err) {
      return res.status(500).json({ error: 'Logout failed' });
    }
    res.clearCookie('connect.sid');
    res.json({ message: 'Logged out successfully' });
  });
});
```

---

## Common Authentication Patterns

### Password Security Best Practices

**Password Requirements:**
```typescript
interface PasswordRequirements {
  minLength: 8;
  requireUppercase: true;
  requireLowercase: true;
  requireNumber: true;
  requireSpecialChar: true;
}

function validatePassword(password: string): boolean {
  const hasMinLength = password.length >= 8;
  const hasUppercase = /[A-Z]/.test(password);
  const hasLowercase = /[a-z]/.test(password);
  const hasNumber = /[0-9]/.test(password);
  const hasSpecial = /[!@#$%^&*]/.test(password);

  return hasMinLength && hasUppercase && hasLowercase && hasNumber && hasSpecial;
}
```

### Rate Limiting

**Login Attempt Limiting:**
```typescript
import rateLimit from 'express-rate-limit';

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts
  message: 'Too many login attempts, please try again later',
  standardHeaders: true,
  legacyHeaders: false
});

app.post('/api/auth/login', loginLimiter, loginHandler);
```

### CSRF Protection

**Token Generation and Validation:**
```typescript
import csrf from 'csurf';

const csrfProtection = csrf({ cookie: true });

app.get('/api/csrf-token', csrfProtection, (req, res) => {
  res.json({ csrfToken: req.csrfToken() });
});

app.post('/api/auth/login', csrfProtection, loginHandler);
```

---

## Security Implementations

### Environment Variable Management
```env
# Supabase projects
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJxxx
SUPABASE_SERVICE_ROLE_KEY=eyJxxx

# Custom auth
SESSION_SECRET=random-secret-string-here
JWT_SECRET=another-secret-string
DATABASE_URL=postgresql://user:pass@localhost:5432/db

# OAuth credentials
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxx
GITHUB_CLIENT_ID=xxx
GITHUB_CLIENT_SECRET=xxx
```

### Token Storage

**Client-Side:**
```typescript
// Secure token storage
class SecureStorage {
  private static readonly TOKEN_KEY = 'auth_token';

  static setToken(token: string) {
    // Use httpOnly cookie when possible
    // Fallback to sessionStorage (not localStorage for security)
    sessionStorage.setItem(this.TOKEN_KEY, token);
  }

  static getToken(): string | null {
    return sessionStorage.getItem(this.TOKEN_KEY);
  }

  static removeToken() {
    sessionStorage.removeItem(this.TOKEN_KEY);
  }
}
```

### API Request Authentication

**Axios Interceptor:**
```typescript
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL
});

apiClient.interceptors.request.use(
  async (config) => {
    const session = await supabase.auth.getSession();
    if (session?.access_token) {
      config.headers.Authorization = `Bearer ${session.access_token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token expired, attempt refresh
      const { data } = await supabase.auth.refreshSession();
      if (data.session) {
        // Retry original request
        error.config.headers.Authorization = `Bearer ${data.session.access_token}`;
        return axios.request(error.config);
      }
    }
    return Promise.reject(error);
  }
);
```

---

## User Experience Features

### Remember Me Functionality
```typescript
async function login(email: string, password: string, rememberMe: boolean) {
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password
  });

  if (error) throw error;

  if (rememberMe) {
    // Extend session duration
    await supabase.auth.setSession({
      access_token: data.session.access_token,
      refresh_token: data.session.refresh_token
    });
  }
}
```

### Password Reset Flow
```typescript
// Send reset email
async function requestPasswordReset(email: string) {
  const { error } = await supabase.auth.resetPasswordForEmail(email, {
    redirectTo: `${window.location.origin}/auth/reset-password`
  });

  if (error) throw error;
}

// Handle reset with token
async function resetPassword(token: string, newPassword: string) {
  const { error } = await supabase.auth.updateUser({
    password: newPassword
  });

  if (error) throw error;
}
```

### Email Verification
```typescript
async function sendVerificationEmail(userId: string) {
  const { error } = await supabase.auth.resend({
    type: 'signup',
    email: userEmail
  });

  if (error) throw error;
}
```

---

## Testing Authentication

### Unit Tests
```typescript
describe('Authentication', () => {
  it('registers new user', async () => {
    const result = await signUp('test@example.com', 'Password123!');
    expect(result.user).toBeDefined();
    expect(result.session).toBeDefined();
  });

  it('rejects weak password', async () => {
    await expect(
      signUp('test@example.com', 'weak')
    ).rejects.toThrow('Password does not meet requirements');
  });

  it('prevents duplicate registration', async () => {
    await signUp('test@example.com', 'Password123!');
    await expect(
      signUp('test@example.com', 'Password123!')
    ).rejects.toThrow('User already exists');
  });
});
```

### E2E Tests
```typescript
test('complete login flow', async ({ page }) => {
  await page.goto('/login');

  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[name="password"]', 'Password123!');
  await page.click('button[type="submit"]');

  await expect(page).toHaveURL('/dashboard');
  await expect(page.locator('text=Welcome back')).toBeVisible();
});
```

---

## Summary

Authentication implementations across the portfolio demonstrate:

1. **Multiple Auth Methods:** Email/password, OAuth, magic links, custom sessions
2. **Security Best Practices:** Password hashing, rate limiting, CSRF protection, JWT
3. **Session Management:** Persistent sessions, token refresh, cross-device sync
4. **User Experience:** Remember me, password reset, email verification
5. **Database Integration:** Row Level Security, session storage, user profiles

Projects use different approaches based on requirements:
- **Describe It:** Full OAuth integration for collaboration features
- **California Puzzle:** Optional auth for progress tracking
- **AVES:** Custom Express sessions for learning platform

---

*End of Authentication Implementation Report*