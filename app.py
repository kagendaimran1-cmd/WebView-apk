import json
import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

DATA_FILE = "apps.json"

# 🔧 CHANGE THESE
GITHUB_TOKEN = "zhshsbshjehddjdjdndjdjdjd"
REPO = "kagendaimran1-cmd/WebView-apk"

def load_data():
    if os.path.exists(DATA_FILE):
        return json.load(open(DATA_FILE))
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def trigger_github_build(url):
    api = f"https://api.github.com/repos/{REPO}/dispatches"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    payload = {
        "event_type": "build-apk",
        "client_payload": {
            "url": url
        }
    }

    r = requests.post(api, json=payload, headers=headers)
    return r.status_code

@app.route("/")
def home():
    return '''
    <h2>APK Builder SaaS</h2>
    <form method="post" action="/create">
        <input name="url" placeholder="Website URL" required>
        <input name="name" placeholder="App Name" required>
        <button type="submit">Generate APK</button>
    </form>
    '''

@app.route("/create", methods=["POST"])
def create():
    url = request.form["url"]
    name = request.form["name"]

    data = load_data()

    app_id = len(data) + 1

    entry = {
        "id": app_id,
        "url": url,
        "name": name,
        "status": "building"
    }

    data.append(entry)
    save_data(data)

    # 🔥 trigger GitHub Actions build
    trigger_github_build(url)

    return f"""
    <h3>App Created!</h3>
    <p>ID: {app_id}</p>
    <p>Status: Building APK...</p>
    <p>URL: {url}</p>
    """

@app.route("/apps")
def apps():
    return jsonify(load_data())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)