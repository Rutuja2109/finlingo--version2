"""Play Store phone screenshots from the running web app, with a populated Pro account (12 Nov 2026 layout).

Needs: local MongoDB, backend on :8001, web dev server on :3000 (REACT_APP_BACKEND_URL=http://localhost:8001),
`pip install websocket-client httpx pymongo python-dotenv`.
Run:  python design/store/make_shots_v2.py     (writes design/store/out/v2/*.png, 1080x2160)
"""
import base64
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import httpx
from dotenv import load_dotenv
from pymongo import MongoClient

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_assets as MA  # reuse the headless-Edge helper

HERE = Path(__file__).resolve().parent
OUT = HERE / "out" / "v2"
OUT.mkdir(parents=True, exist_ok=True)
MA.OUT = OUT
APP, API = MA.APP, MA.API

load_dotenv(HERE.parent.parent / "backend" / ".env")
db = MongoClient(os.environ["MONGO_URL"])[os.environ["DB_NAME"]]


def make_pro_user():
    email = f"shots.{int(time.time()) % 100000}@example.com"
    j = httpx.post(f"{API}/auth/register", json={"email": email, "password": "Passw0rd!x", "name": "Aarav"}, timeout=30).json()
    until = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
    db.users.update_one({"id": j["id"]}, {"$set": {"pro_until": until, "pro_source": "play"}})
    return j["access_token"]


def populate(token):
    H = {"Authorization": f"Bearer {token}"}
    c = httpx.Client(headers=H, timeout=30, base_url=API)
    today = datetime.now().date()
    d = lambda n: (today - timedelta(days=n)).isoformat()
    rows = [("income", 25000, None, "Pocket money and stipend", 6), ("expense", 6500, "rent", "Hostel share", 5),
            ("expense", 2400, "food", "Groceries", 4), ("expense", 900, "transport", "Metro card", 3),
            ("expense", 1800, "eating_out", "Dinner with friends", 3), ("expense", 1200, "shopping", "Sneakers", 2),
            ("expense", 599, "subs", "Streaming", 2), ("expense", 2000, "sip", "Monthly SIP", 1), ("expense", 1000, "savings", "Savings", 1),
            ("expense", 450, "fun", "Movie night", 0)]
    for kind, amt, cat, note, ago in rows:
        body = {"kind": kind, "amount": amt, "note": note, "date": d(ago)}
        if cat:
            body["category"] = cat
        c.post("/money/entries", json=body)
    c.post("/money/goals", json={"name": "New phone", "target": 30000, "months": 6, "saved": 12000})
    c.post("/practice/tour-complete", json={"skipped": True})
    for asset, amt in (("nifty", 40000), ("gold", 25000), ("btc", 10000)):
        c.post("/practice/trade", json={"asset": asset, "side": "buy", "amount": amt})
    for mid in ("upi-history", "two-step", "emergency-start"):
        c.post(f"/missions/{mid}/complete", json={"note": "Done"})
    c.post("/explainer/read", json={})
    return H


def main():
    token = make_pro_user()
    H = populate(token)
    b = MA.Cdp()
    try:
        b.size(390, 780, 2.7692)
        b.go(APP + "/", 3)
        b.js(f"localStorage.clear(); localStorage.setItem('fl_token', {json.dumps(token)}); localStorage.setItem('fl_goal_seen','1')")

        def snap(path, name, wait=4.5, js=None):
            b.go(APP + path, wait)
            b.js("(()=>{const x=[...document.querySelectorAll('button')].find(e=>e.textContent.trim()==='Later'); if(x) x.click(); return 1})()")
            if js:
                b.js(js)
            time.sleep(1.2)
            b.shot(name)

        snap("/dashboard", "1-home.png")
        snap("/dashboard", "2-today-mission.png",
             js="document.querySelector('[data-testid=today-strip]').scrollIntoView({block:'start'}); window.scrollBy(0,-70)")
        snap("/courses", "3-courses.png")
        snap("/practice", "4-practice.png")
        snap("/money", "5-my-money.png")
        snap("/missions", "6-missions.png")
        courses = httpx.get(f"{API}/courses", timeout=30).json()
        crypto = next(x for x in courses if x["slug"] == "bitcoin-and-crypto")
        full = httpx.get(f"{API}/courses/{crypto['id']}/full", headers=H, timeout=30).json()
        tip = next(cn for cn in full["chapters"][0]["modules"][0]["concepts"] if "group chat" in cn["title"].lower())
        b.go(f"{APP}/concept/{tip['id']}", 4)
        b.js("""(async()=>{const w=ms=>new Promise(r=>setTimeout(r,ms));
          for(let i=0;i<10;i++){ if(document.querySelector('[data-testid=scenario-choice-0]')) break;
            const fc=document.querySelector('[data-testid=flashcard]'); if(fc){fc.click(); await w(300);}
            const n=document.querySelector('[data-testid=btn-next-lesson]'); if(n) n.click(); await w(600);} return true})()""")
        time.sleep(1)
        b.shot("7-lesson-choice.png")
        b.js("document.querySelector('[data-testid=scenario-choice-0]').click()")
        time.sleep(1.2)
        b.js("document.querySelector('[data-testid=scenario-feedback]').scrollIntoView({block:'start'}); window.scrollBy(0,-90)")
        time.sleep(1)
        b.shot("8-lesson-result.png")
    finally:
        b.close()


if __name__ == "__main__":
    main()
