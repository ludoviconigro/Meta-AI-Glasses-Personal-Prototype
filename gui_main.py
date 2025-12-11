# gui_main.py

import tkinter as tk
from tkinter.scrolledtext import ScrolledText

import cv2
from PIL import Image, ImageTk

from core.camera import start_camera, stop_camera, get_last_frame
from core.intents import handle_intent


class AssistantGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Assistente AI - Webcam + Chat (testo)")
        self.root.geometry("1100x700")

        # ============================
        #  LAYOUT PRINCIPALE
        # ============================
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Frame sinistro: webcam
        self.left_frame = tk.Frame(self.root, bg="black")
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        # Frame destro: chat
        self.right_frame = tk.Frame(self.root)
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        # ============================
        #  WEBCAM
        # ============================
        self.video_label = tk.Label(self.left_frame, bg="black")
        self.video_label.pack(fill="both", expand=True)

        # Reference all'immagine corrente per non farla garbage-collectare
        self.current_frame_image = None

        # ============================
        #  CHAT
        # ============================
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(1, weight=0)
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(1, weight=0)

        # Area testo scrollabile
        self.chat_box = ScrolledText(
            self.right_frame,
            state="disabled",
            wrap="word",
            font=("Helvetica", 11)
        )
        self.chat_box.grid(row=0, column=0, columnspan=2,
                           sticky="nsew", padx=5, pady=5)

        # Input text
        self.entry = tk.Entry(self.right_frame, font=("Helvetica", 12))
        self.entry.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.entry.bind("<Return>", self._on_send_text)

        # Bottone invio testo
        self.send_button = tk.Button(
            self.right_frame,
            text="Invia",
            command=self.on_send_text
        )
        self.send_button.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        # Messaggio iniziale
        self._append_chat(
            "ASSISTENTE",
            "Ciao, sono il tuo assistente. Scrivi un messaggio a destra. "
            "La webcam è sempre attiva sulla sinistra."
        )

        # Avvia loop aggiornamento webcam
        self.update_webcam_frame()

    # ============================
    #  GESTIONE CHAT
    # ============================

    def _append_chat(self, who: str, text: str):
        """Aggiunge una riga alla chat (Text read-only)."""
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", f"{who}: {text}\n")
        self.chat_box.see("end")
        self.chat_box.configure(state="disabled")

    def _handle_user_text(self, text: str):
        """Logica comune per input testuale."""
        if not text.strip():
            return

        self._append_chat("TU", text)
        response = handle_intent(text)
        self._append_chat("ASSISTENTE", response)

    def on_send_text(self):
        """Invio via bottone."""
        text = self.entry.get()
        self.entry.delete(0, "end")
        self._handle_user_text(text)

    def _on_send_text(self, event):
        """Invio via tasto Invio."""
        self.on_send_text()

    # ============================
    #  WEBCAM
    # ============================

    def update_webcam_frame(self):
        """
        Prende l'ultimo frame dalla CameraManager e lo mostra nella label.
        Viene richiamata in loop tramite .after().
        """
        frame = get_last_frame()
        if frame is not None:
            # frame è BGR (OpenCV) → converti in RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Ridimensiona per stare nella finestra
            h, w, _ = frame_rgb.shape
            max_width = 520
            max_height = 700
            scale = min(max_width / w, max_height / h, 1.0)
            new_w = int(w * scale)
            new_h = int(h * scale)

            frame_resized = cv2.resize(frame_rgb, (new_w, new_h))

            # Converti in immagine Tkinter
            img = Image.fromarray(frame_resized)
            imgtk = ImageTk.PhotoImage(image=img)

            self.current_frame_image = imgtk
            self.video_label.configure(image=imgtk)

        # Richiama se stessa dopo 30ms
        self.root.after(30, self.update_webcam_frame)

    # ============================
    #  CHIUSURA
    # ============================

    def on_close(self):
        """Chiusura finestra."""
        stop_camera()
        self.root.destroy()


def main():
    # Avvia la webcam una volta sola
    start_camera()

    root = tk.Tk()
    app = AssistantGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()


if __name__ == "__main__":
    main()
