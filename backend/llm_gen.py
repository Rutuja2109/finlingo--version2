"""LLM-powered lesson generation for FinLingo.

Calls Claude Sonnet 4.5 (primary) via the Emergent Universal Key.
Returns strict JSON in our internal lesson schema.

Note: send_message() is used (not stream_message) because this is a
backend ingestion job, not a user-facing chat. Streaming makes no sense
here — we need the full JSON before saving.
"""
from __future__ import annotations
import os
import json
import re
import uuid
import logging
from typing import List, Dict, Any

from emergentintegrations.llm.chat import LlmChat, UserMessage

logger = logging.getLogger(__name__)

PRIMARY_MODEL = ("anthropic", "claude-sonnet-4-5-20250929")
FALLBACK_MODEL = ("openai", "gpt-5.2")

SYSTEM_PROMPT = """You are an expert curriculum designer for professional certifications.
You convert dense textbook chapter content into engaging, mastery-oriented interactive lessons.

Rules:
- NEVER hallucinate facts. Stay strictly faithful to the source text provided.
- Simplify language but never change the meaning.
- Each concept gets a clear learning objective, plain-English explanation, 3-5 key takeaways, and 2-3 common mistakes.
- Each concept has 4-5 lessons mixing types: one "intro", two-to-three "mcq", and one "scenario" OR "flashcard".
- MCQ options must be plausible. Exactly one correct answer (0-indexed) per MCQ.
- Output STRICT JSON only. No markdown fences, no prose outside the JSON.
"""

USER_TEMPLATE = """Source: a chapter from the {certification} certification curriculum.

CHAPTER TITLE: {chapter_title}

EXTRACTED CHAPTER TEXT (may be partial due to PDF quality):
\"\"\"
{chapter_text}
\"\"\"

Use the chapter TITLE as your primary guide. If the extracted text is sparse, draw on
your knowledge of the {certification} curriculum to teach the topics this chapter title
implies. Stay faithful to standard {certification} curriculum content. Be concrete and accurate.

Produce JSON with this exact schema (no comments, no trailing commas):

{{
  "modules": [
    {{
      "title": "<short module title>",
      "concepts": [
        {{
          "title": "<concept title>",
          "learning_objective": "<one sentence>",
          "simple_explanation": "<2-4 sentences, plain English>",
          "key_takeaways": ["<takeaway 1>", "<takeaway 2>", "..."],
          "common_mistakes": ["<mistake 1>", "..."],
          "xp_reward": 15,
          "lessons": [
            {{ "type": "intro", "content": {{ "heading": "...", "body": "..." }} }},
            {{ "type": "mcq", "content": {{ "question": "...", "options": ["a","b","c","d"], "correct": 0, "explanation": "..." }} }},
            {{ "type": "mcq", "content": {{ "question": "...", "options": ["a","b","c","d"], "correct": 2, "explanation": "..." }} }},
            {{ "type": "flashcard", "content": {{ "front": "...", "back": "..." }} }}
          ]
        }}
      ]
    }}
  ]
}}

Generate 2-3 modules for this chapter, with 2-3 concepts per module.
Keep total under 10 concepts.
Return ONLY the JSON object, no other text."""


def _strip_json(text: str) -> str:
    """Pull a JSON object out of a possibly-fenced response."""
    text = text.strip()
    # remove ```json ... ``` fences if present
    m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, flags=re.DOTALL)
    if m:
        return m.group(1)
    # Otherwise find first { ... last }
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start:end + 1]
    return text


async def _call_model(provider: str, model: str, system_msg: str, user_msg: str) -> str:
    api_key = os.environ["EMERGENT_LLM_KEY"]
    chat = LlmChat(
        api_key=api_key,
        session_id=f"finlingo-gen-{uuid.uuid4()}",
        system_message=system_msg,
    ).with_model(provider, model)
    reply = await chat.send_message(UserMessage(text=user_msg))
    # send_message may return a string or an object — normalize
    if hasattr(reply, "content"):
        return str(reply.content)
    return str(reply)


async def generate_chapter_lessons(certification: str, chapter_title: str,
                                   chapter_text: str) -> Dict[str, Any]:
    """Return the parsed JSON dict {modules: [...]} for one chapter.

    Tries Claude Sonnet 4.5 first, falls back to GPT-5.2 on parse failure.
    """
    prompt = USER_TEMPLATE.format(
        certification=certification,
        chapter_title=chapter_title,
        chapter_text=chapter_text[:24000],  # safety cap
    )

    last_err: Exception | None = None
    for provider, model in (PRIMARY_MODEL, FALLBACK_MODEL):
        try:
            raw = await _call_model(provider, model, SYSTEM_PROMPT, prompt)
            data = json.loads(_strip_json(raw))
            if isinstance(data, dict) and isinstance(data.get("modules"), list) and data["modules"]:
                return data
            last_err = ValueError("LLM returned no modules")
        except Exception as e:
            last_err = e
            logger.warning("LLM %s/%s failed: %s", provider, model, e)
            continue

    raise RuntimeError(f"All LLM providers failed: {last_err}")
