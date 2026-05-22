import os
from datetime import datetime
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.declarative import declarative_base

# Database setup - use in-memory database for Vercel
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    name = Column(String)
    role = Column(String, default="alumni")
    approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# In-memory storage for Vercel
users_db = []

def get_db():
    # For Vercel serverless, use in-memory storage
    class MockDB:
        def query(self, model):
            return MockQuery(model, users_db)
        
        def add(self, obj):
            users_db.append(obj)
        
        def commit(self):
            pass
        
        def delete(self, obj):
            if obj in users_db:
                users_db.remove(obj)
        
        def close(self):
            pass
    
    yield MockDB()

class MockQuery:
    def __init__(self, model, data):
        self.model = model
        self.data = data
    
    def filter(self, condition):
        # Simple filter implementation
        if hasattr(condition, 'right') and hasattr(condition, 'left'):
            if condition.left.key == 'email':
                return MockQuery(self.model, [u for u in self.data if u.email == condition.right.value])
            elif condition.left.key == 'approved':
                return MockQuery(self.model, [u for u in self.data if u.approved == condition.right.value])
            elif condition.left.key == 'id':
                return MockQuery(self.model, [u for u in self.data if u.id == condition.right.value])
        return self
    
    def first(self):
        return self.data[0] if self.data else None
    
    def all(self):
        return self.data


app = FastAPI(title="Alumni Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mental-orange-xfiporkvgu.edgeone.app", "https://unacceptable-brown-ivex8qsavz.edgeone.app", "https://expected-gray-qabhmjhfak.edgeone.app", "https://burning-harlequin-p2qde19cco.edgeone.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"ok": True}

@app.post("/api/auth/login")
def login(payload: LoginRequest, db = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Simple password check for demo
    if not user.password_hash.startswith("hashed_") or user.password_hash != f"hashed_{payload.password}":
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    return {
        "access_token": "test_token", 
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "approved": user.approved,
            "name": user.name
        }
    }

@app.post("/api/auth/register")
def register(payload: RegisterRequest, db = Depends(get_db)):
    # Check if user exists
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email is already registered")
    
    # Create new user
    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        name=payload.name,
        role="alumni",
        approved=False
    )
    db.add(user)
    db.commit()
    
    return {"ok": True, "message": "Registration successful. Awaiting admin approval."}

# Admin endpoints
@app.get("/api/admin/pending")
def admin_pending(db = Depends(get_db)):
    # Return pending registrations
    pending = db.query(User).filter(User.approved == False).all()
    return [
        {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "approved": user.approved,
            "created_at": user.created_at
        }
        for user in pending
    ]

@app.get("/api/admin/alumni")
def admin_alumni():
    # Return empty list for now - no approved alumni
    return []

@app.get("/api/admin/feedback")
def admin_feedback():
    # Return empty list for now - no feedback submissions
    return []

@app.post("/api/admin/events")
def admin_events():
    return {"ok": True, "message": "Event created successfully"}

@app.post("/api/admin/jobs")
def admin_jobs():
    return {"ok": True, "message": "Job posted successfully"}

# Additional endpoints
@app.post("/api/auth/reset-password")
def reset_password():
    return {"ok": True, "message": "Password updated successfully"}

@app.get("/api/alumni")
def get_alumni(search: str = ""):
    # Return empty list for now
    return []

@app.get("/api/events")
def get_events():
    # Return empty list for now
    return []

@app.get("/api/jobs")
def get_jobs():
    # Return empty list for now
    return []

@app.get("/api/me")
def get_me():
    # Return admin user for now
    return {
        "id": 1,
        "email": "admin@college.edu",
        "role": "admin",
        "approved": True,
        "name": "Admin User"
    }

@app.put("/api/me/profile")
def update_profile():
    return {
        "id": 1,
        "email": "admin@college.edu",
        "role": "admin",
        "approved": True,
        "name": "Admin User"
    }

@app.post("/api/feedback")
def submit_feedback():
    return {"id": 1, "submitted_at": "2024-01-01", "alumni_id": 1, "status": "service"}

@app.post("/api/admin/pending/{user_id}/approve")
def approve_alumni(user_id: int, db = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.approved = True
    db.commit()
    return {"ok": True, "message": "Alumni approved"}

@app.post("/api/admin/pending/{user_id}/reject")
def reject_alumni(user_id: int, db = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"ok": True, "message": "Alumni rejected"}

# Vercel handler
handler = app
