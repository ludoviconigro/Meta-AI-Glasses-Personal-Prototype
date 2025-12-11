from ollama import Client

client = Client(host="http://localhost:11434")

MODEL = "mistral:7b-instruct"
#MODEL = "deepseek-r1:1.5b"   # puoi cambiarlo quando vuoi (7b, ecc.)

SYSTEM_PROMPT = (
    "Sei un assistente italiano chiaro, utile e preciso. "
    "Rispondi in modo naturale, conciso e corretto. "
    "Non inventare dati non necessari."
)

def ask_llm(prompt: str) -> str:
    try:
        response = client.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
        )
        return response["message"]["content"]
    except Exception as e:
        return f"Errore LLM: {e}"
