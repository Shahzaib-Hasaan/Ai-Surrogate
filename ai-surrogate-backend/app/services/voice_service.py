"""
Voice Service - Speech-to-Text and Text-to-Speech

Uses FREE alternatives that require NO billing:
- STT: SpeechRecognition library (free, no API key needed)
- TTS: Edge TTS or gTTS (free, no billing required)

Google Cloud is kept as optional fallback (requires billing).
"""

import os
import logging
import base64
from typing import Optional, Dict, Any
from io import BytesIO
import tempfile

# Free STT - Primary option
try:
    import speech_recognition as sr
    from pydub import AudioSegment
    speech_recognition_available = True
except ImportError:
    speech_recognition_available = False

# Free TTS alternatives (no billing required)
try:
    from gtts import gTTS
    gtts_available = True
except ImportError:
    gtts_available = False

try:
    import edge_tts
    edge_tts_available = True
except ImportError:
    edge_tts_available = False

# Optional: Google Cloud (requires billing - fallback only)
try:
    from google.cloud import speech_v1
    from google.cloud import texttospeech_v1
    from google.oauth2 import service_account
    google_cloud_available = True
except ImportError:
    speech_v1 = None
    texttospeech_v1 = None
    service_account = None
    google_cloud_available = False

from app.config import settings

logger = logging.getLogger(__name__)

# Supported languages
SUPPORTED_LANGUAGES = {
    "en": "en-US",
    "ur": "ur-PK",
    "pa": "pa-IN",  # Punjabi
}

# Supported voices for TTS
SUPPORTED_VOICES = {
    "en": ["en-US-Neural2-A", "en-US-Neural2-C", "en-US-Neural2-D"],
    "ur": ["ur-PK-Standard-A", "ur-PK-Standard-B"],
    "pa": ["pa-IN-Standard-A", "pa-IN-Standard-B"],
}


