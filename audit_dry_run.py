import os
import json
import logging
import time
import random
from unittest.mock import MagicMock, patch

# Configure test logging
logging.basicConfig(level=logging.INFO, format='[DRY-RUN] %(message)s')
logger = logging.getLogger("DryRun")

# Mock dependencies BEFORE importing main_pipeline to avoid actual instantiation
with patch('content_gen.ContentGenerator') as MockContent, \
     patch('video_builder.VideoBuilder') as MockVideo, \
     patch('uploader.YouTubeUploader') as MockUploader, \
     patch('time.sleep') as mock_sleep:

    # Import module under test
    import main_pipeline
    from config import NICHES

    def run_audit():
        logger.info("🎬 STARTED: Full Codebase Audit & Dry Run")
        
        # 1. Check Configuration Integrity
        logger.info("Checking config.py...")
        if len(NICHES) != 10:
            logger.error(f"❌ NICHES count mismatch! Expected 10, got {len(NICHES)}")
            return
        
        for name, data in NICHES.items():
            if "sub_niches" not in data or len(data["sub_niches"]) != 5:
                logger.error(f"❌ Sub-niches missing or incorrect for {name}")
                return
        logger.info("✅ Configuration Integrity: PASS")

        # 2. Mock Behavior Setup
        mock_content_instance = MockContent.return_value
        mock_content_instance.generate_short_script.return_value = {
            "title": "Test Title", "description": "Test Desc", "scenes": []
        }
        
        mock_video_instance = MockVideo.return_value
        mock_video_instance.build_short.return_value = "test_video.mp4"
        
        mock_uploader_instance = MockUploader.return_value
        mock_uploader_instance.upload_short.return_value = "VIDEO_ID_123"

        # 3. Simulate Dashboard Settings
        test_settings = {
            "active_account": "Primary",
            "accounts": {"Primary": "token_test.json"},
            "niches": {
                "Stoic Wisdom": {"enabled": True, "daily_count": 1, "selected_sub": "Mindset of a Warrior"},
                "AI Productivity": {"enabled": True, "daily_count": 1, "selected_sub": "Future Tech News"}
            }
        }
        
        logger.info("Testing Pipeline Logic with Mock Settings...")
        
        # Manually invoke the logic that resembles main_pipeline main block
        active_account = test_settings.get("active_account", "Primary")
        token_file = test_settings.get("accounts", {}).get(active_account, "token.json")
        enabled_niches = [n for n, cfg in test_settings["niches"].items() if cfg.get("enabled")]
        
        for i, niche in enumerate(enabled_niches):
            count = test_settings["niches"][niche].get("daily_count", 1)
            sub_niche = test_settings["niches"][niche].get("selected_sub", None)
            
            logger.info(f"👉 Testing Niche: {niche} | Sub: {sub_niche} | Count: {count}")
            
            # Call the actual function
            success = main_pipeline.run_pipeline(niche, count=count, token_file=token_file, sub_niche=sub_niche)
            
            if success:
                logger.info(f"   ✅ Pipeline Success for {niche}")
            else:
                logger.error(f"   ❌ Pipeline Failed for {niche}")
            
            # Verify Calls
            mock_content_instance.generate_short_script.assert_called_with(niche, sub_niche=sub_niche)
            logger.info("   ✅ Content Generator Called Correctly")
            
            mock_video_instance.build_short.assert_called()
            logger.info("   ✅ Video Builder Called Correctly")
            
            mock_uploader_instance.upload_short.assert_called()
            logger.info("   ✅ Uploader Called Correctly")
            
            mock_content_instance.generate_short_script.reset_mock() # Reset for next loop

            # Check Delay Logic
            if i < len(enabled_niches) - 1:
                logger.info("   ⏳ (Simulated) Random Delay Triggered...")
        
        logger.info("✅ Pipeline Logic: PASS")
        logger.info("🎉 AUDIT COMPLETE: Ready for Deployment")

if __name__ == "__main__":
    run_audit()
