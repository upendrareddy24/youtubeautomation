# 🚀 Pro YouTube Shorts Automator (10-Niche Edition)

A professional-grade, fully autonomous system that generates and uploads 10 viral YouTube Shorts daily across 10 high-potential niches.

## ✨ Features
- **10 Proven Niches**: Pre-configured for AI, Stoicism, Finance, Science, and more.
- **Smart Scripting**: Uses Gemini 1.5 Flash with niche-aware prompt modifiers.
- **Vertical Visuals**: Automated vertical footage from Pexels.
- **Bulk Orchestration**: Processes 10 videos in one loop with anti-spam delays.
- **Fully Automated**: Scheduled via GitHub Actions (10 AM UTC daily).

## 🛠️ Architecture
- `config.py`: The "Brain" containing niche definitions and keywords.
- `main_pipeline.py`: The Orchestrator that runs the multi-niche loop.
- `content_gen.py`: Script generation logic.
- `video_builder.py`: Video stitching and font rendering.
- `uploader.py`: YouTube API integration.

## 🚀 Getting Started

### 1. Local Setup
1. Install requirements: `pip install -r requirements.txt`
2. Set up your `.env` with `GEMINI_API_KEY` and `PEXELS_API_KEY`.
3. Run `python setup_auth.py` once to create your `token.json`.

### 2. Run Daily Loop
```bash
python main_pipeline.py
```

## ☁️ Deployment (GitHub / Heroku)
1. **GitHub**: Add your API keys and the content of `token.json` as GitHub Secrets.
2. **Heroku**: The project includes a `Procfile`. Simply push to Heroku and use the Heroku Scheduler to run `python main_pipeline.py` daily.

## 📈 Included Niches
- AI Productivity
- Stoic Wisdom
- Financial Intelligence
- Mind-Blowing Science
- Psychology Secrets
- Luxury Lifestyle
- Hidden Travel Gems
- Healthy Longevity
- Historical Mysteries
- Productivity Hacks
