import os
from core.intents import handle_command


def load_tests(test_name):
    filename = f"tests/tests_{test_name}.txt"

    if not os.path.exists(filename):
        raise FileNotFoundError(f"❌ File {filename} non trovato.")

    tests = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                tests.append(line)
    return tests


def run_tests(test_name):
    print(f"=== AVVIO TEST: {test_name.upper()} ===\n")

    try:
        tests = load_tests(test_name)
    except FileNotFoundError as e:
        print(e)
        return

    for i, query in enumerate(tests, 1):
        print(f"Test {i}: {query}")
        try:
            response = handle_command(query)
            print(f" ➜ Risposta: {response}")
        except Exception as e:
            print(f" ❌ ERRORE: {e}")
        print("-" * 50)

    print("\n=== TEST COMPLETATI ===")
