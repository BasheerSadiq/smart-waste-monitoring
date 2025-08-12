import argparse
import subprocess
from pathlib import Path
from git import Repo

YOLOV5_DIR = Path(".yolov5")
YOLOV5_REPO = "https://github.com/ultralytics/yolov5.git"

def ensure_yolov5():
    if not YOLOV5_DIR.exists():
        print(f"[setup] Cloning YOLOv5 into {YOLOV5_DIR} ...")
        Repo.clone_from(YOLOV5_REPO, YOLOV5_DIR)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/dataset.yaml")
    ap.add_argument("--weights", default="weights/best.pt")
    ap.add_argument("--img", type=int, default=640)
    ap.add_argument("--batch", type=int, default=16)
    args = ap.parse_args()

    ensure_yolov5()
    cmd = [
        "python", str(YOLOV5_DIR / "val.py"),
        "--data", args.data,
        "--weights", args.weights,
        "--img", str(args.img),
        "--batch-size", str(args.batch),
        "--task", "val"
    ]
    print("[eval]", " ".join(cmd))
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    main()
