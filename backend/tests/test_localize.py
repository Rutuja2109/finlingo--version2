"""Lesson translation layer. Pure logic, no server or database needed."""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import localize as L  # noqa: E402

fails = []


def ok(name, cond):
    print(("OK   " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)


doc = {
    "id": "a1b2c3d4-0000-1111-2222-333344445555", "type": "mcq", "order": 2, "slug": "money-basics", "xp_reward": 25,
    "title": "Your first salary",
    "content": {
        "question": "What should you do first?", "options": ["Save 20%", "Spend it all"], "correct": 0,
        "explanation": "Pay yourself first.", "choices": [{"text": "Pay half (₹20,000)", "correct": True, "verdict": "good"}],
    },
    "key_takeaways": ["Save before you spend"], "hindi": "पैसे की बात",
}
orig = json.dumps(doc, sort_keys=True)

with tempfile.TemporaryDirectory() as d:
    L.DIR = d
    L.load.cache_clear()
    es = {
        L.text_key("Your first salary"): "Tu primer sueldo",
        L.text_key("What should you do first?"): "¿Qué deberías hacer primero?",
        L.text_key("Save 20%"): "Ahorra el 20 %",
        L.text_key("Pay yourself first."): "Págate primero a ti.",
        L.text_key("Pay half (₹20,000)"): "Paga la mitad (₹20,000)",
        L.text_key("Save before you spend"): "Ahorra antes de gastar",
        L.text_key("good"): "bueno",
        L.text_key("mcq"): "pregunta",
    }
    json.dump(es, open(os.path.join(d, "es.json"), "w", encoding="utf-8"), ensure_ascii=False)

    out = L.localize(doc, "es")
    ok("title is translated", out["title"] == "Tu primer sueldo")
    ok("question, options, explanation, takeaways are translated",
       out["content"]["question"].startswith("¿Qué") and out["content"]["options"][0] == "Ahorra el 20 %"
       and out["content"]["explanation"].startswith("Págate") and out["key_takeaways"][0].startswith("Ahorra antes"))
    ok("a nested choice is translated and its flag is kept", out["content"]["choices"][0]["text"].startswith("Paga la mitad") and out["content"]["choices"][0]["correct"] is True)
    ok("ids, types, slugs, orders, numbers and the answer index never change",
       out["id"] == doc["id"] and out["type"] == "mcq" and out["slug"] == "money-basics" and out["order"] == 2 and out["xp_reward"] == 25 and out["content"]["correct"] == 0)
    ok("the verdict code is not translated", out["content"]["choices"][0]["verdict"] == "good")
    ok("the original is not changed", json.dumps(doc, sort_keys=True) == orig)
    ok("a text with no translation stays English", L.localize({"title": "Something new"}, "es")["title"] == "Something new")
    ok("no language, an unknown language or a missing file give English back",
       L.localize(doc, "") is doc and L.localize(doc, "xx") is doc and L.localize(doc, "fr") is doc)
    ok("Hindi source text is left out of translation", not L.is_translatable("title", "पैसे की बात"))
    ok("codes and ids are not collected for translation",
       not L.is_translatable("title", "money-basics") and not L.is_translatable("title", "12,000") and not L.is_translatable("id", "Some Name")
       and not L.is_translatable("title", "0258eefe-da0b-4761-a4e5-4f36e31aacae"))
    ok("real text is collected", [s for _, s in L.walk_strings(doc)].count("Save 20%") == 1 and len(list(L.walk_strings(doc))) >= 6)

    class R:
        def __init__(self, h): self.headers = h
    ok("the X-Lang header picks a supported language only", L.pick_lang(R({"X-Lang": "es"})) == "es" and L.pick_lang(R({"X-Lang": "ES-mx"})) == "es"
       and L.pick_lang(R({"X-Lang": "tr"})) == "" and L.pick_lang(R({})) == "")

print("ALL OK" if not fails else f"FAILED: {fails}")
sys.exit(1 if fails else 0)
