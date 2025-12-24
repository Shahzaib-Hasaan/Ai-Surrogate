# Phase 1 Implementation Plan - AI Surrogate Human Clone
**Foundation & Core Architecture Setup**

> **Duration**: Weeks 1-3 (21 days)  
> **AI-Generated Code Target**: ~60%  
> **Status**: Ready for AI Development  
> **Last Updated**: December 24, 2025

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Development Environment Setup](#development-environment-setup)
4. [Project Structure](#project-structure)
5. [Implementation Tasks](#implementation-tasks)
6. [Testing Requirements](#testing-requirements)
7. [Success Metrics](#success-metrics)
8. [Next Phase Preview](#next-phase-preview)

---

## 🎯 Overview

### Objective
Establish the foundational architecture for the AI Surrogate Human Clone project, including:
- Mobile app scaffolding (Expo/React Native)
- Backend server setup (Python/FastAPI)
- Database initialization (PostgreSQL)
- Basic authentication system
- Simple chat UI with text messaging
- API integration framework

### Key Deliverables
✅ Working mobile app with login/registration  
✅ FastAPI backend with JWT authentication  
✅ PostgreSQL database with core models  
✅ Basic text chat functionality  
✅ API documentation (auto-generated)  
✅ Development environment ready for Phase 2

---

## 📦 Prerequisites

### Required Accounts (All FREE)
- [ ] Expo account (https://expo.dev)
- [ ] Supabase account (https://supabase.com) - PostgreSQL hosting
- [ ] Railway.app OR Render.com account - Backend hosting
- [ ] GitHub account - Version control

### Required Software
```bash
# Node.js 18+ (for Expo)
# Python 3.11+ (for FastAPI)
# Git
# Code editor: Cursor IDE (recommended) or VS Code
```

### API Keys to Obtain
- [ ] DeepSeek API key (basic free tier) - https://platform.deepseek.com
- [ ] Supabase project credentials

---

## 🛠️ Development Environment Setup

### Step 1: Install Development Tools

#### Windows Setup (via PowerShell)
```powershell
# Install Node.js (if not installed)
# Download from https://nodejs.org

# Verify installation
node --version
npm --version

# Install Expo CLI
npm install -g expo-cli eas-cli

# Install Python (if not installed)
# Download from https://python.org

# Verify Python
python --version
pip --version
```

#### Python Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Install core dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic python-jose[cryptography] passlib[bcrypt] python-multipart
```

### Step 2: Project Initialization

#### Frontend (Mobile App)
```bash
# Create Expo project
npx create-expo-app ai-surrogate-mobile --template blank-typescript

# Navigate to project
cd ai-surrogate-mobile

# Install core dependencies
npx expo install @react-navigation/native @react-navigation/stack
npx expo install react-native-paper react-native-safe-area-context
npx expo install axios @tanstack/react-query zustand
npx expo install expo-secure-store @react-native-async-storage/async-storage
npx expo install react-hook-form zod
```

#### Backend (API Server)
```bash
# Create backend directory
mkdir ai-surrogate-backend
cd ai-surrogate-backend

# Initialize Python project
pip install fastapi uvicorn sqlalchemy alembic python-dotenv
```

### Step 3: Cursor IDE Configuration

Create `.cursorrules` in project root:
```
# .cursorrules

You are an expert full-stack AI developer building the AI Surrogate Human Clone project.

**Tech Stack:**
- Frontend: Expo/React Native with TypeScript
- Backend: Python FastAPI with SQLAlchemy
- Database: PostgreSQL (Supabase)

**Code Generation Rules:**
1. Always use TypeScript for frontend code with proper types
2. Add docstrings to all Python functions
3. Include error handling by default
4. Follow functional programming patterns (React hooks)
5. Use async/await for all async operations
6. Add input validation with Pydantic (backend) and Zod (frontend)
7. Include comments for complex logic
8. Follow RESTful API conventions
9. Use proper HTTP status codes
10. Generate both success and error test cases

**File Structure:**
- Frontend: /ai-surrogate-mobile
- Backend: /ai-surrogate-backend
- Docs: /docs
- Core specs: /core

When generating code, always consider:
- Mobile responsiveness
- Offline handling
- Loading states
- Error states
- Accessibility
```

---

## 📁 Project Structure

### Final Phase 1 Structure
```
AI-Surrogate/
├── core/                           # Core specifications (READ-ONLY)
│   ├── SCOPE_DOCUMENT.md
│   ├── SDD.md
│   └── SRS.md
├── docs/                           # Documentation
│   └── Phase1_Implementation_Plan.md
├── ai-surrogate-mobile/           # React Native Mobile App
│   ├── app/                       # Expo Router screens
│   │   ├── (auth)/
│   │   │   ├── login.tsx
│   │   │   └── register.tsx
│   │   ├── (tabs)/
│   │   │   ├── _layout.tsx
│   │   │   ├── index.tsx         # Chat screen
│   │   │   └── profile.tsx
│   │   └── _layout.tsx
│   ├── components/
│   │   ├── ChatBubble.tsx
│   │   ├── MessageInput.tsx
│   │   └── LoadingSpinner.tsx
│   ├── services/
│   │   ├── api.ts                # Axios config
│   │   ├── authService.ts
│   │   └── chatService.ts
│   ├── store/
│   │   ├── authStore.ts          # Zustand auth state
│   │   └── chatStore.ts          # Zustand chat state
│   ├── types/
│   │   └── index.ts              # TypeScript types
│   ├── utils/
│   │   └── secureStorage.ts
│   ├── app.json
│   ├── package.json
│   └── tsconfig.json
└── ai-surrogate-backend/          # Python FastAPI Backend
    ├── app/
    │   ├── __init__.py
    │   ├── main.py               # FastAPI app entry
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
    │   ├── services/
    │   │   ├── __init__.py
    │   │   ├── auth_service.py
    │   │   └── chat_service.py
    │   ├── database.py           # SQLAlchemy setup
    │   ├── config.py             # Environment config
    │   └── dependencies.py       # FastAPI dependencies
    ├── alembic/                  # Database migrations
    ├── tests/
    │   ├── test_auth.py
    │   └── test_chat.py
    ├── .env.example
    ├── requirements.txt
    └── README.md
```

---

## 🚀 Implementation Tasks

### Week 1: Backend Foundation

#### Task 1.1: Database Models (AI-Generated: 80%)
**Prompt for Cursor:**
```
Create SQLAlchemy models for the AI Surrogate backend with the following requirements:

1. User model (app/models/user.py):
   - id: UUID primary key
   - email: unique, indexed
   - username: unique, indexed
   - hashed_password: string
   - created_at: timestamp
   - updated_at: timestamp
   - is_active: boolean (default True)

2. Message model (app/models/message.py):
   - id: UUID primary key
   - user_id: foreign key to User
   - content: text
   - is_from_user: boolean
   - created_at: timestamp
   - conversation_id: UUID (for grouping)

3. Conversation model (app/models/conversation.py):
   - id: UUID primary key
   - user_id: foreign key to User
   - title: string (optional)
   - created_at: timestamp
   - updated_at: timestamp

Include:
- Proper relationships (User has many Conversations, Conversation has many Messages)
- Indexes for common queries
- __repr__ methods
- Docstrings
```

**Deliverable:** `app/models/user.py`, `app/models/message.py`, `app/models/conversation.py`

---

#### Task 1.2: Pydantic Schemas (AI-Generated: 85%)
**Prompt for Cursor:**
```
Create Pydantic schemas for request/response validation in app/schemas/:

1. user_schema.py:
   - UserCreate (email, username, password)
   - UserLogin (email, password)
   - UserResponse (id, email, username, created_at)
   - Token (access_token, token_type)

2. message_schema.py:
   - MessageCreate (content, conversation_id optional)
   - MessageResponse (id, content, is_from_user, created_at)

3. conversation_schema.py:
   - ConversationCreate (title optional)
   - ConversationResponse (id, title, created_at, messages list)

Include:
- Field validation (email format, password min length 8)
- Example values for API docs
- Proper Config class with orm_mode=True
```

**Deliverable:** `app/schemas/user_schema.py`, `app/schemas/message_schema.py`, `app/schemas/conversation_schema.py`

---

#### Task 1.3: Authentication Service (AI-Generated: 75%)
**Prompt for Cursor:**
```
Create authentication service in app/services/auth_service.py:

Functions needed:
1. hash_password(password: str) -> str
   - Use bcrypt

2. verify_password(plain_password: str, hashed_password: str) -> bool
   - Compare passwords

3. create_access_token(data: dict, expires_delta: timedelta = None) -> str
   - Create JWT token with 30-day expiration
   - Use python-jose

4. verify_token(token: str) -> dict
   - Decode and validate JWT
   - Raise HTTPException if invalid

5. get_current_user(token: str, db: Session) -> User
   - Extract user from token
   - Return User model instance

Include:
- Proper error handling
- Type hints
- Docstrings
- Use SECRET_KEY from environment
```

**Deliverable:** `app/services/auth_service.py`

---

#### Task 1.4: Authentication Routes (AI-Generated: 70%)
**Prompt for Cursor:**
```
Create authentication endpoints in app/routes/auth.py:

Endpoints:
1. POST /api/auth/register
   - Input: UserCreate schema
   - Process: Hash password, create user in DB
   - Return: UserResponse + access token
   - Status: 201 Created

2. POST /api/auth/login
   - Input: UserLogin schema
   - Process: Verify credentials, generate token
   - Return: Token schema
   - Status: 200 OK

3. GET /api/auth/me
   - Headers: Authorization: Bearer <token>
   - Process: Get current user from token
   - Return: UserResponse
   - Status: 200 OK

Include:
- Dependency injection for database session
- Error handling (duplicate email, wrong credentials)
- Proper HTTP status codes
- OpenAPI documentation tags
```

**Deliverable:** `app/routes/auth.py`

---

#### Task 1.5: Basic Chat Endpoint (AI-Generated: 65%)
**Prompt for Cursor:**
```
Create basic chat endpoint in app/routes/chat.py:

Endpoints:
1. POST /api/chat/message
   - Input: MessageCreate schema
   - Auth: Requires JWT token
   - Process:
     a. Save user message to DB
     b. Generate simple echo response: "You said: {content}"
     c. Save AI response to DB
   - Return: MessageResponse (AI response)
   - Status: 201 Created

2. GET /api/chat/conversations
   - Auth: Requires JWT token
   - Return: List of user's conversations
   - Status: 200 OK

3. GET /api/chat/conversations/{conversation_id}/messages
   - Auth: Requires JWT token
   - Return: List of messages in conversation
   - Status: 200 OK

Note: Phase 1 uses echo responses. Phase 2 will integrate DeepSeek API.

Include:
- Authentication dependency
- Pagination for message list
- Proper error handling
```

**Deliverable:** `app/routes/chat.py`

---

#### Task 1.6: FastAPI Main Application (AI-Generated: 80%)
**Prompt for Cursor:**
```
Create main FastAPI application in app/main.py:

Requirements:
1. Initialize FastAPI app with:
   - Title: "AI Surrogate API"
   - Version: "1.0.0"
   - Description from SCOPE_DOCUMENT.md

2. Configure CORS:
   - Allow origins: ["*"] for development
   - Allow credentials: True
   - Allow methods: ["*"]
   - Allow headers: ["*"]

3. Include routers:
   - /api/auth (from routes.auth)
   - /api/chat (from routes.chat)

4. Add middleware:
   - Request logging
   - Response time tracking

5. Health check endpoint:
   - GET /health
   - Return: {"status": "healthy", "timestamp": <now>}

6. Database initialization on startup

Include:
- Lifespan context manager
- Exception handlers
- Auto-generated docs at /docs
```

**Deliverable:** `app/main.py`

---

### Week 2: Mobile App Frontend

#### Task 2.1: API Service Layer (AI-Generated: 85%)
**Prompt for Cursor:**
```
Create API service layer for the mobile app:

1. services/api.ts:
   - Axios instance with base URL from environment
   - Request interceptor to add JWT token from SecureStore
   - Response interceptor for error handling
   - Retry logic for network failures

2. services/authService.ts:
   Functions:
   - register(email, username, password): Promise<Token>
   - login(email, password): Promise<Token>
   - getProfile(): Promise<User>
   - logout(): void (clear token)

3. services/chatService.ts:
   Functions:
   - sendMessage(content, conversationId?): Promise<Message>
   - getConversations(): Promise<Conversation[]>
   - getMessages(conversationId): Promise<Message[]>

Include:
- TypeScript types imported from types/index.ts
- Error handling with user-friendly messages
- Offline detection
```

**Deliverable:** `services/api.ts`, `services/authService.ts`, `services/chatService.ts`

---

#### Task 2.2: TypeScript Types (AI-Generated: 90%)
**Prompt for Cursor:**
```
Create TypeScript type definitions in types/index.ts:

Types needed:
1. User:
   - id: string
   - email: string
   - username: string
   - createdAt: string

2. Message:
   - id: string
   - content: string
   - isFromUser: boolean
   - createdAt: string

3. Conversation:
   - id: string
   - title?: string
   - createdAt: string
   - messages?: Message[]

4. Token:
   - accessToken: string
   - tokenType: string

5. ApiError:
   - message: string
   - statusCode: number

Export all types.
```

**Deliverable:** `types/index.ts`

---

#### Task 2.3: Zustand State Stores (AI-Generated: 75%)
**Prompt for Cursor:**
```
Create Zustand state management stores:

1. store/authStore.ts:
   State:
   - user: User | null
   - token: string | null
   - isLoading: boolean
   - error: string | null

   Actions:
   - setUser(user: User): void
   - setToken(token: string): void
   - logout(): void
   - setLoading(isLoading: boolean): void
   - setError(error: string | null): void

2. store/chatStore.ts:
   State:
   - conversations: Conversation[]
   - currentConversation: Conversation | null
   - messages: Message[]
   - isLoading: boolean
   - error: string | null

   Actions:
   - addMessage(message: Message): void
   - setConversations(conversations: Conversation[]): void
   - setCurrentConversation(conversation: Conversation): void
   - clearMessages(): void

Include:
- Persist auth token to SecureStore
- TypeScript types
```

**Deliverable:** `store/authStore.ts`, `store/chatStore.ts`

---

#### Task 2.4: Login Screen (AI-Generated: 70%)
**Prompt for Cursor:**
```
Create login screen in app/(auth)/login.tsx:

Requirements:
1. UI Components:
   - Email input (with validation)
   - Password input (secure text entry)
   - "Login" button
   - "Don't have an account? Register" link
   - Loading indicator during submission
   - Error message display

2. Form Handling:
   - Use react-hook-form with Zod validation
   - Email format validation
   - Password min length 8 characters

3. Functionality:
   - Call authService.login()
   - Save token to SecureStore
   - Update Zustand authStore
   - Navigate to chat screen on success
   - Show error message on failure

4. Styling:
   - Use React Native Paper components
   - Center-aligned layout
   - App logo at top
   - Responsive design

Include:
- TypeScript types
- Keyboard avoiding view
- Auto-focus on email input
```

**Deliverable:** `app/(auth)/login.tsx`

---

#### Task 2.5: Registration Screen (AI-Generated: 70%)
**Prompt for Cursor:**
```
Create registration screen in app/(auth)/register.tsx:

Similar to login screen, but with:
- Username input field
- Password confirmation field
- Validation: passwords must match
- Call authService.register()
- Auto-login after successful registration

Copy styling and structure from login.tsx.
```

**Deliverable:** `app/(auth)/register.tsx`

---

#### Task 2.6: Chat Screen UI (AI-Generated: 60%)
**Prompt for Cursor:**
```
Create main chat screen in app/(tabs)/index.tsx:

Requirements:
1. Layout:
   - Header with app title and profile icon
   - Message list (FlatList) in center
   - Message input at bottom

2. Components:
   - Use components/ChatBubble.tsx for each message
   - Use components/MessageInput.tsx for input field

3. Functionality:
   - Load messages on mount (from chatService)
   - Display messages in chronological order
   - User messages: aligned right (blue)
   - AI messages: aligned left (gray)
   - Scroll to bottom on new message
   - Show "Typing..." indicator when sending

4. State Management:
   - Use React Query for data fetching
   - Use Zustand chatStore for local state

Include:
- Pull-to-refresh
- Empty state ("Start a conversation")
- Loading state
- Error state with retry button
```

**Deliverable:** `app/(tabs)/index.tsx`

---

#### Task 2.7: Chat Components (AI-Generated: 75%)
**Prompt for Cursor:**
```
Create reusable chat components:

1. components/ChatBubble.tsx:
   Props:
   - message: Message
   - isFromUser: boolean
   
   Rendering:
   - Show message content
   - Show timestamp (formatted)
   - Different styling for user vs AI
   - Rounded corners
   - Proper spacing

2. components/MessageInput.tsx:
   Props:
   - onSend: (content: string) => void
   - isLoading: boolean

   Rendering:
   - TextInput with multiline support
   - Send button (icon)
   - Disable input when loading
   - Clear input after send
   - Max height with scroll

Include:
- TypeScript props interfaces
- React Native Paper styling
- Accessibility labels
```

**Deliverable:** `components/ChatBubble.tsx`, `components/MessageInput.tsx`

---

### Week 3: Integration & Testing

#### Task 3.1: Environment Configuration (Manual: 60%)
**Action Items:**
1. Create `.env` file in backend:
```env
DATABASE_URL=postgresql://user:pass@host:5432/dbname
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=43200
```

2. Create `.env` in mobile app:
```env
EXPO_PUBLIC_API_URL=http://localhost:8000
```

3. Add `.env.example` templates to both projects

**Deliverable:** Environment files configured

---

#### Task 3.2: Database Setup (AI-Generated: 70%)
**Prompt for Cursor:**
```
Create database setup utilities:

1. app/database.py:
   - SQLAlchemy engine configuration
   - SessionLocal factory
   - Base class for models
   - get_db() dependency function

2. Create Alembic migration scripts:
   - Initialize Alembic
   - Generate initial migration for all models
   - Apply migration

3. Create seed data script (optional):
   - Add test user
   - Add sample conversation

Include proper connection pooling and error handling.
```

**Deliverable:** `app/database.py`, Alembic migrations

---

#### Task 3.3: Integration Testing (AI-Generated: 50%, Manual: 50%)
**Prompt for Cursor:**
```
Create test files in backend/tests/:

1. tests/test_auth.py:
   - Test user registration (success)
   - Test user registration (duplicate email)
   - Test login (success)
   - Test login (wrong password)
   - Test /me endpoint with valid token
   - Test /me endpoint with invalid token

2. tests/test_chat.py:
   - Test send message
   - Test get conversations
   - Test get messages
   - Test unauthorized access

Use pytest and TestClient from FastAPI.
```

**Manual Testing Checklist:**
- [ ] Run backend with `uvicorn app.main:app --reload`
- [ ] Test all endpoints in Postman/Thunder Client
- [ ] Run mobile app with `npx expo start`
- [ ] Test registration flow
- [ ] Test login flow
- [ ] Test sending messages
- [ ] Test message history
- [ ] Test offline behavior
- [ ] Test error handling

**Deliverable:** Test files + manual test results

---

#### Task 3.4: Documentation (AI-Generated: 80%)
**Prompt for Cursor:**
```
Create comprehensive README.md for both projects:

1. ai-surrogate-backend/README.md:
   - Project description
   - Setup instructions
   - Environment variables
   - Running the server
   - API documentation link
   - Testing instructions

2. ai-surrogate-mobile/README.md:
   - Project description
   - Setup instructions
   - Running on emulator/device
   - Environment configuration
   - Building APK (preview)

Include:
- Code formatting standards
- Git workflow
- Troubleshooting section
```

**Deliverable:** README files for both projects

---

#### Task 3.5: Deployment Preparation (AI-Generated: 65%)
**Prompt for Cursor:**
```
Create deployment configuration:

1. Backend (Railway.app):
   - Create railway.json with build/start commands
   - Configure environment variables
   - Set up PostgreSQL service

2. Mobile App:
   - Create eas.json for Expo build
   - Configure app.json with proper bundle ID
   - Set up preview build profile

Generate deployment checklists for both platforms.
```

**Manual Steps:**
- [ ] Create Railway.app account
- [ ] Deploy backend to Railway
- [ ] Update mobile app API_URL to Railway endpoint
- [ ] Test deployed backend
- [ ] Build preview APK with `eas build --platform android --profile preview`

**Deliverable:** Deployed backend + APK file

---

## ✅ Testing Requirements

### Backend Testing
```bash
# Run all tests
pytest tests/ -v

# Check test coverage
pytest --cov=app tests/
```

### Frontend Testing
```typescript
// Manual testing checklist
- [ ] Authentication flow works
- [ ] Chat messages send/receive correctly
- [ ] UI is responsive on different screen sizes
- [ ] Error messages display properly
- [ ] Loading states show correctly
- [ ] Offline handling works
```

---

## 📊 Success Metrics

### Phase 1 Completion Criteria
- [x] User can register an account
- [x] User can login and receive JWT token
- [x] User can send text messages
- [x] User can receive echo responses (simulated AI)
- [x] User can view conversation history
- [x] Backend is deployed and accessible
- [x] Mobile app runs on physical device (via Expo Go)
- [x] API documentation is auto-generated and accessible
- [x] Code is version controlled on GitHub
- [x] Basic error handling implemented

### Performance Targets
- API response time: < 500ms (for echo responses)
- App launch time: < 3 seconds
- Message send-to-display: < 1 second

---

## 🔮 Next Phase Preview

### Phase 2: AI Core (Weeks 4-6)
What changes in Phase 2:
1. **Replace echo responses** with DeepSeek API integration
2. **Add CrewAI** multi-agent framework
3. **Implement memory system** using Chroma vector database
4. **Add conversation context** to maintain continuity
5. **Integrate emotional intelligence** with sentiment analysis

Files that will be modified:
- `app/services/chat_service.py` - Add LLM integration
- `app/routes/chat.py` - Update to use AI responses
- Add new files for agent orchestration

Phase 1 provides the foundation; Phase 2 brings true AI capabilities.

---

## 🤖 AI-Assisted Development Tips

### Using Cursor Effectively

1. **Generate entire files:**
```
Prompt: "Create a complete FastAPI authentication route with register, login, and get current user endpoints. Include proper error handling and docstrings."
```

2. **Fix errors:**
```
Prompt: "This endpoint is returning 422 validation error. Fix the Pydantic schema and endpoint to accept the correct format."
```

3. **Add features:**
```
Prompt: "Add password reset functionality to the auth service with email verification."
```

4. **Generate tests:**
```
Prompt: "Generate pytest test cases for the auth.py routes, covering success and error scenarios."
```

### Cursor Shortcuts
- `Ctrl+K`: Generate code inline
- `Ctrl+L`: Chat with AI about selected code
- `Ctrl+I`: Edit code with AI instructions

---

## 📞 Support & Resources

### Documentation Links
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Expo Docs](https://docs.expo.dev/)
- [React Native Paper](https://callstack.github.io/react-native-paper/)
- [Zustand Guide](https://github.com/pmndrs/zustand)

### Project Team
- **Shahzaib Hassan** - S22BARIN1M01005
- **Malik Muhammad Saad** - S22BARIN1M01043
- **Sagar Salam** - S22BARIN1M01009

**Supervisor**: Prof. Dr. Najia Saher

---

## 📝 Notes for AI Developer

When implementing this plan:

1. **Start with backend** - Get the API working first
2. **Use Cursor prompts exactly as written** - They're designed for optimal AI code generation
3. **Test each component** before moving to the next
4. **Commit frequently** - After each completed task
5. **Don't skip error handling** - It's included in all prompts
6. **Follow the folder structure** exactly as specified
7. **Phase 1 is just the foundation** - Keep code modular for Phase 2 enhancements

### Common Issues & Solutions

**Issue**: CORS errors in mobile app  
**Solution**: Check CORS middleware in `main.py`, ensure origins include your development server

**Issue**: JWT token not persisting  
**Solution**: Verify SecureStore is properly implemented in `authStore.ts`

**Issue**: Database connection fails  
**Solution**: Check DATABASE_URL format in `.env`, ensure Supabase project is active

**Issue**: Expo app won't start  
**Solution**: Run `npx expo install --fix` to resolve dependency conflicts

---

> **Document Version**: 1.0  
> **AI Development Ready**: ✅ Yes  
> **Estimated Implementation Time**: 3 weeks (with 60% AI assistance)  
> **Next Review Date**: End of Week 3

**Good luck with Phase 1! 🚀**
