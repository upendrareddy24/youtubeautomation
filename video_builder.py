import os
import requests
import logging
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
from dotenv import load_dotenv
from config import NICHES

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

class VideoBuilder:
    def __init__(self):
        self.temp_dir = "temp_assets"
        os.makedirs(self.temp_dir, exist_ok=True)

    def download_pexels_video(self, query):
        if not PEXELS_API_KEY:
            logger.error("Pexels API Key missing!")
            return None

        headers = {"Authorization": PEXELS_API_KEY}
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=1&orientation=portrait"
        
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            if data['videos']:
                video_url = data['videos'][0]['video_files'][0]['link']
                filename = os.path.join(self.temp_dir, f"{query.replace(' ', '_')}.mp4")
                
                logger.info(f"Downloading video for '{query}'...")
                v_res = requests.get(video_url)
                with open(filename, 'wb') as f:
                    f.write(v_res.content)
                return filename
        except Exception as e:
            logger.error(f"Pexels fetch failed for '{query}': {e}")
        return None

    def build_short(self, script_data, niche="General"):
        clips = []
        
        niche_keywords = NICHES.get(niche, {}).get("search_keywords", [])
        
        for scene in script_data['scenes']:
            # Combine niche keywords with scene keywords for better search
            search_query = f"{scene['keywords']}"
            if niche_keywords:
                search_query += f", {niche_keywords[0]}" # Add primary niche keyword
                
            video_path = self.download_pexels_video(search_query)
            if video_path:
                clip = VideoFileClip(video_path)
                duration = min(clip.duration, 5)
                clip = clip.subclipped(0, duration) 
                
                try:
                    # Add Text Overlay
                    txt_clip = TextClip(
                        text=scene['text'], 
                        font_size=50, 
                        color='white', 
                        font='arial.ttf', 
                        method='caption',
                        size=(clip.w * 0.8, None)
                    ).with_position('center').with_duration(5)
                    
                    # Combine video and text
                    final_scene = CompositeVideoClip([clip, txt_clip])
                except Exception as e:
                    logger.warning(f"Text overlay failed (likely missing ImageMagick): {e}. Using raw video.")
                    final_scene = clip
                
                clips.append(final_scene)

        if not clips:
            logger.error("No clips were generated.")
            return None

        final_video = concatenate_videoclips(clips, method="compose")
        output_path = "final_short.mp4"
        
        logger.info("Exporting final video...")
        final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=24)
        return output_path

if __name__ == "__main__":
    # Test Data
    test_script = {
        "scenes": [
            {"text": "Focus on the Goal", "keywords": "mountain climbing"},
            {"text": "Work Hard", "keywords": "coding desk"}
        ]
    }
    builder = VideoBuilder()
    builder.build_short(test_script)
