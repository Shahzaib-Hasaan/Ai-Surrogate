# Sprint 1 - Week 1: Foundation Setup
**AI Surrogate Human Clone - Development Plan**

> **Week**: December 24-30, 2024  
> **Goal**: Setup complete development environment and basic backend  
> **Status**: In Progress ✅

---

## ✅ Completed Tasks

### Day 1 - December 24, 2024

#### Environment Setup
- [x] Created Expo mobile app: `ai-surrogate-mobile`
  - Template: `blank-typescript`
  - Dependencies installed successfully
  - Project structure initialized
  
- [x] Created implementation roadmap
  - 15-week sprint plan
  - Detailed task breakdown
  - Success metrics defined

---

## 📋 Remaining Tasks for Week 1

### Day 1 (Today) - Backend Foundation

#### Task 1: Create Backend Structure
```bash
# Create backend directory structure
mkdir ai-surrogate-backend
cd ai-surrogate-backend

# Create Python virtual environment
python -m venv venv

# Create folder structure
mkdir app
mkdir app/models
mkdir app/schemas
mkdir app/routes
mkdir app/services
mkdir tests
```

**Create these files**:
```
ai-surrogate-backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── message.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user_schema.py
│   │   └── message_schema.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── chat.py
│   └── services/
│       ├── __init__.py
│       ├── auth_service.py
│       └── chat_service.py
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   └── test_chat.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

#### Task 2: Install Backend Dependencies
Create `requirements.txt`:
```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
psycopg2-binary==2.9.9
pydantic==2.5.3
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
python-dotenv==1.0.0
alembic==1.13.1
redis==5.0.1
```

Install dependencies:
```bash
# Activate virtual environment (Windows)
.\venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

#### Task 3: Setup Supabase Database
1. Go to https://supabase.com
2. Create new project: "ai-surrogate"
3. Get database connection string
4. Create `.env` file:
```env
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
SECRET_KEY=your-secret-jwt-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=43200
```

#### Task 4: Create Database Models (Using Cursor AI)

**Prompt for Cursor**:
```
Create SQLAlchemy models for the AI Surrogate backend in app/models/:

1. user.py - User model with:
   - id: UUID primary key (use uuid4)
   - email: unique string, indexed
   - username: unique string, indexed
   - hashed_password: string
   - created_at: timestamp with default now()
   - updated_at: timestamp with default now(), on update now()
   - is_active: boolean, default True

2. message.py - Message model with:
   - id: UUID primary key (use uuid4)
   - user_id: UUID foreign key to User
   - content: text
   - is_from_user: boolean
   - created_at: timestamp with default now()
   - conversation_id: UUID

3. conversation.py - Conversation model with:
   - id: UUID primary key (use uuid4)
   - user_id: UUID foreign key to User
   - title: optional string
   - created_at: timestamp with default now()
   - updated_at: timestamp with default now()

Include:
- Proper SQLAlchemy relationships
- Indexes for queries
- __repr__ methods
- Type hints
```

**Expected Files**:
- `app/models/__init__.py`
- `app/models/user.py`
- `app/models/message.py`
- `app/models/conversation.py`

---

### Day 2 - Backend API Foundation

#### Task 5: Create Pydantic Schemas

**Prompt for Cursor**:
```
Create Pydantic schemas for request/response validation:

1. app/schemas/user_schema.py:
   - UserCreate (email, username, password with min length 8)
   - UserLogin (email, password)
   - UserResponse (id, email, username, created_at) - exclude password
   - Token (access_token, token_type="bearer")

2. app/schemas/message_schema.py:
   - MessageCreate (content: str with min length 1, conversation_id: optional UUID)
   - MessageResponse (id, content, is_from_user, created_at)

3. app/schemas/conversation_schema.py:
   - ConversationCreate (title: optional str)
   - ConversationResponse (id, title, created_at, message_count)
   - ConversationWithMessages (extends ConversationResponse, adds messages: list)

Include:
- Field validation
- Example values for OpenAPI docs
- ConfigDict with from_attributes=True
```

#### Task 6: Authentication Service

