"""FinLearn Pro: subscription status, Google Play purchase verification, and the free/paid line.

Free: the first FREE_CONCEPTS lessons of every course, daily quests, idea of the day, revision of what was learned.
Pro: everything else (all lessons, practice trading, My money, missions, boss battles, calculators).
Purchases happen in the Play Store app; the server never trusts the phone, it asks Google (Play Developer API).
"""
import base64
import hmac
import json
import os
import time
from datetime import datetime, timedelta, timezone
from typing import Optional

import httpx
import jwt
from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel

FREE_CONCEPTS = 2
PRO_FREEZE_MAX = 5  # Pro members can hold more streak freezes (free accounts: 2)
TRIAL_DAYS = int(os.environ.get("TRIAL_DAYS", "7"))  # every new account gets this many days of Pro, no card needed
PRODUCT_ID = "finlearn_pro"
PLANS = [
    {"id": "yearly", "base_plan": "yearly", "label": "Yearly", "price": 399, "per": "year", "was": 588, "per_month": 33, "save_pct": 32,
     "badge": "BEST VALUE", "note": "Just ₹33 a month"},
    {"id": "monthly", "base_plan": "monthly", "label": "Monthly", "price": 49, "per": "month", "note": "Cancel any time"},
]
ACTIVE_STATES = {"SUBSCRIPTION_STATE_ACTIVE", "SUBSCRIPTION_STATE_IN_GRACE_PERIOD", "SUBSCRIPTION_STATE_CANCELED"}
_token_cache = {"value": None, "exp": 0.0}


def now() -> datetime:
    return datetime.now(timezone.utc)


def parse_ts(s: Optional[str]) -> Optional[datetime]:
    if not s:
        return None
    try:
        d = datetime.fromisoformat(s.replace("Z", "+00:00"))
        return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def trial_fields() -> dict:
    """Pro fields for a brand-new account: a free reverse trial (people use the good stuff first, then decide)."""
    if TRIAL_DAYS <= 0:
        return {}
    return {"pro_until": (now() + timedelta(days=TRIAL_DAYS)).isoformat(), "pro_source": "trial"}


