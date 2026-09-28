"""A deterministic, offline stand-in for an LLM provider."""


def ask_llm(question: str, history: list[dict]) -> dict:
    tokens_in = max(1, len(question.split())) + sum(len(turn["content"].split()) for turn in history)
    tokens_out = max(1, min(60, len(question.split()) + 4))
    return {
        "answer": f"Mock response: {question.strip()}",
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "cost_usd": round((tokens_in + tokens_out) * 0.000001, 8),
    }
