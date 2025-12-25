import os
import json

def setup_heroku():
    # 1. PEXELS & GEMINI (to .env)
    with open(".env", "w") as f:
        f.write(f"GEMINI_API_KEY={os.getenv('GEMINI_API_KEY')}\n")
        f.write(f"PEXELS_API_KEY={os.getenv('PEXELS_API_KEY')}\n")

    # 2. token.json
    google_token = os.getenv("GOOGLE_TOKEN")
    if google_token:
        with open("token.json", "w") as f:
            f.write(google_token)

    # 3. client_secrets.json
    client_id = os.getenv("YOUTUBE_CLIENT_ID")
    client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")
    
    if client_id and client_secret:
        secrets = {
            "installed": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs"
            }
        }
        with open("client_secrets.json", "w") as f:
            json.dump(secrets, f)

if __name__ == "__main__":
    setup_heroku()
