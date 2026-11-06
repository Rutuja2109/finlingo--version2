"""Mission tests. Needs the local server on :8001 and the local DB (demo account)."""
import os
import sys
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import missions as M  # noqa: E402

fails = []


def ok(name, cond):
    print(("OK  " if cond else "BAD ") + name)
    if not cond:
        fails.append(name)


# ---- catalog
ids = [m["id"] for m in M.MISSIONS]
ok("mission ids are unique", len(ids) == len(set(ids)))
ok("every mission has what the app needs", all(m["title"] and m["why"] and len(m["steps"]) >= 2 and m["theme"] in M.THEMES and m["xp"] > 0 and m["kind"] in ("self", "auto") for m in M.MISSIONS))
ok("auto missions name a known check", all(m.get("check") in ("log5", "goal", "trade", "spread", "crash") for m in M.MISSIONS if m["kind"] == "auto"))
ok("self missions have a note prompt or a link", all(m.get("note_prompt") or m.get("link") for m in M.MISSIONS if m["kind"] == "self"))
ok("no mission asks the learner to buy a product", not any(w in (m["title"] + " ".join(m["steps"])).lower() for m in M.MISSIONS for w in ("buy a ", "purchase a policy", "invest ₹")))
f1 = M.featured_mission(set(), "2026-W45")
ok("featured mission is stable within a week", f1 == M.featured_mission(set(), "2026-W45"))
ok("featured mission skips done ones", M.featured_mission({f1}, "2026-W45") != f1)
other = next(i for i in ids if i != f1)
ok("finishing a different mission does not change the pick", M.featured_mission({other}, "2026-W45") == f1)
ok("featured is None when everything is done", M.featured_mission(set(ids), "2026-W45") is None)
ok("week_key looks like 2026-W45", M.week_key(date(2026, 11, 6)) == "2026-W45")

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
db.mission_progress.delete_many({"user_id": uid})


def stats():
    return c.get(f"{U}/stats/me", headers=H).json()


j = c.get(f"{U}/missions", headers=H).json()
ok("lists every mission, none done", j["total"] == len(ids) and j["done_count"] == 0 and len(j["missions"]) == len(ids))
ok("exactly one mission is featured", sum(m["featured"] for m in j["missions"]) == 1)
ok("unknown mission -> 404", c.post(f"{U}/missions/nope/complete", headers=H, json={}).status_code == 404)

s0 = stats()
long_note = "x" * 400
res = c.post(f"{U}/missions/upi-history/complete", headers=H, json={"note": long_note})
ok("self mission completes", res.status_code == 200 and res.json() == {"xp": 20, "coins": 10})
s1 = stats()
ok("xp +20, coins +10, xp_today +20", s1["total_xp"] - s0["total_xp"] == 20 and s1["coins"] - s0["coins"] == 10 and s1["xp_today"] - s0["xp_today"] == 20)
ok("second tap pays nothing", c.post(f"{U}/missions/upi-history/complete", headers=H, json={}).status_code == 400 and stats()["total_xp"] == s1["total_xp"])
j = c.get(f"{U}/missions", headers=H).json()
m = next(x for x in j["missions"] if x["id"] == "upi-history")
ok("done, note trimmed to 140", m["done"] and len(m["note"]) == 140 and j["done_count"] == 1)

# auto missions: refused first, then pass once the data exists
db.money_entries.delete_many({"user_id": uid, "note": "mission-test"})
db.money_goals.delete_many({"user_id": uid, "name": "MISSION TEST"})
for mid in ("log-week", "goal-set"):
    ok(f"{mid} refused before the work is done", c.post(f"{U}/missions/{mid}/complete", headers=H, json={}).status_code == 400)
made = []
for _ in range(5):
    made.append(c.post(f"{U}/money/entries", headers=H, json={"kind": "expense", "amount": 50, "category": "food", "note": "mission-test"}).json()["id"])
ok("log-week passes after 5 expenses", c.post(f"{U}/missions/log-week/complete", headers=H, json={}).status_code == 200)
g = c.post(f"{U}/money/goals", headers=H, json={"name": "MISSION TEST", "target": 1000, "months": 2}).json()
ok("goal-set passes after creating a goal", c.post(f"{U}/missions/goal-set/complete", headers=H, json={}).status_code == 200)
for i in made:
    c.delete(f"{U}/money/entries/{i}", headers=H)
c.delete(f"{U}/money/goals/{g['id']}", headers=H)

c.post(f"{U}/practice/reset", headers=H)
ok("first-trade refused with no trades", c.post(f"{U}/missions/first-trade/complete", headers=H, json={}).status_code == 400)
ok("spread refused with no positions", c.post(f"{U}/missions/spread/complete", headers=H, json={}).status_code == 400)
ok("crash refused before a replay", c.post(f"{U}/missions/crash-hold/complete", headers=H, json={}).status_code == 400)
for a in ("nifty", "gold"):
    c.post(f"{U}/practice/trade", headers=H, json={"asset": a, "side": "buy", "amount": 1000})
ok("first-trade passes", c.post(f"{U}/missions/first-trade/complete", headers=H, json={}).status_code == 200)
ok("spread refused with only 2 assets", c.post(f"{U}/missions/spread/complete", headers=H, json={}).status_code == 400)
c.post(f"{U}/practice/trade", headers=H, json={"asset": "btc", "side": "buy", "amount": 1000})
ok("spread passes with 3 assets", c.post(f"{U}/missions/spread/complete", headers=H, json={}).status_code == 200)
db.practice_accounts.update_one({"user_id": uid}, {"$set": {"last_result": {"before": 1, "after": 1, "at": "x"}}})
ok("crash-hold passes once a replay has finished", c.post(f"{U}/missions/crash-hold/complete", headers=H, json={}).status_code == 200)
c.post(f"{U}/practice/reset", headers=H)

j = c.get(f"{U}/missions", headers=H).json()
ok("progress counts 6 done", j["done_count"] == 6)
# an auto mission ignores any note sent with it
ok("auto mission stores no note", next(x for x in j["missions"] if x["id"] == "goal-set")["note"] == "")

db.mission_progress.delete_many({"user_id": uid})
print("\nFAILED: %s" % fails if fails else "\nALL PASSED")
sys.exit(1 if fails else 0)
