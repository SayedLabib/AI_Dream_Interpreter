from pydantic import BaseModel, Field
from typing import Optional, List

class DreamAnalysisRequest(BaseModel):
    dream_description: str = Field(..., description="User's dream description")

class DreamAnalysisResponse(BaseModel):
    interpretation: str = Field(..., description="AI Interpretation of the dream including symbolism analysis")
    emotions: str = Field(..., description="Emotions associated with the dream")   
    suggestions: str = Field(..., description="Suggestions based on the dream analysis formatted as numbered or bulleted points") 

class ImageGenerationRequest(BaseModel):
    dream_description: str = Field(..., description="User's dream description")

class ImageGenerationResponse(BaseModel):
    image_url: str = Field(..., description="URL of the generated dream image")
    prompt_used: str = Field(..., description="Prompt used for image generation")

class CompleteDreamRequest(BaseModel):
    dream_description: str = Field(..., description="User's dream description")

class CompleteDreamResponse(BaseModel):
    analysis: DreamAnalysisResponse
    generated_image: ImageGenerationResponse
    processing_time: float = Field(..., description="Time taken to process the request in seconds")