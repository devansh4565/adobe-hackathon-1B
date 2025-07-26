# Use Python 3.9 slim image for compatibility
FROM --platform=linux/amd64 python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the pre-downloaded model into the image's filesystem
COPY local_model /app/local_model

# Copy application source code
COPY *.py /app/

# Create input and output directories
RUN mkdir -p /input /output

# Set the default command to run the Round 1B system
CMD ["python", "/app/main_round1b.py"]