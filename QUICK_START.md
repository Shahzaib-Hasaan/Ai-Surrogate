# 🚀 Quick Start - AI Surrogate Development

**Last Updated**: December 24, 2024

---

## ✅ What We've Completed (Day 1)

### Project Initialization
- ✅ **Mobile App**: Expo project created (`ai-surrogate-mobile`)
- ✅ **Backend**: FastAPI structure created (`ai-surrogate-backend`)
- ✅ **Documentation**: Complete roadmap and sprint plans
- ✅ **Configuration**: Environment templates, gitignore, requirements.txt

### Files Created
```
📁 AI-Surrogate/
├── 📄 README.md                    # Project overview
├── 📱 ai-surrogate-mobile/         # Expo app (ready)
├── 🖥️ ai-surrogate-backend/        # FastAPI backend (structure ready)
└── 📚 docs/
    ├── IMPLEMENTATION_ROADMAP.md   # 15-week plan
    ├── SPRINT_1_WEEK_1_PLAN.md     # This week's tasks
    ├── SCOPE_DOCUMENT.md           # Full specifications
    └── Phase1_Implementation_Plan.md
```

---

## 📋 Next Steps (In Order)

### Step 1: Setup Supabase Database (15 mins)

1. **Go to**: https://supabase.com
2. **Sign up** for free account
3. **Create new project**:
   - Name: `ai-surrogate`
   - Database Password: Save this!
   - Region: Choose closest to you
4. **Get connection string**:
   - Go to Project Settings → Database
   - Copy the "Connection string" (URI format)
   - Example: `postgresql://postgres:[PASSWORD]@db.[PROJECT].supabase.co:5432/postgres`

### Step 2: Setup Backend Environment (5 mins)

1. Navigate to backend:
   ```bash
   cd ai-surrogate-backend
   ```

2. Copy environment template:
   ```bash
   copy .env.example .env
   ```

3. Edit `.env` file:
   - Replace `DATABASE_URL` with your Supabase connection string
   - Generate a secret key:
     ```bash
     # On PowerShell (Windows):
     -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
     
     # Or use online generator: https://randomkeygen.com/
     ```
   - Paste the generated key as `SECRET_KEY`

### Step 3: Install Backend Dependencies (10 mins)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux

# Install all dependencies
pip install -r requirements.txt
```

### Step 4: Create Database Models (30 mins)

**Open Cursor IDE** and use these prompts from `docs/SPRINT_1_WEEK_1_PLAN.md`:

#### Create User Model
File: `app/models/user.py`

**Cursor Prompt**:
```
Create a SQLAlchemy User model in app/models/user.py with:
- id: UUID primary key (use uuid4)
- email: unique string, indexed
- username: unique string, indexed  
- hashed_password: string
- created_at: timestamp with default now()
- updated_at: timestamp with default now()
- is_active: boolean, default True

Include proper imports, Base from database, and __repr__ method.
```

#### Create Message Model
File: `app/models/message.py`

**Cursor Prompt**:
```
Create a SQLAlchemy Message model in app/models/message.py with:
- id: UUID primary key
- user_id: UUID foreign key to User
- content: text
- is_from_user: boolean
- created_at: timestamp
- conversation_id: UUID

Include relationships to User model.
```

#### Create Conversation Model
File: `app/models/conversation.py`

**Cursor Prompt**:
```
Create Conversation model with:
- id: UUID primary key
- user_id: UUID foreign key
- title: optional string
- created_at, updated_at: timestamps

