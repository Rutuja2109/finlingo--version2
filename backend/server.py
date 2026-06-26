"""FinLingo backend — Auth + Courses + Progress + Gamification + Leaderboard."""
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

import os
import uuid
import asyncio
import logging
import shutil
import bcrypt
import jwt
from datetime import datetime, timezone, timedelta
from pathlib import Path as P
from typing import List, Optional, Any, Dict

from fastapi import FastAPI, APIRouter, HTTPException, Depends, Request, Response, UploadFile, File, Form, BackgroundTasks, status
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr, Field
import httpx

from seed_data import seed_courses
from pdf_ingest import extract_chapters
from llm_gen import generate_chapter_lessons

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


class GoogleSessionIn(BaseModel):
    session_id: str


class ForgotPasswordIn(BaseModel):
    email: EmailStr


class ResetPasswordIn(BaseModel):
    token: str = Field(min_length=10)
    new_password: str = Field(min_length=6)


class GenerateCourseIn(BaseModel):
    name: str = Field(min_length=1, max_length=60)
    title: str = Field(min_length=1, max_length=120)
    certification: str = Field(min_length=1, max_length=40)
    description: str = Field(default="", max_length=400)
    color: str = Field(default="#FF6B35")
    icon: str = Field(default="BookOpen")
    max_chapters: int = Field(default=3, ge=1, le=20)  # cap for cost


class RevisionGradeIn(BaseModel):
    concept_id: str
    quality: int = Field(ge=0, le=3)  # 0=again, 1=hard, 2=good, 3=easy


class BossBattleSubmitIn(BaseModel):
    chapter_id: str
    answers: Dict[str, int]  # {question_id: chosen_option_index}


