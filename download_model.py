#!/usr/bin/env python3
"""
Model Download Script for Adobe Hackathon Round 1B
Downloads the all-MiniLM-L6-v2 model and saves it locally for offline use.
"""

import os
from sentence_transformers import SentenceTransformer

def download_model():
    """Download and save the sentence transformer model locally."""
    
    # Model configuration
    model_name = 'all-MiniLM-L6-v2'
    save_path = './local_model'
    
    print(f"Downloading model: {model_name}")
    print(f"Save path: {save_path}")
    
    try:
        # Download the model from Hugging Face Hub
        model = SentenceTransformer(model_name)
        
        # Create directory if it doesn't exist
        os.makedirs(save_path, exist_ok=True)
        
        # Save the model locally
        model.save(save_path)
        
        print(f"✅ Model '{model_name}' successfully downloaded and saved to '{save_path}'")
        print(f"📁 Model files saved in: {os.path.abspath(save_path)}")
        
        # Verify the model can be loaded locally
        print("🔍 Verifying local model loading...")
        local_model = SentenceTransformer(save_path, local_files_only=True)
        print("✅ Local model loading verified successfully!")
        
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        raise

if __name__ == "__main__":
    download_model() 