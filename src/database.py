"""
Database setup and configuration for NIST-AI-SCM Toolkit.
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./nist_ai_scm.db")

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Assessment(Base):
    """Assessment records table."""
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    system_name = Column(String, index=True)
    model_type = Column(String)
    risk_score = Column(Float)
    risk_level = Column(String)
    assessment_date = Column(DateTime, default=datetime.utcnow)
    compliance_gaps = Column(Text)  # JSON string
    recommended_actions = Column(Text)  # JSON string


class CSFCategory(Base):
    """NIST CSF categories table."""
    __tablename__ = "csf_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    category_code = Column(String, unique=True, index=True)
    function_name = Column(String)
    category_name = Column(String)
    description = Column(Text)


def create_tables():
    """Create database tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully!")