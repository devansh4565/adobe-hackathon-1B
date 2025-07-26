📄 Persona-Driven PDF Intelligence System
An offline, CPU-only, Dockerized Python solution that extracts structured PDF content and ranks it for relevance based on persona-specific queries (e.g., "summary for a Product Manager"). Built for efficiency, interpretability, and extensibility.
🔧 Overview
This system provides a streamlined pipeline for understanding complex PDFs through the lens of specific professional personas. By inputting a PDF and a query, the system identifies and ranks the most relevant sections of the document for a given role, such as a Product Manager or Marketing Lead. The entire process is designed to run efficiently on CPU-only environments and is packaged within a Docker container for easy deployment and scalability.
Features
Intelligent PDF Segmentation: Extracts clean, structured text from PDFs by leveraging heading hierarchies.
Semantic Relevance Scoring: Uses state-of-the-art sentence embeddings to find the most relevant content.
Persona-Driven Queries: Tailors results to the needs of different professional roles.
Offline & CPU-Only: Runs without requiring a GPU or an active internet connection.
Dockerized: Encapsulated for consistent and reliable deployment.
🔁 Modular Pipeline Breakdown
The system operates through a sequential pipeline of four distinct modules:
🧩 1. PDF Segmentation Module
This module is responsible for ingesting a raw PDF and extracting its content in a structured manner.
Process: It uses PyMuPDF for precise text extraction, identifying text blocks associated with headings (H1-H3). To enhance speed, page extraction is parallelized. If a document structure is not found, it defaults to page-by-page segmentation.
Output: A JSON array of text chunks, each with its corresponding heading, level, and page number.
🧠 2. Embedding + Semantic Representation
This module transforms the text chunks and the user query into a format suitable for semantic comparison.
Model: Utilizes the lightweight all-MiniLM-L6-v2 sentence-transformer model.
Process: Encodes all text chunks and the persona-based query into dense vector embeddings. For development efficiency, embeddings can be cached.
Output: A list of vector embeddings for the text chunks and a single embedding for the query.
🎯 3. Multi-Level Relevance Scoring
The core of the system, this module ranks the text chunks based on their relevance to the query.
Process: It calculates the cosine similarity between the query embedding and each chunk embedding. To refine the results, it filters out very short text snippets and applies a soft boost to chunks where the heading text overlaps with the query.
Output: A ranked list of the top N chunks with their relevance scores.
📦 4. JSON Output Synthesizer
The final module assembles the top-ranked sections into a clean, structured JSON output.
Process: It combines the most relevant sections and formats them into a JSON object that includes the persona, the original query, and a list of the top-scoring sections with their titles and text. The output is validated against a predefined schema for consistency.
Output: A structured JSON file ready for downstream applications.
🐳 Docker Plan
Directory Structure
Generated plaintext
project/
├── app/
│   ├── main.py
│   ├── pdf_segmenter.py
│   ├── embedder.py
│   ├── scorer.py
│   └── utils.py
├── requirements.txt
├── Dockerfile
└── test/
    └── sample.pdf
Use code with caution.
Dockerfile
Generated dockerfile
# Use a slim Python base image
FROM python:3.10-slim

# Install system dependencies required for PyMuPDF
RUN apt-get update && apt-get install -y build-essential libmupdf-dev && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY app /app
WORKDIR /app

# Define the command to run the application
CMD ["python", "main.py"]
Use code with caution.
Dockerfile
✅ Polishing & Enhancements
Enhancement	Benefit
Parallelized PDF parsing	Provides a 2–4x speedup on the segmentation process.
Chunk filtering	Reduces noise from irrelevant document elements like headers and footers.
Soft keyword boosting in scoring	Improves semantic relevance, especially for nuanced queries.
Embedding caching (joblib)	Accelerates development cycles and ensures reproducibility.
Colored console logs (rich)	Enhances developer experience and simplifies debugging.
JSON schema validation	Guarantees that the output structure is always consistent and reliable.
🧪 Testing Strategy
To run a test from the command line, use the following format:
Generated bash
# Test with a local file and persona query
python main.py --pdf "./test/sample.pdf" --persona "Marketing Lead" --query "Insights for customer retention"
Use code with caution.
Bash
This will produce:
An output/persona_result.json file.
A console printout of the top 5 ranked chunks with their headings and scores.
Sample Output Snippet
Generated json
{
  "persona": "Marketing Lead",
  "query": "Customer Retention Techniques",
  "sections": [
    {
      "title": "Customer Loyalty Strategies",
      "text": "To retain customers, we focus on personalized outreach...",
      "score": 0.892
    },
    {
      "title": "Retention Metrics",
      "text": "We track CLTV and churn rate to measure success...",
      "score": 0.843
    }
  ]
}
Use code with caution.
Json
This project is engineered for speed, robustness, and scalability, making it an ideal foundation for more advanced features like OCR fallback or interactive Q&A systems. The validated JSON outputs are designed for seamless integration into any downstream UX/UI.