class VoiceService:
    """
    Voice processing service using Google Cloud APIs.
    
    Handles:
    - Speech-to-Text (STT): Convert audio to text
    - Text-to-Speech (TTS): Convert text to audio
    """
    
    def __init__(self):
        """Initialize voice service with free alternatives."""
        self.stt_client = None
        self.tts_client = None
        self.recognizer = None
        
        # Initialize free STT (SpeechRecognition)
        if speech_recognition_available:
            try:
                self.recognizer = sr.Recognizer()
                logger.info("✅ Free STT (SpeechRecognition) initialized")
            except Exception as e:
                logger.warning(f"⚠️ SpeechRecognition initialization failed: {e}")
        
        # Optional: Initialize Google Cloud (requires billing - fallback only)
        if google_cloud_available:
            self._initialize_google_cloud()
        else:
            logger.info("ℹ️ Google Cloud not installed - using free alternatives only")
    
    def _initialize_google_cloud(self):
        """Initialize Google Cloud clients (optional, requires billing)."""
        try:
            google_credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            google_credentials_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
            
            credentials = None
            
            if google_credentials_path and os.path.exists(google_credentials_path):
                credentials = service_account.Credentials.from_service_account_file(
                    google_credentials_path
                )
                logger.info("✅ Google Cloud credentials loaded (fallback only)")
            elif google_credentials_json:
                import json
                creds_dict = json.loads(google_credentials_json)
                credentials = service_account.Credentials.from_service_account_info(creds_dict)
                logger.info("✅ Google Cloud credentials loaded from JSON (fallback only)")
            else:
                return  # No Google Cloud - that's fine, we use free alternatives
            
            # Initialize clients (optional)
            if speech_v1 and credentials:
                self.stt_client = speech_v1.SpeechClient(credentials=credentials)
                logger.info("✅ Google Cloud STT available (fallback)")
            
            if texttospeech_v1 and credentials:
                self.tts_client = texttospeech_v1.TextToSpeechClient(credentials=credentials)
                logger.info("✅ Google Cloud TTS available (fallback)")
                
        except Exception as e:
            logger.warning(f"⚠️ Google Cloud initialization failed (using free alternatives): {e}")
    
    def transcribe_audio(
        self,
        audio_data: bytes,
        language_code: str = "en-US",
        audio_format: str = "webm_opus"
    ) -> Dict[str, Any]:
        """
        Transcribe audio to text using FREE SpeechRecognition library.
        
        Falls back to Google Cloud only if free method fails and credentials are available.
        
        Args:
            audio_data: Audio file bytes
            language_code: Language code (e.g., "en-US", "ur-PK")
            audio_format: Audio format (webm_opus, mp3, wav, etc.)
            
        Returns:
            Dict with transcription text and confidence
        """
        # Try free SpeechRecognition first (primary method)
        if self.recognizer:
            try:
                return self._transcribe_speech_recognition(audio_data, language_code, audio_format)
            except Exception as e:
                logger.warning(f"Free STT failed: {e}, trying fallback...")
        
        # Fallback to Google Cloud (if available and configured)
        if self.stt_client:
            try:
                return self._transcribe_google_cloud(audio_data, language_code, audio_format)
            except Exception as e:
                logger.error(f"Google Cloud STT failed: {e}")
        
        # All methods failed
        return {
            "success": False,
            "error": "STT not available. Please install SpeechRecognition: pip install SpeechRecognition pydub"
        }
    
    def _transcribe_speech_recognition(
        self,
        audio_data: bytes,
        language_code: str,
        audio_format: str
    ) -> Dict[str, Any]:
        """Transcribe using free SpeechRecognition library (no billing required)."""
        # Map language codes
        lang_map = {
            "en-US": "en-US",
            "ur-PK": "ur-PK",
            "pa-IN": "pa-IN",
        }
        sr_lang = lang_map.get(language_code, "en-US")
        
        # Convert audio format if needed
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{audio_format.split('_')[0]}") as temp_file:
            temp_file.write(audio_data)
            temp_path = temp_file.name
        
        try:
            # Convert to WAV if needed (SpeechRecognition works best with WAV)
            if audio_format != "wav":
                audio = AudioSegment.from_file(temp_path, format=audio_format.split('_')[0])
                wav_path = temp_path.replace(f".{audio_format.split('_')[0]}", ".wav")
                audio.export(wav_path, format="wav")
                os.remove(temp_path)
                temp_path = wav_path
            
            # Load audio file
            with sr.AudioFile(temp_path) as source:
                audio = self.recognizer.record(source)
            
            logger.info(f"🎤 Transcribing with free STT ({len(audio_data)} bytes, {sr_lang})")
            
            # Try Google Web Speech API (free, no key needed)
            try:
                text = self.recognizer.recognize_google(audio, language=sr_lang)
                logger.info(f"✅ Transcription: {text[:50]}...")
                return {
                    "success": True,
                    "text": text,
                    "confidence": 0.85,  # Estimated confidence
                    "language_code": language_code,
                    "provider": "speech_recognition_google"
                }
            except sr.UnknownValueError:
                return {
                    "success": False,
                    "error": "Could not understand audio"
                }
            except sr.RequestError as e:
                # Try offline recognition as fallback
                try:
                    text = self.recognizer.recognize_sphinx(audio, language=sr_lang)
                    return {
                        "success": True,
                        "text": text,
                        "confidence": 0.70,
                        "language_code": language_code,
                        "provider": "speech_recognition_sphinx"
                    }
                except:
                    raise Exception(f"Speech recognition failed: {e}")
        
        finally:
            # Cleanup temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def _transcribe_google_cloud(
        self,
        audio_data: bytes,
        language_code: str,
        audio_format: str
    ) -> Dict[str, Any]:
        """Transcribe using Google Cloud (fallback, requires billing)."""
        if not speech_v1 or not self.stt_client:
            raise Exception("Google Cloud STT not available")
        
        encoding_map = {
            "webm_opus": speech_v1.RecognitionConfig.AudioEncoding.WEBM_OPUS,
            "mp3": speech_v1.RecognitionConfig.AudioEncoding.MP3,
            "wav": speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
            "flac": speech_v1.RecognitionConfig.AudioEncoding.FLAC,
        }
        
        encoding = encoding_map.get(audio_format.lower(), speech_v1.RecognitionConfig.AudioEncoding.WEBM_OPUS)
        
        config = speech_v1.RecognitionConfig(
            encoding=encoding,
            sample_rate_hertz=16000,
            language_code=language_code,
            enable_automatic_punctuation=True,
            model="latest_long",
        )
        
        audio = speech_v1.RecognitionAudio(content=audio_data)
        
        logger.info(f"🎤 Transcribing with Google Cloud STT (fallback)")
        response = self.stt_client.recognize(config=config, audio=audio)
        
        if not response.results:
            return {
                "success": False,
                "error": "No speech detected in audio"
            }
        
        result = response.results[0]
        alternative = result.alternatives[0]
        
        return {
            "success": True,
            "text": alternative.transcript,
            "confidence": alternative.confidence,
            "language_code": language_code,
            "provider": "google_cloud"
        }
    
    def synthesize_speech(
        self,
        text: str,
        language_code: str = "en-US",
        voice_name: Optional[str] = None,
        ssml_gender: str = "NEUTRAL"
    ) -> Dict[str, Any]:
        """
        Synthesize text to speech using free alternatives (gTTS or Edge TTS).
        
        Falls back to free TTS if Google Cloud TTS is not available (billing required).
        
        Args:
            text: Text to synthesize
            language_code: Language code (e.g., "en-US", "ur-PK")
            voice_name: Specific voice name (optional, ignored for free TTS)
            ssml_gender: Voice gender (ignored for free TTS)
            
        Returns:
            Dict with audio data (base64) and format
        """
        # Use free TTS options first (no billing required)
        # Try Edge TTS first (better quality)
        if edge_tts_available:
            try:
                return self._synthesize_edge_tts(text, language_code)
            except Exception as e:
                logger.warning(f"Edge TTS failed: {e}")
        
        # Fallback to gTTS
        if gtts_available:
            try:
                return self._synthesize_gtts(text, language_code)
            except Exception as e:
                logger.warning(f"gTTS failed: {e}")
        
        # Last resort: Google Cloud TTS (if available, requires billing)
        if self.tts_client:
            try:
                return self._synthesize_google_cloud(text, language_code, voice_name, ssml_gender)
            except Exception as e:
                logger.warning(f"Google Cloud TTS failed: {e}")
        
        # All TTS methods failed
        return {
            "success": False,
            "error": "TTS not available. Please install: pip install gtts edge-tts"
        }
    
    def _synthesize_google_cloud(
        self,
        text: str,
        language_code: str,
        voice_name: Optional[str],
        ssml_gender: str
    ) -> Dict[str, Any]:
        """Synthesize using Google Cloud TTS (requires billing)."""
        if not texttospeech_v1 or not self.tts_client:
            raise Exception("Google Cloud TTS not available")
        
        if not voice_name:
            lang_prefix = language_code.split("-")[0]
            available_voices = SUPPORTED_VOICES.get(lang_prefix, SUPPORTED_VOICES["en"])
            voice_name = available_voices[0]
        
        synthesis_input = texttospeech_v1.SynthesisInput(text=text)
        voice = texttospeech_v1.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name,
            ssml_gender=getattr(texttospeech_v1.SsmlVoiceGender, ssml_gender)
        )
        audio_config = texttospeech_v1.AudioConfig(
            audio_encoding=texttospeech_v1.AudioEncoding.MP3,
            speaking_rate=1.0,
            pitch=0.0,
        )
        
        logger.info(f"🔊 Using Google Cloud TTS ({len(text)} chars, {language_code})")
        response = self.tts_client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        audio_base64 = base64.b64encode(response.audio_content).decode('utf-8')
        return {
            "success": True,
            "audio_base64": audio_base64,
            "audio_format": "mp3",
            "language_code": language_code,
            "voice_name": voice_name,
            "provider": "google_cloud"
        }
    
    def _synthesize_edge_tts(self, text: str, language_code: str) -> Dict[str, Any]:
        """Synthesize using Edge TTS (free, no billing required)."""
        import asyncio
        
        # Map language codes to Edge TTS format
        lang_map = {
            "en-US": "en-US",
            "ur-PK": "ur",  # Edge TTS may not support Urdu, fallback to English
            "pa-IN": "en-US",  # Fallback to English
        }
        edge_lang = lang_map.get(language_code, "en-US")
        
        # Get available voice for language
        async def get_voice():
            voices = await edge_tts.list_voices()
            for voice in voices:
                if edge_lang in voice["Locale"]:
                    return voice["ShortName"]
            return "en-US-AriaNeural"  # Default English voice
        
        async def synthesize():
            voice_name = await get_voice()
            communicate = edge_tts.Communicate(text, voice_name)
            audio_data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            return audio_data, voice_name
        
        logger.info(f"🔊 Using Edge TTS (free, {len(text)} chars, {language_code})")
        audio_data, voice_name = asyncio.run(synthesize())
        
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        return {
            "success": True,
            "audio_base64": audio_base64,
            "audio_format": "mp3",
            "language_code": language_code,
            "voice_name": voice_name,
            "provider": "edge_tts"
        }
    
    def _synthesize_gtts(self, text: str, language_code: str) -> Dict[str, Any]:
        """Synthesize using gTTS (free, no billing required)."""
        # Map language codes to gTTS format
        lang_map = {
            "en-US": "en",
            "ur-PK": "ur",
            "pa-IN": "pa",
        }
        gtts_lang = lang_map.get(language_code, "en")
        
        logger.info(f"🔊 Using gTTS (free, {len(text)} chars, {language_code})")
        
        # Create gTTS object
        tts = gTTS(text=text, lang=gtts_lang, slow=False)
        
        # Save to bytes
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        audio_data = audio_buffer.read()
        
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        return {
            "success": True,
            "audio_base64": audio_base64,
            "audio_format": "mp3",
            "language_code": language_code,
            "voice_name": f"gTTS-{gtts_lang}",
            "provider": "gtts"
        }
    
    def detect_language_from_audio(
        self,
        audio_data: bytes,
        possible_languages: list = None
    ) -> Optional[str]:
        """
        Detect language from audio by trying multiple language codes.
        
        Args:
            audio_data: Audio file bytes
            possible_languages: List of possible language codes to try
            
        Returns:
            Detected language code or None
        """
        if not possible_languages:
            possible_languages = ["en-US", "ur-PK", "pa-IN"]
        
        # Try each language and pick the one with highest confidence
        best_result = None
        best_confidence = 0.0
        
        for lang_code in possible_languages:
            result = self.transcribe_audio(audio_data, language_code=lang_code)
            if result.get("success") and result.get("confidence", 0) > best_confidence:
                best_confidence = result["confidence"]
                best_result = result
        
        return best_result.get("language_code") if best_result else None


# Global voice service instance
_voice_service = None


def get_voice_service() -> VoiceService:
    """Get or create global voice service instance."""
    global _voice_service
    if _voice_service is None:
        _voice_service = VoiceService()
    return _voice_service
