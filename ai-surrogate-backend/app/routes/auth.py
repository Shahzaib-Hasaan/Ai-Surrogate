"""
Authentication API routes.

Endpoints:
- POST /api/auth/register - Register a new user
- POST /api/auth/login - Login and get JWT token
- GET /api/auth/me - Get current user information
"""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import (
    hash_password,
    create_access_token,
    authenticate_user,
    get_current_user
)
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account and return an access token"
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user account.
    
    - **email**: Valid email address (must be unique)
    - **username**: Display name (must be unique, 3-50 characters)
    - **password**: Password (minimum 8 characters)
    
    Returns a JWT access token that can be used for authentication.
    """
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    # Check if username already exists
    existing_username = db.query(User).filter(User.username == user_data.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken"
        )
    
    # Create new user
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hash_password(user_data.password)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create access token
    access_token = create_access_token(
        data={
            "sub": new_user.email,
            "user_id": str(new_user.id)
        }
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/login",
    response_model=Token,
    summary="Login user",
    description="Authenticate user and return an access token"
)
def login(
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login with email and password.
    
    - **email**: User's email address
    - **password**: User's password
    
    Returns a JWT access token that can be used for authentication.
    """
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(
        data={
            "sub": user.email,
            "user_id": str(user.id)
        }
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Get information about the currently authenticated user"
)
def get_me(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user information.
    
    Requires authentication (JWT token in Authorization header).
    
    Returns the authenticated user's profile information.
    """
    return current_user
