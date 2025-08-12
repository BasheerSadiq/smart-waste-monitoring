FROM python:3.10-slim

# System deps
RUN apt-get update && apt-get install -y git ffmpeg libsm6 libxext6 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Pre-clone YOLOv5 for faster first run
RUN python - <<'PY'
from git import Repo
from pathlib import Path
dir = Path(".yolov5")
if not dir.exists():
    Repo.clone_from("https://github.com/ultralytics/yolov5.git", dir)
PY

CMD ["bash"]
