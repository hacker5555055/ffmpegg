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
    output_name = data.get('output_name', 'output.mp4')

    # Download the video and audio files
    try:
        video_path = '/tmp/video.mp4'
        audio_path = '/tmp/audio.mp3'
        
        # Download video
        with open(video_path, 'wb') as f:
            f.write(requests.get(video_url).content)
        
        # Download audio
        with open(audio_path, 'wb') as f:
            f.write(requests.get(audio_url).content)
        
        # Set output path
        output_path = f'/tmp/{output_name}'
        
        # FFmpeg command to resize video to 1080x1920 and add audio
        ffmpeg_command = [
            'ffmpeg', '-i', video_path, '-i', audio_path,
            '-vf', 'scale=1080:1920',  # Set video resolution to 1080x1920 for reels/shorts
            '-c:v', 'libx264', '-c:a', 'aac', '-b:a', '192k', '-shortest', output_path
        ]
        
        subprocess.run(ffmpeg_command, check=True)

        # Return the path to the output video
        return jsonify({"output_url": f"https://ffmpegg.onrender.com/{output_name}"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
