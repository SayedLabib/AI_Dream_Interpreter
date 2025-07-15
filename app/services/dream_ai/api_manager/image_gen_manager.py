import openai
import asyncio
import time
from typing import Optional, Dict, Any
from app.core.config import settings
from app.services.dream_ai.image_gen_service.image_gen_schema import (
    DreamAnalysisResponse,
    ImageGenerationResponse     
)

class OpenAIManager:
    def __init__(self):
        # Validate API key
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        if not settings.openai_api_key.startswith('sk-'):
            raise ValueError("Invalid OpenAI API key format")
        
        openai.api_key = settings.openai_api_key
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
        
        # Model configurations
        self.chat_model = "gpt-3.5-turbo"
        self.image_model = "dall-e-3"
        self.max_tokens = 1500
        self.temperature = 0.7
    
    def get_model_info(self) -> Dict[str, str]:
        """Get information about the models being used"""
        return {
            "chat_model": self.chat_model,
            "image_model": self.image_model,
            "description": f"Using {self.chat_model} for dream analysis and {self.image_model} for image generation"
        }
    
    async def analyze_dream(self, dream_description: str, user_name: Optional[str] = None) -> DreamAnalysisResponse:
        """
        Analyze a dream description using OpenAI's API.
        """
        prompt = f"""
        As an expert dream analyst, please analyze this dream and provide insights.

        Dream Description: "{dream_description}"
        {f"Dreamer's Name: {user_name}" if user_name else ""}

        Please provide a comprehensive analysis in the following format:

        INTERPRETATION:
        [Provide the overall meaning and significance of the dream]

        SYMBOLISM:
        [Explain the key symbols and metaphors present in the dream]

        EMOTIONS:
        [Discuss the emotional themes and psychological insights]

        SUGGESTIONS:
        [Offer practical guidance and recommendations based on the dream]

        Keep each section focused and meaningful, providing personal insights that help the dreamer understand their subconscious mind.
        """

        try:
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.chat_model,
                messages=[
                    {"role": "system", "content": "You are a compassionate and insightful dream analyst with expertise in psychology, symbolism, and human consciousness. Provide thoughtful, personalized interpretations that help people understand their subconscious mind."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            full_response = response.choices[0].message.content

            # Parse the response into structured format
            sections = self._parse_dream_analysis(full_response)

            return DreamAnalysisResponse(
                interpretation=sections.get("interpretation", full_response[:200] + "..."),
                symbolism=sections.get("symbolism", "Various symbols in your dream carry personal significance."),
                emotions=sections.get("emotions", "Your dream reflects your current emotional state."),
                suggestions=sections.get("suggestions", "Consider reflecting on the themes that emerged.")
            )
        except Exception as e:
            raise Exception(f"Error analyzing dream with {self.chat_model}: {str(e)}")

    def _parse_dream_analysis(self, response: str) -> Dict[str, str]:
        """
        Parse the dream analysis response into structured sections.
        """
        sections = {
            "interpretation": "",
            "symbolism": "",
            "emotions": "",
            "suggestions": ""
        }

        # Split by section headers
        lines = response.split("\n")
        current_section = "interpretation"

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check for section headers
            if line.upper().startswith("INTERPRETATION"):
                current_section = "interpretation"
                continue
            elif line.upper().startswith("SYMBOLISM"):
                current_section = "symbolism"
                continue
            elif line.upper().startswith("EMOTIONS"):
                current_section = "emotions"
                continue
            elif line.upper().startswith("SUGGESTIONS"):
                current_section = "suggestions"
                continue
            elif "symbol" in line.lower() or "metaphor" in line.lower():
                current_section = "symbolism"
            elif "emotion" in line.lower() or "feeling" in line.lower():
                current_section = "emotions"
            elif "suggest" in line.lower() or "recommend" in line.lower() or "guidance" in line.lower():
                current_section = "suggestions"
            
            # Skip empty lines and section headers
            if line.startswith("[") and line.endswith("]"):
                continue
                
            sections[current_section] += line + " "
        
        # Clean up sections and provide defaults
        for key in sections:
            sections[key] = sections[key].strip()
            if not sections[key]:
                if key == "interpretation":
                    sections[key] = response[:200] + "..." if len(response) > 200 else response
                elif key == "symbolism":
                    sections[key] = "Your dream contains meaningful symbols that reflect your subconscious thoughts."
                elif key == "emotions":
                    sections[key] = "This dream appears to reflect your current emotional state and inner feelings."
                elif key == "suggestions":
                    sections[key] = "Consider reflecting on the themes and emotions that emerged in this dream."

        return sections

    async def generate_dream_image(self, dream_description: str, style: str = "realistic") -> ImageGenerationResponse:
        """Generate an image based on the dream description using DALL-E 3"""
        
        # Create an optimized prompt for DALL-E
        image_prompt = self._create_image_prompt(dream_description, style)
        
        try:
            response = await asyncio.to_thread(
                self.client.images.generate,
                model=self.image_model,
                prompt=image_prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            image_url = response.data[0].url
            
            return ImageGenerationResponse(
                image_url=image_url,
                prompt_used=image_prompt
            )
            
        except Exception as e:
            raise Exception(f"Error generating image with {self.image_model}: {str(e)}")
    
    def _create_image_prompt(self, dream_description: str, style: str) -> str:
        """Create an optimized prompt for DALL-E based on the dream description"""
        
        style_prompts = {
            "realistic": "photorealistic, detailed, cinematic lighting",
            "artistic": "artistic interpretation, painterly style, expressive",
            "surreal": "surreal, dreamlike, fantastical, Salvador Dali inspired",
            "minimalist": "minimalist, clean, simple composition",
            "dark": "dark atmosphere, moody, mysterious lighting"
        }
        
        style_modifier = style_prompts.get(style, style_prompts["realistic"])
        
        # Create a prompt that captures the essence of the dream
        prompt = f"""
        A dream scene depicting: {dream_description}
        
        Style: {style_modifier}
        
        The image should capture the emotional essence and symbolic elements of the dream,
        creating a visual representation that feels both mysterious and meaningful.
        High quality, detailed composition.
        """
        
        return prompt.strip()        