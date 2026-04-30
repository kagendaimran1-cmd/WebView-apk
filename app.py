from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "APK Builder Backend Running"

@app.route('/build', methods=['POST'])
def build_apk():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    file_path = "app/src/main/java/com/example/webviewapk/MainActivity.java"

    try:
        with open(file_path, "r") as f:
            content = f.read()

        new_content = content.replace(
            'webView.loadUrl("https://backend-apk-builder.onrender.com");',
            f'webView.loadUrl("{url}");'
        )

        with open(file_path, "w") as f:
            f.write(new_content)

        os.system("git add .")
        os.system(f'git commit -m "Build APK for {url}"')
        os.system("git push")

        return jsonify({
            "message": "Build started!",
            "download": "https://github.com/kagendaimran1-cmd/WebView-apk/actions"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)