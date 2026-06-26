"""One-off: fill missing chapters of LOMA 357 from the uploaded PDF.

Uses a slimmer prompt for faster, more reliable LLM calls.
"""
import asyncio, sys, os, uuid, json, re
from datetime import datetime, timezone
sys.path.insert(0, "/app/backend")
from dotenv import load_dotenv
load_dotenv("/app/backend/.env")

from motor.motor_asyncio import AsyncIOMotorClient
from pdf_ingest import extract_chapters
from emergentintegrations.llm.chat import LlmChat, UserMessage


COURSE_ID = "e3368e1d-ac43-4847-ab15-feaec2aefb45"
PDF_PATH = "/app/data/loma.pdf"  # also at /app/data/uploads/<pdf-id>.pdf

# Slimmer, faster prompt — still comprehensive
SLIM_SYSTEM = """You are an expert curriculum designer for the LOMA certification.
Convert chapter content into engaging interactive lessons.
Output strict JSON only. No markdown fences. No prose outside JSON.
Stay faithful to standard LOMA curriculum. Include real-life examples."""

SLIM_USER = """Chapter from LOMA curriculum: "{chapter_title}"

Source text (may be partial — use your LOMA knowledge to fill gaps):
{chapter_text}

Produce JSON:
{{
  "modules": [
    {{
      "title": "<module title>",
      "concepts": [
        {{
          "title": "<concept title>",
          "learning_objective": "<one sentence>",
          "simple_explanation": "<3-4 sentences with a real-world example>",
          "key_takeaways": ["<3-4 bullets>"],
          "common_mistakes": ["<2-3 traps>"],
          "real_world_example": "<2-sentence scenario with names/dollars>",
          "visual_hint": "<chart|scale|flowchart|comparison|timeline|building|shield|briefcase|gauge>",
          "xp_reward": 20,
          "lessons": [
            {{"type":"intro","content":{{"heading":"...","body":"..."}}}},
            {{"type":"mcq","content":{{"question":"...","options":["a","b","c","d"],"correct":0,"explanation":"..."}}}},
            {{"type":"mcq","content":{{"question":"...","options":["a","b","c","d"],"correct":2,"explanation":"..."}}}},
            {{"type":"flashcard","content":{{"front":"...","back":"..."}}}}
          ]
        }}
      ]
    }}
  ]
}}

3 modules, 2-3 concepts each, total 6-8 concepts.
Vary correct index. Return ONLY the JSON object."""


def strip_json(text):
    text = text.strip()
    m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, flags=re.DOTALL)
    if m: return m.group(1)
    a, b = text.find("{"), text.rfind("}")
    return text[a:b+1] if a != -1 and b > a else text


async def call_llm(chapter_title, chapter_text):
    api_key = os.environ["EMERGENT_LLM_KEY"]
    prompt = SLIM_USER.format(chapter_title=chapter_title, chapter_text=chapter_text[:14000])
    for provider, model in [("openai", "gpt-5.2"), ("anthropic", "claude-sonnet-4-5-20250929")]:
        try:
            chat = LlmChat(api_key=api_key, session_id=f"fill-{uuid.uuid4()}",
                          system_message=SLIM_SYSTEM).with_model(provider, model)
            reply = await asyncio.wait_for(
                chat.send_message(UserMessage(text=prompt)), timeout=120
            )
            text = str(reply.content if hasattr(reply, "content") else reply)
            data = json.loads(strip_json(text))
            if isinstance(data, dict) and isinstance(data.get("modules"), list) and data["modules"]:
                return data
        except Exception as e:
            print(f"  {provider}/{model} failed: {str(e)[:80]}", flush=True)
            continue
    return None


async def main():
    client = AsyncIOMotorClient(os.environ["MONGO_URL"])
    db = client[os.environ["DB_NAME"]]

    course = await db.courses.find_one({"id": COURSE_ID})
    if not course:
        print("Course not found"); return

    # Existing chapters by order
    existing = await db.chapters.find({"course_id": COURSE_ID}, {"_id": 0}).to_list(50)
    existing_orders = {c["order"] for c in existing}
    print(f"Existing chapter orders: {sorted(existing_orders)}")

    # Extract all chapters from PDF
    print("Extracting all PDF chapters...", flush=True)
    pdf_chapters = extract_chapters(PDF_PATH, max_chapters=0)  # all
    print(f"Detected {len(pdf_chapters)} chapters in PDF")

    # Fill in missing ones
    for ch in pdf_chapters:
        if ch.chapter_no in existing_orders:
            print(f"  Ch {ch.chapter_no}: SKIP (already exists)", flush=True)
            continue
        print(f"  Ch {ch.chapter_no}: {ch.title} — generating...", flush=True)
        data = await call_llm(ch.title, ch.body_text)
        if not data:
            print(f"  Ch {ch.chapter_no}: FAILED", flush=True)
            continue
        chapter_id = str(uuid.uuid4())
        await db.chapters.insert_one({
            "id": chapter_id, "course_id": COURSE_ID,
            "order": ch.chapter_no, "title": ch.title,
            "description": f"Chapter {ch.chapter_no} of LOMA 357",
            "source_pages": [ch.start_page, ch.end_page],
        })
        for m_i, m in enumerate(data.get("modules", [])):
            module_id = str(uuid.uuid4())
            await db.modules.insert_one({
                "id": module_id, "chapter_id": chapter_id,
                "order": m_i + 1, "title": m.get("title", f"Module {m_i+1}"),
            })
            for c_i, c in enumerate(m.get("concepts", [])):
                concept_id = str(uuid.uuid4())
                await db.concepts.insert_one({
                    "id": concept_id, "module_id": module_id,
                    "order": c_i + 1,
                    "title": c.get("title", "Untitled"),
                    "learning_objective": c.get("learning_objective", ""),
                    "simple_explanation": c.get("simple_explanation", ""),
                    "key_takeaways": c.get("key_takeaways", []),
                    "common_mistakes": c.get("common_mistakes", []),
                    "real_world_example": c.get("real_world_example", ""),
                    "visual_hint": c.get("visual_hint", "chart"),
                    "xp_reward": int(c.get("xp_reward", 20)),
                })
                for l_i, lesson in enumerate(c.get("lessons", [])):
                    await db.lessons.insert_one({
                        "id": str(uuid.uuid4()), "concept_id": concept_id,
                        "order": l_i + 1, "type": lesson.get("type", "intro"),
                        "content": lesson.get("content", {}),
                    })
        print(f"  Ch {ch.chapter_no}: OK ({len(data.get('modules', []))} modules)", flush=True)

    # Final tally
    chs = await db.chapters.find({"course_id": COURSE_ID}, {"_id": 0}).to_list(50)
    print(f"\nFinal: {len(chs)} chapters in course.")
    client.close()


if __name__ == "__main__":
    asyncio.run(main())
