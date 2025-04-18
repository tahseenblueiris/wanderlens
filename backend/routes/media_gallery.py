# 📁 File: /wanderlens/backend/routes/media_gallery.py
from fastapi import APIRouter
import os, sqlite3

router = APIRouter()

# ===============================
# 🖼️ Public Media Gallery Listing
# ===============================
@router.get("/public-gallery/")
def get_public_gallery():
    conn = sqlite3.connect("media.db")
    c = conn.cursor()
    c.execute("SELECT id, title, description, tags, media_type, filename FROM media ORDER BY id DESC")

    items = []
    for row in c.fetchall():
        file_url = f"/uploads/{row[4]}s/{row[5]}"
        items.append({
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "tags": row[3],
            "media_type": row[4],
            "filename": row[5],
            "url": file_url,
            "preview_only": True  # 👁️ Show watermark / block download until login
        })
    conn.close()
    return items
