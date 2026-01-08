# Environment Variables Setup Guide

## Quick Start

For **immediate functionality**, you need these **REQUIRED** variables:

```env
DATABASE_URL=your-supabase-database-url
SECRET_KEY=your-secret-key
MISTRAL_API_KEY=your-mistral-api-key
```

## Complete Setup

### 1. Core Configuration (REQUIRED)

```env
# Database - Get from Supabase Dashboard
DATABASE_URL=postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres

# Secret Key - Generate with: openssl rand -hex 32
SECRET_KEY=your-generated-secret-key-here

# CORS (for mobile app)
ALLOWED_ORIGINS=http://localhost:8081,http://localhost:19000
```

### 2. AI Configuration (REQUIRED)

```env
# Mistral AI - Get from https://console.mistral.ai/
MISTRAL_API_KEY=your-mistral-api-key
```

### 3. Voice Features (FREE - No Configuration Needed!)

**✅ Voice features work completely FREE with NO billing required!**

The app uses free alternatives that work out of the box:

**Speech-to-Text (STT):**
- **SpeechRecognition library** - Free, no API key needed
- Uses Google Web Speech API (free tier, no billing)
- Works automatically, no configuration required

**Text-to-Speech (TTS):**
- **Edge TTS** (Microsoft Edge TTS) - Completely free, no API key needed
- **gTTS** (Google Text-to-Speech) - Free, no billing required
- Works automatically, no configuration required

**No `.env` variables needed for voice features!**

They work immediately after installing dependencies:
```bash
pip install SpeechRecognition gtts edge-tts pydub
```

**Optional: Google Cloud (Fallback Only)**
If you want to use Google Cloud as a fallback (requires billing), you can optionally add:
```env
GOOGLE_APPLICATION_CREDENTIALS=C:/path/to/credentials.json
```

But this is **NOT required** - voice features work perfectly without it!

### 4. Search Features (OPTIONAL - but recommended)

**Option A: Brave Search (Recommended)**

1. Go to [Brave Search API](https://brave.com/search/api/)
2. Sign up for free account
3. Get API key
4. Add to `.env`:

```env
BRAVE_API_KEY=your-brave-api-key
```

**Free Tier:** 2000 queries/month

**Option B: SerpAPI (Alternative)**

1. Go to [SerpAPI](https://serpapi.com/)
2. Sign up for free account
3. Get API key
4. Add to `.env`:

```env
SERPAPI_KEY=your-serpapi-key
```

**Free Tier:** 100 searches/month

## Minimal Setup (Chat Only)

If you just want basic chat functionality:

```env
DATABASE_URL=your-database-url
SECRET_KEY=your-secret-key
MISTRAL_API_KEY=your-mistral-key
```

Voice and search will be disabled but chat will work.

## Full Setup (All Features)

```env
# Core
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
MISTRAL_API_KEY=your-mistral-key

# Voice
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
# OR
GOOGLE_CREDENTIALS_JSON={"type":"service_account",...}

# Search (at least one)
BRAVE_API_KEY=your-brave-key
# OR
SERPAPI_KEY=your-serpapi-key
```

## Testing Your Setup

After adding variables, test with:

```bash
# Start backend
cd ai-surrogate-backend
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit: http://localhost:8000/docs

Check the `/health` endpoint - it should return "healthy".

## Troubleshooting

### Voice not working?
- Check Google Cloud credentials are valid
- Verify APIs are enabled in Google Cloud Console
- Check logs for authentication errors

### Search not working?
- Verify at least one API key is set (Brave or SerpAPI)
- Check API key is valid
- Check free tier limits haven't been exceeded

### Chat not working?
- Verify MISTRAL_API_KEY is set
- Check Mistral API dashboard for usage/quota

## Security Notes

⚠️ **Never commit `.env` to git!**

- `.env` is in `.gitignore`
- Use environment variables in production (Railway, Render, etc.)
- Rotate keys if accidentally exposed
