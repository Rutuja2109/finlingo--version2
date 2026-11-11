"""Real-life missions: small actions in the learner's own money life, done outside the app.

Some missions can be checked from the learner's data in FinLearn ("auto"). The rest are on the honour system
("self"): the learner taps "I did it" and may leave a short note. Each mission pays out once.
FinLearn never asks learners to buy a product, and never sees their bank or UPI data.
"""
from datetime import date, datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

NOTE_MAX = 140

# theme labels shown in the app
THEMES = {"spend": "Know your spending", "save": "Build savings", "protect": "Protect yourself", "invest": "Start investing", "tax": "Taxes"}

MISSIONS = [
    # ---- know your spending
    {"id": "upi-history", "theme": "spend", "kind": "self", "xp": 20, "title": "Check your UPI history",
     "why": "Small UPI payments hide where your money really goes.",
     "steps": ["Open your UPI app and look at the last 7 days of payments.", "Find your three biggest spends.", "Ask yourself: need or want?"],
     "note_prompt": "What surprised you?"},
    {"id": "log-week", "theme": "spend", "kind": "auto", "check": "log5", "xp": 30, "title": "Log 5 spends in My money this week",
     "why": "What you write down, you notice.", "steps": ["Open My money.", "Add 5 expenses from the last 7 days."], "link": "/money"},
    {"id": "cancel-sub", "theme": "spend", "kind": "self", "xp": 20, "title": "Find one subscription you can cancel",
     "why": "Subscriptions renew quietly. One forgotten ₹199 a month is ₹2,388 a year.",
     "steps": ["Check your UPI autopay list and app store subscriptions.", "List what you still use.", "Cancel one you do not."],
     "note_prompt": "What did you cancel, or keep and why?"},
    {"id": "wants-pause", "theme": "spend", "kind": "self", "xp": 20, "title": "Try a 48-hour pause on a want",
     "why": "Waiting two days kills most impulse buys.",
     "steps": ["Pick something you want to buy that is not a need.", "Write it down and wait 48 hours.", "If you still want it, decide again with a clear head."],
     "note_prompt": "Did you still want it?"},
    # ---- build savings
    {"id": "auto-transfer", "theme": "save", "kind": "self", "xp": 30, "title": "Set up an automatic transfer to savings",
     "why": "Saving that happens by itself beats saving by willpower.",
     "steps": ["Pick a small amount, even ₹200.", "Set a standing instruction or auto-transfer to a savings account on the day money arrives.", "Do not touch it for a month."],
     "note_prompt": "How much did you set up?"},
    {"id": "goal-set", "theme": "save", "kind": "auto", "check": "goal", "xp": 20, "title": "Create a savings goal",
     "why": "A number and a date turn a wish into a plan.", "steps": ["Open My money.", "Add a goal, for example a phone or a trip, with a target and months."], "link": "/money"},
    {"id": "emergency-start", "theme": "save", "kind": "self", "xp": 30, "title": "Put your first ₹1,000 in an emergency fund",
     "why": "A small cushion turns a crisis into an inconvenience.",
     "steps": ["Open or choose a separate savings account.", "Move ₹1,000, or whatever you can, into it.", "Label it 'emergency only'."],
     "note_prompt": "Where did you keep it?"},
    {"id": "calc-run", "theme": "save", "kind": "self", "xp": 20, "title": "Work out your emergency-fund target",
     "why": "You cannot reach a target you have never calculated.",
     "steps": ["Add up your monthly needs (rent, food, travel, bills).", "Multiply by 3 for a first target, 6 for a full one.", "Use the emergency fund calculator if you like."],
     "link": "/calculators", "note_prompt": "What number did you get?"},
    # ---- protect yourself
    {"id": "two-step", "theme": "protect", "kind": "self", "xp": 25, "title": "Turn on two-step verification",
     "why": "Most account break-ins stop at a second lock.",
     "steps": ["Turn on two-step verification for your email.", "Turn on the app lock for your UPI and banking apps.", "Never share an OTP or PIN, with anyone."],
     "note_prompt": "Which accounts did you secure?"},
    {"id": "scam-check", "theme": "protect", "kind": "self", "xp": 20, "title": "Spot a scam message",
     "why": "Scams repeat the same tricks. Once you spot one, you spot them all.",
     "steps": ["Look through your SMS, email or WhatsApp for a message asking for an OTP, KYC update, or a 'prize' claim.", "Do not click. Block and report it.", "Remember the helpline: 1930."],
     "note_prompt": "What trick did it use?"},
    {"id": "health-cover", "theme": "protect", "kind": "self", "xp": 25, "title": "Find out if you have health insurance",
     "why": "Many young people discover the gap during their first hospital visit.",
     "steps": ["Ask your family if you are covered under a family policy.", "Check the sum insured and whether it ends when you start earning.", "Note your employer cover if you have a job."],
     "note_prompt": "Are you covered? Roughly how much?"},
    {"id": "policy-read", "theme": "protect", "kind": "self", "xp": 25, "title": "Read one insurance policy's fine print",
     "why": "Room-rent caps, co-pay and waiting periods hide in the details.",
     "steps": ["Open any health policy (yours or a family member's).", "Find the room-rent limit, waiting period and co-pay.", "Write them down."],
     "note_prompt": "What did you find?"},
    # ---- start investing
    {"id": "first-trade", "theme": "invest", "kind": "auto", "check": "trade", "xp": 20, "title": "Make a practice trade",
     "why": "Learn the buttons with pretend money first.", "steps": ["Open the Practice tab.", "Buy any asset."], "link": "/practice"},
    {"id": "spread", "theme": "invest", "kind": "auto", "check": "spread", "xp": 30, "title": "Hold 3 different practice assets at once",
     "why": "Spreading money across assets is how beginners avoid one bad day.", "steps": ["Open the Practice tab.", "Buy at least three different assets and keep them."], "link": "/practice"},
    {"id": "crash-hold", "theme": "invest", "kind": "auto", "check": "crash", "xp": 30, "title": "Sit through a practice crash",
     "why": "Staying calm in a fall is a skill you can train.", "steps": ["Open the Practice tab.", "Replay a market crash and watch it finish without panic selling."], "link": "/practice"},
    {"id": "sip-ready", "theme": "invest", "kind": "self", "xp": 30, "title": "Check if you are ready for a small SIP",
     "why": "Investing comes after safety. This mission is about readiness, not buying anything.",
     "steps": ["Do you have a starter emergency fund?", "Is this money you will not need for 5 years?", "If both are yes, look up how an index fund SIP works, and what it would cost per month.",
               "You do not have to start one. FinLearn does not recommend any fund or app. This is education, not advice."],
     "link": "/calculators", "note_prompt": "Ready, or not yet? Why?"},
    # ---- taxes
    {"id": "pan-aadhaar", "theme": "tax", "kind": "self", "xp": 20, "title": "Check your PAN and Aadhaar are linked",
     "why": "An unlinked PAN can stop your refunds and cause higher TDS.",
     "steps": ["Open the income tax e-filing website and use the 'Link Aadhaar status' option.", "Confirm the status says linked.", "If not, follow the steps on the official site. Never pay a third party to do it."],
     "note_prompt": "What was the status?"},
    {"id": "ais-look", "theme": "tax", "kind": "self", "xp": 25, "title": "Look at your Annual Information Statement",
     "why": "It shows what banks and employers have reported about you.",
     "steps": ["Log in to the income tax e-filing website (use the official site only).", "Open your AIS and look at salary, interest and any other items.", "Check they match what you know."],
     "note_prompt": "Anything surprising?"},
]
BY_ID = {m["id"]: m for m in MISSIONS}


