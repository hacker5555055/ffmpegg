from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return "FFmpeg is running on Render.com!"

@app.route('/ffmpeg-test')
def ffmpeg_test():
    try:
        # Run an FFmpeg command to check if it works
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        return jsonify({
            "ffmpeg_version": result.stdout
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
