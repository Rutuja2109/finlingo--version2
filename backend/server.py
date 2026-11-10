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
from fastapi.responses import HTMLResponse
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr, Field
import httpx

from seed_data import seed_courses
from seed_finance import seed_finance_courses
from practice import make_router as make_practice_router
from money import make_router as make_money_router
from missions import make_router as make_missions_router
from explainers import make_router as make_explainer_router
import google_auth
import pro
import security
import mailer
from starlette.concurrency import run_in_threadpool
from quests import make_router as make_quests_router, bump as quest_bump
from text_repair import repair_collection
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
    password: str = Field(min_length=8)
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


class GoogleLoginIn(BaseModel):
    id_token: str


class ForgotPasswordIn(BaseModel):
    email: EmailStr


class ResetPasswordIn(BaseModel):
    token: str = Field(min_length=10)
    new_password: str = Field(min_length=8)


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
UPLOAD_DIR = P(os.environ.get("UPLOAD_DIR") or str(ROOT_DIR / "data" / "uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# ---------- App ----------
app = FastAPI(title="FinLingo API")
api = APIRouter(prefix="/api")


@app.on_event("startup")
async def on_startup():
    # Create indexes synchronously (fast)
    await db.users.create_index("email", unique=True)
    await db.user_stats.create_index("user_id", unique=True)
    await db.user_progress.create_index([("user_id", 1), ("concept_id", 1)], unique=True)
    await db.user_enrollments.create_index([("user_id", 1), ("course_id", 1)], unique=True)
    await db.courses.create_index("slug", unique=True)
    # Seed in background so healthcheck passes immediately
    asyncio.create_task(_seed_background())


async def _seed_background():
    try:
        await seed_admin()
        await seed_courses(db)
        await seed_finance_courses(db)
        # One-time-safe cleanup of garbled characters (e.g. 'â‰¤' for '≤') in stored lessons; ids never change.
        for coll in ("lessons", "concepts", "chapters", "modules", "courses"):
            n = await repair_collection(db, coll)
            if n:
                logging.getLogger(__name__).info(f"Repaired garbled text in {n} {coll} documents")
    except Exception as e:
        logging.getLogger(__name__).error(f"Seed error: {e}")


async def seed_admin():
    admin_email = os.environ.get("ADMIN_EMAIL", "admin@finlingo.com").lower()
    admin_pw = os.environ.get("ADMIN_PASSWORD", "Admin@123")
    demo_email = os.environ.get("DEMO_EMAIL", "demo@finlingo.com").lower()
    demo_pw = os.environ.get("DEMO_PASSWORD", "Demo@123")
    accounts = [(admin_email, admin_pw, "Admin", "admin")]
    if os.environ.get("SEED_DEMO") == "1":
        accounts.append((demo_email, demo_pw, "Demo Learner", "user"))  # local tests only
    else:
        # The public demo login is gone: remove the old well-known account.
        gone = await db.users.find_one({"email": demo_email, "role": "user"})
        if gone:
            await db.users.delete_one({"id": gone["id"]})
            await db.user_stats.delete_one({"user_id": gone["id"]})

    for email, pw, name, role in accounts:
        existing = await db.users.find_one({"email": email})
        if not existing:
            user_id = str(uuid.uuid4())
            await db.users.insert_one({
                "id": user_id, "email": email, "name": name, "role": role,
                "password_hash": hash_password(pw),
                "created_at": datetime.now(timezone.utc).isoformat(),
                "avatar_color": "#FF6B35" if role == "admin" else "#10B981",
                **({"pro_until": "2099-01-01T00:00:00+00:00"} if role == "user" else {}),  # local test account only
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
            if role == "admin" and existing.get("role") != "admin":  # ADMIN_EMAIL names an account that already exists
                await db.users.update_one({"email": email}, {"$set": {"role": "admin"}})


# ---------- AUTH ----------
@api.post("/auth/register")
async def register(payload: RegisterIn, request: Request, response: Response):
    security.enforce(request, "register", 30, 3600)  # generous: a hostel or mobile network shares one address
    email = payload.email.lower()
    if await db.users.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    user_id = str(uuid.uuid4())
    user_doc = {
        "id": user_id, "email": email, "name": payload.name, "role": "user",
        "password_hash": hash_password(payload.password),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "avatar_color": _pick_color(email),
        **pro.trial_fields(),
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
async def login(payload: LoginIn, request: Request, response: Response):
    email = payload.email.lower()
    ip_key, mail_key = f"login-ip:{security.client_ip(request)}", f"login-email:{email}"
    security.check_blocked(ip_key, 60, 600)     # a flood of failed logins from one address (generous: shared Wi-Fi)
    security.check_blocked(mail_key, 8, 600)    # too many failed logins for one account
    user = await db.users.find_one({"email": email})
    if not user or not verify_password(payload.password, user.get("password_hash", "")):
        security.record_failure(ip_key, 600)
        security.record_failure(mail_key, 600)
        raise HTTPException(status_code=401, detail="Invalid email or password")
    security.clear(mail_key)
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


class DeleteAccountIn(BaseModel):
    password: Optional[str] = None


@api.delete("/auth/account")
async def delete_account(payload: DeleteAccountIn, response: Response, user: dict = Depends(get_current_user)):
    if user.get("role") == "admin":
        raise HTTPException(status_code=403, detail="Admin accounts cannot be deleted here")
    stored = await db.users.find_one({"id": user["id"]})
    # Password accounts must confirm; Google-only accounts have no password hash
    if stored and stored.get("password_hash"):
        if not payload.password or not verify_password(payload.password, stored["password_hash"]):
            raise HTTPException(status_code=401, detail="Incorrect password")
    uid = user["id"]
    for coll in ("user_stats", "user_progress", "user_enrollments", "boss_battles", "password_resets",
                 "practice_accounts", "money_entries", "money_goals", "daily_quests", "mission_progress", "explainer_reads", "subscriptions"):
        await db[coll].delete_many({"user_id": uid})
    await db.users.delete_one({"id": uid})
    clear_auth_cookies(response)
    return {"ok": True}


require_pro = pro.make_require_pro(get_current_user)


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


def _public_base(request: Request) -> str:
    """The address people reach the server at, for links in emails. Set PUBLIC_BASE_URL to be sure."""
    env = os.environ.get("PUBLIC_BASE_URL", "").strip().rstrip("/")
    if env:
        return env
    base = str(request.base_url).rstrip("/")
    return base.replace("http://", "https://", 1) if os.environ.get("RENDER") else base


@api.post("/auth/forgot-password")
async def forgot_password(payload: ForgotPasswordIn, request: Request):
    """Sends a reset link by email. The link is NEVER returned to the caller (that would let anyone take over any account),
    except in local development (DEV_RESET_LINKS=1 from this same machine). Always answers the same way, so it does not
    reveal whether an email has an account."""
    security.enforce(request, "forgot-ip", 30, 3600)
    email = payload.email.lower()
    security.enforce(request, "forgot-email", 5, 3600, who=email)
    caller = request.client.host if request.client else ""
    dev = os.environ.get("DEV_RESET_LINKS") == "1" and caller in ("127.0.0.1", "::1", "localhost")
    if not mailer.configured() and not dev:
        return {"ok": True, "reset_token": None, "reset_path": None, "delivery": "unavailable",
                "message": "We cannot email reset links yet. If you signed up with Google, use Continue with Google."}
    sent = {"ok": True, "reset_token": None, "reset_path": None, "delivery": "email",
            "message": "If that email has a FinLearn account, we have sent a message with the next step. Check your inbox and spam folder."}

    user = await db.users.find_one({"email": email})
    if not user:
        return sent
    if not user.get("password_hash"):  # Google-only account: there is no password to reset
        await mailer.send_email(email, *mailer.google_only_email(user.get("name", "there")))
        return sent

    token = str(uuid.uuid4()).replace("-", "") + str(uuid.uuid4()).replace("-", "")
    await db.password_resets.update_many({"user_id": user["id"], "used": False}, {"$set": {"used": True}})  # older links stop working
    await db.password_resets.insert_one({
        "id": str(uuid.uuid4()), "user_id": user["id"],
        "token_hash": security.token_hash(token),  # only the hash is stored
        "expires_at": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(), "used": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
    })
    link = f"{_public_base(request)}/reset-password?token={token}"
    if mailer.configured():
        await mailer.send_email(email, *mailer.reset_email(user.get("name", "there"), link))
    if dev:
        return {**sent, "reset_token": token, "reset_path": f"/reset-password?token={token}", "delivery": "dev"}
    return sent


async def _consume_reset(token: str, new_password: str) -> dict:
    """Checks a reset link and sets the new password. Raises HTTPException with a plain message if the link is no good."""
    doc = await db.password_resets.find_one(
        {"$or": [{"token_hash": security.token_hash(token)}, {"token": token}], "used": False}, {"_id": 0})
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
    await db.users.update_one({"id": user["id"]}, {"$set": {"password_hash": hash_password(new_password)}})
    await db.password_resets.update_one({"id": doc["id"]}, {"$set": {"used": True, "used_at": datetime.now(timezone.utc).isoformat()}})
    if mailer.configured():
        await mailer.send_email(user["email"], *mailer.changed_email(user.get("name", "there")))
    return user


@api.post("/auth/reset-password")
async def reset_password(payload: ResetPasswordIn, request: Request, response: Response):
    security.enforce(request, "reset", 30, 3600)
    user = await _consume_reset(payload.token, payload.new_password)
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


@api.get("/auth/config")
async def auth_config():
    """What the app needs to show sign-in options. The client id is public by design."""
    ids = google_auth.client_ids()
    return {"google_client_id": ids[0] if ids else None, "support_email": os.environ.get("PRIVACY_EMAIL", "").strip() or None, "email_reset": mailer.configured()}


@api.post("/auth/google")
async def google_login(payload: GoogleLoginIn, request: Request, response: Response):
    security.enforce(request, "google", 120, 600)
    """Sign in (or sign up) with a Google ID token. We verify it ourselves, then issue our own login."""
    ids = google_auth.client_ids()
    if not ids:
        raise HTTPException(status_code=503, detail="Google sign-in is not set up yet")
    try:
        claims = await run_in_threadpool(google_auth.verify_id_token, payload.id_token, ids)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    email, sub = claims["email"], claims["sub"]
    name = (claims.get("name") or email.split("@")[0])[:80]
    picture = claims.get("picture")

    user = await db.users.find_one({"email": email})
    if user:
        if user.get("google_sub") and user["google_sub"] != sub:
            raise HTTPException(status_code=409, detail="This email is already linked to a different Google account")
        update = {"google_linked": True, "google_sub": sub}
        if picture and user.get("picture") != picture:
            update["picture"] = picture
        if not user.get("google_linked") and user.get("role") != "admin":
            # The email on a password account was never verified, but Google has now verified it for the real owner.
            # Drop the old password and any pending reset links, so nobody who registered this email first keeps access.
            update["password_hash"] = ""
            await db.password_resets.delete_many({"user_id": user["id"]})
        await db.users.update_one({"id": user["id"]}, {"$set": update})
        user_id, user_doc = user["id"], {**user, **update}
    else:
        user_id = str(uuid.uuid4())
        user_doc = {
            "id": user_id, "email": email, "name": name, "role": "user",
            "password_hash": "", "google_linked": True, "google_sub": sub, "picture": picture,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "avatar_color": _pick_color(email),
            **pro.trial_fields(),
        }
        await db.users.insert_one(dict(user_doc))
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
        "access_token": access, "new_account": not user,
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
    cursor = db.courses.find({"hidden": {"$ne": True}}, {"_id": 0}).sort("order", 1)
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
    free = None if pro.is_pro(user) else await pro.free_concept_ids(db, course_id)
    for c in concepts:
        c["locked"] = free is not None and c["id"] not in free
    course["chapters"] = chapters
    course["free_concepts"] = pro.FREE_CONCEPTS
    return course


@api.get("/concepts/{concept_id}")
async def get_concept(concept_id: str, user: dict = Depends(get_current_user)):
    concept = await db.concepts.find_one({"id": concept_id}, {"_id": 0})
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")
    if await pro.concept_locked(db, user, concept):
        raise HTTPException(status_code=402, detail="pro_required")
    lessons = await db.lessons.find({"concept_id": concept_id}, {"_id": 0}).sort("order", 1).to_list(50)
    concept["lessons"] = lessons
    prog = await db.user_progress.find_one(
        {"user_id": user["id"], "concept_id": concept_id}, {"_id": 0}
    )
    concept["progress"] = prog or {"status": "active", "mastery": 0, "attempts": 0}
    return concept


# ---------- PROGRESS & GAMIFICATION ----------
@api.post("/progress/complete-concept")
async def complete_concept(payload: CompleteConceptIn, request: Request, user: dict = Depends(get_current_user)):
    concept = await db.concepts.find_one({"id": payload.concept_id}, {"_id": 0})
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found")
    if await pro.concept_locked(db, user, concept):
        raise HTTPException(status_code=402, detail="pro_required")

    base_xp = int(concept.get("xp_reward", 15))
    # XP scales with score; +50% bonus on perfect
    xp_earned = int(base_xp * (payload.score / 100.0))
    if payload.score == 100:
        xp_earned = int(base_xp * 1.5)
    coins_earned = max(2, xp_earned // 5)
    mastery = payload.score
    status_ = "mastered" if payload.score >= 90 else "completed" if payload.score >= 60 else "active"

    existing = await db.user_progress.find_one(
        {"user_id": user["id"], "concept_id": payload.concept_id}, {"_id": 0}
    )
    already_rewarded = existing is not None and existing.get("status") in ("completed", "mastered")
    # A finished lesson stays finished: replaying it badly must never take the completion (and the unlocks after it) away.
    rank = {"active": 0, "completed": 1, "mastered": 2}
    if existing and rank.get(existing.get("status"), 0) > rank[status_]:
        status_ = existing["status"]
    if already_rewarded:
        # Give a small practice bonus so the screen never shows +0
        xp_earned = max(3, base_xp // 10)
        coins_earned = 1

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
    today_d = learner_today(request)
    today = today_d.isoformat()
    stats = await db.user_stats.find_one({"user_id": user["id"]}, {"_id": 0}) or {}
    last_date = stats.get("last_active_date")
    streak = stats.get("streak_days", 0)
    freezes = stats.get("streak_freezes", 0)
    if last_date != today:
        if last_date:
            try:
                last = datetime.fromisoformat(last_date).date()
                delta = (today_d - last).days
                if delta == 1:
                    streak += 1
                elif delta == 2 and freezes > 0:
                    # exactly one missed day: a streak freeze covers it
                    streak += 1
                    freezes -= 1
                else:
                    streak = 1
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
            "streak_days": streak, "last_active_date": today, "streak_freezes": freezes,
            "concepts_mastered": concepts_mastered, "lessons_completed": lessons_completed,
            "achievements": achievements,
            **_xp_today_fields(stats, xp_earned, today),
        }},
        upsert=True,
    )

    if payload.score >= 60:
        await quest_bump(db, user["id"], today, "lessons")
        if payload.score == 100:
            await quest_bump(db, user["id"], today, "perfect")

    return {
        "xp_earned": xp_earned, "coins_earned": coins_earned,
        "new_xp": new_xp, "new_level": new_level, "new_coins": new_coins,
        "streak_days": streak, "status": status_, "mastery": mastery,
        "new_achievements": new_unlocks,
    }


def learner_today(request: Request):
    """Today's date on the learner's own clock. The app sends X-TZ-Offset (minutes behind UTC, as JS reports it)."""
    try:
        offset = max(-840, min(840, int(request.headers.get("X-TZ-Offset", "0"))))
    except ValueError:
        offset = 0
    return (datetime.now(timezone.utc) - timedelta(minutes=offset)).date()


def _xp_today_fields(stats: dict, delta: int, today: Optional[str] = None) -> dict:
    """Fields that add `delta` XP to today's running total (resets each day on the learner's clock)."""
    today = today or datetime.now(timezone.utc).date().isoformat()
    base = stats.get("xp_today", 0) if stats.get("xp_today_date") == today else 0
    return {"xp_today": base + delta, "xp_today_date": today}


@api.get("/stats/me")
async def my_stats(request: Request, user: dict = Depends(get_current_user)):
    s = await db.user_stats.find_one({"user_id": user["id"]}, {"_id": 0})
    if not s:
        s = {"user_id": user["id"], "total_xp": 0, "level": 1, "coins": 50,
             "streak_days": 0, "achievements": [], "concepts_mastered": 0,
             "lessons_completed": 0}
        await db.user_stats.insert_one(s)
        s.pop("_id", None)
    today = learner_today(request).isoformat()
    s["xp_today"] = s.get("xp_today", 0) if s.get("xp_today_date") == today else 0
    s.pop("xp_today_date", None)
    s.setdefault("streak_freezes", 0)
    # A streak that was not continued in time is shown as broken (it is reset when the learner next studies).
    last = s.get("last_active_date")
    if last and s.get("streak_days", 0) > 0:
        try:
            gap = (learner_today(request) - datetime.fromisoformat(last).date()).days
            if gap >= 3 or (gap == 2 and s.get("streak_freezes", 0) == 0):
                s["streak_days"] = 0
                s["streak_broken"] = True
        except Exception:
            pass
    u = await db.users.find_one({"id": user["id"]}, {"daily_goal_minutes": 1}) or {}
    mins = u.get("daily_goal_minutes")
    s["daily_goal_minutes"] = mins
    s["daily_goal_xp"] = GOAL_XP.get(mins, GOAL_XP[5])
    return s


# Daily goal choices: minutes per day -> XP target (one lesson is about 5 minutes and earns 20 to 33 XP).
GOAL_XP = {5: 20, 10: 40, 15: 60}


class GoalIn(BaseModel):
    minutes: int


@api.put("/me/goal")
async def set_daily_goal(payload: GoalIn, user: dict = Depends(get_current_user)):
    if payload.minutes not in GOAL_XP:
        raise HTTPException(status_code=400, detail="Choose 5, 10 or 15 minutes a day")
    await db.users.update_one({"id": user["id"]}, {"$set": {"daily_goal_minutes": payload.minutes}})
    return {"daily_goal_minutes": payload.minutes, "daily_goal_xp": GOAL_XP[payload.minutes]}


STREAK_FREEZE_COST = 30
STREAK_FREEZE_MAX = 2


@api.post("/shop/streak-freeze")
async def buy_streak_freeze(user: dict = Depends(get_current_user)):
    """Spend coins on a streak freeze, which protects the streak from one missed day."""
    s = await db.user_stats.find_one({"user_id": user["id"]}, {"_id": 0}) or {}
    owned = s.get("streak_freezes", 0)
    cap = pro.PRO_FREEZE_MAX if pro.is_pro(user) else STREAK_FREEZE_MAX
    if owned >= cap:
        raise HTTPException(status_code=400, detail=f"You can hold at most {cap} streak freezes" + ("" if cap > STREAK_FREEZE_MAX else ". Pro members can hold more."))
    # Atomic: only deducts if the user still has enough coins and room for another freeze.
    res = await db.user_stats.update_one(
        {"user_id": user["id"], "coins": {"$gte": STREAK_FREEZE_COST},
         "streak_freezes": {"$lt": cap}} if owned else
        {"user_id": user["id"], "coins": {"$gte": STREAK_FREEZE_COST}},
        {"$inc": {"coins": -STREAK_FREEZE_COST, "streak_freezes": 1}},
    )
    if res.modified_count == 0:
        raise HTTPException(status_code=400, detail=f"You need {STREAK_FREEZE_COST} coins for a streak freeze")
    s = await db.user_stats.find_one({"user_id": user["id"]}, {"_id": 0})
    return {"coins": s["coins"], "streak_freezes": s["streak_freezes"]}


@api.get("/progress/me")
async def my_progress(user: dict = Depends(get_current_user)):
    docs = await db.user_progress.find({"user_id": user["id"]}, {"_id": 0}).to_list(5000)
    return docs


# ---------- NEXT UP (Home screen "Continue" card) ----------
async def _ordered_concepts(course_id: str) -> list:
    """The concepts of a course in reading order (chapter, module, concept)."""
    chapters = await db.chapters.find({"course_id": course_id}, {"_id": 0, "id": 1, "order": 1}).to_list(300)
    ch_order = {c["id"]: c.get("order", 0) for c in chapters}
    modules = await db.modules.find({"chapter_id": {"$in": list(ch_order)}}, {"_id": 0, "id": 1, "chapter_id": 1, "order": 1}).to_list(1000)
    mod_key = {m["id"]: (ch_order[m["chapter_id"]], m.get("order", 0)) for m in modules}
    concepts = await db.concepts.find({"module_id": {"$in": list(mod_key)}}, {"_id": 0, "id": 1, "title": 1, "module_id": 1, "order": 1}).to_list(3000)
    concepts.sort(key=lambda c: (*mod_key[c["module_id"]], c.get("order", 0)))
    return concepts


@api.get("/progress/next")
async def next_up(user: dict = Depends(get_current_user)):
    """The lesson to do next: the first unfinished concept of the course used most recently (or the first course)."""
    uid = user["id"]
    prog = await db.user_progress.find({"user_id": uid}, {"_id": 0}).to_list(5000)
    done_ids = {p["concept_id"] for p in prog if p.get("status") in ("completed", "mastered")}
    enrolled = {r["course_id"] for r in await db.user_enrollments.find({"user_id": uid}, {"_id": 0}).to_list(100)}
    courses = await db.courses.find({"hidden": {"$ne": True}}, {"_id": 0}).sort("order", 1).to_list(100)
    if not courses:
        return {"all_done": True}

    # Most recently practised course first, then the rest in course order.
    target = None
    recent = max((p for p in prog if p.get("last_completed_at")), key=lambda p: p["last_completed_at"], default=None)
    if recent:
        c = await db.concepts.find_one({"id": recent["concept_id"]}, {"_id": 0, "module_id": 1})
        m = c and await db.modules.find_one({"id": c["module_id"]}, {"_id": 0, "chapter_id": 1})
        ch = m and await db.chapters.find_one({"id": m["chapter_id"]}, {"_id": 0, "course_id": 1})
        target = ch["course_id"] if ch else None
    order = ([c for c in courses if c["id"] == target] + [c for c in courses if c["id"] != target]) if target else courses

    for course in order[:4]:
        concepts = await _ordered_concepts(course["id"])
        nxt = next((c for c in concepts if c["id"] not in done_ids), None)
        if nxt:
            return {
                "all_done": False,
                "course": {"id": course["id"], "name": course["name"], "color": course.get("color"), "slug": course.get("slug")},
                "concept": {"id": nxt["id"], "title": nxt["title"]},
                "done": sum(1 for c in concepts if c["id"] in done_ids), "total": len(concepts),
                "enrolled": course["id"] in enrolled,
                "locked": await pro.concept_locked(db, user, nxt),
            }
    return {"all_done": True}


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
            "name": "$u.name", "avatar_color": "$u.avatar_color", "role": "$u.role", "pro_until": "$u.pro_until",
        }},
    ]
    rows = await db.user_stats.aggregate(pipeline).to_list(50)
    for i, r in enumerate(rows):
        r["rank"] = i + 1
        r["is_me"] = r["user_id"] == user["id"]
        r["pro"] = pro.is_pro({"role": r.pop("role", None), "pro_until": r.pop("pro_until", None)})
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
async def revisions_grade(payload: RevisionGradeIn, request: Request, user: dict = Depends(get_current_user)):
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
        cur = await db.user_stats.find_one({"user_id": user["id"]}, {"_id": 0}) or {}
        await db.user_stats.update_one(
            {"user_id": user["id"]},
            {"$inc": {"total_xp": xp_bonus, "coins": xp_bonus // 2},
             "$set": _xp_today_fields(cur, xp_bonus, learner_today(request).isoformat())},
        )
    await quest_bump(db, user["id"], learner_today(request).isoformat(), "revisions")
    return {"next_review_in_days": nxt, "xp_bonus": xp_bonus}


# ---------- BOSS BATTLE ----------
@api.get("/boss-battles/{chapter_id}")
async def boss_battle(chapter_id: str, user: dict = Depends(require_pro)):
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
async def boss_battle_submit(payload: BossBattleSubmitIn, request: Request, user: dict = Depends(require_pro)):
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
                  "achievements": achievements, **_xp_today_fields(stats, xp_award, learner_today(request).isoformat())}},
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


