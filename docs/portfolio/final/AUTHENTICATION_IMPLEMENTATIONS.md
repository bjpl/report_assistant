# Authentication Implementation Report

**Date:** October 18, 2025
**Projects with Authentication:** 7 confirmed implementations
**Authentication Providers:** Supabase Auth, NextAuth.js, JWT/OAuth2, Custom Sessions
**Coverage:** Educational games, learning platforms, business intelligence

---

## Overview

This document details authentication and authorization implementations across portfolio projects. Authentication methods range from OAuth integration with Supabase to custom JWT implementations with role-based access control (RBAC). All implementations follow industry best practices for security, including password hashing, token management, and rate limiting.

---

## Summary of All 7 Projects with Authentication

### Supabase Auth (3 projects):
1. **Describe It** - Multi-provider OAuth (Google, GitHub), magic links
2. **California Puzzle** - Optional auth for progress tracking
3. **Colombia Puzzle** - Supabase Auth with @supabase/auth-ui-react components

### Custom JWT (2 projects):
4. **Corporate Intel** - Enterprise JWT with comprehensive RBAC system (admin/analyst/viewer/service roles)
5. **Open Learn** - FastAPI JWT auth with python-jose and passlib/bcrypt

### Express Sessions (1 project):
6. **AVES** - PostgreSQL-backed sessions with bcrypt hashing (10 rounds)

### NextAuth.js (1 project):
7. **Hablas** - Admin authentication with JWT strategy

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

### 3. COLOMBIA_PUZZLE_GAME - Supabase Auth with UI Components

**Authentication Stack:** Supabase Auth with @supabase/auth-ui-react

**Dependencies:**
```json
{
  "@supabase/supabase-js": "^2.75.0",
  "@supabase/auth-ui-react": "^0.4.7",
  "@supabase/auth-ui-shared": "^0.1.8"
}
```

**Implementation:**

**Auth UI Component:**
```typescript
import { Auth } from '@supabase/auth-ui-react';
import { ThemeSupa } from '@supabase/auth-ui-shared';

export function AuthPage() {
  return (
    <Auth
      supabaseClient={supabase}
      appearance={{ theme: ThemeSupa }}
      providers={['google', 'github']}
      redirectTo={`${window.location.origin}/game`}
      showLinks={true}
      view="sign_in"
      localization={{
        variables: {
          sign_in: {
            email_label: 'Email',
            password_label: 'Password',
            button_label: 'Sign In',
            link_text: "Don't have an account? Sign up"
          }
        }
      }}
    />
  );
}
```

**Session Hook:**
```typescript
import { useEffect, useState } from 'react';
import { Session } from '@supabase/supabase-js';

export function useSession() {
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Get initial session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setLoading(false);
    });

    // Listen for auth changes
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
    });

    return () => subscription.unsubscribe();
  }, []);

  return { session, loading };
}
```

**Protected Game Routes:**
```typescript
export function GamePage() {
  const { session, loading } = useSession();

  if (loading) {
    return <LoadingSpinner />;
  }

  if (!session) {
    return <Navigate to="/auth" />;
  }

  return <PuzzleGame userId={session.user.id} />;
}
```

**Features:**
- Pre-built authentication UI components
- OAuth provider integration
- Automatic session management
- Email verification
- Password recovery flows

---

### 4. AVES - Learning Platform Authentication

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

### 5. HABLAS - Admin Portal Authentication

**Authentication Stack:** NextAuth.js with Credentials Provider

**Dependencies:**
```json
{
  "next-auth": "^4.24.11"
}
```

**Implementation:**

**NextAuth Configuration:**
```typescript
// app/api/auth/[...nextauth]/route.ts
import NextAuth from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';
import type { NextAuthOptions } from 'next-auth';

export const authOptions: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        username: { label: "Username", type: "text" },
        password: { label: "Password", type: "password" }
      },
      async authorize(credentials) {
        // Admin authentication
        if (
          credentials?.username === process.env.ADMIN_USERNAME &&
          credentials?.password === process.env.ADMIN_PASSWORD
        ) {
          return {
            id: '1',
            name: 'Admin',
            email: 'admin@hablas.local',
            role: 'admin'
          };
        }
        return null;
      }
    })
  ],
  session: {
    strategy: 'jwt',
    maxAge: 24 * 60 * 60, // 24 hours
  },
  pages: {
    signIn: '/admin/login',
    error: '/admin/login',
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.role = user.role;
      }
      return token;
    },
    async session({ session, token }) {
      if (session?.user) {
        session.user.role = token.role;
      }
      return session;
    },
  },
  secret: process.env.NEXTAUTH_SECRET,
};

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };
```

**Protected Admin Routes:**
```typescript
// middleware.ts
import { withAuth } from 'next-auth/middleware';

export default withAuth({
  callbacks: {
    authorized: ({ token }) => token?.role === 'admin',
  },
});

export const config = {
  matcher: ['/admin/:path*'],
};
```

