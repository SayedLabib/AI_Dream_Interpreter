import openai
import asyncio
from typing import Optional, Dict, Any
from app.core.config import settings
from app.services.dream_ai.image_gen_service.image_gen_schema import DreamPattern

class OpenAIManager:
    def __init__(self):
        # Validate API key
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        if not settings.openai_api_key.startswith('sk-'):
            raise ValueError("Invalid OpenAI API key format")
        
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
        
        # Model configurations
        self.chat_model = "gpt-3.5-turbo"
        self.image_model = "dall-e-3"
        self.max_tokens = 1500
        self.temperature = 0.7
        
        # Define common system message to avoid duplication
        self.system_message = "You are Dr. Elena Nightingale, a warm and deeply compassionate dream analyst with 20+ years of experience in Jungian psychology, depth psychology, and symbolic interpretation. You genuinely care about each person who shares their dreams with you, understanding that dreams can sometimes be frightening, confusing, or emotionally overwhelming. Your heart goes out to anyone experiencing difficult dreams, and you always respond with genuine empathy and concern. You have helped thousands of people understand their subconscious minds through dream analysis, always treating each dream as sacred and meaningful. When someone shares a troubling dream, you acknowledge their feelings with phrases like 'I can understand how unsettling this must have been for you' or 'It's completely natural to feel concerned about such vivid imagery.' You validate their emotions while gently guiding them toward healing and understanding. Your approach combines scientific psychological principles with deep human compassion and intuitive symbolic understanding. You never minimize someone's experience, always seek the deeper meaning with love and care, and present even the most difficult themes as opportunities for growth, healing, and self-understanding. Your responses feel like receiving comfort and wisdom from a caring mentor who truly understands the complexity of the human psyche."
    
    def get_model_info(self) -> Dict[str, str]:
        """Get information about the models being used"""
        return {
            "chat_model": self.chat_model,
            "image_model": self.image_model,
            "description": f"Using {self.chat_model} for dream analysis and {self.image_model} for image generation"
        }

    async def analyze_dream_complete(self, dream_description: str, image_prompt: str) -> Dict[str, Any]:
        """
        Complete dream analysis with title, content, and dream pattern categorization
        """
        prompt = f"""
        You are Dr. Elena Nightingale, an expert dream analyst. CRITICAL: Respond with VALID JSON ONLY using EXACT field names.
        
        Dream: {dream_description}
        Image: {image_prompt}
        
        YOU MUST use these EXACT field names in dreamPatterns - NO OTHER VARIATIONS ALLOWED:
        - "adventure" (NOT Adventure)
        - "nature" (NOT Nature) 
        - "homeFamily" (NOT Home & Family, NOT Home_Family)
        - "nightmare" (NOT Nightmare)
        - "romantic" (NOT Romantic)
        - "fantasySurreal" (NOT Fantasy & Surreal, NOT Fantasy_Surreal)
        
        Content requirements: Write a comprehensive dream analysis (300-400 words) as one flowing narrative that includes:
        - Detailed interpretation of dream symbols using Jungian psychology
        - Emotional acknowledgment with empathetic phrases like "I can understand how this dream may have felt"
        - Practical suggestions for working with the dream (journaling, meditation, reflection)
        
        Maintain Dr. Elena's warm, mentor-like voice throughout.
        
        Pattern scoring (0-100 based on actual dream content):
        - adventure: travel, exploration, journeys, movement, discovery
        - nature: animals, plants, weather, landscapes, water, natural elements
        - homeFamily: houses, family members, childhood, domestic settings, relationships
        - nightmare: fear, anxiety, chasing, falling, scary elements, terror
        - romantic: love, intimate moments, passion, relationships, attraction
        - fantasySurreal: magic, flying, impossible scenarios, transformation, surreal elements
        
        Respond with valid JSON in this exact format:
        {{
            "title": "Dream Title Here",
            "content": "Your complete analysis as one continuous string with natural paragraph breaks",
            "dreamPatterns": {{
                "adventure": 25,
                "nature": 40,
                "homeFamily": 10,
                "nightmare": 5,
                "romantic": 0,
                "fantasySurreal": 60
            }}
        }}
        
        RESPOND WITH VALID JSON ONLY - NO EXTRA TEXT!
        """

        try:
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.chat_model,
                messages=[
                    {"role": "system", "content": "You are Dr. Elena Nightingale, a warm and deeply compassionate dream analyst with 20+ years of experience in Jungian psychology and symbolic interpretation. You provide detailed, caring dream analysis that combines psychological insight with genuine empathy. You respond only with valid JSON in the exact format requested, ensuring your content is rich, detailed, and emotionally supportive."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Parse JSON response
            import json
            try:
                result = json.loads(response_text)
                
                # Clean up content field - ensure it's a string
                content = result.get('content', '')
                
                # Handle cases where AI returns content as an object instead of string
                if isinstance(content, dict):
                    # If content is a dictionary, try to extract text values
                    content_parts = []
                    for key, value in content.items():
                        if isinstance(value, str):
                            content_parts.append(value)
                    content = ' '.join(content_parts) if content_parts else "Dream analysis provided with symbolic interpretation, emotional acknowledgment, and practical guidance."
                elif not isinstance(content, str):
                    # If content is not a string or dict, convert to string
                    content = str(content) if content else "Dream analysis provided with symbolic interpretation, emotional acknowledgment, and practical guidance."
                
                # Create DreamPattern object with comprehensive field mapping
                pattern_data = result.get('dreamPatterns', {})
                
                # Helper function to safely extract and convert to float
                def safe_float(value, default=0.0):
                    try:
                        return float(value) if value is not None else default
                    except (ValueError, TypeError):
                        return default
                
                # Normalize field names - handle all possible variations
                def get_pattern_value(patterns, field_variations):
                    for variation in field_variations:
                        if variation in patterns and patterns[variation] is not None:
                            return safe_float(patterns[variation])
                    return 0.0
                
                dream_pattern = DreamPattern(
                    adventure=get_pattern_value(pattern_data, ['adventure', 'Adventure']),
                    nature=get_pattern_value(pattern_data, ['nature', 'Nature']),
                    homeFamily=get_pattern_value(pattern_data, ['homeFamily', 'Home & Family', 'Home_Family', 'familyHome']),
                    nightmare=get_pattern_value(pattern_data, ['nightmare', 'Nightmare']),
                    romantic=get_pattern_value(pattern_data, ['romantic', 'Romantic']),
                    fantasySurreal=get_pattern_value(pattern_data, ['fantasySurreal', 'Fantasy & Surreal', 'Fantasy_Surreal', 'surreal'])
                )
                
                return {
                    'title': result['title'],
                    'content': content,
                    'dreamPatterns': dream_pattern
                }
                
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return {
                    'title': "A Meaningful Dream Experience",
                    'content': response_text,
                    'dreamPatterns': DreamPattern(
                        adventure=20.0,
                        nature=20.0,
                        homeFamily=20.0,
                        nightmare=10.0,
                        romantic=15.0,
                        fantasySurreal=15.0
                    )
                }
                
        except Exception as e:
            raise Exception(f"Error analyzing dream completely with {self.chat_model}: {str(e)}")

    async def generate_dream_image(self, dream_description: str, style: str = "realistic") -> Dict[str, str]:
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
            
            return {
                "image_url": image_url,
                "prompt_used": image_prompt
            }
            
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