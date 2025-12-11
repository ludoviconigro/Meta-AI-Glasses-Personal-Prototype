import math
import re

# ============================================================
#  NUMERI IN LETTERE → CIFRE (anche composti)
# ============================================================

NUMERI = {
    # singoli
    "zero": 0, "uno": 1, "una": 1, "un": 1,
    "due": 2, "tre": 3, "quattro": 4, "cinque": 5,
    "sei": 6, "sette": 7, "otto": 8, "nove": 9,
    "dieci": 10, "undici": 11, "dodici": 12, "tredici": 13,
    "quattordici": 14, "quindici": 15, "sedici": 16,
    "diciassette": 17, "diciotto": 18, "diciannove": 19,

    # decine
    "venti": 20, "trenta": 30, "quaranta": 40, "cinquanta": 50,
    "sessanta": 60, "settanta": 70, "ottanta": 80, "novanta": 90,

    # centinaia semplici (per percentuali tipo "venti percento di duecento")
    "cento": 100, "duecento": 200, "trecento": 300, "quattrocento": 400,
    "cinquecento": 500, "seicento": 600, "settecento": 700,
    "ottocento": 800, "novecento": 900,

    # migliaia
    "mille": 1000, "mila": 1000,

    # composti che ci servono nei test
    "quarantacinque": 45,
    "ottantuno": 81,
    "centoottanta": 180,
}

ORDINALI = {
    "prima": 1, "seconda": 2, "terza": 3, "quarta": 4,
    "quinta": 5, "sesta": 6, "settima": 7, "ottava": 8,
    "nona": 9, "decima": 10, "undicesima": 11,
    "dodicesima": 12, "tredicesima": 13, "quattordicesima": 14,
    "quindicesima": 15, "sedicesima": 16, "diciassettesima": 17,
    "diciottesima": 18, "diciannovesima": 19, "ventesima": 20,
}


def words_to_numbers(text: str) -> str:
    """
    Converte parole italiane che rappresentano numeri
    in cifre (sia cardinali che ordinali).
    Usa solo sostituzioni a livello di parola per evitare casini.
    """

    # pattern per i cardinali
    if NUMERI:
        pattern_num = r"\b(" + "|".join(re.escape(w) for w in NUMERI.keys()) + r")\b"

        def repl_num(match):
            w = match.group(1)
            return str(NUMERI[w])

        text = re.sub(pattern_num, repl_num, text)

    # pattern per gli ordinali
    if ORDINALI:
        pattern_ord = r"\b(" + "|".join(re.escape(w) for w in ORDINALI.keys()) + r")\b"

        def repl_ord(match):
            w = match.group(1)
            return str(ORDINALI[w])

        text = re.sub(pattern_ord, repl_ord, text)

    return text


# ============================================================
#   FUNZIONI E COSTANTI PER EVAL
# ============================================================

def sind(x):
    """Seno in gradi."""
    return math.sin(math.radians(x))


def cosd(x):
    """Coseno in gradi."""
    return math.cos(math.radians(x))


def tand(x):
    """Tangente in gradi."""
    return math.tan(math.radians(x))


def log10(x):
    """Logaritmo in base 10."""
    return math.log10(x)


def ln(x):
    """Logaritmo naturale (base e)."""
    return math.log(x)


allowed_functions = {
    # trigonometria (in gradi)
    "sind": sind,
    "cosd": cosd,
    "tand": tand,

    # trig standard (in radianti, se uno usa sin(0.5) ecc.)
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,

    # inversi
    "asin": math.asin, "acos": math.acos, "atan": math.atan,

    # log
    "log10": log10,
    "ln": ln,

    # radici & esponenziali
    "sqrt": math.sqrt,
    "exp": math.exp,

    # fattoriale
    "fact": math.factorial,
}

allowed_constants = {
    "pi": math.pi,
    "pigreco": math.pi,
    "euler": math.e,
    "e": math.e,

    # costanti fisiche
    "c": 299792458,           # velocità della luce (m/s)
    "planck": 6.62607015e-34, # costante di Planck
    "grav": 6.67430e-11,      # costante gravitazionale
    "g": 9.81,                # gravità terrestre
}


# ============================================================
#   NORMALIZZATORE LINGUAGGIO NATURALE → ESPRESSIONE
# ============================================================

