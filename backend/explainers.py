"""The 60-second daily explainer: one money idea in plain words, with a one-question check.

Two kinds, one per day:
  * "news"   written by an admin about a real headline, with a source link. Only published when a person has checked it.
  * "evergreen"  a built-in library that explains the idea behind common headlines, with no claims about today's news.
When no news explainer is published for the day, the evergreen of the day is shown, so the feature never goes stale
and never shows unchecked news. Reading it and answering the question pays a small reward once per day.
"""
import re
import uuid
from datetime import date, datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

READ_XP = 5
CORRECT_XP = 5
READ_COINS = 2

EVERGREEN = [
    {"id": "eg-repo", "headline": "“RBI cuts the repo rate.” What does that mean for you?",
     "summary": "The repo rate is the interest rate at which the RBI lends money to banks. When it falls, borrowing gets cheaper for banks, and many loans linked to it get cheaper for you too.",
     "points": ["Example: a ₹30 lakh, 20-year home loan at 9.00% has an EMI of about ₹26,992. At 8.75% it is about ₹26,511, which is roughly ₹480 less every month.",
                "Banks usually cut FD rates after a cut too, so savers earn a little less."],
     "why": "If you have a floating-rate loan, a cut can lower your EMI. If you live on FD interest, it can lower your income.",
     "term": ["Repo rate", "The rate at which the RBI lends short-term money to banks."],
     "quiz": ["When the RBI cuts the repo rate, what usually happens to new loan rates?", ["They tend to fall", "They always rise", "They stay fixed forever", "They become zero"], 0, "Cheaper money for banks usually feeds through to cheaper loans, though not instantly and not always by the full amount."]},
    {"id": "eg-inflation", "headline": "“Inflation rises to 6%.” Why should savers care?",
     "summary": "Inflation is how fast prices rise. At 6% a year, something that costs ₹100 today costs about ₹106 next year, so the same money buys less.",
     "points": ["Money kept idle loses buying power. ₹1,00,000 under a mattress for 10 years at 6% inflation buys only what about ₹55,800 buys today.",
                "Your savings need to earn more than inflation just to stay even."],
     "why": "This is why a savings plan that only keeps cash can slowly lose value, even though the number never goes down.",
     "term": ["Real return", "Your return after taking away inflation. It tells you how much your buying power actually grew."],
     "quiz": ["Inflation is 6% and your money earns 4%. What is happening to your buying power?", ["It is falling", "It is growing fast", "It is unchanged", "It doubles every year"], 0, "You earn less than prices rise, so each rupee buys a little less each year."]},
    {"id": "eg-index", "headline": "“Sensex falls 800 points.” Is that a lot?",
     "summary": "Sensex and Nifty are scoreboards for the market. Sensex tracks 30 large companies on the BSE. Nifty 50 tracks 50 large companies on the NSE.",
     "points": ["A fall of 800 points sounds big, but on a Sensex of about 80,000 it is only about 1%.",
                "Always look at the percentage, not the points."],
     "why": "Headlines use big numbers to grab attention. A 1% move is a normal day. A 10% fall in a month is the kind of thing to notice.",
     "term": ["Index", "A basket of shares used to measure how a part of the market is doing."],
     "quiz": ["What is the best way to judge how big a market fall is?", ["Look at the percentage change", "Look at the points only", "Ask what a friend thinks", "Wait for the next headline"], 0, "Points depend on the index level. A percentage lets you compare days and years fairly."]},
    {"id": "eg-gdp", "headline": "“India’s GDP grows 7%.” What is GDP?",
     "summary": "GDP is the total value of goods and services made in a country in a year. If it grows 7%, the economy produced about 7% more than before (after adjusting for prices).",
     "points": ["More production usually means more jobs, more business and more income.",
                "GDP is an average. It does not show how evenly the gains are shared."],
     "why": "A growing economy helps jobs and company profits. A shrinking one can mean layoffs and slower salary rises.",
     "term": ["GDP", "The total value of everything a country produces in a year."],
     "quiz": ["What does GDP measure?", ["The value of goods and services made in a year", "How much gold a country owns", "The rupee’s price in dollars", "Total bank deposits"], 0, "GDP adds up the value of all goods and services produced in a year."]},
    {"id": "eg-rupee", "headline": "“Rupee falls to a record low against the dollar.” Who pays?",
     "summary": "The exchange rate is the price of one dollar in rupees. When the rupee weakens, you need more rupees for each dollar.",
     "points": ["Example: if the rate moves from ₹80 to ₹90 per dollar, a $100 gadget goes from ₹8,000 to ₹9,000, which is 12.5% more.",
                "Imports like phones, petrol and foreign education cost more. Exporters and IT firms earning dollars can gain."],
     "why": "If you plan to study abroad or buy imported goods, a weaker rupee raises your costs.",
     "term": ["Exchange rate", "How many rupees one unit of a foreign currency costs."],
     "quiz": ["The rupee weakens from ₹80 to ₹90 per dollar. What happens to the price of a $100 import?", ["It costs more rupees", "It costs fewer rupees", "It stays the same", "It becomes free"], 0, "You need more rupees to buy the same dollars, so the import costs more."]},
    {"id": "eg-fd", "headline": "“FD rates are at 7%.” Is that actually good?",
     "summary": "An FD rate is the headline number. What matters is how it compares with inflation and tax.",
     "points": ["With 7% interest and 5% inflation, your real return is only about 1.9%, since (1.07 ÷ 1.05) − 1 ≈ 1.9%.",
                "FD interest is added to your income and taxed at your slab, which lowers the return further."],
     "why": "FDs are safe and steady, which suits an emergency fund or a short goal. For long goals, other options may grow faster, with more risk.",
     "term": ["Real interest rate", "The interest rate after subtracting inflation."],
     "quiz": ["An FD pays 7% while inflation is 5%. About how much is your real return?", ["About 2%", "7%", "12%", "Zero, always"], 0, "Roughly 7% − 5%, a little under 2% before tax."]},
    {"id": "eg-ipo", "headline": "“Hot IPO opens for subscription.” What is an IPO?",
     "summary": "An IPO is when a private company sells shares to the public for the first time, so it can raise money and list on the stock exchange.",
     "points": ["The company sets a price band and a minimum lot you must apply for.",
                "If more people apply than shares are available, allotment is by lottery, so you may get nothing.",
                "A strong listing day is not guaranteed. Some IPOs fall below their issue price."],
     "why": "Hype is loudest around IPOs. Read the company’s papers (the prospectus) and decide with money you can afford to lock up.",
     "term": ["Prospectus", "The official document where a company describes its business, risks and finances before an IPO."],
     "quiz": ["Is a profit on listing day guaranteed in an IPO?", ["No, some IPOs list below their price", "Yes, always", "Yes, if you apply early", "Yes, for small investors"], 0, "An IPO can list above or below its issue price. Nothing is guaranteed."]},
    {"id": "eg-credit", "headline": "“Your credit score decides your loan rate.” How is it made?",
     "summary": "A credit score (300 to 900, in India) summarises how reliably you repay loans and cards. Scores around 750 and above are generally seen as good.",
     "points": ["Paying EMIs and card bills on time matters most.",
                "Using too much of your card limit lowers your score. Many people try to stay under about 30%.",
                "Applying for many loans in a short time can pull the score down."],
     "why": "A good score can get you lower interest rates on a loan, which can save thousands over the years.",
     "term": ["Credit utilisation", "The share of your card limit you are using."],
     "quiz": ["Which habit helps your credit score the most?", ["Paying bills and EMIs on time", "Maxing out your card every month", "Applying for many loans at once", "Ignoring due dates"], 0, "Repayment history is the biggest factor in most credit scores."]},
    {"id": "eg-gold", "headline": "“Gold hits a new high.” Why does gold rise when people worry?",
     "summary": "Gold is seen as a safe place to park money when markets or currencies look shaky. More buyers push the price up.",
     "points": ["Gold does not pay interest or dividends. Its return comes only from a price rise.",
                "It can also fall for years. It is not a guaranteed shield."],
     "why": "A small amount of gold can balance a portfolio of shares, because they often move differently. It should not be everything.",
     "term": ["Diversification", "Spreading money across different things so one bad day does not sink you."],
     "quiz": ["Why do some people hold a little gold alongside shares?", ["It often moves differently, which spreads risk", "It always rises", "It pays a fixed monthly income", "It is tax free"], 0, "Different assets rise and fall at different times, so mixing them smooths the ride."]},
    {"id": "eg-nav", "headline": "“Fund’s NAV is ₹52.” Is that cheap or expensive?",
     "summary": "NAV is the price of one unit of a mutual fund: the value of what the fund owns, minus costs, divided by the number of units. A low NAV does not mean a bargain.",
     "points": ["₹10,000 buys the same share of a fund whether its NAV is ₹20 or ₹200. You just get a different number of units.",
                "The expense ratio is the yearly fee. A 1% fee on ₹1,00,000 is ₹1,000 a year, taken from the fund. Direct plans have lower fees than regular plans."],
     "why": "Compare funds by long-term results, fees and what they hold, not by the NAV number.",
     "term": ["Expense ratio", "The yearly fee a fund charges, as a percentage of your money."],
     "quiz": ["Is a fund with a ₹20 NAV cheaper than one with a ₹200 NAV?", ["No, NAV is not a measure of cheapness", "Yes, always", "Yes, it is ten times better", "Only on Mondays"], 0, "NAV just reflects the unit price. What matters is the fund’s results, holdings and fees."]},
    {"id": "eg-bull", "headline": "“Bears take control of the market.” What is a bear market?",
     "summary": "A bull market is a long stretch of rising prices. A bear market is a long stretch of falling prices, often described as a fall of 20% or more from a recent high.",
     "points": ["Markets have gone through many bull and bear phases and have recovered, but not on a fixed timetable.",
                "People who panic and sell in a bear market lock in the loss."],
     "why": "If you invest through an SIP for years, bear markets will happen. Knowing that in advance helps you stay calm.",
     "term": ["Bear market", "A long period of falling prices, usually a drop of 20% or more from a peak."],
     "quiz": ["A bear market is usually described as a fall of how much from a recent high?", ["About 20% or more", "About 1%", "About 2%", "About 5% in a day"], 0, "A fall of around 20% or more from a peak is the common rule of thumb."]},
    {"id": "eg-regulators", "headline": "“SEBI bans a finfluencer.” Who protects your money?",
     "summary": "India has separate regulators for each kind of money. The RBI looks after banks, loans and the rupee. SEBI looks after shares, mutual funds and brokers. IRDAI looks after insurance.",
     "points": ["Before you trust an adviser, check whether they are registered with SEBI (the register is public on its website).",
                "A regulator cannot protect you from your own risky choices, but it can act against fraud."],
     "why": "Anyone promising guaranteed returns on social media is a warning sign. Verify registration first.",
     "term": ["SEBI", "The Securities and Exchange Board of India, which regulates the stock market and mutual funds."],
     "quiz": ["Which regulator oversees shares and mutual funds in India?", ["SEBI", "IRDAI", "RBI only", "GST Council"], 0, "SEBI regulates the securities markets, including mutual funds and brokers."]},
    {"id": "eg-budget", "headline": "“Budget raises spending on roads and railways.” Where does the money come from?",
     "summary": "The Union Budget is the government’s plan for the year: how much it expects to earn, mainly from taxes like income tax, GST and corporate tax, and how it will spend it.",
     "points": ["When the government spends more than it earns, it borrows to cover the gap. That gap is called the fiscal deficit.",
                "Spending on infrastructure, welfare, defence and interest on old loans all compete for the same money."],
     "why": "Budget choices can change tax slabs, prices and the jobs created, so they reach your wallet too.",
     "term": ["Fiscal deficit", "The gap between what the government spends and what it earns, filled by borrowing."],
     "quiz": ["What is a fiscal deficit?", ["Spending more than the government earns", "A tax on shares", "A bank charge", "A type of insurance"], 0, "It is the shortfall between income and spending, which the government borrows to cover."]},
    {"id": "eg-lifestyle", "headline": "“Your salary rose 30%.” Why do some people still feel broke?",
     "summary": "Lifestyle inflation is when your spending rises every time your income does, so your savings never grow.",
     "points": ["Example: income goes from ₹30,000 to ₹40,000. If spending also rises by ₹10,000, you still save the same amount as before.",
                "A simple fix: decide in advance to put half of any raise into savings before you get used to it."],
     "why": "A bigger salary is only useful if some of it stays with you.",
     "term": ["Lifestyle inflation", "Spending more because you earn more, instead of saving the difference."],
     "quiz": ["You get a raise. What helps your savings the most?", ["Save a fixed part of the raise straight away", "Spend all of it right away", "Wait and see what is left", "Take on a new EMI"], 0, "Deciding in advance, before you adjust to the higher income, keeps the raise from disappearing."]},
]
for _e in EVERGREEN:
    _e["kind"] = "evergreen"
