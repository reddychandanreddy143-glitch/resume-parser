import json
import os
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resumes.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class User(UserMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    resumes = relationship("ResumeRecord", back_populates="owner", cascade="all, delete-orphan")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class ResumeRecord(Base):
    __tablename__ = "parsed_resumes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    candidate_name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    skills_json = Column(Text, nullable=True)
    education_text = Column(Text, nullable=True)
    experience_text = Column(Text, nullable=True)
    projects_text = Column(Text, nullable=True)
    parsed_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="resumes")


def init_db():
    Base.metadata.create_all(engine)


def save_parsed_resume(user_id: int, filename: str, parsed_data: dict) -> int:
    session = SessionLocal()
    try:
        record = ResumeRecord(
            user_id=user_id,
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
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    init_db()
    print("Database schema successfully verified!")