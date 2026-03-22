# app.py
# THE MAIN ENTRY POINT FOR THE DARSH FLASK SERVER
#
# Run with: python app.py
# API runs on: http://localhost:5001
# Serves the real app entry: frontend/index.html -> frontend/src/app/main.js

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from api.routes import api_bp

app = Flask(__name__)

# Allow Vue dev server (port 5173) to call Flask API (port 5001)
CORS(app, origins=["http://localhost:5173", "http://localhost:3000"])

# Register all API routes
app.register_blueprint(api_bp)

# Serve the built Vue app in production (not needed for development)
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    dist_dir = os.path.join(os.path.dirname(__file__), "frontend", "dist")
    if path and os.path.exists(os.path.join(dist_dir, path)):
        return send_from_directory(dist_dir, path)
    return send_from_directory(dist_dir, "index.html")


if __name__ == "__main__":
    print("\n" + "="*50)
    print("  DARSH API SERVER")
    print("  Running on: http://localhost:5001")
    print("  Make sure ollama serve is running in another tab")
    print("="*50 + "\n")

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True,
        use_reloader=False  # prevents double-loading with threading
    )
