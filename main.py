from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# API endpoint (keep this)
@app.get("/api")
def api_info():
    return {"message": "DentalAI Pro API", "status": "operational"}

# Serve frontend HTML at root
@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")

# Optional: Serve all frontend files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="frontend"), name="static")
