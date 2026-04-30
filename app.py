@app.route('/build', methods=['POST'])
def build_apk():
    url = request.json.get('url')

    if not url:
        return jsonify({"error": "No URL provided"}), 400

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

    # Push to GitHub → triggers build
    os.system("git add .")
    os.system(f'git commit -m "Build APK for {url}"')
    os.system("git push")

    # 🔥 RETURN DOWNLOAD LINK
    apk_link = "https://github.com/kagendaimran1-cmd/WebView-apk/releases/download/latest/app-debug.apk"

    return jsonify({
        "message": "APK is building...",
        "download": apk_link
    })