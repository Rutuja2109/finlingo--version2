"""Creates a local test account in a given Pro state and prints its login token (for browser checks).
Usage: python tests/ui_state.py trial|trial2|ended|free|paid   (needs the local backend on :8001)"""
import os
import sys
import time
from datetime import datetime, timedelta, timezone

import httpx
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
db = MongoClient(os.environ["MONGO_URL"])[os.environ["DB_NAME"]]
state = sys.argv[1]
email = f"ui.{state}.{int(time.time()) % 100000}@example.com"
j = httpx.post("http://localhost:8001/api/auth/register", json={"email": email, "password": "Passw0rd!x", "name": f"UI {state}"}, timeout=30).json()
iso = lambda d: (datetime.now(timezone.utc) + timedelta(days=d)).isoformat()
sets = {
    "trial": {},
    "trial2": {"pro_until": iso(1.5)},
    "ended": {"pro_until": iso(-1)},
    "free": {"$unset": True},
    "paid": {"pro_until": iso(30), "pro_source": "play"},
}[state]
if sets.get("$unset"):
    db.users.update_one({"id": j["id"]}, {"$unset": {"pro_until": "", "pro_source": ""}})
elif sets:
    db.users.update_one({"id": j["id"]}, {"$set": sets})
print(j["access_token"])
