.PHONY: setup train detect lint

setup:
	python -m venv .env && \
	. .env/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt

train:
	python src/train.py --epochs 50 --img 640 --batch 16

detect:
	python src/detect.py --weights weights/best.pt --source data/images/sample/ --conf 0.25 --alert

lint:
	python -m pip install ruff && ruff check src
