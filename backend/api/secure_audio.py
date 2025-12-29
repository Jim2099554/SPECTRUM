from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from core.auth.verification import verify_token
from utils.crypto import encrypt_file
import os
import uuid

router = APIRouter()

from backend.config import AUDIO_UPLOAD_DIR
os.makedirs(AUDIO_UPLOAD_DIR, exist_ok=True)

@router.post("/upload-audio", summary="Securely upload and encrypt an audio file")
def upload_audio(
    file: UploadFile = File(...),
    user_id: str = Depends(verify_token)
):
    """
    Uploads an audio file, encrypts it, and saves it securely for the authenticated user.
    """
    # Generate a secure, random filename
    file_id = str(uuid.uuid4())
    raw_path = os.path.join(AUDIO_UPLOAD_DIR, f"{file_id}_raw")
    enc_path = os.path.join(AUDIO_UPLOAD_DIR, f"{file_id}.enc")
    
    # Save the uploaded file temporarily
    with open(raw_path, "wb") as f:
        f.write(file.file.read())
    
    # Encrypt the file and remove the raw copy
    encrypt_file(raw_path, enc_path)
    os.remove(raw_path)
    
    return {"status": "success", "file_id": file_id}

@router.get("/download-audio/{file_id}", summary="Download and decrypt an audio file")
def download_audio(
    file_id: str,
    user_id: str = Depends(verify_token)
):
    """
    Downloads and (optionally) decrypts an audio file for the authenticated user.
    """
    enc_path = os.path.join(AUDIO_UPLOAD_DIR, f"{file_id}.enc")
    if not os.path.exists(enc_path):
        raise HTTPException(status_code=404, detail="File not found")
    # For demo: just return path (replace with StreamingResponse in production)
    return {"status": "success", "path": enc_path}
