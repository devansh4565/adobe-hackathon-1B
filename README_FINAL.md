# Adobe Hackathon Round 1B: Persona-Driven Document Intelligence

## 🎯 Overview

This project implements a **Persona-Driven Document Intelligence System** for Adobe Hackathon Round 1B. The system analyzes PDF documents and extracts the most relevant sections based on a specific user persona and their job-to-be-done, using advanced semantic embeddings and ranking algorithms.

## 🚀 Challenge Requirements

**Theme**: "Connect What Matters — For the User Who Matters"

The system acts as an intelligent document analyst that:
- Processes 3-10 related PDF documents
- Takes a **persona** (user role/expertise) and **job-to-be-done** (specific task)
- Extracts and ranks the most relevant sections using semantic analysis
- Outputs structured JSON with ranked sections and sub-section analysis

### Sample Test Cases from Challenge:
1. **Academic Research**: PhD Researcher analyzing Graph Neural Networks papers for literature review
2. **Business Analysis**: Investment Analyst examining annual reports for revenue trends
3. **Educational Content**: Chemistry Student identifying key concepts from textbooks

## 📋 System Architecture

### Four-Stage Pipeline:

1. **📚 Document Processing**: Extract content using Round 1A outlines or generate new ones
2. **🧠 Semantic Embeddings**: Create query embeddings from persona+JBTD and content embeddings
3. **🏆 Ranking Analysis**: Multi-level ranking of sections and sub-sections
4. **📝 Output Generation**: Structured JSON with metadata and ranked results

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.9+
- Docker (for containerized execution)
- 8GB+ RAM, CPU-only execution

### Quick Setup
```bash
# Clone the repository
git clone https://github.com/devansh4565/adobe-hackathon-1B.git
cd adobe-hackathon-1B

# Install dependencies
pip install -r requirements.txt

# Download the model (if not already present)
python download_model.py
```

## 💡 Usage

### Method 1: Command Line Arguments ✨ **RECOMMENDED**
```bash
python main_round1b.py \
  --persona "PhD Researcher in Computational Biology" \
  --jbtd "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"
```

### Method 2: Environment Variables 🐳 **DOCKER FRIENDLY**
```bash
export PERSONA="Investment Analyst"
export JBTD="Analyze revenue trends, R&D investments, and market positioning strategies"
python main_round1b.py
```

### Method 3: Input Files (Backward Compatibility)
Create these files in your input directory:
- `persona.txt` - Contains persona description
- `job_to_be_done.txt` - Contains job-to-be-done description

```bash
python main_round1b.py
```

### Method 4: Custom Directories
```bash
python main_round1b.py \
  --input-dir ./my_input \
  --output-dir ./my_output \
  --persona "Undergraduate Chemistry Student" \
  --jbtd "Identify key concepts for exam preparation"
```

## 🐳 Docker Usage

### Build the Image
```bash
docker build --platform linux/amd64 -t adobe-hackathon-1b:latest .
```

### Run with Environment Variables (Recommended)
```bash
docker run --rm \
  -e PERSONA="PhD Researcher in Computational Biology" \
  -e JBTD="Prepare comprehensive literature review" \
  -v $(pwd)/input:/input \
  -v $(pwd)/output:/output \
  --network none \
  adobe-hackathon-1b:latest
```

### Run with Command Arguments
```bash
docker run --rm \
  -v $(pwd)/input:/input \
  -v $(pwd)/output:/output \
  --network none \
  adobe-hackathon-1b:latest \
  python main_round1b.py \
    --persona "Investment Analyst" \
    --jbtd "Analyze revenue trends and market positioning"
```

### Challenge Execution Format
```bash
docker run --rm \
  -v $(pwd)/input:/input \
  -v $(pwd)/output:/output \
  --network none \
  adobe-hackathon-1b:latest
```

## 📁 Project Structure

```
adobe-hackathon-1B/
├── main_round1b.py           # Main orchestration module
├── content_segmenter.py      # Document content extraction
├── semantic_embedder.py      # Embedding creation and similarity
├── ranking_engine.py         # Multi-level ranking algorithms
├── main.py                   # Round 1A outline generation (fallback)
├── process_docs.py           # PDF text extraction utilities
├── download_model.py         # Model download script
├── dockerfile                # Docker configuration
├── requirements.txt          # Python dependencies
├── local_model/              # Pre-downloaded sentence transformer model
├── input/                    # Input PDFs and persona files
├── output/                   # Generated outlines and results
├── round1b_output/           # Round 1B specific outputs
├── test_new_interface.py     # Interface testing script
└── README.md                 # This file
```

