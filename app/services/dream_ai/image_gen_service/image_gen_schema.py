from pydantic import BaseModel, Field
from typing import Optional, List

class DreamAnalysisRequest(BaseModel):
    dream_description: str = Field(..., description="User's dream description")
    user_name: Optional[str] = Field(None, description="Optional user name for personalization")

class DreamAnalysisResponse(BaseModel):
    interpretation: str = Field(..., description="AI Interpretation of the dream")
    symbolism: str = Field(..., description="Symbolism analysis of the dream")
    emotions: str = Field(..., description="Emotions associated with the dream")   
    suggestions: str = Field(..., description="Suggestions based on the dream analysis") 

class ImageGenerationRequest(BaseModel):
    dream_description: str = Field(..., description="User's dream description")
    style: Optional[str] = Field("realistic", description="Image style preference")

class ImageGenerationResponse(BaseModel):
    image_url: str = Field(..., description="URL of the generated dream image")
    prompt_used: str = Field(..., description="Prompt used for image generation")

class CompleteDreamResponse(BaseModel):
    analysis: DreamAnalysisResponse
    generated_image: ImageGenerationResponse
    processing_time: float = Field(..., description="Time taken to process the request in seconds")