"""
Static demo server only.
Serves frontend/demo.html -> frontend/src/demo/main.js on port 5002.
This does not register the live API or run the real graph/simulation pipeline.
"""

import os
import sys

from flask import Flask, send_from_directory

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_demo(path):
    dist_dir = os.path.join(os.path.dirname(__file__), "frontend", "dist")

    if path and os.path.exists(os.path.join(dist_dir, path)):
        return send_from_directory(dist_dir, path)

    demo_entry = os.path.join(dist_dir, "demo.html")
    if os.path.exists(demo_entry):
        return send_from_directory(dist_dir, "demo.html")

    return (
        "Demo build not found. Run `cd frontend && npm run build` first, then start `python app_demo.py`.",
        503,
    )


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  DARSH DEMO SERVER")
    print("  Running on: http://localhost:5002")
    print("  Serving the static demo walkthrough")
    print("=" * 50 + "\n")

    app.run(
        host="0.0.0.0",
        port=5002,
        debug=True,
        use_reloader=False,
    )
