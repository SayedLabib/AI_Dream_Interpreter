from pydantic import BaseModel, Field
from typing import Optional, List

class DreamPattern(BaseModel):
    adventure: float = Field(..., description="Percentage of adventure elements in the dream (0-100)")
    nature: float = Field(..., description="Percentage of nature elements in the dream (0-100)")
    homeFamily: float = Field(..., description="Percentage of home & family elements in the dream (0-100)")
    nightmare: float = Field(..., description="Percentage of nightmare elements in the dream (0-100)")
    romantic: float = Field(..., description="Percentage of romantic elements in the dream (0-100)")
    fantasySurreal: float = Field(..., description="Percentage of fantasy & surreal elements in the dream (0-100)")

    class Config:
        populate_by_name = True

class CompleteDreamRequest(BaseModel):
    dream_description: str = Field(..., description="User's dream description")

class CompleteDreamResponse(BaseModel):
    title: str = Field(..., description="A descriptive title for the dream")
    content: str = Field(..., description="Complete dream analysis including interpretation, emotions, and suggestions")
    imageUrl: str = Field(..., description="URL of the generated dream image")
    dreamPatterns: DreamPattern = Field(..., description="Percentage breakdown of dream categories")