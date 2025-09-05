def fallback_sentiment(text):
    text_lower = text.lower()
    if any(word in text_lower for word in ["good", "great", "happy", "love"]):
        return "positive"
    elif any(word in text_lower for word in ["bad", "sad", "angry", "hate"]):
        return "negative"
    return "neutral"

def fallback_topics(text, top_k=3):
    words = list({w.lower() for w in text.split() if len(w) > 4})
    return words[:top_k]

def fallback_summary(text, max_len=100):
    return text[:max_len] + ("..." if len(text) > max_len else "")
