"""Translate lesson text into another language with the Claude API.

  python tools/translate_content.py --lang es --dry-run          # count and estimate cost, no API calls
  python tools/translate_content.py --lang es --limit 40         # try 40 strings first and read the result
  python tools/translate_content.py --lang es                    # everything not translated yet (safe to stop and re-run)

Needs:  pip install anthropic   and   ANTHROPIC_API_KEY set in your own terminal (never commit it).
Reads English text from the local database (MONGO_URL / DB_NAME from backend/.env) and writes backend/translations/<lang>.json.
Every result is checked: same numbers, same {placeholders}, sane length. Anything that fails is skipped and listed, not saved.
A native speaker must still read the result before it ships.
"""
import argparse
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dotenv import load_dotenv  # noqa: E402
from pymongo import MongoClient  # noqa: E402

import localize  # noqa: E402

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

NAMES = {
    "hi": "Hindi", "es": "Spanish (neutral Latin American)", "fr": "French", "ar": "Arabic (Modern Standard)", "bn": "Bengali",
    "pt": "Portuguese (Brazil)", "ru": "Russian", "ur": "Urdu", "id": "Indonesian", "de": "German", "ja": "Japanese", "zh": "Simplified Chinese",
}
SYSTEM = """You translate lessons for FinLearn, an educational app that teaches personal finance, investing, tax, insurance and crypto to learners aged 18 and over.
Translate from English into {lang}. Rules:
- Natural, clear, friendly and accurate. Short sentences. Explain, do not lecture. Keep the meaning exactly; never add advice, claims or guarantees.
- Keep every number, percentage, currency amount and symbol (for example ₹, %, +) exactly as written. Do not convert currencies or units.
- Keep placeholders like {{answer}} or {{price}} and any HTML tags exactly as written.
- Keep names of people, companies, products and tickers (FinLearn, Lumi, UPI, SIP, Nifty, Bitcoin) unless a widely used local form exists.
- Use the standard local words for finance terms. Use informal 'you' where the language has it.
Input is a JSON list of {{"k": id, "t": English text}}. Reply with ONLY a JSON list of {{"k": same id, "t": translation}}, same order, nothing else."""

NUM = re.compile(r"\d(?:[\d,\.]*\d)?")  # a number never ends in the comma or full stop that follows it
PH = re.compile(r"\{[^{}]+\}|</?\w+[^>]*>")


def collect(db):
    seen = {}
    for coll in ("courses", "chapters", "modules", "concepts", "lessons"):
        for doc in db[coll].find({}, {"_id": 0}):
            for key, s in localize.walk_strings(doc):
                seen.setdefault(localize.text_key(s), s.strip())
    return seen


def check(src: str, out: str):
    if sorted(NUM.findall(src)) != sorted(NUM.findall(out)):
        return "numbers changed"
    if sorted(PH.findall(src)) != sorted(PH.findall(out)):
        return "placeholders or tags changed"
    if len(out) > max(40, len(src) * 4) or not out.strip():
        return "odd length"
    return None


def ask(client, model, lang, batch):
    msg = client.messages.create(
        model=model, max_tokens=16000, system=SYSTEM.format(lang=NAMES[lang]),
        messages=[{"role": "user", "content": json.dumps([{"k": k, "t": t} for k, t in batch], ensure_ascii=False)}],
    )
    text = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text").strip()
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
    return {r["k"]: r["t"] for r in json.loads(text)}, msg.usage


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", required=True, choices=sorted(NAMES))
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--batch-chars", type=int, default=9000)
    ap.add_argument("--model", default=os.environ.get("TRANSLATE_MODEL", "claude-sonnet-5-5"))
    ap.add_argument("--price-in", type=float, default=3.0, help="USD per million input tokens (check current pricing)")
    ap.add_argument("--price-out", type=float, default=15.0, help="USD per million output tokens (check current pricing)")
    a = ap.parse_args()

    strings = collect(MongoClient(os.environ["MONGO_URL"])[os.environ["DB_NAME"]])
    path = os.path.join(localize.DIR, f"{a.lang}.json")
    done = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
    todo = [(k, t) for k, t in strings.items() if k not in done]
    if a.limit:
        todo = todo[: a.limit]
    chars = sum(len(t) for _, t in todo)
    tin, tout = chars / 3.5 + len(todo) * 12, chars / 3.0 * (1.6 if a.lang in {"ar", "ur", "hi", "bn", "ru", "ja", "zh"} else 1.2)
    print(f"{a.lang}: {len(strings)} distinct texts, {len(done)} already translated, {len(todo)} to do ({chars:,} characters)")
    print(f"estimate: about {tin/1e6:.2f}M input and {tout/1e6:.2f}M output tokens, roughly ${tin/1e6*a.price_in + tout/1e6*a.price_out:.0f} at ${a.price_in}/${a.price_out} per million (rough)")
    if a.dry_run or not todo:
        return

    import anthropic

    client = anthropic.Anthropic()
    os.makedirs(localize.DIR, exist_ok=True)
    failed, i = [], 0
    while i < len(todo):
        batch, size = [], 0
        while i < len(todo) and (not batch or size + len(todo[i][1]) <= a.batch_chars):
            batch.append(todo[i]); size += len(todo[i][1]); i += 1
        for attempt in (1, 2):
            try:
                got, usage = ask(client, a.model, a.lang, batch)
                break
            except Exception as e:  # network, rate limit, bad JSON: wait and try once more
                print("  retry after:", str(e)[:120]); time.sleep(8); got = None
        if got is None:
            failed += [k for k, _ in batch]; continue
        ok = 0
        for k, src in batch:
            out = got.get(k)
            why = check(src, out) if isinstance(out, str) else "missing"
            if why:
                failed.append((k, why, src[:60]))
            else:
                done[k] = out.strip(); ok += 1
        tmp = path + ".tmp"
        json.dump(done, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        os.replace(tmp, path)
        print(f"  {len(done)} saved (+{ok}, skipped {len(batch) - ok}) in/out tokens {usage.input_tokens}/{usage.output_tokens}")
    print(f"done: {len(done)} translated, {len(failed)} skipped")
    for f in failed[:20]:
        print("  skipped", f)


if __name__ == "__main__":
    main()
