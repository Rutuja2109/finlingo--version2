"""My money: a manual expense tracker with a 50/30/20 split, plus a savings-goal planner.
Entries are typed in by the user. Nothing reads SMS, bank accounts or UPI apps."""
import re
import uuid
from datetime import date, datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

# category -> (label, bucket). Buckets follow the 50/30/20 rule: needs / wants / savings.
CATEGORIES = {
    "rent": ("Rent and home", "needs"),
    "food": ("Groceries and food", "needs"),
    "transport": ("Transport", "needs"),
    "bills": ("Bills and recharge", "needs"),
    "education": ("Education", "needs"),
    "health": ("Health", "needs"),
    "emi": ("EMI and loan payments", "needs"),
    "eating_out": ("Eating out", "wants"),
    "shopping": ("Shopping", "wants"),
    "fun": ("Movies and fun", "wants"),
    "subs": ("Subscriptions", "wants"),
    "travel": ("Trips", "wants"),
    "sip": ("SIP and investing", "savings"),
    "savings": ("Savings", "savings"),
    "emergency": ("Emergency fund", "savings"),
}
TARGETS = {"needs": 50, "wants": 30, "savings": 20}
MAX_AMOUNT = 10_000_000
MONTH_RE = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")


class EntryIn(BaseModel):
    kind: str                      # "expense" | "income"
    amount: float
    category: Optional[str] = None  # required for expenses
    note: Optional[str] = None
    date: Optional[str] = None      # YYYY-MM-DD, defaults to the learner's today


class GoalIn(BaseModel):
    name: str
    target: float
    months: int                    # how many months from today
    saved: float = 0


class AddSavedIn(BaseModel):
    amount: float


def _clean_amount(v: float, what: str = "Amount") -> float:
    if v != v or v <= 0 or v > MAX_AMOUNT:
        raise HTTPException(status_code=400, detail=f"{what} must be more than 0 and at most ₹1,00,00,000")
    return round(float(v), 2)


