import runpod
import subprocess
import os
import uuid
import firebase_admin
from firebase_admin import credentials, storage

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-adminsdk.json")
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'wav2lip-dan.appspot.com'
    })

def handler(event):
    video_url = event['input']['video']
    audio_url = event['input']['audio']

    uid = str(uuid.uuid4())
    video_path = f"{uid}_video.mp4"
    audio_path = f"{uid}_audio.wav"
    output_path = f"{uid}_result.mp4"

    os.system(f"wget \"{video_url}\" -O {video_path}")
    os.system(f"wget \"{audio_url}\" -O {audio_path}")

    command = f"python3 inference.py --checkpoint_path checkpoints/wav2lip.pth --face {video_path} --audio {audio_path} --outfile {output_path}"
    subprocess.run(command, shell=True)

    # Upload result to Firebase
    bucket = storage.bucket()
    blob = bucket.blob(f"results/{uid}_result.mp4")
    blob.upload_from_filename(output_path)
    blob.make_public()
    firebase_url = blob.public_url

    return {
        "output": firebase_url
    }

runpod.serverless.start({"handler": handler})