Ecco un **README.md** pronto per GitHub, chiaro, professionale e adatto allo stato “primordiale” del progetto.
Puoi incollarlo direttamente nel repository.

---

# 👓 Meta AI Glasses – Personal Prototype

Un progetto personale e sperimentale per la creazione di **occhiali assistivi con intelligenza artificiale integrata**, ispirati ai Meta AI Glasses ma sviluppati *per diletto* e completamente in locale.

L’obiettivo è realizzare un sistema che combini **ascolto vocale**, **riconoscimento visivo** e **risposte dell’IA**, il tutto eseguibile su una macchina locale senza dipendere da servizi cloud.

---

## 🚧 Stato del progetto

Il progetto è attualmente **in una fase primordiale**.
Sto lavorando alla struttura di base e sperimentando le funzioni fondamentali.
Tutto ciò che è presente qui è da considerarsi *work-in-progress* e soggetto a forti miglioramenti.

---

## 💻 Ambiente di sviluppo

Sto sviluppando il progetto su un **Mac con chip Apple Silicon (M1)** utilizzando esclusivamente strumenti e risorse gratuite o open-source.

L’intelligenza artificiale è eseguita **interamente in locale** tramite **Ollama**, usando al momento il modello:

* **mistral:7b-instruct**

---

## 🎤 Modalità Vocal Assistant

La parte dedicata alle richieste vocali viene avviata con:

```bash
python main.py
```

Questa modalità permette all’assistente di ascoltare, interpretare e rispondere via voce utilizzando il modello AI locale.

---

## 👁️ Modalità Visual Assistant

La componente visiva, che utilizza la webcam per analisi o riconoscimento in tempo reale, viene avviata con:

```bash
python gui.main.py
```

Questa parte è anch’essa in sviluppo iniziale e richiede ancora molte ottimizzazioni.

---

## 🧠 Intelligenza artificiale usata

Il progetto utilizza:

* **Ollama** per gestire i modelli AI localmente
* **mistral:7b-instruct** come LLM principale

L’obiettivo è mantenere tutto in locale per privacy, velocità e sperimentazione libera.

---

## 🛣️ Roadmap (provvisoria)

* [ ] Migliorare la stabilità del sistema vocale
* [ ] Potenziare il riconoscimento visivo
* [ ] Integrare nuovi strumenti e funzioni (meteo, calcoli, RAG locale, ecc.)
* [ ] Creare un’interfaccia più fluida tra la parte vocale e quella visiva
* [ ] Testare modelli AI più performanti senza sacrificare la località
* [ ] Prototipare integrazione con veri occhiali / hardware dedicato

---

## 📌 Nota finale

Questo progetto nasce **per sperimentazione personale**, ma con il sogno di avvicinarsi un giorno a un vero paio di occhiali AI integrati.
Ogni contributo, idea o segnalazione è ben accetto.

---
