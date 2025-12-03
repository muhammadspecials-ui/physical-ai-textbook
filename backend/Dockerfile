# Use official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the backend directory contents into the container at /app
COPY backend/ /app/

# Install any needed packages specified in requirements.txt
# If requirements.txt is missing, we install manually based on our knowledge
RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy psycopg2-binary qdrant-client openai pydantic python-dotenv python-multipart

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV MODULE_NAME="main"
ENV VARIABLE_NAME="app"
ENV PORT="8000"

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