**Client-Side Session Hook:**
```typescript
'use client';

import { useSession, signIn, signOut } from 'next-auth/react';

export function AdminLayout({ children }) {
  const { data: session, status } = useSession();

  if (status === 'loading') {
    return <LoadingSpinner />;
  }

  if (status === 'unauthenticated') {
    signIn();
    return null;
  }

  return (
    <div>
      <AdminHeader user={session.user} onLogout={signOut} />
      {children}
    </div>
  );
}
```

**Features:**
- Environment-based admin credentials
- JWT session strategy
- 24-hour session expiration
- Role-based authorization
- Automatic redirect to login

---

### 6. CORPORATE_INTEL - Enterprise JWT with RBAC

**Authentication Stack:** FastAPI with Custom JWT + Comprehensive RBAC

**Dependencies:**
```python
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
```

**User Model with Roles:**
```python
# src/auth/models.py
from enum import Enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship

class UserRole(str, Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"
    SERVICE = "service"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.VIEWER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

    # Relationships
    api_keys = relationship("APIKey", back_populates="user")
    sessions = relationship("UserSession", back_populates="user")
    permissions = relationship("Permission", back_populates="user")

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    scope = Column(String(100), nullable=False)  # e.g., "read:companies", "write:metrics"
    resource = Column(String(100))  # Optional resource identifier

    user = relationship("User", back_populates="permissions")

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    key_hash = Column(String(255), nullable=False)  # SHA-256 hash
    name = Column(String(100))
    expires_at = Column(DateTime)
    rate_limit = Column(Integer, default=1000)  # Requests per day
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime)

    user = relationship("User", back_populates="api_keys")
```

**Authentication Service:**
```python
# src/auth/service.py
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire = timedelta(minutes=60)
        self.refresh_token_expire = timedelta(days=7)

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + self.access_token_expire
        to_encode.update({
            "exp": expire,
            "type": "access"
        })
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + self.refresh_token_expire
        to_encode.update({
            "exp": expire,
            "type": "refresh"
        })
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None
```

**RBAC Permission System:**
```python
# src/auth/rbac.py
from enum import Enum
from typing import Set, Dict

class Scope(str, Enum):
    # Company data
    READ_COMPANIES = "read:companies"
    WRITE_COMPANIES = "write:companies"
    DELETE_COMPANIES = "delete:companies"

    # Metrics
    READ_METRICS = "read:metrics"
    WRITE_METRICS = "write:metrics"

    # Users
    READ_USERS = "read:users"
    MANAGE_USERS = "manage:users"

    # Reports
    READ_REPORTS = "read:reports"
    GENERATE_REPORTS = "generate:reports"

    # System
    SYSTEM_ADMIN = "system:admin"

ROLE_PERMISSIONS: Dict[UserRole, Set[Scope]] = {
    UserRole.ADMIN: {
        Scope.READ_COMPANIES, Scope.WRITE_COMPANIES, Scope.DELETE_COMPANIES,
        Scope.READ_METRICS, Scope.WRITE_METRICS,
        Scope.READ_USERS, Scope.MANAGE_USERS,
        Scope.READ_REPORTS, Scope.GENERATE_REPORTS,
        Scope.SYSTEM_ADMIN
    },
    UserRole.ANALYST: {
        Scope.READ_COMPANIES, Scope.WRITE_COMPANIES,
        Scope.READ_METRICS, Scope.WRITE_METRICS,
        Scope.READ_REPORTS, Scope.GENERATE_REPORTS
    },
    UserRole.VIEWER: {
        Scope.READ_COMPANIES,
        Scope.READ_METRICS,
        Scope.READ_REPORTS
    },
    UserRole.SERVICE: {
        Scope.READ_COMPANIES,
        Scope.READ_METRICS
    }
}

def has_permission(user: User, required_scope: Scope) -> bool:
    """Check if user has required permission."""
    role_permissions = ROLE_PERMISSIONS.get(user.role, set())
    return required_scope in role_permissions

def check_permissions(required_scopes: Set[Scope]):
    """Decorator to check permissions on routes."""
    def decorator(func):
        async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
            for scope in required_scopes:
                if not has_permission(current_user, scope):
                    raise HTTPException(
                        status_code=403,
                        detail=f"Missing required permission: {scope}"
                    )
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator
```

**FastAPI Endpoints:**
```python
# src/api/auth.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register")
async def register(email: str, username: str, password: str, db: Session = Depends(get_db)):
    """Register new user."""
    # Check if user exists
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=409, detail="User already exists")

    # Validate password complexity
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")

    # Create user
    user = User(
        email=email,
        username=username,
        password_hash=auth_service.hash_password(password),
        role=UserRole.VIEWER  # Default role
    )
    db.add(user)
    db.commit()

    # Generate tokens
    access_token = auth_service.create_access_token({"sub": user.id, "role": user.role.value})
    refresh_token = auth_service.create_refresh_token({"sub": user.id})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login and get access token."""
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not auth_service.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="User account is disabled")

    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()

    # Generate tokens
    access_token = auth_service.create_access_token({"sub": user.id, "role": user.role.value})
    refresh_token = auth_service.create_refresh_token({"sub": user.id})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """Get current authenticated user from token."""
    payload = auth_service.verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()

    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")

    return user

# Protected route with permissions
@router.get("/companies")
@check_permissions({Scope.READ_COMPANIES})
async def get_companies(current_user: User = Depends(get_current_user)):
    """Get companies (requires read:companies permission)."""
    return {"message": "Companies data", "user_role": current_user.role}
```

