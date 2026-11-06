"""My money tests. Pure-logic checks run anywhere; API checks need the local server on :8001 (demo account)."""
import os
import sys
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import money as M  # noqa: E402

fails = []


def ok(name, cond):
    print(("OK  " if cond else "BAD ") + name)
    if not cond:
        fails.append(name)


# ---- logic
ok("add_months simple", M.add_months(date(2026, 11, 6), 6) == date(2027, 5, 6))
ok("add_months clamps month end", M.add_months(date(2026, 8, 31), 6) == date(2027, 2, 28))
ok("add_months leap year", M.add_months(date(2027, 8, 31), 6) == date(2028, 2, 29))
ok("months_between 6", M.months_between(date(2026, 11, 6), date(2027, 5, 6)) == 6)
ok("months_between past deadline is 0", M.months_between(date(2026, 11, 6), date(2026, 10, 1)) == 0)
ok("months_between 10 days ahead is at least 1", M.months_between(date(2026, 11, 6), date(2026, 11, 16)) == 1)

e = lambda kind, amt, cat=None: {"kind": kind, "amount": amt, "category": cat or "income", "bucket": M.CATEGORIES[cat][1] if cat else None}
s = M.split_summary([e("income", 20000), e("expense", 10000, "rent"), e("expense", 6000, "shopping"), e("expense", 4000, "sip")])
ok("split 50/30/20", s["pct"] == {"needs": 50.0, "wants": 30.0, "savings": 20.0} and s["left"] == 0)
ok("coach: on target", M.coach(s)["tone"] == "good")
s2 = M.split_summary([e("income", 20000), e("expense", 8000, "shopping")])
ok("coach: wants too high", M.coach(s2)["title"].startswith("Wants"))
s3 = M.split_summary([e("income", 20000), e("expense", 14000, "rent")])
ok("coach: needs too high", M.coach(s3)["title"].startswith("Needs"))
s4 = M.split_summary([e("income", 20000), e("expense", 9000, "food"), e("expense", 5000, "fun")])
ok("coach: low savings", M.coach(s4)["title"].startswith("Pay yourself"))
ok("coach: no income asks for income", M.coach(M.split_summary([e("expense", 500, "food")]))["title"] == "Add your income")
g = M.goal_view({"id": "x", "name": "Phone", "target": 50000.0, "saved": 5000.0, "deadline": "2027-05-06"}, date(2026, 11, 6))
ok("goal planner: (50000-5000)/6 = 7500 a month", g["months_left"] == 6 and abs(g["monthly"] - 7500) < 0.01 and g["pct"] == 10)

# ---- API
import httpx  # noqa: E402

U = "http://localhost:8001/api"
c = httpx.Client(timeout=30)
r = c.post(f"{U}/auth/login", json={"email": "demo@finlingo.com", "password": "Demo@123"}).json()
H = {"Authorization": f"Bearer {r['access_token']}", "X-TZ-Offset": "-330"}
MONTH = "2031-03"  # far-future month so real data is never touched
D = "2031-03-10"
made = []


def post(path, body):
    return c.post(f"{U}{path}", headers=H, json=body)


bad = post("/money/entries", {"kind": "expense", "amount": 0, "category": "food", "date": D})
ok("amount 0 -> 400", bad.status_code == 400)
ok("negative amount -> 400", post("/money/entries", {"kind": "expense", "amount": -5, "category": "food", "date": D}).status_code == 400)
ok("expense without category -> 400", post("/money/entries", {"kind": "expense", "amount": 100, "date": D}).status_code == 400)
ok("unknown category -> 400", post("/money/entries", {"kind": "expense", "amount": 100, "category": "yacht", "date": D}).status_code == 400)
ok("bad date -> 400", post("/money/entries", {"kind": "expense", "amount": 100, "category": "food", "date": "10-03-2031"}).status_code == 400)
ok("huge amount -> 400", post("/money/entries", {"kind": "expense", "amount": 1e12, "category": "food", "date": D}).status_code == 400)

