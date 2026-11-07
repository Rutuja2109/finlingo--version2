"""Checks Money Basics chapter 2: lesson structure (incl. the new interactive types) and every rupee figure in the text."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from seed_money_more import build_money_chapter_two  # noqa: E402

bad = []
chk = lambda cond, msg: None if cond else bad.append(msg)
ch = build_money_chapter_two("course-x")
lessons_n = 0
texts = []


def fv(m, years, r):  # monthly deposits at the start of each month, monthly compounding
    i = r / 12
    n = years * 12
    return m * (((1 + i) ** n - 1) / i) * (1 + i)


for cp in ch["modules"][0]["concepts"]:
    where = cp["title"]
    types = [l["type"] for l in cp["lessons"]]
    chk(types[0] == "intro", where + ": starts with intro")
    chk(types.count("mcq") >= 2 and types.count("scenario") >= 2, where + ": 2+ mcq and 2+ scenarios")
    chk(len(cp["key_takeaways"]) >= 3 and len(cp["common_mistakes"]) >= 3, where + ": takeaways/mistakes")
    chk({"chat", "swipe"} <= set(types), where + ": uses chat and swipe")
    for l in cp["lessons"]:
        lessons_n += 1
        t, x = l["type"], l["content"]
        texts.append(str(x))
        if t == "mcq":
            chk(0 <= x["correct"] < len(x["options"]) and len(set(x["options"])) == len(x["options"]), where + ": mcq " + x["question"][:25])
        if t == "scenario":
            good = [c for c in x["choices"] if c["verdict"] == "good"]
            chk(len(good) == 1 and all(c["feedback"] for c in x["choices"]), where + ": scenario " + x["question"][:25])
        if t == "teach":
            chk(len(x["bullets"]) >= 2, where + ": teach bullets")
        if t == "chat":
            chk(len(x["messages"]) >= 5 and all(m["who"] in ("lumi", "friend", "you") and m["text"] for m in x["messages"]), where + ": chat messages")
            chk(x["takeaway"], where + ": chat takeaway")
        if t == "swipe":
            chk(len(x["cards"]) >= 4 and all(c["answer"] in ("myth", "fact") and c["why"] for c in x["cards"]), where + ": swipe cards")
            chk({c["answer"] for c in x["cards"]} == {"myth", "fact"}, where + ": swipe has both myths and facts")
        if t == "slider":
            chk(x["kind"] in ("growth", "inflation"), where + ": slider kind")
            keys = {c["key"] for c in x["controls"]}
            chk(keys >= ({"years", "rate", "price"} if x["kind"] == "inflation" else {"years", "rate"}), where + ": slider keys")
            chk(all(c["min"] <= c["value"] <= c["max"] and c["step"] > 0 for c in x["controls"]), where + ": slider ranges")
        if t == "budget":
            chk(x["income"] > 0 and x["start"]["needs"] + x["start"]["wants"] <= 100, where + ": budget start")

# ---- every figure quoted in the lessons
body = " ".join(texts)
asha32 = fv(3000, 10, 0.10)
asha52 = asha32 * (1 + 0.10 / 12) ** 240
bala52 = fv(3000, 20, 0.10)
chk(abs(asha52 - 4540885) < 5 and "₹45 lakh" in body, "Asha at 52 is about 45 lakh")
chk(abs(bala52 - 2297091) < 5 and "₹23 lakh" in body, "Bala at 52 is about 23 lakh")
chk(3000 * 120 == 360000 and "₹3.6 lakh" in body and 3000 * 240 == 720000 and "₹7.2 lakh" in body, "amounts put in")
chk(asha52 > bala52 and 3000 * 120 < 3000 * 240, "Asha ends higher with half the deposits")
chk(round(fv(1000, 10, 0.10)) == 206552, "1,000 a month for 10 years")
chk(round(3000 * 1.035 ** 12) == 4533, "3,000 on a card for a year")
chk(round(20000 * 1.035 ** 12) == 30221 and "30,221" not in body.replace("30221", ""), "20,000 on a card for a year")
chk(abs(1.035 ** 12 - 1.51) < 0.01, "3.5% a month is about 51% a year")
chk([round(10000 * 1.08 ** y) for y in (10, 20, 30)] == [21589, 46610, 100627] and all(s in body for s in ("₹21,589", "₹46,610", "₹1,00,627")), "10,000 at 8%")
chk(round(100 * 1.06 ** 10) == 179 and "₹179" in body, "100 -> 179")
chk(round(100000 / 1.06 ** 10) == 55839 and round(100000 * 1.06 ** 10) == 179085, "1,00,000 buying power")
chk(round(30000 * 1.03 / 1.06) == 29151 and 30000 * 1.03 == 30900, "Priya's real pay")
chk(72 / 8 == 9, "rule of 72 at 8%")
chk(abs((1 - 100000 / 1.06 ** 10 / 100000) - 0.44) < 0.005, "about 44% lost")
chk(150 * 30 == 4500 and 4500 / 2 == 2250, "UPI leak numbers")
chk(30000 * 0.2 == 6000 and 30000 * 0.3 == 9000 and 30000 * 0.5 == 15000, "50/30/20 on 30,000")

print(f"{lessons_n} lessons checked in {len(ch['modules'][0]['concepts'])} concepts")
print("FAILED:\n" + "\n".join(bad) if bad else "ALL PASSED")
sys.exit(1 if bad else 0)
