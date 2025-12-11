# skills/weather.py

import requests
from skills.location import (
    extract_city,
    clean_city,
    get_current_city,
    get_coordinates
)

# ============================================================
# METEO — API MET Norway
# ============================================================
def get_weather(city: str):

    lat, lon = get_coordinates(city)
    if not lat:
        return None

    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={lon}"
    headers = {"User-Agent": "LudoAssistant/1.0"}

    try:
        data = requests.get(url, headers=headers).json()
    except:
        return None

    timeseries = data["properties"]["timeseries"]

    today = timeseries[0]
    tomorrow = timeseries[24] if len(timeseries) > 24 else timeseries[-1]

    today_details = today["data"].get("next_1_hours", {}).get("details", {})
    today_instant = today["data"].get("instant", {}).get("details", {})

    tomorrow_details = tomorrow["data"].get("next_6_hours", {}).get("details", {})
    tomorrow_instant = tomorrow["data"].get("instant", {}).get("details", {})

    today_symbol = today["data"].get("next_1_hours", {}).get("summary", {}).get("symbol_code", "")
    tomorrow_symbol = tomorrow["data"].get("next_6_hours", {}).get("summary", {}).get("symbol_code", "")

    return {
        # OGGI
        "temp": today_instant.get("air_temperature"),
        "feels_like": today_instant.get("air_temperature_feels_like"),
        "wind": today_instant.get("wind_speed"),
        "rain": today_details.get("precipitation_amount", 0) > 0,
        "snow": "snow" in today_symbol,
        "fog": "fog" in today_symbol,
        "storm": "storm" in today_symbol,

        # DOMANI
        "tomorrow_min": tomorrow_details.get("air_temperature_min"),
        "tomorrow_max": tomorrow_details.get("air_temperature_max"),
        "tomorrow_rain": tomorrow_details.get("precipitation_amount", 0) > 0,
        "tomorrow_snow": "snow" in tomorrow_symbol,
        "tomorrow_fog": "fog" in tomorrow_symbol,
        "tomorrow_storm": "storm" in tomorrow_symbol,
    }


# ============================================================
# Risposta meteo stile Alexa
# ============================================================
def handle_weather_query(query: str) -> str:
    query = query.lower().strip()

    city = extract_city(query)
    if not city:
        city = get_current_city()
        if not city:
            return "Non ho capito la città e non so dove sei."

    is_tomorrow = "domani" in query

    ask_rain = "piove" in query or "pioggia" in query
    ask_snow = "neve" in query or "nevica" in query
    ask_wind = "vento" in query or "ventoso" in query
    ask_feel = "percepita" in query or "sembra" in query

    weather = get_weather(city)
    if not weather:
        return f"Non trovo il meteo di {city}."

    # --- Pioggia ---
    if ask_rain:
        if is_tomorrow:
            return (f"Sì, domani a {city} è prevista pioggia."
                    if weather["tomorrow_rain"]
                    else f"No, domani a {city} non dovrebbe piovere.")
        else:
            return (f"Sì, oggi a {city} piove."
                    if weather["rain"]
                    else f"No, oggi a {city} non dovrebbe piovere.")

    # --- Neve ---
    if ask_snow:
        if is_tomorrow:
            return (f"Sì, domani a {city} è prevista neve."
                    if weather["tomorrow_snow"]
                    else f"No, domani a {city} non nevicherà.")
        else:
            return (f"Sì, oggi a {city} nevica."
                    if weather["snow"]
                    else f"No, oggi a {city} non nevica.")

    # --- Vento ---
    if ask_wind:
        wind = weather["wind"]
        if wind >= 40:
            level = "vento fortissimo"
        elif wind >= 25:
            level = "vento forte"
        elif wind >= 10:
            level = "vento moderato"
        else:
            level = "vento debole"

        return f"Domani a {city} ci sarà {level}." if is_tomorrow else f"Oggi a {city} c'è {level}."

    # --- Temperatura percepita ---
    if ask_feel:
        return f"A {city} la temperatura percepita è di {weather['feels_like']} gradi."

    # --- Domani ---
    if is_tomorrow:
        return (
            f"Domani a {city} ci saranno tra "
            f"{weather['tomorrow_min']} e {weather['tomorrow_max']} gradi."
        )

    # --- Oggi ---
    return f"A {city} ci sono {weather['temp']} gradi e vento a {weather['wind']} km/h."
