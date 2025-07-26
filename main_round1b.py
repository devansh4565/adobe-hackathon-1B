#!/usr/bin/env python3
"""
Main Orchestration Module for Adobe Hackathon Round 1B
Implements the complete four-stage pipeline for persona-driven document intelligence.
"""

import os
import json
import time
import argparse
import numpy as np
from typing import List, Dict, Any
from datetime import datetime

from content_segmenter import ContentSegmenter
from semantic_embedder import SemanticEmbedder
from ranking_engine import RankingEngine

class PersonaDrivenDocumentIntelligence:
    """Main orchestrator for the persona-driven document intelligence system."""
    
    def __init__(self, model_path: str = "./local_model"):
        """
        Initialize the system with all components.
        
        Args:
            model_path: Path to the locally saved sentence transformer model
        """
        print("🚀 Initializing Persona-Driven Document Intelligence System...")
        
        # Initialize components
        self.content_segmenter = ContentSegmenter()
        self.semantic_embedder = SemanticEmbedder(model_path)
        self.ranking_engine = RankingEngine(self.semantic_embedder)
        
        print("✅ System initialized successfully!")
    
    def get_persona_and_jbtd(self, persona: str = None, jbtd: str = None, input_dir: str = None) -> Dict[str, str]:
        """
        Get persona and job-to-be-done from multiple sources in priority order:
        1. Command line arguments/function parameters
        2. Environment variables
        3. Input files (for backward compatibility)
        4. Default values
        
        Args:
            persona: Persona text from command line
            jbtd: Job-to-be-done text from command line
            input_dir: Directory to check for input files (fallback)
            
        Returns:
            Dictionary with persona and jbtd text
        """
        print("📁 Getting persona and job-to-be-done...")
        
        persona_text = ""
        jbtd_text = ""
        
        try:
            # Priority 1: Use provided parameters (command line args)
            if persona and persona.strip():
                persona_text = persona.strip()
                print(f"✅ Using persona from command line: {persona_text[:100]}...")
            elif os.getenv('PERSONA'):
                # Priority 2: Environment variables
                persona_text = os.getenv('PERSONA').strip()
                print(f"✅ Using persona from environment: {persona_text[:100]}...")
            elif input_dir:
                # Priority 3: Try to read from files (backward compatibility)
                persona_files = ["persona.txt", "persona", "user_persona.txt"]
                for persona_file in persona_files:
                    persona_path = os.path.join(input_dir, persona_file)
                    if os.path.exists(persona_path):
                        with open(persona_path, 'r', encoding='utf-8') as f:
                            persona_text = f.read().strip()
                        print(f"✅ Read persona from {persona_file}: {persona_text[:100]}...")
                        break
            
            if not persona_text:
                # Priority 4: Default value
                persona_text = "document analyst"
                print("⚠️  Using default persona: document analyst")
            
            # Same priority order for job-to-be-done
            if jbtd and jbtd.strip():
                jbtd_text = jbtd.strip()
                print(f"✅ Using JBTD from command line: {jbtd_text[:100]}...")
            elif os.getenv('JBTD') or os.getenv('JOB_TO_BE_DONE'):
                jbtd_text = (os.getenv('JBTD') or os.getenv('JOB_TO_BE_DONE')).strip()
                print(f"✅ Using JBTD from environment: {jbtd_text[:100]}...")
            elif input_dir:
                jbtd_files = ["job_to_be_done.txt", "job_to_be_done", "task.txt", "objective.txt"]
                for jbtd_file in jbtd_files:
                    jbtd_path = os.path.join(input_dir, jbtd_file)
                    if os.path.exists(jbtd_path):
                        with open(jbtd_path, 'r', encoding='utf-8') as f:
                            jbtd_text = f.read().strip()
                        print(f"✅ Read JBTD from {jbtd_file}: {jbtd_text[:100]}...")
                        break
            
            if not jbtd_text:
                jbtd_text = "extract relevant information from documents"
                print("⚠️  Using default JBTD: extract relevant information from documents")
            
            return {
                'persona': persona_text,
                'jbtd': jbtd_text
            }
            
        except Exception as e:
            print(f"❌ Error getting persona and JBTD: {e}")
            # Return defaults on error
            return {
                'persona': "document analyst",
                'jbtd': "extract relevant information from documents"
            }
    
    def process_documents(self, input_dir: str, output_dir: str) -> List[Dict[str, Any]]:
        """
        Stage 1: Process all PDF documents and extract section content.
        
        Args:
            input_dir: Directory containing PDF files
            output_dir: Directory containing Round 1A outlines
            
        Returns:
            List of all extracted sections from all documents
        """
        print("📚 Stage 1: Processing documents and extracting content...")
        
        all_sections = []
        
        try:
            # Get all PDF files
            pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
            print(f"📄 Found {len(pdf_files)} PDF files")
            
            for pdf_file in pdf_files:
                pdf_path = os.path.join(input_dir, pdf_file)
                
                # Try different possible outline file names
                outline_candidates = [
                    os.path.join(output_dir, os.path.splitext(pdf_file)[0] + ".json"),
                    os.path.join(output_dir, pdf_file + ".json"),
                    os.path.join(input_dir, os.path.splitext(pdf_file)[0] + ".json"),
                    os.path.join(input_dir, pdf_file + ".json")
                ]
                
                outline_path = None
                for candidate in outline_candidates:
                    if os.path.exists(candidate):
                        outline_path = candidate
                        break
                
                print(f"🔍 Processing {pdf_file}...")
                
                if outline_path:
                    # Extract content using Round 1A outline
                    sections = self.content_segmenter.process_document(pdf_path, outline_path)
                    all_sections.extend(sections)
                    print(f"✅ Extracted {len(sections)} sections from {pdf_file}")
                else:
                    print(f"⚠️  No outline found for {pdf_file}, attempting to generate outline...")
                    # Try to generate outline using Round 1A approach
                    try:
                        from main import process_pdf
                        outline_data = process_pdf(pdf_path)
                        outline_path = os.path.join(output_dir, os.path.splitext(pdf_file)[0] + ".json")
                        with open(outline_path, 'w', encoding='utf-8') as f:
                            json.dump(outline_data, f, indent=2, ensure_ascii=False)
                        
                        # Now extract content
                        sections = self.content_segmenter.process_document(pdf_path, outline_path)
                        all_sections.extend(sections)
                        print(f"✅ Generated outline and extracted {len(sections)} sections from {pdf_file}")
                    except Exception as e:
                        print(f"❌ Failed to generate outline for {pdf_file}: {e}")
            
            print(f"📊 Total sections extracted: {len(all_sections)}")
            return all_sections
            
        except Exception as e:
            print(f"❌ Error processing documents: {e}")
            raise
    
    def create_semantic_embeddings(self, sections: List[Dict[str, Any]], 
                                 persona_text: str, jbtd_text: str) -> tuple:
        """
        Stage 2: Create semantic embeddings for query and content.
        
        Args:
            sections: List of extracted sections
            persona_text: User persona description
            jbtd_text: Job-to-be-done description
            
        Returns:
            Tuple of (query_embedding, content_embeddings)
        """
        print("🧠 Stage 2: Creating semantic embeddings...")
        
        try:
            # Create query embedding
            query_embedding = self.semantic_embedder.create_query_embedding(persona_text, jbtd_text)
            
            # Create content embeddings
            content_embeddings = self.semantic_embedder.create_content_embeddings(sections)
            
            return query_embedding, content_embeddings
            
        except Exception as e:
            print(f"❌ Error creating embeddings: {e}")
            raise
    
    def perform_ranking_analysis(self, sections: List[Dict[str, Any]], 
                               query_embedding: np.ndarray) -> tuple:
        """
        Stage 3: Perform multi-level ranking analysis.
        
        Args:
            sections: List of extracted sections
            query_embedding: Query embedding vector
            
        Returns:
            Tuple of (ranked_sections, sub_section_results)
        """
        print("🏆 Stage 3: Performing ranking analysis...")
        
        try:
            # Stage 1: Rank all sections
            ranked_sections = self.ranking_engine.rank_sections(sections, query_embedding)
            
            # Stage 2: Analyze sub-sections
            sub_section_results = self.ranking_engine.analyze_sub_sections(ranked_sections, query_embedding)
            
            return ranked_sections, sub_section_results
            
        except Exception as e:
            print(f"❌ Error performing ranking analysis: {e}")
            raise
    
    def generate_output_json(self, ranked_sections: List[Dict[str, Any]], 
                           sub_section_results: List[Dict[str, Any]],
                           persona_text: str, jbtd_text: str,
                           input_files: List[str]) -> Dict[str, Any]:
        """
        Stage 4: Generate the final JSON output.
        
        Args:
            ranked_sections: Ranked sections from Stage 1
            sub_section_results: Sub-section analysis results
            persona_text: User persona description
            jbtd_text: Job-to-be-done description
            input_files: List of input PDF filenames
            
        Returns:
            Complete JSON output structure
        """
        print("📝 Stage 4: Generating output JSON...")
        
        try:
            # Format sections for output
            output_sections = self.ranking_engine.get_top_sections_for_output(ranked_sections)
            output_analysis = self.ranking_engine.get_sub_section_analysis_for_output(sub_section_results)
            
            # Create the complete output structure
            output = {
                "metadata": {
                    "input_documents": input_files,
                    "persona": persona_text,
                    "job_to_be_done": jbtd_text,
                    "processing_timestamp": datetime.now().isoformat(),
                    "model_info": self.semantic_embedder.get_model_info()
                },
                "extracted_sections": output_sections,
                "subsection_analysis": output_analysis
            }
            
            print(f"✅ Generated output with {len(output_sections)} sections and {len(output_analysis)} sub-sections")
            return output
            
        except Exception as e:
            print(f"❌ Error generating output: {e}")
            raise
    
    def run_pipeline(self, input_dir: str, output_dir: str, persona: str = None, jbtd: str = None) -> Dict[str, Any]:
        """
        Run the complete four-stage pipeline.
        
        Args:
            input_dir: Directory containing input files
            output_dir: Directory for output files
            persona: Persona description (optional - will try multiple sources)
            jbtd: Job-to-be-done description (optional - will try multiple sources)
            
        Returns:
            Complete analysis results
        """
        start_time = time.time()
        print("🎯 Starting Persona-Driven Document Intelligence Pipeline...")
        
        try:
            # Get persona and job-to-be-done from multiple sources
            input_data = self.get_persona_and_jbtd(persona, jbtd, input_dir)
            persona_text = input_data['persona']
            jbtd_text = input_data['jbtd']
            
            # Get list of PDF files
            pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
            
            # Stage 1: Process documents
            sections = self.process_documents(input_dir, output_dir)
            
            if not sections:
                print("⚠️  No sections extracted, creating minimal output")
                return self.generate_output_json([], [], persona_text, jbtd_text, pdf_files)
            
            # Stage 2: Create embeddings
            query_embedding, _ = self.create_semantic_embeddings(sections, persona_text, jbtd_text)
            
            # Stage 3: Perform ranking
            ranked_sections, sub_section_results = self.perform_ranking_analysis(sections, query_embedding)
            
            # Stage 4: Generate output
            output = self.generate_output_json(ranked_sections, sub_section_results, 
                                             persona_text, jbtd_text, pdf_files)
            
            total_time = time.time() - start_time
            print(f"🎉 Pipeline completed successfully in {total_time:.2f} seconds!")
            
            return output
            
        except Exception as e:
            print(f"❌ Pipeline failed: {e}")
            raise

