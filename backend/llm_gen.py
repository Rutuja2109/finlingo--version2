"""LLM-powered lesson generation for FinLingo — Comprehensive edition.

Generates EXAM-READY, real-life-grounded interactive lessons.
Calls Claude Sonnet 4.5 (primary) via Emergent Universal Key, falls back to GPT-5.2.
"""
from __future__ import annotations
import os
import json
import re
import uuid
import logging
from typing import Dict, Any

from emergentintegrations.llm.chat import LlmChat, UserMessage

logger = logging.getLogger(__name__)

PRIMARY_MODEL = ("openai", "gpt-5.2")
FALLBACK_MODEL = ("anthropic", "claude-sonnet-4-5-20250929")

SYSTEM_PROMPT = """You are a world-class curriculum designer for professional certification exams.
You convert dense textbook chapter content into engaging, mastery-oriented interactive learning experiences
that prepare learners for the actual exam.

Rules:
- Be COMPREHENSIVE — cover every important sub-topic the chapter title implies. Aim for breadth and depth.
- Stay faithful to the standard certification curriculum. Never fabricate facts.
- Use plain English. Define every jargon term inline the first time it appears.
- EVERY concept must include a real-life example or scenario (named characters, dollar amounts, realistic context).
- Generate exam-style MCQs that mirror the actual certification exam style (one best answer, plausible distractors).
- Include "common_mistakes" that learners typically make — these are gold for exam prep.
- Output STRICT JSON only. No markdown fences. No prose outside JSON.
"""

USER_TEMPLATE = """Source: Chapter from the {certification} certification curriculum.

CHAPTER TITLE: "{chapter_title}"

EXTRACTED CHAPTER TEXT (may be partial — supplement with curriculum knowledge):
\"\"\"
{chapter_text}
\"\"\"

Produce JSON. Lessons must appear in THIS EXACT ORDER per concept:
  (1) intro     — hook & framing
  (2) teach     — clear explanation of the core idea
  (3) teach     — deeper detail / formula / mechanics with a worked example
  (4) example   — vivid real-world scenario (not a quiz, just a story to anchor memory)
  (5) flashcard — recall prompt
  (6) mcq       — easy understanding check
  (7) mcq       — application question
  (8) mcq       — exam-style question with subtle distractors
  (9) mcq       — calculation or scenario question
  (10) mcq      — common-mistake trap question
  (11) scenario — apply the concept in a real situation

Schema (strict, no comments, no trailing commas):

{{
  "modules": [
    {{
      "title": "<short module title>",
      "concepts": [
        {{
          "title": "<specific concept title>",
          "learning_objective": "<one sentence>",
          "simple_explanation": "<3-5 sentences with a real-life example using named characters + dollar amounts>",
          "key_takeaways": ["<takeaway 1>", "<takeaway 2>", "<takeaway 3>", "<takeaway 4>"],
          "common_mistakes": ["<exam trap 1>", "<trap 2>", "<trap 3>"],
          "real_world_example": "<2-3 sentence concrete scenario>",
          "visual_hint": "<chart|scale|flowchart|comparison|timeline|building|shield|briefcase|gauge>",
          "xp_reward": 25,
          "lessons": [
            {{ "type": "intro", "content": {{ "heading": "<hook>", "body": "<2-3 sentences making learner curious>" }} }},
            {{ "type": "teach", "content": {{ "heading": "<plain-English headline>", "body": "<4-6 sentences explaining the concept clearly>", "bullets": ["<key point 1>", "<key point 2>", "<key point 3>"] }} }},
            {{ "type": "teach", "content": {{ "heading": "<mechanics or formula>", "body": "<4-6 sentences explaining HOW it works, with a worked example>", "bullets": ["<sub-step 1>", "<sub-step 2>"] }} }},
            {{ "type": "example", "content": {{ "heading": "<real-world story>", "scenario": "<5-7 sentence vivid scenario with names, dollar amounts, decisions>", "lesson": "<one-sentence moral / what the example demonstrates>" }} }},
            {{ "type": "flashcard", "content": {{ "front": "<prompt>", "back": "<concise answer>" }} }},
            {{ "type": "mcq", "content": {{ "question": "<easy question>", "options": ["a","b","c","d"], "correct": 0, "explanation": "<why>" }} }},
            {{ "type": "mcq", "content": {{ "question": "<application>", "options": ["a","b","c","d"], "correct": 1, "explanation": "<why>" }} }},
            {{ "type": "mcq", "content": {{ "question": "<exam-style>", "options": ["a","b","c","d"], "correct": 2, "explanation": "<full reasoning>" }} }},
            {{ "type": "mcq", "content": {{ "question": "<calculation or scenario>", "options": ["a","b","c","d"], "correct": 3, "explanation": "<step-by-step>" }} }},
            {{ "type": "mcq", "content": {{ "question": "<common-mistake trap>", "options": ["a","b","c","d"], "correct": 0, "explanation": "<the trap & truth>" }} }},
            {{ "type": "scenario", "content": {{ "scene": "<realistic scenario with names + dollar amounts>", "question": "<what should X do?>", "choices": [
              {{ "text": "<option 1>", "correct": false, "feedback": "<why wrong>" }},
              {{ "text": "<option 2>", "correct": true, "feedback": "<why right + the lesson>" }},
              {{ "text": "<option 3>", "correct": false, "feedback": "<why wrong>" }}
            ] }} }}
          ]
        }}
      ]
    }}
  ]
}}

REQUIREMENTS:
- 3 modules with 2-3 concepts each (total 6-8 concepts per chapter).
- Each concept MUST have ALL 11 lessons in the exact order above.
- Each MCQ has exactly 4 options; vary the correct index.
- Keep teaching screens substantive — at least 4 sentences each.

Return ONLY the JSON object."""


def _strip_json(text: str) -> str:
    text = text.strip()
    m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, flags=re.DOTALL)
    if m:
        return m.group(1)
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start:end + 1]
    return text


async def _call_model(provider: str, model: str, system_msg: str, user_msg: str) -> str:
    import asyncio as _aio
    api_key = os.environ["EMERGENT_LLM_KEY"]
    chat = LlmChat(
        api_key=api_key,
        session_id=f"finlingo-gen-{uuid.uuid4()}",
        system_message=system_msg,
    ).with_model(provider, model)
    # Hard cap per call so a stuck provider doesn't block the whole job
    reply = await _aio.wait_for(
        chat.send_message(UserMessage(text=user_msg)),
        timeout=180.0,
    )
    if hasattr(reply, "content"):
        return str(reply.content)
    return str(reply)


async def generate_chapter_lessons(certification: str, chapter_title: str,
                                   chapter_text: str) -> Dict[str, Any]:
    """Return parsed JSON dict {modules: [...]} for one chapter.

    Tries Claude Sonnet 4.5 first, falls back to GPT-5.2 on parse failure.
    """
    prompt = USER_TEMPLATE.format(
        certification=certification,
        chapter_title=chapter_title,
        chapter_text=chapter_text[:20000],
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
