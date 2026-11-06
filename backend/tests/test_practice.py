"""Practice trading tests. Run against a local server: python backend/tests/test_practice.py
Uses the demo account (needs the server on :8001). Pure-logic checks run without it."""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import practice as P  # noqa: E402

fails = []


def ok(name, cond):
    print(("OK  " if cond else "BAD ") + name)
    if not cond:
        fails.append(name)


# ---- pure logic
t = 1_800_000_000
ok("prices are deterministic", P.normal_price(P.ASSETS[0], t) == P.normal_price(P.ASSETS[0], t))
ok("prices stay positive and sane", all(0.3 * a["base"] < P.normal_price(a, t + k * 997) < 3 * a["base"] for a in P.ASSETS for k in range(400)))
ok("bitcoin moves more than the index fund",
   (lambda f: f(P.BY_ID["btc"]) > f(P.BY_ID["nifty"]))(lambda a: max(P.normal_price(a, t + k * 300) for k in range(300)) / min(P.normal_price(a, t + k * 300) for k in range(300))))
ok("crash: bitcoin falls hard, gold does not", P.scenario_mult(P.BY_ID["btc"], 5, 24) < 0.6 and P.scenario_mult(P.BY_ID["gold"], 5, 24) > 0.8)
ok("crash: index fund falls a bit", 0.55 < P.scenario_mult(P.BY_ID["nifty"], 5, 24) < 0.9)

acct = P.new_account("u")
acct["positions"]["btc"] = {"units": 1.0, "cost": 6500000.0}
acct["scenario"] = {"id": "crash", "started_at": t, "salt": 5, "base": {a["id"]: 100.0 for a in P.ASSETS}, "before_value": 100000.0}
ok("scenario price at start near base", abs(P.price_of(acct, P.BY_ID["btc"], t + 0.1) - 100.0 * P.scenario_mult(P.BY_ID["btc"], 5, 0)) < 1e-6)
late = t + P.SCEN_TICKS * P.SCEN_TICK_SECONDS + 5
ok("settle ends the scenario and records a result", P.settle_scenario(acct, late) and acct["scenario"] is None and acct["last_result"]["after"] < acct["last_result"]["before"] + 1e12)
ok("price continues smoothly after settle", abs(P.price_of(acct, P.BY_ID["btc"], t + P.SCEN_TICKS * P.SCEN_TICK_SECONDS) / (100.0 * P.scenario_mult(P.BY_ID["btc"], 5, P.SCEN_TICKS - 1)) - 1) < 1e-6)

# ---- API
try:
    import httpx
except ImportError:
    print("httpx missing, skipping API tests")
    sys.exit(1 if fails else 0)

U = "http://localhost:8001/api"
c = httpx.Client(timeout=30)
r = c.post(f"{U}/auth/login", json={"email": "demo@finlingo.com", "password": "Demo@123"}).json()
H = {"Authorization": f"Bearer {r['access_token']}", "X-TZ-Offset": "-330"}

s = c.post(f"{U}/practice/reset", headers=H).json()
ok("reset gives 1,00,000 cash", s["cash"] == 100000 and s["positions"] == [] and s["total"] == 100000)
s = c.get(f"{U}/practice/state?asset=gold&tf=1D", headers=H).json()
ok("state returns 4 assets and a chart for the chosen asset", len(s["assets"]) == 4 and s["selected"]["asset"] == "gold" and len(s["selected"]["series"]) == 144)

res = c.post(f"{U}/practice/trade", headers=H, json={"asset": "nifty", "side": "buy", "amount": 50})
ok("buy below minimum -> 400", res.status_code == 400)
res = c.post(f"{U}/practice/trade", headers=H, json={"asset": "nifty", "side": "buy", "amount": 999999})
ok("buy more than cash -> 400", res.status_code == 400)
res = c.post(f"{U}/practice/trade", headers=H, json={"asset": "doge", "side": "buy", "amount": 500})
ok("unknown asset -> 400", res.status_code == 400)
res = c.post(f"{U}/practice/trade", headers=H, json={"asset": "nifty", "side": "sell", "percent": 100})
ok("sell without owning -> 400", res.status_code == 400)

res = c.post(f"{U}/practice/trade", headers=H, json={"asset": "nifty", "side": "buy", "amount": 40000})
st = res.json()["state"]
ok("buy 40,000 -> cash 60,000 and one position", res.status_code == 200 and abs(st["cash"] - 60000) < 0.01 and len(st["positions"]) == 1)
ok("total stays about 1,00,000 right after buying", abs(st["total"] - 100000) < 5)
c.post(f"{U}/practice/trade", headers=H, json={"asset": "btc", "side": "buy", "amount": 30000})
res = c.post(f"{U}/practice/trade", headers=H, json={"asset": "btc", "side": "sell", "percent": 50})
j = res.json()
ok("sell half of bitcoin returns cash and keeps half", res.status_code == 200 and abs(j["result"]["amount"] - 15000) < 200 and len(j["state"]["positions"]) == 2)
res = c.post(f"{U}/practice/trade", headers=H, json={"asset": "btc", "side": "sell", "percent": 100})
ok("sell all removes the position", len(res.json()["state"]["positions"]) == 1)
ok("history lists trades newest first", len(res.json()["state"]["trades"]) == 4 and res.json()["state"]["trades"][0]["side"] == "sell")

# Crash replay
before = c.get(f"{U}/practice/state", headers=H).json()["total"]
st = c.post(f"{U}/practice/scenario/start", headers=H, json={"id": "crash"}).json()
ok("scenario starts active", st["scenario"]["active"] is True)
res = c.post(f"{U}/practice/scenario/start", headers=H, json={"id": "crash"})
ok("second scenario while running -> 400", res.status_code == 400)
time.sleep(3)
mid = c.get(f"{U}/practice/state", headers=H).json()
ok("during the replay the series is the scenario's and ticks advance", mid["scenario"]["active"] and mid["scenario"]["tick"] >= 3)
time.sleep(P.SCEN_TICKS * P.SCEN_TICK_SECONDS)
end = c.get(f"{U}/practice/state", headers=H).json()
ok("replay settles and records before/after", not end["scenario"]["active"] and end["last_result"] and end["last_result"]["after"] < end["last_result"]["before"])
ok("index fund holding lost value in the crash", end["total"] < before)
again = c.get(f"{U}/practice/state", headers=H).json()
ok("value is stable after settle (no jump)", abs(again["total"] - end["total"]) < end["total"] * 0.02)

# Tour reward only once
xp0 = c.get(f"{U}/stats/me", headers=H).json()["total_xp"]
c.post(f"{U}/practice/reset", headers=H)
j1 = c.post(f"{U}/practice/tour-complete", headers=H, json={"skipped": False}).json()
j2 = c.post(f"{U}/practice/tour-complete", headers=H, json={"skipped": False}).json()
xp1 = c.get(f"{U}/stats/me", headers=H).json()["total_xp"]
ok("tour reward given once (or already done earlier)", j2["xp"] == 0 and (j1["xp"] in (0, P.TOUR_XP)) and xp1 - xp0 == j1["xp"])
ok("state reports tour_done", c.get(f"{U}/practice/state", headers=H).json()["tour_done"] is True)

c.post(f"{U}/practice/reset", headers=H)
print("\nFAILED: %s" % fails if fails else "\nALL PASSED")
sys.exit(1 if fails else 0)
