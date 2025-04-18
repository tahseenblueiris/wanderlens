# 📁 File: /wanderlens/backend/routes/verify_otp.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from database import get_db
from models import User
from utils import verify_otp

router = APIRouter()

# ===============================
# 📦 SCHEMA: OTP Verification
# ===============================
class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str

# ===================================
# 🚀 ROUTE: Verify User Email by OTP
# ===================================
@router.post("/verify-otp/")
def verify_user_otp(data: OTPVerifyRequest, db: Session = Depends(get_db)):
    # ✅ Step 1: Validate OTP
    if not verify_otp(data.email, data.otp):
        raise HTTPException(status_code=401, detail="Invalid or expired OTP")

    # 🔍 Step 2: Fetch user
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ Step 3: Mark verified (we need to add this field to model)
    if hasattr(user, 'verified'):
        user.verified = True
        db.commit()

    return {"message": "✅ Email verified successfully! You can now log in."}