# Where uploaded PDFs are stored (ephemeral container disk)
UPLOAD_DIR = P("/app/data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


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


@api.post("/auth/forgot-password")
async def forgot_password(payload: ForgotPasswordIn):
    """Generate a 1-hour reset token. In dev-mode (no email service wired),
    we return the token + path so the frontend can build a same-origin reset link.
    Always returns 200 to avoid revealing whether an email exists.
    """
    email = payload.email.lower()
    user = await db.users.find_one({"email": email})
    if not user:
        return {"ok": True, "reset_token": None, "reset_path": None,
                "message": "If this email exists, a reset link has been generated."}

    token = str(uuid.uuid4()).replace("-", "") + str(uuid.uuid4()).replace("-", "")
    expires_at = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    await db.password_resets.insert_one({
        "id": str(uuid.uuid4()), "user_id": user["id"],
        "token": token, "expires_at": expires_at, "used": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
    })
    return {
        "ok": True,
        "reset_token": token,
        "reset_path": f"/reset-password?token={token}",
        "message": "Reset link generated. In production this would be emailed to you.",
    }


@api.post("/auth/reset-password")
async def reset_password(payload: ResetPasswordIn, response: Response):
    doc = await db.password_resets.find_one({"token": payload.token, "used": False}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=400, detail="Invalid or already-used token")
    expires_at = doc["expires_at"]
    if isinstance(expires_at, str):
        expires_at = datetime.fromisoformat(expires_at)
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    if expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Reset link has expired")

    user = await db.users.find_one({"id": doc["user_id"]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.users.update_one(
        {"id": user["id"]}, {"$set": {"password_hash": hash_password(payload.new_password)}}
    )
    await db.password_resets.update_one(
        {"token": payload.token}, {"$set": {"used": True,
                                            "used_at": datetime.now(timezone.utc).isoformat()}}
    )
    # Auto-login on successful reset
    access = create_access_token(user["id"], user["email"])
    refresh = create_refresh_token(user["id"])
    set_auth_cookies(response, access, refresh)
    return {
        "id": user["id"], "email": user["email"], "name": user["name"],
        "role": user.get("role", "user"),
        "avatar_color": user.get("avatar_color", "#FF6B35"),
        "access_token": access,
    }


@api.post("/auth/google/session")
async def google_session(payload: GoogleSessionIn, response: Response):
    """Exchange Emergent OAuth session_id for our JWT.

    Flow:
    1. Call Emergent's /session-data with the session_id to get verified user info.
    2. Find or create the user in our users collection (linked by email).
    3. Issue our own JWT cookies + Bearer token so the rest of the app works unchanged.
    """
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            r = await client.get(
                "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data",
                headers={"X-Session-ID": payload.session_id},
            )
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Auth provider unreachable: {e}")
    if r.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid Google session")
    info = r.json()
    email = (info.get("email") or "").lower()
    if not email:
        raise HTTPException(status_code=400, detail="Google account missing email")
    name = info.get("name") or email.split("@")[0]
    picture = info.get("picture")

    user = await db.users.find_one({"email": email})
    if user:
        # Link the Google identity to existing user if not already
        update = {}
        if not user.get("google_linked"):
            update["google_linked"] = True
        if picture and user.get("picture") != picture:
            update["picture"] = picture
        if update:
            await db.users.update_one({"id": user["id"]}, {"$set": update})
        user_id = user["id"]
        user_doc = user
    else:
        user_id = str(uuid.uuid4())
        user_doc = {
            "id": user_id, "email": email, "name": name, "role": "user",
            # No password — google-only account; can be set later via "change password" if needed.
            "password_hash": "", "google_linked": True, "picture": picture,
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
        "id": user_id, "email": email, "name": user_doc.get("name", name),
        "role": user_doc.get("role", "user"),
        "avatar_color": user_doc.get("avatar_color", "#FF6B35"),
        "picture": user_doc.get("picture"),
        "access_token": access,
    }


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
    # Schedule first review 1 day out if newly completed
    set_doc = {
        "user_id": user["id"], "concept_id": payload.concept_id,
        "status": status_, "mastery": max(mastery, (existing or {}).get("mastery", 0)),
        "last_completed_at": now,
    }
    if status_ in ("completed", "mastered") and not (existing and existing.get("next_review_at")):
        set_doc["next_review_at"] = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
        set_doc["review_interval_days"] = 1
    await db.user_progress.update_one(
        {"user_id": user["id"], "concept_id": payload.concept_id},
        {"$set": set_doc, "$inc": {"attempts": 1, "xp_earned": xp_earned}},
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


# ---------- ADMIN: PDF -> COURSE ----------
async def _require_admin(user: dict = Depends(get_current_user)) -> dict:
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return user


@api.post("/admin/pdf/upload")
async def upload_pdf(file: UploadFile = File(...), admin: dict = Depends(_require_admin)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only .pdf files accepted")
    pdf_id = str(uuid.uuid4())
    dest = UPLOAD_DIR / f"{pdf_id}.pdf"
    with dest.open("wb") as f:
        shutil.copyfileobj(file.file, f)
    size = dest.stat().st_size
    doc = {
        "id": pdf_id, "original_name": file.filename, "path": str(dest),
        "size_bytes": size, "uploaded_by": admin["id"],
        "uploaded_at": datetime.now(timezone.utc).isoformat(),
    }
    await db.pdf_uploads.insert_one({**doc})
    return {"pdf_id": pdf_id, "filename": file.filename, "size_bytes": size}


@api.get("/admin/pdf/list")
async def list_pdfs(admin: dict = Depends(_require_admin)):
    rows = await db.pdf_uploads.find({}, {"_id": 0}).sort("uploaded_at", -1).to_list(100)
    return rows


@api.get("/admin/jobs")
async def list_jobs(admin: dict = Depends(_require_admin)):
    rows = await db.generation_jobs.find({}, {"_id": 0}).sort("created_at", -1).to_list(50)
    return rows


@api.get("/admin/jobs/{job_id}")
async def get_job(job_id: str, admin: dict = Depends(_require_admin)):
    row = await db.generation_jobs.find_one({"id": job_id}, {"_id": 0})
    if not row:
        raise HTTPException(status_code=404, detail="Job not found")
    return row


async def _run_generation_job(job_id: str, pdf_path: str, course_meta: dict, max_chapters: int):
    """Background task: parse PDF -> per chapter LLM call -> persist course."""
    try:
        await db.generation_jobs.update_one(
            {"id": job_id}, {"$set": {"status": "extracting", "progress": 5}}
        )

        # 1. Extract chapters from PDF (synchronous, CPU-bound, run in thread)
        chapters = await asyncio.to_thread(extract_chapters, pdf_path, None, 12000, max_chapters)
        chapters = chapters[:max_chapters]
        if not chapters:
            raise RuntimeError("No chapters detected in PDF — try a different document or pattern.")

        await db.generation_jobs.update_one(
            {"id": job_id},
            {"$set": {"status": "generating", "progress": 15,
                      "chapters_detected": len(chapters)}}
        )

        # 2. Create course shell
        course_id = str(uuid.uuid4())
        slug_base = course_meta["name"].lower().replace(" ", "-")
        slug = f"{slug_base}-{course_id[:6]}"
        course_doc = {
            "id": course_id, "slug": slug,
            "name": course_meta["name"], "title": course_meta["title"],
            "certification": course_meta["certification"],
            "description": course_meta["description"],
            "color": course_meta["color"], "icon": course_meta["icon"],
            "order": 99, "ai_generated": True,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        await db.courses.insert_one(course_doc)

        # 3. For each chapter, call LLM and persist
        for idx, ch in enumerate(chapters):
            pct = 15 + int(80 * (idx / max(1, len(chapters))))
            await db.generation_jobs.update_one(
                {"id": job_id},
                {"$set": {"progress": pct, "current_chapter": ch.title}}
            )
            try:
                data = await generate_chapter_lessons(
                    certification=course_meta["certification"],
                    chapter_title=ch.title,
                    chapter_text=ch.body_text,
                )
            except Exception as e:
                logger.warning("LLM failed for ch %s: %s — skipping", ch.title, e)
                continue

            chapter_id = str(uuid.uuid4())
            await db.chapters.insert_one({
                "id": chapter_id, "course_id": course_id,
                "order": idx + 1, "title": ch.title,
                "description": f"Chapter {ch.chapter_no} of {course_meta['name']}",
                "source_pages": [ch.start_page, ch.end_page],
            })

            for m_i, m in enumerate(data.get("modules", [])):
                module_id = str(uuid.uuid4())
                await db.modules.insert_one({
                    "id": module_id, "chapter_id": chapter_id,
                    "order": m_i + 1, "title": m.get("title", f"Module {m_i+1}"),
                })
                for c_i, c in enumerate(m.get("concepts", [])):
                    concept_id = str(uuid.uuid4())
                    await db.concepts.insert_one({
                        "id": concept_id, "module_id": module_id,
                        "order": c_i + 1,
                        "title": c.get("title", "Untitled concept"),
                        "learning_objective": c.get("learning_objective", ""),
                        "simple_explanation": c.get("simple_explanation", ""),
                        "key_takeaways": c.get("key_takeaways", []),
                        "common_mistakes": c.get("common_mistakes", []),
                        "xp_reward": int(c.get("xp_reward", 15)),
                    })
                    for l_i, lesson in enumerate(c.get("lessons", [])):
                        await db.lessons.insert_one({
                            "id": str(uuid.uuid4()), "concept_id": concept_id,
                            "order": l_i + 1, "type": lesson.get("type", "intro"),
                            "content": lesson.get("content", {}),
                        })

        await db.generation_jobs.update_one(
            {"id": job_id},
            {"$set": {"status": "completed", "progress": 100, "course_id": course_id,
                      "completed_at": datetime.now(timezone.utc).isoformat()}}
        )
    except Exception as e:
        logger.exception("Generation job %s failed", job_id)
        await db.generation_jobs.update_one(
            {"id": job_id},
            {"$set": {"status": "failed", "error": str(e),
                      "failed_at": datetime.now(timezone.utc).isoformat()}}
        )


@api.post("/admin/pdf/{pdf_id}/generate")
async def generate_course_from_pdf(pdf_id: str, payload: GenerateCourseIn,
                                   bg: BackgroundTasks,
                                   admin: dict = Depends(_require_admin)):
    pdf = await db.pdf_uploads.find_one({"id": pdf_id}, {"_id": 0})
    if not pdf:
        raise HTTPException(status_code=404, detail="PDF not found")

    job_id = str(uuid.uuid4())
    await db.generation_jobs.insert_one({
        "id": job_id, "pdf_id": pdf_id, "status": "queued", "progress": 0,
        "course_meta": payload.model_dump(),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "created_by": admin["id"],
    })
    bg.add_task(_run_generation_job, job_id, pdf["path"],
                payload.model_dump(), payload.max_chapters)
    return {"job_id": job_id, "status": "queued"}


# ---------- REVISION (Spaced Repetition, SM-2 lite) ----------
def _next_review_interval(prev_interval_days: int, quality: int) -> int:
    """SM-2-lite: quality 0=again, 1=hard, 2=good, 3=easy."""
    if quality == 0:
        return 1
    if quality == 1:
        return max(1, prev_interval_days)
    if quality == 2:
        return max(2, int(prev_interval_days * 2.0)) if prev_interval_days else 2
    # easy
    return max(4, int(prev_interval_days * 2.7)) if prev_interval_days else 4


@api.get("/revisions/due")
async def revisions_due(user: dict = Depends(get_current_user)):
    """Return concepts that are due for review (mastered/completed + next_review_at <= now)."""
    now_iso = datetime.now(timezone.utc).isoformat()
    rows = await db.user_progress.find(
        {"user_id": user["id"],
         "status": {"$in": ["completed", "mastered"]},
         "$or": [{"next_review_at": {"$lte": now_iso}}, {"next_review_at": {"$exists": False}}]},
        {"_id": 0},
    ).limit(20).to_list(20)
    concept_ids = [r["concept_id"] for r in rows]
    concepts = await db.concepts.find({"id": {"$in": concept_ids}}, {"_id": 0}).to_list(50)
    by_id = {c["id"]: c for c in concepts}
    return [{"progress": r, "concept": by_id.get(r["concept_id"])} for r in rows if by_id.get(r["concept_id"])]


@api.post("/revisions/grade")
async def revisions_grade(payload: RevisionGradeIn, user: dict = Depends(get_current_user)):
    prog = await db.user_progress.find_one(
        {"user_id": user["id"], "concept_id": payload.concept_id}, {"_id": 0}
    )
    if not prog:
        raise HTTPException(status_code=404, detail="No progress for concept")
    prev = int(prog.get("review_interval_days", 0))
    nxt = _next_review_interval(prev, payload.quality)
    next_at = (datetime.now(timezone.utc) + timedelta(days=nxt)).isoformat()
    xp_bonus = [0, 2, 5, 8][payload.quality]
    await db.user_progress.update_one(
        {"user_id": user["id"], "concept_id": payload.concept_id},
        {"$set": {"review_interval_days": nxt, "next_review_at": next_at,
                  "last_reviewed_at": datetime.now(timezone.utc).isoformat()}},
        upsert=True,
    )
    if xp_bonus:
        await db.user_stats.update_one(
            {"user_id": user["id"]}, {"$inc": {"total_xp": xp_bonus, "coins": xp_bonus // 2}}
        )
    return {"next_review_in_days": nxt, "xp_bonus": xp_bonus}


# ---------- BOSS BATTLE ----------
@api.get("/boss-battles/{chapter_id}")
async def boss_battle(chapter_id: str, user: dict = Depends(get_current_user)):
    """Return chapter info + a mixed quiz of MCQs sampled from that chapter's concepts."""
    chapter = await db.chapters.find_one({"id": chapter_id}, {"_id": 0})
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    modules = await db.modules.find({"chapter_id": chapter_id}, {"_id": 0}).to_list(50)
    module_ids = [m["id"] for m in modules]
    concepts = await db.concepts.find({"module_id": {"$in": module_ids}}, {"_id": 0}).to_list(200)
    concept_ids = [c["id"] for c in concepts]

    # Require all concepts completed
    prog = await db.user_progress.find(
        {"user_id": user["id"], "concept_id": {"$in": concept_ids}}, {"_id": 0}
    ).to_list(500)
    done_ids = {p["concept_id"] for p in prog if p.get("status") in ("completed", "mastered")}
    unlocked = len(done_ids) >= max(1, len(concept_ids))

    # Pull MCQs from lessons of those concepts
    lessons = await db.lessons.find(
        {"concept_id": {"$in": concept_ids}, "type": "mcq"}, {"_id": 0}
    ).to_list(500)
    import random as _r
    questions = _r.sample(lessons, min(8, len(lessons))) if lessons else []
    return {
        "chapter": chapter, "unlocked": unlocked,
        "concepts_total": len(concept_ids), "concepts_done": len(done_ids),
        "questions": [{"id": q["id"], "content": q["content"]} for q in questions],
    }


@api.post("/boss-battles/submit")
async def boss_battle_submit(payload: BossBattleSubmitIn, user: dict = Depends(get_current_user)):
    # Server-side scoring: look up each question id and grade against stored correct answer
    if not payload.answers:
        raise HTTPException(status_code=400, detail="No answers submitted")
    lesson_docs = await db.lessons.find(
        {"id": {"$in": list(payload.answers.keys())}, "type": "mcq"}, {"_id": 0}
    ).to_list(200)
    if not lesson_docs:
        raise HTTPException(status_code=400, detail="No valid questions found")
    correct = 0
    for l in lesson_docs:
        truth = l.get("content", {}).get("correct")
        if truth is not None and payload.answers.get(l["id"]) == truth:
            correct += 1
    total = len(lesson_docs)
    score = int(round(100 * correct / max(1, total)))
    passed = score >= 70
    xp_award = 50 if passed else 10
    coins_award = 15 if passed else 3
    # Stats update
    stats = await db.user_stats.find_one({"user_id": user["id"]}, {"_id": 0}) or {}
    new_xp = stats.get("total_xp", 0) + xp_award
    new_coins = stats.get("coins", 0) + coins_award
    new_level = 1 + new_xp // 100
    achievements = stats.get("achievements", [])
    unlocked = []
    if passed and "boss_slayer" not in achievements:
        achievements.append("boss_slayer")
        unlocked.append({"code": "boss_slayer", "title": "Boss Slayer", "icon": "Crown"})
    await db.user_stats.update_one(
        {"user_id": user["id"]},
        {"$set": {"total_xp": new_xp, "level": new_level, "coins": new_coins,
                  "achievements": achievements}},
        upsert=True,
    )
    # Record battle
    await db.boss_battles.insert_one({
        "id": str(uuid.uuid4()), "user_id": user["id"], "chapter_id": payload.chapter_id,
        "score": score, "passed": passed,
        "completed_at": datetime.now(timezone.utc).isoformat(),
    })
    return {
        "score": score, "passed": passed, "xp_earned": xp_award,
        "coins_earned": coins_award, "new_xp": new_xp, "new_level": new_level,
        "new_achievements": unlocked,
        "correct_count": correct, "total": total,
    }


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
