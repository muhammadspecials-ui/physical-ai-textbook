from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import settings

# Create database engine
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    """User model for authentication and profiling."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # Background profiling
    software_experience = Column(String(50))  # beginner, intermediate, advanced
    hardware_experience = Column(String(50))  # beginner, intermediate, advanced
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ChatHistory(Base):
    """Chat history for RAG conversations."""
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)  # Optional: for logged-in users
    session_id = Column(String(255), index=True)
    
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    context_used = Column(Text)  # JSON string of retrieved chunks
    
    created_at = Column(DateTime, default=datetime.utcnow)


class ContentPersonalization(Base):
    """Store personalized content for users."""
    __tablename__ = "content_personalization"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    page_path = Column(String(500), nullable=False)
    
    original_content = Column(Text)
    personalized_content = Column(Text)
    language = Column(String(10), default="en")  # en, ur
    
    created_at = Column(DateTime, default=datetime.utcnow)


def get_db():
    """Dependency for getting database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
