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
    
    async def analyze_dream(self, dream_description: str) -> DreamAnalysisResponse:
        """
        Analyze a dream with allowance for symbolic interpretations of intense or disturbing imagery.
        """
        prompt = f"""
        You are an expert dream analyst with deep knowledge in Jungian psychology, symbolic interpretation, and subconscious mind analysis. 
        Your role is to provide compassionate, caring, and psychologically grounded interpretations of dreams with genuine warmth and understanding.
        
        TONE AND APPROACH:
        - Begin with acknowledgment of the dreamer's experience (e.g., "I can sense this dream felt quite vivid/unsettling/meaningful to you")
        - Show genuine care and concern for their emotional state
        - Use warm, validating language that makes them feel heard and understood
        - For disturbing dreams: "I understand this must have been quite unsettling" or "It's completely natural to feel concerned about such imagery"
        - For positive dreams: "What a beautiful and meaningful dream experience" or "This sounds like a wonderful gift from your subconscious"
        - For confusing dreams: "Dreams can often feel puzzling, but there's always deeper wisdom within them"
        
        GUIDELINES FOR ANALYSIS:
        - Approach each dream with empathy, warmth, and professional insight
        - Use symbolic and metaphorical language to explain dream elements with care
        - Draw connections between dream symbols and psychological states with understanding
        - Handle sensitive content (violence, fear, disturbing imagery) with extra compassion and sensitivity
        - Absolutely NO sexual content or interpretations under any circumstances
        - Focus on transformation, growth, and psychological healing themes with hopeful language
        - Provide practical wisdom that helps the dreamer feel supported and understood
        
        CONTENT HANDLING WITH CARE:
        - Disturbing imagery: "While this imagery may feel frightening, your subconscious is often working through important themes..."
        - Fear/anxiety elements: "These feelings in your dream, though uncomfortable, can guide us toward valuable insights..."
        - Dark themes: "Even in the darkest dreams, there are often seeds of healing and understanding..."
        - Violent imagery: "Such intense imagery can represent inner conflicts that your mind is working to resolve..."
        
        Dream to analyze: "{dream_description}"
        
        Provide your analysis in exactly this format, with 4-6 lines per section, using warm and caring language:
        
        INTERPRETATION:
        [Start with a caring acknowledgment, then provide a comprehensive symbolic interpretation that merges the dream's meaning with its symbolism. 
        Explain what the dream represents psychologically, what the key symbols mean, and how they connect 
        to the dreamer's subconscious mind. Be profound yet accessible, metaphorical yet clear, always with warmth and understanding.]
        
        EMOTIONS:
        [Begin with empathy for what they felt, then analyze the emotional landscape of the dream. What feelings does it evoke? What emotional states 
        or psychological conditions might it reflect? Connect the emotions to potential life circumstances 
        or inner psychological processes with compassionate understanding.]
        
        SUGGESTIONS:
        [Offer gentle, supportive guidance with 2-3 actionable, numbered points for personal growth and reflection:
         1. [Specific reflection or mindfulness practice based on the dream's themes, offered with care]
         2. [Practical action or behavioral insight the dreamer can apply, presented supportively]
         3. [Deeper psychological work or journaling prompt, if applicable, offered as gentle invitation]
        ]
        
        Maintain a warm, deeply caring tone throughout - like speaking with a wise, compassionate counselor who genuinely cares about the dreamer's wellbeing and growth.
        """



        try:
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.chat_model,
                messages=[
                    {"role": "system", "content": "You are Dr. Elena Nightingale, a warm and deeply compassionate dream analyst with 20+ years of experience in Jungian psychology, depth psychology, and symbolic interpretation. You genuinely care about each person who shares their dreams with you, understanding that dreams can sometimes be frightening, confusing, or emotionally overwhelming. Your heart goes out to anyone experiencing difficult dreams, and you always respond with genuine empathy and concern. You have helped thousands of people understand their subconscious minds through dream analysis, always treating each dream as sacred and meaningful. When someone shares a troubling dream, you acknowledge their feelings with phrases like 'I can understand how unsettling this must have been for you' or 'It's completely natural to feel concerned about such vivid imagery.' You validate their emotions while gently guiding them toward healing and understanding. Your approach combines scientific psychological principles with deep human compassion and intuitive symbolic understanding. You never minimize someone's experience, always seek the deeper meaning with love and care, and present even the most difficult themes as opportunities for growth, healing, and self-understanding. Your responses feel like receiving comfort and wisdom from a caring mentor who truly understands the complexity of the human psyche."},
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
                emotions=sections.get("emotions", "Your dream reflects your current emotional state."),
                suggestions=sections.get("suggestions", "Consider reflecting on the themes that emerged.")
            )
        except Exception as e:
            raise Exception(f"Error analyzing dream with {self.chat_model}: {str(e)}")

    async def analyze_dream_with_image(self, dream_description: str, image_prompt: str) -> DreamAnalysisResponse:
        """
        Analyze a dream with context of the generated image, explaining how the image represents the dream
        """
        prompt = f"""
        You are an expert dream analyst with deep knowledge in Jungian psychology, symbolic interpretation, and subconscious mind analysis. 
        Your role is to provide compassionate, caring, and psychologically grounded interpretations of dreams with genuine warmth and understanding.
        
        IMPORTANT: The user has had their dream visualized as an image. You must explain how the visual elements in the generated image represent and symbolize the psychological content of their dream.
        
        TONE AND APPROACH:
        - Begin with acknowledgment of the dreamer's experience
        - Show genuine care and concern for their emotional state
        - Use warm, validating language that makes them feel heard and understood
        - For disturbing dreams: "I understand this must have been quite unsettling"
        - For positive dreams: "What a beautiful and meaningful dream experience"
        - For confusing dreams: "Dreams can often feel puzzling, but there's always deeper wisdom within them"
        
        Original Dream: "{dream_description}"
        Generated Image Description: "{image_prompt}"
        
        Provide your analysis in exactly this format, with 4-6 lines per section, using warm and caring language:
        
        INTERPRETATION:
        [Start with a caring acknowledgment, then provide a comprehensive symbolic interpretation. Explain what the dream represents psychologically and what the key symbols mean. CRUCIALLY: Explain how the generated image visually represents these themes - describe which specific visual elements (landscapes, lighting, atmosphere, objects) in the image symbolize which aspects of the original dream. Connect the visual metaphors in the image to the psychological content of the dream.]
        
        EMOTIONS:
        [Begin with empathy for what they felt, then analyze the emotional landscape of the dream. What feelings does it evoke? What emotional states might it reflect? IMPORTANTLY: Explain how the visual elements in the generated image (colors, lighting, atmosphere, terrain) capture and represent these specific emotions from the dream.]
        
        SUGGESTIONS:
        [Offer gentle, supportive guidance with 2-3 actionable, numbered points for personal growth and reflection:
         1. [Specific reflection or mindfulness practice based on the dream's themes, offered with care]
         2. [Practical action or behavioral insight the dreamer can apply, presented supportively]
         3. [Deeper psychological work or journaling prompt, if applicable, offered as gentle invitation]
        ]
        
        Maintain a warm, deeply caring tone throughout - like speaking with a wise, compassionate counselor who genuinely cares about the dreamer's wellbeing and growth.
        """

        try:
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.chat_model,
                messages=[
                    {"role": "system", "content": "You are Dr. Elena Nightingale, a warm and deeply compassionate dream analyst with 20+ years of experience in Jungian psychology, depth psychology, and symbolic interpretation. You genuinely care about each person who shares their dreams with you, understanding that dreams can sometimes be frightening, confusing, or emotionally overwhelming. Your heart goes out to anyone experiencing difficult dreams, and you always respond with genuine empathy and concern. You have helped thousands of people understand their subconscious minds through dream analysis, always treating each dream as sacred and meaningful. When someone shares a troubling dream, you acknowledge their feelings with phrases like 'I can understand how unsettling this must have been for you' or 'It's completely natural to feel concerned about such vivid imagery.' You validate their emotions while gently guiding them toward healing and understanding. Your approach combines scientific psychological principles with deep human compassion and intuitive symbolic understanding. You never minimize someone's experience, always seek the deeper meaning with love and care, and present even the most difficult themes as opportunities for growth, healing, and self-understanding. Your responses feel like receiving comfort and wisdom from a caring mentor who truly understands the complexity of the human psyche."},
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
                emotions=sections.get("emotions", "Your dream reflects your current emotional state."),
                suggestions=sections.get("suggestions", "1. Reflect on the themes and emotions that emerged in this dream.\n2. Consider how these symbols relate to your current life situation.\n3. Take time for self-reflection and journaling about these insights.")
            )
        except Exception as e:
            raise Exception(f"Error analyzing dream with image context with {self.chat_model}: {str(e)}")

    def _parse_dream_analysis(self, response: str) -> Dict[str, str]:
        """
        Parse the dream analysis response into structured sections.
        """
        sections = {
            "interpretation": "",
            "emotions": "",
            "suggestions": ""
        }

        # Split by section headers and parse more carefully
        lines = response.split("\n")
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check for section headers (case insensitive)
            line_upper = line.upper()
            if line_upper.startswith("INTERPRETATION"):
                current_section = "interpretation"
                continue
            elif line_upper.startswith("EMOTIONS"):
                current_section = "emotions"
                continue
            elif line_upper.startswith("SUGGESTIONS"):
                current_section = "suggestions"
                continue
            elif line.startswith("[") and line.endswith("]"):
                # Skip instruction lines in brackets
                continue
            
            # Add content to current section
            if current_section and line:
                if sections[current_section]:
                    sections[current_section] += " "
                sections[current_section] += line
        
        # Clean up sections and provide defaults if needed
        for key in sections:
            sections[key] = sections[key].strip()
            if not sections[key]:
                if key == "interpretation":
                    # Use first part of response as fallback
                    sections[key] = response[:300] + "..." if len(response) > 300 else response
                elif key == "emotions":
                    sections[key] = "This dream appears to reflect your current emotional state and inner feelings."
                elif key == "suggestions":
                    sections[key] = "1. Reflect on the themes and emotions that emerged in this dream.\n2. Consider how these symbols relate to your current life situation.\n3. Take time for self-reflection and journaling about these insights."

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
        
        # Check for sensitive content and create appropriate prompt
        sensitive_keywords = [
            'blood', 'violence', 'violent', 'sexual', 'sex', 'nude', 'naked', 'explicit',
            'murder', 'kill', 'death', 'dead', 'gore', 'graphic', 'brutal', 'weapon',
            'gun', 'knife', 'attack', 'assault', 'vulgar', 'inappropriate', 'fight',
            'war', 'battle', 'wound', 'injury', 'hurt', 'pain', 'suffering', 'torture',
            'snake', 'baby', 'child', 'infant', 'toddler', 'kid', 'children', 'minor',
            'chase', 'chasing', 'pursue', 'pursuing', 'follow', 'following', 'hunt',
            'danger', 'threat', 'threatening', 'scary', 'frightening', 'terror', 'horror',
            'scream', 'screaming', 'cry', 'crying', 'fear', 'afraid', 'panic', 'escape',
            'bite', 'biting', 'predator', 'prey', 'monster', 'demon', 'evil', 'dark'
        ]
        
        has_sensitive_content = any(keyword in dream_description.lower() for keyword in sensitive_keywords)
        
        if has_sensitive_content:
            # Let the LLM create a safe metaphorical prompt
            return self._generate_safe_metaphorical_prompt(dream_description, style)
        else:
            # Create realistic prompt for non-sensitive content
            prompt = f"""
            A realistic dream scene depicting: {dream_description}
            
            Style: photorealistic, detailed, cinematic lighting
            
            The image should realistically capture the atmosphere, mood, and elements of the dream,
            creating a photorealistic visual representation that honestly reflects the dream's emotional tone.
            Maintain the original intensity and atmosphere of the dream whether positive, negative, or neutral.
            High quality, realistic composition.
            """
        
        return prompt.strip()
    
    def _generate_safe_metaphorical_prompt(self, dream_description: str, style_modifier: str) -> str:
        """Use LLM to generate a safe, realistic image prompt for sensitive content that stays true to the dream's intensity"""
        try:
            metaphor_prompt = f"""
            You are an expert at creating realistic image descriptions for DALL-E 3 that capture the true nature and intensity of dreams while staying within content policy limits.
            
            Original dream description: "{dream_description}"
            
            Your task is to create a REALISTIC image prompt that:
            1. Stays as TRUE to the original dream as possible
            2. Maintains the EMOTIONAL INTENSITY and ATMOSPHERE of the dream
            3. Uses realistic elements that DALL-E can generate without violating policies
            4. Does NOT make dark/serious dreams artificially beautiful or peaceful
            5. Preserves the psychological impact and mood of the original dream
            
            TRANSFORMATION GUIDELINES (maintain intensity):
            - Snake threatening someone → Winding dark path in a threatening landscape
            - Chase/pursuit → Person running through realistic challenging terrain  
            - Fear/terror → Dark, stormy, ominous realistic landscape
            - Danger → Realistic dangerous-looking environment (cliff, storm, dark forest)
            - Screaming → Wind howling through a dramatic, intense landscape
            - Violence → Realistic turbulent natural forces (powerful storm, rough seas)
            - Blood → Realistic red elements in nature (red rocks, red sunset, red flowers)
            - Death/ending → Realistic autumn/winter scenes, wilted landscapes
            
            IMPORTANT RULES:
            - Keep the DARK and SERIOUS tone if the dream is dark/serious
            - Use REALISTIC imagery, not artistic or beautiful interpretations
            - Maintain the original EMOTIONAL INTENSITY
            - Focus on ATMOSPHERE that matches the dream's mood
            - Use dramatic lighting and realistic environments
            - NO children, babies, or people in vulnerable situations
            - NO direct violence, weapons, or explicit content
            - Replace problematic elements with intense natural phenomena
            
            Style: photorealistic, detailed, cinematic lighting
            
            Create a realistic image description that honestly represents the dream's intensity and mood.
            Respond with ONLY the image prompt, nothing else. Keep it under 200 words.
            """
            
            import asyncio
            response = asyncio.run(asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.chat_model,
                messages=[
                    {"role": "system", "content": "You are an expert at creating realistic image descriptions that honor the true emotional intensity of dreams while staying within DALL-E 3's content policies. You never artificially beautify dark or serious dreams - you represent them realistically."},
                    {"role": "user", "content": metaphor_prompt}
                ],
                max_tokens=300,
                temperature=0.7
            ))
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            # Fallback that maintains intensity if possible
            return f"""
            A realistic, dramatic landscape reflecting inner emotional turmoil and intensity.
            Style: photorealistic, detailed, cinematic lighting.
            Dark, moody atmosphere with stormy skies, rough terrain, and dramatic lighting that conveys emotional weight and psychological tension.
            Realistic environmental elements that reflect the serious nature of inner psychological processes.
            """        