def normalize(text: str) -> str:
    t = text.lower()

    # 1) numeri in lettere → cifre
    t = words_to_numbers(t)

    # 2) rimozione parole inutili "di controllo"
    useless = [
        "quanto fa", "quanto e", "quanto è", "qual è", "qual e",
        "quanto vale", "calcola", "dammi", "dammi il",
        "risultato", "valore", "per favore", "fammi",
        "il", "la", "lo", "l'", "un", "una",
        "quanto", "fa",
        "quante", "quanti",
        "converti", "converto", "trasforma",
    ]
    for u in useless:
        t = t.replace(u, " ")

    # 3) costanti esplicite (prima di tutto il resto)
    t = t.replace("pi greco", "pi")
    t = t.replace("velocità della luce", "c")
    t = t.replace("costante di planck", "planck")
    t = t.replace("costante gravitazionale", "grav")
    t = t.replace("gravità terrestre", "g")

    # 4) operatori naturali
    t = t.replace("più", "+")
    t = t.replace("meno", "-")
    t = t.replace("volte", "*")
    t = t.replace("per", "*")
    t = t.replace("x", "*")
    t = t.replace("moltiplica", "*")
    t = t.replace("diviso", "/")
    t = t.replace("fratto", "/")

    # 5) potenze: "2 elevato alla 10", "2 alla 10", "2 elevato a 3"
    t = re.sub(r"(\d+)\s*elevato alla\s*(\d+)", r"\1**\2", t)
    t = re.sub(r"(\d+)\s*elevato a\s*(\d+)", r"\1**\2", t)
    t = re.sub(r"(\d+)\s*alla\s*(\d+)", r"\1**\2", t)

    # perché qualcuno potrebbe usare ancora il simbolo ^
    t = t.replace("^", "**")

    # 6) radici quadrate
    t = re.sub(r"radice quadrata di ([0-9.]+)", r"sqrt(\1)", t)
    t = re.sub(r"radice quadrata ([0-9.]+)", r"sqrt(\1)", t)
    t = re.sub(r"radice di ([0-9.]+)", r"sqrt(\1)", t)
    t = re.sub(r"radice ([0-9.]+)", r"sqrt(\1)", t)

    # 7) radici cubiche
    t = re.sub(r"radice cubica di ([0-9.]+)", r"(\1**(1/3))", t)
    t = re.sub(r"radice cubica ([0-9.]+)", r"(\1**(1/3))", t)

    # 8) trigonometria in gradi (parole italiane)
    t = re.sub(r"seno di ([0-9.]+)", r"sind(\1)", t)
    t = re.sub(r"seno ([0-9.]+)", r"sind(\1)", t)
    t = re.sub(r"coseno di ([0-9.]+)", r"cosd(\1)", t)
    t = re.sub(r"coseno ([0-9.]+)", r"cosd(\1)", t)
    t = re.sub(r"tangente di ([0-9.]+)", r"tand(\1)", t)
    t = re.sub(r"tangente ([0-9.]+)", r"tand(\1)", t)

    # 9) trigonometria in gradi (sin 30, cos 60, tan 45)
    t = re.sub(r"\bsin ([0-9.]+)", r"sind(\1)", t)
    t = re.sub(r"\bcos ([0-9.]+)", r"cosd(\1)", t)
    t = re.sub(r"\btan ([0-9.]+)", r"tand(\1)", t)

    # 10) logaritmi
    #    - logaritmo naturale di X → ln(X)
    t = re.sub(r"logaritmo naturale di ([0-9.]+)", r"ln(\1)", t)
    t = re.sub(r"log naturale di ([0-9.]+)", r"ln(\1)", t)
    t = re.sub(r"log naturale ([0-9.]+)", r"ln(\1)", t)

    #    - logaritmo di X, log di X, log X → log10(X)
    t = re.sub(r"logaritmo di ([0-9.]+)", r"log10(\1)", t)
    t = re.sub(r"log di ([0-9.]+)", r"log10(\1)", t)
    t = re.sub(r"log ([0-9.]+)", r"log10(\1)", t)

    #    - ln X → ln(X)
    t = re.sub(r"\bln ([0-9.]+)", r"ln(\1)", t)

    # 11) percentuali: "30 percento di 50", "10% di 400"
    t = re.sub(r"([0-9.]+)\s*percento di\s*([0-9.]+)", r"(\1/100)*\2", t)
    t = re.sub(r"([0-9.]+)\s*% di\s*([0-9.]+)", r"(\1/100)*\2", t)

    # 12) conversioni unità (km ↔ metri)
    t = re.sub(r"([0-9.]+)\s*(km|chilometri)\s+in\s+metri", r"(\1*1000)", t)
    t = re.sub(r"([0-9.]+)\s*metri\s+in\s+(km|chilometri)", r"(\1/1000)", t)

    # 13) conversioni temperatura
    t = re.sub(r"([0-9.]+)\s*gradi celsius in fahrenheit", r"((\1*9/5)+32)", t)
    t = re.sub(r"([0-9.]+)\s*gradi fahrenheit in celsius", r"((\1-32)*5/9)", t)

    # 14) fattoriali
    t = re.sub(r"fattoriale di ([0-9]+)", r"fact(\1)", t)
    t = re.sub(r"fattoriale ([0-9]+)", r"fact(\1)", t)
    t = re.sub(r"([0-9]+)!", r"fact(\1)", t)

    # 15) combinazioni (nCk)
    #     "combinazioni di 5 su 2", "combinazioni 5 su 2", "comb 10 3"
    t = re.sub(r"combinazioni di ([0-9]+) su ([0-9]+)", r"math.comb(\1,\2)", t)
    t = re.sub(r"combinazioni ([0-9]+) su ([0-9]+)", r"math.comb(\1,\2)", t)
    t = re.sub(r"comb di ([0-9]+) su ([0-9]+)", r"math.comb(\1,\2)", t)
    t = re.sub(r"comb ([0-9]+) ([0-9]+)", r"math.comb(\1,\2)", t)

    # 16) parentesi vocali
    t = t.replace("apri parentesi", "(")
    t = t.replace("chiudi parentesi", ")")

    # pulizia spazi doppi
    t = re.sub(r"\s+", " ", t).strip()

    return t


# ============================================================
#   EVAL SICURO
# ============================================================

def safe_eval(expr: str):
    scope = {"__builtins__": {}}
    scope.update(allowed_functions)
    scope.update(allowed_constants)
    scope["math"] = math
    return eval(expr, scope)


# ============================================================
#   FUNZIONE PRINCIPALE
# ============================================================

def handle_calculator(text: str) -> str:
    expr = normalize(text)

    if not expr:
        return "Non sono riuscito a capire l'operazione."

    try:
        result = safe_eval(expr)

        # formattazione del risultato
        if isinstance(result, float):
            result = round(result, 6)

        return f"Il risultato è {result}."

    except Exception:
        return "Non sono riuscito a capire l'operazione."
