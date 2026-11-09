"""Pro subscription tests. A fake Google Play API stands in for the real one; backend on port 8005 (needs local MongoDB)."""
import json
import os
import subprocess
import sys
import threading
import time
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer

import httpx
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from dotenv import load_dotenv
from pymongo import MongoClient

HERE = os.path.dirname(__file__)
fails = []


def ok(name, cond):
    print(("OK  " if cond else "BAD ") + name)
    if not cond:
        fails.append(name)


def iso(days):
    return (datetime.now(timezone.utc) + timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%S.000Z")


PURCHASES = {}  # token -> subscriptionsv2 body
ACKS = []
key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
pem = key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8, serialization.NoEncryption()).decode()


class Play(BaseHTTPRequestHandler):
    def _send(self, code, body):
        b = json.dumps(body).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(b)

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0)); self.rfile.read(n)
        if self.path == "/token":
            return self._send(200, {"access_token": "fake-access", "expires_in": 3600})
        if self.path.endswith(":acknowledge"):
            ACKS.append(self.path); return self._send(200, {})
        self._send(404, {})

    def do_GET(self):
        if self.headers.get("Authorization") != "Bearer fake-access":
            return self._send(401, {})
        tok = self.path.rsplit("/", 1)[-1]
        if tok in PURCHASES:
            return self._send(200, PURCHASES[tok])
        self._send(404, {})

    def log_message(self, *a):
        pass


def sub(state="SUBSCRIPTION_STATE_ACTIVE", days=30, product="finlearn_pro", ack="ACKNOWLEDGEMENT_STATE_PENDING"):
    return {"subscriptionState": state, "acknowledgementState": ack, "latestOrderId": "GPA.1",
            "lineItems": [{"productId": product, "expiryTime": iso(days)}]}


PURCHASES["tok-active"] = sub()
PURCHASES["tok-cancelled"] = sub("SUBSCRIPTION_STATE_CANCELED", 10)
PURCHASES["tok-expired"] = sub("SUBSCRIPTION_STATE_EXPIRED", -3)
PURCHASES["tok-holdoff"] = sub("SUBSCRIPTION_STATE_ON_HOLD", 5)
PURCHASES["tok-otherproduct"] = sub(product="something_else")
PURCHASES["tok-renew"] = sub(days=30)
threading.Thread(target=HTTPServer(("127.0.0.1", 9098), Play).serve_forever, daemon=True).start()