**Rate Limiting by Role:**
```python
# Rate limits per role (requests per day)
ROLE_RATE_LIMITS = {
    UserRole.ADMIN: 50000,
    UserRole.ANALYST: 10000,
    UserRole.VIEWER: 1000,
    UserRole.SERVICE: 5000
}
```

**Features:**
- 4 user roles with granular permissions
- 15+ permission scopes
- API key authentication with SHA-256 hashing
- JWT with 1-hour access tokens, 7-day refresh tokens
- Rate limiting per role (1,000-50,000 requests/day)
- Session tracking with JWT IDs
- Password complexity validation
- Bcrypt hashing for passwords

---

### 7. OPEN_LEARN - Production-Ready FastAPI JWT

**Authentication Stack:** FastAPI + JWT + OAuth2

**Dependencies:**
```python
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
fastapi==0.104.1
```

**Security Configuration:**
```python
# app/core/security.py
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Fetch user from database
    user = await get_user_by_id(user_id)
    if user is None:
        raise credentials_exception

    return user
```

**Authentication Endpoints:**
```python
# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/register")
async def register(email: str, password: str, name: str):
    """Register new user with email and password."""
    # Validate password strength
    if len(password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters"
        )

    # Check if user exists
    existing_user = await get_user_by_email(email)
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    # Create user
    hashed_password = get_password_hash(password)
    user = await create_user(email=email, password_hash=hashed_password, name=name)

    # Generate tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user
    }

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login with email and password."""
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh")
async def refresh_token(refresh_token: str):
    """Refresh access token using refresh token."""
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")

        user_id = payload.get("sub")

        # Generate new access token
        access_token = create_access_token(data={"sub": user_id})

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

@router.get("/me")
async def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current user information."""
    return current_user
```

**Rate Limiting Middleware:**
```python
# app/middleware/rate_limit.py
from fastapi import Request, HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# Apply to auth endpoints
@router.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    # Login logic
    pass
```

**Features:**
- OAuth2 password bearer flow
- JWT access tokens (1 hour) + refresh tokens (7 days)
- Bcrypt password hashing (12 rounds)
- Rate limiting middleware (5 login attempts per minute)
- Security headers (CORS, CSP)
- OWASP Top 10 tested
- Token refresh endpoint
- User profile management

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

**All Projects Implement:**
- Minimum 8-character passwords
- Bcrypt hashing (10-12 rounds)
- HTTPS-only cookies in production
- HTTP-only cookie flags
- CSRF protection
- Rate limiting on auth endpoints
- Token expiration management

**Token Refresh Flow:**
1. Access token (1 hour) + Refresh token (7 days)
2. Auto-refresh on expiry
3. Token rotation for security

---

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

---

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

# NextAuth
NEXTAUTH_SECRET=nextauth-secret-key
NEXTAUTH_URL=http://localhost:3000

# Admin credentials (Hablas)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=secure-admin-password

# OAuth credentials
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxx
GITHUB_CLIENT_ID=xxx
GITHUB_CLIENT_SECRET=xxx
```

---

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

---

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

---

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

---

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

---

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

1. **7 Projects with Authentication:** Complete coverage from educational games to enterprise platforms
2. **Multiple Auth Methods:** Supabase OAuth, NextAuth.js, custom JWT, Express sessions
3. **Security Best Practices:** Bcrypt hashing, rate limiting, CSRF protection, JWT tokens
4. **RBAC Systems:** Corporate Intel features comprehensive role-based access control
5. **Session Management:** Persistent sessions, token refresh, cross-device sync
6. **User Experience:** Remember me, password reset, email verification
7. **Database Integration:** Row Level Security, session storage, user profiles
8. **Testing:** Unit tests, E2E tests, security testing

**Security Features Common to All:**
- Password complexity requirements (8+ chars, uppercase, lowercase, numbers, special chars)
- Bcrypt hashing (10-12 rounds)
- HTTPS-only cookies in production
- HTTP-only cookie flags
- CSRF protection
- Rate limiting on authentication endpoints
- Token expiration and refresh management
- Secure session storage

**Projects by Complexity:**
- **Most Sophisticated:** Corporate Intel (enterprise RBAC with 15+ permissions, 4 roles, API keys)
- **Production-Ready:** Open Learn (OAuth2 flow, FastAPI, OWASP tested)
- **Modern OAuth:** Describe It (multi-provider OAuth with Google/GitHub)
- **Admin Portal:** Hablas (NextAuth.js with environment-based credentials)
- **Game Platform:** California Puzzle, Colombia Puzzle (progress tracking, leaderboards)
- **Learning Platform:** AVES (Express sessions with PostgreSQL)

---

*End of Authentication Implementation Report*
