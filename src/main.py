"""
SenseFlow - FastAPI Server Entry Point
Run this file to start the backend API (RoBERTa)
"""

import uvicorn

if __name__ == "__main__":
    print("[🚀] Starting SenseFlow API with RoBERTa...")
    print("[📡] Server running at http://localhost:8000")
    print("[🔗] Open browser → http://localhost:8000/docs")

    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
    