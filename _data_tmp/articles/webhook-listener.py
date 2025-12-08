from flask import Flask
import subprocess

app = Flask(__name__)


@app.route("/run/fetch-alerts", methods=["POST", "GET"])
def fetch_alerts():
    try:
        subprocess.run(["python3", "gmail-parser.py"], check=True)
        return "✅ Fetch Alerts ran successfully", 200
    except subprocess.CalledProcessError as e:
        return f"❌ Fetch Alerts failed: {e}", 500


@app.route("/run/sync-notion", methods=["POST", "GET"])
def sync_notion():
    try:
        subprocess.run(["node", "notion-editorial-sync.js"], check=True)
        return "✅ Sync to Notion ran successfully", 200
    except subprocess.CalledProcessError as e:
        return f"❌ Sync to Notion failed: {e}", 500


@app.route("/run/generate-blogs", methods=["POST", "GET"])
def generate_blogs():
    try:
        subprocess.run(["python3", "generate_md_posts.py"], check=True)
        return "✅ Blog generation ran successfully", 200
    except subprocess.CalledProcessError as e:
        return f"❌ Blog generation failed: {e}", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
