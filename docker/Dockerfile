# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy the project files
COPY requirements.txt ./
COPY src/ ./src/
COPY data/ ./data/

# Install Python dependencies
RUN pip install -r requirements.txt

# Set PYTHONPATH to include the src directory
ENV PYTHONPATH=/app/src

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the main script
CMD ["python", "/app/src/main.py"]