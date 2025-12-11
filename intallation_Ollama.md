# 🧠 Installazione e utilizzo di Ollama (Mac M1)

Questo documento spiega come installare **Ollama** su macOS (M1/M2/M3) e come scaricare i modelli AI da usare localmente — **gratis e senza cloud**.

---

## 1️⃣ Installare Ollama su Mac (Apple Silicon)

1. Cerca su Google: **“Ollama download”**
2. Scarica il file `.dmg` per macOS
3. Apri il `.dmg` e trascina **Ollama** nella cartella `Applicazioni`
4. Avvia Ollama (per attivare il servizio in background)

Verifica l’installazione aprendo il Terminale:

```bash
ollama --version
```

Se non dà errori, tutto è configurato correttamente.

---

# 2️⃣ Installare DeepSeek R1

Dal Terminale:

```bash
ollama pull deepseek-r1
```

Questo comando:

* scarica il modello,
* lo ottimizza per l’esecuzione locale.

### 📌 Varianti disponibili

#### ✔ Versione consigliata (7B)

```bash
ollama pull deepseek-r1:7b
```

#### ✔ Versione super veloce (1.5B)

```bash
ollama pull deepseek-r1:1.5b
```

#### ✔ Versione completa (circa 5.2 GB)

```bash
ollama pull deepseek-r1
```

---

## 3️⃣ Testare DeepSeek R1 da terminale

Prova interattiva:

```bash
ollama run deepseek-r1
```

Esempio di prompt:

> Spiegami in modo semplice cosa significa overfitting

Per uscire:

```
CTRL + C
```

Se funziona → il modello è installato correttamente.

---

# 4️⃣ Installare Mistral 7B Instruct (per il tuo assistente)

Nel terminale:

```bash
ollama pull mistral:7b-instruct
```

(Sono circa 3–4 GB.)

Poi aggiorna il tuo file Python `core/llm.py`:

```python
MODEL = "mistral:7b-instruct"
```

Il tuo assistente userà automaticamente il modello locale tramite Ollama.

---

# 5️⃣ Usare Ollama da Python

Per comunicare con l’API locale di Ollama (`http://localhost:11434`) installa il client ufficiale:

```bash
pip install ollama
```

Esempio minimale:

```python
import ollama

response = ollama.chat(
    model="mistral:7b-instruct",
    messages=[
        {"role": "user", "content": "Ciao! Spiegami cos’è un LLM."}
    ],
)

print(response["message"]["content"])
```

---

## ✔ Ora sei pronto

Con Ollama installato e i modelli DeepSeek / Mistral configurati, il tuo assistente AI può:

* generare risposte vocali,
* processare immagini,
* usare modelli LLM completamente **offline**.

---
