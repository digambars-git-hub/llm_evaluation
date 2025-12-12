# evaluator.py
# I wrote the logic here for relevance, completeness, hallucination etc.
# These are simple heuristics only.

import numpy as np
from utils import embed, cosine_sim, get_entities
from datetime import datetime


class Evaluator:
    def __init__(self):
        # all embeddings will use same helper function
        pass

    # main evaluation function
    def evaluate_chat(self, chat, ctx):
        msgs = chat.get("messages", [])
        if len(msgs) < 2:
            return {"error": "not enough messages"}

        # using last user + assistant messages
        user_msg = msgs[-2]
        bot_msg = msgs[-1]

        user_text = user_msg.get("text", "")
        bot_text = bot_msg.get("text", "")

        relevance = self.compute_relevance(bot_text, ctx)
        comp, missing = self.compute_completeness(user_text, bot_text)
        hallu = self.compute_hallucination(bot_text, ctx)

        # latency calculation (simple)
        t1 = user_msg.get("ts")
        t2 = bot_msg.get("ts")
        latency_ms = None
        if t1 and t2:
            try:
                dt1 = datetime.fromisoformat(t1.replace("Z", "+00:00"))
                dt2 = datetime.fromisoformat(t2.replace("Z", "+00:00"))
                latency_ms = int((dt2 - dt1).total_seconds() * 1000)
            except:
                latency_ms = None

        return {
            "relevance_score": relevance,
            "completeness_score": comp,
            "missing_parts": missing,
            "hallucination_score": hallu,
            "latency_ms": latency_ms
        }

    # --- individual metric functions ---

    def compute_relevance(self, bot_text, ctx_json):
        bot_emb = embed(bot_text)
        sims = []

        for c in ctx_json.get("contexts", []):
            txt = c.get("text", "")
            ce = embed(txt)
            sims.append(cosine_sim(bot_emb, ce))

        if not sims:
            return 0.0

        # avg of all sims
        return float(np.mean(sims))

    def compute_completeness(self, user_text, bot_text):
        # entities from user msg
        ents = get_entities(user_text)
        missing = []

        for e in ents:
            if e.lower() not in bot_text.lower():
                missing.append(e)

        if len(ents) == 0:
            return (1.0, [])
        else:
            score = (len(ents) - len(missing)) / len(ents)
            return (round(score, 2), missing)

    def compute_hallucination(self, bot_text, ctx_json):
        # splitting into simple sentences
        parts = [p.strip() for p in bot_text.split(".") if p.strip()]
        if not parts:
            return 1.0

        ctx_embs = [embed(c.get("text", "")) for c in ctx_json.get("contexts", [])]
        hallu_count = 0

        for s in parts:
            emb = embed(s)
            sims = [cosine_sim(emb, ce) for ce in ctx_embs]
            if sims:
                best = max(sims)
                if best < 0.45:  # threshold chosen after trying
                    hallu_count += 1

        score = 1 - (hallu_count / len(parts))
        return round(score, 2)
