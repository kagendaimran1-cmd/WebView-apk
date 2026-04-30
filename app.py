from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "APK Builder Backend Running"

@app.route('/build', methods=['POST'])
def build_apk():
    url = request.json.get('url')

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # Path to your Android project
    file_path = "WebView-apk/app/src/main/java/com/example/webviewapk/MainActivity.java"

    # Replace URL inside Java file
    with open(file_path, "r") as f:
        content = f.read()

    new_content = content.replace(
        'webView.loadUrl("https://backend-apk-builder.onrender.com");',
        f'webView.loadUrl("{url}");'
    )

    with open(file_path, "w") as f:
        f.write(new_content)

    # Push to GitHub
    os.system("git add .")
    os.system(f'git commit -m "Build APK for {url}"')
    os.system("git push")

    return jsonify({"message": "Build started!"})

if __name__ == '__main__':
    app.run()