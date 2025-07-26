# Use a standard Python base image
FROM python:3.9-slim

WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Include the Model for Offline Use ---
# Set an environment variable to tell the library where to find the model cache
ENV TRANSFORMERS_CACHE="/app/model_cache"
# Copy the locally saved model files into the specified cache directory
COPY ./model_cache /app/model_cache

# Copy the rest of your application
COPY . .

# Set the command to run when the container starts
# Note: You'll need to adapt this if your script needs command-line arguments
# for persona, job, etc.
CMD ["python", "process_docs.py"]