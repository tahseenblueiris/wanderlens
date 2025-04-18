from sqlalchemy import Column, Integer, String
from database import Base

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