def featured_mission(done_ids: set, week_key: str) -> Optional[str]:
    """One not-yet-done mission highlighted for the week; stable for the whole week."""
    if len(done_ids) >= len(MISSIONS):
        return None
    # Start from a position fixed by the week, then walk forward to the first mission not done.
    # Finishing some other mission therefore never changes the pick; only finishing the pick itself does.
    start = sum(ord(c) for c in week_key) % len(MISSIONS)
    for i in range(len(MISSIONS)):
        mid = MISSIONS[(start + i) % len(MISSIONS)]["id"]
        if mid not in done_ids:
            return mid
    return None


def week_key(d: date) -> str:
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


class CompleteIn(BaseModel):
    note: Optional[str] = None


def make_router(db, get_current_user, xp_today_fields, learner_today, any_user=None):
    r = APIRouter(prefix="/missions")

    async def check_auto(user_id: str, check: str, today: date) -> bool:
        if check == "log5":
            since = (today - timedelta(days=6)).isoformat()
            n = await db.money_entries.count_documents({"user_id": user_id, "kind": "expense", "date": {"$gte": since, "$lte": today.isoformat()}})
            return n >= 5
        if check == "goal":
            return await db.money_goals.count_documents({"user_id": user_id}) >= 1
        acct = await db.practice_accounts.find_one({"user_id": user_id}, {"_id": 0}) or {}
        if check == "trade":
            return bool(acct.get("trades"))
        if check == "spread":
            return len([p for p in (acct.get("positions") or {}).values() if p.get("units", 0) > 0]) >= 3
        if check == "crash":
            return bool(acct.get("last_result"))
        return False

    if any_user is not None:
        @r.get("/featured")
        async def featured(request: Request, user: dict = Depends(any_user)):
            """This week's mission for the Home card. Open to every account (free users see it as a taster)."""
            rows = await db.mission_progress.find({"user_id": user["id"]}, {"_id": 0, "mission_id": 1}).to_list(200)
            done = {x["mission_id"] for x in rows}
            feat = featured_mission(done, week_key(learner_today(request)))
            m = BY_ID.get(feat) if feat else None
            return {"mission": ({"id": m["id"], "title": m["title"], "why": m["why"], "xp": m["xp"], "coins": m["xp"] // 2,
                                 "steps": len(m["steps"])} if m else None),
                    "done_count": len(done), "total": len(MISSIONS)}

    @r.get("")
    async def listing(request: Request, user: dict = Depends(get_current_user)):
        today = learner_today(request)
        rows = await db.mission_progress.find({"user_id": user["id"]}, {"_id": 0}).to_list(200)
        done = {x["mission_id"]: x for x in rows}
        feat = featured_mission(set(done), week_key(today))
        out = []
        for m in MISSIONS:
            d = done.get(m["id"])
            out.append({**{k: m[k] for k in ("id", "theme", "kind", "xp", "title", "why", "steps")},
                        "link": m.get("link"), "note_prompt": m.get("note_prompt"), "coins": m["xp"] // 2,
                        "done": bool(d), "done_at": d["done_at"] if d else None, "note": d.get("note", "") if d else "",
                        "featured": m["id"] == feat})
        return {"themes": THEMES, "missions": out, "done_count": len(done), "total": len(MISSIONS)}

    @r.post("/{mission_id}/complete")
    async def complete(mission_id: str, body: CompleteIn, request: Request, user: dict = Depends(get_current_user)):
        m = BY_ID.get(mission_id)
        if not m:
            raise HTTPException(status_code=404, detail="Mission not found")
        today = learner_today(request)
        if m["kind"] == "auto" and not await check_auto(user["id"], m["check"], today):
            raise HTTPException(status_code=400, detail="Not done yet. Finish the steps, then check again.")
        note = (body.note or "").strip()[:NOTE_MAX] if m["kind"] == "self" else ""
        doc = {"user_id": user["id"], "mission_id": mission_id, "done_at": datetime.now(timezone.utc).isoformat(), "note": note}
        # unique per user and mission: a second tap (or a race) matches the existing document and pays nothing
        res = await db.mission_progress.update_one({"user_id": user["id"], "mission_id": mission_id}, {"$setOnInsert": doc}, upsert=True)
        if res.upserted_id is None:
            raise HTTPException(status_code=400, detail="You already completed this mission")
        xp, coins = m["xp"], m["xp"] // 2
        stats = await db.user_stats.find_one({"user_id": user["id"]}, {"_id": 0}) or {}
        new_xp = stats.get("total_xp", 0) + xp
        await db.user_stats.update_one(
            {"user_id": user["id"]},
            {"$set": {"total_xp": new_xp, "level": 1 + new_xp // 100, "coins": stats.get("coins", 0) + coins,
                      **xp_today_fields(stats, xp, today.isoformat())}},
            upsert=True,
        )
        return {"xp": xp, "coins": coins}

    return r
