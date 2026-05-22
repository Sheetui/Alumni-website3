import os
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from database import engine, get_db, init_db, User, Event, Job, Feedback

# Load environment variables
load_dotenv()

# Initialize database
init_db()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# FastAPI app
app = FastAPI(title="Alumni Backend")

# CORS configuration
origins = os.getenv("CORS_ORIGINS", "*").split(",") if os.getenv("CORS_ORIGINS") else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str
    batch: str = ""
    course: str = ""
    company_type: str = "company"
    company: str = ""

class ProfileUpdateRequest(BaseModel):
    name: str
    email: str
    mobile: str = ""
    gender: str = ""
    batch: str = ""
    course: str = ""
    company_type: str = ""
    company: str = ""
    experience: str = ""
    profile_picture: str = ""
    skills: str = ""
    achievements: str = ""

class EventCreateRequest(BaseModel):
    title: str
    date: str
    description: str

class JobCreateRequest(BaseModel):
    title: str
    company: str
    type: str
    description: str
    contact: str = ""

class FeedbackCreateRequest(BaseModel):
    name: str
    email: str
    academic_year: str
    address: str
    status: str
    designation: str = ""
    organization: str = ""
    program: str = ""
    institution: str = ""
    teaching_learning: int
    curriculum_satisfaction: int
    academic_facilities: int
    student_interaction: int
    student_discipline: int
    internship: int
    career_counseling: int
    placement_drive: int
    extra_curricular: int
    overall_facilities: int

# Helper functions
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Health check
@app.get("/api/health")
def health():
    return {"ok": True, "database": "connected"}

# Authentication endpoints
@app.post("/api/auth/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    if user.role == "alumni" and not user.approved:
        raise HTTPException(status_code=403, detail="Your registration is pending admin approval.")
    
    return {
        "access_token": "token_placeholder",  # In production, use JWT
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "approved": user.approved,
            "name": user.name,
            "profile_picture": user.profile_picture or ""
        }
    }

