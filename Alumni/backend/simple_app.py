import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Alumni Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mental-orange-xfiporkvgu.edgeone.app", "https://unacceptable-brown-ivex8qsavz.edgeone.app", "https://expected-gray-qabhmjhfak.edgeone.app", "https://burning-harlequin-p2qde19cco.edgeone.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
users_db = []

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str

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

@app.get("/api/health")
def health():
    return {"ok": True}

@app.post("/api/auth/login")
def login(payload: LoginRequest):
    return {
        "access_token": "test_token", 
        "user": {
            "id": 1,
            "email": payload.email,
            "role": "admin",
            "approved": True,
            "name": "Admin User"
        }
    }

@app.post("/api/auth/register")
def register(payload: RegisterRequest):
    # Check if user exists
    for user in users_db:
        if user["email"] == payload.email:
            return {"ok": False, "message": "Email is already registered"}
    
    # Create new user
    new_user = {
        "id": len(users_db) + 1,
        "email": payload.email,
        "password_hash": f"hashed_{payload.password}",
        "name": payload.name,
        "role": "alumni",
        "approved": False,
        "profile_picture": ""
    }
    users_db.append(new_user)
    
    return {"ok": True, "message": "Registration successful. Awaiting admin approval."}

@app.get("/api/admin/pending")
def admin_pending():
    # Return pending registrations
    pending = [user for user in users_db if not user["approved"]]
    return pending

@app.post("/api/admin/pending/{user_id}/approve")
def approve_alumni(user_id: int):
    for user in users_db:
        if user["id"] == user_id:
            user["approved"] = True
            return {"ok": True, "message": "Alumni approved"}
    return {"ok": False, "message": "User not found"}

@app.post("/api/admin/pending/{user_id}/reject")
def reject_alumni(user_id: int):
    for user in users_db:
        if user["id"] == user_id:
            users_db.remove(user)
            return {"ok": True, "message": "Alumni rejected"}
    return {"ok": False, "message": "User not found"}

@app.get("/api/admin/alumni")
def admin_alumni():
    # Return approved alumni
    approved = [user for user in users_db if user["approved"]]
    return approved

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

@app.post("/api/auth/reset-password")
def reset_password():
    return {"ok": True, "message": "Password updated successfully"}

@app.get("/api/alumni")
def get_alumni():
    # Return approved alumni
    approved = [user for user in users_db if user["approved"]]
    return approved

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
def update_profile(payload: ProfileUpdateRequest):
    # Update user in database with profile picture
    for user in users_db:
        if user["email"] == payload.email:
            user["name"] = payload.name
            user["profile_picture"] = payload.profile_picture
            return {
                "id": user["id"],
                "email": user["email"],
                "role": user["role"],
                "approved": user["approved"],
                "name": user["name"],
                "profile_picture": user["profile_picture"]
            }
    
    # If user not found, return default response
    return {
        "id": 1,
        "email": payload.email,
        "role": "admin",
        "approved": True,
        "name": payload.name,
        "profile_picture": payload.profile_picture
    }

@app.post("/api/feedback")
def submit_feedback():
    return {"id": 1, "submitted_at": "2024-01-01", "alumni_id": 1, "status": "service"}

# Vercel handler
handler = app
