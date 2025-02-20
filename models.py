from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from config import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    jobs = relationship("JobApplication", back_populates="user")

class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, index=True)
    job_title = Column(String)
    status = Column(String, default="applied")  
    applied_date = Column(DateTime, default=datetime.now(timezone.utc))

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="jobs")
