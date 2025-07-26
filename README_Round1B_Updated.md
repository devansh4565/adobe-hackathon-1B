# Adobe Hackathon Round 1B - Updated Interface

## Overview

The system has been updated to properly handle persona and job-to-be-done inputs according to the challenge requirements. Instead of requiring manual text files, the system now accepts these inputs through multiple flexible methods.

## Input Methods (Priority Order)

### 1. Command Line Arguments ✨ **RECOMMENDED**
```bash
python main_round1b.py \
  --persona "PhD Researcher in Computational Biology" \
  --jbtd "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"
```

### 2. Environment Variables ✨ **DOCKER FRIENDLY**
```bash
export PERSONA="Investment Analyst"
export JBTD="Analyze revenue trends, R&D investments, and market positioning strategies"
python main_round1b.py
```

### 3. Input Files (Backward Compatibility)
- `persona.txt` - Contains persona description
- `job_to_be_done.txt` - Contains job-to-be-done description

### 4. Default Values (Fallback)
- Persona: "document analyst"
- Job-to-be-done: "extract relevant information from documents"

## Usage Examples

### Local Testing
```bash
# Method 1: Command line arguments
python main_round1b.py \
  --persona "Undergraduate Chemistry Student" \
  --jbtd "Identify key concepts and mechanisms for exam preparation on reaction kinetics"

# Method 2: Environment variables
export PERSONA="Undergraduate Chemistry Student"
export JBTD="Identify key concepts and mechanisms for exam preparation"
python main_round1b.py

# Method 3: Custom directories
python main_round1b.py \
  --input-dir ./my_input \
  --output-dir ./my_output \
  --persona "Investment Analyst" \
  --jbtd "Analyze market trends"
```

### Docker Usage

#### Method 1: Environment Variables (Recommended for Docker)
```bash
docker run --rm \
  -e PERSONA="PhD Researcher in Computational Biology" \
  -e JBTD="Prepare comprehensive literature review" \
  -v $(pwd)/input:/input \
  -v $(pwd)/output:/output \
  --network none \
  mysolution:tag
```

#### Method 2: Command Arguments in Docker
```bash
docker run --rm \
  -v $(pwd)/input:/input \
  -v $(pwd)/output:/output \
  --network none \
  mysolution:tag \
  python main_round1b.py \
    --persona "Investment Analyst" \
    --jbtd "Analyze revenue trends and market positioning"
```

#### Method 3: Default Behavior (Backward Compatible)
```bash
# This will look for input files, then use defaults
docker run --rm \
  -v $(pwd)/input:/input \
  -v $(pwd)/output:/output \
  --network none \
  mysolution:tag
```

## Challenge Requirements Alignment

This update aligns with the Adobe Hackathon Round 1B requirements:

1. ✅ **Test cases provide persona and JBTD as inputs** - System accepts them via command line/environment
2. ✅ **Generic solution** - Handles diverse personas and jobs-to-be-done
3. ✅ **No manual file creation needed** - Teams don't need to create text files
4. ✅ **Docker compatible** - Works with challenge execution environment
5. ✅ **Backward compatible** - Still works with existing input files

## Sample Test Cases from Challenge

### Test Case 1: Academic Research
```bash
python main_round1b.py \
  --persona "PhD Researcher in Computational Biology" \
  --jbtd "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"
```

### Test Case 2: Business Analysis  
```bash
python main_round1b.py \
  --persona "Investment Analyst" \
  --jbtd "Analyze revenue trends, R&D investments, and market positioning strategies"
```

### Test Case 3: Educational Content
```bash
python main_round1b.py \
  --persona "Undergraduate Chemistry Student" \
  --jbtd "Identify key concepts and mechanisms for exam preparation on reaction kinetics"
```

## Help
```bash
python main_round1b.py --help
```

## Testing the New Interface
```bash
python test_new_interface.py
```

This script demonstrates all the input methods and shows how they work together.
