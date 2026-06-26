"""FinLingo backend — Auth + Courses + Progress + Gamification + Leaderboard."""
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

import os
import uuid
import logging
import bcrypt
import jwt
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Any, Dict

from fastapi import FastAPI, APIRouter, HTTPException, Depends, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr, Field

from seed_data import seed_courses

# ---------- Mongo ----------
mongo_url = os.environ["MONGO_URL"]
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ["DB_NAME"]]

# ---------- Auth utilities ----------
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MIN = 60 * 24  # 1 day, simpler for learning app
REFRESH_TOKEN_EXPIRE_DAYS = 30


def jwt_secret() -> str:
    return os.environ["JWT_SECRET"]


def hash_password(pw: str) -> str:
    return bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(pw: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(pw.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


def create_access_token(user_id: str, email: str) -> str:
    payload = {
        "sub": user_id, "email": email, "type": "access",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN),
    }
    return jwt.encode(payload, jwt_secret(), algorithm=JWT_ALGORITHM)


def create_refresh_token(user_id: str) -> str:
    payload = {
        "sub": user_id, "type": "refresh",
        "exp": datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    }
    return jwt.encode(payload, jwt_secret(), algorithm=JWT_ALGORITHM)


def set_auth_cookies(response: Response, access: str, refresh: str):
    response.set_cookie("access_token", access, httponly=True, secure=True,
                        samesite="none", max_age=ACCESS_TOKEN_EXPIRE_MIN * 60, path="/")
    response.set_cookie("refresh_token", refresh, httponly=True, secure=True,
                        samesite="none", max_age=REFRESH_TOKEN_EXPIRE_DAYS * 86400, path="/")


def clear_auth_cookies(response: Response):
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")


async def get_current_user(request: Request) -> dict:
    token = request.cookies.get("access_token")
    if not token:
        auth = request.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            token = auth[7:]
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, jwt_secret(), algorithms=[JWT_ALGORITHM])
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user = await db.users.find_one({"id": payload["sub"]})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        user.pop("_id", None)
        user.pop("password_hash", None)
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ---------- Models ----------
class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    name: str = Field(min_length=1, max_length=50)


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class ProgressUpdate(BaseModel):
    concept_id: str
    correct: bool
    xp_delta: Optional[int] = None


class CompleteConceptIn(BaseModel):
    concept_id: str
    score: int = Field(ge=0, le=100)  # percent correct
    duration_sec: int = 0


class EnrollIn(BaseModel):
    course_id: str


# ---------- App ----------
app = FastAPI(title="FinLingo API")
api = APIRouter(prefix="/api")


@app.on_event("startup")
async def on_startup():
    await db.users.create_index("email", unique=True)
    await db.user_stats.create_index("user_id", unique=True)
    await db.user_progress.create_index([("user_id", 1), ("concept_id", 1)], unique=True)
    await db.user_enrollments.create_index([("user_id", 1), ("course_id", 1)], unique=True)
    await db.courses.create_index("slug", unique=True)
    await seed_admin()
    await seed_courses(db)


async def seed_admin():
    admin_email = os.environ.get("ADMIN_EMAIL", "admin@finlingo.com").lower()
    admin_pw = os.environ.get("ADMIN_PASSWORD", "Admin@123")
    demo_email = os.environ.get("DEMO_EMAIL", "demo@finlingo.com").lower()
    demo_pw = os.environ.get("DEMO_PASSWORD", "Demo@123")

    for email, pw, name, role in [
        (admin_email, admin_pw, "Admin", "admin"),
        (demo_email, demo_pw, "Demo Learner", "user"),
    ]:
        existing = await db.users.find_one({"email": email})
        if not existing:
            user_id = str(uuid.uuid4())
            await db.users.insert_one({
                "id": user_id, "email": email, "name": name, "role": role,
                "password_hash": hash_password(pw),
                "created_at": datetime.now(timezone.utc).isoformat(),
                "avatar_color": "#FF6B35" if role == "admin" else "#10B981",
            })
            await db.user_stats.insert_one({
                "user_id": user_id, "total_xp": 0, "level": 1, "coins": 50,
                "streak_days": 0, "last_active_date": None, "achievements": [],
                "concepts_mastered": 0, "lessons_completed": 0,
            })
        else:
            if not verify_password(pw, existing.get("password_hash", "")):
                await db.users.update_one(
                    {"email": email},
                    {"$set": {"password_hash": hash_password(pw)}},
                )


