from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder="../frontend/out", static_url_path="")

@app.route("/")
def serve_frontend():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route("/api")
def home():
    return jsonify({"message": "Earnmoney backend is running!"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)