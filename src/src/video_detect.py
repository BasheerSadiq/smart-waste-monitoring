import argparse, cv2, time
from pathlib import Path
import torch
from iot_alert import send_alert

def load_model(weights):
    m = torch.hub.load("ultralytics/yolov5","custom",path=weights,force_reload=False)
    m.conf = 0.25
    return m

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--weights", default="weights/best.pt")
    ap.add_argument("--source", default="0", help="0 webcam | path to video")
    ap.add_argument("--conf", type=float, default=0.25)
    ap.add_argument("--record", action="store_true", help="save annotated mp4")
    ap.add_argument("--alert", action="store_true")
    args = ap.parse_args()

    model = load_model(args.weights); model.conf = args.conf

    cap = cv2.VideoCapture(0 if args.source=="0" else args.source)
    if not cap.isOpened():
        raise SystemExit(f"cannot open source: {args.source}")

    writer = None
    if args.record:
        Path("results/video").mkdir(parents=True, exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = cap.get(cv2.CAP_PROP_FPS) or 25
        w, h = int(cap.get(3)), int(cap.get(4))
        writer = cv2.VideoWriter("results/video/output.mp4", fourcc, fps, (w,h))

    while True:
        ok, frame = cap.read()
        if not ok: break
        results = model(frame, size=640)
        # draw boxes on frame
        annotated = results.render()[0]

        if args.alert:
            names = results.names
            for *xyxy, conf, cls in results.pred[0].tolist():
                label = names[int(cls)]
                if label == "overflowing_bin":
                    send_alert(label, conf, "stream", use_mqtt=False)

        if writer: writer.write(annotated)
        cv2.imshow("Waste Monitor", annotated)
        if cv2.waitKey(1)&0xFF==27: break  # ESC to quit

    cap.release()
    if writer: writer.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
