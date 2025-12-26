import os
import json
import logging
from google import genai
from dotenv import load_dotenv
from config import NICHES

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class ContentGenerator:
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

    def generate_short_script(self, niche="Success Habits", sub_niche=None):
        if not self.client:
            logger.error("Gemini API key not found. Using dummy data.")
            return {
                "title": f"Top 3 {niche} Tips #Shorts",
                "description": f"Master your day with these {niche} secrets. #Shorts #Success",
                "scenes": [
                    {"text": "Wake up at 5 AM", "keywords": "morning sunrise laptop"},
                    {"text": "Read for 30 mins", "keywords": "library books peaceful"},
                    {"text": "Plan your day", "keywords": "journal writing focus"}
                ]
            }

        niche_config = NICHES.get(niche, {})
        prompt_mod = niche_config.get("prompt_mod", "")
        hashtags = niche_config.get("hashtags", "#Shorts")

        topic_focus = f"specifically regarding '{sub_niche}'" if sub_niche else ""

        prompt = f"""
        You are an elite YouTube Shorts strategist and creator with 30+ years of experience in viral content. 
        Your goal is to create a script that is GUARANTEED to go viral (1M+ views).
        
        Niche: '{niche}' {topic_focus}
        {prompt_mod}
        
        VIRAL FORMULA:
        1. **The Hook (0-3s)**: A controversial statement, a surprising fact, or a "Stop scrolling" command.
        2. **The Retention (3-45s)**: High-value, fast-paced information. No fluff. Constant dopamine hits. 
        3. **The CTAs**: Subtle cues to subscribe or like.
        
        Generate a script for a 30-50 second YouTube Short.
        
        Provide the result in STRICT JSON format:
        {{
            "title": "CLICKBAIT TITLE with {hashtags}",
            "description": "Viral SEO description with {hashtags}",
            "scenes": [
                {{
                    "narration": "The spoken words for the voiceover. Use colloquial, punchy language.",
                    "text": "Short visual hook (MAX 3-5 WORDS) - e.g. 'STOP DOING THIS'",
                    "keywords": "3 specific visual keywords for Pexels search"
                }},
                ... (create enough scenes for 30-50s)
            ]
        }}
        """
        
        try:
            response = self.client.models.generate_content(
                model="gemini-flash-latest",
                contents=prompt
            )
            # Find the JSON block in the response text
            text = response.text
            start = text.find('{')
            end = text.rfind('}') + 1
            return json.loads(text[start:end])
        except Exception as e:
            logger.error(f"Gemini generation failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None

if __name__ == "__main__":
    gen = ContentGenerator()
    script = gen.generate_short_script()
    print(json.dumps(script, indent=4))