EG_BY_ID = {e["id"]: e for e in EVERGREEN}

URL_RE = re.compile(r"^https://[^\s]+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def evergreen_for(d: date) -> dict:
    return EVERGREEN[d.toordinal() % len(EVERGREEN)]


def public_view(e: dict, d: str) -> dict:
    """What the app shows. The correct answer is not included."""
    quiz = e["quiz"]
    return {
        "id": e["id"], "kind": e["kind"], "date": d, "headline": e["headline"], "summary": e["summary"],
        "points": e.get("points", []), "why": e["why"], "term": {"word": e["term"][0], "meaning": e["term"][1]},
        "quiz": {"question": quiz[0], "options": quiz[1]},
        "source_name": e.get("source_name"), "source_url": e.get("source_url"),
    }


class NewsIn(BaseModel):
    date: str
    headline: str
    summary: str
    points: List[str] = []
    why: str
    term_word: str
    term_meaning: str
    quiz_question: str
    quiz_options: List[str]
    quiz_correct: int
    quiz_explanation: str
    source_name: str
    source_url: str


class ReadIn(BaseModel):
    answer: int


def make_router(db, get_current_user, xp_today_fields, learner_today, on_read=None):
    r = APIRouter(prefix="/explainer")

    def need_admin(user: dict):
        if user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Admins only")

    async def explainer_for(d: date) -> dict:
        row = await db.explainers.find_one({"date": d.isoformat()}, {"_id": 0})
        if row:
            row["kind"] = "news"
            row["term"] = [row["term_word"], row["term_meaning"]]
            row["quiz"] = [row["quiz_question"], row["quiz_options"], row["quiz_correct"], row["quiz_explanation"]]
            return row
        return evergreen_for(d)

    @r.get("/today")
    async def today(request: Request, user: dict = Depends(get_current_user)):
        d = learner_today(request)
        e = await explainer_for(d)
        out = public_view(e, d.isoformat())
        read = await db.explainer_reads.find_one({"user_id": user["id"], "date": d.isoformat()}, {"_id": 0})
        out["done"] = bool(read)
        if read:
            out["result"] = {"correct": read["correct"], "correct_index": e["quiz"][2], "chosen": read["answer"], "explanation": e["quiz"][3], "xp": read["xp"]}
        return out

    @r.post("/read")
    async def read(body: ReadIn, request: Request, user: dict = Depends(get_current_user)):
        d = learner_today(request)
        e = await explainer_for(d)
        quiz = e["quiz"]
        if not 0 <= body.answer < len(quiz[1]):
            raise HTTPException(status_code=400, detail="Choose one of the answers")
        correct = body.answer == quiz[2]
        xp = READ_XP + (CORRECT_XP if correct else 0)
        doc = {"user_id": user["id"], "date": d.isoformat(), "explainer_id": e["id"], "answer": body.answer, "correct": correct, "xp": xp,
               "at": datetime.now(timezone.utc).isoformat()}
        res = await db.explainer_reads.update_one({"user_id": user["id"], "date": d.isoformat()}, {"$setOnInsert": doc}, upsert=True)
        if res.upserted_id is None:
            raise HTTPException(status_code=400, detail="You already read today's explainer")
        stats = await db.user_stats.find_one({"user_id": user["id"]}, {"_id": 0}) or {}
        new_xp = stats.get("total_xp", 0) + xp
        await db.user_stats.update_one(
            {"user_id": user["id"]},
            {"$set": {"total_xp": new_xp, "level": 1 + new_xp // 100, "coins": stats.get("coins", 0) + READ_COINS, **xp_today_fields(stats, xp, d.isoformat())}},
            upsert=True,
        )
        if on_read:
            await on_read(user["id"], d.isoformat())
        return {"correct": correct, "correct_index": quiz[2], "explanation": quiz[3], "xp": xp, "coins": READ_COINS}

    # ---------------- admin: write and publish a news explainer
    @r.get("/admin")
    async def admin_list(user: dict = Depends(get_current_user)):
        need_admin(user)
        return await db.explainers.find({}, {"_id": 0}).sort("date", -1).to_list(60)

    @r.post("/admin")
    async def admin_save(body: NewsIn, user: dict = Depends(get_current_user)):
        need_admin(user)
        if not DATE_RE.match(body.date):
            raise HTTPException(status_code=400, detail="Date must look like 2026-11-06")
        try:
            date.fromisoformat(body.date)
        except ValueError:
            raise HTTPException(status_code=400, detail="That date does not exist")
        if not URL_RE.match(body.source_url.strip()):
            raise HTTPException(status_code=400, detail="The source link must start with https://")
        opts = [o.strip() for o in body.quiz_options if o.strip()]
        if not 3 <= len(opts) <= 4 or len(set(opts)) != len(opts):
            raise HTTPException(status_code=400, detail="Give 3 or 4 different answer options")
        if not 0 <= body.quiz_correct < len(opts):
            raise HTTPException(status_code=400, detail="The correct answer must be one of the options")
        for name, val, lo, hi in [("Headline", body.headline, 10, 140), ("Summary", body.summary, 40, 600), ("Why it matters", body.why, 20, 400),
                                  ("Word", body.term_word, 2, 40), ("Meaning", body.term_meaning, 10, 200), ("Question", body.quiz_question, 10, 200),
                                  ("Explanation", body.quiz_explanation, 10, 300), ("Source name", body.source_name, 2, 60)]:
            if not lo <= len(val.strip()) <= hi:
                raise HTTPException(status_code=400, detail=f"{name} must be {lo} to {hi} characters")
        points = [p.strip()[:300] for p in body.points if p.strip()][:3]
        doc = {"id": str(uuid.uuid4()), "date": body.date, "headline": body.headline.strip(), "summary": body.summary.strip(), "points": points,
               "why": body.why.strip(), "term_word": body.term_word.strip(), "term_meaning": body.term_meaning.strip(),
               "quiz_question": body.quiz_question.strip(), "quiz_options": opts, "quiz_correct": body.quiz_correct,
               "quiz_explanation": body.quiz_explanation.strip(), "source_name": body.source_name.strip(), "source_url": body.source_url.strip(),
               "published_by": user["id"], "created_at": datetime.now(timezone.utc).isoformat()}
        await db.explainers.replace_one({"date": body.date}, doc, upsert=True)
        return {k: v for k, v in doc.items() if k != "published_by"}

    @r.delete("/admin/{date_}")
    async def admin_delete(date_: str, user: dict = Depends(get_current_user)):
        need_admin(user)
        res = await db.explainers.delete_one({"date": date_})
        if res.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Nothing published for that date")
        return {"ok": True}

    return r
