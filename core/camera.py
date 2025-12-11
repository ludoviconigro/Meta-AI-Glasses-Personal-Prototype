# core/camera.py

import threading
import time
from typing import Optional

import cv2


class CameraManager:
    """
    Gestisce la webcam in un thread separato.
    Mantiene sempre l'ultimo frame disponibile.
    """

    def __init__(self, camera_index: int = 0):
        self.camera_index = camera_index
        self._cap: Optional[cv2.VideoCapture] = None
        self._thread: Optional[threading.Thread] = None
        self._running: bool = False
        self._last_frame = None
        self._lock = threading.Lock()

    def start(self):
        """Avvia la lettura continua dalla webcam."""
        if self._running:
            return

        self._cap = cv2.VideoCapture(self.camera_index)
        if not self._cap.isOpened():
            print("[CAMERA] Impossibile aprire la webcam.")
            return

        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        print("[CAMERA] Webcam avviata.")

    def _loop(self):
        """Loop interno che legge continuamente i frame."""
        while self._running:
            if self._cap is None:
                time.sleep(0.05)
                continue

            ret, frame = self._cap.read()
            if not ret:
                time.sleep(0.05)
                continue

            with self._lock:
                self._last_frame = frame

        # Pulizia alla fine
        if self._cap is not None:
            self._cap.release()
            self._cap = None
        print("[CAMERA] Webcam fermata.")

    def stop(self):
        """Ferma la webcam e il thread."""
        self._running = False

    def get_last_frame(self):
        """
        Ritorna l'ultimo frame disponibile (numpy array BGR) oppure None
        se non c'è ancora nessun frame.
        """
        with self._lock:
            if self._last_frame is None:
                return None
            return self._last_frame.copy()

    def is_running(self) -> bool:
        return self._running


# Istanza globale riutilizzabile in tutto il progetto
_camera_manager: Optional[CameraManager] = None


def get_camera_manager() -> CameraManager:
    global _camera_manager
    if _camera_manager is None:
        _camera_manager = CameraManager(camera_index=0)
    return _camera_manager


def start_camera():
    """Helper per avviare la webcam dal main."""
    manager = get_camera_manager()
    manager.start()


def stop_camera():
    """Helper per fermare la webcam (se ti serve alla chiusura)."""
    manager = get_camera_manager()
    manager.stop()


def get_last_frame():
    """Helper per ottenere l'ultimo frame."""
    manager = get_camera_manager()
    return manager.get_last_frame()
