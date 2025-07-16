from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.services.dream_ai.image_gen_service.image_gen_service import DreamAIService
from app.services.dream_ai.image_gen_service.image_gen_schema import (
    CompleteDreamRequest,
    CompleteDreamResponse
)

router = APIRouter(prefix="/api/v1/dream-ai", tags=["Dream AI"])

# Dependency to get the service
def get_dream_service() -> DreamAIService:
    try:
        return DreamAIService()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Service initialization failed: {str(e)}")

@router.post("/complete-interpretation", response_model=CompleteDreamResponse)
async def complete_dream_interpretation(
    request: CompleteDreamRequest,
    service: DreamAIService = Depends(get_dream_service)
):
    """
    Complete dream interpretation including analysis and image generation.
    
    - **dream_description**: The user's dream description
    Note: Style is hardcoded to 'realistic' for consistency
    """
    try:
        result = await service.complete_dream_interpretation(
            dream_description=request.dream_description
        )
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Configuration error: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Complete interpretation failed: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Dream AI API"}

@router.get("/models")
async def get_models_info(service: DreamAIService = Depends(get_dream_service)):
    """Get information about the AI models being used"""
    model_info = service.openai_manager.get_model_info()
    return {
        "status": "active",
        "models": model_info,
        "capabilities": {
            "dream_analysis": f"Powered by {model_info['chat_model']}",
            "image_generation": f"Powered by {model_info['image_model']}",
            "supported_styles": ["realistic (hardcoded)"]
        }
    }