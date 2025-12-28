"""
Main FastAPI application.

This is the entry point for the AI Surrogate backend API.
"""

from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.database import init_db
from app.config import settings
from app.routes import auth_router, chat_router
from app.routes.preferences import router as preferences_router
from app.routes.conversations import router as conversations_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup: Initialize database
    print("🚀 Starting up AI Surrogate API...")
    print("📊 Initializing database...")
    init_db()
    print("✅ Database initialized successfully!")
    
    yield
    
    # Shutdown
    print("👋 Shutting down AI Surrogate API...")


# Create FastAPI application
app = FastAPI(
    title="AI Surrogate API",
    version="1.0.0",
    description="""
    Backend API for AI Surrogate Human Clone mobile application.
    
    ## Features
    
    * **Authentication**: User registration and login with JWT tokens
    * **Chat**: Real-time messaging with AI assistant
    * **Conversations**: Manage conversation history
    * **Multilingual**: Support for multiple languages (Phase 2)
    * **Voice**: Speech-to-text and text-to-speech (Phase 2)
    
    ## Authentication
    
    Most endpoints require authentication. To authenticate:
    
    1. Register a new account at `/api/auth/register`
    2. Login at `/api/auth/login` to get an access token
    3. Include the token in the Authorization header: `Bearer <token>`
    
    ## Phase 1 (Current)
    
    - Basic authentication
    - Echo chat responses
    - Conversation management
    
    ## Coming Soon
    
    - Real AI responses (DeepSeek API)
    - Voice input/output
    - Multilingual support
    - Task execution agents
    """,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(preferences_router)
app.include_router(conversations_router)


@app.get(
    "/",
    tags=["Root"],
    summary="API Root",
    description="Welcome endpoint with API information"
)
def root():
    """
    Root endpoint providing API information.
    """
    return {
        "message": "Welcome to AI Surrogate API",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "auth": "/api/auth",
            "chat": "/api/chat"
        }
    }


@app.get(
    "/health",
    tags=["Health"],
    summary="Health Check",
    description="Check if the API is running and healthy"
)
def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns the current status and timestamp.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "AI Surrogate API",
        "version": "1.0.0"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors.
    """
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc) if settings.DATABASE_URL else "An error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
