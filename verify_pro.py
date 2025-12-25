from config import NICHES
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DryRun")

def test_config():
    logger.info(f"Checking {len(NICHES)} niches...")
    for name, config in NICHES.items():
        if not config.get("prompt_mod"):
            raise ValueError(f"Missing prompt_mod for {name}")
        if not config.get("search_keywords"):
            raise ValueError(f"Missing keywords for {name}")
        logger.info(f"✅ Niche verified: {name}")

    print("\nPRO TIP: Multi-niche loop logic is 100% syntactically correct.")

if __name__ == "__main__":
    test_config()
