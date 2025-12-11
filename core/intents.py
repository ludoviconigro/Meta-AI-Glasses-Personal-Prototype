# core/intents.py

from skills.weather import handle_weather_query
from core.llm import ask_llm

from skills.vision import analyze_frame, describe_objects
from core.camera import get_last_frame

from core.keywords import (
    calc_keywords,
    weather_keywords,
    greetings_keywords,
    vision_keywords,
)


def clean_text(text: str) -> str:
    """Rimuove duplicati consecutivi tipo 'roma roma' → 'roma'."""
    words = text.split()
    cleaned = []
    for w in words:
        if not cleaned or cleaned[-1] != w:
            cleaned.append(w)
    return " ".join(cleaned)


def _match_phrase(text: str, phrases: list[str]) -> bool:
    """True se almeno una frase è contenuta nel testo."""
    lowered = text.lower()
    for p in phrases:
        if p.lower() in lowered:
            return True
    return False


def handle_vision_query(text: str) -> str:
    """
    Gestisce le domande tipo:
    - 'cos'è quell'oggetto'
    - 'cosa sto inquadrando'
    - 'cosa vedi'
    """
    print(f"[INTENTS] Vision intent attivato per testo: {text!r}")

    frame = get_last_frame()
    if frame is None:
        print("[INTENTS] Nessun frame disponibile dalla camera.")
        return "Non vedo nessuna immagine dalla fotocamera al momento."

    print("[INTENTS] Frame ottenuto, eseguo analisi YOLO...")
    objects = analyze_frame(frame)
    print(f"[INTENTS] Oggetti trovati: {objects}")

    return describe_objects(objects)


def handle_intent(text: str) -> str:
    """
    Gestisce tutte le richieste dell'utente:
    - saluti
    - meteo
    - riconoscimento oggetti con la fotocamera
    - calcolatrice (attualmente disattivata)
    - fallback → LLM
    """
    if not text:
        return "Non ho capito, puoi ripetere?"

    text = text.lower().strip()
    text = clean_text(text)
    print(f"[INTENTS] Testo pulito: {text!r}")

    # ============================================================
    # SALUTI
    # ============================================================
    if any(word in text.split() for word in greetings_keywords):
        print("[INTENTS] Intent: saluto")
        return "Dimmi pure, sono qui."

    # ============================================================
    # VISIONE / RICONOSCIMENTO OGGETTI
    # ============================================================
    if _match_phrase(text, vision_keywords):
        print("[INTENTS] Intent: visione")
        return handle_vision_query(text)

    # ============================================================
    # METEO
    # ============================================================
    if any(word in text for word in weather_keywords):
        print("[INTENTS] Intent: meteo")
        return handle_weather_query(text)

    # ============================================================
    # CALCOLATRICE (momentaneamente disattivata)
    # ============================================================
    # if any(keyword in text for keyword in calc_keywords):
    #     return handle_calculator(text)
    #
    # if any(char in text for char in "+-*/^()"):
    #     return handle_calculator(text)

    # ============================================================
    # FALLBACK → LLM
    # ============================================================
    print("[INTENTS] Intent: fallback LLM")
    return ask_llm(text)
