import runpod
import subprocess
import os
import uuid

def handler(event):
    video_url = event['input']['video']
    audio_url = event['input']['audio']

    uid = str(uuid.uuid4())
    video_path = f"{uid}_video.mp4"
    audio_path = f"{uid}_audio.wav"
    output_path = f"{uid}_result.mp4"

    # Download input files
    os.system(f"wget \"{video_url}\" -O {video_path}")
    os.system(f"wget \"{audio_url}\" -O {audio_path}")

    # Run Wav2Lip inference
    command = f"python3 inference.py --checkpoint_path checkpoints/wav2lip.pth --face {video_path} --audio {audio_path} --outfile {output_path}"
    subprocess.run(command, shell=True)

    # You would normally upload result to a public URL (e.g. Firebase or S3)
    # For now, return just the filename
    return {
        "output": output_path
    }

runpod.serverless.start({"handler": handler})