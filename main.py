# main.py

from core.voice import listen_streaming, speak
from core.intents import handle_intent
from core.camera import start_camera, stop_camera


def run_assistant():
    # Avvia la webcam una volta sola
    start_camera()

    speak("Ciao, sono il tuo assistente. Premi Invio per iniziare a parlare.")

    try:
        while True:
            input("👉 Premi INVIO per iniziare a parlare...")

            speak("Sto ascoltando. Premi di nuovo Invio per fermarti.")

            # Registrazione continua fino al secondo Invio
            text = listen_streaming()

            if not text:
                speak("Non ho capito, puoi ripetere?")
                continue

            response = handle_intent(text)

            if response:
                speak(response)
            else:
                speak("Non ho capito, puoi ripetere?")
    finally:
        # Alla chiusura del programma fermiamo la webcam
        stop_camera()


if __name__ == "__main__":
    run_assistant()
