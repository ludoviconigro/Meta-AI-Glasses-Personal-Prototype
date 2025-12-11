# skills/vision.py

from typing import List, Optional

import numpy as np
from ultralytics import YOLO


# Modello caricato una sola volta (lazy)
_model: Optional[YOLO] = None


def _load_model():
    """Carica il modello YOLOv8n una sola volta."""
    global _model
    if _model is None:
        print("[VISION] Caricamento modello YOLOv8n...")
        # Modello nano (più leggero) e gratuito
        _model = YOLO("yolov8n.pt")
        print("[VISION] Modello YOLOv8n caricato.")


def analyze_frame(frame: np.ndarray, conf_threshold: float = 0.4) -> List[str]:
    """
    Prende un frame BGR (OpenCV) e restituisce una lista di nomi oggetti riconosciuti.
    Esempio: ["person", "cup", "laptop"]
    """
    if frame is None:
        return []

    _load_model()
    assert _model is not None

    # Esegui l'inferenza
    results = _model.predict(source=frame, verbose=False)

    if not results:
        return []

    result = results[0]  # primo (e unico) risultato
    names = _model.names  # mapping class_id -> name

    found_labels: List[str] = []

    if result.boxes is not None:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            if conf < conf_threshold:
                continue

            label = names.get(cls_id, f"class_{cls_id}")
            found_labels.append(label)

    # Restituisci nomi unici, preservando l'ordine
    unique_labels: List[str] = []
    for label in found_labels:
        if label not in unique_labels:
            unique_labels.append(label)

    return unique_labels


def describe_objects(objects: List[str]) -> str:
    """
    Trasforma la lista di oggetti in una frase in italiano.
    """
    if not objects:
        return "Non riesco a riconoscere chiaramente cosa stai inquadrando."

    if len(objects) == 1:
        return f"Mi sembra che tu stia inquadrando principalmente: {objects[0]}."

    # Prendiamo i primi 3 per non fare elenchi infiniti
    main_objs = ", ".join(objects[:3])
    return f"Vedo principalmente: {main_objs}."
