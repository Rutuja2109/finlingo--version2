"""Password reset by email, end to end. A tiny fake SMTP server catches the emails; the backend runs on port 8008 (needs local MongoDB)."""
import email
import os
import re
import socketserver
import subprocess
import sys
import threading
import time
import uuid
from datetime import datetime, timedelta, timezone

import httpx
from dotenv import load_dotenv
from pymongo import MongoClient

HERE = os.path.dirname(__file__)
fails = []
MAILS = []


def ok(name, cond):
    print(("OK  " if cond else "BAD ") + name)
    if not cond:
        fails.append(name)


class SMTP(socketserver.StreamRequestHandler):
    def handle(self):
        def w(s):
            self.wfile.write((s + "\r\n").encode())
            self.wfile.flush()
        w("220 test")
        data, buf, rcpt = False, [], None
        while True:
            line = self.rfile.readline()
            if not line:
                break
            t = line.decode(errors="replace").rstrip("\r\n")
            if data:
                if t == ".":
                    MAILS.append({"to": rcpt, "raw": "\n".join(buf)})
                    data, buf = False, []
                    w("250 ok")
                else:
                    buf.append(t[1:] if t.startswith("..") else t)
                continue
            u = t.upper()
            if u.startswith(("EHLO", "HELO")):
                w("250 test")
            elif u.startswith("RCPT TO"):
                rcpt = t.split("<")[1].split(">")[0]
                w("250 ok")
            elif u == "DATA":
                data = True
                w("354 go")
            elif u == "QUIT":
                w("221 bye")
                break
            else:
                w("250 ok")


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


smtp = Server(("127.0.0.1", 2525), SMTP)
threading.Thread(target=smtp.serve_forever, daemon=True).start()

env = {k: v for k, v in os.environ.items() if k not in ("DEV_RESET_LINKS", "RESEND_API_KEY")}
env.update({"DISABLE_RATE_LIMIT": "1", "SMTP_HOST": "127.0.0.1", "SMTP_PORT": "2525", "SMTP_STARTTLS": "0",
            "MAIL_FROM": "FinLearn <noreply@finlearn.test>", "PUBLIC_BASE_URL": "http://127.0.0.1:8008"})