@api.get("/health")
async def health():
    return {"status": "ok"}


@api.get("/health/deep")
async def health_deep():
    """For uptime monitors: checks that the database answers, not just that the web process is up."""
    try:
        await asyncio.wait_for(db.command("ping"), timeout=5)
    except Exception:
        raise HTTPException(status_code=503, detail="database unavailable")
    return {"status": "ok", "db": "ok"}


# ---------- MOUNT ----------
PRIVACY_UPDATED = "9 November 2026"


def _fill(text: str) -> str:
    import html
    operator = html.escape(os.environ.get("PRIVACY_OPERATOR", "").strip() or "[operator name not set yet]")
    email = html.escape(os.environ.get("PRIVACY_EMAIL", "").strip() or "[support email not set yet]")
    return text.replace("{{OPERATOR}}", operator).replace("{{EMAIL}}", email).replace("{{UPDATED}}", PRIVACY_UPDATED)


def _privacy_page() -> str:
    """Public privacy policy. Operator name and contact email come from environment variables."""
    return _fill((ROOT_DIR / "privacy.html").read_text(encoding="utf-8"))


@app.get("/privacy", response_class=HTMLResponse, include_in_schema=False)
async def privacy_policy():
    return HTMLResponse(_privacy_page())


@app.get("/terms", response_class=HTMLResponse, include_in_schema=False)
async def terms_page():
    return HTMLResponse(_fill((ROOT_DIR / "pages" / "terms.html").read_text(encoding="utf-8")))


