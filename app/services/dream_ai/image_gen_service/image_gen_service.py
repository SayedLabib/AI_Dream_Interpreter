import time
import logging
from typing import Optional
from app.services.dream_ai.api_manager.image_gen_manager import OpenAIManager
from app.services.dream_ai.image_gen_service.image_gen_schema import (
    DreamAnalysisRequest,
    ImageGenerationRequest,
    CompleteDreamRequest,
    CompleteDreamResponse,
    DreamAnalysisResponse,
    ImageGenerationResponse
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DreamAIService:
    def __init__(self):
        try:
            self.openai_manager = OpenAIManager()
            logger.info("DreamAIService initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize DreamAIService: {str(e)}")
            raise
    
    async def analyze_dream_only(self, request: DreamAnalysisRequest) -> DreamAnalysisResponse:
        """Analyze a dream without generating an image"""
        try:
            analysis = await self.openai_manager.analyze_dream(
                dream_description=request.dream_description
            )
            return analysis
        except Exception as e:
            raise Exception(f"Dream analysis failed: {str(e)}")
    
    async def generate_image_only(self, request: ImageGenerationRequest) -> ImageGenerationResponse:
        """Generate an image based on dream description"""
        try:
            image_response = await self.openai_manager.generate_dream_image(
                dream_description=request.dream_description,
                style="realistic"  # Hardcoded to realistic
            )
            return image_response
        except Exception as e:
            raise Exception(f"Image generation failed: {str(e)}")
    
    async def complete_dream_interpretation(
        self, 
        dream_description: str
    ) -> CompleteDreamResponse:
        """
        Complete dream interpretation: Generate image first, then analyze with image context.
        The analysis will explain what each visual element in the generated image symbolizes.
        """
        
        start_time = time.time()
        logger.info(f"Starting complete dream interpretation for description: {dream_description[:100]}...")
        
        try:
            # Step 1: Generate the image based on dream description
            logger.info("Step 1: Generating dream image...")
            generated_image = await self.openai_manager.generate_dream_image(
                dream_description=dream_description, 
                style="realistic"
            )
            logger.info(f"Image generated successfully. Prompt used: {generated_image.prompt_used[:100]}...")
            
            # Step 2: Analyze the dream WITH the context of the generated image
            # This will explain how the visual elements in the image represent the dream symbols
            logger.info("Step 2: Analyzing dream with generated image context...")
            analysis = await self.openai_manager.analyze_dream_with_image(
                dream_description=dream_description, 
                image_prompt=generated_image.prompt_used
            )
            logger.info("Dream analysis with image context completed successfully")
            
            processing_time = time.time() - start_time
            logger.info(f"Complete interpretation finished in {processing_time:.2f} seconds")
            
            return CompleteDreamResponse(
                analysis=analysis,
                generated_image=generated_image,
                processing_time=processing_time
            )
            
        except Exception as e:
            error_msg = f"Complete dream interpretation failed: {str(e)}"
            logger.error(error_msg)
            logger.exception("Full traceback:")
            raise Exception(error_msg)