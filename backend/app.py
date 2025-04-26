from flask import Flask, request, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')

    # Basic sanity check
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    try:
        # Custom filename
        filename = "output.mp4"
        filepath = os.path.join("/home/ArcherArjunG/vidzo", filename)

        ydl_opts = {
            'format': 'bv*[height<=1080]+ba/b[height<=1080]',
            'outtmpl': filepath,
            'merge_output_format': 'mp4',
            'postprocessor_args': ['-c:v', 'libx264', '-c:a', 'aac', '-b:a', '192k'],
            'noplaylist': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.download([url])

        # Check file size
        size_bytes = os.path.getsize(filepath)
        if size_bytes > 100 * 1024 * 1024:
            os.remove(filepath)
            return jsonify({"error": "We are currently experiencing backend issues, due to this the convertible file size is 100MB, please provide a smaller length video. We are Sorry for the inconvenience"}), 400

        return send_file(filepath, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
