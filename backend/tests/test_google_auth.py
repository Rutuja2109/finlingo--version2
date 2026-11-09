"""Google sign-in tests. No real Google account is used: tokens are signed with a throwaway key, and a local fake
key server stands in for Google's. Part 2 starts its own backend on port 8002 (needs the local MongoDB)."""
import json
import os
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import jwt  # noqa: E402
from cryptography.hazmat.primitives.asymmetric import rsa  # noqa: E402

import google_auth as G  # noqa: E402

fails = []


def ok(name, cond):
    print(("OK  " if cond else "BAD ") + name)
    if not cond:
        fails.append(name)


CLIENT = "test-client.apps.googleusercontent.com"
priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
other = rsa.generate_private_key(public_exponent=65537, key_size=2048)
now = int(time.time())


def token(extra=None, key=priv, alg="RS256", kid="k1"):
    claims = {"iss": "https://accounts.google.com", "aud": CLIENT, "sub": "1234567890", "email": "Ada.Test@Example.com",
              "email_verified": True, "name": "Ada Test", "picture": "https://example.com/a.png", "iat": now - 5, "exp": now + 3600}
    claims.update(extra or {})
    return jwt.encode({k: v for k, v in claims.items() if v is not None}, key, algorithm=alg, headers={"kid": kid})


class FakeKeys:  # stands in for PyJWKClient
    def get_signing_key_from_jwt(self, t):
        class K:
            key = priv.public_key()
        return K()


def verify(t, aud=None):
    try:
        return G.verify_id_token(t, aud if aud is not None else [CLIENT], keys=FakeKeys())
    except ValueError as e:
        return str(e)


# ---- part 1: the checker
c = verify(token())
ok("valid token accepted, email lower-cased", isinstance(c, dict) and c["email"] == "ada.test@example.com" and c["sub"] == "1234567890")
ok("second issuer form accepted", isinstance(verify(token({"iss": "accounts.google.com"})), dict))
ok("wrong audience refused", verify(token({"aud": "someone-elses-client"})) == "Google sign-in could not be verified")
ok("any one of several client ids accepted", isinstance(verify(token(), [CLIENT, "other"]), dict))
ok("expired refused", verify(token({"exp": now - 600})) == "Google sign-in could not be verified")
ok("wrong issuer refused", verify(token({"iss": "https://evil.example.com"})) == "Google sign-in could not be verified")
ok("signed with another key refused", verify(token(key=other)) == "Google sign-in could not be verified")
ok("HS256 forged with a public value refused", verify(jwt.encode({"iss": "https://accounts.google.com", "aud": CLIENT, "sub": "1", "email": "a@b.com", "email_verified": True, "iat": now, "exp": now + 99}, "secret-secret-secret-secret-123", algorithm="HS256")) == "Google sign-in could not be verified")
ok("unsigned (alg none) refused", verify(jwt.encode({"iss": "https://accounts.google.com", "aud": CLIENT, "sub": "1", "email": "a@b.com", "email_verified": True, "iat": now, "exp": now + 99}, None, algorithm="none")) == "Google sign-in could not be verified")
ok("email not verified refused", verify(token({"email_verified": False})) == "Your Google email is not verified")
ok("no email refused", verify(token({"email": None})) == "Your Google email is not verified")
ok("missing expiry refused", verify(token({"exp": None})) == "Google sign-in could not be verified")
ok("garbage refused", verify("not.a.token") == "Google sign-in could not be verified")
ok("no client id configured refused", verify(token(), []) == "Google sign-in is not set up")

# ---- part 2: the real endpoint, against a fake key server
jwk = json.loads(jwt.algorithms.RSAAlgorithm.to_jwk(priv.public_key()))
jwk.update({"kid": "k1", "alg": "RS256", "use": "sig"})


