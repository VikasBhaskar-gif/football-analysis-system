"""
launch_web_app.py
=================
Single-command launcher for the Football Tactical Predictor web application.
Serves both the FastAPI backend API and the compiled React production frontend
on http://127.0.0.1:8000.
"""

import os
import sys
import uvicorn

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

def main():
    print("=" * 60)
    print(" FOOTBALL TACTICAL PREDICTOR - WEB APPLICATION")
    print("=" * 60)
    print(" URL: http://127.0.0.1:8000")
    print(" API Docs: http://127.0.0.1:8000/docs")
    print(" Press Ctrl+C to terminate.")
    print("=" * 60)

    uvicorn.run(
        "webapp.backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="info",
    )

if __name__ == "__main__":
    main()
