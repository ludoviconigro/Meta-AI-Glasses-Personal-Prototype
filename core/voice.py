import sounddevice as sd
import soundfile as sf
import tempfile
import subprocess
import threading
import numpy as np
import speech_recognition as sr
from config import LANGUAGE


# ------------------------------------------------------------
# TTS NATIVO MACOS (COMANDO SAY)
# ------------------------------------------------------------
def speak(text: str):
    print(f"[ASSISTENTE]: {text}")

    try:
        sd.stop()
    except Exception:
        pass

    subprocess.run(["say", text])

    try:
        sd.stop()
    except Exception:
        pass


# ------------------------------------------------------------
# STREAMING AUDIO FINO A SECONDA PRESSIONE DI INVIO
# ------------------------------------------------------------
stop_recording_flag = False

def _stop_recording_input():
    """Thread che aspetta la seconda pressione di INVIO."""
    global stop_recording_flag
    input("")  # attende il secondo Invio
    stop_recording_flag = True


def listen_streaming(samplerate=16000, channels=1):
    """
    Registra audio in streaming finché l'utente non preme di nuovo Invio.
    Poi salva e converte in testo.
    """
    global stop_recording_flag
    stop_recording_flag = False

    frames = []

    try:
        sd.stop()
    except:
        pass

    print("[DEBUG] Registrazione avviata. Premi INVIO per fermarti.")

    # thread che ascolta il secondo invio
    stopper = threading.Thread(target=_stop_recording_input)
    stopper.start()

    def callback(indata, frames_count, time_info, status):
        if stop_recording_flag:
            raise sd.CallbackStop()
        frames.append(indata.copy())

    try:
        with sd.InputStream(samplerate=samplerate, channels=channels, dtype="int16", callback=callback):
            while not stop_recording_flag:
                sd.sleep(100)
    except sd.CallbackStop:
        pass
    except Exception as e:
        print(f"[ERRORE] durante la registrazione streaming: {e}")
        return ""

    # Converti stream in array numpy
    if not frames:
        print("[ERRORE] Nessun audio catturato.")
        return ""

    audio = np.concatenate(frames)

    # Salva in WAV temporaneo
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    sf.write(tmp_file.name, audio, samplerate)
    tmp_file.close()

    # Ora riconosci il parlato
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(tmp_file.name) as source:
            audio_data = recognizer.record(source)
    except Exception as e:
        print(f"[ERRORE] lettura file audio: {e}")
        return ""

    try:
        text = recognizer.recognize_google(audio_data, language=LANGUAGE)
        print(f"[TU]: {text}")
        return text.lower()

    except sr.UnknownValueError:
        speak("Non ho capito, puoi ripetere?")
        return ""

    except sr.RequestError:
        speak("Problemi di connessione al servizio di riconoscimento vocale.")
        return ""

    except Exception as e:
        print(f"[ERRORE] riconoscimento vocale: {e}")
        return ""

