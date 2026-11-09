"""Password-reset safety tests. Needs the local MongoDB. Starts its own servers on ports 8003 (production-like) and 8004 (dev flag on)."""
import os
import subprocess
import sys
import time

import httpx
from dotenv import load_dotenv
from pymongo import MongoClient

fails = []


def ok(name, cond):
    print(("OK  " if cond else "BAD ") + name)
    if not cond:
        fails.append(name)


here = os.path.join(os.path.dirname(__file__), "..")
load_dotenv(os.path.join(here, ".env"))
db = MongoClient(os.environ["MONGO_URL"])[os.environ["DB_NAME"]]


def start(port, extra):
    env = {k: v for k, v in os.environ.items() if k != "DEV_RESET_LINKS"}
    env["DISABLE_RATE_LIMIT"] = "1"
    env.update(extra)
    p = subprocess.Popen([sys.executable, "-m", "uvicorn", "server:app", "--port", str(port)], cwd=here, env=env,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(45):
        try:
            if httpx.get(f"http://127.0.0.1:{port}/api/health", timeout=2).status_code == 200:
                return p
        except Exception:
            time.sleep(1)
    return p


EM = "reset-safety-test@example.com"
prod = start(8003, {"PRIVACY_EMAIL": "help@example.com"})
dev = start(8004, {"DEV_RESET_LINKS": "1"})
try:
    P, D = "http://127.0.0.1:8003/api", "http://127.0.0.1:8004/api"
    c = httpx.Client(timeout=30)
    db.users.delete_many({"email": EM})
    reg = c.post(f"{P}/auth/register", json={"email": EM, "password": "Original@123", "name": "Reset Test"}).json()
    uid = reg["id"]
    before = db.password_resets.count_documents({"user_id": uid})

    # ---- production-like server
    r = c.post(f"{P}/auth/forgot-password", json={"email": EM})
    j = r.json()
    ok("forgot-password answers 200", r.status_code == 200 and j["ok"] is True)
    ok("the reset token is NOT returned", j["reset_token"] is None and j["reset_path"] is None and "token" not in str(j).replace("reset_token", ""))
    ok("it says delivery is unavailable and points to Google", j["delivery"] == "unavailable" and "Google" in j["message"])
    ok("no reset record was created", db.password_resets.count_documents({"user_id": uid}) == before)
    ok("an unknown email gets the identical answer", c.post(f"{P}/auth/forgot-password", json={"email": "nobody-here@example.com"}).json() == j)
    spoof = c.post(f"{P}/auth/forgot-password", json={"email": EM}, headers={"X-Forwarded-For": "127.0.0.1"}).json()
    ok("a spoofed forwarded-for header does not unlock it", spoof["reset_token"] is None)
    ok("a made-up token does not reset anything", c.post(f"{P}/auth/reset-password", json={"token": "made-up-token-0123456789", "new_password": "Hacked@123"}).status_code == 400)
    ok("the original password still works", c.post(f"{P}/auth/login", json={"email": EM, "password": "Original@123"}).status_code == 200)
    ok("config shows the support email", c.get(f"{P}/auth/config").json().get("support_email") == "help@example.com")

    # ---- dev flag on, caller on this machine: the old behaviour for local development
    jd = c.post(f"{D}/auth/forgot-password", json={"email": EM}).json()
    ok("dev mode on this machine returns a link", jd["delivery"] == "dev" and jd["reset_token"] and jd["reset_path"].startswith("/reset-password?token="))
    ok("dev mode still hides unknown emails", c.post(f"{D}/auth/forgot-password", json={"email": "nobody-here@example.com"}).json()["reset_token"] is None)
    tok = jd["reset_token"]
    r2 = c.post(f"{D}/auth/reset-password", json={"token": tok, "new_password": "Changed@123"})
    ok("the dev link resets the password", r2.status_code == 200)
    ok("the link cannot be used twice", c.post(f"{D}/auth/reset-password", json={"token": tok, "new_password": "Again@12345"}).status_code == 400)
    ok("new password works, old one does not", c.post(f"{D}/auth/login", json={"email": EM, "password": "Changed@123"}).status_code == 200
       and c.post(f"{D}/auth/login", json={"email": EM, "password": "Original@123"}).status_code == 401)
finally:
    prod.terminate()
    dev.terminate()
    u = db.users.find_one({"email": EM})
    if u:
        for coll in ("user_stats", "password_resets"):
            db[coll].delete_many({"user_id": u["id"]})
        db.users.delete_one({"id": u["id"]})

print("\nFAILED: %s" % fails if fails else "\nALL PASSED")
sys.exit(1 if fails else 0)
