# AI Surrogate Human Clone - Project Overview

## 📱 What Is This Project?

The **AI Surrogate Human Clone** is a mobile application that serves as an intelligent AI assistant capable of:
- **Natural conversations** with emotional intelligence
- **Voice interactions** (speech-to-text and text-to-speech)
- **Multilingual support** (English, Urdu, Punjabi)
- **Task execution** (scheduling, document creation, web search)
- **Persistent memory** of user preferences and conversation history

Think of it as a personal AI assistant that understands you, remembers you, and helps you with daily tasks.

---

## 🏗️ Project Structure

```
AI-Surrogate/
├── 📱 ai-surrogate-mobile/        # Mobile app (Expo/React Native)
│   ├── App.tsx                    # Main app entry
│   ├── app.json                   # Expo configuration
│   ├── src/                       # Source code (to be created)
│   │   ├── components/            # Reusable UI components
│   │   ├── screens/               # App screens
│   │   ├── services/              # API client
│   │   ├── store/                 # State management
│   │   ├── types/                 # TypeScript types
│   │   └── utils/                 # Helper functions
│   └── package.json
│
├── 🖥️ ai-surrogate-backend/       # Backend API (Python/FastAPI)
│   ├── app/
│   │   ├── main.py                # FastAPI entry point
│   │   ├── models/                # Database models
│   │   ├── schemas/               # API request/response schemas
│   │   ├── routes/                # API endpoints
│   │   └── services/              # Business logic
│   ├── requirements.txt           # Python dependencies
│   └── .env.example               # Environment variables template
│
├── 📚 docs/                       # Documentation
│   ├── SCOPE_DOCUMENT.md          # Complete project specifications
│   ├── Phase1_Implementation_Plan.md  # Detailed Phase 1 plan
│   ├── IMPLEMENTATION_ROADMAP.md  # 15-week sprint breakdown
│   └── SPRINT_1_WEEK_1_PLAN.md    # Current week tasks
│
└── 📖 core/                       # Original specifications (READ-ONLY)
    ├── SRS.md                     # Software Requirements Specification
    └── SDD.md                     # Software Design Document
```

---

## 🛠️ Technology Stack

### **Mobile App (Frontend)**
- **Framework**: Expo SDK 52+ (React Native)
- **Language**: TypeScript
- **UI Library**: React Native Paper
- **Navigation**: React Navigation 6
- **State Management**: Zustand
- **Data Fetching**: TanStack Query (React Query)
- **API Client**: Axios
- **Forms**: React Hook Form + Zod validation

### **Backend API**
- **Framework**: Python FastAPI
- **Database**: PostgreSQL (hosted on Supabase)
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT (JSON Web Tokens)
- **Cache**: Redis (Upstash free tier)

### **AI & Voice Services** (Phase 2+)
- **LLM**: DeepSeek API
- **AI Agents**: CrewAI framework
- **Speech-to-Text**: Google Cloud STT
- **Text-to-Speech**: ElevenLabs or Amazon Polly
- **Translation**: Google Translate API
- **Vector DB**: Chroma (for memory)

### **Infrastructure**
- **Backend Hosting**: Railway.app (free tier)
- **Database**: Supabase (free tier)
- **APK Building**: EAS Build (30 builds/month free)
- **Version Control**: Git + GitHub

---

## 📅 Development Timeline

### **Current Status**: Sprint 1, Week 1 - Foundation Setup ✅

| Sprint | Duration | Goal | Status |
|--------|----------|------|--------|
| **Sprint 1** | Weeks 1-3 | Foundation & Basic Chat | 🚧 In Progress |
| **Sprint 2** | Weeks 4-6 | AI Core Integration | ⏳ Planned |
| **Sprint 3** | Weeks 7-9 | Voice & Multilingual | ⏳ Planned |
| **Sprint 4** | Weeks 10-12 | Task Execution Agents | ⏳ Planned |
| **Sprint 5** | Weeks 13-14 | Polish & Features | ⏳ Planned |
| **Sprint 6** | Week 15 | Testing & Deployment | ⏳ Planned |

**Total Duration**: 15 weeks  
**Target Completion**: March 2025

---

## 🎯 Sprint 1 Goals (Weeks 1-3)

### Week 1: Backend Foundation ✅
- [x] Initialize Expo mobile app
- [x] Create backend structure
- [ ] Setup database models
- [ ] Implement authentication API
- [ ] Create basic chat endpoint (echo)
- [ ] Deploy to Railway.app

