FROM nvidia/cuda:11.3.1-cudnn8-runtime-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libsm6 \
    libxext6 \
    wget \
    python3 \
    python3-pip \
    python3-dev \
    && apt-get clean

WORKDIR /app

COPY . /app

RUN pip3 install --upgrade pip
# RUN pip3 install -r requirements.txt
RUN pip3 install librosa moviepy flask

# Download pretrained Wav2Lip model
RUN apt-get install -y curl && \
    mkdir -p checkpoints && \
    curl -L "https://storage.googleapis.com/wav2lip-pretrained/Wav2Lip.pth" -o checkpoints/wav2lip.pth

EXPOSE 5000

CMD ["python3", "server.py"]
