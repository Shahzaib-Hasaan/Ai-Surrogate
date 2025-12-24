# AI Surrogate Backend API

Backend server for the AI Surrogate Human Clone mobile application.

## Tech Stack
- **Framework**: FastAPI
- **Database**: PostgreSQL (via Supabase)
- **Authentication**: JWT
- **ORM**: SQLAlchemy 2.0
- **AI**: DeepSeek API, CrewAI (Phase 2)

## Setup

### 1. Create Virtual Environment
```bash
python -m venv venv
```

### 2. Activate Virtual Environment
**Windows**:
```bash
.\venv\Scripts\activate
```

**macOS/Linux**:
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
1. Copy `.env.example` to `.env`
2. Update database URL from Supabase
3. Generate a secret key: `openssl rand -hex 32`

### 5. Run Development Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. View API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure
```
ai-surrogate-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── dependencies.py      # FastAPI dependencies
│   ├── models/              # SQLAlchemy models
│   │   ├── user.py
│   │   └── message.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── user_schema.py
│   │   └── message_schema.py
│   ├── routes/              # API endpoints
│   │   ├── auth.py
│   │   └── chat.py
│   └── services/            # Business logic
│       ├── auth_service.py
│       └── chat_service.py
├── tests/                   # Unit tests
├── .env.example            # Environment template
├── requirements.txt        # Python dependencies
└── README.md
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Chat
- `POST /api/chat/message` - Send message
- `GET /api/chat/conversations` - List conversations
- `GET /api/chat/conversations/{id}/messages` - Get messages

## Development

### Database Migrations (Future)
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

### Running Tests
```bash
pytest
```

## Deployment
This backend is designed to be deployed on Railway.app or Render.com.

See deployment guide in `/docs/DEPLOYMENT.md` (coming soon).

## Phase 1 Status ✅
- [x] Project structure created
- [ ] Database models implemented
- [ ] Authentication endpoints completed
- [ ] Basic chat (echo) working
- [ ] Deployed to Railway.app

## Next Steps
See `/docs/SPRINT_1_WEEK_1_PLAN.md` for detailed implementation tasks.
