"""Regenerate LOMA 357 with the upgraded rich 11-lesson structure."""
import asyncio, sys, os, uuid
from datetime import datetime, timezone
sys.path.insert(0, "/app/backend")
from dotenv import load_dotenv
load_dotenv("/app/backend/.env")

from motor.motor_asyncio import AsyncIOMotorClient
from pdf_ingest import extract_chapters
from llm_gen import generate_chapter_lessons


COURSE_ID = "e3368e1d-ac43-4847-ab15-feaec2aefb45"
PDF_PATH = "/app/data/loma.pdf"


async def main():
    client = AsyncIOMotorClient(os.environ["MONGO_URL"])
    db = client[os.environ["DB_NAME"]]

    course = await db.courses.find_one({"id": COURSE_ID})
    if not course:
        print("Course not found"); return

    existing = await db.chapters.find({"course_id": COURSE_ID}, {"_id": 0}).to_list(50)
    existing_orders = {c["order"] for c in existing}
    print(f"Existing chapter orders: {sorted(existing_orders)}", flush=True)

    print("Extracting all PDF chapters...", flush=True)
    pdf_chapters = extract_chapters(PDF_PATH, max_chapters=0)
    print(f"Detected {len(pdf_chapters)} chapters in PDF", flush=True)

    for ch in pdf_chapters:
        if ch.chapter_no in existing_orders:
            print(f"  Ch {ch.chapter_no}: SKIP", flush=True)
            continue
        print(f"  Ch {ch.chapter_no}: {ch.title} — generating (rich)...", flush=True)
        try:
            data = await generate_chapter_lessons("LOMA", ch.title, ch.body_text)
        except Exception as e:
            print(f"  Ch {ch.chapter_no}: FAILED ({str(e)[:100]})", flush=True)
            continue
        chapter_id = str(uuid.uuid4())
        await db.chapters.insert_one({
            "id": chapter_id, "course_id": COURSE_ID,
            "order": ch.chapter_no, "title": ch.title,
            "description": f"Chapter {ch.chapter_no} of LOMA 357",
            "source_pages": [ch.start_page, ch.end_page],
        })
        n_modules = n_concepts = n_lessons = 0
        for m_i, m in enumerate(data.get("modules", [])):
            module_id = str(uuid.uuid4())
            await db.modules.insert_one({
                "id": module_id, "chapter_id": chapter_id,
                "order": m_i + 1, "title": m.get("title", f"Module {m_i+1}"),
            })
            n_modules += 1
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
                    "xp_reward": int(c.get("xp_reward", 25)),
                })
                n_concepts += 1
                for l_i, lesson in enumerate(c.get("lessons", [])):
                    await db.lessons.insert_one({
                        "id": str(uuid.uuid4()), "concept_id": concept_id,
                        "order": l_i + 1, "type": lesson.get("type", "intro"),
                        "content": lesson.get("content", {}),
                    })
                    n_lessons += 1
        print(f"  Ch {ch.chapter_no}: OK ({n_modules}m, {n_concepts}c, {n_lessons}l)", flush=True)

    chs = await db.chapters.find({"course_id": COURSE_ID}, {"_id": 0}).to_list(50)
    print(f"\nFinal: {len(chs)} chapters in course.", flush=True)
    client.close()


if __name__ == "__main__":
    asyncio.run(main())
