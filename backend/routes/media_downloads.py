# 📁 File: /wanderlens/backend/routes/media_download.py
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
from database import get_db
from models import User

router = APIRouter()

# ===============================
# 🔒 ROUTE: Secure Media Download
# ===============================
@router.get("/download-media/{media_type}/{filename}")
def secure_media_download(media_type: str, filename: str, request: Request, db: Session = Depends(get_db)):
    email = request.headers.get("X-User-Email")
    firebase_uid = request.headers.get("X-Firebase-UID")

    if not email or not firebase_uid:
        raise HTTPException(status_code=401, detail="Missing credentials")

    user = db.query(User).filter(User.email == email).first()
    if not user or not user.verified or user.firebase_uid != firebase_uid:
        raise HTTPException(status_code=403, detail="Access denied")

    file_path = os.path.join("uploads", f"{media_type}s", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=file_path, filename=filename, media_type="application/octet-stream")

