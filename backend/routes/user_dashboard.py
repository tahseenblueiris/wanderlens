# 📁 File: /wanderlens/backend/routes/user_dashboard.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
from models import User

router = APIRouter()

# =============================
# 👤 ROUTE: User Dashboard Data
# =============================
@router.get("/user-dashboard/")
def get_user_dashboard(request: Request, db: Session = Depends(get_db)):
    email = request.headers.get("X-User-Email")
    firebase_uid = request.headers.get("X-Firebase-UID")

    if not email or not firebase_uid:
        raise HTTPException(status_code=401, detail="Missing authentication headers")

    user = db.query(User).filter(User.email == email).first()
    if not user or user.firebase_uid != firebase_uid:
        raise HTTPException(status_code=403, detail="Invalid credentials")

    return {
        "email": user.email,
        "full_name": user.full_name,
        "verified": user.verified,
        "bonus_points": user.bonus_points,
        "city": user.city,
        "country": user.country
    }
