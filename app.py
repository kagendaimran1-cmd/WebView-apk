from flask import Flask, request, jsonify
import os
import uuid

app = Flask(__name__)

GITHUB_REPO = "https://github.com/kagendaimran1-cmd/WebView-apk"
RAW_APK_URL = "https://github.com/kagendaimran1-cmd/WebView-apk/releases/latest/download/app-debug.apk"

@app.route('/')
def home():
    return "APK Builder Running"

@app.route('/build', methods=['POST'])
def build_apk():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    build_id = str(uuid.uuid4())

    # Replace URL in Java file
    file_path = "app/src/main/java/com/example/webviewapk/MainActivity.java"

    with open(file_path, "r") as f:
        content = f.read()

    new_content = content.replace(
        'webView.loadUrl("https://example.com");',
        f'webView.loadUrl("{url}");'
    )

    with open(file_path, "w") as f:
        f.write(new_content)

    # Commit & push (triggers GitHub Action)
    os.system("git add .")
    os.system(f'git commit -m "Build APK for {url}"')
    os.system("git push")

    return jsonify({
        "message": "Build started",
        "download": RAW_APK_URL,
        "note": "Wait 1–2 minutes then download"
    })

if __name__ == '__main__':
    app.run()