import os
import ffmpeg
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/merge_media', methods=['POST'])
def merge_media():
    # Get URLs for video, audio, and subtitles from request JSON body
    data = request.get_json()
    video_url = data.get('video_url')
    audio_url = data.get('audio_url')
    subtitle_url = data.get('subtitle_url')

    # Check if URLs are provided
    if not video_url or not audio_url or not subtitle_url:
        return jsonify({"error": "Missing video, audio, or subtitle URL"}), 400

    # Define output file
    output_file = "merged_output.mp4"

    # Download the files from URLs
    try:
        # Load video, audio, and subtitles into ffmpeg
        input_video = ffmpeg.input(video_url)
        input_audio = ffmpeg.input(audio_url)
        input_subtitles = ffmpeg.input(subtitle_url)

        # Merge video, audio, and subtitles
        ffmpeg.concat(input_video, input_audio, input_subtitles, v=1, a=1).output(output_file).run()
        
        # Respond with a success message
        return jsonify({"message": "Media merged successfully", "output_file": output_file}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Use the PORT environment variable or default to 8000
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
