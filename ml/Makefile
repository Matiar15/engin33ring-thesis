ml-prepare:
	uv run --active python scripts/prepare_dataset.py

ml-train:
	uv run --active python scripts/train.py

ml-evaluate:
	uv run --active python scripts/evaluate.py --weights /home/matiar/Programming/engin33ring-thesis/runs/detect/runs/detect/train/weights/best.pt

ml-export:
	uv run --active python scripts/export_model.py --weights /home/matiar/Programming/engin33ring-thesis/runs/detect/runs/detect/train/weights/best.pt
