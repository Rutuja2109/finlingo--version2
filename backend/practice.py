"""Practice trading: virtual money, simulated prices. Nothing here uses real money or real market data.

Prices are a deterministic function of the clock (smooth waves plus small noise), so every request sees
the same market and charts need no stored history. A "market crash replay" temporarily swaps in a scripted
price path; when it ends the account keeps the post-crash price level so values never jump.
"""
import math
import time
from datetime import datetime, timezone
from typing import Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

START_CASH = 100000.0
MIN_BUY = 100.0
SCEN_TICKS = 50
SCEN_TICK_SECONDS = 0.6
TOUR_XP = 15
TOUR_COINS = 5

ASSETS = [
    {"id": "nifty", "name": "Nifty 50 Index Fund", "short": "NIFTY", "base": 250.0, "vol": 0.045, "color": "#2563EB", "icon": "BarChart3",
     "why": "An index fund holds 50 big companies, so one company falling does not sink it. That is why it moves gently."},
    {"id": "gold", "name": "Gold (per gram)", "short": "GOLD", "base": 7400.0, "vol": 0.03, "color": "#F59E0B", "icon": "Coins",
     "why": "Gold often holds up or rises when shares fall, because people look for a safe place to park money."},
    {"id": "btc", "name": "Bitcoin", "short": "BTC", "base": 6500000.0, "vol": 0.16, "color": "#FF9500", "icon": "Bitcoin",
     "why": "Bitcoin has no profits to anchor its price, only buyers and sellers, so it swings a lot."},
    {"id": "rkt", "name": "Rocket Tech (a made-up stock)", "short": "RKT", "base": 1280.0, "vol": 0.10, "color": "#EC4899", "icon": "Rocket",
     "why": "One company can jump or fall on a single news item. That is the risk of owning just one stock."},
]
BY_ID = {a["id"]: a for a in ASSETS}
for _i, _a in enumerate(ASSETS):
    _a["seed"] = 1000003 * (_i + 1)

# Smooth components: (period in seconds, weight of the asset's volatility)
WAVES = [(1800, 0.15), (5400, 0.20), (21600, 0.30), (112320, 0.40), (406080, 0.50), (950400, 0.60)]
CRASH_DRIFT = {"nifty": -0.014, "gold": 0.004, "btc": -0.034, "rkt": -0.03}

# Chart timeframes: (points, seconds between points)
TIMEFRAMES = {"1MIN": (60, 1), "5MIN": (60, 5), "15MIN": (90, 10), "30MIN": (90, 20), "1H": (120, 30), "1D": (144, 600), "1W": (168, 3600)}


def _u(seed: int, n: int) -> float:
    """Deterministic pseudo-random number in [0, 1) for integer inputs."""
    x = (int(n) * 2654435761 + int(seed) * 40503) & 0xFFFFFFFF
    x ^= x >> 15
    x = (x * 2246822519) & 0xFFFFFFFF
    x ^= x >> 13
    x = (x * 3266489917) & 0xFFFFFFFF
    x ^= x >> 16
    return x / 4294967296.0


def _noise(seed: int, n: int) -> float:
    """Roughly bell-shaped noise with standard deviation about 0.5."""
    return _u(seed, n) + _u(seed + 7, n) + _u(seed + 13, n) - 1.5


def normal_price(a: dict, t: float) -> float:
    x = 0.0
    for k, (period, w) in enumerate(WAVES):
        phase = _u(a["seed"] + k, 99) * 2 * math.pi
        x += a["vol"] * w * math.sin(2 * math.pi * t / period + phase)
    x += a["vol"] * 0.024 * _noise(a["seed"], int(t))
    return a["base"] * math.exp(x)


def scenario_mult(a: dict, salt: int, i: int) -> float:
    """Cumulative price multiplier of the crash replay at tick i (0..SCEN_TICKS-1)."""
    drift_down = CRASH_DRIFT[a["id"]]
    m = 0.0
    for j in range(i + 1):
        if j < 25:
            d = drift_down
        else:
            d = -0.002 if a["id"] == "gold" else abs(drift_down) * 0.55
        m += d + a["vol"] * 0.03 * _noise(a["seed"] + salt, j)
    return math.exp(m)


# ---------------------------------------------------------------- account logic

