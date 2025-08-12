from pathlib import Path

def check_labels(labels_dir: Path, classes=2):
    issues = 0
    for txt in labels_dir.glob("*.txt"):
        with txt.open() as f:
            for i, line in enumerate(f, start=1):
                parts = line.strip().split()
                if len(parts) != 5:
                    print(f"[warn] {txt}:{i} -> expected 5 items, got {len(parts)}")
                    issues += 1
                    continue
                cid, *box = parts
                try:
                    cid = int(cid)
                except ValueError:
                    print(f"[warn] {txt}:{i} class id not int: {cid}")
                    issues += 1
                if cid < 0 or cid >= classes:
                    print(f"[warn] {txt}:{i} class id out of range [0,{classes-1}]: {cid}")
                    issues += 1
                for v in box:
                    try:
                        fv = float(v)
                        if fv < 0 or fv > 1:
                            print(f"[warn] {txt}:{i} normalized value out of [0,1]: {fv}")
                            issues += 1
                    except ValueError:
                        print(f"[warn] {txt}:{i} non-float value: {v}")
                        issues += 1
    if issues == 0:
        print("[ok] labels look good.")
    else:
        print(f"[done] found {issues} potential issues.")

if __name__ == "__main__":
    check_labels(Path("data/labels/train"))
    check_labels(Path("data/labels/val"))