# ---------- AUTH ----------
@api.post("/auth/register")
async def register(payload: RegisterIn, response: Response):
    email = payload.email.lower()
    if await db.users.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    user_id = str(uuid.uuid4())
    user_doc = {
        "id": user_id, "email": email, "name": payload.name, "role": "user",
        "password_hash": hash_password(payload.password),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "avatar_color": _pick_color(email),
    }
    await db.users.insert_one(user_doc)
    await db.user_stats.insert_one({
        "user_id": user_id, "total_xp": 0, "level": 1, "coins": 50,
        "streak_days": 0, "last_active_date": None, "achievements": [],
        "concepts_mastered": 0, "lessons_completed": 0,
    })
    access = create_access_token(user_id, email)
    refresh = create_refresh_token(user_id)
    set_auth_cookies(response, access, refresh)
    return {
        "id": user_id, "email": email, "name": payload.name, "role": "user",
        "avatar_color": user_doc["avatar_color"],
        "access_token": access,  # also returned for clients that can't use cookies
    }


@api.post("/auth/login")
async def login(payload: LoginIn, response: Response):
    email = payload.email.lower()
    user = await db.users.find_one({"email": email})
    if not user or not verify_password(payload.password, user.get("password_hash", "")):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access = create_access_token(user["id"], email)
    refresh = create_refresh_token(user["id"])
    set_auth_cookies(response, access, refresh)
    return {
        "id": user["id"], "email": email, "name": user["name"], "role": user.get("role", "user"),
        "avatar_color": user.get("avatar_color", "#FF6B35"),
        "access_token": access,
    }


@api.post("/auth/logout")
async def logout(response: Response):
    clear_auth_cookies(response)
    return {"ok": True}


@api.get("/auth/me")
async def me(user: dict = Depends(get_current_user)):
    return user


