# Adobe India Hackathon 2025 - Round 1B: Persona-Driven Document Intelligence

## 🎯 Overview

This repository contains a comprehensive solution for the Adobe India Hackathon 2025 Round 1B challenge: **Persona-Driven Document Intelligence**. The system implements a four-stage modular pipeline that extends the Round 1A structural analysis capabilities to provide semantic intelligence for multi-document analysis.

## 🏗️ System Architecture

The solution follows a modular, four-stage pipeline design:

### Stage 1: Content Segmentation
- **Module**: `content_segmenter.py`
- **Purpose**: Extracts full text content for each heading identified in Round 1A outlines
- **Input**: PDF files + Round 1A JSON outlines
- **Output**: Structured list of sections with full content

### Stage 2: Semantic Embedding
- **Module**: `semantic_embedder.py`
- **Purpose**: Converts text to semantic vectors using all-MiniLM-L6-v2 model
- **Input**: User persona, job-to-be-done, and document content
- **Output**: High-dimensional numerical representations

### Stage 3: Multi-Level Ranking
- **Module**: `ranking_engine.py`
- **Purpose**: Implements two-stage hierarchical analysis
- **Stage 3a**: High-level section ranking (60 points)
- **Stage 3b**: Sub-section analysis (40 points)
- **Output**: Ranked sections and refined text chunks

### Stage 4: Output Synthesis
- **Module**: `main_round1b.py`
- **Purpose**: Generates final JSON output in required format
- **Output**: `output.json` with metadata, extracted sections, and sub-section analysis

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Docker (for containerized execution)
- Internet connection (for initial model download)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd adobe-hackathon-1B
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download the model (required for offline operation)**
   ```bash
   python download_model.py
   ```

4. **Test the system**
   ```bash
   python test_system.py
   ```

### Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t adobe-hackathon-1b .
   ```

2. **Run the container**
   ```bash
   docker run -v /path/to/input:/input -v /path/to/output:/output adobe-hackathon-1b
   ```

## 📁 Input Format

The system expects the following input structure:

```
/input/
├── document1.pdf
├── document2.pdf
├── ...
├── persona.txt (or persona, user_persona.txt)
└── job_to_be_done.txt (or job_to_be_done, task.txt, objective.txt)
```

### Input Files

- **PDF Documents**: 3-10 PDF files to analyze
- **persona.txt**: Text file describing the user persona (e.g., "PhD Researcher in Computational Biology")
- **job_to_be_done.txt**: Text file describing the specific task/objective (e.g., "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks")

### Sample Test Cases

**Test Case 1: Academic Research**
- Documents: 4 research papers on "Graph Neural Networks for Drug Discovery"
- Persona: PhD Researcher in Computational Biology
- Job: "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"

**Test Case 2: Business Analysis**
- Documents: 3 annual reports from competing tech companies (2022-2024)
- Persona: Investment Analyst
- Job: "Analyze revenue trends, R&D investments, and market positioning strategies"

### Example Input Files

**persona.txt:**
```
investment analyst specializing in technology sector
```

**job_to_be_done.txt:**
```
analyze market trends and identify investment opportunities in emerging technologies
```

## 📊 Output Format

The system generates a single `output.json` file with the following structure:

```json
{
  "metadata": {
    "input_documents": ["document1.pdf", "document2.pdf"],
    "persona": "investment analyst specializing in technology sector",
    "job_to_be_done": "analyze market trends and identify investment opportunities",
    "processing_timestamp": "2025-01-27T12:00:00",
    "model_info": {
      "max_seq_length": 256,
      "embedding_dimension": 384,
      "model_name": "all-MiniLM-L6-v2"
    }
  },
  "extracted_section": [
    {
      "document": "document1.pdf",
      "page_number": 1,
      "section_title": "Market Analysis",
      "importance_rank": 1
    }
  ],
  "sub-section_analysis": [
    {
      "document": "document1.pdf",
      "page_number": 1,
      "refined_text": "The most relevant paragraph or chunk from this section..."
    }
  ]
}
```

## 🔧 Technical Details

### Model Selection: all-MiniLM-L6-v2

- **Size**: ~90 MB (well within 1GB limit)
- **Speed**: Optimized for fast inference
- **Performance**: Strong semantic similarity capabilities
- **Offline Operation**: Fully supported with local model storage

### Performance Optimizations

1. **Batch Processing**: All embeddings computed in batches for efficiency
2. **Vectorized Operations**: NumPy-based similarity calculations
3. **Hierarchical Analysis**: Two-stage ranking reduces computational complexity
4. **Memory Management**: Sequential document processing

### Offline Operation

The system is designed for complete offline operation:
- Model pre-downloaded and packaged in Docker image
- No network access required during execution
- Local file system only for input/output

## 🧪 Testing

### Unit Tests
```bash
python test_system.py
```

### Component Tests
```bash
# Test content segmentation
python content_segmenter.py

