import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Database configuration - works with PostgreSQL on various platforms
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:pIKGnUZDXREKqAuXVSITIwgPXugKisQG@postgres.railway.internal:5432/railway")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, default="alumni", nullable=False)
    approved = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Profile fields
    mobile = Column(String)
    gender = Column(String)
    batch = Column(String)
    course = Column(String)
    company_type = Column(String)
    company = Column(String)
    experience = Column(String)
    profile_picture = Column(Text)
    skills = Column(Text)
    achievements = Column(Text)
    
    # Relationships
    feedback = relationship("Feedback", back_populates="user")

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    date = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    type = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    contact = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    academic_year = Column(String, nullable=False)
    address = Column(String, nullable=False)
    status = Column(String, nullable=False)  # "service" or "higher"
    
    # Service fields
    designation = Column(String)
    organization = Column(String)
    
    # Higher studies fields
    program = Column(String)
    institution = Column(String)
    
    # Ratings
    teaching_learning = Column(Integer)
    curriculum_satisfaction = Column(Integer)
    academic_facilities = Column(Integer)
    student_interaction = Column(Integer)
    student_discipline = Column(Integer)
    internship = Column(Integer)
    career_counseling = Column(Integer)
    placement_drive = Column(Integer)
    extra_curricular = Column(Integer)
    overall_facilities = Column(Integer)
    
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship
    user = relationship("User", back_populates="feedback")

# Database functions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

def reset_db():
    """Drop and recreate all tables - use with caution"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