def trial_state(user: dict) -> dict:
    until = parse_ts(user.get("pro_until"))
    if user.get("pro_source") != "trial" or not until:
        return {"active": False, "ended": False, "ends_at": None, "days_left": 0}
    left = until - now()
    active = left.total_seconds() > 0
    return {"active": active, "ended": not active, "ends_at": until.isoformat(), "days_left": max(0, -(-int(left.total_seconds()) // 86400))}


def is_pro(user: dict) -> bool:
    if user.get("role") == "admin":
        return True
    until = parse_ts(user.get("pro_until"))
    return bool(until and until > now())


def make_require_pro(get_current_user):
    async def require_pro(user: dict = Depends(get_current_user)) -> dict:
        if not is_pro(user):
            raise HTTPException(status_code=402, detail="pro_required")
        return user
    return require_pro


async def free_concept_ids(db, course_id: str) -> set:
    """The first FREE_CONCEPTS concepts of a course, in reading order (chapter, module, concept)."""
    chapters = await db.chapters.find({"course_id": course_id}, {"_id": 0, "id": 1, "order": 1}).sort("order", 1).to_list(200)
    out = []
    for ch in chapters:
        mods = await db.modules.find({"chapter_id": ch["id"]}, {"_id": 0, "id": 1, "order": 1}).sort("order", 1).to_list(200)
        for m in mods:
            cons = await db.concepts.find({"module_id": m["id"]}, {"_id": 0, "id": 1, "order": 1}).sort("order", 1).to_list(500)
            out += [c["id"] for c in cons]
            if len(out) >= FREE_CONCEPTS:
                return set(out[:FREE_CONCEPTS])
    return set(out)


async def concept_course_id(db, concept: dict) -> Optional[str]:
    m = await db.modules.find_one({"id": concept.get("module_id")}, {"_id": 0, "chapter_id": 1})
    ch = m and await db.chapters.find_one({"id": m["chapter_id"]}, {"_id": 0, "course_id": 1})
    return ch["course_id"] if ch else None


async def concept_locked(db, user: dict, concept: dict) -> bool:
    if is_pro(user):
        return False
    cid = await concept_course_id(db, concept)
    return not cid or concept["id"] not in await free_concept_ids(db, cid)


# ---------- Google Play Developer API ----------
def service_account() -> Optional[dict]:
    raw = os.environ.get("GOOGLE_PLAY_SERVICE_ACCOUNT_JSON", "").strip()
    if not raw:
        return None
    try:
        sa = json.loads(raw)
        return sa if sa.get("client_email") and sa.get("private_key") else None
    except ValueError:
        return None


def package_name() -> str:
    return os.environ.get("PLAY_PACKAGE_NAME", "com.finlearn.app")


def api_base() -> str:
    return os.environ.get("PLAY_API_BASE", "https://androidpublisher.googleapis.com/androidpublisher/v3")


async def _access_token(client: httpx.AsyncClient, sa: dict) -> str:
    if _token_cache["value"] and _token_cache["exp"] > time.time() + 60:
        return _token_cache["value"]
    uri = sa.get("token_uri") or "https://oauth2.googleapis.com/token"
    t = int(time.time())
    assertion = jwt.encode(
        {"iss": sa["client_email"], "scope": "https://www.googleapis.com/auth/androidpublisher", "aud": uri, "iat": t, "exp": t + 3000},
        sa["private_key"], algorithm="RS256")
    r = await client.post(uri, data={"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": assertion})
    r.raise_for_status()
    body = r.json()
    _token_cache.update(value=body["access_token"], exp=time.time() + int(body.get("expires_in", 3000)))
    return body["access_token"]


async def play_lookup(token: str, product_id: str, ack: bool = True) -> dict:
    """Ask Google about a purchase token. Returns {active, expiry(datetime|None), state, order_id}. Raises on API failure."""
    sa = service_account()
    if not sa:
        raise RuntimeError("not_configured")
    async with httpx.AsyncClient(timeout=15) as client:
        at = await _access_token(client, sa)
        h = {"Authorization": f"Bearer {at}"}
        r = await client.get(f"{api_base()}/applications/{package_name()}/purchases/subscriptionsv2/tokens/{token}", headers=h)
        if r.status_code in (400, 404, 410):
            return {"active": False, "expiry": None, "state": "INVALID", "order_id": None}
        r.raise_for_status()
        d = r.json()
        items = d.get("lineItems") or []
        item = next((i for i in items if i.get("productId") == product_id), None)
        expiry = parse_ts(item.get("expiryTime")) if item else None
        state = d.get("subscriptionState", "")
        active = bool(item) and state in ACTIVE_STATES and bool(expiry and expiry > now())
        if active and ack and d.get("acknowledgementState") == "ACKNOWLEDGEMENT_STATE_PENDING":
            await client.post(f"{api_base()}/applications/{package_name()}/purchases/subscriptions/{product_id}/tokens/{token}:acknowledge",
                              headers=h, json={})
        return {"active": active, "expiry": expiry, "state": state, "order_id": d.get("latestOrderId")}


class VerifyIn(BaseModel):
    product_id: str = PRODUCT_ID
    purchase_token: str


class GrantIn(BaseModel):
    email: str
    days: int = 30


def make_router(db, get_current_user):
    r = APIRouter(prefix="/subscription", tags=["subscription"])
    admin_router = APIRouter(prefix="/admin/pro", tags=["subscription"])

    async def refresh_from_play(user: dict) -> dict:
        """Renewals and cancellations: re-ask Google when the stored period is about to end (or just ended)."""
        until, tok = parse_ts(user.get("pro_until")), user.get("pro_token")
        if tok and service_account() and until and until < now() + timedelta(days=1):
            try:
                res = await play_lookup(tok, user.get("pro_product") or PRODUCT_ID, ack=False)
                new_until = res["expiry"].isoformat() if res["active"] else (until.isoformat())
                await db.users.update_one({"id": user["id"]}, {"$set": {"pro_until": new_until}})
                user = {**user, "pro_until": new_until}
            except Exception:
                pass  # keep the stored state; Google may just be unreachable
        return user

    @r.get("/status")
    async def status(user: dict = Depends(get_current_user)):
        user = await refresh_from_play(user)
        until = parse_ts(user.get("pro_until"))
        return {
            "pro": is_pro(user), "until": until.isoformat() if until else None, "admin": user.get("role") == "admin",
            "trial": trial_state(user), "free_concepts": FREE_CONCEPTS, "product_id": PRODUCT_ID, "plans": PLANS, "billing_ready": service_account() is not None,
        }

    @r.get("/usage")
    async def usage(user: dict = Depends(get_current_user)):
        """What the learner has done with the Pro tools, for the trial checklist and the 'what you will keep' reminder."""
        uid = user["id"]
        acct = await db.practice_accounts.find_one({"user_id": uid}, {"_id": 0, "trades": 1}) or {}
        return {
            "trades": len(acct.get("trades", [])),
            "spends": await db.money_entries.count_documents({"user_id": uid}),
            "goals": await db.money_goals.count_documents({"user_id": uid}),
            "missions": await db.mission_progress.count_documents({"user_id": uid}),
            "lessons": await db.user_progress.count_documents({"user_id": uid, "status": {"$in": ["completed", "mastered"]}}),
        }

    @r.post("/rtdn")
    async def rtdn(token: str = "", body: dict = Body(...)):
        """Google Play's real-time notifications (renewals, cancellations, refunds, chargebacks), delivered by a Pub/Sub push
        subscription pointed at /api/subscription/rtdn?token=<PLAY_RTDN_SECRET>. We re-ask Google about the purchase, so the
        message itself is never trusted, and a refunded or revoked subscription stops being Pro right away."""
        secret = os.environ.get("PLAY_RTDN_SECRET", "")
        if not secret or not hmac.compare_digest(token.encode(), secret.encode()):
            raise HTTPException(status_code=403, detail="Forbidden")
        try:
            data = json.loads(base64.b64decode(body["message"]["data"]))
        except Exception:
            raise HTTPException(status_code=400, detail="Bad message")
        if data.get("packageName") != package_name():
            return {"ok": True, "ignored": "other app"}
        note = data.get("subscriptionNotification")
        if not note or not note.get("purchaseToken"):
            return {"ok": True, "ignored": "not a subscription event"}  # test messages and one-time products
        tok = note["purchaseToken"]
        known = await db.subscriptions.find_one({"purchase_token": tok})
        if not known:
            return {"ok": True, "ignored": "purchase not linked to an account yet"}  # the app's own verify call links it
        try:
            res = await play_lookup(tok, note.get("subscriptionId") or PRODUCT_ID, ack=False)
        except Exception:
            raise HTTPException(status_code=503, detail="Could not reach Google Play")  # Pub/Sub will deliver it again
        until = res["expiry"].isoformat() if res["active"] and res["expiry"] else now().isoformat()
        await db.subscriptions.update_one({"purchase_token": tok}, {"$set": {"state": res["state"], "expiry": until, "updated_at": now().isoformat()}})
        # Only the account that currently owns this purchase changes, and a manual grant is never touched.
        await db.users.update_one({"id": known["user_id"], "pro_token": tok}, {"$set": {"pro_until": until}})
        return {"ok": True, "active": res["active"]}

    @r.post("/verify")
    async def verify(body: VerifyIn, user: dict = Depends(get_current_user)):
        if body.product_id != PRODUCT_ID:
            raise HTTPException(status_code=400, detail="Unknown product")
        if not service_account():
            raise HTTPException(status_code=503, detail="Purchases are not switched on yet")
        owner = await db.subscriptions.find_one({"purchase_token": body.purchase_token})
        if owner and owner["user_id"] != user["id"]:
            raise HTTPException(status_code=409, detail="This purchase belongs to another account")
        try:
            res = await play_lookup(body.purchase_token, body.product_id)
        except Exception:
            raise HTTPException(status_code=502, detail="Could not reach Google Play. Please try again.")
        if not res["active"]:
            raise HTTPException(status_code=402, detail="That purchase is not active")
        await db.subscriptions.update_one(
            {"purchase_token": body.purchase_token},
            {"$set": {"user_id": user["id"], "product_id": body.product_id, "state": res["state"], "order_id": res["order_id"],
                      "expiry": res["expiry"].isoformat(), "updated_at": now().isoformat()}}, upsert=True)
        await db.users.update_one({"id": user["id"]}, {"$set": {
            "pro_until": res["expiry"].isoformat(), "pro_token": body.purchase_token, "pro_product": body.product_id,
            "pro_source": "play"}})
        return {"pro": True, "until": res["expiry"].isoformat()}

    @admin_router.post("/grant")
    async def grant(body: GrantIn, user: dict = Depends(get_current_user)):
        """Admin gives Pro for N days (testers, reviewers, promo). days=0 removes a manual grant."""
        if user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Admin only")
        days = max(0, min(body.days, 3650))
        target = await db.users.find_one({"email": body.email.strip().lower()})
        if not target:
            raise HTTPException(status_code=404, detail="No user with that email")
        until = (now() + timedelta(days=days)).isoformat() if days else None
        await db.users.update_one({"id": target["id"]}, {"$set": {"pro_until": until, "pro_source": "grant"}})
        return {"email": target["email"], "pro_until": until}

    outer = APIRouter()
    outer.include_router(r)
    outer.include_router(admin_router)
    return outer
