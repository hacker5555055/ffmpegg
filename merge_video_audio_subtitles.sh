#!/bin/bash

# Input URLs
VIDEO_URL=$1
AUDIO_URL=$2
SUBTITLE_URL=$3
OUTPUT_FILE=$4

# Download video, audio, and subtitle files
curl -O "$VIDEO_URL"
curl -O "$AUDIO_URL"
curl -O "$SUBTITLE_URL"

# Extract filenames from the URLs
VIDEO_FILE=$(basename "$VIDEO_URL")
AUDIO_FILE=$(basename "$AUDIO_URL")
SUBTITLE_FILE=$(basename "$SUBTITLE_URL")

# Merge the files with FFmpeg
ffmpeg -i "$VIDEO_FILE" -i "$AUDIO_FILE" -i "$SUBTITLE_FILE" -c:v copy -c:a aac -c:s mov_text "$OUTPUT_FILE"
