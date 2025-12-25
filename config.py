# Multi-Niche Configuration for Pro YouTube Automation

NICHES = {
    "AI Productivity": {
        "prompt_mod": "Focus on revolutionary AI tools, productivity hacks, and future tech. Use futuristic and energetic language.",
        "search_keywords": ["tech", "artificial intelligence", "coding", "future", "modern office"],
        "hashtags": "#AI #Productivity #TechHacks"
    },
    "Stoic Wisdom": {
        "prompt_mod": "Focus on ancient philosophy, mental resilience, and peace of mind. Use calm, profound, and wise language.",
        "search_keywords": ["statue", "nature mountain", "peaceful forest", "meditation"],
        "hashtags": "#Stoicism #Wisdom #Mindset"
    },
    "Financial Intelligence": {
        "prompt_mod": "Focus on wealth building, investment secrets, and financial freedom. Use authoritative and bold language.",
        "search_keywords": ["money", "bitcoin", "stock market", "luxury watch", "gold"],
        "hashtags": "#Wealth #Finance #MoneyTips"
    },
    "Mind-Blowing Science": {
        "prompt_mod": "Focus on space, physics, and natural wonders. Use awe-inspiring and educational language.",
        "search_keywords": ["galaxy", "planet", "microscope", "laboratory", "physics"],
        "hashtags": "#Science #Space #Wonders"
    },
    "Psychology Secrets": {
        "prompt_mod": "Focus on human behavior, dark psychology, and body language. Use mysterious and intriguing language.",
        "search_keywords": ["eye contact", "shadow", "people whispering", "thinking person"],
        "hashtags": "#Psychology #HumanBehavior #DarkPsychology"
    },
    "Luxury Lifestyle": {
        "prompt_mod": "Focus on high-end cars, mansions, and luxury living. Use aspirational and premium language.",
        "search_keywords": ["supercar", "private jet", "luxury villa", "yacht"],
        "hashtags": "#Luxury #BillionaireMindset #Aspiration"
    },
    "Hidden Travel Gems": {
        "prompt_mod": "Focus on exotic, lesser-known travel destinations. Use adventurous and visual language.",
        "search_keywords": ["tropical island", "hidden waterfall", "ancient ruins", "drone view"],
        "hashtags": "#TravelGems #Adventure #Wanderlust"
    },
    "Healthy Longevity": {
        "prompt_mod": "Focus on biohacking, superfoods, and longevity habits. Use health-conscious and scientific language.",
        "search_keywords": ["healthy food", "running", "vitamin", "cold plunge", "sleep"],
        "hashtags": "#Biohacking #Longevity #Health"
    },
    "Historical Mysteries": {
        "prompt_mod": "Focus on unsolved mysteries, strange events, and hidden history. Use suspenseful and storytelling language.",
        "search_keywords": ["ancient pyramid", "old parchment", "dark castle", "detective"],
        "hashtags": "#History #Mysteries #Unsolved"
    },
    "Productivity Hacks": {
        "prompt_mod": "Focus on time management, study tips, and work optimization. Use practical and direct language.",
        "search_keywords": ["calendar", "desk setup", "pomodoro", "notebook"],
        "hashtags": "#Productivity #Success #TimeManagement"
    }
}

# Pipeline Settings
DAILY_UPLOADS_PER_NICHE = 1
DELAY_BETWEEN_UPLOADS_SECONDS = 300 # 5 minutes to avoid spam filters
