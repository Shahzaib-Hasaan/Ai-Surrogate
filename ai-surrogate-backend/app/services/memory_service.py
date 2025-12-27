"""
Memory Service

Handles conversation memory using vector embeddings and semantic search.
Uses ChromaDB for vector storage and sentence-transformers for embeddings.
"""

import os
from typing import List, Dict, Optional
import chromadb
from sentence_transformers import SentenceTransformer
from datetime import datetime
import json

class MemoryService:
    def __init__(self):
        """Initialize the memory service with ChromaDB and embedding model."""
        # Initialize ChromaDB client with new API
        self.client = chromadb.PersistentClient(path="./chroma_db")
        
        # Create or get collection for conversations
        self.collection = self.client.get_or_create_collection(
            name="conversations",
            metadata={"description": "User conversation history"}
        )
        
        # Initialize embedding model (lightweight, fast)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for text."""
        embedding = self.embedding_model.encode(text)
        return embedding.tolist()
    
    def save_conversation(
        self,
        user_id: str,
        conversation_id: str,
        user_message: str,
        ai_response: str,
        metadata: Optional[Dict] = None
    ) -> None:
        """
        Save a conversation turn to vector database.
        
        Args:
            user_id: User identifier
            conversation_id: Conversation identifier
            user_message: User's message
            ai_response: AI's response
            metadata: Additional metadata
        """
        # Combine user message and AI response for context
        combined_text = f"User: {user_message}\nAI: {ai_response}"
        
        # Generate embedding
        embedding = self.embed_text(combined_text)
        
        # Prepare metadata
        meta = {
            "user_id": user_id,
            "conversation_id": conversation_id,
            "user_message": user_message,
            "ai_response": ai_response,
            "timestamp": datetime.utcnow().isoformat(),
            **(metadata or {})
        }
        
        # Create unique ID
        doc_id = f"{conversation_id}_{datetime.utcnow().timestamp()}"
        
        # Add to collection
        self.collection.add(
            embeddings=[embedding],
            documents=[combined_text],
            metadatas=[meta],
            ids=[doc_id]
        )
    
    def recall_relevant_memories(
        self,
        user_id: str,
        query: str,
        n_results: int = 5
    ) -> List[Dict]:
        """
        Retrieve relevant past conversations using semantic search.
        
        Args:
            user_id: User identifier
            query: Current query to find relevant context
            n_results: Number of results to return
            
        Returns:
            List of relevant conversation memories
        """
        # Generate query embedding
        query_embedding = self.embed_text(query)
        
        # Search for similar conversations
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where={"user_id": user_id}
        )
        
        # Format results
        memories = []
        if results['metadatas'] and len(results['metadatas'][0]) > 0:
            for i, metadata in enumerate(results['metadatas'][0]):
                memory = {
                    "user_message": metadata.get("user_message", ""),
                    "ai_response": metadata.get("ai_response", ""),
                    "timestamp": metadata.get("timestamp", ""),
                    "relevance_score": 1 - results['distances'][0][i] if results['distances'] else 0
                }
                memories.append(memory)
        
        return memories
    
    def get_conversation_summary(
        self,
        user_id: str,
        conversation_id: str
    ) -> str:
        """
        Get a summary of a specific conversation.
        
        Args:
            user_id: User identifier
            conversation_id: Conversation identifier
            
        Returns:
            Summary of the conversation
        """
        # Query all messages from this conversation
        results = self.collection.get(
            where={
                "user_id": user_id,
                "conversation_id": conversation_id
            }
        )
        
        if not results['metadatas']:
            return "No conversation history found."
        
        # Build summary
        messages = []
        for metadata in results['metadatas']:
            messages.append({
                "user": metadata.get("user_message", ""),
                "ai": metadata.get("ai_response", ""),
                "time": metadata.get("timestamp", "")
            })
        
        # Sort by timestamp
        messages.sort(key=lambda x: x['time'])
        
        # Create summary
        summary = f"Conversation with {len(messages)} exchanges:\n"
        for msg in messages[:3]:  # Show first 3
            summary += f"- User asked about: {msg['user'][:50]}...\n"
        
        return summary
    
    def delete_user_memories(self, user_id: str) -> None:
        """Delete all memories for a user."""
        # Get all IDs for this user
        results = self.collection.get(
            where={"user_id": user_id}
        )
        
        if results['ids']:
            self.collection.delete(ids=results['ids'])


# Global instance
memory_service = MemoryService()
