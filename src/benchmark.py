import argparse, time, torch, cv2, numpy as np
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--weights", default="weights/best.pt")
    p.add_argument("--warmup", type=int, default=5)
    p.add_argument("--iters", type=int, default=50)
    args = p.parse_args()

    model = torch.hub.load("ultralytics/yolov5","custom",path=args.weights)
    dummy = np.zeros((640,640,3), dtype=np.uint8)

    for _ in range(args.warmup): model(dummy, size=640)

    t0 = time.time()
    for _ in range(args.iters): model(dummy, size=640)
    dt = (time.time()-t0)/args.iters
    print(f"median-ish latency ~{dt*1000:.1f} ms | ~{1/dt:.2f} FPS")
if __name__ == "__main__":
    main()
