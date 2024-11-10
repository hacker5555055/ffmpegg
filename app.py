import os
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/merge', methods=['POST'])
def merge_media():
    data = request.get_json()
    video_url = data.get("video_url")
    audio_url = data.get("audio_url")
    subtitle_url = data.get("subtitle_url")

    # Download files from URLs
    video_file = 'video.mp4'
    audio_file = 'audio.mp3'
    subtitle_file = 'subtitles.srt'
    output_file = 'merged_output.mp4'

    # Using wget to download the files
    subprocess.run(["wget", "-O", video_file, video_url])
    subprocess.run(["wget", "-O", audio_file, audio_url])
    subprocess.run(["wget", "-O", subtitle_file, subtitle_url])

    # Merge video, audio, and subtitles using FFmpeg
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', video_file,
        '-i', audio_file,
        '-vf', f"subtitles={subtitle_file}",
        '-c:v', 'libx264', '-c:a', 'aac',
        '-strict', 'experimental', '-y', output_file
    ]
    subprocess.run(ffmpeg_cmd)

    # Return the output file URL (assuming you'll host it or store it somewhere accessible)
    return jsonify({"message": "Video merged successfully", "output_file": output_file})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
