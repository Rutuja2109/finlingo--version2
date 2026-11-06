"""Daily quests: three small goals per day, picked from a pool, with coin rewards and a chest.
Counters live in `daily_quests` (one document per user per learner-day). XP progress comes from user_stats.xp_today."""
import hashlib
from datetime import date, datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

QUEST_COINS = 5
CHEST_COINS = 15

QUESTS = {
    "xp": {"title": "Earn 30 XP", "goal": 30, "metric": "xp"},
    "lesson": {"title": "Finish 1 lesson", "goal": 1, "metric": "lessons"},
    "perfect": {"title": "Score 100% on a lesson", "goal": 1, "metric": "perfect"},
    "revise": {"title": "Revise 3 concepts", "goal": 3, "metric": "revisions"},
    "explainer": {"title": "Read today's 60-second explainer", "goal": 1, "metric": "explainers"},
    "trade": {"title": "Make a practice trade", "goal": 1, "metric": "trades"},
    "log": {"title": "Log a spend or income in My money", "goal": 1, "metric": "entries"},
}
SLOTS = [["xp", "lesson"], ["perfect", "revise", "explainer"], ["trade", "log"]]


def pick_quests(user_id: str, day: str, can_revise: bool) -> list:
    """Three quest ids for this user and day: one from each slot, stable for the whole day."""
    h = hashlib.sha256(f"{user_id}:{day}".encode()).digest()
    out = []
    for i, options in enumerate(SLOTS):
        opts = [o for o in options if not (o == "revise" and not can_revise)]
        out.append(opts[h[i] % len(opts)])
    return out


async def bump(db, user_id: str, day: str, metric: str, n: int = 1):
    """Count one thing done today (lessons, perfect, revisions, trades, entries)."""
    await db.daily_quests.update_one(
        {"user_id": user_id, "date": day},
        {"$inc": {f"counts.{metric}": n}, "$setOnInsert": {"claimed": [], "chest": False}},
        upsert=True,
    )


class ClaimIn(BaseModel):
    id: str


def make_router(db, get_current_user, learner_today):
    r = APIRouter(prefix="/quests")

    def local_now(request: Request) -> datetime:
        try:
            off = max(-840, min(840, int(request.headers.get("X-TZ-Offset", "0"))))
        except ValueError:
            off = 0
        return datetime.now(timezone.utc) - timedelta(minutes=off)

    async def todays(user: dict, day: str):
        stats = await db.user_stats.find_one({"user_id": user["id"]}, {"_id": 0}) or {}
        doc = await db.daily_quests.find_one({"user_id": user["id"], "date": day}, {"_id": 0}) or {"counts": {}, "claimed": [], "chest": False}
        xp = stats.get("xp_today", 0) if stats.get("xp_today_date") == day else 0
        counts = {**doc.get("counts", {}), "xp": xp}
        can_revise = stats.get("lessons_completed", 0) >= 3
        ids = doc.get("quest_ids") or pick_quests(user["id"], day, can_revise)
        if not doc.get("quest_ids"):  # freeze the choice for the day so it cannot change mid-day
            await db.daily_quests.update_one({"user_id": user["id"], "date": day}, {"$set": {"quest_ids": ids}, "$setOnInsert": {"claimed": [], "chest": False}}, upsert=True)
        quests = []
        for qid in ids:
            q = QUESTS[qid]
            prog = int(counts.get(q["metric"], 0))
            quests.append({"id": qid, "title": q["title"], "goal": q["goal"], "progress": min(prog, q["goal"]),
                           "done": prog >= q["goal"], "claimed": qid in doc.get("claimed", []), "reward": QUEST_COINS})
        return quests, doc

    @r.get("/today")
    async def today(request: Request, user: dict = Depends(get_current_user)):
        d = learner_today(request)
        day = d.isoformat()
        quests, doc = await todays(user, day)
        monday = d - timedelta(days=d.weekday())
        days = [(monday + timedelta(days=i)).isoformat() for i in range(7)]
        rows = await db.daily_quests.find({"user_id": user["id"], "date": {"$in": days}}, {"_id": 0, "date": 1, "claimed": 1}).to_list(7)
        active = {x["date"] for x in rows if x.get("claimed")}
        now = local_now(request)
        midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        all_claimed = all(q["claimed"] for q in quests)
        return {
            "date": day, "quests": quests,
            "done_count": sum(q["done"] for q in quests), "claimed_count": sum(q["claimed"] for q in quests),
            "chest": {"reward": CHEST_COINS, "ready": all_claimed and not doc.get("chest"), "opened": bool(doc.get("chest"))},
            "week": [{"date": x, "label": "MTWTFSS"[i], "on": x in active, "today": x == day} for i, x in enumerate(days)],
            "resets_in_seconds": int((midnight - now).total_seconds()),
        }

    async def pay(user_id: str, coins: int):
        await db.user_stats.update_one({"user_id": user_id}, {"$inc": {"coins": coins}}, upsert=True)

    @r.post("/claim")
    async def claim(body: ClaimIn, request: Request, user: dict = Depends(get_current_user)):
        day = learner_today(request).isoformat()
        quests, _ = await todays(user, day)
        q = next((x for x in quests if x["id"] == body.id), None)
        if not q:
            raise HTTPException(status_code=404, detail="That is not one of today's quests")
        if not q["done"]:
            raise HTTPException(status_code=400, detail="Finish the quest first")
        res = await db.daily_quests.update_one({"user_id": user["id"], "date": day, "claimed": {"$ne": q["id"]}}, {"$push": {"claimed": q["id"]}})
        if res.matched_count == 0:
            raise HTTPException(status_code=400, detail="Already claimed")
        await pay(user["id"], QUEST_COINS)
        return {"coins": QUEST_COINS}

    @r.post("/chest")
    async def chest(request: Request, user: dict = Depends(get_current_user)):
        day = learner_today(request).isoformat()
        quests, doc = await todays(user, day)
        if not all(q["claimed"] for q in quests):
            raise HTTPException(status_code=400, detail="Claim all three quests first")
        res = await db.daily_quests.update_one({"user_id": user["id"], "date": day, "chest": {"$ne": True}}, {"$set": {"chest": True}})
        if res.matched_count == 0:
            raise HTTPException(status_code=400, detail="Chest already opened")
        await pay(user["id"], CHEST_COINS)
        return {"coins": CHEST_COINS}

    return r
