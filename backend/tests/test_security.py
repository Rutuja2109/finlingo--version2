"""Abuse protection and public pages. Starts its own backend on port 8007 WITH rate limiting on (needs local MongoDB)."""
import os
import subprocess
import sys
import time

import httpx
from dotenv import load_dotenv
from pymongo import MongoClient

HERE = os.path.dirname(__file__)
fails = []


def ok(name, cond):
    print(("OK  " if cond else "BAD ") + name)
    if not cond:
        fails.append(name)


env = {k: v for k, v in os.environ.items() if k not in ("DISABLE_RATE_LIMIT", "DEV_RESET_LINKS", "SMTP_HOST", "RESEND_API_KEY", "RENDER", "TRUST_PROXY")}
env.update({"PRIVACY_EMAIL": "help@example.com", "PRIVACY_OPERATOR": "Test Operator"})
srv = subprocess.Popen([sys.executable, "-m", "uvicorn", "server:app", "--port", "8007"], cwd=os.path.join(HERE, ".."), env=env,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
load_dotenv(os.path.join(HERE, "..", ".env"))
db = MongoClient(os.environ["MONGO_URL"])[os.environ["DB_NAME"]]
B = "http://127.0.0.1:8007"
U = B + "/api"
EMS = [f"sec.test.{i}@example.com" for i in range(12)] + ["sec.login@example.com", "sec.other@example.com", "sec.short@example.com"]
try:
    for _ in range(60):
        try:
            if httpx.get(f"{U}/health", timeout=2).status_code == 200:
                break
        except Exception:
            time.sleep(1)
    db.users.delete_many({"email": {"$in": EMS}})
    c = httpx.Client(timeout=30)

    # ---- headers and public pages
    h = c.get(f"{U}/health")
    ok("API responses carry nosniff and no-referrer", h.headers.get("x-content-type-options") == "nosniff" and h.headers.get("referrer-policy") == "no-referrer")
    ok("no HSTS header off Render (local http)", "strict-transport-security" not in h.headers)
    for path in ("/privacy", "/terms", "/delete-account"):
        r = c.get(B + path)
        ok(f"{path} is a public page", r.status_code == 200 and "text/html" in r.headers["content-type"] and "{{" not in r.text)
        ok(f"{path} is locked down (CSP, no framing, no caching)", "default-src 'none'" in r.headers.get("content-security-policy", "") and r.headers.get("x-frame-options") == "DENY" and "no-store" in r.headers.get("cache-control", ""))
    ok("terms state the price, auto-renewal and how to cancel", all(x in c.get(B + "/terms").text for x in ("₹49", "₹399", "renews automatically", "Google Play", "not financial")))
    ok("terms and privacy show the support email and operator", "help@example.com" in c.get(B + "/terms").text and "Test Operator" in c.get(B + "/privacy").text)
    ok("the deletion page explains the in-app steps and that Pro is not cancelled", "Delete account" in c.get(B + "/delete-account").text and "does not cancel" in c.get(B + "/delete-account").text)
    ok("privacy now covers subscriptions and links the other pages", "Subscription data" in c.get(B + "/privacy").text and "/terms" in c.get(B + "/privacy").text and "/delete-account" in c.get(B + "/privacy").text)
    d = c.get(f"{U}/health/deep")
    ok("the deep health check confirms the database", d.status_code == 200 and d.json() == {"status": "ok", "db": "ok"})

    # ---- passwords
    ok("a 7-character password is refused at sign-up", c.post(f"{U}/auth/register", json={"email": EMS[14], "password": "Abc1234", "name": "Short"}).status_code == 422)
    ok("an 8-character password is accepted", c.post(f"{U}/auth/register", json={"email": EMS[14], "password": "Abcd1234", "name": "Short"}).status_code == 200)

    # ---- login: guessing a password is slowed down
    c.post(f"{U}/auth/register", json={"email": EMS[12], "password": "Right-pass-1", "name": "Login Test"})
    c.post(f"{U}/auth/register", json={"email": EMS[13], "password": "Other-pass-1", "name": "Other"})
    codes = [c.post(f"{U}/auth/login", json={"email": EMS[12], "password": f"wrong-{i}"}).status_code for i in range(8)]
    ok("8 wrong passwords are answered 401 each", codes == [401] * 8)
    r = c.post(f"{U}/auth/login", json={"email": EMS[12], "password": "Right-pass-1"})
    ok("the 9th try is refused with 429 and a Retry-After, even with the right password", r.status_code == 429 and int(r.headers.get("retry-after", "0")) > 0)
    ok("the message is calm and plain", "Too many attempts" in r.json()["detail"])
    ok("another account is not affected", c.post(f"{U}/auth/login", json={"email": EMS[13], "password": "Other-pass-1"}).status_code == 200)
    # a flood of failed logins from one address (different accounts each time) is also stopped, at a generous number
    flood = [c.post(f"{U}/auth/login", json={"email": f"nobody{i}@example.com", "password": "x" * 8}).status_code for i in range(70)]
    ok("a flood of failed logins from one address ends in 429 (after about 60 failures)", 429 in flood and 45 <= flood.index(429) <= 60)
    ok("while it is flooding, even a correct login from that address waits", c.post(f"{U}/auth/login", json={"email": EMS[13], "password": "Other-pass-1"}).status_code == 429)

    # ---- sign-up flood (generous: 30 an hour per address)
    codes = [c.post(f"{U}/auth/register", json={"email": f"sec.flood.{i}@example.com", "password": "Passw0rd!x", "name": "Flood"}).status_code for i in range(34)]
    ok("sign-ups from one address stop at 30 an hour (429 after)", codes.count(200) <= 30 and codes[-1] == 429 and 429 not in codes[:25])

    # ---- forgot password flood
    codes = [c.post(f"{U}/auth/forgot-password", json={"email": "victim@example.com"}).status_code for i in range(7)]
    ok("asking for reset emails for one address is limited to 5 an hour", codes[:5] == [200] * 5 and codes[5:] == [429, 429])
    r = c.post(f"{U}/auth/forgot-password", json={"email": "someone.else@example.com"})
    ok("with no email service set up the answer stays the safe 'cannot email yet'", r.status_code == 200 and r.json()["delivery"] == "unavailable" and r.json()["reset_token"] is None)
    ok("reset-link guessing is limited too", 429 in [c.post(f"{U}/auth/reset-password", json={"token": "x" * 20, "new_password": "Whatever123"}).status_code for _ in range(34)])
finally:
    srv.terminate()
    db.users.delete_many({"email": {"$in": EMS + [f"sec.flood.{i}@example.com" for i in range(34)]}})

print("\nFAILED: " + ", ".join(fails) if fails else "\nALL OK")
sys.exit(1 if fails else 0)
