# 📁 File: /wanderlens/backend/routes/post_blog.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import os, uuid, shutil
from database import get_db
from models import Blog, User

router = APIRouter()

# Allowed media types for blog
PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}

# ==========================
# 📤 BLOG POST API ENDPOINT
# ==========================
@router.post("/post-blog/")
def post_blog(
    title: str = Form(...),
    description: str = Form(...),
    email: str = Form(...),
    photo: UploadFile = File(None),
    video: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.verified:
        raise HTTPException(status_code=403, detail="Please verify your account to post")

    photo_filename = None
    video_filename = None

    # 📸 Save photo if uploaded
    if photo:
        ext = os.path.splitext(photo.filename)[1].lower()
        if ext not in PHOTO_EXTENSIONS:
            raise HTTPException(status_code=400, detail="Unsupported photo format")
        photo_filename = f"blog_{uuid.uuid4().hex}{ext}"
        os.makedirs("uploads/blog_photos", exist_ok=True)
        with open(f"uploads/blog_photos/{photo_filename}", "wb") as f:
            shutil.copyfileobj(photo.file, f)

    # 🎞️ Save video if uploaded
    if video:
        ext = os.path.splitext(video.filename)[1].lower()
        if ext not in VIDEO_EXTENSIONS:
            raise HTTPException(status_code=400, detail="Unsupported video format")
        video_filename = f"blog_{uuid.uuid4().hex}{ext}"
        os.makedirs("uploads/blog_videos", exist_ok=True)
        with open(f"uploads/blog_videos/{video_filename}", "wb") as f:
            shutil.copyfileobj(video.file, f)

    new_blog = Blog(
        title=title,
        description=description,
        user_email=email,
        date=datetime.utcnow().date(),
        time=datetime.utcnow().time(),
        photo_filename=photo_filename,
        video_filename=video_filename
    )
    db.add(new_blog)

    # 🎁 Bonus point system
    user.bonus_points += 5
    db.commit()

    return {"message": "Blog posted successfully with bonus!"}

