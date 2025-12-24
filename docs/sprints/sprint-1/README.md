# Sprint 1: Foundation & Basic Chat
**AI Surrogate Human Clone - Development Sprint**

> **Duration**: Weeks 1-3 (December 24, 2024 - January 13, 2025)  
> **Goal**: Create working mobile app with authentication and basic chat  
> **Status**: 🚧 In Progress - Week 1, Day 1

---

## 📋 Sprint Overview

### Objective
Establish the foundational architecture for the AI Surrogate Human Clone project, including mobile app scaffolding, backend server, database, authentication, and basic text chat functionality.

### Key Deliverables
- ✅ Working mobile app that runs on Expo Go
- ✅ User registration and login system
- ✅ Backend API with JWT authentication
- ✅ PostgreSQL database with core models
- ✅ Basic text chat (echo responses initially)
- ✅ API documentation (auto-generated at /docs)
- ✅ Backend deployed to Railway.app

---

## 📅 Sprint Timeline

### Week 1: Backend Foundation (Dec 24-30)
**Focus**: Setup development environment and create backend API

#### Completed ✅
- [x] Expo mobile app initialized
- [x] Backend structure created
- [x] Documentation organized
- [x] Requirements defined

#### In Progress 🚧
- [ ] Database models (User, Message, Conversation)
- [ ] Authentication service (JWT)
- [ ] API endpoints (register, login, chat)
- [ ] Supabase database setup

#### Deliverables
- Backend API running locally
- Database schema created
- Authentication working
- Echo chat endpoint functional

**📖 Detailed Plan**: [Week 1 Plan](./week-1/WEEK_1_PLAN.md)

---

### Week 2: Mobile App UI (Dec 31 - Jan 6)
**Focus**: Create mobile app screens and connect to backend

#### Tasks
- [ ] Setup React Navigation
- [ ] Create login/register screens
- [ ] Implement state management (Zustand)
- [ ] Create API service layer
- [ ] Build chat UI components
- [ ] Connect frontend to backend

#### Deliverables
- Login/register flows working
- Chat screen with UI
- Token persistence
- End-to-end authentication

**📖 Detailed Plan**: [Week 2 Plan](./week-2/WEEK_2_PLAN.md) *(Coming Soon)*

---

### Week 3: Integration & Testing (Jan 7-13)
**Focus**: Connect all pieces and deploy

#### Tasks
- [ ] End-to-end testing
- [ ] Bug fixes and refinements
- [ ] Deploy backend to Railway.app
- [ ] Test on real devices
- [ ] Performance optimization
- [ ] Documentation updates

#### Deliverables
- Fully working app on Expo Go
- Backend deployed and accessible
- All features tested
- Ready for Sprint 2

**📖 Detailed Plan**: [Week 3 Plan](./week-3/WEEK_3_PLAN.md) *(Coming Soon)*

---

## 🎯 Sprint Goals & Success Metrics

### Technical Goals
- [ ] App startup time < 2 seconds
- [ ] API response time < 1 second
- [ ] Zero crashes during testing
- [ ] 100% of MVP features working

### User Experience Goals
- [ ] Smooth login/register flow
- [ ] Instant message sending
- [ ] Clear error messages
- [ ] Intuitive navigation

### Development Goals
- [ ] Clean, documented code
- [ ] Reusable components
- [ ] Proper error handling
- [ ] Git commits for each feature

---

## 🛠️ Technology Stack

### Mobile App
- **Framework**: Expo SDK 54
- **Language**: TypeScript
- **UI**: React Native Paper
- **Navigation**: React Navigation 6
- **State**: Zustand
- **API Client**: Axios

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL (Supabase)
- **ORM**: SQLAlchemy 2.0
- **Auth**: JWT tokens
- **Hosting**: Railway.app

---

## 📁 Sprint Documentation Structure

```
docs/sprints/sprint-1/
├── README.md                    # This file - Sprint overview
├── week-1/
│   ├── WEEK_1_PLAN.md          # Detailed daily tasks
│   ├── PROGRESS.md             # Daily progress tracking
│   └── RETROSPECTIVE.md        # Week 1 learnings
├── week-2/
│   ├── WEEK_2_PLAN.md          # Week 2 tasks
│   ├── PROGRESS.md             # Daily progress
│   └── RETROSPECTIVE.md        # Week 2 learnings
└── week-3/
    ├── WEEK_3_PLAN.md          # Week 3 tasks
    ├── PROGRESS.md             # Daily progress
    └── RETROSPECTIVE.md        # Week 3 learnings
```

