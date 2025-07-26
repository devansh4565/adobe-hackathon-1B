#!/usr/bin/env python3
"""
Semantic Embedding Module for Adobe Hackathon Round 1B
Converts text to semantic vectors using all-MiniLM-L6-v2 model for offline use.
"""

import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Tuple
import os
import time

class SemanticEmbedder:
    """Handles semantic embedding of text using sentence transformers."""
    
    def __init__(self, model_path: str = "./local_model"):
        """
        Initialize the semantic embedder with a local model.
        
        Args:
            model_path: Path to the locally saved sentence transformer model
        """
        self.model_path = model_path
        self.model = None
        self.model_info = {}
        self._load_model()
    
    def _load_model(self):
        """Load the sentence transformer model from local path."""
        try:
            print(f"Loading model from: {self.model_path}")
            start_time = time.time()
            
            # Load model with local_files_only=True to ensure offline operation
            self.model = SentenceTransformer(self.model_path, local_files_only=True)
            
            load_time = time.time() - start_time
            print(f"✅ Model loaded successfully in {load_time:.2f} seconds")
            
            # Get model information
            self.model_info = {
                'max_seq_length': self.model.max_seq_length,
                'embedding_dimension': self.model.get_sentence_embedding_dimension(),
                'model_name': os.path.basename(self.model_path)
            }
            
            print(f"📊 Model Info: {self.model_info}")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise
    
    def create_query_embedding(self, persona_text: str, jbtd_text: str) -> np.ndarray:
        """
        Create a unified query embedding from persona and job-to-be-done.
        
        Args:
            persona_text: The user persona description
            jbtd_text: The job-to-be-done description
            
        Returns:
            Query embedding vector
        """
        # Combine persona and JBTD into a unified query
        query_text = f"As a {persona_text}, my primary objective is to {jbtd_text}."
        
        print(f"🔍 Creating query embedding for: {query_text[:100]}...")
        
        try:
            # Encode the query
            query_embedding = self.model.encode(query_text, convert_to_numpy=True)
            print(f"✅ Query embedding created: {query_embedding.shape}")
            return query_embedding
            
        except Exception as e:
            print(f"❌ Error creating query embedding: {e}")
            raise
    
    def create_content_embeddings(self, sections: List[Dict[str, Any]], batch_size: int = 32) -> np.ndarray:
        """
        Create embeddings for all content sections in batches.
        
        Args:
            sections: List of section dictionaries with 'content_text' field
            batch_size: Batch size for processing
            
        Returns:
            Matrix of content embeddings
        """
        if not sections:
            return np.array([])
        
        # Extract content texts
        content_texts = [section['content_text'] for section in sections]
        
        print(f"📚 Creating embeddings for {len(content_texts)} sections...")
        start_time = time.time()
        
        try:
            # Encode all content in batches
            content_embeddings = self.model.encode(
                content_texts, 
                batch_size=batch_size,
                convert_to_numpy=True,
                show_progress_bar=True
            )
            
            processing_time = time.time() - start_time
            print(f"✅ Content embeddings created in {processing_time:.2f} seconds")
            print(f"📊 Embedding matrix shape: {content_embeddings.shape}")
            
            return content_embeddings
            
        except Exception as e:
            print(f"❌ Error creating content embeddings: {e}")
            raise
    
    def create_chunk_embeddings(self, chunks: List[str], batch_size: int = 32) -> np.ndarray:
        """
        Create embeddings for text chunks (for sub-section analysis).
        
        Args:
            chunks: List of text chunks
            batch_size: Batch size for processing
            
        Returns:
            Matrix of chunk embeddings
        """
        if not chunks:
            return np.array([])
        
        print(f"🔍 Creating embeddings for {len(chunks)} chunks...")
        start_time = time.time()
        
        try:
            # Encode all chunks in batches
            chunk_embeddings = self.model.encode(
                chunks, 
                batch_size=batch_size,
                convert_to_numpy=True,
                show_progress_bar=True
            )
            
            processing_time = time.time() - start_time
            print(f"✅ Chunk embeddings created in {processing_time:.2f} seconds")
            print(f"📊 Chunk embedding matrix shape: {chunk_embeddings.shape}")
            
            return chunk_embeddings
            
        except Exception as e:
            print(f"❌ Error creating chunk embeddings: {e}")
            raise
    
    def compute_cosine_similarities(self, query_embedding: np.ndarray, content_embeddings: np.ndarray) -> np.ndarray:
        """
        Compute cosine similarities between query and all content embeddings.
        
        Args:
            query_embedding: Single query embedding vector
            content_embeddings: Matrix of content embeddings
            
        Returns:
            Array of cosine similarity scores
        """
        if content_embeddings.size == 0:
            return np.array([])
        
        print("🧮 Computing cosine similarities...")
        start_time = time.time()
        
        try:
            # Normalize vectors for cosine similarity
            query_norm = np.linalg.norm(query_embedding)
            content_norms = np.linalg.norm(content_embeddings, axis=1)
            
            # Compute dot products
            dot_products = np.dot(content_embeddings, query_embedding)
            
            # Compute cosine similarities
            similarities = dot_products / (content_norms * query_norm)
            
            # Handle any NaN values (shouldn't occur with normalized vectors)
            similarities = np.nan_to_num(similarities, nan=0.0)
            
            computation_time = time.time() - start_time
            print(f"✅ Similarities computed in {computation_time:.4f} seconds")
            print(f"📊 Similarity scores range: {similarities.min():.4f} to {similarities.max():.4f}")
            
            return similarities
            
        except Exception as e:
            print(f"❌ Error computing similarities: {e}")
            raise
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        return self.model_info.copy()

def main():
    """Test the semantic embedder."""
    embedder = SemanticEmbedder()
    
    # Test with sample data
    persona = "investment analyst"
    jbtd = "analyze market trends and identify investment opportunities"
    
    # Create query embedding
    query_emb = embedder.create_query_embedding(persona, jbtd)
    
    # Test with sample content
    sample_sections = [
        {"content_text": "This is a sample section about market analysis."},
        {"content_text": "Another section discussing investment strategies."},
        {"content_text": "A third section about risk management."}
    ]
    
    # Create content embeddings
    content_embs = embedder.create_content_embeddings(sample_sections)
    
    # Compute similarities
    similarities = embedder.compute_cosine_similarities(query_emb, content_embs)
    
    print(f"Sample similarities: {similarities}")

if __name__ == "__main__":
    main() 