Include relationship to User and Messages.
```

### Step 5: Create Pydantic Schemas (20 mins)

Use Cursor to create validation schemas in `app/schemas/`:
- `user_schema.py` - UserCreate, UserLogin, UserResponse, Token
- `message_schema.py` - MessageCreate, MessageResponse
- `conversation_schema.py` - ConversationCreate, ConversationResponse

**Refer to**: `docs/SPRINT_1_WEEK_1_PLAN.md` for detailed prompts

### Step 6: Implement Authentication (45 mins)

1. **Create** `app/services/auth_service.py`:
   - Password hashing functions
   - JWT token creation/verification
   - User authentication logic

2. **Create** `app/routes/auth.py`:
   - POST `/api/auth/register`
   - POST `/api/auth/login`
   - GET `/api/auth/me`

3. **Create** `app/database.py`:
   - Database connection setup
   - SessionLocal factory
   - get_db dependency

4. **Create** `app/main.py`:
   - FastAPI app initialization
   - CORS configuration
   - Router inclusion

### Step 7: Test Backend (15 mins)

```bash
# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Open in browser:
# http://localhost:8000/docs

# Test endpoints:
# 1. POST /api/auth/register
# 2. POST /api/auth/login
# 3. GET /api/auth/me
```

---

## 🎯 Today's Goal

By end of today, you should have:
- ✅ Supabase database created
- ✅ Backend dependencies installed
- ✅ Database models implemented
- ✅ Authentication service working
- ✅ Backend API running locally
- ✅ Tested with Swagger UI

**Estimated Time**: 2-3 hours

---

## 📚 Resources You'll Need

### During Development
- **Sprint Plan**: `docs/SPRINT_1_WEEK_1_PLAN.md` (copy prompts from here)
- **Scope Doc**: `docs/SCOPE_DOCUMENT.md` (reference for features)
- **Backend README**: `ai-surrogate-backend/README.md` (setup guide)

### External Resources
- **Supabase**: https://supabase.com
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **SQLAlchemy Tutorial**: https://docs.sqlalchemy.org/en/20/tutorial/
- **Cursor IDE**: https://cursor.com (download if not installed)

---

## 🐛 Common Issues & Solutions

### Issue: `pip install` fails
**Solution**: 
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Then retry
pip install -r requirements.txt
```

### Issue: Database connection fails
**Solution**:
- Verify Supabase connection string is correct
- Check password has no special characters in URL (encode if needed)
- Ensure database is "active" in Supabase dashboard

### Issue: Import errors in Python
**Solution**:
```bash
# Make sure virtual environment is activated
# Windows: Should see (venv) in prompt
.\venv\Scripts\activate

# Reinstall if needed
pip install -r requirements.txt
```

---

## ⏭️ Tomorrow's Plan (Day 2)

- [ ] Create chat endpoint (echo responses)
- [ ] Implement conversation management
- [ ] Create basic tests
- [ ] Deploy to Railway.app

---

## 💡 Pro Tips

### Using Cursor Effectively
1. **Copy the exact prompts** from `SPRINT_1_WEEK_1_PLAN.md`
2. **Let AI generate code**, then review it
3. **Ask for explanations**: "Explain this function"
4. **Iterate**: "Add error handling to this"

### Testing Workflow
1. **Write code** (or let Cursor generate it)
2. **Run server**: `uvicorn app.main:app --reload`
3. **Test in Swagger UI**: http://localhost:8000/docs
4. **See errors immediately** in terminal
5. **Fix and auto-reload** happens instantly

### Commit Often
```bash
# After each working feature
git add .
git commit -m "feat: added user authentication"
git push
```

---

## 🎉 Success Checklist

After completing today's tasks, you should be able to:
- [ ] Visit http://localhost:8000/docs and see API documentation
- [ ] Register a new user via Swagger UI
- [ ] Login and receive JWT token
- [ ] Use token to access /api/auth/me endpoint
- [ ] See user data in Supabase dashboard

---

## 📞 Need Help?

1. **Check** `docs/SPRINT_1_WEEK_1_PLAN.md` for detailed prompts
2. **Review** backend `README.md` for setup steps
3. **Read** error messages carefully (they're usually helpful!)
4. **Google** the error if stuck
5. **Ask Cursor** to explain or fix code

---

**Ready?** Start with Step 1: Setup Supabase! 🚀

**Current Status**: Day 1 - Backend Foundation  
**Next Milestone**: Week 1 Complete - Working API deployed
