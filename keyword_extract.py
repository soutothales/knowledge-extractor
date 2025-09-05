import re
from collections import Counter
from spacy_pipeline import nlp

def extract_keywords(text, top_k=3):
    if nlp:
        doc = nlp(text)
        nouns = [token.text.lower() for token in doc if token.pos_ == "NOUN"]
    else:
        nouns = re.findall(r"\b\w+\b", text.lower())

    counter = Counter(nouns)
    return [word for word, _ in counter.most_common(top_k)]
