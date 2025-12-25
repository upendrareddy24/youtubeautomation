import os
import json
import logging
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

class YouTubeUploader:
    def __init__(self, secrets_file="client_secrets.json", token_file="token.json"):
        self.secrets_file = secrets_file
        self.token_file = token_file
        self.creds = self.get_credentials()
        self.youtube = build("youtube", "v3", credentials=self.creds)

    def get_credentials(self):
        creds = None
        if os.path.exists(self.token_file):
            try:
                creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
            except Exception as e:
                logger.error(f"Failed to load {self.token_file}: {e}")
                logger.error("Your GOOGLE_TOKEN content is likely corrupted or empty.")
                # Don't return None, let it fall through or re-raise if strictly required.
                # If we continue, it will try to refresh active creds (which is None) or use secrets file.
                # But typically if token file exists but is bad, we should probably delete it or fail hard?
                # Failing hard is safer to alert user.
                raise ValueError(f"Corrupted {self.token_file}. Check your Heroku GOOGLE_TOKEN variable.")

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.secrets_file):
                    raise FileNotFoundError(f"Please provide {self.secrets_file} from Google Cloud Console.")
                flow = InstalledAppFlow.from_client_secrets_file(self.secrets_file, SCOPES)
                # For Heroku, we usually don't run local server, but this is for local setup
                creds = flow.run_local_server(port=0)
            
            with open(self.token_file, "w") as token:
                token.write(creds.to_json())
        return creds

    def upload_short(self, file_path, title, description):
        logger.info(f"Uploading {file_path} to YouTube...")
        
        body = {
            "snippet": {
                "title": title,
                "description": description + "\n#Shorts",
                "categoryId": "22", # People & Blogs
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False,
            }
        }

        media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
        request = self.youtube.videos().insert(part="snippet,status", body=body, media_body=media)
        
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                logger.info(f"Uploaded {int(status.progress() * 100)}%")
        
        logger.info(f"Upload Complete! Video ID: {response.get('id')}")
        return response.get('id')

if __name__ == "__main__":
    # This requires setup first
    pass