# Test semantic embedding
python semantic_embedder.py

# Test ranking engine
python ranking_engine.py
```

### Integration Test
```bash
# Test complete pipeline
python main_round1b.py
```

## 📈 Scoring Strategy

The system is optimized for the hackathon scoring criteria:

### Section Relevance (60 points)
- **Strategy**: Global ranking of all sections across all documents
- **Implementation**: Cosine similarity between query and section embeddings
- **Output**: Ranked list with importance_rank

### Sub-Section Relevance (40 points)
- **Strategy**: Granular analysis within top-ranked sections
- **Implementation**: Text chunking and re-ranking
- **Output**: Refined text chunks with highest relevance

## 🎯 Key Features

### 1. Hierarchical Analysis
- Two-stage approach mirrors scoring criteria
- Section-level relevance followed by sub-section refinement
- Context-aware ranking

### 2. Semantic Intelligence
- Moves beyond keyword matching to semantic understanding
- Handles synonyms, paraphrasing, and domain-specific terminology
- Robust across different document types

### 3. Performance Optimized
- Designed to meet 60-second execution limit
- Efficient batch processing and vectorized operations
- Memory-conscious document processing

### 4. Robust Error Handling
- Graceful degradation on missing files
- Minimal output generation on failures
- Comprehensive logging and debugging

## 🔍 Advanced Configuration

### Model Parameters
```python
# In semantic_embedder.py
BATCH_SIZE = 32  # Adjust for memory constraints
MAX_SEQ_LENGTH = 256  # Model-specific limit
```

### Ranking Parameters
```python
# In ranking_engine.py
MAX_SECTIONS_TO_ANALYZE = 20  # Top sections for sub-analysis
MIN_CHUNK_LENGTH = 50  # Minimum meaningful chunk size
```

### Content Segmentation
```python
# In content_segmenter.py
NEGATIVE_KEYWORDS = [...]  # Filter out non-headings
HEADING_SIZE_FACTOR = 1.1  # Font size threshold
```

## 🚨 Constraints Compliance

### ✅ Model Size
- all-MiniLM-L6-v2: ~90 MB
- Total system size: < 1GB

### ✅ Execution Time
- Target: < 60 seconds for 10 documents
- Optimized batch processing and vectorized operations

### ✅ Offline Operation
- Model pre-downloaded and packaged
- No network access during execution
- Local file system only

### ✅ Output Format
- Strict JSON compliance
- Required fields: metadata, extracted_section, sub-section_analysis
- Proper data types and structure

## 🐛 Troubleshooting

### Common Issues

1. **Model Loading Error**
   ```bash
   # Solution: Download model first
   python download_model.py
   ```

2. **Memory Issues**
   ```bash
   # Reduce batch size in semantic_embedder.py
   BATCH_SIZE = 16  # or lower
   ```

3. **Timeout Errors**
   ```bash
   # Check document size and complexity
   # Consider reducing MAX_SECTIONS_TO_ANALYZE
   ```

4. **Missing Input Files**
   ```bash
   # Ensure persona.txt and job_to_be_done.txt exist
   # Check PDF file permissions
   ```

### Debug Mode
```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 References

- [Sentence Transformers Documentation](https://www.sbert.net/)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [all-MiniLM-L6-v2 Model Card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Adobe Hackathon Challenge Documentation](https://github.com/jhaaj08/Adobe-India-Hackathon25/tree/main/Challenge_1b)

## 🤝 Contributing

This is a hackathon submission. For questions or issues, please refer to the hackathon documentation.

## 📄 License

This project is created for the Adobe India Hackathon 2025. All rights reserved. 