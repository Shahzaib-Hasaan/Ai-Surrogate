"""
Voice API routes.

Endpoints:
- POST /api/voice/transcribe - Convert audio to text
- POST /api/voice/synthesize - Convert text to audio
- GET /api/voice/languages - List supported languages
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional
import logging

from app.database import get_db
from app.models import User
from app.services.auth_service import get_current_user
from app.services.voice_service import get_voice_service, SUPPORTED_LANGUAGES, SUPPORTED_VOICES

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/voice", tags=["Voice"])


@router.post(
    "/transcribe",
    summary="Transcribe audio to text",
    description="Convert audio file to text using Google Cloud Speech-to-Text"
)
async def transcribe_audio(
    audio_file: UploadFile = File(...),
    language_code: Optional[str] = Form("en-US"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Transcribe audio to text.
    
    - **audio_file**: Audio file (WebM, MP3, WAV, FLAC)
    - **language_code**: Language code (en-US, ur-PK, pa-IN)
    
    Returns transcribed text with confidence score.
    """
    try:
        # Read audio file
        audio_data = await audio_file.read()
        
        if len(audio_data) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Audio file is empty"
            )
        
        # Determine audio format from filename or content type
        filename = audio_file.filename or ""
        content_type = getattr(audio_file, 'content_type', '') or ''
        
        # Detect format
        audio_format = "webm_opus"  # Default for Expo
        if filename.endswith(".mp3") or "mp3" in content_type.lower():
            audio_format = "mp3"
        elif filename.endswith(".wav") or "wav" in content_type.lower():
            audio_format = "wav"
        elif filename.endswith(".flac") or "flac" in content_type.lower():
            audio_format = "flac"
        elif filename.endswith(".webm") or "webm" in content_type.lower():
            audio_format = "webm_opus"
        
        logger.info(f"📁 Audio file: {filename}, format: {audio_format}, size: {len(audio_data)} bytes")
        
        # Get voice service
        voice_service = get_voice_service()
        
        # Transcribe with timeout
        import asyncio
        try:
            result = await asyncio.wait_for(
                asyncio.to_thread(
                    voice_service.transcribe_audio,
                    audio_data=audio_data,
                    language_code=language_code,
                    audio_format=audio_format
                ),
                timeout=30.0
            )
        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Transcription timeout. Please try again with a shorter audio."
            )
        
        if not result.get("success"):
            error_msg = result.get("error", "Transcription failed")
            logger.error(f"❌ Transcription failed: {error_msg}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=error_msg
            )
        
        return {
            "success": True,
            "text": result["text"],
            "confidence": result["confidence"],
            "language_code": result["language_code"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Transcription error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error transcribing audio: {str(e)}"
        )


@router.post(
    "/synthesize",
    summary="Synthesize text to speech",
    description="Convert text to audio using Google Cloud Text-to-Speech"
)
async def synthesize_speech(
    text: str = Form(...),
    language_code: Optional[str] = Form("en-US"),
    voice_name: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Synthesize text to speech.
    
    - **text**: Text to synthesize (max 5000 characters)
    - **language_code**: Language code (en-US, ur-PK, pa-IN)
    - **voice_name**: Specific voice name (optional)
    
    Returns base64-encoded audio (MP3 format).
    """
    try:
        # Validate text length
        if len(text) > 5000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text too long (max 5000 characters)"
            )
        
        if not text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text cannot be empty"
            )
        
        # Get voice service
        voice_service = get_voice_service()
        
        # Synthesize
        result = voice_service.synthesize_speech(
            text=text,
            language_code=language_code,
            voice_name=voice_name
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Synthesis failed")
            )
        
        return {
            "success": True,
            "audio_base64": result["audio_base64"],
            "audio_format": result["audio_format"],
            "language_code": result["language_code"],
            "voice_name": result["voice_name"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error synthesizing speech: {str(e)}"
        )


@router.get(
    "/languages",
    summary="Get supported languages",
    description="List all supported languages for STT and TTS"
)
async def get_supported_languages(
    current_user: User = Depends(get_current_user)
):
    """
    Get list of supported languages and voices.
    
    Returns available languages with their codes and voices.
    """
    return {
        "success": True,
        "languages": {
            code: {
                "name": name,
                "voices": SUPPORTED_VOICES.get(code.split("-")[0], [])
            }
            for code, name in SUPPORTED_LANGUAGES.items()
        },
        "supported_codes": list(SUPPORTED_LANGUAGES.values())
    }