@api.post("/auth/refresh")
async def refresh_token(request: Request, response: Response):
    rt = request.cookies.get("refresh_token")
    if not rt:
        raise HTTPException(status_code=401, detail="No refresh token")
    try:
        payload = jwt.decode(rt, jwt_secret(), algorithms=[JWT_ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user = await db.users.find_one({"id": payload["sub"]})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        new_access = create_access_token(user["id"], user["email"])
        response.set_cookie("access_token", new_access, httponly=True, secure=True,
                            samesite="none", max_age=ACCESS_TOKEN_EXPIRE_MIN * 60, path="/")
        return {"ok": True}
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


def _pick_color(seed: str) -> str:
    palette = ["#FF6B35", "#10B981", "#2563EB", "#EC4899", "#F59E0B", "#8B5CF6", "#06B6D4"]
    return palette[hash(seed) % len(palette)]


# ---------- COURSES ----------
def _clean(doc):
    if doc:
        doc.pop("_id", None)
    return doc


@api.get("/courses")
async def list_courses():
    cursor = db.courses.find({}, {"_id": 0}).sort("order", 1)
    return await cursor.to_list(length=200)


@api.get("/courses/{course_id}/full")
async def course_full(course_id: str, user: dict = Depends(get_current_user)):
    course = await db.courses.find_one({"id": course_id}, {"_id": 0})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    chapters = await db.chapters.find({"course_id": course_id}, {"_id": 0}).sort("order", 1).to_list(100)
    chapter_ids = [c["id"] for c in chapters]
    modules = await db.modules.find({"chapter_id": {"$in": chapter_ids}}, {"_id": 0}).sort("order", 1).to_list(500)
    module_ids = [m["id"] for m in modules]
    concepts = await db.concepts.find({"module_id": {"$in": module_ids}}, {"_id": 0}).sort("order", 1).to_list(2000)
    concept_ids = [c["id"] for c in concepts]

    # progress map for this user
    progress_docs = await db.user_progress.find(
        {"user_id": user["id"], "concept_id": {"$in": concept_ids}}, {"_id": 0}
    ).to_list(5000)
    progress_map = {p["concept_id"]: p for p in progress_docs}

    # attach progress + unlock logic
    for i, concept in enumerate(concepts):
        prog = progress_map.get(concept["id"])
        concept["progress"] = prog or {"status": "locked", "mastery": 0, "attempts": 0}

    # unlock: first concept in module always active if not completed; later concepts unlock when previous completed
    by_module: Dict[str, List[dict]] = {}
    for c in concepts:
        by_module.setdefault(c["module_id"], []).append(c)
    for mid, cs in by_module.items():
        cs.sort(key=lambda x: x.get("order", 0))
        prev_completed = True
        for c in cs:
            status_ = c["progress"]["status"]
            if status_ in ("completed", "mastered"):
                prev_completed = True
                continue
            if prev_completed:
                c["progress"]["status"] = "active"
                prev_completed = False
            else:
                c["progress"]["status"] = "locked"

    # nest
    for m in modules:
        m["concepts"] = [c for c in concepts if c["module_id"] == m["id"]]
    for ch in chapters:
        ch["modules"] = [m for m in modules if m["chapter_id"] == ch["id"]]
    course["chapters"] = chapters
    return course


@api.get("/concepts/{concept_id}")
async def get_concept(concept_id: str, user: dict = Depends(get_current_user)):
    concept = await db.concepts.find_one({"id": concept_id}, {"_id": 0})
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")
    lessons = await db.lessons.find({"concept_id": concept_id}, {"_id": 0}).sort("order", 1).to_list(50)
    concept["lessons"] = lessons
    prog = await db.user_progress.find_one(
        {"user_id": user["id"], "concept_id": concept_id}, {"_id": 0}
    )
    concept["progress"] = prog or {"status": "active", "mastery": 0, "attempts": 0}
    return concept


# ---------- PROGRESS & GAMIFICATION ----------
@api.post("/progress/complete-concept")
async def complete_concept(payload: CompleteConceptIn, user: dict = Depends(get_current_user)):
    concept = await db.concepts.find_one({"id": payload.concept_id}, {"_id": 0})
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")

    base_xp = int(concept.get("xp_reward", 15))
    # XP scales with score; +50% bonus on perfect
    xp_earned = int(base_xp * (payload.score / 100.0))
    if payload.score == 100:
        xp_earned = int(base_xp * 1.5)
    coins_earned = max(2, xp_earned // 5)
    mastery = payload.score
    status_ = "mastered" if payload.score >= 90 else "completed" if payload.score >= 60 else "active"

    # Idempotency: if user already mastered/completed this concept, do NOT re-award XP.
    # They get the practice attempt logged but no new XP/coins/level changes.
    existing = await db.user_progress.find_one(
        {"user_id": user["id"], "concept_id": payload.concept_id}, {"_id": 0}
    )
    already_rewarded = existing is not None and existing.get("status") in ("completed", "mastered")
    if already_rewarded:
        xp_earned = 0
        coins_earned = 0

    now = datetime.now(timezone.utc).isoformat()
    await db.user_progress.update_one(
        {"user_id": user["id"], "concept_id": payload.concept_id},
        {"$set": {
            "user_id": user["id"], "concept_id": payload.concept_id,
            "status": status_, "mastery": max(mastery, (existing or {}).get("mastery", 0)),
            "last_completed_at": now,
        }, "$inc": {"attempts": 1, "xp_earned": xp_earned}},
        upsert=True,
    )

    # update user stats + streak
    today = datetime.now(timezone.utc).date().isoformat()
    stats = await db.user_stats.find_one({"user_id": user["id"]}, {"_id": 0}) or {}
    last_date = stats.get("last_active_date")
    streak = stats.get("streak_days", 0)
    if last_date != today:
        if last_date:
            try:
                last = datetime.fromisoformat(last_date).date()
                today_d = datetime.now(timezone.utc).date()
                delta = (today_d - last).days
                streak = streak + 1 if delta == 1 else 1
            except Exception:
                streak = 1
        else:
            streak = 1

    new_xp = stats.get("total_xp", 0) + xp_earned
    new_level = 1 + new_xp // 100  # every 100 xp = next level
    new_coins = stats.get("coins", 0) + coins_earned
    # Only count mastery the first time
    first_time_mastered = (status_ == "mastered") and not already_rewarded
    concepts_mastered = stats.get("concepts_mastered", 0) + (1 if first_time_mastered else 0)
    lessons_completed = stats.get("lessons_completed", 0) + 1

    # achievements
    achievements = stats.get("achievements", [])
    new_unlocks = []

    def unlock(code, title, icon):
        if code not in achievements:
            achievements.append(code)
            new_unlocks.append({"code": code, "title": title, "icon": icon})

    if lessons_completed >= 1:
        unlock("first_step", "First Step", "Footprints")
    if streak >= 3:
        unlock("streak_3", "3-Day Streak", "Flame")
    if streak >= 7:
        unlock("streak_7", "Week Warrior", "Flame")
    if new_level >= 5:
        unlock("level_5", "Rising Scholar", "GraduationCap")
    if concepts_mastered >= 5:
        unlock("master_5", "Mastery x5", "Trophy")
    if payload.score == 100:
        unlock("perfect", "Perfect Score", "Star")

    await db.user_stats.update_one(
        {"user_id": user["id"]},
        {"$set": {
            "total_xp": new_xp, "level": new_level, "coins": new_coins,
            "streak_days": streak, "last_active_date": today,
            "concepts_mastered": concepts_mastered, "lessons_completed": lessons_completed,
            "achievements": achievements,
        }},
        upsert=True,
    )

    return {
        "xp_earned": xp_earned, "coins_earned": coins_earned,
        "new_xp": new_xp, "new_level": new_level, "new_coins": new_coins,
        "streak_days": streak, "status": status_, "mastery": mastery,
        "new_achievements": new_unlocks,
    }


@api.get("/stats/me")
async def my_stats(user: dict = Depends(get_current_user)):
    s = await db.user_stats.find_one({"user_id": user["id"]}, {"_id": 0})
    if not s:
        s = {"user_id": user["id"], "total_xp": 0, "level": 1, "coins": 50,
             "streak_days": 0, "achievements": [], "concepts_mastered": 0,
             "lessons_completed": 0}
        await db.user_stats.insert_one(s)
        s.pop("_id", None)
    return s


@api.get("/progress/me")
async def my_progress(user: dict = Depends(get_current_user)):
    docs = await db.user_progress.find({"user_id": user["id"]}, {"_id": 0}).to_list(5000)
    return docs


# ---------- ENROLLMENT ----------
@api.post("/enrollments")
async def enroll(payload: EnrollIn, user: dict = Depends(get_current_user)):
    course = await db.courses.find_one({"id": payload.course_id})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    await db.user_enrollments.update_one(
        {"user_id": user["id"], "course_id": payload.course_id},
        {"$set": {"user_id": user["id"], "course_id": payload.course_id,
                  "enrolled_at": datetime.now(timezone.utc).isoformat()}},
        upsert=True,
    )
    return {"ok": True}


@api.get("/enrollments/me")
async def my_enrollments(user: dict = Depends(get_current_user)):
    rows = await db.user_enrollments.find({"user_id": user["id"]}, {"_id": 0}).to_list(100)
    course_ids = [r["course_id"] for r in rows]
    courses = await db.courses.find({"id": {"$in": course_ids}}, {"_id": 0}).to_list(100)
    return courses


# ---------- LEADERBOARD (REAL) ----------
@api.get("/leaderboard")
async def leaderboard(user: dict = Depends(get_current_user)):
    pipeline = [
        {"$sort": {"total_xp": -1}},
        {"$limit": 50},
        {"$lookup": {"from": "users", "localField": "user_id", "foreignField": "id", "as": "u"}},
        {"$unwind": "$u"},
        {"$project": {
            "_id": 0, "user_id": 1, "total_xp": 1, "level": 1, "streak_days": 1,
            "name": "$u.name", "avatar_color": "$u.avatar_color",
        }},
    ]
    rows = await db.user_stats.aggregate(pipeline).to_list(50)
    for i, r in enumerate(rows):
        r["rank"] = i + 1
        r["is_me"] = r["user_id"] == user["id"]
    return rows


# ---------- HEALTH ----------
@api.get("/")
async def root():
    return {"app": "FinLingo", "status": "ok"}


# ---------- MOUNT ----------
app.include_router(api)

# CORS — allow credentials with explicit origins
cors_origins_env = os.environ.get("CORS_ORIGINS", "*")
if cors_origins_env == "*":
    # Use regex to allow all origins while still permitting credentials
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=".*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[o.strip() for o in cors_origins_env.split(",") if o.strip()],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@app.on_event("shutdown")
async def on_shutdown():
    client.close()
