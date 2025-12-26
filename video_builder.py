import os
import requests
import logging
import gc
import asyncio
import edge_tts
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip, afx
from moviepy.video.fx import FadeIn, FadeOut, Resize

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

    async def generate_voiceover(self, text, output_path):
        """Generates TTS audio using Edge TTS."""
        voice = "en-US-ChristopherNeural"  # Deep, engaging male voice
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        return output_path

    def download_pexels_video(self, query):
        if not PEXELS_API_KEY:
            logger.error("Pexels API Key missing!")
            return None

        headers = {"Authorization": PEXELS_API_KEY}
        # Request portrait videos specifically
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=1&orientation=portrait"
        
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            if data['videos']:
                # Get the highest quality video file available
                video_files = data['videos'][0]['video_files']
                # Sort by resolution (width * height) descending
                video_files.sort(key=lambda x: x['width'] * x['height'], reverse=True)
                
                video_url = video_files[0]['link']
                filename = os.path.join(self.temp_dir, f"{query.replace(' ', '_')}.mp4")
                
                if not os.path.exists(filename):
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
        
        # Audio Setup
        bg_music = None
        music_path = os.path.join("assets", "music", "background.mp3")
        if os.path.exists(music_path):
             try:
                 bg_music = AudioFileClip(music_path)
                 # Lower volume heavily so voiceover pops
                 bg_music = bg_music.with_volume_scaled(0.12)
             except Exception as e:
                 logger.error(f"Failed to load background music: {e}")
        
        scene_idx = 0
        for scene in script_data['scenes']:
            scene_idx += 1
            # Combine niche keywords with scene keywords for better search
            search_query = f"{scene['keywords']}"
            if niche_keywords:
                search_query += f", {niche_keywords[0]}"
                
            video_path = self.download_pexels_video(search_query)
            
            # --- VOICE GENERATION ---
            narration_text = scene.get('narration', scene.get('text')) # Fallback
            voice_path = os.path.join(self.temp_dir, f"voice_{scene_idx}.mp3")
            
            try:
                # Run async TTS generation
                asyncio.run(self.generate_voiceover(narration_text, voice_path))
                voice_clip = AudioFileClip(voice_path)
                scene_duration = voice_clip.duration
            except Exception as e:
                logger.error(f"TTS failed: {e}")
                scene_duration = 5 # Fallback duration
                voice_clip = None

            if video_path:
                try:
                    clip = VideoFileClip(video_path)
                    
                    # --- RESIZING LOGIC ---
                    target_w, target_h = 1080, 1920
                    # Initial resize to cover dimensions
                    if clip.w / clip.h > target_w / target_h:
                         clip = clip.resized(height=target_h)
                    else:
                         clip = clip.resized(width=target_w)
                    
                    # Center crop
                    clip = clip.cropped(width=target_w, height=target_h, x_center=int(clip.w/2), y_center=int(clip.h/2))
                    
                    # --- LOOP VIDEO IF TOO SHORT ---
                    if clip.duration < scene_duration:
                        # Loop the video to match audio length
                        loop_count = int(scene_duration / clip.duration) + 1
                        clip = concatenate_videoclips([clip] * loop_count)
                    
                    # Trim to exact audio length
                    clip = clip.subclipped(0, scene_duration)
                    
                    # Attach voiceover
                    if voice_clip:
                        clip = clip.with_audio(voice_clip)

                    # --- PRO VISUALS: TEXT OVERLAY ---
                    # Style: "Hormozi" - Yellow text, black outline, bottom center
                    txt_clip = TextClip(
                        text=scene['text'].upper(), 
                        font_size=90,
                        color='#FFD700', # Gold/Yellow
                        stroke_color='black',
                        stroke_width=4,
                        font='arial.ttf', 
                        method='caption',
                        size=(int(target_w * 0.8), None), # 80% width constraint
                        interline=10
                    ).with_position(('center', 0.75), relative=True).with_duration(scene_duration) # Positioned lower down
                    
                    # Add subtle pop-in animation to text? (Simple fade for now)
                    
                    final_scene = CompositeVideoClip([clip, txt_clip])
                    clips.append(final_scene)
                    
                except Exception as e:
                    logger.error(f"Scene processing failed: {e}")
                    continue

        if not clips:
            logger.error("No clips were generated.")
            return None

        final_video = concatenate_videoclips(clips, method="compose")
        
        # --- AUDIO MIXING ---
        if bg_music:
            try:
                # Loop background music
                bg_music_looped = afx.audio_loop(bg_music, duration=final_video.duration)
                
                # Composite Audio: Voice is already in 'final_video', so we add bg music
                # IMPORTANT: CompositeAudioClip combines list of audios
                from moviepy import CompositeAudioClip
                final_audio = CompositeAudioClip([final_video.audio, bg_music_looped])
                final_video = final_video.with_audio(final_audio)
                
            except Exception as e:
                logger.error(f"Audio mixing failed: {e}")
            
        output_path = "final_short.mp4"
        
        logger.info("Exporting VIRAL Video...")
        try:
            final_video.write_videofile(
                output_path, 
                codec="libx264", 
                audio_codec="aac", 
                fps=30,
                preset='medium',
                bitrate="6000k",
                threads=4
            )
        finally:
            # Cleanup
            final_video.close()
            for clip in clips:
                clip.close()
            # Clean temp files
             
        return output_path

if __name__ == "__main__":
    # Test Data
    test_script = {

        "scenes": [
            {
                "narration": "Listen, if you want to achieve your goals, you have to stay focused.",
                "text": "FOCUS ON GOALS", 
                "keywords": "mountain climbing"
            },
            {
                "narration": "Stop wasting time on things that don't matter. Grind now, shine later.",
                "text": "STOP WASTING TIME", 
                "keywords": "coding desk dark"
            }
        ]
    }
    builder = VideoBuilder()
    builder.build_short(test_script)
