"""Repair mojibake (UTF-8 text that was decoded as cp1252/latin-1 and saved again), e.g. 'â‰¤' -> '≤'."""
import re

import ftfy

_MARKERS = re.compile("[ÂÃâ][\u0080-¿€‚-™ŒœŠ-Ÿ]")


def has_mojibake(text: str) -> bool:
    return bool(_MARKERS.search(text))


def repair_text(text: str) -> str:
    return ftfy.fix_encoding(text) if has_mojibake(text) else text


def repair(obj):
    """Recursively repair every string inside dicts/lists. Returns (new_obj, changed)."""
    if isinstance(obj, str):
        new = repair_text(obj)
        return new, new != obj
    if isinstance(obj, list):
        changed = False
        out = []
        for item in obj:
            new, ch = repair(item)
            out.append(new)
            changed = changed or ch
        return out, changed
    if isinstance(obj, dict):
        changed = False
        out = {}
        for k, v in obj.items():
            if k == "_id":
                out[k] = v
                continue
            new, ch = repair(v)
            out[k] = new
            changed = changed or ch
        return out, changed
    return obj, False


async def repair_collection(db, name, keys=None):
    """Fix garbled text in place for one collection. Ids are never touched. Returns number of docs fixed."""
    fixed = 0
    async for doc in db[name].find({}):
        new, changed = repair({k: v for k, v in doc.items() if k != "_id"} if keys is None else {k: doc[k] for k in keys if k in doc})
        if changed:
            await db[name].update_one({"_id": doc["_id"]}, {"$set": new})
            fixed += 1
    return fixed
