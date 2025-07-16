from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.services.dream_ai.image_gen_service.image_gen_router import router as dream_router

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="AI-powered dream interpretation and visualization service",
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

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Dream AI - Your Personal Dream Interpreter",
        "version": "1.0.0",
        "models": {
            "chat": "gpt-3.5-turbo",
            "image": "dall-e-3"
        },
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "analyze": "/api/v1/dream-ai/analyze",
            "generate_image": "/api/v1/dream-ai/generate-image",
            "complete": "/api/v1/dream-ai/complete-interpretation"
        },
        "features": {
            "style": "hardcoded to realistic",
            "personalization": "removed user_name field"
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
        port=8020,
        reload=settings.debug
    )