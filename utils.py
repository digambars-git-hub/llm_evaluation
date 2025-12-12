# utils.py
# small helper functions (embeddings, similarity, entity extraction)
# kept simple on purpose

import numpy as np
from sentence_transformers import SentenceTransformer
import re

_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed(text):
    t = text.strip()
    return np.array(_model.encode(t))


def cosine_sim(a, b):
    # normal cosine similarity
    if a.size == 0 or b.size == 0:
        return 0.0
    a = a / (np.linalg.norm(a) + 1e-9)
    b = b / (np.linalg.norm(b) + 1e-9)
    return float(np.dot(a, b))


def get_entities(text):
    # not using spacy here to keep it lightweight
    # just pick out words > 3 chars (simple heuristic)
    words = re.findall(r"[A-Za-z]{4,}", text)
    uniq = []
    for w in words:
        wl = w.lower()
        if wl not in uniq:
            uniq.append(wl)
    return uniq[:8]
