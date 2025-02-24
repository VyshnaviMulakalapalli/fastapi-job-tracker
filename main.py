from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth import get_db, create_access_token, hash_password, get_user, verify_password
from models import User, JobApplication
from config import engine, Base
from auth import get_current_user
from typing import List

# Initialize FastAPI
app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    username: str
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Pydantic model for JobApplication
class JobApplicationCreate(BaseModel):
    job_title: str
    company_name: str
    status: str

class JobApplicationResponse(BaseModel):
    id: int
    job_title: str
    company_name: str
    status: str

# User registration endpoint
@app.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)  # Hash password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# User login endpoint
@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Create a job application
@app.post("/applications/", response_model=JobApplicationResponse)
def create_application(app: JobApplicationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    job_application = JobApplication(**app.dict(), user_id=current_user.id)
    db.add(job_application)
    db.commit()
    db.refresh(job_application)
    return job_application

# Get all job applications for the current user
@app.get("/applications/", response_model=List[JobApplicationResponse])
def read_applications(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    applications = db.query(JobApplication).filter(JobApplication.user_id == current_user.id).offset(skip).limit(limit).all()
    return applications

# Get a specific job application by ID
@app.get("/applications/{app_id}", response_model=JobApplicationResponse)
def read_application(app_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    application = db.query(JobApplication).filter(JobApplication.id == app_id, JobApplication.user_id == current_user.id).first()
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return application

# Update a job application
@app.put("/applications/{app_id}", response_model=JobApplicationResponse)
def update_application(app_id: int, app: JobApplicationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    application = db.query(JobApplication).filter(JobApplication.id == app_id, JobApplication.user_id == current_user.id).first()
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    for key, value in app.dict().items():
        setattr(application, key, value)
    db.commit()
    db.refresh(application)
    return application

# Delete a job application
@app.delete("/applications/{app_id}", response_model=JobApplicationResponse)
def delete_application(app_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    application = db.query(JobApplication).filter(JobApplication.id == app_id, JobApplication.user_id == current_user.id).first()
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(application)
    db.commit()
    return application
