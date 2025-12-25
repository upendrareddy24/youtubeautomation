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
        Act as a viral YouTube Shorts creator in the '{niche}' niche, {topic_focus}.
        {prompt_mod}
        Generate a script for a 30-60 second YouTube Short.
        
        Provide the result in JSON format:
        {{
            "title": "Viral title with {hashtags}",
            "description": "Engaging description with {hashtags}",
            "scenes": [
                {{
                    "text": "Short punchy text overlay (max 8 words)",
                    "keywords": "3 keywords for searching stock footage on Pexels"
                }},
                ... (3-5 scenes total)
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