@app.post("/api/auth/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    email = payload.email.strip().lower()
    
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email is already registered.")
    
    if len(payload.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters.")
    
    user = User(
        email=email,
        password_hash=hash_password(payload.password),
        name=payload.name,
        role="alumni",
        approved=False,
        batch=payload.batch,
        course=payload.course,
        company_type=payload.company_type,
        company=payload.company
    )
    db.add(user)
    db.commit()
    
    return {"ok": True, "message": "Registration successful. Awaiting admin approval."}

@app.post("/api/auth/reset-password")
def reset_password(email: str, new_password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.password_hash = hash_password(new_password)
    db.commit()
    
    return {"ok": True, "message": "Password updated successfully"}

# Profile endpoints
@app.get("/api/me")
def get_me(db: Session = Depends(get_db)):
    # In production, get from JWT token
    return {
        "id": 1,
        "email": "admin@college.edu",
        "role": "admin",
        "approved": True,
        "name": "Admin User"
    }

@app.put("/api/me/profile")
def update_profile(payload: ProfileUpdateRequest, db: Session = Depends(get_db)):
    # In production, get user from JWT token
    user = db.query(User).filter(User.email == payload.email).first()
    if user:
        user.name = payload.name
        user.mobile = payload.mobile
        user.gender = payload.gender
        user.batch = payload.batch
        user.course = payload.course
        user.company_type = payload.company_type
        user.company = payload.company
        user.experience = payload.experience
        user.profile_picture = payload.profile_picture
        user.skills = payload.skills
        user.achievements = payload.achievements
        db.commit()
        
        return {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "approved": user.approved,
            "name": user.name,
            "profile_picture": user.profile_picture or ""
        }
    
    return {"ok": False, "message": "User not found"}

# Public data endpoints
@app.get("/api/alumni")
def get_alumni(search: str = "", db: Session = Depends(get_db)):
    query = db.query(User).filter(User.approved == True, User.role == "alumni")
    if search:
        query = query.filter(
            User.name.ilike(f"%{search}%") | 
            User.course.ilike(f"%{search}%") |
            User.company.ilike(f"%{search}%")
        )
    alumni = query.all()
    
    return [
        {
            "id": a.id,
            "name": a.name,
            "batch": a.batch,
            "course": a.course,
            "company": a.company,
            "profile_picture": a.profile_picture or ""
        }
        for a in alumni
    ]

@app.get("/api/events")
def get_events(db: Session = Depends(get_db)):
    events = db.query(Event).order_by(Event.created_at.desc()).all()
    
    return [
        {
            "id": e.id,
            "title": e.title,
            "date": e.date,
            "description": e.description
        }
        for e in events
    ]

@app.get("/api/jobs")
def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).order_by(Job.created_at.desc()).all()
    
    return [
        {
            "id": j.id,
            "title": j.title,
            "company": j.company,
            "type": j.type,
            "description": j.description,
            "contact": j.contact
        }
        for j in jobs
    ]

@app.post("/api/feedback")
def submit_feedback(payload: FeedbackCreateRequest, db: Session = Depends(get_db)):
    feedback = Feedback(
        user_id=1,  # In production, get from JWT
        name=payload.name,
        email=payload.email,
        academic_year=payload.academic_year,
        address=payload.address,
        status=payload.status,
        designation=payload.designation,
        organization=payload.organization,
        program=payload.program,
        institution=payload.institution,
        teaching_learning=payload.teaching_learning,
        curriculum_satisfaction=payload.curriculum_satisfaction,
        academic_facilities=payload.academic_facilities,
        student_interaction=payload.student_interaction,
        student_discipline=payload.student_discipline,
        internship=payload.internship,
        career_counseling=payload.career_counseling,
        placement_drive=payload.placement_drive,
        extra_curricular=payload.extra_curricular,
        overall_facilities=payload.overall_facilities
    )
    db.add(feedback)
    db.commit()
    
    return {
        "id": feedback.id,
        "submitted_at": feedback.submitted_at,
        "alumni_id": feedback.user_id,
        "status": feedback.status
    }

# Admin endpoints
@app.get("/api/admin/pending")
def admin_pending(search: str = "", db: Session = Depends(get_db)):
    query = db.query(User).filter(User.approved == False)
    if search:
        query = query.filter(User.name.ilike(f"%{search}%") | User.email.ilike(f"%{search}%"))
    
    pending = query.all()
    
    return [
        {
            "id": p.id,
            "email": p.email,
            "name": p.name,
            "batch": p.batch,
            "course": p.course,
            "company": p.company,
            "created_at": p.created_at
        }
        for p in pending
    ]

@app.get("/api/admin/alumni")
def admin_alumni(search: str = "", db: Session = Depends(get_db)):
    query = db.query(User).filter(User.approved == True, User.role == "alumni")
    if search:
        query = query.filter(User.name.ilike(f"%{search}%") | User.email.ilike(f"%{search}%"))
    
    alumni = query.all()
    
    return [
        {
            "id": a.id,
            "email": a.email,
            "name": a.name,
            "batch": a.batch,
            "course": a.course,
            "company": a.company,
            "mobile": a.mobile,
            "gender": a.gender,
            "experience": a.experience,
            "skills": a.skills,
            "achievements": a.achievements
        }
        for a in alumni
    ]

@app.get("/api/admin/feedback")
def admin_feedback(db: Session = Depends(get_db)):
    feedback = db.query(Feedback).order_by(Feedback.submitted_at.desc()).all()
    
    return [
        {
            "id": f.id,
            "submitted_at": f.submitted_at,
            "alumni_id": f.user_id,
            "status": f.status,
            "name": f.name,
            "email": f.email
        }
        for f in feedback
    ]

@app.post("/api/admin/pending/{user_id}/approve")
def approve_alumni(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.approved = True
    db.commit()
    
    return {"ok": True, "message": "Alumni approved"}

@app.post("/api/admin/pending/{user_id}/reject")
def reject_alumni(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    
    return {"ok": True, "message": "Alumni rejected"}

@app.post("/api/admin/events")
def admin_events(payload: EventCreateRequest, db: Session = Depends(get_db)):
    event = Event(
        title=payload.title,
        date=payload.date,
        description=payload.description
    )
    db.add(event)
    db.commit()
    
    return {"ok": True, "message": "Event created successfully"}

@app.post("/api/admin/jobs")
def admin_jobs(payload: JobCreateRequest, db: Session = Depends(get_db)):
    job = Job(
        title=payload.title,
        company=payload.company,
        type=payload.type,
        description=payload.description,
        contact=payload.contact
    )
    db.add(job)
    db.commit()
    
    return {"ok": True, "message": "Job posted successfully"}

# Create default admin user
def create_default_admin():
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.email == "admin@college.edu").first()
        if not admin:
            admin = User(
                email="admin@college.edu",
                password_hash=hash_password("admin123"),
                name="Admin User",
                role="admin",
                approved=True
            )
            db.add(admin)
            db.commit()
            print("Default admin user created")
    finally:
        db.close()

# Initialize with admin user
create_default_admin()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
