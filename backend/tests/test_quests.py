"""Daily quest tests. Needs the local server on :8001 and the local DB (demo account)."""
import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import quests as Q  # noqa: E402

fails = []


def ok(name, cond):
    print(("OK  " if cond else "BAD ") + name)
    if not cond:
        fails.append(name)


# ---- pure logic
a = Q.pick_quests("user-1", "2026-11-06", True)
ok("three quests, one per slot", len(a) == 3 and all(a[i] in Q.SLOTS[i] for i in range(3)))
ok("same user and day gives the same quests", a == Q.pick_quests("user-1", "2026-11-06", True))
days = {tuple(Q.pick_quests("user-1", f"2026-11-{d:02d}", True)) for d in range(1, 29)}
ok("quests vary from day to day", len(days) >= 4)
ok("no revise quest until 3 lessons are done", all("revise" not in Q.pick_quests("u", f"2026-12-{d:02d}", False) for d in range(1, 29)))

# ---- API
import httpx  # noqa: E402
from dotenv import load_dotenv  # noqa: E402
from pymongo import MongoClient  # noqa: E402

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
db = MongoClient(os.environ["MONGO_URL"])[os.environ["DB_NAME"]]
U = "http://localhost:8001/api"
c = httpx.Client(timeout=30)
r = c.post(f"{U}/auth/login", json={"email": "demo@finlingo.com", "password": "Demo@123"}).json()
uid = r["id"]
H = {"Authorization": f"Bearer {r['access_token']}", "X-TZ-Offset": "-330"}
today = (datetime.now(timezone.utc) + timedelta(minutes=330)).date().isoformat()

db.daily_quests.delete_many({"user_id": uid, "date": {"$gte": today[:8] + "01"}})
db.user_stats.update_one({"user_id": uid}, {"$set": {"xp_today": 0, "xp_today_date": today}})

t = c.get(f"{U}/quests/today", headers=H).json()
ids = [q["id"] for q in t["quests"]]
ok("today has 3 quests, none done or claimed", len(ids) == 3 and not any(q["done"] or q["claimed"] for q in t["quests"]))
ok("chest is locked", t["chest"]["ready"] is False and t["chest"]["opened"] is False)
ok("week has 7 days with today marked", len(t["week"]) == 7 and sum(w["today"] for w in t["week"]) == 1)
ok("resets_in is within a day", 0 < t["resets_in_seconds"] <= 86400)
ok("quests stay the same on a second call", [q["id"] for q in c.get(f"{U}/quests/today", headers=H).json()["quests"]] == ids)
ok("claiming an unfinished quest -> 400", c.post(f"{U}/quests/claim", headers=H, json={"id": ids[0]}).status_code == 400)
ok("claiming a quest that is not today's -> 404", c.post(f"{U}/quests/claim", headers=H, json={"id": "nope"}).status_code == 404)
ok("opening the chest early -> 400", c.post(f"{U}/quests/chest", headers=H).status_code == 400)

# Do everything a quest could ask for
if not db.user_progress.find_one({"user_id": uid, "status": {"$in": ["completed", "mastered"]}}):  # fresh test database: finish one lesson first
    first = db.concepts.find_one({}, {"_id": 0, "id": 1}, sort=[("order", 1)])
    c.post(f"{U}/progress/complete-concept", headers=H, json={"concept_id": first["id"], "score": 100})
concept = next(p["concept_id"] for p in db.user_progress.find({"user_id": uid, "status": {"$in": ["completed", "mastered"]}}) if db.concepts.find_one({"id": p["concept_id"]}))
res = c.post(f"{U}/progress/complete-concept", headers=H, json={"concept_id": concept, "score": 100})
ok("complete lesson with 100%", res.status_code == 200)
for _ in range(3):
    c.post(f"{U}/revisions/grade", headers=H, json={"concept_id": concept, "quality": 2})
db.explainer_reads.delete_many({"user_id": uid, "date": today})
c.post(f"{U}/explainer/read", headers=H, json={"answer": 0})
c.post(f"{U}/practice/reset", headers=H)
c.post(f"{U}/practice/trade", headers=H, json={"asset": "nifty", "side": "buy", "amount": 500})
c.post(f"{U}/practice/reset", headers=H)
e = c.post(f"{U}/money/entries", headers=H, json={"kind": "expense", "amount": 10, "category": "food"}).json()
old = c.post(f"{U}/money/entries", headers=H, json={"kind": "expense", "amount": 10, "category": "food", "date": "2020-01-01"}).json()
doc = db.daily_quests.find_one({"user_id": uid, "date": today})
ok("counters recorded (lesson, perfect, 3 revisions, trade, 1 entry; backdated entry ignored)",
   doc["counts"].get("lessons", 0) >= 1 and doc["counts"].get("perfect", 0) >= 1 and doc["counts"].get("revisions", 0) >= 3
   and doc["counts"].get("trades", 0) >= 1 and doc["counts"].get("entries", 0) == 1)
db.user_stats.update_one({"user_id": uid}, {"$set": {"xp_today": 45, "xp_today_date": today}})
for i in (e["id"], old["id"]):
    c.delete(f"{U}/money/entries/{i}", headers=H)

t = c.get(f"{U}/quests/today", headers=H).json()
ok("all three quests are done", all(q["done"] and q["progress"] == q["goal"] for q in t["quests"]))
coins0 = c.get(f"{U}/stats/me", headers=H).json()["coins"]
ok("chest still locked until claimed", c.post(f"{U}/quests/chest", headers=H).status_code == 400)
for q in t["quests"]:
    ok(f"claim {q['id']}", c.post(f"{U}/quests/claim", headers=H, json={"id": q["id"]}).status_code == 200)
    ok(f"claim {q['id']} again -> 400", c.post(f"{U}/quests/claim", headers=H, json={"id": q["id"]}).status_code == 400)
t = c.get(f"{U}/quests/today", headers=H).json()
ok("chest is ready after all claimed", t["chest"]["ready"] is True and t["claimed_count"] == 3)
ok("open chest", c.post(f"{U}/quests/chest", headers=H).status_code == 200)
ok("open chest again -> 400", c.post(f"{U}/quests/chest", headers=H).status_code == 400)
coins1 = c.get(f"{U}/stats/me", headers=H).json()["coins"]
ok("coins went up by exactly 3 x 5 + 15 = 30", coins1 - coins0 == 30)
t = c.get(f"{U}/quests/today", headers=H).json()
ok("today shows as an active day this week", any(w["today"] and w["on"] for w in t["week"]) and t["chest"]["opened"])

print("\nFAILED: %s" % fails if fails else "\nALL PASSED")
sys.exit(1 if fails else 0)
