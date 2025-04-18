# 📁 File: /wanderlens/backend/routes/login_user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
import requests, random, string
from database import get_db
from models import User
from utils import send_otp_email, store_temp_otp

router = APIRouter()

# ===========================
# 📦 SCHEMA: Login Request
# ===========================
class LoginRequest(BaseModel):
    firebase_uid: str
    email: EmailStr
    recaptcha_token: str

# ======================================
# 🔐 reCAPTCHA Verify (reused function)
# ======================================
def verify_recaptcha(token: str) -> bool:
    secret_key = "6LdZQBwrAAAAAIEJTrO9zzJ4pXmnymFsS9KVLqii"
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", data={"secret": secret_key, "response": token})
    return response.json().get("success", False)

# ===========================
# 🚀 Login + OTP Verification
# ===========================
@router.post("/login-user/")
def login_user(data: LoginRequest, db: Session = Depends(get_db)):
    # ✅ reCAPTCHA check
    if not verify_recaptcha(data.recaptcha_token):
        raise HTTPException(status_code=403, detail="Failed reCAPTCHA validation")

    # 🔍 Find user by email
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found. Please sign up.")

    # 🔐 Firebase UID must match
    if user.firebase_uid != data.firebase_uid:
        raise HTTPException(status_code=401, detail="Firebase identity mismatch")

    # 🚦 If already verified, login allowed
    if user.verified:
        return {"message": "Login verified.", "bonus_points": user.bonus_points, "verified": True}

    # 📧 Otherwise, resend OTP
    otp = ''.join(random.choices(string.digits, k=6))
    store_temp_otp(user.email, otp)
    if not send_otp_email(to=user.email, otp=otp):
        raise HTTPException(status_code=500, detail="OTP resend failed")

    return {"message": "OTP sent again. Please verify to complete login.", "verified": False}

