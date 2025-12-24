# Railway Deployment Guide - AI Surrogate Backend

## 🚀 Quick Deploy to Railway (Free)

### Prerequisites
- GitHub account
- Railway account (sign up at railway.app)

---

## Step 1: Push Code to GitHub

```bash
# Initialize git (if not already done)
cd F:\Projects\AI-Surrogate
git init
git add .
git commit -m "Initial commit - AI Surrogate"

# Create a new repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/ai-surrogate.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy to Railway

### A. Sign Up & Create Project
1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your `ai-surrogate` repository
6. Select the `ai-surrogate-backend` folder

### B. Add PostgreSQL Database
1. In your Railway project, click "New"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically create a database

### C. Configure Environment Variables
Click on your backend service → "Variables" tab:

```env
# Database (Railway auto-fills this)
DATABASE_URL=postgresql://...  # Auto-generated

# App Settings
SECRET_KEY=your-secret-key-here-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Mistral AI
MISTRAL_API_KEY=your-mistral-api-key
MISTRAL_CHAT_MODEL=mistral-small-latest
MISTRAL_TITLE_MODEL=mistral-tiny-latest

# AI Settings
AI_TEMPERATURE=0.7
MAX_RESPONSE_TOKENS=1000

# CORS (Important!)
ALLOWED_ORIGINS=*
```

### D. Deploy Settings
Railway should auto-detect:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

If not, set them manually in Settings → Deploy.

---

## Step 3: Update Mobile App

Once deployed, Railway gives you a URL like:
```
https://ai-surrogate-backend-production.up.railway.app
```

Update `ai-surrogate-mobile/src/config/api.ts`:
```typescript
export const API_BASE_URL = 'https://your-app.railway.app';
```

---

## Step 4: Test Deployment

1. Visit: `https://your-app.railway.app/docs`
2. You should see the Swagger UI
3. Test the `/api/auth/register` endpoint
4. If it works, update your mobile app!

---

## 🔄 Auto-Deploy on Changes

**Every time you push to GitHub, Railway auto-deploys!**

```bash
# Make changes to your code
git add .
git commit -m "Updated feature X"
git push

# Railway automatically deploys in ~2 minutes
```

---

## 📊 Monitor Your App

Railway Dashboard shows:
- Deployment logs
- CPU/Memory usage
- Database metrics
- Request logs

---

## 💰 Free Tier Limits

Railway Free Tier:
- ✅ 500 hours/month (enough for development)
- ✅ 1GB RAM
- ✅ 1GB disk
- ✅ PostgreSQL database included

**Tip**: App sleeps after 5 min of inactivity, wakes up on first request (~2s delay)

---

## 🐛 Troubleshooting

### Database Connection Issues
Railway auto-sets `DATABASE_URL`. Make sure your `app/database.py` uses:
```python
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
```

### CORS Errors
Add to environment variables:
```
ALLOWED_ORIGINS=*
```

### Build Fails
Check `requirements.txt` has all dependencies:
```bash
pip freeze > requirements.txt
```

---

## Alternative: Render.com (Also Free)

If Railway doesn't work:
1. Go to render.com
2. Create "New Web Service"
3. Connect GitHub repo
4. Same environment variables
5. Free tier: 750 hours/month

---

## 🎯 Next Steps After Deployment

1. ✅ Deploy backend to Railway
2. ✅ Update mobile app with Railway URL
3. ✅ Test login from Expo Go
4. ✅ Push changes → auto-deploy!

---

**Estimated Time**: 15 minutes  
**Cost**: $0 (Free tier)  
**Auto-deploy**: Yes ✅
