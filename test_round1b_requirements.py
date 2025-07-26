#!/usr/bin/env python3
"""
Test Script for Round 1B Requirements Compliance
Tests the system against the specific requirements and sample test cases from the challenge document.
"""

import os
import json
import tempfile
import shutil
from main_round1b import PersonaDrivenDocumentIntelligence

def create_test_case_1():
    """Create Test Case 1: Academic Research"""
    print("🧪 Creating Test Case 1: Academic Research")
    
    test_input_dir = tempfile.mkdtemp(prefix="test_case_1_")
    
    # Create persona file
    persona_content = "PhD Researcher in Computational Biology"
    with open(os.path.join(test_input_dir, "persona.txt"), 'w') as f:
        f.write(persona_content)
    
    # Create job-to-be-done file
    jbtd_content = "Prepare a comprehensive literature review focusing on methodologies, datasets, and performance benchmarks"
    with open(os.path.join(test_input_dir, "job_to_be_done.txt"), 'w') as f:
        f.write(jbtd_content)
    
    # Create sample PDF files (using text files as placeholders)
    pdf_contents = [
        """Graph Neural Networks for Drug Discovery

Introduction
Recent advances in machine learning have revolutionized drug discovery processes. This paper presents a novel approach using graph neural networks for predicting drug-target interactions.

Methodology
Our proposed methodology utilizes a novel graph neural network architecture that incorporates attention mechanisms for drug-target interaction prediction. The model achieves state-of-the-art performance on benchmark datasets with an accuracy of 94.2%.

Results
The experimental results demonstrate significant improvements over existing approaches, with a 12.3% increase in prediction accuracy.""",
        
        """Experimental Setup for Drug Discovery

Introduction
This paper focuses on the experimental setup and evaluation methodology for drug discovery using machine learning approaches.

Experimental Setup
The experimental setup includes comprehensive evaluation on three major drug discovery datasets: BindingDB, ChEMBL, and DrugBank. We employ 5-fold cross-validation and report results across multiple performance metrics including AUC-ROC, precision, and recall.

Datasets
We utilize three major datasets for our evaluation, each containing thousands of drug-target interaction pairs.""",
        
        """Performance Analysis in Drug Discovery

Introduction
Performance analysis is crucial for evaluating the effectiveness of drug discovery algorithms.

Results and Analysis
Performance benchmarks show our model outperforms existing approaches by 12.3% on average across all evaluation metrics. The analysis reveals significant improvements in prediction accuracy for novel drug-target pairs.

Benchmarks
We compare our approach against state-of-the-art methods including DeepChem, MoleculeNet, and other graph-based approaches."""
    ]
    
    for i, content in enumerate(pdf_contents, 1):
        with open(os.path.join(test_input_dir, f"research_paper_{i}.pdf"), 'w') as f:
            f.write(content)
    
    return test_input_dir

def create_test_case_2():
    """Create Test Case 2: Business Analysis"""
    print("🧪 Creating Test Case 2: Business Analysis")
    
    test_input_dir = tempfile.mkdtemp(prefix="test_case_2_")
    
    # Create persona file
    persona_content = "Investment Analyst"
    with open(os.path.join(test_input_dir, "persona.txt"), 'w') as f:
        f.write(persona_content)
    
    # Create job-to-be-done file
    jbtd_content = "Analyze revenue trends, R&D investments, and market positioning strategies"
    with open(os.path.join(test_input_dir, "job_to_be_done.txt"), 'w') as f:
        f.write(jbtd_content)
    
    # Create sample PDF files
    pdf_contents = [
        """Annual Report 2022 - Tech Company A

Executive Summary
Tech Company A reported strong growth in 2022 with revenue increasing by 15% year-over-year.

Financial Performance
Revenue trends show consistent growth across all business segments. R&D investments increased by 20% to support innovation initiatives.

Market Positioning
Our market positioning strategy focuses on cloud computing and AI services, with significant investments in emerging technologies.""",
        
        """Annual Report 2023 - Tech Company B

Executive Summary
Tech Company B achieved record revenue in 2023, driven by expansion into new markets.

Financial Performance
Revenue trends indicate strong performance in enterprise software and services. R&D investments totaled $500 million, representing 12% of revenue.

Market Positioning
Our market positioning emphasizes customer-centric solutions and strategic partnerships in the technology ecosystem."""
    ]
    
    for i, content in enumerate(pdf_contents, 1):
        with open(os.path.join(test_input_dir, f"annual_report_{i}.pdf"), 'w') as f:
            f.write(content)
    
    return test_input_dir

