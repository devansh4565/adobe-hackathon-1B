# Approach Explanation: Persona-Driven Document Intelligence

## Methodology Overview

Our solution implements a four-stage modular pipeline that transforms the structural understanding from Round 1A into semantic intelligence for multi-document analysis. The system is designed to understand user intent through persona and job-to-be-done definitions, then intelligently rank and extract the most relevant content from document collections.

## Stage 1: Content Segmentation
Building upon Round 1A's structural outlines, we extract full text content for each identified heading using PyMuPDF's advanced text extraction capabilities. Our algorithm defines content boundaries by locating heading coordinates and extracting all text within the "stripe" between consecutive headings. This approach handles multi-page sections, edge cases, and maintains document hierarchy while providing complete content for semantic analysis.

## Stage 2: Semantic Embedding
We employ the all-MiniLM-L6-v2 model (~90MB) for its optimal balance of size, speed, and performance. The model converts user persona and job-to-be-done into a unified query embedding, while simultaneously encoding all document sections into high-dimensional vectors. This semantic representation enables understanding beyond keyword matching, capturing contextual meaning and domain-specific terminology.

## Stage 3: Multi-Level Ranking
Our hierarchical analysis directly addresses the scoring criteria through a two-stage approach:

**Stage 3a - Section Relevance (60 points):** Global ranking of all sections across the document collection using cosine similarity between query and section embeddings. This identifies the most relevant high-level sections for the user's specific needs.

**Stage 3b - Sub-Section Relevance (40 points):** Granular analysis within top-ranked sections by chunking content into meaningful paragraphs and re-ranking these chunks against the original query. This extracts the most potent, concise information nuggets.

## Stage 4: Output Synthesis
The final stage meticulously formats results into the required JSON structure, ensuring strict compliance with the challenge specifications while providing comprehensive metadata for transparency and debugging.

## Key Innovations

**Hierarchical Intelligence:** Unlike flat search approaches, our two-stage ranking preserves document context while identifying specific relevant content, directly mapping to the scoring criteria.

**Semantic Understanding:** The embedding-based approach handles synonyms, paraphrasing, and domain-specific terminology, making the solution robust across diverse document types and user personas.

**Performance Optimization:** Batch processing, vectorized operations, and efficient memory management ensure compliance with the 60-second execution limit while maintaining accuracy.

**Offline Operation:** Complete offline capability through pre-downloaded model packaging, ensuring reliable execution in constrained environments.

## Technical Implementation

The system leverages PyMuPDF for robust PDF processing, sentence-transformers for semantic embeddings, and NumPy for efficient similarity calculations. The modular design enables independent optimization of each component while maintaining clear data flow between stages. Error handling and graceful degradation ensure robust operation across diverse input scenarios.

This approach successfully bridges the gap between structural document understanding and semantic intelligence, providing users with contextually relevant, ranked content that directly addresses their specific needs and expertise areas. 