from duckduckgo_search import DDGS


def search_live_news(sport: str, max_results: int = 5) -> list:
    """
    Fetch a handful of recent headlines/snippets about a sport to ground
    the quiz in up-to-date, real-world information. This mitigates LLM
    hallucination for anything that happened after its training cutoff.
    """
    query = f"latest {sport} news results 2026"
    snippets = []

    try:
        with DDGS() as ddgs:
            for result in ddgs.text(query, max_results=max_results):
                title = result.get("title", "")
                body = result.get("body", "")
                snippet = f"{title}: {body}".strip()
                if snippet:
                    snippets.append(snippet)
    except Exception as e:
        # Web search is a "nice to have" -- if DuckDuckGo is unavailable or
        # rate-limiting us, the quiz can still be generated from local
        # facts alone, so we don't let this crash the app.
        snippets.append(f"[web search unavailable: {e}]")

    return snippets
