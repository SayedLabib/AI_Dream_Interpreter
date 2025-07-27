import openai
import asyncio
import json
import re
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
        self.chat_model = "gpt-4o-mini"  # Better for JSON formatting than gpt-3.5-turbo
        self.image_model = "dall-e-3"
        self.max_tokens = 2000
        self.temperature = 0.3  # Lower temperature for more consistent JSON output
        
        # Define common system message to avoid duplication
        self.system_message = "You are Dr. Elena Nightingale, a warm and deeply compassionate dream analyst with 20+ years of experience in Jungian psychology, depth psychology, and symbolic interpretation. You genuinely care about each person who shares their dreams with you, understanding that dreams can sometimes be frightening, confusing, or emotionally overwhelming. Your heart goes out to anyone experiencing difficult dreams, and you always respond with genuine empathy and concern. You have helped thousands of people understand their subconscious minds through dream analysis, always treating each dream as sacred and meaningful. When someone shares a troubling dream, you acknowledge their feelings with phrases like 'I can understand how unsettling this must have been for you' or 'It's completely natural to feel concerned about such vivid imagery.' You validate their emotions while gently guiding them toward healing and understanding. Your approach combines scientific psychological principles with deep human compassion and intuitive symbolic understanding. You never minimize someone's experience, always seek the deeper meaning with love and care, and present even the most difficult themes as opportunities for growth, healing, and self-understanding. Your responses feel like receiving comfort and wisdom from a caring mentor who truly understands the complexity of the human psyche."
    
    def get_model_info(self) -> Dict[str, str]:
        """Get information about the models being used"""
        return {
            "chat_model": self.chat_model,
            "image_model": self.image_model,
            "description": f"Using {self.chat_model} for dream analysis and {self.image_model} for image generation"
        }

    def _extract_json_from_response(self, text: str) -> Optional[Dict]:
        """Extract JSON from response text with multiple fallback strategies"""
        # Strategy 1: Try to find JSON block between ```json and ```
        json_block_match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_block_match:
            try:
                return json.loads(json_block_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Strategy 2: Find the largest JSON object in the text
        json_matches = list(re.finditer(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL))
        for match in sorted(json_matches, key=lambda m: len(m.group(0)), reverse=True):
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                continue
        
        # Strategy 3: Try to parse the entire text as JSON
        try:
            return json.loads(text.strip())
        except json.JSONDecodeError:
            pass
        
        return None

    def _calculate_pattern_scores(self, dream_text: str, analysis_text: str) -> DreamPattern:
        """Calculate dream pattern scores using keyword analysis and content scoring"""
        combined_text = f"{dream_text} {analysis_text}".lower()
        print(f"[Analyzing text]: {combined_text[:300]}...")
        
        # Generic keyword patterns - no bias toward specific dream types
        pattern_keywords = {
            'adventure': [
                'travel', 'traveling', 'journey', 'quest', 'explore', 'exploring', 'exploration', 
                'adventure', 'expedition', 'voyage', 'discover', 'discovery', 'movement', 'moving',
                'run', 'running', 'walk', 'walking', 'climb', 'climbing', 'drive', 'driving',
                'chase', 'chasing', 'escape', 'escaping', 'pursue', 'pursuing', 'search', 'searching'
            ],
            'nature': [
                'animal', 'animals', 'dog', 'cat', 'bird', 'fish', 'tree', 'trees', 'forest',
                'ocean', 'sea', 'river', 'lake', 'water', 'mountain', 'mountains', 'sky',
                'flower', 'flowers', 'grass', 'field', 'garden', 'park', 'beach', 'desert',
                'rain', 'snow', 'wind', 'storm', 'sun', 'moon', 'star', 'stars', 'nature',
                'outdoor', 'outside', 'landscape', 'weather', 'season', 'plant', 'plants'
            ],
            'homeFamily': [
                'home', 'house', 'room', 'bedroom', 'kitchen', 'living room', 'bathroom',
                'family', 'mother', 'father', 'mom', 'dad', 'parent', 'parents', 'child',
                'children', 'son', 'daughter', 'brother', 'sister', 'sibling', 'grandparent',
                'grandmother', 'grandfather', 'relative', 'childhood', 'domestic', 'household',
                'marriage', 'wedding', 'divorce', 'relationship', 'friendship', 'friend'
            ],
            'nightmare': [
                'fear', 'afraid', 'scared', 'terror', 'terrified', 'panic', 'anxiety', 'anxious',
                'nightmare', 'scary', 'frightening', 'frightened', 'horror', 'horrible',
                'monster', 'demon', 'ghost', 'evil', 'dark', 'darkness', 'shadow', 'danger',
                'dangerous', 'threat', 'threatening', 'attack', 'attacking', 'hurt', 'pain',
                'death', 'dying', 'dead', 'kill', 'killing', 'violence', 'violent', 'blood',
                'trapped', 'lost', 'falling', 'drowning', 'suffocating', 'helpless'
            ],
            'romantic': [
                'love', 'loving', 'romance', 'romantic', 'kiss', 'kissing', 'hug', 'hugging',
                'embrace', 'embracing', 'attraction', 'attractive', 'beautiful', 'handsome',
                'partner', 'boyfriend', 'girlfriend', 'husband', 'wife', 'lover', 'dating',
                'relationship', 'intimate', 'intimacy', 'passion', 'passionate', 'desire',
                'flirt', 'flirting', 'seduction', 'sexual', 'affection', 'affectionate',
                'wedding', 'marriage', 'engagement', 'couple'
            ],
            'fantasySurreal': [
                'magic', 'magical', 'spell', 'wizard', 'witch', 'fantasy', 'mythical',
                'dragon', 'unicorn', 'fairy', 'angel', 'demon', 'god', 'goddess',
                'fly', 'flying', 'float', 'floating', 'levitate', 'levitating',
                'transform', 'transformation', 'shapeshifting', 'metamorphosis',
                'impossible', 'surreal', 'bizarre', 'strange', 'weird', 'unusual',
                'dreamlike', 'unreal', 'supernatural', 'paranormal', 'psychic',
                'teleport', 'telepathy', 'time travel', 'parallel universe',
                'giant', 'tiny', 'shrink', 'grow', 'morph', 'change', 'mutate'
            ]
        }
        
        # Calculate raw scores based on keyword frequency and context weight
        raw_scores = {}
        total_words = len(combined_text.split())
        
        for category, keywords in pattern_keywords.items():
            score = 0
            matched_keywords = []
            
            for keyword in keywords:
                # Count exact word matches (not just substring matches)
                import re
                word_pattern = r'\b' + re.escape(keyword) + r'\b'
                matches = re.findall(word_pattern, combined_text)
                count = len(matches)
                
                if count > 0:
                    matched_keywords.append(f"{keyword}({count})")
                    # Weight keywords found in original dream higher than in analysis
                    dream_weight = 2.0 if re.search(word_pattern, dream_text.lower()) else 1.0
                    # Also consider keyword importance (longer keywords = more specific)
                    keyword_weight = len(keyword.split()) * 1.2
                    score += count * dream_weight * keyword_weight
            
            raw_scores[category] = score
            if matched_keywords:
                print(f"[{category}]: {matched_keywords} = {score:.1f}")
        
        print(f"[Raw scores]: {raw_scores}")
        
        # Normalize scores to percentages (0-100)
        total_score = sum(raw_scores.values())
        
        if total_score == 0:
            # If no keywords matched, return balanced low scores
            print("[No keywords matched - using balanced fallback]")
            return DreamPattern(
                adventure=15.0,
                nature=15.0,
                homeFamily=15.0,
                nightmare=15.0,
                romantic=15.0,
                fantasySurreal=25.0  # Dreams are inherently a bit surreal
            )
        
        # Convert to percentages
        normalized_scores = {}
        for category, score in raw_scores.items():
            percentage = (score / total_score) * 100
            normalized_scores[category] = round(percentage, 1)
        
        print(f"[Normalized scores]: {normalized_scores}")
        
        return DreamPattern(
            adventure=normalized_scores['adventure'],
            nature=normalized_scores['nature'],
            homeFamily=normalized_scores['homeFamily'],
            nightmare=normalized_scores['nightmare'],
            romantic=normalized_scores['romantic'],
            fantasySurreal=normalized_scores['fantasySurreal']
        )

    async def analyze_dream_complete(self, dream_description: str, image_prompt: str) -> Dict[str, Any]:
        """
        Complete dream analysis with title, content, and dream pattern categorization
        """
        
        # Step 1: Generate the analysis content first
        try:
            analysis_response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.chat_model,
                messages=[
                    {"role": "system", "content": self.system_message},
                    {"role": "user", "content": f"""
                    Please provide a comprehensive dream analysis for: {dream_description}
                    
                    Include:
                    1. A meaningful title (4-8 words)
                    2. Detailed interpretation using Jungian psychology (300-400 words)
                    3. Empathetic acknowledgment of emotions
                    4. Practical suggestions for working with the dream
                    
                    Format as: Title: [title here]
                    Analysis: [full analysis here]
                    """}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            analysis_text = analysis_response.choices[0].message.content.strip()
            print(f"[Analysis Response]: {analysis_text}")
            
            # Extract title and content
            title_match = re.search(r'Title:\s*(.+)', analysis_text)
            title = title_match.group(1).strip() if title_match else "Dream Analysis"
            
            analysis_match = re.search(r'Analysis:\s*(.+)', analysis_text, re.DOTALL)
            content = analysis_match.group(1).strip() if analysis_match else analysis_text
            
        except Exception as e:
            print(f"[Analysis Error]: {e}")
            title = "Dream Analysis"
            content = f"Analysis of your dream about {dream_description}. This dream contains meaningful symbols that reflect your subconscious mind and inner experiences."
        
        # Step 2: Calculate pattern scores using our own logic (don't rely on OpenAI for this)
        dream_pattern = self._calculate_pattern_scores(dream_description, content)
        print(f"[Calculated Patterns]: {dream_pattern}")
        
        # Step 3: Try to get better scores from OpenAI without examples
        try:
            pattern_response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.chat_model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a dream pattern analyzer. You must respond with ONLY a JSON object containing numerical scores 0-100 for dream patterns. No other text."
                    },
                    {
                        "role": "user",
                        "content": f"""Analyze this dream and score how much each pattern is present (0-100):

Dream: {dream_description}

Score these patterns based on the dream content:
- adventure: exploration, travel, journeys, quests, movement, discovery
- nature: animals, plants, weather, landscapes, water, natural elements
- homeFamily: houses, family members, childhood, domestic settings, relationships
- nightmare: fear, anxiety, chasing, falling, scary elements, terror
- romantic: love, intimate moments, passion, relationships, attraction  
- fantasySurreal: magic, flying, impossible scenarios, transformation, surreal elements

Respond with ONLY this JSON format:
{{
    "adventure": [score],
    "nature": [score], 
    "homeFamily": [score],
    "nightmare": [score],
    "romantic": [score],
    "fantasySurreal": [score]
}}"""
                    }
                ],
                max_tokens=200,
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            pattern_text = pattern_response.choices[0].message.content.strip()
            print(f"[Pattern Response]: {pattern_text}")
            
            # Try to parse the pattern scores
            pattern_json = self._extract_json_from_response(pattern_text)
            if pattern_json:
                def safe_float(value, default=0.0):
                    try:
                        return max(0.0, min(100.0, float(value)))  # Clamp between 0-100
                    except (ValueError, TypeError):
                        return default
                
                # Override our calculated patterns with OpenAI's scores if they seem valid
                ai_patterns = DreamPattern(
                    adventure=safe_float(pattern_json.get('adventure', 0)),
                    nature=safe_float(pattern_json.get('nature', 0)),
                    homeFamily=safe_float(pattern_json.get('homeFamily', 0)),
                    nightmare=safe_float(pattern_json.get('nightmare', 0)),
                    romantic=safe_float(pattern_json.get('romantic', 0)),
                    fantasySurreal=safe_float(pattern_json.get('fantasySurreal', 0))
                )
                
                # Check if AI patterns seem reasonable (not all zeros or the hardcoded example)
                total_score = (ai_patterns.adventure + ai_patterns.nature + ai_patterns.homeFamily + 
                              ai_patterns.nightmare + ai_patterns.romantic + ai_patterns.fantasySurreal)
                
                # Don't use if it's the exact hardcoded example or all zeros
                hardcoded_total = 25 + 40 + 10 + 5 + 0 + 60  # 140
                if total_score > 10 and abs(total_score - hardcoded_total) > 20:
                    dream_pattern = ai_patterns
                    print(f"[Using AI Patterns]: {ai_patterns}")
                else:
                    print(f"[AI patterns rejected, using calculated]: total={total_score}")
                    
        except Exception as e:
            print(f"[Pattern Analysis Error]: {e}")
            # Keep our calculated patterns
        
        return {
            'title': title,
            'content': content,
            'dreamPatterns': dream_pattern
        }

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