## 📤 Input Specification

### Required Inputs:
1. **PDFs**: 3-10 related PDF documents in input directory
2. **Persona**: User role description (e.g., "PhD Researcher in Biology")
3. **Job-to-be-Done**: Specific task (e.g., "Prepare literature review")

### Input Methods (Priority Order):
1. **Command Line**: `--persona "..."` `--jbtd "..."`
2. **Environment**: `PERSONA="..."` `JBTD="..."`
3. **Files**: `persona.txt`, `job_to_be_done.txt`
4. **Defaults**: "document analyst", "extract relevant information"

## 📊 Output Format

### Generated Files:
- `output.json` - Main results file
- Individual PDF outline files (if generated)

### JSON Structure:
```json
{
  "metadata": {
    "input_documents": ["doc1.pdf", "doc2.pdf"],
    "persona": "PhD Researcher in Biology",
    "job_to_be_done": "Prepare literature review",
    "processing_timestamp": "2025-01-27T...",
    "model_info": {...}
  },
  "extracted_sections": [
    {
      "document": "doc1.pdf",
      "page_number": 5,
      "section_title": "Methodology",
      "importance_rank": 1,
      "relevance_score": 0.95,
      "content": "..."
    }
  ],
  "subsection_analysis": [
    {
      "document": "doc1.pdf",
      "page_number": 5,
      "refined_text": "Key methodological insights...",
      "relevance_score": 0.92
    }
  ]
}
```

## 🧪 Testing

### Test the Interface
```bash
python test_new_interface.py
```

### Run Sample Tests
```bash
# Academic Research Test
python main_round1b.py \
  --persona "PhD Researcher in Computational Biology" \
  --jbtd "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"

# Business Analysis Test  
python main_round1b.py \
  --persona "Investment Analyst" \
  --jbtd "Analyze revenue trends, R&D investments, and market positioning strategies"

# Educational Test
python main_round1b.py \
  --persona "Undergraduate Chemistry Student" \
  --jbtd "Identify key concepts and mechanisms for exam preparation on reaction kinetics"
```

### Help Command
```bash
python main_round1b.py --help
```

## ⚙️ Configuration

### Environment Variables:
- `PERSONA` - User persona description
- `JBTD` or `JOB_TO_BE_DONE` - Job-to-be-done description

### Command Line Options:
- `--persona, -p` - Persona description
- `--jbtd, -j` - Job-to-be-done description  
- `--input-dir, -i` - Input directory path
- `--output-dir, -o` - Output directory path

## 🎯 Challenge Compliance

### ✅ Requirements Met:
- **Model size**: ≤ 1GB (sentence transformer ~384MB)
- **Processing time**: ≤ 60 seconds for 3-5 documents
- **CPU only**: No GPU dependencies
- **Offline**: No internet access during execution
- **Platform**: AMD64 compatible
- **Generic solution**: Handles diverse personas and tasks

### ✅ Scoring Criteria:
- **Section Relevance (60 points)**: Semantic ranking with persona+JBTD context
- **Sub-Section Relevance (40 points)**: Granular analysis and ranking

## 🔧 Development

### Key Components:

1. **PersonaDrivenDocumentIntelligence**: Main orchestrator class
2. **ContentSegmenter**: Extracts content from PDFs using outlines
3. **SemanticEmbedder**: Creates and manages sentence embeddings
4. **RankingEngine**: Multi-level ranking and analysis

### Model Information:
- **Model**: Sentence Transformer (all-MiniLM-L6-v2)
- **Embedding Dimension**: 384
- **Max Sequence Length**: 256 tokens
- **Size**: ~384MB

## 🚨 Troubleshooting

### Common Issues:

1. **Missing Model**: Run `python download_model.py`
2. **No PDFs Found**: Check input directory path
3. **Memory Issues**: Reduce batch size in embeddings
4. **Docker Platform**: Ensure `--platform linux/amd64`

### Debug Mode:
```bash
python main_round1b.py --persona "Test" --jbtd "Test" -v
```

## 📚 Documentation

- `README_Round1B_Updated.md` - Detailed interface documentation
- `approach_explanation.md` - Technical methodology (300-500 words)
- Inline code documentation with docstrings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

## 📄 License

This project is part of the Adobe India Hackathon 2025.

## 🏆 Adobe Hackathon Round 1B Challenge

**"Connecting the Dots"** - Rethink Reading. Rediscover Knowledge.

This system transforms static PDFs into intelligent, persona-aware documents that understand context and surface the most relevant insights for each user's specific needs.

---

**Ready to connect the dots? Let's build the future of document intelligence! 🚀**
