import sys

# --- ChromaDB / SQLite compatibility patch -------------------------------
try:
    __import__("pysqlite3")
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    # Not on Linux, or pysqlite3-binary isn't installed -> assume the
    # system sqlite3 is already new enough (normal on macOS/Windows).
    pass
# ---------------------------------------------------------------------------

import chromadb
from chromadb.utils import embedding_functions

DB_PATH = ".chroma_store"
COLLECTION_NAME = "sports_facts"

# A small, hand-verified "textbook" of facts per sport.
# Extend this list to make quizzes richer/more varied.
STATIC_FACTS = {
    "Cricket": [
        "The ICC Cricket World Cup is held every four years and is cricket's premier international 50-over tournament.",
        "A standard cricket pitch is 22 yards (20.12 metres) long between the two sets of stumps.",
        "The 'Ashes' is a Test cricket series played between England and Australia, contested since 1882.",
        "In cricket, a 'century' refers to a batter scoring 100 or more runs in a single innings.",
        "The Indian Premier League (IPL), founded in 2008, is one of the most-watched domestic T20 leagues in the world.",
        "A 'hat-trick' in cricket occurs when a bowler takes three wickets on three consecutive deliveries.",
        "Sachin Tendulkar holds the record for the most runs scored in both Test and One Day International cricket.",
        "The Duckworth-Lewis-Stern (DLS) method is used to calculate target scores in matches interrupted by weather.",
    ],
    "Football": [
        "The FIFA World Cup is held every four years and is the most-watched sporting event in the world.",
        "A standard football match consists of two 45-minute halves, for 90 minutes of regulation play.",
        "Lionel Messi and Cristiano Ronaldo are widely regarded as two of the greatest footballers of their generation.",
        "The offside rule states an attacking player cannot be nearer to the opponent's goal line than both the ball and the second-last opponent when the ball is played to them.",
        "The UEFA Champions League is Europe's top-tier club football competition, held annually since 1955.",
        "A 'hat-trick' in football means a single player scores three goals in one match.",
        "The English Premier League, founded in 1992, is one of the most-watched football leagues globally.",
        "Pele won three FIFA World Cups with Brazil, in 1958, 1962, and 1970.",
    ],
    "Badminton": [
        "Badminton is played with a shuttlecock, which can be made of feathers or synthetic materials.",
        "A standard badminton match is typically the best of three games, each played to 21 points.",
        "The Thomas Cup and Uber Cup are the premier international men's and women's team badminton championships.",
        "Badminton became an official Olympic sport at the 1992 Barcelona Olympics.",
        "P. V. Sindhu is an Indian badminton player who won a silver medal at the 2016 Rio Olympics.",
        "In badminton, a 'rally' ends when the shuttlecock touches the ground or a fault is committed.",
        "The badminton net is set at a height of 1.55 metres at the poles and 1.524 metres at the center.",
        "Lin Dan and Lee Chong Wei had one of the most celebrated rivalries in men's singles badminton.",
    ],
}


def get_chroma_client():
    """Return a persistent ChromaDB client stored on local disk."""
    return chromadb.PersistentClient(path=DB_PATH)


def get_embedding_function():
    """
    Free, local sentence-transformer embedding function. Runs entirely
    offline once the model weights are cached — no API key needed.
    """
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )


def setup_and_populate_db():
    """
    Idempotent setup: creates (or reuses) the 'sports_facts' collection and
    loads it with our static facts exactly once. Safe to call on every app
    startup (paired with @st.cache_resource in app.py).
    """
    client = get_chroma_client()
    embed_fn = get_embedding_function()

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME, embedding_function=embed_fn
    )

    if collection.count() == 0:
        documents, ids, metadatas = [], [], []
        for sport, facts in STATIC_FACTS.items():
            for i, fact in enumerate(facts):
                documents.append(fact)
                ids.append(f"{sport.lower()}_{i}")
                metadatas.append({"sport": sport})

        collection.upsert(documents=documents, ids=ids, metadatas=metadatas)

    return collection


def search_local_facts(sport: str, n_results: int = 5) -> list:
    """
    Query our local 'textbook' for the most relevant facts about a sport.
    Filters on exact sport metadata plus semantic ranking, so results stay
    on-topic even as the fact bank grows.
    """
    collection = get_chroma_client().get_or_create_collection(
        name=COLLECTION_NAME, embedding_function=get_embedding_function()
    )

    results = collection.query(
        query_texts=[f"Interesting and important facts about {sport}"],
        n_results=n_results,
        where={"sport": sport},
    )

    docs = results.get("documents", [[]])
    return docs[0] if docs else []

