# Statupbox AI-Powered Sports Quiz Generation Agent

A RAG-based Streamlit app that generates grounded, factually-checked
multiple-choice sports quizzes by combining a local ChromaDB "textbook"
of verified facts with live DuckDuckGo web search, then asking an LLM
(OpenAI by default) to write questions using *only* that retrieved context.

## Project Structure

```
sports-quiz-agent/
├── app.py                 # Streamlit dashboard (entry point)
├── requirements.txt
├── .env.example            # Copy to .env and add your API key
├── .gitignore
└── src/
    ├── __init__.py
    ├── database.py         # ChromaDB setup + local fact search
    ├── web_search.py       # DuckDuckGo live news search
    └── generator.py        # RAG orchestration + LLM call
```

## Setup

1. **Python version**: use 3.9, 3.10, or 3.11 (avoid 3.12+ — some
   ChromaDB dependencies aren't fully compatible yet).

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your API key**
   ```bash
   cp .env.example .env
   # then edit .env and paste your OpenAI key
   ```

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

## How it works

1. On startup, `setup_and_populate_db()` creates a persistent ChromaDB
   collection and loads it with a small hand-curated set of verified
   facts about Cricket, Football, and Badminton (only runs once thanks
   to `@st.cache_resource` + an emptiness check).
2. When you click **Generate Fresh Quiz**, `compile_quiz_data()`:
   - Queries ChromaDB for the most relevant local facts about the
     chosen sport.
   - Queries DuckDuckGo for live/recent news snippets about the sport.
   - Combines both into one context block.
   - Sends that context to the LLM with a strict JSON schema
     (`response_format`), so the output is always parseable and never
     hallucinates facts outside the given context.
3. The quiz is rendered in a copyable text box, with an expander to
   inspect the exact "ground truth" context the quiz was built from.

## Troubleshooting

- **`sqlite3` version errors on Linux**: `pip install pysqlite3-binary`
  (already in `requirements.txt` for Linux). `src/database.py` swaps it
  in for the standard library's `sqlite3` before ChromaDB is imported.
- **API key errors**: make sure `.env` exists (not just `.env.example`)
  and is never committed — it's already in `.gitignore`.
- **Malformed quiz JSON**: this build uses OpenAI's `response_format`
  JSON Schema (strict mode) specifically to avoid label-drift issues
  (e.g., the model writing "AI_Option" instead of a clean option string).
