import openai
import asyncio
import tempfile
import os
from typing import Optional, Dict, Any
from app.core.config import settings
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WhisperSTTManager:
    def __init__(self):
        # Validate API key
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        if not settings.openai_api_key.startswith('sk-'):
            raise ValueError("Invalid OpenAI API key format")
        
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
        
        # Whisper model configuration
        self.whisper_model = "whisper-1"
        
        # Supported audio formats
        self.supported_formats = {
            'mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'wav', 'webm'
        }
        
        # Maximum file size (25MB as per OpenAI limit)
        self.max_file_size = 25 * 1024 * 1024  # 25MB in bytes
        
        logger.info("WhisperSTTManager initialized successfully")
    
    def get_model_info(self) -> Dict[str, str]:
        """Get information about the Whisper model being used"""
        return {
            "stt_model": self.whisper_model,
            "supported_formats": list(self.supported_formats),
            "max_file_size_mb": "25",
            "description": f"Using {self.whisper_model} for speech-to-text conversion"
        }
    
    async def transcribe_audio(
        self, 
        audio_file_content: bytes, 
        filename: str,
        language: Optional[str] = None,
        prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Transcribe audio file to text using OpenAI Whisper
        
        Args:
            audio_file_content: Raw audio file bytes
            filename: Original filename (used to determine format)
            language: Optional language code (e.g., 'en', 'es', 'fr')
            prompt: Optional prompt to guide the model's style
        
        Returns:
            Dict containing transcription text and metadata
        """
        
        try:
            # Validate file size
            if len(audio_file_content) > self.max_file_size:
                raise ValueError(f"Audio file too large. Maximum size is 25MB, got {len(audio_file_content) / (1024*1024):.2f}MB")
            
            # Validate file format
            file_extension = filename.lower().split('.')[-1] if '.' in filename else ''
            if file_extension not in self.supported_formats:
                raise ValueError(f"Unsupported audio format: {file_extension}. Supported formats: {', '.join(self.supported_formats)}")
            
            logger.info(f"Starting transcription for file: {filename} ({len(audio_file_content)} bytes)")
            
            # Create temporary file for OpenAI API
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
                temp_file.write(audio_file_content)
                temp_file_path = temp_file.name
            
            try:
                # Prepare API parameters
                api_params = {
                    "model": self.whisper_model,
                    "file": open(temp_file_path, "rb"),
                    "response_format": "text"  # Simple text response
                }
                
                # Add optional parameters
                if language:
                    api_params["language"] = language
                if prompt:
                    api_params["prompt"] = prompt
                
                # Call OpenAI Whisper API asynchronously
                response = await asyncio.to_thread(
                    self.client.audio.transcriptions.create,
                    **api_params
                )
                
                # Close the file
                api_params["file"].close()
                
                logger.info(f"Transcription completed successfully. Text length: {len(response)} characters")
                
                return {
                    "text": response,
                    "language": language or 'auto-detected',
                    "filename": filename,
                    "file_size_bytes": len(audio_file_content)
                }
                
            finally:
                # Clean up temporary file
                try:
                    os.unlink(temp_file_path)
                except OSError:
                    logger.warning(f"Could not delete temporary file: {temp_file_path}")
                
        except Exception as e:
            error_msg = f"Audio transcription failed: {str(e)}"
            logger.error(error_msg)
            logger.exception("Full traceback:")
            raise Exception(error_msg)