---

## 📊 Progress Tracking

### Overall Sprint Progress: 5%

| Week | Status | Progress | Completion Date |
|------|--------|----------|-----------------|
| Week 1 | 🚧 In Progress | 10% | Dec 30, 2024 |
| Week 2 | ⏳ Planned | 0% | Jan 6, 2025 |
| Week 3 | ⏳ Planned | 0% | Jan 13, 2025 |

### Feature Completion

| Feature | Status | Progress |
|---------|--------|----------|
| Project Setup | ✅ Complete | 100% |
| Backend Structure | ✅ Complete | 100% |
| Database Models | 🚧 In Progress | 0% |
| Authentication API | ⏳ Planned | 0% |
| Chat API | ⏳ Planned | 0% |
| Mobile UI | ⏳ Planned | 0% |
| Integration | ⏳ Planned | 0% |
| Deployment | ⏳ Planned | 0% |

---

## 🚀 Quick Start

### For Backend Development
```bash
cd ai-surrogate-backend

# Setup virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload
```

### For Mobile Development
```bash
cd ai-surrogate-mobile

# Start Expo
npx expo start

# Or with tunnel (recommended)
npx expo start --tunnel
```

---

## 📝 Daily Standups

### Week 1 - Day 1 (Dec 24, 2024)

#### Completed Today ✅
- Initialized Expo mobile app
- Created backend structure
- Organized documentation
- Fixed Expo Go compatibility issues

#### Working On Today 🚧
- Setting up Supabase database
- Creating database models
- Installing backend dependencies

#### Blockers 🚫
- Expo Go loading issues (troubleshooting in progress)

#### Next Steps ⏭️
- Complete database models
- Implement authentication service
- Test backend locally

---

## 🎓 Learning & Resources

### Key Documentation
- [Week 1 Detailed Plan](./week-1/WEEK_1_PLAN.md)
- [Project Scope Document](../../SCOPE_DOCUMENT.md)
- [Implementation Roadmap](../../IMPLEMENTATION_ROADMAP.md)
- [Quick Start Guide](../../../QUICK_START.md)

### External Resources
- **FastAPI Tutorial**: https://fastapi.tiangolo.com/tutorial/
- **Expo Documentation**: https://docs.expo.dev
- **SQLAlchemy Guide**: https://docs.sqlalchemy.org/en/20/tutorial/
- **Supabase Docs**: https://supabase.com/docs

### Tools & Services
- **Cursor IDE**: AI-assisted coding
- **Supabase**: PostgreSQL database (free tier)
- **Railway.app**: Backend hosting (free tier)
- **Expo Go**: Mobile app testing

---

## 🐛 Known Issues & Solutions

### Issue 1: Expo Go "Something went wrong" error
**Status**: 🔧 Troubleshooting  
**Solution**: Removed `newArchEnabled` and edge-to-edge features  
**Documentation**: [Troubleshooting Guide](../../../ai-surrogate-mobile/TROUBLESHOOTING.md)

### Issue 2: Network connectivity for Expo Go
**Status**: 📖 Documented  
**Solution**: Use tunnel mode with Expo account  
**Command**: `npx expo start --tunnel`

---

## 🎯 Sprint Retrospective (End of Sprint)

*To be completed on January 13, 2025*

### What Went Well ✅
- TBD

### What Could Be Improved 🔄
- TBD

### Action Items for Sprint 2 📋
- TBD

### Key Learnings 📚
- TBD

---

## 📞 Team & Support

### Team Members
- **Shahzaib Hassan** (S22BARIN1M01005)
- **Malik Muhammad Saad** (S22BARIN1M01043)
- **Sagar Salam** (S22BARIN1M01009)

### Supervisor
**Prof. Dr. Najia Saher**

### Communication
- **Daily Standups**: Review progress, plan tasks, identify blockers
- **Weekly Reviews**: Demo working features, retrospective
- **Documentation**: Update progress daily in respective PROGRESS.md files

---

## 🔗 Related Documents

- [Main Project README](../../../README.md)
- [Complete Scope Document](../../SCOPE_DOCUMENT.md)
- [15-Week Implementation Roadmap](../../IMPLEMENTATION_ROADMAP.md)
- [Phase 1 Implementation Plan](../../Phase1_Implementation_Plan.md)
- [Quick Start Guide](../../../QUICK_START.md)

---

**Last Updated**: December 24, 2024  
**Sprint Status**: Week 1, Day 1 - In Progress  
**Next Review**: December 30, 2024 (End of Week 1)
