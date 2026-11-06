"""Structural checks for the finance courses: every lesson has the fields the player needs."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import seed_cfa, seed_finance, seed_hindi, seed_life

bad = []
def chk(cond, msg):
    if not cond:
        bad.append(msg)

courses = seed_finance.build_finance_courses() + seed_life.build_life_courses() + [seed_hindi.build_hindi_course(), seed_cfa.build_cfa_course()]
n = 0
for c in courses:
    for ch in c["chapters"]:
        for m in ch["modules"]:
            for cp in m["concepts"]:
                where = f"{c['slug']}/{cp['title']}"
                chk(len(cp["key_takeaways"]) >= 3 and len(cp["common_mistakes"]) >= 3, where + ": takeaways/mistakes")
                types = [l["type"] for l in cp["lessons"]]
                chk(types[0] == "intro", where + ": starts with intro")
                chk(types.count("mcq") >= 2 and types.count("scenario") >= 2, where + ": needs 2+ mcq and 2+ scenarios")
                for l in cp["lessons"]:
                    n += 1
                    t, x = l["type"], l["content"]
                    if t == "mcq":
                        chk(0 <= x["correct"] < len(x["options"]) and len(x["options"]) >= 3, where + ": mcq index " + x["question"][:30])
                        chk(len(set(x["options"])) == len(x["options"]), where + ": duplicate mcq options")
                    if t == "scenario":
                        ch_ = x["choices"]
                        chk(sum(1 for k in ch_ if k.get("verdict") == "good") == 1, where + ": exactly one good choice: " + x["question"][:30])
                        chk(all(k["feedback"] for k in ch_), where + ": feedback missing")
                        for k in ch_:
                            o = k.get("outcome")
                            if o:
                                chk(isinstance(o["before"][1], (int, float)) and isinstance(o["after"][1], (int, float)), where + ": outcome numbers")
                    if t == "teach":
                        chk(len(x["bullets"]) >= 2, where + ": teach bullets")
print(f"{n} lessons checked in {len(courses)} courses")
print("FAILED:\n" + "\n".join(bad) if bad else "ALL PASSED")
sys.exit(1 if bad else 0)