class H(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({"keys": [jwk]}).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers(); self.wfile.write(body)

    def log_message(self, *a):
        pass


keysrv = HTTPServer(("127.0.0.1", 9099), H)
threading.Thread(target=keysrv.serve_forever, daemon=True).start()

env = {**os.environ, "DISABLE_RATE_LIMIT": "1", "GOOGLE_CLIENT_IDS": CLIENT, "GOOGLE_JWKS_URL": "http://127.0.0.1:9099/jwks"}
srv = subprocess.Popen([sys.executable, "-m", "uvicorn", "server:app", "--port", "8002"], cwd=os.path.join(os.path.dirname(__file__), ".."),
                       env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
import httpx  # noqa: E402
from dotenv import load_dotenv  # noqa: E402
from pymongo import MongoClient  # noqa: E402

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
db = MongoClient(os.environ["MONGO_URL"])[os.environ["DB_NAME"]]
U = "http://127.0.0.1:8002/api"
EM = "ada.test@example.com"
EM2 = "pre-hijack-test@example.com"
try:
    for _ in range(40):
        try:
            if httpx.get(f"{U}/health", timeout=2).status_code == 200:
                break
        except Exception:
            time.sleep(1)
    db.users.delete_many({"email": {"$in": [EM, EM2]}})
    c = httpx.Client(timeout=30)

    ok("config reports the client id", c.get(f"{U}/auth/config").json()["google_client_id"] == CLIENT)
    ok("bad token -> 401", c.post(f"{U}/auth/google", json={"id_token": "nope"}).status_code == 401)
    ok("wrong audience -> 401", c.post(f"{U}/auth/google", json={"id_token": token({"aud": "x"})}).status_code == 401)
    ok("unverified email -> 401", c.post(f"{U}/auth/google", json={"id_token": token({"email_verified": False})}).status_code == 401)

    r = c.post(f"{U}/auth/google", json={"id_token": token()})
    j = r.json()
    ok("new Google user is created and logged in", r.status_code == 200 and j["email"] == EM and j["new_account"] is True and j["access_token"] and j["name"] == "Ada Test")
    me = c.get(f"{U}/auth/me", headers={"Authorization": f"Bearer {j['access_token']}"})
    ok("our own login token works on the API", me.status_code == 200 and me.json()["email"] == EM)
    ok("starting stats were created (50 coins)", c.get(f"{U}/stats/me", headers={"Authorization": f"Bearer {j['access_token']}"}).json()["coins"] == 50)
    r2 = c.post(f"{U}/auth/google", json={"id_token": token()})
    ok("signing in again finds the same account", r2.status_code == 200 and r2.json()["id"] == j["id"] and r2.json()["new_account"] is False)
    ok("only one user document exists", db.users.count_documents({"email": EM}) == 1)
    ok("a Google-only account cannot log in with a blank password", c.post(f"{U}/auth/login", json={"email": EM, "password": ""}).status_code in (401, 422))
    r3 = c.post(f"{U}/auth/google", json={"id_token": token({"sub": "999"})})
    ok("same email, different Google account -> 409", r3.status_code == 409)

    # an earlier password sign-up for the same email loses its password once the real owner signs in with Google
    reg = c.post(f"{U}/auth/register", json={"email": EM2, "password": "Attacker@123", "name": "Squatter"})
    uid = reg.json()["id"]
    db.password_resets.insert_one({"id": "t", "user_id": uid, "token": "pending-reset-token", "expires_at": "2999-01-01T00:00:00+00:00", "used": False})
    ok("password account exists and can log in", c.post(f"{U}/auth/login", json={"email": EM2, "password": "Attacker@123"}).status_code == 200)
    g = c.post(f"{U}/auth/google", json={"id_token": token({"email": EM2, "sub": "555"})})
    ok("owner signs in with Google and gets the existing account", g.status_code == 200 and g.json()["id"] == uid and g.json()["new_account"] is False)
    ok("the squatter's password no longer works", c.post(f"{U}/auth/login", json={"email": EM2, "password": "Attacker@123"}).status_code == 401)
    ok("pending reset links were removed", db.password_resets.count_documents({"user_id": uid}) == 0)

    ok("old Emergent endpoint is gone", c.post(f"{U}/auth/google/session", json={"session_id": "x"}).status_code in (404, 405))
finally:
    srv.terminate()
    keysrv.shutdown()
    for e in (EM, EM2):
        u = db.users.find_one({"email": e})
        if u:
            for coll in ("user_stats", "password_resets"):
                db[coll].delete_many({"user_id": u["id"]})
            db.users.delete_one({"id": u["id"]})

print("\nFAILED: %s" % fails if fails else "\nALL PASSED")
sys.exit(1 if fails else 0)
