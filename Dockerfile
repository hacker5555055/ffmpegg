# Start from the FFmpeg base image
FROM jrottenberg/ffmpeg:latest

# Set the working directory
WORKDIR /app

# Install curl to download the video, audio, and subtitle files
RUN apt-get update && apt-get install -y curl

# Copy your shell script into the container
COPY merge_video_audio_subtitles.sh .

# Ensure the shell script is executable
RUN chmod +x merge_video_audio_subtitles.sh

# Copy your Node.js app into the container (if you're using Express)
COPY server.js .

# Expose the necessary port (3000 is common)
EXPOSE 3000

# Start the Node.js app (or use a different command based on your setup)
CMD ["node", "server.js"]
