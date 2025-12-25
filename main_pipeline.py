import logging
import time
from content_gen import ContentGenerator
from video_builder import VideoBuilder
from uploader import YouTubeUploader
from config import NICHES, DELAY_BETWEEN_UPLOADS_SECONDS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_pipeline(niche):
    try:
        content_engine = ContentGenerator()
        video_engine = VideoBuilder()
        uploader = YouTubeUploader()

        logger.info(f"--- Starting Pipeline for Niche: {niche} ---")
        
        # Step 1: Content Meta
        script_data = content_engine.generate_short_script(niche)
        if not script_data:
            logger.error(f"Script generation failed for {niche}.")
            return False

        # Step 2: Build Video
        video_path = video_engine.build_short(script_data, niche=niche)
        if not video_path:
            logger.error(f"Video building failed for {niche}.")
            return False

        # Step 3: Upload
        uploader.upload_short(
            video_path, 
            script_data['title'], 
            script_data['description']
        )
        
        logger.info(f"--- Successfully Finished Niche: {niche} ---")
        return True

    except Exception as e:
        logger.error(f"Pipeline failed for {niche}: {e}")
        return False

if __name__ == "__main__":
    niche_list = list(NICHES.keys())
    logger.info(f"Starting Pro Automation for {len(niche_list)} niches.")
    
    for i, niche in enumerate(niche_list):
        success = run_pipeline(niche)
        
        # Delay between niches to avoid spam detection
        if i < len(niche_list) - 1:
            wait_time = DELAY_BETWEEN_UPLOADS_SECONDS
            logger.info(f"Waiting {wait_time} seconds before the next niche...")
            time.sleep(wait_time)
            
    logger.info("All daily automation tasks completed.")
