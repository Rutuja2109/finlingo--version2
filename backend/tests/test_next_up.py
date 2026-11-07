"""Home 'Continue' card endpoint (/progress/next). Starts its own backend on port 8006 (needs local MongoDB with the courses seeded)."""
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


env = {**os.environ}
env.pop("SEED_DEMO", None)
srv = subprocess.Popen([sys.executable, "-m", "uvicorn", "server:app", "--port", "8006"], cwd=os.path.join(HERE, ".."), env=env,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
load_dotenv(os.path.join(HERE, "..", ".env"))
db = MongoClient(os.environ["MONGO_URL"])[os.environ["DB_NAME"]]
U = "http://127.0.0.1:8006/api"
EM = "next.up.test@example.com"
try:
    for _ in range(60):
        try:
            if httpx.get(f"{U}/health", timeout=2).status_code == 200:
                break
        except Exception:
            time.sleep(1)
    db.users.delete_many({"email": EM})
    c = httpx.Client(timeout=30)
    j = c.post(f"{U}/auth/register", json={"email": EM, "password": "Passw0rd!x", "name": "Next Up"}).json()
    H = {"Authorization": f"Bearer {j['access_token']}"}
    uid = j["id"]
    nxt = lambda: c.get(f"{U}/progress/next", headers=H).json()

    ok("needs login", c.get(f"{U}/progress/next").status_code == 401)
    n = nxt()
    ok("a new learner starts at the first course, first lesson", n["course"]["slug"] == "money-basics" and n["concept"]["title"] == "Where does your money go?" and n["done"] == 0 and n["enrolled"] is False)
    ok("total counts every lesson of the course", n["total"] >= 6)
    ok("the trial lets a new learner open it", n["locked"] is False)

    c.post(f"{U}/enrollments", headers=H, json={"course_id": n["course"]["id"]})
    ok("enrolled flag follows enrollment", nxt()["enrolled"] is True)

    c.post(f"{U}/progress/complete-concept", headers=H, json={"concept_id": n["concept"]["id"], "score": 100})
    n2 = nxt()
    ok("after finishing lesson 1 the next one is lesson 2", n2["concept"]["title"] == "The emergency fund" and n2["done"] == 1)
    c.post(f"{U}/progress/complete-concept", headers=H, json={"concept_id": n2["concept"]["id"], "score": 100})
    n3 = nxt()
    ok("lesson 3 follows lesson 2", n3["concept"]["title"] == "Credit cards and EMIs" and n3["done"] == 2)

    db.users.update_one({"id": uid}, {"$unset": {"pro_until": "", "pro_source": ""}})
    ok("for a free learner the third lesson is marked locked", nxt()["locked"] is True)
    db.users.update_one({"id": uid}, {"$set": {"pro_until": "2099-01-01T00:00:00+00:00", "pro_source": "grant"}})
    ok("and open again for Pro", nxt()["locked"] is False)

    # Chapter order: after the first chapter comes chapter 2, not a random concept.
    c.post(f"{U}/progress/complete-concept", headers=H, json={"concept_id": n3["concept"]["id"], "score": 100})
    n4 = nxt()
    ok("the next lesson after chapter 1 is the first of chapter 2", n4["concept"]["title"] == "Plan your month" and n4["done"] == 3)

    # A finished lesson stays finished, even if it is replayed badly.
    before = nxt()["done"]
    c.post(f"{U}/progress/complete-concept", headers=H, json={"concept_id": n["concept"]["id"], "score": 0})
    ok("replaying a finished lesson with a bad score does not un-finish it", nxt()["done"] == before)
    first_prog = db.user_progress.find_one({"user_id": uid, "concept_id": n["concept"]["id"]})
    ok("its status is still completed or mastered", first_prog["status"] in ("completed", "mastered"))
    c.post(f"{U}/progress/complete-concept", headers=H, json={"concept_id": n["concept"]["id"], "score": 65})
    ok("a lesson finished with 100 stays mastered after a 65 replay", db.user_progress.find_one({"user_id": uid, "concept_id": n["concept"]["id"]})["status"] == "mastered")

    # The course used most recently wins.
    stock = db.courses.find_one({"slug": "stock-market-basics"})
    chs = [x["id"] for x in db.chapters.find({"course_id": stock["id"]})]
    mods = [x["id"] for x in db.modules.find({"chapter_id": {"$in": chs}})]
    first = db.concepts.find_one({"module_id": {"$in": mods}, "title": "What is a share?"})
    c.post(f"{U}/progress/complete-concept", headers=H, json={"concept_id": first["id"], "score": 100})
    n5 = nxt()
    ok("practising another course moves 'continue' to that course", n5["course"]["slug"] == "stock-market-basics" and n5["concept"]["title"] == "SIP and index funds")
finally:
    srv.terminate()
    u = db.users.find_one({"email": EM})
    if u:
        for coll in ("user_progress", "user_stats", "user_enrollments", "daily_quests"):
            db[coll].delete_many({"user_id": u["id"]})
        db.users.delete_one({"id": u["id"]})

print("\nFAILED: " + ", ".join(fails) if fails else "\nALL OK")
sys.exit(1 if fails else 0)