@app.get("/delete-account", response_class=HTMLResponse, include_in_schema=False)
async def delete_account_page():
    return HTMLResponse(_fill((ROOT_DIR / "pages" / "delete_account.html").read_text(encoding="utf-8")))


def _reset_html(title: str, body: str, status_code: int = 200) -> HTMLResponse:
    text = (ROOT_DIR / "pages" / "reset.html").read_text(encoding="utf-8")
    return HTMLResponse(text.replace("{{TITLE}}", title).replace("{{BODY}}", body), status_code=status_code)


def _reset_form(token: str, error: str = "") -> HTMLResponse:
    import html
    err = f'<div class="err" role="alert">{html.escape(error)}</div>' if error else ""
    return _reset_html("Choose a new password", f'''<p>Type a new password for your FinLearn account. At least 8 characters.</p>{err}
<form method="post" action="/reset-password">
<input type="hidden" name="token" value="{html.escape(token)}">
<label for="p1">New password</label><input id="p1" name="password" type="password" minlength="8" required autocomplete="new-password">
<label for="p2">Type it again</label><input id="p2" name="password2" type="password" minlength="8" required autocomplete="new-password">
<button type="submit">Save new password</button></form>''')


@app.get("/reset-password", response_class=HTMLResponse, include_in_schema=False)
async def reset_page(token: str = ""):
    """The page an emailed reset link opens (in any browser, so it works whether or not the app is installed)."""
    if len(token) < 10:
        return _reset_html("This link is not valid", "<p>The reset link is incomplete. Please use the link from your email, or ask for a new one in the app.</p>", 400)
    return _reset_form(token)