### Week 2: Mobile App UI
- [ ] Create login/register screens
- [ ] Setup navigation
- [ ] Create chat UI components
- [ ] Implement API service layer
- [ ] Connect to backend

### Week 3: Integration & Testing
- [ ] End-to-end testing
- [ ] Bug fixes
- [ ] First working demo

---

## 💻 Development Workflow

### Using Expo Go for Testing
1. Install **Expo Go** app on your phone (Android/iOS)
2. Run `npx expo start` in the mobile directory
3. Scan the QR code with your phone
4. App loads instantly with hot reload!

### AI-Assisted Development with Cursor
- Use **Cursor IDE** (https://cursor.com) for coding
- AI generates ~70% of boilerplate code
- Copy prompts from `/docs/SPRINT_1_WEEK_1_PLAN.md`
- Paste into Cursor, get instant code generation
- Saves hours of manual coding

### Daily Development Cycle
1. **Plan** - Review tasks for the day
2. **Code** - Use Cursor AI to generate code
3. **Test** - Test on Expo Go immediately
4. **Iterate** - Fix issues, refine features
5. **Commit** - Save progress to Git

---

## 🚀 Quick Start Guide

### For Mobile App Development

```bash
# Navigate to mobile directory
cd ai-surrogate-mobile

# Start Expo development server
npx expo start

# Open Expo Go on your phone and scan QR code
```

### For Backend Development

```bash
# Navigate to backend directory
cd ai-surrogate-backend

# Create virtual environment (first time only)
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload
```

Backend API will be available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📊 Cost Breakdown

**Total Cost**: $0 - $5 for entire project! 💰

| Service | Free Tier | Cost |
|---------|-----------|------|
| Expo + EAS Builds | 30 builds/month | **$0** |
| Supabase (PostgreSQL) | 500MB database | **$0** |
| Railway.app (Backend) | $5 credit/month | **$0** |
| Upstash (Redis) | 10K commands/day | **$0** |
| DeepSeek API | ~$0.10/million tokens | **~$1-5** |
| Google Cloud STT | 60 mins/month free | **$0** |

---

## 🎓 Learning Resources

### Essential Tutorials
- **Expo**: https://docs.expo.dev/tutorial/introduction/
- **FastAPI**: https://fastapi.tiangolo.com/tutorial/
- **React Navigation**: https://reactnavigation.org/docs/getting-started
- **SQLAlchemy**: https://docs.sqlalchemy.org/en/20/tutorial/

### Key Documentation
- Expo Docs: https://docs.expo.dev
- React Native Paper: https://callstack.github.io/react-native-paper/
- Zustand: https://github.com/pmndrs/zustand
- React Query: https://tanstack.com/query/latest

---

## 🤝 Team Members

- **Shahzaib Hassan** (S22BARIN1M01005)
- **Malik Muhammad Saad** (S22BARIN1M01043)
- **Sagar Salam** (S22BARIN1M01009)

**Supervisor**: Prof. Dr. Najia Saher  
**Institution**: The Islamia University of Bahawalpur  
**Department**: Artificial Intelligence  
**Session**: 2022-2025

---

## 📝 Next Steps

### Immediate Tasks (Today)
1. ✅ Review this overview
2. [ ] Setup Supabase account and create database
3. [ ] Install backend dependencies
4. [ ] Create database models (use Cursor AI)
5. [ ] Test backend locally

### This Week
- Complete backend API with authentication
- Deploy backend to Railway.app
- Prepare for mobile UI development next week

### Resources to Read
- 📖 `/docs/SPRINT_1_WEEK_1_PLAN.md` - Detailed daily tasks
- 📖 `/docs/SCOPE_DOCUMENT.md` - Full project specifications
- 📖 Backend README - Setup instructions

---

## 🎉 Success Criteria

By the end of Sprint 1, you will have:
- ✅ A working mobile app that can run on your phone
- ✅ User registration and login
- ✅ Basic text chat with AI (echo responses)
- ✅ Conversation history
- ✅ Deployed backend API
- ✅ Foundation for all future features

---

## 📧 Support & Questions

For implementation guidance, refer to:
- `/docs/SPRINT_1_WEEK_1_PLAN.md` - Daily task breakdown with Cursor prompts
- `/docs/IMPLEMENTATION_ROADMAP.md` - Overall project roadmap
- Backend `README.md` - Backend setup guide

---

**Last Updated**: December 24, 2024  
**Version**: 1.0  
**Status**: Sprint 1, Week 1 - Day 1 ✅

Let's build something amazing! 🚀
