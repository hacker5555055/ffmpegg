from flask import Flask, jsonify, request
import subprocess
import os
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "FFmpeg is running on Render.com!"

@app.route('/ffmpeg', methods=['POST'])
def run_ffmpeg():
    # Parse JSON data from the request
    data = request.get_json()
    video_url = data.get('video_url')
    audio_url = data.get('audio_url')
    subtitle_url = data.get('subtitle_url')
    output_name = data.get('output_name', 'output.mp4')

    # Download the video, audio, and subtitle files
    try:
        video_path = '/tmp/video.mp4'
        audio_path = '/tmp/audio.mp3'
        subtitle_path = '/tmp/subtitle.srt'
        
        # Download video
        with open(video_path, 'wb') as f:
            f.write(requests.get(video_url).content)
        
        # Download audio
        with open(audio_path, 'wb') as f:
            f.write(requests.get(audio_url).content)
        
        # Download subtitle
        with open(subtitle_path, 'wb') as f:
            f.write(requests.get(subtitle_url).content)
        
        # Run FFmpeg command to combine them
        output_path = f'/tmp/{output_name}'
        ffmpeg_command = [
            'ffmpeg', '-i', video_path, '-i', audio_path,
            '-vf', f"subtitles={subtitle_path}",
            '-c:v', 'libx264', '-c:a', 'aac', output_path
        ]
        
        subprocess.run(ffmpeg_command, check=True)

        # Return the path to the output video
        return jsonify({"output_url": f"https://ffmpegg.onrender.com/{output_name}"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
