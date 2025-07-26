#!/usr/bin/env python3
"""
Multi-Level Ranking Engine for Adobe Hackathon Round 1B
Implements two-stage hierarchical analysis for section and sub-section relevance.
"""

import numpy as np
from typing import List, Dict, Any, Tuple
import re
from semantic_embedder import SemanticEmbedder

class RankingEngine:
    """Implements hierarchical ranking for document sections and sub-sections."""
    
    def __init__(self, embedder: SemanticEmbedder):
        """
        Initialize the ranking engine.
        
        Args:
            embedder: SemanticEmbedder instance for creating embeddings
        """
        self.embedder = embedder
    
    def rank_sections(self, sections: List[Dict[str, Any]], query_embedding: np.ndarray) -> List[Dict[str, Any]]:
        """
        Stage 1: Rank all sections by relevance to the query.
        
        Args:
            sections: List of section dictionaries
            query_embedding: Query embedding vector
            
        Returns:
            List of ranked sections with importance_rank
        """
        if not sections:
            return []
        
        print("🏆 Stage 1: Ranking sections by relevance...")
        
        try:
            # Create embeddings for all sections
            content_embeddings = self.embedder.create_content_embeddings(sections)
            
            # Compute similarities
            similarities = self.embedder.compute_cosine_similarities(query_embedding, content_embeddings)
            
            # Combine sections with their scores
            ranked_sections = []
            for i, section in enumerate(sections):
                ranked_section = section.copy()
                ranked_section['relevance_score'] = float(similarities[i])
                ranked_sections.append(ranked_section)
            
            # Sort by relevance score (descending)
            ranked_sections.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            # Add importance rank (1-indexed)
            for i, section in enumerate(ranked_sections):
                section['importance_rank'] = i + 1
            
            print(f"✅ Ranked {len(ranked_sections)} sections")
            top_scores = [f"{s['relevance_score']:.4f}" for s in ranked_sections[:3]]
            print(f"📊 Top 3 scores: {top_scores}")
            
            return ranked_sections
            
        except Exception as e:
            print(f"❌ Error ranking sections: {e}")
            raise
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into meaningful chunks for sub-section analysis.
        
        Args:
            text: Text to chunk
            
        Returns:
            List of text chunks
        """
        # Split by double newlines (paragraphs)
        chunks = re.split(r'\n\s*\n', text.strip())
        
        # Filter out empty chunks and very short chunks
        valid_chunks = []
        for chunk in chunks:
            chunk = chunk.strip()
            if len(chunk) > 50:  # Minimum meaningful length
                valid_chunks.append(chunk)
        
        # If no valid chunks found, split by single newlines
        if not valid_chunks:
            lines = text.split('\n')
            current_chunk = []
            for line in lines:
                line = line.strip()
                if line:
                    current_chunk.append(line)
                elif current_chunk:
                    chunk_text = ' '.join(current_chunk)
                    if len(chunk_text) > 50:
                        valid_chunks.append(chunk_text)
                    current_chunk = []
            
            # Add the last chunk if it exists
            if current_chunk:
                chunk_text = ' '.join(current_chunk)
                if len(chunk_text) > 50:
                    valid_chunks.append(chunk_text)
        
        return valid_chunks
    
    def analyze_sub_sections(self, top_sections: List[Dict[str, Any]], query_embedding: np.ndarray, 
                           max_sections: int = 20) -> List[Dict[str, Any]]:
        """
        Stage 2: Analyze sub-sections within top-ranked sections.
        
        Args:
            top_sections: Top-ranked sections from Stage 1
            query_embedding: Query embedding vector
            max_sections: Maximum number of top sections to analyze
            
        Returns:
            List of sub-section analysis results
        """
        if not top_sections:
            return []
        
        print(f"🔍 Stage 2: Analyzing sub-sections in top {min(max_sections, len(top_sections))} sections...")
        
        try:
            sub_section_results = []
            sections_to_analyze = top_sections[:max_sections]
            
            for section in sections_to_analyze:
                # Chunk the section content
                chunks = self.chunk_text(section['content_text'])
                
                if not chunks:
                    # If no valid chunks, use the original content
                    refined_text = section['content_text'][:500] + "..." if len(section['content_text']) > 500 else section['content_text']
                    sub_section_results.append({
                        'doc_name': section['doc_name'],
                        'page_number': section['page_num'],
                        'refined_text': refined_text
                    })
                    continue
                
                # Create embeddings for chunks
                chunk_embeddings = self.embedder.create_chunk_embeddings(chunks)
                
                # Compute similarities for chunks
                chunk_similarities = self.embedder.compute_cosine_similarities(query_embedding, chunk_embeddings)
                
                # Find the best chunk
                best_chunk_idx = np.argmax(chunk_similarities)
                best_chunk = chunks[best_chunk_idx]
                best_score = chunk_similarities[best_chunk_idx]
                
                # Create refined text (limit length for output)
                refined_text = best_chunk
                if len(refined_text) > 1000:
                    refined_text = refined_text[:1000] + "..."
                
                sub_section_results.append({
                    'doc_name': section['doc_name'],
                    'page_number': section['page_num'],
                    'refined_text': refined_text,
                    'chunk_score': float(best_score)
                })
            
            print(f"✅ Analyzed sub-sections for {len(sub_section_results)} sections")
            
            return sub_section_results
            
        except Exception as e:
            print(f"❌ Error analyzing sub-sections: {e}")
            raise
    
    def get_top_sections_for_output(self, ranked_sections: List[Dict[str, Any]], 
                                  max_sections: int = 50) -> List[Dict[str, Any]]:
        """
        Get top sections formatted for JSON output.
        
        Args:
            ranked_sections: All ranked sections
            max_sections: Maximum number of sections to include
            
        Returns:
            List of sections formatted for output
        """
        top_sections = ranked_sections[:max_sections]
        
        output_sections = []
        for section in top_sections:
            output_section = {
                'document': section['doc_name'],
                'page_number': section['page_num'],
                'section_title': section['heading_text'],
                'importance_rank': section['importance_rank']
            }
            output_sections.append(output_section)
        
        return output_sections
    
    def get_sub_section_analysis_for_output(self, sub_section_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format sub-section analysis results for JSON output.
        
        Args:
            sub_section_results: Results from sub-section analysis
            
        Returns:
            List of sub-section analysis formatted for output
        """
        output_analysis = []
        for result in sub_section_results:
            output_item = {
                'document': result['doc_name'],
                'page_number': result['page_number'],
                'refined_text': result['refined_text']
            }
            output_analysis.append(output_item)
        
        return output_analysis

