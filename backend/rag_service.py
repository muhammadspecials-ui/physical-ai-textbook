from openai import OpenAI
from qdrant_service import qdrant_service
from config import settings
from typing import List, Dict, Optional


class RAGService:
    """Service for Retrieval-Augmented Generation."""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
    
    def generate_answer(
        self,
        question: str,
        context_chunks: List[Dict],
        user_profile: Optional[Dict] = None
    ) -> str:
        """Generate answer using RAG."""
        
        # Build context from retrieved chunks
        context = "\n\n".join([
            f"[Source: {chunk['metadata'].get('source', 'Unknown')}]\n{chunk['text']}"
            for chunk in context_chunks
        ])
        
        # Build system prompt with user profile
        system_prompt = "You are an expert AI assistant for a Physical AI & Humanoid Robotics textbook."
        
        if user_profile:
            sw_exp = user_profile.get('software_experience', 'intermediate')
            hw_exp = user_profile.get('hardware_experience', 'intermediate')
            system_prompt += f"\n\nThe user has {sw_exp} software experience and {hw_exp} hardware experience. Tailor your explanations accordingly."
        
        # Build user prompt
        user_prompt = f"""Based on the following context from the textbook, answer the question.

Context:
{context}

Question: {question}

Provide a clear, comprehensive answer based on the context. If the context doesn't contain enough information, say so."""
        
        # Generate response
        response = self.client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    
    def answer_question(
        self,
        question: str,
        selected_text: Optional[str] = None,
        user_profile: Optional[Dict] = None
    ) -> Dict:
        """Answer a question using RAG."""
        
        # Search for relevant context
        if selected_text:
            context_chunks = qdrant_service.search_selected_text(selected_text, question)
        else:
            context_chunks = qdrant_service.search(question, limit=5)
        
        # Generate answer
        answer = self.generate_answer(question, context_chunks, user_profile)
        
        return {
            "answer": answer,
            "sources": [
                {
                    "text": chunk["text"][:200] + "...",
                    "score": chunk["score"],
                    "metadata": chunk["metadata"]
                }
                for chunk in context_chunks
            ]
        }
    
    def personalize_content(
        self,
        content: str,
        user_profile: Dict
    ) -> str:
        """Personalize content based on user profile."""
        
        sw_exp = user_profile.get('software_experience', 'intermediate')
        hw_exp = user_profile.get('hardware_experience', 'intermediate')
        
        prompt = f"""Rewrite the following educational content to match the reader's experience level:
- Software Experience: {sw_exp}
- Hardware Experience: {hw_exp}

Original Content:
{content}

Rewrite the content to be appropriate for this experience level. Adjust technical depth, add or remove explanations, and modify examples as needed. Keep the same structure and main points."""
        
        response = self.client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": "You are an expert educational content adapter."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    
    def translate_to_urdu(self, content: str) -> str:
        """Translate content to Urdu."""
        
        prompt = f"""Translate the following educational content to Urdu. Maintain technical terms in English where appropriate, but provide Urdu explanations.

Content:
{content}

Provide a natural, educational translation in Urdu."""
        
        response = self.client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": "You are an expert translator specializing in technical educational content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=2000
        )
        
        return response.choices[0].message.content


rag_service = RAGService()
