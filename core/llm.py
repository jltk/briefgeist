import requests

def ask_local_llm(letter_text: str) -> str:
    """
    Analysiert einen deutschen Brief und erstellt eine klare, formelle Antwort
    im behördlichen Stil. Gibt strukturiert zurück:
      1. Absender
      2. Zweck des Schreibens
      3. Handlungsbedarf (Ja/Nein + Details)
      4. Antwortvorschlag oder Hinweis 'Keine Antwort erforderlich.'
    """
    system_prompt = (
        "Du bist ein deutscher Verwaltungsassistent für die rechtssichere Analyse von Briefen. "
        "Antworte präzise aber detailliert auf Deutsch:\n\n"
        "1. Wer ist der Absender?\n"
        "2. Was ist der Zweck des Schreibens (z. B. Rechnung, Mahnung, Mitteilung)? Gibt es Fristen oder Forderungen?\n"
        "3. Muss der Empfänger handeln? (Ja/Nein). Wenn ja: Was genau?\n"
        "4. Wenn konrekt ein Antwortschreiben erforderlich ist, erstelle eine klare, formelle Antwort im Verwaltungston aus der Sicht des Empfängers vom Schreiben. "
        "Wenn keine Antwort nötig ist, schreibe: 'Keine Antwort erforderlich. Nur zur Kenntnisnahme.'\n\n"
        f"Briefinhalt:\n{letter_text.strip()}"
    )

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma:7b",   # alternativ: "mistral", "gemma:2b", "gemma:7b"
                "prompt": system_prompt,
                "stream": False
            },
            timeout=120
        )
        response.raise_for_status()
        data = response.json()
        result = data.get("response", "").strip()
        print("[DEBUG] LLM response received:\n", result)
        return result or "[Fehler] Keine Antwort erhalten."
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] LLM request failed: {e}")
        return "[Fehler] Sprachmodell nicht erreichbar."
