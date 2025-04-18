# 📁 File: /wanderlens/backend/routes/get_blogs.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Blog

router = APIRouter()

# =============================
# 📚 ROUTE: Get All Blog Posts
# =============================
@router.get("/get-blogs/")
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(Blog).order_by(Blog.id.desc()).all()
    return [
        {
            "id": blog.id,
            "email": blog.user_email,
            "title": blog.title,
            "description": blog.description,
            "photo_url": f"/uploads/blog_photos/{blog.photo_filename}" if blog.photo_filename else None,
            "video_url": f"/uploads/blog_videos/{blog.video_filename}" if blog.video_filename else None,
            "date": blog.date.isoformat(),
            "time": blog.time.strftime("%H:%M:%S")
        }
        for blog in blogs
    ]

