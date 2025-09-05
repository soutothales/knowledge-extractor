from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock").lower()

_JSON_KEYS_DESC = (
    "Return ONLY a strict JSON object with keys: "
    "title (string or null), topics (array of exactly 3 short nouns), "
    "sentiment (one of: positive, neutral, negative), summary (1-2 sentences)."
)


def _coerce_json(s):
    """Try to parse JSON. If it fails, extract the first {...} block and parse."""
    try:
        return json.loads(s)
    except Exception:
        m = re.search(r"\{[\s\S]*\}", s)
        if m:
            return json.loads(m.group(0))
        raise

def call_llm(text):
    meta = {"provider": LLM_PROVIDER, "fallback_used": False, "error": None}

    if LLM_PROVIDER == "ollama":
        import ollama # type: ignore
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
        client = ollama.Client(host=base_url)

        system = (
            "You are a precise analyst. "
            + _JSON_KEYS_DESC
            + " Output only the JSON with no extra text."
        )
        user = f"TEXT:\n{text}"


        # Chat call for better instruction‑following
        resp = client.chat(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            options={"temperature": 0.2},
        )
        content = resp["message"]["content"]
        data = _coerce_json(content)
        return data, meta

    data = {
        "title": None,
        "topics": ["text", "analysis", "summary"],
        "sentiment": "neutral",
        "summary": (text.strip().split(". ")[0] + ".")[:200] if text else "",
    }
    return data, meta
