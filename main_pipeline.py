import os
import json
import logging
import time
import random
from content_gen import ContentGenerator
from video_builder import VideoBuilder
from uploader import YouTubeUploader
from config import NICHES, DELAY_BETWEEN_UPLOADS_SECONDS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_pipeline(niche, count=1, token_file="token.json", sub_niche=None):
    try:
        content_engine = ContentGenerator()
        video_engine = VideoBuilder()
        uploader = YouTubeUploader(token_file=token_file)

        logger.info(f"--- Starting Pipeline for Niche: {niche} (Sub: {sub_niche}, Count: {count}) ---")
        
        for i in range(count):
            logger.info(f"Generating video {i+1} of {count} for {niche}...")
            # Step 1: Content Meta
            script_data = content_engine.generate_short_script(niche, sub_niche=sub_niche)
            if not script_data:
                continue

            # Step 2: Build Video
            video_path = video_engine.build_short(script_data, niche=niche)
            if not video_path:
                continue

            # Step 3: Upload
            uploader.upload_short(
                video_path, 
                script_data['title'], 
                script_data['description']
            )
            
            # Brief pause between videos in same niche
            if i < count - 1:
                time.sleep(30)
        
        logger.info(f"--- Successfully Finished Niche: {niche} ---")
        return True

    except Exception as e:
        logger.error(f"Pipeline failed for {niche}: {e}")
        return False

def load_dashboard_settings():
    if os.path.exists("settings.json"):
        with open("settings.json", "r") as f:
            return json.load(f)
    return None

if __name__ == "__main__":
    settings = load_dashboard_settings()
    if not settings:
        niche_list = list(NICHES.keys())
        logger.warning("No settings.json found. Using default niches.")
        active_niches = {n: {"enabled": True, "daily_count": 1} for n in niche_list}
    else:
        active_niches = settings.get("niches", {})

    logger.info("Starting Pro Automation via Dashboard Settings.")
    
    active_account = settings.get("active_account", "Primary")
    token_file = settings.get("accounts", {}).get(active_account, "token.json")
    
    enabled_niches = [n for n, cfg in active_niches.items() if cfg.get("enabled")]
    
    for i, niche in enumerate(enabled_niches):
        count = active_niches[niche].get("daily_count", 1)
        sub_niche = active_niches[niche].get("selected_sub", None)
        
        if count <= 0: continue
        
        success = run_pipeline(niche, count=count, token_file=token_file, sub_niche=sub_niche)
        
        # Update last run in settings
        if settings:
            settings["last_run"] = time.strftime("%Y-%m-%d %H:%M:%S")
            settings["status"] = "Idle"
            with open("settings.json", "w") as f:
                json.dump(settings, f, indent=4)

        # Delay between niches to avoid spam detection
        if i < len(enabled_niches) - 1:
            # Random delay 20-40 minutes
            wait_time = random.randint(1200, 2400) 
            minutes = wait_time // 60
            logger.info(f"Waiting {minutes} minutes ({wait_time}s) before the next niche to mimic human behavior...")
            time.sleep(wait_time)
            
    logger.info("All daily automation tasks completed.")