srv = subprocess.Popen([sys.executable, "-m", "uvicorn", "server:app", "--port", "8008"], cwd=os.path.join(HERE, ".."), env=env,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
load_dotenv(os.path.join(HERE, "..", ".env"))
db = MongoClient(os.environ["MONGO_URL"])[os.environ["DB_NAME"]]
B = "http://127.0.0.1:8008"
U = B + "/api"
EM, GM = "mail.reset.test@example.com", "mail.google.test@example.com"


def wait_mail(n, timeout=8):
    end = time.time() + timeout
    while len(MAILS) < n and time.time() < end:
        time.sleep(0.2)
    return len(MAILS) >= n


def body(mail):
    """The readable text of an email, decoded the way a mail app would (quoted-printable and all)."""
    msg = email.message_from_string(mail["raw"])
    parts = [p.get_payload(decode=True).decode("utf-8", "replace") for p in msg.walk() if p.get_content_maintype() == "text"]
    return "\n".join(parts)


def link_in(mail):
    m = re.search(r"http://127\.0\.0\.1:8008/reset-password\?token=([0-9a-f]+)", body(mail))
    return m.group(1) if m else None


try:
    for _ in range(60):
        try:
            if httpx.get(f"{U}/health", timeout=2).status_code == 200:
                break
        except Exception:
            time.sleep(1)
    db.users.delete_many({"email": {"$in": [EM, GM]}})
    c = httpx.Client(timeout=30)
    ok("the app is told that email reset is available", c.get(f"{U}/auth/config").json()["email_reset"] is True)

    j = c.post(f"{U}/auth/register", json={"email": EM, "password": "Original-pass-1", "name": "Mail Tester"}).json()
    uid = j["id"]

    # ---- ask for a link
    r = c.post(f"{U}/auth/forgot-password", json={"email": EM})
    ok("asking answers with a neutral message and never returns the link", r.status_code == 200 and r.json()["delivery"] == "email" and r.json()["reset_token"] is None and r.json()["reset_path"] is None and "token" not in str(r.json()).replace("reset_token", ""))
    ok("the email arrives, addressed to the account", wait_mail(1) and MAILS[0]["to"] == EM)
    tok1 = link_in(MAILS[0])
    ok("it contains a one-time reset link and a clear subject", bool(tok1) and "Reset your FinLearn password" in MAILS[0]["raw"] and "Mail Tester" in body(MAILS[0]))
    doc = db.password_resets.find_one({"user_id": uid, "used": False})
    ok("only a hash of the link is stored, never the link itself", doc and "token_hash" in doc and "token" not in doc and doc["token_hash"] != tok1)

    n = len(MAILS)
    r2 = c.post(f"{U}/auth/forgot-password", json={"email": "nobody.here@example.com"})
    time.sleep(1.2)
    ok("an unknown email gets the same answer and no email is sent", r2.json() == r.json() and len(MAILS) == n)

    # ---- google-only accounts get a helpful message, not a link
    db.users.insert_one({"id": str(uuid.uuid4()), "email": GM, "name": "Google Person", "role": "user", "password_hash": "", "google_linked": True, "created_at": datetime.now(timezone.utc).isoformat()})
    c.post(f"{U}/auth/forgot-password", json={"email": GM})
    ok("a Google-only account is told to use Continue with Google (no link)", wait_mail(n + 1) and MAILS[-1]["to"] == GM and "Continue with Google" in body(MAILS[-1]) and "reset-password?token" not in body(MAILS[-1]))

    # ---- the hosted page
    page = c.get(f"{B}/reset-password?token={tok1}")
    ok("the emailed link opens a simple password form in any browser", page.status_code == 200 and 'name="password"' in page.text and "form-action 'self'" in page.headers["content-security-policy"])
    ok("a link with no token says it is not valid", c.get(f"{B}/reset-password").status_code == 400)
    ok("mismatched passwords are explained", "do not match" in c.post(f"{B}/reset-password", data={"token": tok1, "password": "Brand-new-pass-1", "password2": "different-pass-1"}).text)
    ok("a short password is explained", "at least 8" in c.post(f"{B}/reset-password", data={"token": tok1, "password": "short", "password2": "short"}).text)
    ok("the link still works after those mistakes", c.get(f"{B}/reset-password?token={tok1}").status_code == 200 and db.password_resets.find_one({"user_id": uid, "used": False}) is not None)

    # ---- a newer request cancels the older link
    c.post(f"{U}/auth/forgot-password", json={"email": EM})
    time.sleep(1.5)
    ok("a second request sends a second email", len([m for m in MAILS if m["to"] == EM]) == 2)
    tok2 = link_in([m for m in MAILS if m["to"] == EM][-1])
    ok("the newer link is different", tok2 and tok2 != tok1)
    stale = c.post(f"{B}/reset-password", data={"token": tok1, "password": "Brand-new-pass-1", "password2": "Brand-new-pass-1"})
    ok("the older link no longer works", stale.status_code == 400 and "already used" in stale.text)

    # ---- use the newer link
    before = len(MAILS)
    done = c.post(f"{B}/reset-password", data={"token": tok2, "password": "Brand-new-pass-1", "password2": "Brand-new-pass-1"})
    ok("choosing a new password works", done.status_code == 200 and "Password changed" in done.text)
    ok("the new password logs in and the old one does not", c.post(f"{U}/auth/login", json={"email": EM, "password": "Brand-new-pass-1"}).status_code == 200 and c.post(f"{U}/auth/login", json={"email": EM, "password": "Original-pass-1"}).status_code == 401)
    ok("a 'your password was changed' notice is emailed", wait_mail(before + 1) and any("password for your FinLearn account was just changed" in body(m) for m in MAILS[before:]))
    again = c.post(f"{B}/reset-password", data={"token": tok2, "password": "Another-pass-123", "password2": "Another-pass-123"})
    ok("the link cannot be used twice", again.status_code == 400 and c.post(f"{U}/auth/login", json={"email": EM, "password": "Another-pass-123"}).status_code == 401)

    # ---- expiry and the API route
    c.post(f"{U}/auth/forgot-password", json={"email": EM})
    time.sleep(1.5)
    tok3 = link_in([m for m in MAILS if m["to"] == EM][-1])
    db.password_resets.update_many({"user_id": uid, "used": False}, {"$set": {"expires_at": (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat()}})
    exp = c.post(f"{B}/reset-password", data={"token": tok3, "password": "Brand-new-pass-2", "password2": "Brand-new-pass-2"})
    ok("an expired link says so and changes nothing", exp.status_code == 400 and "expired" in exp.text and c.post(f"{U}/auth/login", json={"email": EM, "password": "Brand-new-pass-1"}).status_code == 200)
    ok("the API route also needs 8 characters", c.post(f"{U}/auth/reset-password", json={"token": "x" * 20, "new_password": "short77"}).status_code == 422)
finally:
    srv.terminate()
    smtp.shutdown()
    u = db.users.find_one({"email": EM})
    if u:
        for coll in ("user_stats", "password_resets"):
            db[coll].delete_many({"user_id": u["id"]})
    db.users.delete_many({"email": {"$in": [EM, GM]}})

print("\nFAILED: " + ", ".join(fails) if fails else "\nALL OK")
sys.exit(1 if fails else 0)
