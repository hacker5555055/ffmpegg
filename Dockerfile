# Start with a base image that has FFmpeg installed
FROM jrottenberg/ffmpeg:latest

# Set the working directory
WORKDIR /usr/src/app

# Install curl or wget to download files
RUN apt-get update && apt-get install -y curl

# Copy the script into the container
COPY merge_video_audio_subtitles.sh .

# Command to run when the container starts
CMD ["bash", "merge_video_audio_subtitles.sh"]
