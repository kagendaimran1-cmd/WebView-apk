import json
import os
from flask import Flask, request

app = Flask(__name__)

DATA_FILE = "apps.json"

# -------------------------
# Data handling functions
# -------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# -------------------------
# Home Page (UI)
# -------------------------
@app.route('/')
def home():
    return '''
    <h2>URL to App Builder</h2>
    <form action="/create" method="post">
        <input name="url" placeholder="Enter website URL">
        <button type="submit">Create App</button>
    </form>
    <br>
    <a href="/apps">View Created Apps</a>
    '''

# -------------------------
# Create App Route
# -------------------------
@app.route('/create', methods=['POST'])
def create():
    url = request.form['url']

    data = load_data()
    app_id = len(data) + 1

    new_app = {
        "id": app_id,
        "url": url,
        "status": "pending"
    }

    data.append(new_app)
    save_data(data)

    return f"""
    <h3>App Saved!</h3>
    <p><b>ID:</b> {app_id}</p>
    <p><b>URL:</b> {url}</p>
    <a href="/apps">Go to Dashboard</a>
    """

# -------------------------
# Apps Dashboard
# -------------------------
@app.route('/apps')
def apps():
    data = load_data()

    html = "<h2>Created Apps</h2>"

    if not data:
        return "<h3>No apps created yet</h3>"

    for app_item in data:
        html += f"""
        <div style="padding:10px; border:1px solid #ccc; margin:10px;">
            <p><b>ID:</b> {app_item['id']}</p>
            <p><b>URL:</b> {app_item['url']}</p>
            <p><b>Status:</b> {app_item['status']}</p>
        </div>
        """

    return html

# -------------------------
# Run Server
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
@app.route('/generate/<int:app_id>')
def generate(app_id):
    data = load_data()

    # find app by ID
    app_data = None
    for a in data:
        if a["id"] == app_id:
            app_data = a
            break

    if not app_data:
        return "App not found"

    folder_name = f"app_{app_id}"
    os.makedirs(folder_name, exist_ok=True)

    # create simple Android WebView template (simulation)
    main_java = f"""
package com.example.app{app_id};

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;

public class MainActivity extends Activity {{
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);

        WebView webView = new WebView(this);
        webView.getSettings().setJavaScriptEnabled(true);
        webView.loadUrl("{app_data['url']}");

        setContentView(webView);
    }}
}}
"""

    with open(f"{folder_name}/MainActivity.java", "w") as f:
        f.write(main_java)

    app_data["status"] = "generated"
    save_data(data)

    return f"""
    <h3>App Generated!</h3>
    <p>App ID: {app_id}</p>
    <p>Folder: {folder_name}</p>
    <a href="/apps">Back to Dashboard</a>
    """