@app.post("/reset-password", response_class=HTMLResponse, include_in_schema=False)
async def reset_page_submit(request: Request, token: str = Form(""), password: str = Form(""), password2: str = Form("")):
    try:
        security.enforce(request, "reset", 30, 3600)
    except HTTPException:
        return _reset_html("Please wait", "<p>Too many attempts. Please wait a few minutes and try again.</p>", 429)
    if len(password) < 8:
        return _reset_form(token, "Your password must be at least 8 characters.")
    if password != password2:
        return _reset_form(token, "The two passwords do not match.")
    try:
        await _consume_reset(token, password)
    except HTTPException as e:
        return _reset_html("This link did not work", f"<p>{'That link has expired.' if 'expired' in str(e.detail) else 'That link was already used or is not valid.'} Please ask for a new one in the app (Log in, then Forgot password).</p>", 400)
    return _reset_html("Password changed", '<div class="ok">Your password has been changed.</div><p>Open the FinLearn app and log in with your new password.</p>')


api.include_router(make_practice_router(db, require_pro, _xp_today_fields, learner_today, on_trade=lambda uid, day: quest_bump(db, uid, day, "trades")))
api.include_router(make_explainer_router(db, get_current_user, _xp_today_fields, learner_today, on_read=lambda uid, day: quest_bump(db, uid, day, "explainers")))
api.include_router(make_missions_router(db, require_pro, _xp_today_fields, learner_today))
api.include_router(make_money_router(db, require_pro, learner_today, on_entry=lambda uid, day: quest_bump(db, uid, day, "entries")))
api.include_router(pro.make_router(db, get_current_user))
api.include_router(make_quests_router(db, get_current_user, learner_today, pro.is_pro))
app.include_router(api)

# CORS — open for mobile app (Capacitor sends null origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    return security.add_security_headers(response, is_html=response.headers.get("content-type", "").startswith("text/html"))


# Error monitoring: only active when SENTRY_DSN is set (free plan at sentry.io); no personal data is sent.
if os.environ.get("SENTRY_DSN"):
    try:
        import sentry_sdk
        sentry_sdk.init(dsn=os.environ["SENTRY_DSN"], traces_sample_rate=0.05, send_default_pii=False,
                        environment=os.environ.get("SENTRY_ENV", "production"))
    except Exception as _e:  # monitoring must never stop the app from starting
        print(f"[sentry] not started: {type(_e).__name__}")


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@app.on_event("shutdown")
async def on_shutdown():
    client.close()
