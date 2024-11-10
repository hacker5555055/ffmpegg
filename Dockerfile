FROM jrottenberg/ffmpeg:latest

WORKDIR /app

# Install curl for fetching the files
RUN apt-get update && apt-get install -y curl

# Copy the script to the container
COPY merge_video_audio_subtitles.sh .

# Make the script executable
RUN chmod +x merge_video_audio_subtitles.sh

# Expose the port the app will run on
EXPOSE 3000

# Command to run the application
CMD ["node", "server.js"]
