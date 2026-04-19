# 🚦 Road Sign Detection – ML Training Pipeline

Pipeline do fine-tuningu modelu YOLOv11 na zadanie detekcji znaków drogowych z bounding boxami.

## Architektura

```
ml/
├── pyproject.toml              # Zależności projektu (uv)
├── configs/
│   └── train_config.yaml       # Hiperparametry treningu
├── data/
│   └── dataset.yaml            # Konfiguracja datasetu YOLO
├── notebooks/
│   └── exploration.ipynb       # Eksploracja datasetu i wizualizacja predykcji
├── scripts/
│   ├── prepare_dataset.py      # Pobranie i konwersja datasetu do formatu YOLO
│   ├── train.py                # Skrypt treningowy
│   ├── evaluate.py             # Ewaluacja modelu
│   └── export_model.py         # Eksport do ONNX
└── src/
    ├── __init__.py
    ├── dataset_converter.py    # Konwersja adnotacji do formatu YOLO
    ├── label_mapping.py        # Mapowanie klas znaków drogowych
    └── visualize.py            # Wizualizacja predykcji
```

## Szybki start

### 1. Instalacja zależności

```bash
cd ml
uv sync
```

### 2. Przygotowanie datasetu

Skrypt pobierze German Traffic Sign Detection Benchmark (GTSDB) i skonwertuje
adnotacje do formatu YOLO:

```bash
uv run python scripts/prepare_dataset.py
```

### 3. Trening modelu

```bash
uv run python scripts/train.py
```

Konfiguracja treningu znajduje się w `configs/train_config.yaml`.

### 4. Ewaluacja

```bash
uv run python scripts/evaluate.py --weights runs/detect/train/weights/best.pt
```

### 5. Eksport do ONNX

```bash
uv run python scripts/export_model.py --weights runs/detect/train/weights/best.pt
```

## Notebook

Interaktywna eksploracja datasetu i wizualizacja predykcji:

```bash
cd ml
uv run jupyter notebook notebooks/exploration.ipynb
```

Notebook zawiera:
- Przegląd mapowania 43 klas
- Wizualizację obrazów z nałożonymi bounding boxami (YOLO labels)
- Rozkład klas i rozmiarów bboxów
- Predykcje modelu + porównanie GT vs prediction
- Histogram confidence per klasa
- Inferencję przez ONNX Runtime

## Dataset

Używamy **GTSDB** (German Traffic Sign Detection Benchmark) który zawiera:
- 900 obrazów treningowych (1360×800)
- **43 klasy znaków drogowych** rozpoznawane indywidualnie, m.in.:
  - Ograniczenia prędkości (20, 30, 50, 60, 70, 80, 100, 120 km/h)
  - Stop, Yield, No entry, No vehicles
  - Znaki nakazu (ahead only, keep right/left, roundabout…)
  - Znaki ostrzegawcze (road work, children crossing, slippery road…)
  - Pełna lista w `data/dataset.yaml`

## Model bazowy

**YOLOv11n** (nano) – szybki, lekki, idealny do fine-tuningu.
Można zmienić na większy wariant (s/m/l/x) w `configs/train_config.yaml`.

## Wyniki

Po treningu wyniki znajdziesz w `runs/detect/train/`:
- `weights/best.pt` – najlepszy model
- `weights/last.pt` – ostatni checkpoint
- `results.csv` – metryki per epoka
- `confusion_matrix.png` – macierz pomyłek
- `val_batch*_pred.jpg` – predykcje na zbiorze walidacyjnym

