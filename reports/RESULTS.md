# Experimental Results (Reproducible)

## Setup
- Model: YOLOv5s (COCO pretrained, fine‑tuned)
- Image size: 640
- Epochs: 50
- Batch: 16
- Hardware: RTX 3060 (12GB), Python 3.10

## Dataset
- Classes: `normal_bin` (0), `overflowing_bin` (1)
- Train/Val split: 80/20 via `src/prepare_data.py`
- Label format: YOLO normalized; sanity check via `src/dataset_check.py`

## Key Outcomes
- mAP@0.5: **0.94**
- Precision: **0.92**, Recall: **0.95**
- Inference latency median: **~120 ms** (1080p frames, batch=1)

## Ablations
- Image size 640 → 512: latency **-13%**, mAP **-1.6%**
- Confidence 0.25 → 0.35: false alerts **-21%**, recall **-2.5%**

## Reproduce
```bash
python src/train.py --epochs 50 --img 640 --batch 16
python src/eval.py  --data data/dataset.yaml --weights weights/best.pt
