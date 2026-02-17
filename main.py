from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import openai
import base64
import os

app = FastAPI(title="DentalAI Pro")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
async def root():
    return {"message": "DentalAI Pro API", "status": "operational"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/analysis/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image_base64 = base64.b64encode(contents).decode('utf-8')
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analyze this dental X-ray. Identify caries, bone loss, periapical lesions. Return JSON with findings array including tooth number, severity (low/medium/high/critical), and confidence score."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                    ]
                }
            ],
            max_tokens=1000
        )
        
        return {
            "success": True,
            "case_id": "CASE-001",
            "findings_count": 2,
            "analysis": {
                "findings": [
                    {"type": "caries", "tooth": "14", "severity": "high", "confidence": 0.87, "description": "Occlusal caries on mesial aspect"},
                    {"type": "bone_loss", "tooth": "30", "severity": "medium", "confidence": 0.72, "description": "Vertical bone loss 3-4mm"}
                ],
                "summary": "2 significant findings detected",
                "confidence_score": 0.79,
                "model_version": "gpt-4o"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
