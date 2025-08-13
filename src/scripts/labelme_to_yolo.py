"""
Convert LabelMe JSON annotations to YOLO txt format (1 class or multi-class).
Usage:
  python scripts/labelme_to_yolo.py --in data/labelme --out data --classes normal_bin overflowing_bin
"""
import json, argparse
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", dest="out", required=True)
    ap.add_argument("--classes", nargs="+", required=True)
    args = ap.parse_args()

    inp, out = Path(args.inp), Path(args.out)
    (out/"labels/all").mkdir(parents=True, exist_ok=True)
    for jf in inp.glob("*.json"):
        data = json.loads(jf.read_text())
        H, W = data["imageHeight"], data["imageWidth"]
        lines = []
        for s in data.get("shapes", []):
            cls = s["label"]; pts = s["points"]
            if cls not in args.classes: continue
            xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
            x1,y1,x2,y2 = min(xs),min(ys),max(xs),max(ys)
            x = ((x1+x2)/2)/W; y = ((y1+y2)/2)/H
            w = (x2-x1)/W; h = (y2-y1)/H
            cid = args.classes.index(cls)
            lines.append(f"{cid} {x:.6f} {y:.6f} {w:.6f} {h:.6f}")
        (out/"labels/all"/(jf.stem+".txt")).write_text("\n".join(lines))
    print("[convert] done.")
if __name__ == "__main__":
    main()
