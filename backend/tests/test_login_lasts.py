"""A login lasts ~180 days and renews itself. Needs the local server on :8001 and local MongoDB."""
import os
import sys
import time
from datetime import datetime, timedelta, timezone

import httpx
import jwt
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
U = "http://localhost:8001/api"
fails = []


def ok(name, cond):
    print(("OK   " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)


email = f"lasts.{int(time.time())}@example.com"
c = httpx.Client(timeout=30)
r = c.post(f"{U}/auth/register", json={"email": email, "password": "Passw0rd!x", "name": "Lasts"})
tok = r.json()["access_token"]
exp = datetime.fromtimestamp(jwt.decode(tok, options={"verify_signature": False})["exp"], timezone.utc)
days = (exp - datetime.now(timezone.utc)).days
ok(f"a new login lasts about 180 days (got {days})", 175 <= days <= 181)

H = {"Authorization": f"Bearer {tok}"}
r = c.get(f"{U}/auth/me", headers=H)
ok("fresh login is not renewed yet", r.status_code == 200 and "x-new-token" not in r.headers)

uid = r.json()["id"]
secret = os.environ["JWT_SECRET"]
old = jwt.encode({"sub": uid, "email": email, "type": "access", "exp": datetime.now(timezone.utc) + timedelta(days=10)}, secret, algorithm="HS256")
r = c.get(f"{U}/auth/me", headers={"Authorization": f"Bearer {old}"})
new = r.headers.get("x-new-token")
ok("a login with 10 days left is renewed", r.status_code == 200 and bool(new))
if new:
    left = (datetime.fromtimestamp(jwt.decode(new, options={"verify_signature": False})["exp"], timezone.utc) - datetime.now(timezone.utc)).days
    ok(f"the renewed login lasts about 180 days (got {left})", left >= 175)
    ok("the renewed login works", c.get(f"{U}/auth/me", headers={"Authorization": f"Bearer {new}"}).status_code == 200)

expired = jwt.encode({"sub": uid, "email": email, "type": "access", "exp": datetime.now(timezone.utc) - timedelta(minutes=1)}, secret, algorithm="HS256")
ok("an expired login is refused", c.get(f"{U}/auth/me", headers={"Authorization": f"Bearer {expired}"}).status_code == 401)
cors = c.get(f"{U}/auth/me", headers={"Authorization": f"Bearer {old}", "Origin": "https://x.test"})
ok("browsers are allowed to read the renewal header", "x-new-token" in cors.headers.get("access-control-expose-headers", "").lower())

print("ALL OK" if not fails else f"FAILED: {fails}")
sys.exit(1 if fails else 0)
