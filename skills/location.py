# skills/location.py

import requests

# ============================================================
# 1) Rilevamento posizione automatica (IP)
# ============================================================
def get_current_city():
    """
    Geolocalizzazione precisa usando IP.
    Priorità:
    1) ipapi.co  (più preciso)
    2) ipwho.is  (backup)
    """
    # --- 1) ipapi.co ---
    try:
        r = requests.get("https://ipapi.co/json/").json()
        city = r.get("city")
        if city:
            return city
    except:
        pass

    # --- 2) ipwho.is ---
    try:
        r = requests.get("https://ipwho.is/").json()
        city = r.get("city")
        if city:
            return city
    except:
        pass

    return None


# ============================================================
# 2) Ripulisce il testo per ottenere la città
# ============================================================
def clean_city(text):
    stopwords = [
        "che", "tempo", "fa", "oggi", "domani", "c'è", "ce",
        "meteo", "piove", "pioggia", "neve", "nevica",
        "vento", "ventoso", "forte", "debole",
        "il", "la", "lo", "di", "a", "ad"
    ]

    parts = text.split()
    cleaned = [w for w in parts if w not in stopwords]

    if not cleaned:
        return None

    if cleaned[0] in stopwords:
        return None

    return cleaned[0].capitalize()


# ============================================================
# 3) Estrae la città dalla frase (stile Alexa)
# ============================================================
def extract_city(query: str):
    query = query.lower().strip()

    if query.startswith("a "):
        c = clean_city(query[2:].strip())
        if c: return c

    if query.startswith("ad "):
        c = clean_city(query[3:].strip())
        if c: return c

    if " a " in query:
        c = clean_city(query.split(" a ")[1])
        if c: return c

    if " di " in query:
        c = clean_city(query.split(" di ")[1])
        if c: return c

    first = query.split()[0]
    stop = ["che", "come", "fa", "oggi", "domani", "il", "la", "c'è", "meteo", "a", "ad", "di"]
    if first not in stop:
        c = clean_city(first)
        if c: return c

    return None


# ============================================================
# 4) Geocoding tramite Open-Meteo (gratis)
# ============================================================
def get_coordinates(city: str):
    """
    Usa Open-Meteo Geocoding (100% gratuito, no limiti, stabile).
    """
    url = (
        f"https://geocoding-api.open-meteo.com/v1/search?"
        f"name={city}&count=1&language=it&format=json"
    )

    try:
        data = requests.get(url).json()
        results = data.get("results")
        if not results:
            return None, None

        lat = results[0]["latitude"]
        lon = results[0]["longitude"]
        return lat, lon

    except:
        return None, None
