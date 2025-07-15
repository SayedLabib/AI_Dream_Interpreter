import time
from typing import Optional
from app.services.dream_ai.api_manager.image_gen_manager import OpenAIManager
from app.services.dream_ai.image_gen_service.image_gen_schema import (
    DreamAnalysisRequest,
    ImageGenerationRequest,
    CompleteDreamResponse,
    DreamAnalysisResponse,
    ImageGenerationResponse
)

class DreamAIService:
    def __init__(self):
        self.openai_manager = OpenAIManager()
    
    async def analyze_dream_only(self, request: DreamAnalysisRequest) -> DreamAnalysisResponse:
        """Analyze a dream without generating an image"""
        try:
            analysis = await self.openai_manager.analyze_dream(
                dream_description=request.dream_description,
                user_name=request.user_name
            )
            return analysis
        except Exception as e:
            raise Exception(f"Dream analysis failed: {str(e)}")
    
    async def generate_image_only(self, request: ImageGenerationRequest) -> ImageGenerationResponse:
        """Generate an image based on dream description"""
        try:
            image_response = await self.openai_manager.generate_dream_image(
                dream_description=request.dream_description,
                style=request.style
            )
            return image_response
        except Exception as e:
            raise Exception(f"Image generation failed: {str(e)}")
    
    async def complete_dream_interpretation(
        self, 
        dream_description: str, 
        user_name: Optional[str] = None,
        image_style: str = "realistic"
    ) -> CompleteDreamResponse:
        """Complete dream analysis and image generation"""
        
        start_time = time.time()
        
        try:
            # Perform dream analysis and image generation concurrently
            analysis_task = self.openai_manager.analyze_dream(dream_description, user_name)
            image_task = self.openai_manager.generate_dream_image(dream_description, image_style)
            
            # Wait for both tasks to complete
            import asyncio
            analysis, generated_image = await asyncio.gather(analysis_task, image_task)
            
            processing_time = time.time() - start_time
            
            return CompleteDreamResponse(
                analysis=analysis,
                generated_image=generated_image,
                processing_time=processing_time
            )
            
        except Exception as e:
            raise Exception(f"Complete dream interpretation failed: {str(e)}")