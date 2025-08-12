import cv2
from pathlib import Path

def draw_boxes(image_path, label_path, class_names):
    img = cv2.imread(str(image_path))
    h, w = img.shape[:2]
    if not label_path.exists():
        return img
    with open(label_path) as f:
        for line in f:
            c, x, y, bw, bh = map(float, line.strip().split())
            c = int(c)
            x1 = int((x - bw/2) * w)
            y1 = int((y - bh/2) * h)
            x2 = int((x + bw/2) * w)
            y2 = int((y + bh/2) * h)
            cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)
            cv2.putText(img, class_names[c], (x1, max(0, y1-5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
    return img

if __name__ == "__main__":
    classes = ["normal_bin", "overflowing_bin"]
    img_dir = Path("data/images/sample")
    lbl_dir = Path("data/labels/sample")
    out_dir = Path("results/preview"); out_dir.mkdir(parents=True, exist_ok=True)

    for img in img_dir.glob("*.jpg"):
        lbl = lbl_dir / (img.stem + ".txt")
        vis = draw_boxes(img, lbl, classes)
        cv2.imwrite(str(out_dir / img.name), vis)
    print("[preview] wrote previews to results/preview")
