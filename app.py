import os
import json
import logging
import threading
import subprocess
from flask import Flask, render_template, request, jsonify
from config import NICHES

app = Flask(__name__)
SETTINGS_FILE = "settings.json"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

@app.route("/")
def index():
    settings = load_settings()
    # Default accounts if missing
    if "accounts" not in settings:
        settings["accounts"] = {"Primary": "token.json"}
        settings["active_account"] = "Primary"
        save_settings(settings)
        
    return render_template("index.html", settings=settings, all_niches=NICHES)

@app.route("/api/switch_account", methods=["POST"])
def switch_account():
    account_name = request.json.get("account")
    settings = load_settings()
    if account_name in settings.get("accounts", {}):
        settings["active_account"] = account_name
        save_settings(settings)
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Account not found"}), 404

@app.route("/api/settings", methods=["GET"])
def get_settings():
    return jsonify(load_settings())

@app.route("/api/settings", methods=["POST"])
def update_settings():
    new_settings = request.json
    current_settings = load_settings()
    current_settings.update(new_settings)
    save_settings(current_settings)
    return jsonify({"status": "success"})

@app.route("/api/run", methods=["POST"])
def trigger_pipeline():
    def run_job():
        settings = load_settings()
        settings["status"] = "Running..."
        save_settings(settings)
        
        try:
            # Trigger the main pipeline script
            subprocess.run(["python", "main_pipeline.py"], check=True)
            logger.info("Pipeline execution complete.")
        except Exception as e:
            logger.error(f"Background pipeline failed: {e}")
            settings = load_settings()
            settings["status"] = "Error"
            save_settings(settings)

    thread = threading.Thread(target=run_job)
    thread.start()
    return jsonify({"status": "started"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
