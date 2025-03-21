from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="Spectrum",
    description="Advanced phone call analysis tool",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Spectrum API"}

@app.post("/analyze/audio")
async def analyze_audio(file: UploadFile = File(...)):
    """
    Endpoint for uploading and analyzing audio files
    """
    return {"filename": file.filename, "status": "processing"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
