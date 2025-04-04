from flask import Flask, request, jsonify
import subprocess
import os
import uuid

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    video_url = data.get("video")
    audio_url = data.get("audio")

    uid = str(uuid.uuid4())
    video_path = f"{uid}_video.mp4"
    audio_path = f"{uid}_audio.wav"
    output_path = f"{uid}_result.mp4"

    os.system(f"wget {video_url} -O {video_path}")
    os.system(f"wget {audio_url} -O {audio_path}")

    command = f"python3 inference.py --checkpoint_path checkpoints/wav2lip.pth --face {video_path} --audio {audio_path} --outfile {output_path}"
    subprocess.run(command, shell=True)

    return jsonify({
        "output": output_path
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
# Triggering rebuild on RunPod
