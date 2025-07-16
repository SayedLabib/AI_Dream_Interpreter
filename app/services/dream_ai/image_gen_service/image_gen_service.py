import time
import logging
from typing import Optional
from app.services.dream_ai.api_manager.image_gen_manager import OpenAIManager
from app.services.dream_ai.image_gen_service.image_gen_schema import (
    CompleteDreamRequest,
    CompleteDreamResponse
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
    
    async def complete_dream_interpretation(
        self, 
        dream_description: str
    ) -> CompleteDreamResponse:
        """
        Complete dream interpretation: Generate image first, then analyze with image context and categorize dream patterns.
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
            logger.info(f"Image generated successfully. Prompt used: {generated_image['prompt_used'][:100]}...")
            
            # Step 2: Generate comprehensive analysis with dream patterns
            logger.info("Step 2: Analyzing dream with image context and categorizing patterns...")
            analysis_result = await self.openai_manager.analyze_dream_complete(
                dream_description=dream_description, 
                image_prompt=generated_image['prompt_used']
            )
            logger.info("Complete dream analysis finished successfully")
            
            processing_time = time.time() - start_time
            logger.info(f"Complete interpretation finished in {processing_time:.2f} seconds")
            
            return CompleteDreamResponse(
                title=analysis_result['title'],
                content=analysis_result['content'],
                imageUrl=generated_image['image_url'],
                dreamPatterns=analysis_result['dreamPatterns']
            )
            
        except Exception as e:
            error_msg = f"Complete dream interpretation failed: {str(e)}"
            logger.error(error_msg)
            logger.exception("Full traceback:")
            raise Exception(error_msg)