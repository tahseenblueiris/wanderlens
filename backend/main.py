from fastapi.responses import FileResponse, HTMLResponse
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import shutil
import uuid
import sqlite3
# 🧩 Route Imports (after defining app)
from routes import register_user  # ✅ Your new route file
from routes import login_user
from routes import media_gallery


app = FastAPI()

# 🔄 Middleware Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔗 Static File Mount
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 🧠 Include Routes
app.include_router(register_user.router)
app.include_router(login_user.router)
app.include_router(media_gallery.router)

# Allowed extensions
PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}

# Max file sizes
MAX_PHOTO_SIZE = 100 * 1024 * 1024     # 100 MB
MAX_VIDEO_SIZE = 5 * 1024 * 1024 * 1024  # 5 GB

# =======================
# DB Initialization
# =======================
def init_db():
    conn = sqlite3.connect("media.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS media (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    description TEXT,
                    tags TEXT,
                    media_type TEXT,
                    filename TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

# =======================
# Upload Endpoint
# =======================
@app.post("/upload/")
async def upload_file(
    title: str = Form(...),
    description: str = Form(...),
    tags: str = Form(...),
    media_type: str = Form(...),
    file: UploadFile = File(...)
):
    # Validate media_type
    if media_type not in ['photo', 'video']:
        raise HTTPException(status_code=400, detail="Invalid media_type. Use 'photo' or 'video'.")

    ext = os.path.splitext(file.filename)[1].lower()

    if media_type == 'photo' and ext not in PHOTO_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only image formats are allowed.")
    if media_type == 'video' and ext not in VIDEO_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only video formats are allowed.")

    # Read file into memory (check size before saving)
    contents = await file.read()
    file_size = len(contents)

    if media_type == 'photo' and file_size > MAX_PHOTO_SIZE:
        raise HTTPException(status_code=413, detail="Photo size exceeds 100 MB limit.")
    if media_type == 'video' and file_size > MAX_VIDEO_SIZE:
        raise HTTPException(status_code=413, detail="Video size exceeds 5 GB limit.")

    filename = f"{uuid.uuid4().hex}{ext}"
    upload_folder = os.path.join("uploads", f"{media_type}s")
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, filename)

    with open(file_path, "wb") as f:
        f.write(contents)

    conn = sqlite3.connect("media.db")
    c = conn.cursor()
    c.execute("INSERT INTO media (title, description, tags, media_type, filename) VALUES (?, ?, ?, ?, ?)",
              (title, description, tags, media_type, filename))
    conn.commit()
    conn.close()

    return {"message": f"{media_type.capitalize()} uploaded successfully", "filename": filename}

# =======================
# Get All Media
# =======================
@app.get("/media/")
def get_all_media():
    conn = sqlite3.connect("media.db")
    c = conn.cursor()
    c.execute("SELECT id, title, description, tags, media_type, filename FROM media ORDER BY id DESC")

    items = []
    for row in c.fetchall():
        file_path = os.path.join("uploads", f"{row[4]}s", row[5])
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            items.append({
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "tags": row[3],
                "media_type": row[4],
                "filename": row[5],
                "file_size_bytes": file_size,
                "url": f"/uploads/{row[4]}s/{row[5]}"
            })

    conn.close()
    return items

# =======================
# Delete Media by ID
# =======================
@app.delete("/delete/{media_id}")
def delete_media(media_id: int):
    conn = sqlite3.connect("media.db")
    c = conn.cursor()
    c.execute("SELECT media_type, filename FROM media WHERE id = ?", (media_id,))
    row = c.fetchone()

    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Media not found.")

    file_path = os.path.join("uploads", f"{row[0]}s", row[1])
    if os.path.exists(file_path):
        os.remove(file_path)

    c.execute("DELETE FROM media WHERE id = ?", (media_id,))
    conn.commit()
    conn.close()

    return {"message": "Media deleted successfully."}

# =======================
# Root
# =======================
@app.get("/", response_class=HTMLResponse)
def root():
    return "<h2>🌍 WanderLens Backend Running</h2><p>Use /upload/, /media/, and /delete/{id} endpoints</p>"
