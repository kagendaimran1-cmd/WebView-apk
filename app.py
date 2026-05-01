from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid

app = Flask(__name__)
CORS(app)  # 🔥 THIS FIXES YOUR ERROR

@app.route('/')
def home():
    return "APK Builder Backend Running"

@app.route('/build', methods=['POST'])
def build_apk():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data received"}), 400

        url = data.get('url')
        app_name = data.get('name', 'MyApp')

        if not url:
            return jsonify({"error": "No URL provided"}), 400

        app_id = str(uuid.uuid4())[:8]

        java_file = "app/src/main/java/com/example/webviewapk/MainActivity.java"

        with open(java_file, "r") as f:
            content = f.read()

        content = content.replace(
            'webView.loadUrl("https://example.com");',
            f'webView.loadUrl("{url}");'
        )

        content = content.replace("MyApp", app_name)

        with open(java_file, "w") as f:
            f.write(content)

        with open("apps.json", "a") as f:
            f.write(f"{app_id} - {app_name} - {url}\n")

        # Trigger GitHub Actions
        os.system("git add .")
        os.system(f'git commit -m "Build {app_name} ({app_id})"')
        os.system("git push")

        download_link = "https://github.com/kagendaimran1-cmd/WebView-apk/releases/download/latest/app-debug.apk"

        return jsonify({
            "message": "Your APK is being built...",
            "app_id": app_id,
            "download": download_link
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run()