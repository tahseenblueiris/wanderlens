from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

# Define the DB URL (your password contains special characters, so it’s already correctly URL-encoded)
DATABASE_URL = "mysql+mysqlconnector://root:Tanaz2411##@localhost/wanderlens"

# Create SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for all ORM models
Base = declarative_base()

# Dependency to get DB session in FastAPI
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
