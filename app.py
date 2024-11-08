from flask import Flask, jsonify, request
import subprocess
import os
import requests
import mimetypes

app = Flask(__name__)

@app.route('/')
def home():
    return "FFmpeg is running on Render.com!"

@app.route('/ffmpeg', methods=['POST'])
def run_ffmpeg():
    data = request.get_json()
    video_url = data.get('video_url')
    audio_url = data.get('audio_url')
    output_name = data.get('output_name', 'output.mp4')

    video_path = '/tmp/video.mp4'
    audio_path = '/tmp/audio.mp3'
    output_path = f'/tmp/{output_name}'

    try:
        # Download file function with improved error handling
        def download_file(url, path):
            headers = {"User-Agent": "Mozilla/5.0"} if "drive.google.com" in url else {}
            response = requests.get(url, headers=headers, stream=True)
            response.raise_for_status()

            # Write content in chunks to avoid incomplete downloads
            with open(path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            # Verify the file type by checking its MIME type
            mime_type, _ = mimetypes.guess_type(path)
            if not mime_type or not mime_type.startswith('video'):
                raise ValueError("Downloaded file is not a valid video format.")

        # Download video and audio files
        download_file(video_url, video_path)
        download_file(audio_url, audio_path)

        # Double-check if files are downloaded and readable
        if os.path.getsize(video_path) == 0 or os.path.getsize(audio_path) == 0:
            raise ValueError("Downloaded video or audio file is empty.")

        # FFmpeg command to combine video and audio, resizing video for reels
        ffmpeg_command = [
            'ffmpeg', '-i', video_path, '-i', audio_path,
            '-vf', 'scale=1080:1920',  # Set for 1080x1920 resolution
            '-c:v', 'libx264', '-c:a', 'aac', '-b:a', '192k', '-shortest', output_path
        ]

        subprocess.run(ffmpeg_command, check=True)

        # Return the output video link
        return jsonify({"output_url": f"https://ffmpegg.onrender.com/{output_name}"})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"File download failed: {str(e)}"}), 500
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"FFmpeg processing failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
