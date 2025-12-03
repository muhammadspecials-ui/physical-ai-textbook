from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from openai import OpenAI
from config import settings
from typing import List, Dict
import uuid


class QdrantService:
    """Service for managing Qdrant vector database operations."""
    
    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key
        )
        self.openai_client = OpenAI(api_key=settings.openai_api_key)
        self.collection_name = settings.qdrant_collection_name
        
    def create_collection(self):
        """Create Qdrant collection if it doesn't exist."""
        try:
            self.client.get_collection(self.collection_name)
            print(f"Collection '{self.collection_name}' already exists")
        except:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=settings.embedding_dimension,
                    distance=Distance.COSINE
                )
            )
            print(f"Created collection '{self.collection_name}'")
    
    def get_embedding(self, text: str) -> List[float]:
        """Generate embedding using OpenAI."""
        response = self.openai_client.embeddings.create(
            model=settings.embedding_model,
            input=text
        )
        return response.data[0].embedding
    
    def add_documents(self, documents: List[Dict[str, str]]):
        """
        Add documents to Qdrant.
        documents: [{"text": "...", "metadata": {...}}, ...]
        """
        points = []
        for doc in documents:
            embedding = self.get_embedding(doc["text"])
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "text": doc["text"],
                    **doc.get("metadata", {})
                }
            )
            points.append(point)
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        print(f"Added {len(points)} documents to Qdrant")
    
    def search(self, query: str, limit: int = 5) -> List[Dict]:
        """Search for similar documents."""
        query_embedding = self.get_embedding(query)
        
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=limit
        )
        
        return [
            {
                "text": hit.payload["text"],
                "score": hit.score,
                "metadata": {k: v for k, v in hit.payload.items() if k != "text"}
            }
            for hit in results.points
        ]
    
    def search_selected_text(self, selected_text: str, query: str, limit: int = 3) -> List[Dict]:
        """Search within selected text context."""
        # First, find chunks related to the selected text
        selected_embedding = self.get_embedding(selected_text)
        
        # Get chunks similar to selected text
        context_results = self.client.search(
            collection_name=self.collection_name,
            query_vector=selected_embedding,
            limit=10
        )
        
        # Filter and re-rank based on the actual query
        query_embedding = self.get_embedding(query)
        filtered_results = []
        
        for hit in context_results:
            # Simple relevance check: if selected text is in the chunk
            if selected_text.lower() in hit.payload["text"].lower():
                filtered_results.append({
                    "text": hit.payload["text"],
                    "score": hit.score,
                    "metadata": {k: v for k, v in hit.payload.items() if k != "text"}
                })
        
        return filtered_results[:limit]


# Global instance
qdrant_service = QdrantService()
