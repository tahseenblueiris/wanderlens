# 📁 File: /wanderlens/backend/utils.py

import os
import smtplib
import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# ===========================
# 🔄 Load .env for SMTP Creds
# ===========================
load_dotenv()
SMTP_SERVER = "smtp.zoho.com"
SMTP_PORT = 465
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "blueirisoft@zohomail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# ======================================
# 📤 FUNCTION: Send OTP Email to User
# ======================================
def send_otp_email(to: str, otp: str) -> bool:
    FROM_EMAIL = SMTP_USERNAME
    SUBJECT = "WanderLens OTP Verification"
    BODY = f"""
    Hello,

    Your One-Time Password (OTP) for WanderLens is: {otp}

    This OTP is valid for 10 minutes. Do not share it with anyone.

    Thank you,
    WanderLens Team
    """
    try:
        msg = MIMEMultipart()
        msg["From"] = FROM_EMAIL
        msg["To"] = to
        msg["Subject"] = SUBJECT
        msg.attach(MIMEText(BODY, "plain"))

        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(FROM_EMAIL, to, msg.as_string())
        server.quit()
        print(f"✅ OTP sent to {to}")
        return True
    except Exception as e:
        print(f"❌ Failed to send OTP to {to}: {e}")
        return False

# ======================================
# 🗄️ FUNCTION: Store OTP Temporarily
# DB: otp_store.db with table `otp`
# ======================================
def store_temp_otp(email: str, otp: str):
    conn = sqlite3.connect("otp_store.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS otp (
            email TEXT PRIMARY KEY,
            otp TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("REPLACE INTO otp (email, otp) VALUES (?, ?)", (email, otp))
    conn.commit()
    conn.close()

# ======================================
# ✅ FUNCTION: Verify OTP
# ======================================
def verify_otp(email: str, input_otp: str) -> bool:
    conn = sqlite3.connect("otp_store.db")
    c = conn.cursor()
    c.execute("SELECT otp FROM otp WHERE email = ?", (email,))
    row = c.fetchone()
    conn.close()
    return row and row[0] == input_otp

