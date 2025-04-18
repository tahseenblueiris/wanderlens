# 📁 File: /wanderlens/backend/routes/register_user.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
import re, random, string, requests, os
from database import get_db
from models import User
from auth import hash_password
from utils import send_otp_email, store_temp_otp

router = APIRouter()

# ================================
# 📦 SCHEMA: Registration Request
# ================================
class RegisterRequest(BaseModel):
    firebase_uid: str
    full_name: str
    email: EmailStr
    address: str
    country: str
    state: str
    city: str
    zipcode: str
    mobile: str
    bonus_points: int
    recaptcha_token: str

# ============================================
# 🔐 SECTION: Verify Google reCAPTCHA (Server)
# ============================================
def verify_recaptcha(token: str) -> bool:
    secret_key = "6LdZQBwrAAAAAIEJTrO9zzJ4pXmnymFsS9KVLqii"
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={"secret": secret_key, "response": token},
    )
    return response.json().get("success", False)

# ======================================
# 🚀 ROUTE: Register New User with Bonus
# ======================================
@router.post("/register-user/")
def register_user(data: RegisterRequest, db: Session = Depends(get_db)):
    # 🚨 Input Validation: Prevent basic XSS
    if not re.match(r"^[a-zA-Z0-9 .,\-']+$", data.full_name):
        raise HTTPException(status_code=400, detail="Invalid name")

    # 🔐 Check reCAPTCHA
    if not verify_recaptcha(data.recaptcha_token):
        raise HTTPException(status_code=403, detail="reCAPTCHA verification failed")

    # 🔍 Check if user exists
    user = db.query(User).filter(User.email == data.email).first()
    if user:
        raise HTTPException(status_code=409, detail="User already registered")

    # 📧 Generate OTP
    otp = ''.join(random.choices(string.digits, k=6))
    store_temp_otp(data.email, otp)

    # 📤 Send OTP
    sent = send_otp_email(to=data.email, otp=otp)
    if not sent:
        raise HTTPException(status_code=500, detail="Failed to send OTP")

    # 💾 Save user
    new_user = User(
        firebase_uid=data.firebase_uid,
        full_name=data.full_name,
        email=data.email,
    )
    db.add(new_user)
    db.commit()

    return {"message": "OTP sent successfully. Please verify to complete registration."}

