import argparse, subprocess
from pathlib import Path
from git import Repo

YOLOV5_DIR = Path(".yolov5")
YOLOV5_REPO = "https://github.com/ultralytics/yolov5.git"
YOLOV5_COMMIT = "e8f3bd0"  

def ensure_yolov5():
    if not YOLOV5_DIR.exists():
        print(f"[setup] cloning YOLOv5…")
        Repo.clone_from(YOLOV5_REPO, YOLOV5_DIR)
    Repo(YOLOV5_DIR).git.checkout(YOLOV5_COMMIT)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--weights", default="weights/best.pt")
    ap.add_argument("--img", type=int, default=640)
    ap.add_argument("--opset", type=int, default=12)
    ap.add_argument("--half", action="store_true")
    ap.add_argument("--format", choices=["onnx","torchscript"], default="onnx")
    args = ap.parse_args()

    ensure_yolov5()
    export_py = YOLOV5_DIR / "export.py"
    cmd = [
        "python", str(export_py),
        "--weights", args.weights,
        "--imgsz", str(args.img),
        "--include", args.format,
        "--opset", str(args.opset)
    ]
    if args.half: cmd += ["--half"]
    print("[export]", " ".join(cmd))
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    main()
