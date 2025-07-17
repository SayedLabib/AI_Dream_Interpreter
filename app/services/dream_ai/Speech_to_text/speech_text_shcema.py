from pydantic import BaseModel, Field
from typing import Optional

class TranscriptionRequest(BaseModel):
    """Request model for audio transcription"""
    language: Optional[str] = Field(None, description="Optional language code (e.g., 'en', 'es', 'fr')")

class TranscriptionResponse(BaseModel):
    """Response model for audio transcription"""
    text: str = Field(..., description="Transcribed text from the audio")
    language: str = Field(..., description="Language used for transcription (detected or specified)")
    filename: str = Field(..., description="Original filename of the audio file")
    file_size_bytes: int = Field(..., description="Size of the audio file in bytes")
    processing_time: float = Field(..., description="Time taken to process the audio in seconds")

class SupportedFormatsResponse(BaseModel):
    """Response model for supported formats information"""
    supported_formats: list[str] = Field(..., description="List of supported audio formats")
    max_file_size_mb: int = Field(..., description="Maximum file size in MB")
    model: str = Field(..., description="Whisper model being used")
    supported_languages: str = Field(..., description="Information about supported languages")
    description: str = Field(..., description="Service description")

class HealthCheckResponse(BaseModel):
    """Response model for health check"""
    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    model: Optional[dict] = Field(None, description="Model information")

class ErrorResponse(BaseModel):
    """Response model for errors"""
    detail: str = Field(..., description="Error message")