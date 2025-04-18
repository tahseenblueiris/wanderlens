# 📁 File: /wanderlens/backend/models.py
from sqlalchemy import Column, Integer, String, Boolean, Date, Time
from database import Base

# ===========================
# 🧍‍♂️ User Model for MySQL DB
# ===========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    firebase_uid = Column(String, unique=True)
    country = Column(String)
    city = Column(String)
    state = Column(String)
    zipcode = Column(String)
    address = Column(String)
    mobile = Column(String)
    verified = Column(Boolean, default=False)
    bonus_points = Column(Integer, default=0)

# ===========================
# 📝 Blog Model for Blog Post
# ===========================
class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True)
    user_email = Column(String)
    title = Column(String)
    description = Column(String)
    photo_filename = Column(String, nullable=True)
    video_filename = Column(String, nullable=True)
    date = Column(Date)
    time = Column(Time)
