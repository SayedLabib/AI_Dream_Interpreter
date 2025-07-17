from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.services.dream_ai.image_gen_service.image_gen_router import router as dream_router
from app.services.dream_ai.Speech_to_text.speech_to_text_router import router as stt_router

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="AI-powered dream interpretation and visualization service with speech-to-text capabilities",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(dream_router)
app.include_router(stt_router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Dream AI - Your Personal Dream Interpreter with Speech-to-Text",
        "version": "1.0.0",
        "models": {
            "chat": "gpt-3.5-turbo",
            "image": "dall-e-3",
            "speech": "whisper-1"
        },
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "dream_analysis": "/api/v1/dream-ai/complete-interpretation",
            "speech_transcribe": "/api/v1/speech-to-text/transcribe",
            "speech_formats": "/api/v1/speech-to-text/supported-formats",
            "speech_health": "/api/v1/speech-to-text/health"
        },
        "features": {
            "dream_analysis": "Complete interpretation with image generation",
            "dream_patterns": "Categorization across 6 dream types with percentages",
            "visual_symbolism": "AI explains how image elements represent dream symbols",
            "speech_to_text": "Convert voice recordings to text using OpenAI Whisper"
        }
    }

@app.get("/health")
async def health_check():
    """Application health check"""
    return {"status": "healthy", "app": settings.app_name}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8063,
        reload=settings.debug
    )