def main():
    """Test the ranking engine."""
    from semantic_embedder import SemanticEmbedder
    
    # Initialize embedder
    embedder = SemanticEmbedder()
    ranking_engine = RankingEngine(embedder)
    
    # Test data
    persona = "investment analyst"
    jbtd = "analyze market trends and identify investment opportunities"
    
    # Create query embedding
    query_emb = embedder.create_query_embedding(persona, jbtd)
    
    # Sample sections
    sample_sections = [
        {
            'doc_name': 'sample1.pdf',
            'heading_text': 'Market Analysis',
            'page_num': 1,
            'content_text': 'This section discusses market trends and analysis methods. The market has shown significant growth in recent quarters. Investment opportunities are abundant in the technology sector.'
        },
        {
            'doc_name': 'sample2.pdf',
            'heading_text': 'Investment Strategies',
            'page_num': 5,
            'content_text': 'Various investment strategies are explored here. Long-term investments provide better returns. Risk management is crucial for success.'
        }
    ]
    
    # Rank sections
    ranked_sections = ranking_engine.rank_sections(sample_sections, query_emb)
    
    # Analyze sub-sections
    sub_section_results = ranking_engine.analyze_sub_sections(ranked_sections, query_emb)
    
    print("Ranking test completed successfully!")

if __name__ == "__main__":
    main() 