def add_months(d: date, n: int) -> date:
    m = d.month - 1 + n
    y, mo = d.year + m // 12, m % 12 + 1
    day = min(d.day, [31, 29 if y % 4 == 0 and (y % 100 or y % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][mo - 1])
    return date(y, mo, day)


def months_between(today: date, deadline: date) -> int:
    """Whole months left until the deadline, at least 1 while the deadline is still ahead."""
    n = (deadline.year - today.year) * 12 + deadline.month - today.month
    if deadline.day < today.day:
        n -= 1
    return max(1, n) if deadline > today else 0


def goal_view(g: dict, today: date) -> dict:
    deadline = date.fromisoformat(g["deadline"])
    left = max(0.0, g["target"] - g["saved"])
    m = months_between(today, deadline)
    return {
        "id": g["id"], "name": g["name"], "target": g["target"], "saved": g["saved"], "deadline": g["deadline"],
        "left": left, "months_left": m,
        "monthly": (left / m) if (m and left) else 0.0,
        "done": left <= 0, "overdue": bool(left > 0 and m == 0),
        "pct": min(100, round(g["saved"] / g["target"] * 100)) if g["target"] else 0,
    }


def split_summary(entries: list) -> dict:
    income = sum(e["amount"] for e in entries if e["kind"] == "income")
    buckets = {"needs": 0.0, "wants": 0.0, "savings": 0.0}
    by_cat = {}
    for e in entries:
        if e["kind"] == "expense":
            buckets[e["bucket"]] += e["amount"]
            by_cat[e["category"]] = by_cat.get(e["category"], 0.0) + e["amount"]
    spent = buckets["needs"] + buckets["wants"]  # savings are money kept, not money spent
    base = income if income > 0 else sum(buckets.values())
    pct = {k: (round(v / base * 100, 1) if base else 0.0) for k, v in buckets.items()}
    return {
        "income": income, "buckets": buckets, "pct": pct, "targets": TARGETS, "spent": spent,
        "left": income - spent - buckets["savings"], "by_category": by_cat, "has_income": income > 0,
    }


def coach(s: dict) -> dict:
    """One short, plain-words observation about the month so far."""
    if not s["has_income"]:
        return {"mood": "happy", "tone": "", "title": "Add your income", "text": "Add what you earn or get as pocket money this month. Then I can show how your spending splits into needs, wants and savings."}
    p = s["pct"]
    if p["needs"] > 60:
        return {"mood": "nervous", "tone": "warn", "title": "Needs are taking a lot", "text": f"Needs are {p['needs']:.0f}% of your income. The usual target is 50%. Look for bills or food costs you can trim, or think about growing your income."}
    if p["wants"] > 35:
        return {"mood": "angry", "tone": "bad", "title": "Wants are running high", "text": f"Wants are {p['wants']:.0f}% of your income, the target is 30%. Small things like eating out and subscriptions add up quickly."}
    if p["savings"] < 10:
        return {"mood": "nervous", "tone": "warn", "title": "Pay yourself first", "text": f"You have saved {p['savings']:.0f}% so far, the target is 20%. Try moving a fixed amount to savings or an SIP the day money arrives."}
    if p["savings"] >= 20:
        return {"mood": "cheer", "tone": "good", "title": "Great month", "text": "You are saving 20% or more. That is how wealth builds, one steady month at a time."}
    return {"mood": "happy", "tone": "good", "title": "On track", "text": "Your split is close to 50/30/20. Keep logging and aim for 20% in savings."}


def make_router(db, get_current_user, learner_today, on_entry=None):
    r = APIRouter(prefix="/money")

    @r.get("/categories")
    async def categories(user: dict = Depends(get_current_user)):
        return [{"id": k, "label": v[0], "bucket": v[1]} for k, v in CATEGORIES.items()]

    @r.get("/summary")
    async def summary(request: Request, month: Optional[str] = None, user: dict = Depends(get_current_user)):
        today = learner_today(request)
        month = month or today.strftime("%Y-%m")
        if not MONTH_RE.match(month):
            raise HTTPException(status_code=400, detail="Month must look like 2026-11")
        entries = await db.money_entries.find(
            {"user_id": user["id"], "date": {"$regex": f"^{month}"}}, {"_id": 0, "user_id": 0}
        ).sort([("date", -1), ("created_at", -1)]).to_list(1000)
        s = split_summary(entries)
        return {"month": month, "today": today.isoformat(), "entries": entries, "summary": s, "coach": coach(s)}

    @r.post("/entries")
    async def add_entry(body: EntryIn, request: Request, user: dict = Depends(get_current_user)):
        if body.kind not in ("expense", "income"):
            raise HTTPException(status_code=400, detail="Kind must be expense or income")
        amount = _clean_amount(body.amount)
        d = body.date or learner_today(request).isoformat()
        try:
            date.fromisoformat(d)
        except ValueError:
            raise HTTPException(status_code=400, detail="Date must look like 2026-11-06")
        if body.kind == "expense":
            if body.category not in CATEGORIES:
                raise HTTPException(status_code=400, detail="Choose a category")
            category, bucket = body.category, CATEGORIES[body.category][1]
        else:
            category, bucket = "income", None
        if await db.money_entries.count_documents({"user_id": user["id"]}) >= 5000:
            raise HTTPException(status_code=400, detail="You have reached the limit of 5,000 entries. Delete some old ones.")
        doc = {
            "id": str(uuid.uuid4()), "user_id": user["id"], "kind": body.kind, "amount": amount, "category": category,
            "bucket": bucket, "note": (body.note or "").strip()[:80], "date": d,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        await db.money_entries.insert_one(dict(doc))
        if on_entry and d == learner_today(request).isoformat():  # backdated entries do not count for today's quest
            await on_entry(user["id"], d)
        doc.pop("_id", None); doc.pop("user_id", None)
        return doc

    @r.delete("/entries/{entry_id}")
    async def delete_entry(entry_id: str, user: dict = Depends(get_current_user)):
        res = await db.money_entries.delete_one({"id": entry_id, "user_id": user["id"]})
        if res.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Entry not found")
        return {"ok": True}

    # ---------------- goals
    @r.get("/goals")
    async def goals(request: Request, user: dict = Depends(get_current_user)):
        today = learner_today(request)
        rows = await db.money_goals.find({"user_id": user["id"]}, {"_id": 0}).sort("created_at", 1).to_list(100)
        return [goal_view(g, today) for g in rows]

    @r.post("/goals")
    async def add_goal(body: GoalIn, request: Request, user: dict = Depends(get_current_user)):
        name = body.name.strip()[:40]
        if not name:
            raise HTTPException(status_code=400, detail="Give your goal a name")
        target = _clean_amount(body.target, "Target")
        if not 1 <= body.months <= 120:
            raise HTTPException(status_code=400, detail="Choose between 1 and 120 months")
        saved = round(max(0.0, float(body.saved)), 2)
        if saved > target:
            raise HTTPException(status_code=400, detail="You cannot have saved more than the target")
        if await db.money_goals.count_documents({"user_id": user["id"]}) >= 20:
            raise HTTPException(status_code=400, detail="You can keep up to 20 goals")
        today = learner_today(request)
        g = {"id": str(uuid.uuid4()), "user_id": user["id"], "name": name, "target": target, "saved": saved,
             "deadline": add_months(today, body.months).isoformat(), "created_at": datetime.now(timezone.utc).isoformat()}
        await db.money_goals.insert_one(dict(g))
        return goal_view(g, today)

    @r.post("/goals/{goal_id}/add")
    async def goal_add(goal_id: str, body: AddSavedIn, request: Request, user: dict = Depends(get_current_user)):
        amount = _clean_amount(body.amount)
        g = await db.money_goals.find_one({"id": goal_id, "user_id": user["id"]}, {"_id": 0})
        if not g:
            raise HTTPException(status_code=404, detail="Goal not found")
        g["saved"] = round(min(g["target"], g["saved"] + amount), 2)
        await db.money_goals.update_one({"id": goal_id, "user_id": user["id"]}, {"$set": {"saved": g["saved"]}})
        return goal_view(g, learner_today(request))

    @r.delete("/goals/{goal_id}")
    async def goal_delete(goal_id: str, user: dict = Depends(get_current_user)):
        res = await db.money_goals.delete_one({"id": goal_id, "user_id": user["id"]})
        if res.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Goal not found")
        return {"ok": True}

    return r
