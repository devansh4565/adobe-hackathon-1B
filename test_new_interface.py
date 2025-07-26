#!/usr/bin/env python3
"""
Test script to demonstrate the new interface for Round 1B
"""

import subprocess
import os

def test_command_line_args():
    """Test using command line arguments"""
    print("=" * 60)
    print("🧪 Testing Command Line Arguments")
    print("=" * 60)
    
    cmd = [
        "python", "main_round1b.py",
        "--persona", "PhD Researcher in Computational Biology",
        "--jbtd", "Prepare a comprehensive literature review focusing on methodologies and datasets"
    ]
    
    print(f"Running: {' '.join(cmd)}")
    print()
    
    # Note: This would run the actual pipeline if you have input PDFs
    # For now, just show the command structure
    return cmd

def test_environment_variables():
    """Test using environment variables"""
    print("=" * 60)
    print("🧪 Testing Environment Variables")
    print("=" * 60)
    
    # Set environment variables
    os.environ['PERSONA'] = 'Investment Analyst'
    os.environ['JBTD'] = 'Analyze revenue trends, R&D investments, and market positioning strategies'
    
    cmd = ["python", "main_round1b.py"]
    
    print("Environment variables set:")
    print(f"PERSONA = {os.environ.get('PERSONA')}")
    print(f"JBTD = {os.environ.get('JBTD')}")
    print()
    print(f"Running: {' '.join(cmd)}")
    print()
    
    return cmd

def test_default_behavior():
    """Test default behavior (backward compatibility)"""
    print("=" * 60)
    print("🧪 Testing Default Behavior")
    print("=" * 60)
    
    # Clear environment variables
    if 'PERSONA' in os.environ:
        del os.environ['PERSONA']
    if 'JBTD' in os.environ:
        del os.environ['JBTD']
    
    cmd = ["python", "main_round1b.py"]
    
    print("No command line args or environment variables")
    print("Will check for input files, then use defaults")
    print(f"Running: {' '.join(cmd)}")
    print()
    
    return cmd

def show_help():
    """Show help message"""
    print("=" * 60)
    print("📚 Help Message")
    print("=" * 60)
    
    cmd = ["python", "main_round1b.py", "--help"]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        print(result.stdout)
    except Exception as e:
        print(f"Could not run help command: {e}")

def main():
    """Demonstrate all the new interface options"""
    
    print("🚀 Adobe Hackathon Round 1B - New Interface Demo")
    print("This shows the different ways to provide persona and job-to-be-done")
    print()
    
    # Show help first
    show_help()
    
    # Test different input methods
    cmd1 = test_command_line_args()
    cmd2 = test_environment_variables()
    cmd3 = test_default_behavior()
    
    print("=" * 60)
    print("📋 Summary")
    print("=" * 60)
    print("The system now supports multiple input methods in priority order:")
    print("1. ✅ Command line arguments (--persona, --jbtd)")
    print("2. ✅ Environment variables (PERSONA, JBTD)")
    print("3. ✅ Input files (persona.txt, job_to_be_done.txt) - backward compatibility")
    print("4. ✅ Default values (document analyst, extract relevant information)")
    print()
    print("This aligns with the challenge requirements where:")
    print("- Test cases provide persona and JBTD as inputs")
    print("- Teams don't need to manually create text files")
    print("- The solution should be generic and flexible")
    print()
    
    print("🐳 Docker Usage Examples:")
    print("# Using environment variables in Docker")
    print("docker run --rm \\")
    print("  -e PERSONA='PhD Researcher in Biology' \\")
    print("  -e JBTD='Prepare literature review' \\")
    print("  -v $(pwd)/input:/input \\")
    print("  -v $(pwd)/output:/output \\")
    print("  --network none \\")
    print("  mysolution:tag")
    print()
    
    print("# Using command within Docker")
    print("docker run --rm \\")
    print("  -v $(pwd)/input:/input \\")
    print("  -v $(pwd)/output:/output \\")
    print("  --network none \\")
    print("  mysolution:tag \\")
    print("  python main_round1b.py --persona 'Investment Analyst' --jbtd 'Analyze revenue trends'")

if __name__ == "__main__":
    main()
