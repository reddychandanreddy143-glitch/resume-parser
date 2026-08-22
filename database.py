import json
import os
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = "resumes.db"
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class ResumeRecord(Base):
    __tablename__ = "parsed_resumes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    candidate_name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    skills_json = Column(Text, nullable=True)
    education_text = Column(Text, nullable=True)
    experience_text = Column(Text, nullable=True)
    projects_text = Column(Text, nullable=True)
    parsed_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    """Initializes SQLite database and tables."""
    Base.metadata.create_all(engine)

def save_parsed_resume(filename: str, parsed_data: dict) -> int:
    """
    Saves a parsed candidate record into the database.
    
    Returns:
        int: Database record ID.
    """
    session = SessionLocal()
    try:
        record = ResumeRecord(
            filename=filename,
            candidate_name=parsed_data.get("candidate_name"),
            email=parsed_data.get("email"),
            phone=parsed_data.get("phone"),
            skills_json=json.dumps(parsed_data.get("skills", {})),
            education_text=parsed_data.get("sections", {}).get("education", ""),
            experience_text=parsed_data.get("sections", {}).get("experience", ""),
            projects_text=parsed_data.get("sections", {}).get("projects", "")
        )
        session.add(record)
        session.commit()
        session.refresh(record)
        return record.id
    finally:
        session.close()

if __name__ == "__main__":
    init_db()
    print("Database and 'parsed_resumes' table initialized successfully!")