def main():
    """Main execution function."""
    import numpy as np
    
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(
        description="Adobe Hackathon Round 1B: Persona-Driven Document Intelligence",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Using command line arguments
  python main_round1b.py --persona "PhD Researcher in Biology" --jbtd "Prepare literature review"
  
  # Using environment variables
  export PERSONA="Investment Analyst"
  export JBTD="Analyze revenue trends and market positioning"
  python main_round1b.py
  
  # Using default values (will also check for input files)
  python main_round1b.py
        """
    )
    
    parser.add_argument(
        '--persona', '-p',
        type=str,
        default=None,
        help='User persona description (e.g., "PhD Researcher in Computational Biology")'
    )
    
    parser.add_argument(
        '--jbtd', '--job-to-be-done', '-j',
        type=str,
        default=None,
        help='Job-to-be-done description (e.g., "Prepare comprehensive literature review")'
    )
    
    parser.add_argument(
        '--input-dir', '-i',
        type=str,
        default=None,
        help='Input directory path (default: ./input for local, /input for Docker)'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        type=str,
        default=None,
        help='Output directory path (default: ./output for local, /output for Docker)'
    )
    
    args = parser.parse_args()
    
    # Configuration - use relative paths for local testing, absolute for Docker
    current_dir = os.getcwd()
    if args.input_dir:
        INPUT_DIR = args.input_dir
    elif current_dir.startswith("/") or current_dir.startswith("C:"):
        # Local environment
        INPUT_DIR = "./input"
    else:
        # Docker environment
        INPUT_DIR = "/input"
    
    if args.output_dir:
        OUTPUT_DIR = args.output_dir
    elif current_dir.startswith("/") or current_dir.startswith("C:"):
        # Local environment
        OUTPUT_DIR = "./output"
    else:
        # Docker environment
        OUTPUT_DIR = "/output"
    
    # Print configuration
    print("🔧 Configuration:")
    print(f"   Input Directory: {INPUT_DIR}")
    print(f"   Output Directory: {OUTPUT_DIR}")
    if args.persona:
        print(f"   Persona: {args.persona}")
    if args.jbtd:
        print(f"   Job-to-be-Done: {args.jbtd}")
    print()
    
    try:
        # Create output directory
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # Initialize the system
        system = PersonaDrivenDocumentIntelligence()
        
        # Run the pipeline with persona and jbtd arguments
        results = system.run_pipeline(INPUT_DIR, OUTPUT_DIR, args.persona, args.jbtd)
        
        # Save results
        output_path = os.path.join(OUTPUT_DIR, "output.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Results saved to {output_path}")
        
    except Exception as e:
        print(f"❌ Execution failed: {e}")
        # Create minimal output on failure
        try:
            minimal_output = {
                "metadata": {
                    "input_documents": [],
                    "persona": args.persona or os.getenv('PERSONA', 'document analyst'),
                    "job_to_be_done": args.jbtd or os.getenv('JBTD', 'extract relevant information'),
                    "processing_timestamp": datetime.now().isoformat(),
                    "error": str(e)
                },
                "extracted_sections": [],
                "subsection_analysis": []
            }
            
            output_path = os.path.join(OUTPUT_DIR, "output.json")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(minimal_output, f, indent=2, ensure_ascii=False)
            
            print(f"⚠️  Minimal output saved to {output_path}")
            
        except Exception as save_error:
            print(f"❌ Failed to save minimal output: {save_error}")

if __name__ == "__main__":
    main() 