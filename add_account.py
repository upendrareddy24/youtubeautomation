import os
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
SECRETS_FILE = "client_secrets.json"

def add_account():
    account_name = input("Enter a name for this account (e.g., Secondary): ").strip()
    if not account_name:
        print("Invalid name.")
        return

    token_file = f"token_{account_name.lower()}.json"
    
    if not os.path.exists(SECRETS_FILE):
        print(f"Error: {SECRETS_FILE} not found.")
        return

    flow = InstalledAppFlow.from_client_secrets_file(SECRETS_FILE, SCOPES)
    creds = flow.run_local_server(port=0)

    with open(token_file, "w") as token:
        token.write(creds.to_json())

    print(f"\n✅ Successfully authenticated {account_name}!")
    print(f"📁 Token saved to: {token_file}")
    print(f"💡 Now you can switch to this account in the Dashboard.")

if __name__ == "__main__":
    add_account()