sa = json.dumps({"client_email": "svc@test.iam.gserviceaccount.com", "private_key": pem, "token_uri": "http://127.0.0.1:9098/token"})
env = {**os.environ, "DISABLE_RATE_LIMIT": "1", "PLAY_RTDN_SECRET": "rtdn-secret", "GOOGLE_PLAY_SERVICE_ACCOUNT_JSON": sa, "PLAY_API_BASE": "http://127.0.0.1:9098/v3", "PLAY_PACKAGE_NAME": "com.test.app"}
env.pop("SEED_DEMO", None)
srv = subprocess.Popen([sys.executable, "-m", "uvicorn", "server:app", "--port", "8005"], cwd=os.path.join(HERE, ".."),
                       env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
load_dotenv(os.path.join(HERE, "..", ".env"))
db = MongoClient(os.environ["MONGO_URL"])[os.environ["DB_NAME"]]
U = "http://127.0.0.1:8005/api"
EMAILS = ["pro.a@example.com", "pro.b@example.com"]
try:
    for _ in range(40):
        try:
            if httpx.get(f"{U}/health", timeout=2).status_code == 200:
                break
        except Exception:
            time.sleep(1)
    db.users.delete_many({"email": {"$in": EMAILS}})
    db.subscriptions.delete_many({"purchase_token": {"$regex": "^tok-"}})
    c = httpx.Client(timeout=30)

    def signup(email):
        j = c.post(f"{U}/auth/register", json={"email": email, "password": "Passw0rd!x", "name": "Pro Tester"}).json()
        return {"Authorization": f"Bearer {j['access_token']}"}, j["id"]

    A, aid = signup(EMAILS[0])
    B, bid = signup(EMAILS[1])
    st = c.get(f"{U}/subscription/status", headers=A).json()
    ok("new account starts a 7-day free Pro trial", st["pro"] is True and st["trial"]["active"] and st["trial"]["days_left"] == 7)
    ok("trial opens practice trading", c.get(f"{U}/practice/state", headers=A).status_code == 200)
    db.users.update_one({"id": aid}, {"$set": {"pro_until": iso(-1)}})
    st = c.get(f"{U}/subscription/status", headers=A).json()
    ok("after the trial: not Pro, trial marked ended", st["pro"] is False and st["trial"]["ended"] and not st["trial"]["active"])
    ok("practice locks again after the trial", c.get(f"{U}/practice/state", headers=A).status_code == 402)
    db.users.update_many({"id": {"$in": [aid, bid]}}, {"$unset": {"pro_until": "", "pro_source": ""}})  # plain free accounts for the checks below

    s = c.get(f"{U}/subscription/status", headers=A).json()
    ok("free account is not Pro", s["pro"] is False and s["until"] is None)
    ok("status lists both plans at the agreed prices", {p["id"]: p["price"] for p in s["plans"]} == {"monthly": 49, "yearly": 399})
    ok("yearly plan carries the saving figures", next(p for p in s["plans"] if p["id"] == "yearly")["save_pct"] == 32 and next(p for p in s["plans"] if p["id"] == "yearly")["was"] == 588)
    ok("billing is reported ready when configured", s["billing_ready"] is True)

    # free vs locked lessons
    courses = c.get(f"{U}/courses").json()
    free_total = locked_total = 0
    for co in courses:
        full = c.get(f"{U}/courses/{co['id']}/full", headers=A).json()
        cons = [x for ch in full["chapters"] for m in ch["modules"] for x in m["concepts"]]
        fl = [x for x in cons if not x["locked"]]
        free_total += len(fl); locked_total += len(cons) - len(fl)
        if len(cons) >= 3 and len(fl) != 2:
            ok(f"course {co['id']} has exactly 2 free lessons", False)
    ok("every course offers at most 2 free lessons", free_total <= 2 * len(courses) and locked_total > 0)
    ok("the first lessons are open", free_total >= len(courses))
    first = next(co for co in courses)
    full = c.get(f"{U}/courses/{first['id']}/full", headers=A).json()
    cons = [x for ch in full["chapters"] for m in ch["modules"] for x in m["concepts"]]
    free_c = next(x for x in cons if not x["locked"])
    lock_c = next(x for x in cons if x["locked"])
    ok("free lesson opens", c.get(f"{U}/concepts/{free_c['id']}", headers=A).status_code == 200)
    ok("locked lesson -> 402", c.get(f"{U}/concepts/{lock_c['id']}", headers=A).status_code == 402)
    ok("completing a locked lesson -> 402", c.post(f"{U}/progress/complete-concept", headers=A, json={"concept_id": lock_c["id"], "score": 100}).status_code == 402)
    ok("practice trading is Pro only", c.get(f"{U}/practice/state", headers=A).status_code == 402)
    ok("My money is Pro only", c.get(f"{U}/money/summary", headers=A).status_code == 402)
    ok("missions are Pro only", c.get(f"{U}/missions", headers=A).status_code == 402)
    ok("daily quests stay free", c.get(f"{U}/quests/today", headers=A).status_code == 200)
    q = c.get(f"{U}/quests/today", headers=A).json()["quests"]
    ok("free quests never ask for a trade or money log", all(x["id"] not in ("trade", "log") for x in q))
    ok("idea of the day stays free", c.get(f"{U}/explainer/today", headers=A).status_code in (200, 404))

    # purchases
    v = lambda t, h=A, p="finlearn_pro": c.post(f"{U}/subscription/verify", headers=h, json={"product_id": p, "purchase_token": t})
    ok("unknown product refused", v("tok-active", p="other").status_code == 400)
    ok("unknown token refused", v("nope").status_code == 402)
    ok("expired purchase refused", v("tok-expired").status_code == 402)
    ok("on-hold purchase refused", v("tok-holdoff").status_code == 402)
    ok("a different product's purchase refused", v("tok-otherproduct").status_code == 402)
    ok("still not Pro after refusals", c.get(f"{U}/subscription/status", headers=A).json()["pro"] is False)

    r = v("tok-active")
    ok("active purchase verified", r.status_code == 200 and r.json()["pro"] is True)
    ok("purchase was acknowledged with Google", any("tok-active:acknowledge" in a for a in ACKS))
    s = c.get(f"{U}/subscription/status", headers=A).json()
    ok("status now Pro with an expiry", s["pro"] is True and s["until"])
    ok("Pro opens locked lessons", c.get(f"{U}/concepts/{lock_c['id']}", headers=A).status_code == 200)
    ok("Pro opens practice trading", c.get(f"{U}/practice/state", headers=A).status_code == 200)
    ok("Pro opens My money", c.get(f"{U}/money/summary", headers=A).status_code == 200)
    u = c.get(f"{U}/subscription/usage", headers=A).json()
    ok("usage summary lists what the learner did with the tools", set(u) >= {"trades", "spends", "goals", "missions", "lessons"} and all(isinstance(v, int) for v in u.values()))
    ok("usage needs login", c.get(f"{U}/subscription/usage").status_code == 401)
    db.user_stats.update_one({"user_id": aid}, {"$set": {"coins": 1000, "streak_freezes": 2, "total_xp": 900000}})
    ok("Pro can hold a third streak freeze", c.post(f"{U}/shop/streak-freeze", headers=A).status_code == 200)
    db.user_stats.update_one({"user_id": aid}, {"$set": {"streak_freezes": 5}})
    r5 = c.post(f"{U}/shop/streak-freeze", headers=A)
    ok("Pro stops at 5 freezes", r5.status_code == 400 and "at most 5" in r5.json()["detail"])
    db.user_stats.update_one({"user_id": bid}, {"$set": {"coins": 1000, "streak_freezes": 2, "total_xp": 899999}})
    rf = c.post(f"{U}/shop/streak-freeze", headers=B)
    ok("a free account stops at 2 freezes and is told Pro holds more", rf.status_code == 400 and "at most 2" in rf.json()["detail"] and "Pro" in rf.json()["detail"])
    lb = {x["user_id"]: x for x in c.get(f"{U}/leaderboard", headers=A).json()}
    ok("the leaderboard marks Pro members, and only that (no dates leak)", lb[aid]["pro"] is True and lb[bid]["pro"] is False and "pro_until" not in lb[aid] and "role" not in lb[aid])

    # ---- Google Play real-time notifications (renewals, refunds, chargebacks)
    import base64
    note = lambda data, tok="rtdn-secret": c.post(f"{U}/subscription/rtdn", params={"token": tok}, json={"message": {"data": base64.b64encode(json.dumps(data).encode()).decode()}})
    sn = lambda t, ptype=2: {"packageName": "com.test.app", "subscriptionNotification": {"version": "1.0", "notificationType": ptype, "purchaseToken": t, "subscriptionId": "finlearn_pro"}}
    ok("a notification without the secret is refused", note(sn("tok-active"), tok="wrong").status_code == 403)
    ok("a notification with no secret at all is refused", c.post(f"{U}/subscription/rtdn", json={"message": {"data": ""}}).status_code == 403)
    ok("a message for another app is ignored", note({"packageName": "com.other.app", "subscriptionNotification": {"purchaseToken": "tok-active"}}).json().get("ignored") == "other app")
    ok("a test message is ignored", note({"packageName": "com.test.app", "testNotification": {"version": "1.0"}}).json().get("ignored"))
    ok("a purchase we never linked to an account is ignored", note(sn("tok-never-seen")).json().get("ignored"))
    ok("garbage is a 400", c.post(f"{U}/subscription/rtdn", params={"token": "rtdn-secret"}, json={"message": {"data": "!!notbase64!!"}}).status_code == 400)
    before_until = c.get(f"{U}/subscription/status", headers=A).json()["until"]
    PURCHASES["tok-active"] = sub(days=90)
    ok("a renewal notification extends Pro", note(sn("tok-active", 2)).json()["active"] is True and c.get(f"{U}/subscription/status", headers=A).json()["until"] > before_until)
    PURCHASES["tok-active"] = sub("SUBSCRIPTION_STATE_EXPIRED", -1)
    ok("a refund or revoke notification ends Pro at once", note(sn("tok-active", 12)).json()["active"] is False and c.get(f"{U}/subscription/status", headers=A).json()["pro"] is False)
    ok("and the Pro tools lock again", c.get(f"{U}/practice/state", headers=A).status_code == 402)
    PURCHASES["tok-active"] = sub()
    ok("the learner can restore Pro by verifying the purchase again", v("tok-active").status_code == 200 and c.get(f"{U}/subscription/status", headers=A).json()["pro"] is True)
    db.users.update_one({"id": aid}, {"$set": {"pro_token": "someone-else"}})
    PURCHASES["tok-active"] = sub("SUBSCRIPTION_STATE_EXPIRED", -1)
    note(sn("tok-active", 12))
    ok("an account that no longer owns the purchase is not changed", c.get(f"{U}/subscription/status", headers=A).json()["pro"] is True)
    db.users.update_one({"id": aid}, {"$set": {"pro_token": "tok-active"}})
    PURCHASES["tok-active"] = sub()
    full = c.get(f"{U}/courses/{first['id']}/full", headers=A).json()
    ok("nothing is marked locked for Pro", not any(x["locked"] for ch in full["chapters"] for m in ch["modules"] for x in m["concepts"]))
    ok("same account can verify again", v("tok-active").status_code == 200)
    ok("a purchase cannot be shared with another account", v("tok-active", B).status_code == 409)
    ok("other account is still free", c.get(f"{U}/subscription/status", headers=B).json()["pro"] is False)
    ok("cancelled-but-paid-up purchase counts", v("tok-cancelled", B).status_code == 200)

    # expiry and renewal refresh
    db.users.update_one({"id": bid}, {"$set": {"pro_until": iso(-1)}})
    PURCHASES["tok-cancelled"] = sub("SUBSCRIPTION_STATE_ACTIVE", 25)
    ok("an ended period is refreshed from Google (renewed)", c.get(f"{U}/subscription/status", headers=B).json()["pro"] is True)
    db.users.update_one({"id": bid}, {"$set": {"pro_until": iso(-1)}})
    PURCHASES["tok-cancelled"] = sub("SUBSCRIPTION_STATE_EXPIRED", -1)
    ok("a lapsed subscription turns Pro off", c.get(f"{U}/subscription/status", headers=B).json()["pro"] is False)
    ok("and locks the lessons again", c.get(f"{U}/concepts/{lock_c['id']}", headers=B).status_code == 402)

    # admin grant
    ok("normal user cannot grant Pro", c.post(f"{U}/admin/pro/grant", headers=A, json={"email": EMAILS[1], "days": 5}).status_code == 403)
    adm = c.post(f"{U}/auth/login", json={"email": os.environ.get("ADMIN_EMAIL", "admin@finlingo.com"), "password": os.environ.get("ADMIN_PASSWORD", "Admin@123")})
    if adm.status_code == 200:
        AD = {"Authorization": f"Bearer {adm.json()['access_token']}"}
        ok("admin can grant Pro", c.post(f"{U}/admin/pro/grant", headers=AD, json={"email": EMAILS[1], "days": 5}).status_code == 200)
        ok("granted account is Pro", c.get(f"{U}/subscription/status", headers=B).json()["pro"] is True)
        ok("admin can remove a grant", c.post(f"{U}/admin/pro/grant", headers=AD, json={"email": EMAILS[1], "days": 0}).status_code == 200
           and c.get(f"{U}/subscription/status", headers=B).json()["pro"] is False)
        ok("grant to unknown email -> 404", c.post(f"{U}/admin/pro/grant", headers=AD, json={"email": "nobody@example.com", "days": 5}).status_code == 404)
        ok("admin is always Pro", c.get(f"{U}/subscription/status", headers=AD).json()["pro"] is True)
    else:
        ok("admin login (set ADMIN_PASSWORD env to run these)", False)
    ok("no login -> 401", c.get(f"{U}/subscription/status").status_code == 401)
finally:
    srv.terminate()
    db.users.delete_many({"email": {"$in": EMAILS}})
    db.subscriptions.delete_many({"purchase_token": {"$regex": "^tok-"}})

print("\nFAILED: " + ", ".join(fails) if fails else "\nALL OK")
sys.exit(1 if fails else 0)
