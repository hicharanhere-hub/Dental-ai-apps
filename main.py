from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Serve frontend at root
@app.get("/")
def home():
    return FileResponse("frontend/index.html")

# Serve other frontend files (CSS, JS, images)
app.mount("/", StaticFiles(directory="frontend"), name="frontend")

# API endpoint
@app.get("/api")
def api():
    return {"message": "DentalAI Pro API", "status": "operational"}
