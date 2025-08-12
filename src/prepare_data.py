import argparse
from pathlib import Path
import random
import shutil

def split_dataset(images_dir, labels_dir, out_images_train, out_images_val, out_labels_train, out_labels_val, val_ratio=0.2, seed=42):
    random.seed(seed)
    images = list(Path(images_dir).glob("*.jpg")) + list(Path(images_dir).glob("*.png"))
    random.shuffle(images)
    n_val = int(len(images) * val_ratio)
    val_set = set(images[:n_val])

    for img in images:
        lbl = Path(labels_dir) / (img.stem + ".txt")
        if img in val_set:
            shutil.copy2(img, out_images_val / img.name)
            if lbl.exists(): shutil.copy2(lbl, out_labels_val / lbl.name)
        else:
            shutil.copy2(img, out_images_train / img.name)
            if lbl.exists(): shutil.copy2(lbl, out_labels_train / lbl.name)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--images", default="data/images/all")
    p.add_argument("--labels", default="data/labels/all")
    p.add_argument("--val_ratio", type=float, default=0.2)
    args = p.parse_args()

    base = Path("data")
    (base / "images/train").mkdir(parents=True, exist_ok=True)
    (base / "images/val").mkdir(parents=True, exist_ok=True)
    (base / "labels/train").mkdir(parents=True, exist_ok=True)
    (base / "labels/val").mkdir(parents=True, exist_ok=True)

    split_dataset(
        args.images, args.labels,
        base / "images/train", base / "images/val",
        base / "labels/train", base / "labels/val",
        val_ratio=args.val_ratio
    )
    print("[data] split complete.")
