from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from typing import Optional
import time
import logging
from app.services.dream_ai.api_manager.Speech_to_text_manager import WhisperSTTManager
from app.services.dream_ai.Speech_to_text.speech_text_shcema import (
    TranscriptionResponse,
    SupportedFormatsResponse,
    HealthCheckResponse,
    ErrorResponse
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/speech-to-text", tags=["Speech to Text"])

# Initialize the STT manager
stt_manager = None

def get_stt_manager() -> WhisperSTTManager:
    """Dependency to get or create the STT manager instance"""
    global stt_manager
    if stt_manager is None:
        try:
            stt_manager = WhisperSTTManager()
            logger.info("STT manager initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize STT manager: {str(e)}")
            raise HTTPException(status_code=500, detail=f"STT service initialization failed: {str(e)}")
    return stt_manager

@router.post(
    "/transcribe", 
    response_model=TranscriptionResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request - Invalid file or parameters"},
        500: {"model": ErrorResponse, "description": "Internal Server Error - Processing failed"}
    }
)
async def transcribe_audio(
    audio_file: UploadFile = File(..., description="Audio file to transcribe (max 25MB)"),
    language: Optional[str] = Form(None, description="Optional language code (e.g., 'en', 'es', 'fr')"),
    manager: WhisperSTTManager = Depends(get_stt_manager)
):
    """
    Transcribe an audio file to text using OpenAI Whisper.
    
    **Supported formats:** mp3, mp4, mpeg, mpga, m4a, wav, webm  
    **Maximum file size:** 25MB  
    **Languages:** Auto-detect or specify language code
    
    **Returns:**
    - **text**: The transcribed text
    - **language**: Language used for transcription
    - **filename**: Original filename
    - **file_size_bytes**: Size of uploaded file
    - **processing_time**: Time taken to process
    """
    start_time = time.time()
    
    try:
        # Validate file type
        if not audio_file.content_type:
            raise HTTPException(status_code=400, detail="Could not determine file type")
            
        if not any(fmt in audio_file.content_type.lower() for fmt in ['audio', 'video']):
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type: {audio_file.content_type}. Must be an audio or video file"
            )
        
        # Read file content
        logger.info(f"Reading audio file: {audio_file.filename}")
        audio_content = await audio_file.read()
        
        if len(audio_content) == 0:
            raise HTTPException(status_code=400, detail="Empty audio file")
        
        # Transcribe the audio
        logger.info(f"Starting transcription for file: {audio_file.filename} ({len(audio_content)} bytes)")
        result = await manager.transcribe_audio(
            audio_file_content=audio_content,
            filename=audio_file.filename or "audio_file",
            language=language
        )
        
        processing_time = time.time() - start_time
        logger.info(f"Transcription completed in {processing_time:.2f} seconds")
        
        # Return the structured response
        return TranscriptionResponse(
            text=result["text"],
            language=result["language"],
            filename=result["filename"],
            file_size_bytes=result["file_size_bytes"],
            processing_time=round(processing_time, 2)
        )
        
    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        error_msg = f"Transcription failed: {str(e)}"
        logger.error(error_msg)
        logger.exception("Full traceback:")
        raise HTTPException(status_code=500, detail=error_msg)

@router.get(
    "/supported-formats", 
    response_model=SupportedFormatsResponse,
    summary="Get supported audio formats",
    description="Get information about supported audio formats, file size limits, and other constraints"
)
async def get_supported_formats():
    """Get information about supported audio formats and limitations"""
    return SupportedFormatsResponse(
        supported_formats=["mp3", "mp4", "mpeg", "mpga", "m4a", "wav", "webm"],
        max_file_size_mb=25,
        model="whisper-1",
        supported_languages="Auto-detect or specify language code (e.g., 'en', 'es', 'fr', 'de', etc.)",
        description="Convert speech to text using OpenAI Whisper"
    )

@router.get(
    "/health", 
    response_model=HealthCheckResponse,
    summary="Health check",
    description="Check if the Speech-to-Text service is healthy and operational"
)
async def stt_health_check(manager: WhisperSTTManager = Depends(get_stt_manager)):
    """Speech-to-Text service health check"""
    try:
        model_info = manager.get_model_info()
        return HealthCheckResponse(
            status="healthy", 
            service="Speech-to-Text API",
            model=model_info
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"STT service unhealthy: {str(e)}")