from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional, List
import uuid

from config import settings
from database import get_db, init_db, User, ChatHistory, ContentPersonalization
from auth_service import auth_service
from rag_service import rag_service
from qdrant_service import qdrant_service

# Initialize FastAPI app
app = FastAPI(
    title="Physical AI Textbook API",
    description="Backend API for Physical AI & Humanoid Robotics Textbook",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models
class SignupRequest(BaseModel):
    email: EmailStr
    name: str
    password: str
    software_experience: str  # beginner, intermediate, advanced
    hardware_experience: str  # beginner, intermediate, advanced


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ChatRequest(BaseModel):
    question: str
    selected_text: Optional[str] = None
    session_id: Optional[str] = None


class PersonalizeRequest(BaseModel):
    content: str
    page_path: str


class TranslateRequest(BaseModel):
    content: str


class IngestDocumentsRequest(BaseModel):
    documents: List[dict]


# Dependency to get current user
async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Get current user from JWT token."""
    if not authorization or not authorization.startswith("Bearer "):
        return None
    
    token = authorization.replace("Bearer ", "")
    payload = auth_service.verify_token(token)
    
    if not payload:
        return None
    
    user = auth_service.get_user_by_id(db, payload["user_id"])
    return user


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database and Qdrant on startup."""
    init_db()
    qdrant_service.create_collection()
    print("[OK] Database and Qdrant initialized")


# Health check
@app.get("/")
async def root():
    return {
        "message": "Physical AI Textbook API",
        "status": "running",
        "version": "1.0.0"
    }


# Auth endpoints
@app.post("/api/auth/signup")
async def signup(request: SignupRequest, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if user exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    user = auth_service.create_user(
        db=db,
        email=request.email,
        name=request.name,
        password=request.password,
        software_experience=request.software_experience,
        hardware_experience=request.hardware_experience
    )
    
    # Generate token
    token = auth_service.create_access_token(user.id, user.email)
    
    return {
        "message": "User created successfully",
        "token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "software_experience": user.software_experience,
            "hardware_experience": user.hardware_experience
        }
    }


@app.post("/api/auth/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Login user."""
    user = auth_service.authenticate_user(db, request.email, request.password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = auth_service.create_access_token(user.id, user.email)
    
    return {
        "message": "Login successful",
        "token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "software_experience": user.software_experience,
            "hardware_experience": user.hardware_experience
        }
    }


@app.get("/api/auth/me")
async def get_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user profile."""
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "software_experience": current_user.software_experience,
        "hardware_experience": current_user.hardware_experience
    }


# RAG Chat endpoints
@app.post("/api/chat")
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    """Chat with RAG bot."""
    
    # Get user profile if authenticated
    user_profile = None
    if current_user:
        user_profile = {
            "software_experience": current_user.software_experience,
            "hardware_experience": current_user.hardware_experience
        }
    
    # Generate answer
    result = rag_service.answer_question(
        question=request.question,
        selected_text=request.selected_text,
        user_profile=user_profile
    )
    
    # Save to chat history
    session_id = request.session_id or str(uuid.uuid4())
    chat_history = ChatHistory(
        user_id=current_user.id if current_user else None,
        session_id=session_id,
        question=request.question,
        answer=result["answer"],
        context_used=str(result["sources"])
    )
    db.add(chat_history)
    db.commit()
    
    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "session_id": session_id
    }


# Content personalization
@app.post("/api/personalize")
async def personalize_content(
    request: PersonalizeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Personalize content for user."""
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    user_profile = {
        "software_experience": current_user.software_experience,
        "hardware_experience": current_user.hardware_experience
    }
    
    personalized = rag_service.personalize_content(request.content, user_profile)
    
    # Save personalization
    personalization = ContentPersonalization(
        user_id=current_user.id,
        page_path=request.page_path,
        original_content=request.content,
        personalized_content=personalized,
        language="en"
    )
    db.add(personalization)
    db.commit()
    
    return {"personalized_content": personalized}


# Translation
@app.post("/api/translate")
async def translate_content(request: TranslateRequest):
    """Translate content to Urdu."""
    translated = rag_service.translate_to_urdu(request.content)
    return {"translated_content": translated}


# Admin: Ingest documents
@app.post("/api/admin/ingest")
async def ingest_documents(request: IngestDocumentsRequest):
    """Ingest documents into Qdrant (admin only)."""
    qdrant_service.add_documents(request.documents)
    return {
        "message": f"Successfully ingested {len(request.documents)} documents",
        "count": len(request.documents)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