def new_account(user_id: str) -> dict:
    return {
        "user_id": user_id, "cash": START_CASH, "positions": {}, "trades": [], "offsets": {},
        "scenario": None, "last_result": None, "tour_done": False, "rev": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


OFFSET_DECAY_SECONDS = 7200.0


def offset_at(acct: dict, asset_id: str, t: float) -> float:
    """Price level left behind by a crash replay. It fades back to 1 over a couple of hours so repeated replays never drive prices to zero."""
    o = acct["offsets"].get(asset_id)
    if not o:
        return 1.0
    if not isinstance(o, dict):
        return float(o)
    return math.exp(math.log(o["r"]) * math.exp(-max(0.0, t - o["t"]) / OFFSET_DECAY_SECONDS))


def _scenario_tick(acct: dict, now: float) -> Optional[int]:
    sc = acct.get("scenario")
    if not sc:
        return None
    return int((now - sc["started_at"]) / SCEN_TICK_SECONDS)


def price_of(acct: dict, a: dict, now: float) -> float:
    tick = _scenario_tick(acct, now)
    if tick is not None and tick < SCEN_TICKS:
        sc = acct["scenario"]
        return sc["base"][a["id"]] * scenario_mult(a, sc["salt"], max(0, tick))
    return normal_price(a, now) * offset_at(acct, a["id"], now)


def total_value(acct: dict, now: float) -> float:
    t = acct["cash"]
    for aid, p in acct["positions"].items():
        t += p["units"] * price_of(acct, BY_ID[aid], now)
    return t


def settle_scenario(acct: dict, now: float) -> bool:
    """If the crash replay has run its course, keep its end prices and record the result. True if state changed."""
    tick = _scenario_tick(acct, now)
    if tick is None or tick < SCEN_TICKS:
        return False
    sc = acct["scenario"]
    final = {a["id"]: sc["base"][a["id"]] * scenario_mult(a, sc["salt"], SCEN_TICKS - 1) for a in ASSETS}
    after = acct["cash"] + sum(p["units"] * final[aid] for aid, p in acct["positions"].items())
    end_time = sc["started_at"] + SCEN_TICKS * SCEN_TICK_SECONDS
    for a in ASSETS:
        acct["offsets"][a["id"]] = {"r": final[a["id"]] / normal_price(a, end_time), "t": end_time}
    acct["last_result"] = {"before": round(sc["before_value"], 2), "after": round(after, 2),
                           "at": datetime.fromtimestamp(end_time, timezone.utc).isoformat()}
    acct["scenario"] = None
    return True


def build_state(acct: dict, now: float, asset_id: str, tf: str) -> dict:
    a = BY_ID.get(asset_id) or ASSETS[0]
    n, step = TIMEFRAMES.get(tf, TIMEFRAMES["1MIN"])
    tick = _scenario_tick(acct, now)
    in_scenario = tick is not None and tick < SCEN_TICKS
    series = []
    if in_scenario:
        sc = acct["scenario"]
        first = max(0, tick - 59)
        # lead-in: the minute before the crash, so the chart shows calm then the drop
        t0 = sc["started_at"]
        scale = sc["base"][a["id"]] / normal_price(a, t0)
        pre = 60 - (tick + 1 - first)
        for k in range(pre, 0, -1):
            series.append({"t": t0 - k, "p": normal_price(a, t0 - k) * scale})
        for i in range(first, tick + 1):
            series.append({"t": t0 + i * SCEN_TICK_SECONDS, "p": sc["base"][a["id"]] * scenario_mult(a, sc["salt"], i)})
    else:
        base_t = int(now)
        for k in range(n - 1, -1, -1):
            t = base_t - k * step
            series.append({"t": t, "p": normal_price(a, t) * offset_at(acct, a["id"], t)})
    assets = []
    for x in ASSETS:
        assets.append({k: x[k] for k in ("id", "name", "short", "color", "icon", "why")} | {"price": price_of(acct, x, now)})
    positions = []
    for aid, p in acct["positions"].items():
        price = price_of(acct, BY_ID[aid], now)
        value = p["units"] * price
        positions.append({"asset": aid, "units": p["units"], "cost": p["cost"], "value": value, "pnl": value - p["cost"]})
    return {
        "cash": acct["cash"], "total": total_value(acct, now), "start_cash": START_CASH,
        "assets": assets, "selected": {"asset": a["id"], "tf": tf if tf in TIMEFRAMES else "1MIN", "series": series},
        "positions": positions, "trades": acct["trades"][-30:][::-1],
        "scenario": {"active": in_scenario, "tick": tick if in_scenario else None, "total": SCEN_TICKS} if in_scenario else {"active": False},
        "last_result": acct.get("last_result"), "tour_done": acct.get("tour_done", False),
        "min_buy": MIN_BUY, "now": now,
    }


class TradeIn(BaseModel):
    asset: str
    side: str
    amount: Optional[float] = None    # rupees to spend (buy)
    percent: Optional[float] = None   # share of the holding to sell (sell)


class ScenarioIn(BaseModel):
    id: str = "crash"


class TourIn(BaseModel):
    skipped: bool = False


def make_router(db, get_current_user, xp_today_fields, learner_today):
    r = APIRouter(prefix="/practice")

    async def load(user_id: str) -> dict:
        acct = await db.practice_accounts.find_one({"user_id": user_id}, {"_id": 0})
        if not acct:
            acct = new_account(user_id)
            await db.practice_accounts.insert_one(dict(acct))
        return acct

    async def save(acct: dict, old_rev: int):
        doc = {k: v for k, v in acct.items() if k not in ("user_id",)}
        doc["rev"] = old_rev + 1
        res = await db.practice_accounts.update_one({"user_id": acct["user_id"], "rev": old_rev}, {"$set": doc})
        if res.matched_count == 0:
            raise HTTPException(status_code=409, detail="Your practice account changed. Please try again.")
        acct["rev"] = old_rev + 1

    @r.get("/state")
    async def state(asset: str = "nifty", tf: str = "1MIN", user: dict = Depends(get_current_user)):
        acct = await load(user["id"])
        now = time.time()
        rev = acct["rev"]
        if settle_scenario(acct, now):
            await save(acct, rev)
        return build_state(acct, now, asset, tf)

    @r.post("/trade")
    async def trade(body: TradeIn, user: dict = Depends(get_current_user)):
        a = BY_ID.get(body.asset)
        if not a:
            raise HTTPException(status_code=400, detail="Unknown asset")
        if body.side not in ("buy", "sell"):
            raise HTTPException(status_code=400, detail="Side must be buy or sell")
        acct = await load(user["id"])
        rev = acct["rev"]
        now = time.time()
        settle_scenario(acct, now)
        price = price_of(acct, a, now)
        result = {}
        if body.side == "buy":
            amount = round(float(body.amount or 0), 2)
            if amount < MIN_BUY:
                raise HTTPException(status_code=400, detail=f"The smallest purchase is ₹{int(MIN_BUY)}")
            if amount > acct["cash"] + 1e-6:
                raise HTTPException(status_code=400, detail="You do not have that much practice money")
            units = amount / price
            pos = acct["positions"].get(a["id"], {"units": 0.0, "cost": 0.0})
            pos["units"] += units
            pos["cost"] += amount
            acct["positions"][a["id"]] = pos
            acct["cash"] -= amount
            acct["trades"].append({"side": "buy", "asset": a["id"], "name": a["name"], "amount": amount, "price": price, "at": now})
            result = {"side": "buy", "amount": amount, "units": units}
        else:
            pos = acct["positions"].get(a["id"])
            pct = float(body.percent or 0)
            if not pos or pos["units"] <= 0:
                raise HTTPException(status_code=400, detail="You do not own this asset")
            if pct <= 0 or pct > 100:
                raise HTTPException(status_code=400, detail="Choose a percentage between 1 and 100")
            frac = pct / 100.0
            sold = pos["units"] * frac
            proceeds = sold * price
            cost_part = pos["cost"] * frac
            pnl = proceeds - cost_part
            pos["units"] -= sold
            pos["cost"] -= cost_part
            if pos["units"] < 1e-9:
                del acct["positions"][a["id"]]
            acct["cash"] += proceeds
            acct["trades"].append({"side": "sell", "asset": a["id"], "name": a["name"], "amount": proceeds, "price": price, "pnl": pnl, "at": now})
            result = {"side": "sell", "amount": proceeds, "pnl": pnl, "during_scenario": acct.get("scenario") is not None}
        acct["trades"] = acct["trades"][-100:]
        await save(acct, rev)
        return {"result": result, "state": build_state(acct, now, a["id"], "1MIN")}

    @r.post("/reset")
    async def reset(user: dict = Depends(get_current_user)):
        acct = await load(user["id"])
        rev = acct["rev"]
        fresh = new_account(user["id"])
        fresh["tour_done"] = acct.get("tour_done", False)
        fresh["rev"] = rev
        await save(fresh, rev)
        return build_state(fresh, time.time(), "nifty", "1MIN")

    @r.post("/scenario/start")
    async def scenario_start(body: ScenarioIn, user: dict = Depends(get_current_user)):
        if body.id != "crash":
            raise HTTPException(status_code=400, detail="Unknown scenario")
        acct = await load(user["id"])
        rev = acct["rev"]
        now = time.time()
        settle_scenario(acct, now)
        if acct.get("scenario"):
            raise HTTPException(status_code=400, detail="A replay is already running")
        acct["scenario"] = {
            "id": "crash", "started_at": now, "salt": int(now) % 100000,
            "base": {x["id"]: price_of(acct, x, now) for x in ASSETS}, "before_value": total_value(acct, now),
        }
        acct["last_result"] = None
        await save(acct, rev)
        return build_state(acct, now, "nifty", "1MIN")

    @r.post("/tour-complete")
    async def tour_complete(body: TourIn, request: Request, user: dict = Depends(get_current_user)):
        acct = await load(user["id"])
        rev = acct["rev"]
        first_time = not acct.get("tour_done")
        acct["tour_done"] = True
        await save(acct, rev)
        xp = coins = 0
        if first_time and not body.skipped:
            xp, coins = TOUR_XP, TOUR_COINS
            stats = await db.user_stats.find_one({"user_id": user["id"]}, {"_id": 0}) or {}
            new_xp = stats.get("total_xp", 0) + xp
            await db.user_stats.update_one(
                {"user_id": user["id"]},
                {"$set": {"total_xp": new_xp, "level": 1 + new_xp // 100, "coins": stats.get("coins", 0) + coins,
                          **xp_today_fields(stats, xp, learner_today(request).isoformat())}},
                upsert=True,
            )
        return {"tour_done": True, "xp": xp, "coins": coins}

    return r