**Prompt for Cursor**:
```
Create authentication service in app/services/auth_service.py:

Functions:
1. hash_password(password: str) -> str
   - Use bcrypt from passlib

2. verify_password(plain: str, hashed: str) -> bool
   - Compare passwords

3. create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str
   - Create JWT token with 30-day expiration
   - Use SECRET_KEY from environment

4. verify_token(token: str) -> dict
   - Decode JWT
   - Raise HTTPException if invalid

5. get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session) -> User
   - Extract user from token
   - Query database
   - Return User model

Include:
- Type hints
- Error handling
- Docstrings
```

---

### Day 3 - API Routes

#### Task 7: Authentication Routes

**Prompt for Cursor**:
```
Create authentication endpoints in app/routes/auth.py:

Endpoints:

1. POST /api/auth/register
   - Input: UserCreate
   - Check if email/username exists
   - Hash password
   - Create user in database
   - Generate JWT token
   - Return: UserResponse + access_token
   - Status: 201 Created

2. POST /api/auth/login
   - Input: UserLogin
   - Find user by email
   - Verify password
   - Generate JWT token
   - Return: Token
   - Status: 200 OK

3. GET /api/auth/me
   - Requires: JWT token in Authorization header
   - Get current user from token
   - Return: UserResponse
   - Status: 200 OK

Include:
- Proper error handling (401, 404, 409)
- Dependencies: get_db for database session
- OpenAPI tags and descriptions
- Response models
```

#### Task 8: Basic Chat Route

**Prompt for Cursor**:
```
Create basic chat endpoint in app/routes/chat.py:

Endpoints:

1. POST /api/chat/message
   - Requires: JWT authentication
   - Input: MessageCreate
   - Process:
     a. Save user message to database
     b. Create echo response: "Echo: {content}"
     c. Save AI response to database
   - Return: MessageResponse (the AI response)
   - Status: 201 Created

2. GET /api/chat/conversations
   - Requires: JWT authentication
   - Get all user's conversations
   - Return: List[ConversationResponse]
   - Status: 200 OK

3. GET /api/chat/conversations/{conversation_id}/messages
   - Requires: JWT authentication
   - Get all messages in conversation
   - Return: List[MessageResponse]
   - Status: 200 OK

Note: Use echo responses for now. Real AI in Phase 2.

Include:
- get_current_user dependency
- Error handling
- Pagination (limit 50 messages)
```

---

### Day 4 - FastAPI Main App

#### Task 9: Database Configuration

**Prompt for Cursor**:
```
Create database configuration in app/database.py:

Requirements:
1. Create SQLAlchemy engine from DATABASE_URL
2. Create SessionLocal factory
3. Create Base for models
4. Create get_db() dependency that yields session
5. Add connection pooling
6. Add error handling for database connection

Include proper type hints and docstrings.
```

#### Task 10: Main FastAPI App

**Prompt for Cursor**:
```
Create main FastAPI application in app/main.py:

Requirements:
1. Initialize FastAPI with:
   - title: "AI Surrogate API"
   - version: "1.0.0"
   - description: "Backend API for AI Surrogate Human Clone mobile app"

2. Configure CORS:
   - allow_origins: ["*"] (for development)
   - allow_credentials: True
   - allow_methods: ["*"]
   - allow_headers: ["*"]

3. Include routers:
   - app.routes.auth with prefix="/api/auth" and tag="Authentication"
   - app.routes.chat with prefix="/api/chat" and tag="Chat"

4. Add lifespan context manager:
   - On startup: Create database tables
   - On shutdown: Dispose engine

5. Add health check:
   - GET /health
   - Return: {"status": "healthy", "timestamp": current_time}

6. Add global exception handler

Include:
- Proper imports
- CORS middleware
- Logging configuration
```

---

### Day 5 - Testing & Integration

#### Task 11: Manual API Testing
1. Run backend server:
```bash
cd ai-surrogate-backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

2. Open Swagger UI: http://localhost:8000/docs

3. Test endpoints:
   - [ ] POST /api/auth/register - Create test user
   - [ ] POST /api/auth/login - Get JWT token
   - [ ] GET /api/auth/me - Verify token works
   - [ ] POST /api/chat/message - Send a message
   - [ ] GET /api/chat/conversations - List conversations

#### Task 12: Deploy Backend to Railway.app
1. Go to https://railway.app
2. Create new project
3. Deploy from GitHub (push backend code)
4. Add environment variables
5. Get deployment URL
6. Test API with deployed URL

---

### Weekend (Days 6-7) - Mobile App Setup

#### Task 13: Install Mobile Dependencies
```bash
cd ai-surrogate-mobile