for body in [
    {"kind": "income", "amount": 20000, "note": "pocket money", "date": D},
    {"kind": "expense", "amount": 10000, "category": "rent", "date": D},
    {"kind": "expense", "amount": 6000, "category": "shopping", "date": D},
    {"kind": "expense", "amount": 4000, "category": "sip", "date": D},
]:
    res = post("/money/entries", body)
    made.append(res.json().get("id"))
    ok(f"add {body['kind']} {body['amount']}", res.status_code == 200 and "user_id" not in res.json())

j = c.get(f"{U}/money/summary?month={MONTH}", headers=H).json()
ok("summary: 4 entries and 50/30/20", len(j["entries"]) == 4 and j["summary"]["pct"] == {"needs": 50.0, "wants": 30.0, "savings": 20.0})
ok("summary: income 20000, left 0", j["summary"]["income"] == 20000 and j["summary"]["left"] == 0)
ok("other month is empty", c.get(f"{U}/money/summary?month=2031-04", headers=H).json()["entries"] == [])
ok("bad month -> 400", c.get(f"{U}/money/summary?month=March", headers=H).status_code == 400)

# another user must not see or delete these
tmp = c.post(f"{U}/auth/register", json={"email": "money-test-other@example.com", "password": "Test@12345", "name": "Money Other"})
if tmp.status_code == 200:
    H2 = {"Authorization": f"Bearer {tmp.json()['access_token']}"}
    ok("other user sees nothing", c.get(f"{U}/money/summary?month={MONTH}", headers=H2).json()["entries"] == [])
    ok("other user cannot delete my entry", c.delete(f"{U}/money/entries/{made[1]}", headers=H2).status_code == 404)
    c.request("DELETE", f"{U}/auth/account", headers=H2, json={"password": "Test@12345"})
else:
    print("skip other-user checks:", tmp.status_code)

ok("delete entry", c.delete(f"{U}/money/entries/{made[1]}", headers=H).status_code == 200)
ok("delete again -> 404", c.delete(f"{U}/money/entries/{made[1]}", headers=H).status_code == 404)
for i in made:
    c.delete(f"{U}/money/entries/{i}", headers=H)
ok("cleanup leaves month empty", c.get(f"{U}/money/summary?month={MONTH}", headers=H).json()["entries"] == [])

# goals
ok("goal without name -> 400", post("/money/goals", {"name": " ", "target": 1000, "months": 3}).status_code == 400)
ok("goal 0 months -> 400", post("/money/goals", {"name": "x", "target": 1000, "months": 0}).status_code == 400)
ok("goal saved > target -> 400", post("/money/goals", {"name": "x", "target": 1000, "months": 3, "saved": 2000}).status_code == 400)
res = post("/money/goals", {"name": "TEST phone", "target": 50000, "months": 6, "saved": 5000})
gj = res.json()
ok("goal planner via API: 7,500 a month", res.status_code == 200 and abs(gj["monthly"] - 7500) < 0.01 and gj["months_left"] == 6)
res = post(f"/money/goals/{gj['id']}/add", {"amount": 7500})
ok("add 7,500 saved -> 12,500 and 25%", res.status_code == 200 and res.json()["saved"] == 12500 and res.json()["pct"] == 25)
res = post(f"/money/goals/{gj['id']}/add", {"amount": 999999})
ok("saved is capped at target and marked done", res.json()["saved"] == 50000 and res.json()["done"] is True)
ok("goal list includes it", any(x["id"] == gj["id"] for x in c.get(f"{U}/money/goals", headers=H).json()))
ok("delete goal", c.delete(f"{U}/money/goals/{gj['id']}", headers=H).status_code == 200)
ok("delete goal again -> 404", c.delete(f"{U}/money/goals/{gj['id']}", headers=H).status_code == 404)

print("\nFAILED: %s" % fails if fails else "\nALL PASSED")
sys.exit(1 if fails else 0)
