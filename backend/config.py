from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    
    # Qdrant
    qdrant_url: str
    qdrant_api_key: Optional[str] = None
    qdrant_collection_name: str = "physical_ai_textbook"
    
    # Neon Database
    database_url: str
    
    # Auth
    auth_secret: str
    auth_url: str = "http://localhost:8000"
    
    # CORS
    frontend_url: str = "http://localhost:3000"
    
    # Embedding
    embedding_model: str = "text-embedding-3-small"
    embedding_dimension: int = 1536
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