# Navigation
npx expo install @react-navigation/native @react-navigation/stack
npx expo install react-native-screens react-native-safe-area-context

# UI Components
npx expo install react-native-paper

# State Management
npm install zustand

# API & Data
npm install axios @tanstack/react-query

# Storage
npx expo install expo-secure-store @react-native-async-storage/async-storage

# Forms
npm install react-hook-form zod @hookform/resolvers
```

#### Task 14: Create Folder Structure
```bash
cd ai-surrogate-mobile
mkdir src
mkdir src/components
mkdir src/screens
mkdir src/services
mkdir src/store
mkdir src/types
mkdir src/utils
```

#### Task 15: Create TypeScript Types

**Create `src/types/index.ts`**:
```typescript
export interface User {
  id: string;
  email: string;
  username: string;
  createdAt: string;
}

export interface Message {
  id: string;
  content: string;
  isFromUser: boolean;
  createdAt: string;
}

export interface Conversation {
  id: string;
  title?: string;
  createdAt: string;
  messages?: Message[];
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface ApiError {
  detail: string;
}
```

#### Task 16: Create API Service

**Create `src/services/api.ts`** (Use Cursor):
```
Create Axios instance for API calls:
- Base URL from environment variable
- Request interceptor to add JWT token
- Response interceptor for error handling
- Retry logic for network errors
```

**Create `src/services/authService.ts`** (Use Cursor):
```
Create auth service with:
- register(email, username, password)
- login(email, password)
- getProfile()
- logout()
All functions should use the api instance and return properly typed responses.
```

---

## 🎯 Week 1 Success Criteria

By end of Week 1, you should have:
- ✅ Expo mobile app initialized
- ✅ Backend API with FastAPI running
- ✅ Database models created
- ✅ Authentication endpoints working
- ✅ Basic chat endpoint (echo) working
- ✅ API documentation at /docs
- ✅ Backend deployed to Railway.app
- ✅ Mobile app dependencies installed
- ✅ API service layer created

---

## 🚀 Testing Checklist

### Backend Tests
- [ ] Can register new user
- [ ] Can login with credentials
- [ ] JWT token works for /me endpoint
- [ ] Can send message and get echo response
- [ ] Conversations are created automatically
- [ ] Messages are stored in database

### Mobile App Tests (Week 2)
- [ ] App starts without errors
- [ ] Can navigate between screens
- [ ] API service connects to backend

---

## 📝 Daily Progress Log

### December 24, 2024
- [x] Initialized Expo project
- [x] Created implementation roadmap
- [x] Created Week 1 plan
- [ ] Setup backend structure
- [ ] Install backend dependencies
- [ ] Create database models

### December 25, 2024
- [ ] Create Pydantic schemas
- [ ] Create auth service
- [ ] Setup database connection

### December 26, 2024
- [ ] Create authentication routes
- [ ] Create chat routes
- [ ] Test endpoints

### December 27, 2024
- [ ] Create main FastAPI app
- [ ] Test all endpoints
- [ ] Fix any bugs

### December 28, 2024
- [ ] Deploy to Railway.app
- [ ] Test deployed API
- [ ] Setup mobile dependencies

### December 29-30, 2024 (Weekend)
- [ ] Create mobile folder structure
- [ ] Setup API service layer
- [ ] Create TypeScript types
- [ ] Review week progress

---

## 🔗 Resources

### Documentation
- **FastAPI Tutorial**: https://fastapi.tiangolo.com/tutorial/
- **SQLAlchemy ORM**: https://docs.sqlalchemy.org/en/20/orm/
- **Supabase Docs**: https://supabase.com/docs
- **Railway.app Docs**: https://docs.railway.app/

### Tools
- **Cursor IDE**: Use AI to generate code
- **Postman/Thunder Client**: Test API endpoints
- **Expo Go**: Test mobile app on phone

---

**Next Week Preview**: Week 2 will focus on creating the mobile app UI (login, register, chat screens) and connecting it to the backend API.