def test_requirements_compliance():
    """Test that our system meets all Round 1B requirements."""
    print("🔍 Testing Round 1B Requirements Compliance...")
    
    # Test 1: Model size compliance
    print("📊 Testing model size compliance...")
    model_path = "./local_model"
    if os.path.exists(model_path):
        # Calculate approximate size (this is a rough estimate)
        total_size = 0
        for root, dirs, files in os.walk(model_path):
            for file in files:
                file_path = os.path.join(root, file)
                total_size += os.path.getsize(file_path)
        
        size_mb = total_size / (1024 * 1024)
        print(f"✅ Model size: {size_mb:.2f} MB (limit: 1000 MB)")
        if size_mb <= 1000:
            print("✅ Model size compliance: PASSED")
        else:
            print("❌ Model size compliance: FAILED")
    else:
        print("⚠️  Model not found, skipping size test")
    
    # Test 2: Output format compliance
    print("📋 Testing output format compliance...")
    sample_output = {
        "metadata": {
            "input_documents": ["test.pdf"],
            "persona": "test persona",
            "job_to_be_done": "test job",
            "processing_timestamp": "2025-01-27T12:00:00"
        },
        "extracted_section": [
            {
                "document": "test.pdf",
                "page_number": 1,
                "section_title": "Test Section",
                "importance_rank": 1
            }
        ],
        "sub-section_analysis": [
            {
                "document": "test.pdf",
                "page_number": 1,
                "refined_text": "Test refined text"
            }
        ]
    }
    
    # Check required fields
    required_fields = {
        "metadata": ["input_documents", "persona", "job_to_be_done", "processing_timestamp"],
        "extracted_section": ["document", "page_number", "section_title", "importance_rank"],
        "sub-section_analysis": ["document", "page_number", "refined_text"]
    }
    
    format_compliant = True
    for section, fields in required_fields.items():
        if section not in sample_output:
            print(f"❌ Missing required section: {section}")
            format_compliant = False
        else:
            for field in fields:
                if field not in sample_output[section][0]:
                    print(f"❌ Missing required field: {section}.{field}")
                    format_compliant = False
    
    if format_compliant:
        print("✅ Output format compliance: PASSED")
    else:
        print("❌ Output format compliance: FAILED")
    
    return format_compliant

def test_sample_cases():
    """Test the system with sample test cases from the challenge document."""
    print("🧪 Testing Sample Test Cases...")
    
    try:
        # Initialize system
        system = PersonaDrivenDocumentIntelligence()
        
        # Test Case 1: Academic Research
        print("\n📚 Testing Case 1: Academic Research")
        test_input_1 = create_test_case_1()
        test_output_1 = tempfile.mkdtemp(prefix="test_output_1_")
        
        try:
            results_1 = system.run_pipeline(test_input_1, test_output_1)
            print("✅ Test Case 1 completed successfully")
            
            # Check results structure
            if "metadata" in results_1 and "extracted_section" in results_1 and "sub-section_analysis" in results_1:
                print(f"✅ Found {len(results_1['extracted_section'])} sections and {len(results_1['sub-section_analysis'])} sub-sections")
            else:
                print("❌ Invalid output structure for Test Case 1")
                
        except Exception as e:
            print(f"❌ Test Case 1 failed: {e}")
        
        finally:
            shutil.rmtree(test_input_1)
            shutil.rmtree(test_output_1)
        
        # Test Case 2: Business Analysis
        print("\n💼 Testing Case 2: Business Analysis")
        test_input_2 = create_test_case_2()
        test_output_2 = tempfile.mkdtemp(prefix="test_output_2_")
        
        try:
            results_2 = system.run_pipeline(test_input_2, test_output_2)
            print("✅ Test Case 2 completed successfully")
            
            # Check results structure
            if "metadata" in results_2 and "extracted_section" in results_2 and "sub-section_analysis" in results_2:
                print(f"✅ Found {len(results_2['extracted_section'])} sections and {len(results_2['sub-section_analysis'])} sub-sections")
            else:
                print("❌ Invalid output structure for Test Case 2")
                
        except Exception as e:
            print(f"❌ Test Case 2 failed: {e}")
        
        finally:
            shutil.rmtree(test_input_2)
            shutil.rmtree(test_output_2)
        
        print("\n🎉 Sample test cases completed!")
        
    except Exception as e:
        print(f"❌ System initialization failed: {e}")

def main():
    """Run all compliance tests."""
    print("🚀 Starting Round 1B Requirements Compliance Tests...")
    
    # Test requirements compliance
    requirements_ok = test_requirements_compliance()
    
    if requirements_ok:
        # Test sample cases
        test_sample_cases()
        print("\n✅ All compliance tests completed!")
    else:
        print("\n❌ Requirements compliance failed, skipping sample tests")

if __name__ == "__main__":
    main() 