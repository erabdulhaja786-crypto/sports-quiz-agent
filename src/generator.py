import os
import json
from openai import OpenAI
from dotenv import load_dotenv

from src.database import search_local_facts
from src.web_search import search_live_news

load_dotenv()

_client = None


def get_client() -> OpenAI:
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Copy .env.example to .env and add your key."
            )
        _client = OpenAI(api_key=api_key)
    return _client


# A strict JSON Schema forces the model to always return well-formed,
# parseable quiz data. This is the fix for the "A) Option vs AI_Option"
# label-drift issue called out in the assignment's troubleshooting section.
QUIZ_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "quiz_response",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "questions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                            "options": {
                                "type": "array",
                                "items": {"type": "string"},
                                "minItems": 4,
                                "maxItems": 4,
                            },
                            "correct_option_index": {"type": "integer"},
                            "explanation": {"type": "string"},
                        },
                        "required": [
                            "question",
                            "options",
                            "correct_option_index",
                            "explanation",
                        ],
                        "additionalProperties": False,
                    },
                }
            },
            "required": ["questions"],
            "additionalProperties": False,
        },
    },
}


def build_context(sport: str) -> str:
    """Combine local 'textbook' facts and live web snippets into one block."""
    local_facts = search_local_facts(sport)
    web_snippets = search_live_news(sport)

    context_lines = ["## Local Verified Facts (ChromaDB)"]
    context_lines += [f"- {fact}" for fact in local_facts] or ["- (none found)"]

    context_lines.append("\n## Live Web Search Snippets (DuckDuckGo)")
    context_lines += [f"- {s}" for s in web_snippets] or ["- (none found)"]

    return "\n".join(context_lines)


def generate_quiz(sport: str, difficulty: str, context: str) -> dict:
    """Call the LLM, grounded strictly in `context`, and return parsed JSON."""
    client = get_client()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    system_prompt = (
        "You are a rigorous sports quiz-writer. Generate quiz questions "
        "using ONLY the facts provided in the context. Do not use outside "
        "knowledge, and do not invent statistics, dates, or names that are "
        "not present in the context. If the context is insufficient for a "
        "fact, write a question about a fact that IS present instead."
    )

    user_prompt = (
        f"Sport: {sport}\n"
        f"Difficulty: {difficulty}\n\n"
        f"Context:\n{context}\n\n"
        "Generate exactly 5 multiple-choice questions (4 options each) at "
        "the requested difficulty. Return only the structured JSON."
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format=QUIZ_SCHEMA,
        temperature=0.7 if difficulty == "Hard" else 0.4,
    )

    return json.loads(response.choices[0].message.content)


def format_quiz_text(quiz_data: dict) -> str:
    """Turn the structured quiz JSON into the readable text shown in the UI."""
    lines = []
    letters = ["A", "B", "C", "D"]

    for i, q in enumerate(quiz_data.get("questions", []), start=1):
        lines.append(f"Q{i}. {q['question']}")
        for letter, option in zip(letters, q["options"]):
            lines.append(f"   {letter}) {option}")
        correct_letter = letters[q["correct_option_index"]]
        lines.append(f"   Answer: {correct_letter}")
        lines.append(f"   Explanation: {q['explanation']}")
        lines.append("")

    return "\n".join(lines).strip()


def compile_quiz_data(sport: str, difficulty: str):
    """
    Full pipeline used by app.py:
    1. Gather context (local facts + live web search).
    2. Ask the LLM to generate a grounded quiz.
    3. Format the result as display-ready text.

    Returns (quiz_text, context_used) so the UI can show both the quiz
    and the "ground truth" context it was built from.
    """
    context = build_context(sport)
    quiz_data = generate_quiz(sport, difficulty, context)
    quiz_text = format_quiz_text(quiz_data)
    return quiz_text, context
