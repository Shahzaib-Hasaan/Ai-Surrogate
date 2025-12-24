# Package Installation Tracker

**Last Updated**: December 24, 2024  
**Purpose**: Track all packages that need to be installed for the AI Surrogate project

---

## 🐍 Backend (Python) - `ai-surrogate-backend/`

### Installation Command
```bash
cd f:\Projects\AI-Surrogate\ai-surrogate-backend
pip install -r requirements.txt
```

### Current Packages (`requirements.txt`)

#### Core Framework
- `fastapi==0.109.0` - Web framework
- `uvicorn[standard]==0.27.0` - ASGI server
- `python-multipart==0.0.6` - Form data parsing

#### Database
- `sqlalchemy==2.0.25` - ORM
- `psycopg2-binary==2.9.9` - PostgreSQL driver
- `alembic==1.13.1` - Database migrations

#### Validation & Settings
- `pydantic==2.5.3` - Data validation
- `pydantic-settings==2.1.0` - Settings management

#### Authentication
- `python-jose[cryptography]==3.3.0` - JWT tokens
- `passlib[bcrypt]==1.7.4` - Password hashing

#### Utilities
- `python-dotenv==1.0.0` - Environment variables
- `redis==5.0.1` - Caching (future use)
- `httpx==0.26.0` - HTTP client

#### AI Integration (Sprint 2)
- `mistralai>=1.0.0` - **NEW** Mistral AI SDK

### Installation Status
- ✅ All packages installed
- ✅ `mistralai` installed in Sprint 2

---

## 📱 Frontend (React Native/Expo) - `ai-surrogate-mobile/`

### Installation Command
```bash
cd f:\Projects\AI-Surrogate\ai-surrogate-mobile
npm install
```

### Current Packages (`package.json`)

#### Core Framework
- `expo` - Expo framework
- `react` - React library
- `react-native` - React Native

#### Navigation
- `@react-navigation/native` - Navigation library
- `@react-navigation/native-stack` - Stack navigator
- `react-native-screens` - Native screens
- `react-native-safe-area-context` - Safe area handling

#### State Management
- `zustand` - State management

#### HTTP & Storage
- `axios` - HTTP client
- `@react-native-async-storage/async-storage` - Local storage
- `expo-secure-store` - Secure storage (not used in web)

#### UI Components
- `react-native-paper` - Material Design components
- `react-dom` - React DOM (for web)
- `react-native-web` - Web support

### Installation Status
- ✅ All packages installed
- ✅ No new packages in Sprint 2 (yet)

---

## 🔮 Planned Packages (Future Sprints)

### Backend (Sprint 3+)
- [ ] `google-cloud-speech` - Google Cloud STT
- [ ] `elevenlabs` - Text-to-speech
- [ ] `googletrans` - Translation API
- [ ] `chromadb` - Vector database
- [ ] `langchain` - LLM framework (optional)

### Frontend (Sprint 2-3)
- [ ] `react-native-markdown-display` - Markdown rendering
- [ ] `react-native-typing-animation` - Typing indicator
- [ ] `expo-av` - Audio/video playback
- [ ] `expo-speech` - Text-to-speech
- [ ] `@react-native-voice/voice` - Speech recognition

---

## 📋 Installation Checklist

### Initial Setup (Done)
- [x] Backend: `pip install -r requirements.txt`
- [x] Frontend: `npm install`

### Sprint 2 Updates
- [x] Backend: `pip install mistralai`
- [ ] Frontend: No new packages yet

### Before Each Sprint
1. Check this document for new packages
2. Update `requirements.txt` or `package.json`
3. Run installation commands
4. Verify installations

---

## 🔄 How to Update

### Adding Backend Package
1. Add to `requirements.txt`
2. Run: `pip install package-name`
3. Update this document
4. Commit changes

### Adding Frontend Package
1. Run: `npm install package-name`
2. Updates `package.json` automatically
3. Update this document
4. Commit changes

---

## 📝 Notes

### Backend
- Use virtual environment (venv)
- Pin versions for stability
- Test after installing new packages

### Frontend
- Use exact versions in package.json
- Run `npm install` after pulling changes
- Clear cache if issues: `npm cache clean --force`

---

## 🚨 Important Reminders

1. **Always update this document** when adding packages
2. **Test installations** before committing
3. **Document why** each package is needed
4. **Check compatibility** between packages
5. **Monitor package sizes** for mobile app

---

**Last Package Added**: `mistralai>=1.0.0` (Sprint 2, Dec 24, 2024)
