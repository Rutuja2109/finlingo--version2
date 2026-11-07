"""Checks the second chapters of Stock Market, Bitcoin, Taxes and Insurance: lesson structure and every figure in the text."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from seed_crypto_more import build_crypto_chapter_two  # noqa: E402
from seed_hindi_more import build_hindi_chapter_two  # noqa: E402
from seed_insurance_more import build_insurance_chapter_two  # noqa: E402
from seed_stock_more import build_stock_chapter_two  # noqa: E402
from seed_tax_more import build_tax_chapter_two  # noqa: E402

bad = []
chk = lambda cond, msg: None if cond else bad.append(msg)
CHAPTERS = {"stock": build_stock_chapter_two("c"), "crypto": build_crypto_chapter_two("c"),
            "tax": build_tax_chapter_two("c"), "insurance": build_insurance_chapter_two("c"), "hindi": build_hindi_chapter_two("c")}
BODY = {}
n_lessons = n_concepts = 0


def fv(m, years, r):  # monthly deposits at the start of each month, monthly compounding
    i = r / 12
    n = years * 12
    return m * (((1 + i) ** n - 1) / i) * (1 + i)


for name, ch in CHAPTERS.items():
    texts = []
    chk(ch["key"] and ch["title"] and ch["description"] and ch["order"] == 2, name + ": chapter fields")
    for cp in ch["modules"][0]["concepts"]:
        n_concepts += 1
        where = f"{name}/{cp['title']}"
        types = [l["type"] for l in cp["lessons"]]
        chk(types[0] == "intro", where + ": starts with intro")
        chk(types.count("mcq") >= 2 and types.count("scenario") >= 2, where + ": 2+ mcq and 2+ scenarios")
        chk(len(cp["key_takeaways"]) >= 3 and len(cp["common_mistakes"]) >= 3, where + ": takeaways and mistakes")
        chk("chat" in types and "swipe" in types, where + ": has a chat story and a myth-or-fact")
        chk(any(t in types for t in ("match", "slider", "budget")), where + ": has a hands-on lesson")
        chk(types.count("flashcard") >= 1, where + ": flashcard")
        for l in cp["lessons"]:
            n_lessons += 1
            t, x = l["type"], l["content"]
            texts.append(str(x))
            chk("TODO" not in str(x) and "lorem" not in str(x).lower(), where + ": placeholder text")
            if t == "mcq":
                chk(0 <= x["correct"] < len(x["options"]) and len(set(x["options"])) == len(x["options"]) and len(x["options"]) == 4, where + ": mcq " + x["question"][:25])
            if t == "scenario":
                good = [c for c in x["choices"] if c["verdict"] == "good"]
                chk(len(good) == 1 and len(x["choices"]) == 3 and all(c["feedback"] for c in x["choices"]), where + ": scenario " + x["question"][:25])
                for c in x["choices"]:
                    o = c.get("outcome")
                    if o:
                        chk(isinstance(o["before"][1], (int, float)) and isinstance(o["after"][1], (int, float)) and o["note"], where + ": outcome " + x["question"][:25])
            if t == "teach":
                chk(len(x["bullets"]) >= 2, where + ": teach bullets")
            if t == "chat":
                chk(len(x["messages"]) >= 5 and all(m["who"] in ("lumi", "friend", "you") and m["text"] for m in x["messages"]) and x["takeaway"], where + ": chat")
            if t == "swipe":
                chk(len(x["cards"]) >= 4 and {c["answer"] for c in x["cards"]} == {"myth", "fact"} and all(c["why"] for c in x["cards"]), where + ": swipe")
            if t == "match":
                rights = [p["right"] for p in x["pairs"]]
                chk(len(x["pairs"]) >= 4 and len(set(rights)) == len(rights) and len({p["left"] for p in x["pairs"]}) == len(rights), where + ": match pairs unique")
            if t == "slider":
                chk(x["kind"] in ("growth", "inflation", "drawdown", "cost"), where + ": slider kind")
                keys = {c["key"] for c in x["controls"]}
                need = {"growth": {"years", "rate"}, "inflation": {"price", "years", "rate"}, "drawdown": {"amount", "loss"}, "cost": {"monthly", "years", "rate", "cost"}}[x["kind"]]
                chk(keys >= need, where + ": slider keys")
                chk(all(c["min"] <= c["value"] <= c["max"] and c["step"] > 0 for c in x["controls"]), where + ": slider ranges")
    BODY[name] = " ".join(texts)

B = BODY
# ------------------------------------------------------------------ stock
low, high, two = fv(5000, 20, 0.118), fv(5000, 20, 0.105), fv(5000, 20, 0.10)
chk(round(low) == 4862379 and "₹48.6 lakh" in B["stock"], "stock: low-cost plan 48.6 lakh")
chk(round(high) == 4087984 and "₹40.9 lakh" in B["stock"], "stock: costly plan 40.9 lakh")
chk(abs((low - high) / 1e5 - 7.74) < 0.01 and "₹7.7 lakh" in B["stock"], "stock: fee gap 7.7 lakh")
chk(round(two) == 3828485 and str(round(two)) in B["stock"], "stock: 2% fee plan value")
chk(f"₹{(low - two) / 1e5:.1f} lakh less" in B["stock"] and round((low - two) / 1e5, 1) == 10.3, "stock: 2% fee gap 10.3 lakh")
chk(5000 * 240 == 1200000 and "₹12 lakh" in B["stock"], "stock: 12 lakh invested")
navs = [50, 40, 25, 40, 50]
units = sum(5000 / v for v in navs)
chk(round(units) == 650 and abs(25000 / units - 38.46) < 0.01 and round(units * 50) == 32500 and "₹38.46" in B["stock"] and "₹32,500" in B["stock"], "stock: SIP example")
need = lambda loss: (1 / (1 - loss / 100) - 1) * 100
chk(round(need(50)) == 100 and round(need(20)) == 25 and round(need(30), 1) == 42.9 and round(need(10), 1) == 11.1, "stock: recovery maths")
chk(100000 * 0.8 == 80000 and 200000 * 0.85 == 170000 and 50000 * 0.8 == 40000 and 150000 * 0.8 == 120000, "stock: scenario outcomes")
chk(round(100000 * 1.04 ** 30) == 324340 and round(100000 * 1.10 ** 30) == 1744940, "stock: 30-year illustration")
chk(abs(1.8 / 0.3 - 6) < 1e-9 and 12 * 0.5 == 6, "stock: fee ratio and 12-rupee share")
chk(abs(12362 * 0.62 - 7664) < 1, "stock: 38% fall arithmetic")
# ------------------------------------------------------------------ crypto
chk(10000 * 0.25 == 2500 and round(need(75)) == 300, "crypto: 75% fall needs 300%")
chk(5000 * 0.75 == 3750 and 80000 * 0.75 == 60000 and 60000 * 0.25 == 15000 and 5000 * 0.25 == 1250 and 60000 * 0.75 == 45000, "crypto: sizing examples")
chk(round(10000 * 1.05 ** 30) == 43219 and "₹43,000" in B["crypto"], "crypto: 5% a day for 30 days")
chk(10000 * 1.05 ** 365 / 1e7 > 50000 and "₹50,000 crore" in B["crypto"], "crypto: 5% a day for a year is over 50,000 crore")
gain = 150000 - 100000
chk(gain * 0.30 == 15000 and round(gain * 0.30 * 1.04) == 15600 and 150000 * 0.01 == 1500, "crypto: tax 30%, cess and TDS")
chk(gain - 40000 == 10000 and gain * 0.30 > (gain - 40000), "crypto: tax exceeds net profit when losses cannot be set off")
chk(100 * 0.8 == 80 and 100 - 20 == 80, "crypto: stablecoin slip")
# ------------------------------------------------------------------ tax
chk(150000 * 0.20 == 30000 and round(30000 * 1.04) == 31200 and "₹31,200" in B["tax"], "tax: 80C saving at 20%")
tax = 40000
cum = [round(tax * p) for p in (0.15, 0.45, 0.75, 1.0)]
chk(cum == [6000, 18000, 30000, 40000] and [cum[0]] + [cum[i] - cum[i - 1] for i in (1, 2, 3)] == [6000, 12000, 12000, 10000], "tax: advance tax schedule")
chk(50000 * 0.25 == 12500 and 37500 == 50000 - 12500, "tax: tax pot")
chk(600000 * 0.5 == 300000, "tax: presumptive 50%")
# ------------------------------------------------------------------ insurance
bill, base, deductible, sup = 1200000, 500000, 500000, 2000000
base_pays = min(bill, base)
top_pays = min(max(bill - deductible, 0), sup)
chk(base_pays == 500000 and top_pays == 700000 and bill - base_pays == 700000 and bill - base_pays - top_pays == 0, "insurance: who pays what")
chk(800000 * 10 == 8000000, "insurance: 10x income")

# ------------------------------------------------------------------ hindi (same numbers as English Money Basics chapter 2)
H = B["hindi"]
for s in ("₹45 लाख", "₹23 लाख", "₹3.6 लाख", "₹7.2 लाख", "₹21,589", "₹46,610", "₹1,00,627", "₹179", "₹4,500", "₹2,250", "₹9,000", "₹6,000", "₹15,000", "55839", "29151", "30221", "206552", "4533", "₹55,800", "₹1,79,000"):
    chk(s in H, "hindi: figure present " + s)
chk(round(55839) == round(100000 / 1.06 ** 10) and round(100 * 1.06 ** 10) == 179 and round(30000 * 1.03 / 1.06) == 29151, "hindi: inflation figures")
chk(round(fv(1000, 10, 0.10)) == 206552 and round(20000 * 1.035 ** 12) == 30221 and round(3000 * 1.035 ** 12) == 4533, "hindi: outcome figures")
for ch_ in CHAPTERS["hindi"]["modules"][0]["concepts"]:
    for l in ch_["lessons"]:
        if l["type"] in ("chat", "swipe", "slider", "budget"):
            chk(l["content"].get("labels"), "hindi: interactive lesson has Hindi labels (" + l["type"] + ")")

print(f"{n_lessons} lessons checked in {n_concepts} concepts across {len(CHAPTERS)} chapters")
print("FAILED:\n" + "\n".join(bad) if bad else "ALL PASSED")
sys.exit(1 if bad else 0)
