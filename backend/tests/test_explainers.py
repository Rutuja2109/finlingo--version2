"""Daily explainer tests. Needs the local server on :8001 and the local DB (demo account, plus a temporary admin check)."""
import os
import sys
from datetime import date, datetime, timedelta, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import explainers as E  # noqa: E402

fails = []


def ok(name, cond):
    print(("OK  " if cond else "BAD ") + name)
    if not cond:
        fails.append(name)


# ---- library
ok("14 evergreen explainers with unique ids", len(E.EVERGREEN) == 14 and len({e["id"] for e in E.EVERGREEN}) == 14)
for e in E.EVERGREEN:
    q = e["quiz"]
    ok(f"{e['id']}: complete and quiz index valid", all(e.get(k) for k in ("headline", "summary", "why", "term")) and 3 <= len(q[1]) <= 4 and 0 <= q[2] < len(q[1]) and len(set(q[1])) == len(q[1]) and q[3])
ok("no evergreen links to a source or claims today's news", all("source_url" not in e for e in E.EVERGREEN))
ok("every evergreen is short enough for 60 seconds (under 160 words)", all(len((e["summary"] + " " + " ".join(e["points"]) + " " + e["why"]).split()) < 160 for e in E.EVERGREEN))
days = [E.evergreen_for(date(2026, 11, 1) + timedelta(days=i)) ["id"] for i in range(14)]
ok("14 consecutive days show 14 different explainers", len(set(days)) == 14)
ok("public view hides the correct answer", "correct" not in str(E.public_view(E.EVERGREEN[0], "2026-11-06")["quiz"]).lower())

# the numbers quoted in the library
emi = lambda p, r, n: p * (r / 1200) * (1 + r / 1200) ** n / ((1 + r / 1200) ** n - 1)
ok("repo example: EMI 26,992 at 9% and 26,511 at 8.75% (about 480 less)", round(emi(3e6, 9, 240)) == 26992 and round(emi(3e6, 8.75, 240)) == 26511)
ok("inflation example: 1,00,000 at 6% for 10 years is about 55,800", round(1e5 / 1.06 ** 10, -2) == 55800)
ok("FD example: real return about 1.9%", round((1.07 / 1.05 - 1) * 100, 1) == 1.9)
ok("rupee example: 80 to 90 is 12.5% costlier", (9000 - 8000) / 8000 * 100 == 12.5)

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
today = (datetime.now(timezone.utc) + timedelta(minutes=330)).date()
db.explainer_reads.delete_many({"user_id": uid})
db.explainers.delete_many({"date": today.isoformat()})


def stats():
    return c.get(f"{U}/stats/me", headers=H).json()


t = c.get(f"{U}/explainer/today", headers=H).json()
exp = E.evergreen_for(today)
ok("today is the evergreen of the day", t["id"] == exp["id"] and t["kind"] == "evergreen" and not t["done"])
ok("answer is not leaked before reading", "correct" not in str(t["quiz"]).lower() and "result" not in t)
ok("bad answer index -> 400", c.post(f"{U}/explainer/read", headers=H, json={"answer": 9}).status_code == 400)
s0 = stats()
right = exp["quiz"][2]
res = c.post(f"{U}/explainer/read", headers=H, json={"answer": right}).json()
ok("right answer pays 10 XP and 2 coins", res["correct"] is True and res["xp"] == 10 and res["coins"] == 2)
s1 = stats()
ok("stats went up by exactly that", s1["total_xp"] - s0["total_xp"] == 10 and s1["coins"] - s0["coins"] == 2 and s1["xp_today"] - s0["xp_today"] == 10)
ok("second read pays nothing -> 400", c.post(f"{U}/explainer/read", headers=H, json={"answer": right}).status_code == 400 and stats()["total_xp"] == s1["total_xp"])
t = c.get(f"{U}/explainer/today", headers=H).json()
ok("done state shows the result and explanation", t["done"] and t["result"]["correct"] and t["result"]["explanation"] and t["result"]["correct_index"] == right)

# wrong answer pays less
db.explainer_reads.delete_many({"user_id": uid})
wrong = (right + 1) % len(exp["quiz"][1])
res = c.post(f"{U}/explainer/read", headers=H, json={"answer": wrong}).json()
ok("wrong answer pays 5 XP and shows the right one", res["correct"] is False and res["xp"] == 5 and res["correct_index"] == right)
db.explainer_reads.delete_many({"user_id": uid})

# admin
ok("non-admin cannot list", c.get(f"{U}/explainer/admin", headers=H).status_code == 403)
news = {"date": today.isoformat(), "headline": "TEST: RBI keeps the repo rate unchanged", "summary": "The RBI left its main lending rate unchanged at this meeting, so loan rates are unlikely to move soon.",
        "points": ["Point one", "Point two"], "why": "It means floating-rate EMIs stay about where they are for now.", "term_word": "Monetary policy", "term_meaning": "How the central bank uses interest rates to manage prices and growth.",
        "quiz_question": "What does an unchanged repo rate mean for floating EMIs?", "quiz_options": ["They stay about the same", "They double", "They vanish"], "quiz_correct": 0,
        "quiz_explanation": "No change in the policy rate means no push on loan rates.", "source_name": "RBI", "source_url": "https://www.rbi.org.in/"}
db.users.update_one({"id": uid}, {"$set": {"role": "admin"}})
try:
    ok("bad link -> 400", c.post(f"{U}/explainer/admin", headers=H, json={**news, "source_url": "javascript:alert(1)"}).status_code == 400)
    ok("http link -> 400", c.post(f"{U}/explainer/admin", headers=H, json={**news, "source_url": "http://example.com"}).status_code == 400)
    ok("correct index out of range -> 400", c.post(f"{U}/explainer/admin", headers=H, json={**news, "quiz_correct": 5}).status_code == 400)
    ok("too few options -> 400", c.post(f"{U}/explainer/admin", headers=H, json={**news, "quiz_options": ["a", "b"]}).status_code == 400)
    ok("impossible date -> 400", c.post(f"{U}/explainer/admin", headers=H, json={**news, "date": "2026-13-45"}).status_code == 400)
    ok("short summary -> 400", c.post(f"{U}/explainer/admin", headers=H, json={**news, "summary": "too short"}).status_code == 400)
    ok("admin publishes a news explainer", c.post(f"{U}/explainer/admin", headers=H, json=news).status_code == 200)
    t = c.get(f"{U}/explainer/today", headers=H).json()
    ok("news explainer replaces the evergreen for that day, with its source", t["kind"] == "news" and t["source_url"] == "https://www.rbi.org.in/" and t["headline"].startswith("TEST"))
    ok("publishing again for the same date replaces it", c.post(f"{U}/explainer/admin", headers=H, json={**news, "headline": "TEST: second version of the headline"}).status_code == 200
       and len([x for x in c.get(f"{U}/explainer/admin", headers=H).json() if x["date"] == today.isoformat()]) == 1)
    ok("read the news explainer", c.post(f"{U}/explainer/read", headers=H, json={"answer": 0}).json()["correct"] is True)
    ok("delete it", c.delete(f"{U}/explainer/admin/{today.isoformat()}", headers=H).status_code == 200)
    ok("evergreen is back after delete", c.get(f"{U}/explainer/today", headers=H).json()["kind"] == "evergreen")
finally:
    db.users.update_one({"id": uid}, {"$set": {"role": "user"}})
    db.explainer_reads.delete_many({"user_id": uid})
    db.explainers.delete_many({"date": today.isoformat()})

print("\nFAILED: %s" % fails if fails else "\nALL PASSED")
sys.exit(1 if fails else 0)
