"""Lesson translations.

Translations live in backend/translations/<lang>.json as {key: translated_text}, where key is a short hash of the English text.
Keying on the text (not on ids) means they survive a re-seed, which generates new ids. Anything without a translation stays English.
The app sends its language in the X-Lang header; `localize(doc, lang)` swaps the strings in a response.
"""
import hashlib
import json
import os
import re
from functools import lru_cache

LANGS = {"hi", "es", "fr", "ar", "bn", "pt", "ru", "ur", "id", "de", "ja", "zh"}
DIR = os.path.join(os.path.dirname(__file__), "translations")

# Fields that are ids, switches or codes, never learner-facing text.
SKIP_KEYS = {
    "id", "_id", "type", "slug", "key", "kind", "who", "color", "icon", "seed_version", "certification", "verdict",
    "answer", "status", "hidden", "order", "correct", "highlight_id", "mood", "asset", "chart", "format", "unit",
}
HAS_LETTERS = re.compile(r"[^\W\d_]{2,}", re.UNICODE)
DEVANAGARI = re.compile(r"[ऀ-ॿ]")
UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-")


def text_key(s: str) -> str:
    return hashlib.sha1(s.strip().encode("utf-8")).hexdigest()[:16]


def is_translatable(key, s) -> bool:
    """True for a string that a learner reads and that we are willing to translate."""
    if not isinstance(s, str) or key in SKIP_KEYS or (key and key.endswith("_id")):
        return False
    t = s.strip()
    if len(t) < 2 or UUID.match(t) or not HAS_LETTERS.search(t):
        return False
    if re.fullmatch(r"[a-z0-9_\-:/.#]+", t) and " " not in t and len(t) <= 24:
        return False  # looks like a code or a class name
    if DEVANAGARI.search(t):
        return False  # the Hindi course is already written in Hindi
    return True


def walk_strings(obj, key=None):
    """Yield every translatable (key, string) in a document."""
    if isinstance(obj, str):
        if is_translatable(key, obj):
            yield key, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk_strings(v, k)
    elif isinstance(obj, list):
        for x in obj:
            yield from walk_strings(x, key)


@lru_cache(maxsize=16)
def load(lang: str) -> dict:
    path = os.path.join(DIR, f"{lang}.json")
    if lang not in LANGS or not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _swap(obj, table, key=None):
    if isinstance(obj, str):
        if is_translatable(key, obj):
            return table.get(text_key(obj), obj)
        return obj
    if isinstance(obj, dict):
        return {k: _swap(v, table, k) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_swap(x, table, key) for x in obj]
    return obj


def localize(doc, lang):
    """Return a copy of doc with translated text; the original is untouched. No language or no file means English."""
    table = load(lang) if lang else {}
    return _swap(doc, table) if table else doc


def pick_lang(request) -> str:
    code = (request.headers.get("X-Lang") or "").lower()[:2]
    return code if code in LANGS else ""
