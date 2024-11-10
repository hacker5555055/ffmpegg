# Use a lightweight Python image
FROM python:3.9-slim

# Install FFmpeg and necessary dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy application code into the container
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose port for the Flask app
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
