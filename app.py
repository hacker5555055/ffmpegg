from flask import Flask, jsonify, request
import subprocess
import os
import requests
import mimetypes
import logging

app = Flask(__name__)

# Configure logging to output to console
logging.basicConfig(level=logging.INFO)

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
        def download_file(url, path, file_type):
            headers = {"User-Agent": "Mozilla/5.0"} if "drive.google.com" in url else {}
            response = requests.get(url, headers=headers, stream=True)
            response.raise_for_status()

            with open(path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            mime_type, _ = mimetypes.guess_type(path)
            if not mime_type or not mime_type.startswith(file_type):
                raise ValueError(f"Downloaded file is not a valid {file_type} format.")
        
        # Download video and audio files with type checking
        download_file(video_url, video_path, 'video')
        download_file(audio_url, audio_path, 'audio')

        # Verify files are not empty
        if os.path.getsize(video_path) == 0 or os.path.getsize(audio_path) == 0:
            raise ValueError("Downloaded video or audio file is empty.")

        # FFmpeg command to combine video and audio, set resolution for reels
        ffmpeg_command = [
            'ffmpeg', '-y',  # -y flag forces overwriting output file without asking
            '-i', video_path, '-i', audio_path,
            '-vf', 'scale=1080:1920',  # Set for 1080x1920 resolution
            '-c:v', 'libx264', '-c:a', 'aac', '-b:a', '192k', '-shortest', output_path
        ]

        logging.info(f"Running FFmpeg command: {' '.join(ffmpeg_command)}")
        subprocess.run(ffmpeg_command, check=True)

        # Return the output video link
        return jsonify({"output_url": f"https://ffmpegg.onrender.com/{output_name}"})

    except requests.exceptions.RequestException as e:
        logging.error(f"File download failed: {str(e)}")
        return jsonify({"error": f"File download failed: {str(e)}"}), 500
    except subprocess.CalledProcessError as e:
        logging.error(f"FFmpeg processing failed: {str(e)}")
        return jsonify({"error": f"FFmpeg processing failed: {str(e)}"}), 500
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
