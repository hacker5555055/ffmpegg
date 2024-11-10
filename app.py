import os
import requests
from flask import Flask, request, jsonify, send_file
import ffmpeg

app = Flask(__name__)

# Set the upload directory
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def download_file(url, filename):
    """Download file from a URL to a specified location."""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    else:
        raise Exception(f"Failed to download file from {url}")

def merge_audio_video_with_subtitles(video_path, audio_path, subtitle_path, output_path):
    """Merge audio and video files with subtitles."""
    input_video = ffmpeg.input(video_path)
    input_audio = ffmpeg.input(audio_path)
    input_subtitle = ffmpeg.input(subtitle_path)

    # Merge video and audio, then add subtitles
    (
        ffmpeg
        .concat(input_video, input_audio, v=1, a=1)
        .output(output_path, vf=f"subtitles={subtitle_path}")
        .run()
    )

@app.route('/merge', methods=['POST'])
def merge():
    video_url = request.json.get('video_url')
    audio_url = request.json.get('audio_url')
    subtitle_url = request.json.get('subtitle_url')

    if not video_url or not audio_url or not subtitle_url:
        return jsonify({"error": "video_url, audio_url, and subtitle_url are required"}), 400

    # Set file paths
    video_path = os.path.join(UPLOAD_FOLDER, "video.mp4")
    audio_path = os.path.join(UPLOAD_FOLDER, "audio.mp3")
    subtitle_path = os.path.join(UPLOAD_FOLDER, "subtitles.srt")
    output_path = os.path.join(UPLOAD_FOLDER, "merged_output_with_subtitles.mp4")

    try:
        # Download the video, audio, and subtitle files
        download_file(video_url, video_path)
        download_file(audio_url, audio_path)
        download_file(subtitle_url, subtitle_path)

        # Merge the video, audio, and subtitles
        merge_audio_video_with_subtitles(video_path, audio_path, subtitle_path, output_path)

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Clean up the downloaded files
        for file_path in [video_path, audio_path, subtitle_path, output_path]:
            if os.path.exists(file_path):
                os.remove(file_path)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
