from flask import Flask, request, jsonify
import os
import uuid

app = Flask(__name__)

@app.route('/')
def home():
    return "APK Builder Backend Running"

@app.route('/build', methods=['POST'])
def build_apk():
    data = request.json

    url = data.get('url')
    app_name = data.get('name', 'MyApp')

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # 🔥 Unique ID for each app
    app_id = str(uuid.uuid4())[:8]

    java_file = "app/src/main/java/com/example/webviewapk/MainActivity.java"

    with open(java_file, "r") as f:
        content = f.read()

    # Replace URL
    content = content.replace(
        'webView.loadUrl("https://example.com");',
        f'webView.loadUrl("{url}");'
    )

    # Replace app name (optional if added in strings.xml)
    content = content.replace("MyApp", app_name)

    with open(java_file, "w") as f:
        f.write(content)

    # Save app info (optional tracking)
    with open("apps.json", "a") as f:
        f.write(f"{app_id} - {app_name} - {url}\n")

    # Commit & push → triggers build
    os.system("git add .")
    os.system(f'git commit -m "Build {app_name} ({app_id})"')
    os.system("git push")

    # 🔥 Unique download link
    download_link = f"https://github.com/kagendaimran1-cmd/WebView-apk/releases/download/latest/app-debug.apk"

    return jsonify({
        "message": "Your APK is being built...",
        "app_id": app_id,
        "download": download_link
    })

if __name__ == '__main__':
    app.run()