"""Seed real course content for FinLingo. Generic structure that works for any certification."""
from datetime import datetime, timezone
import uuid


def _id():
    return str(uuid.uuid4())


def build_seed():
    """Return courses with embedded chapters, modules, concepts, and lessons."""

    # ---------- LOMA 280: Principles of Insurance ----------
    loma = {
        "id": _id(),
        "slug": "loma-280",
        "name": "LOMA 280",
        "title": "Principles of Insurance",
        "certification": "LOMA",
        "description": "Foundations of life insurance, risk management, and the insurance industry.",
        "color": "#FF6B35",
        "icon": "Shield",
        "order": 1,
        "chapters": [],
    }

    ch1 = {
        "id": _id(), "course_id": loma["id"], "order": 1,
        "title": "Risk & Insurance Basics",
        "description": "Understand risk, how insurance transfers it, and the role of insurers.",
        "modules": [],
    }
    m1 = {
        "id": _id(), "chapter_id": ch1["id"], "order": 1, "title": "What is Risk?",
        "concepts": [],
    }
    c1 = {
        "id": _id(), "module_id": m1["id"], "order": 1,
        "title": "Pure vs. Speculative Risk",
        "learning_objective": "Distinguish pure risk (only loss possible) from speculative risk (loss or gain possible).",
        "simple_explanation": "Pure risk has only two outcomes: loss or no loss. A house burning down is pure risk. Speculative risk includes the chance of gain — buying stocks is speculative. Insurance only covers pure risk.",
        "key_takeaways": [
            "Pure risk: loss or no loss only",
            "Speculative risk: loss, no change, or gain",
            "Only pure risk is insurable",
        ],
        "common_mistakes": [
            "Thinking investment risk is insurable",
            "Confusing risk with uncertainty",
        ],
        "xp_reward": 15,
        "lessons": [
            {
                "id": _id(), "type": "intro", "order": 1,
                "content": {
                    "heading": "Pure vs. Speculative Risk",
                    "body": "Insurance only deals with pure risk — situations where you can lose but never gain. Let's explore why.",
                },
            },
            {
                "id": _id(), "type": "mcq", "order": 2,
                "content": {
                    "question": "Which of the following is a pure risk?",
                    "options": [
                        "Investing in cryptocurrency",
                        "A house catching fire",
                        "Starting a new business",
                        "Buying stock options",
                    ],
                    "correct": 1,
                    "explanation": "A house fire results in loss or no loss — never gain. That's pure risk.",
                },
            },
            {
                "id": _id(), "type": "mcq", "order": 3,
                "content": {
                    "question": "Why isn't speculative risk insurable?",
                    "options": [
                        "It's too expensive",
                        "Because gain is also possible, violating the principle of indemnity",
                        "Insurers don't understand it",
                        "It's illegal to insure",
                    ],
                    "correct": 1,
                    "explanation": "Insurance restores you — it doesn't profit you. If gain is possible, insurance can't apply.",
                },
            },
            {
                "id": _id(), "type": "match", "order": 4,
                "content": {
                    "instruction": "Match each scenario with its risk type",
                    "pairs": [
                        {"left": "Car accident", "right": "Pure risk"},
                        {"left": "Stock market trade", "right": "Speculative risk"},
                        {"left": "Theft of property", "right": "Pure risk"},
                        {"left": "Real estate flip", "right": "Speculative risk"},
                    ],
                },
            },
        ],
    }
    c2 = {
        "id": _id(), "module_id": m1["id"], "order": 2,
        "title": "Law of Large Numbers",
        "learning_objective": "Explain how insurers predict losses using statistical aggregation.",
        "simple_explanation": "The more people in a risk pool, the more accurately insurers can predict average losses. This is why insurance works at scale.",
        "key_takeaways": [
            "Larger pools = more accurate predictions",
            "Enables fair pricing of premiums",
            "Foundation of actuarial science",
        ],
        "common_mistakes": ["Thinking it predicts individual losses (it predicts group averages)"],
        "xp_reward": 15,
        "lessons": [
            {"id": _id(), "type": "intro", "order": 1, "content": {"heading": "Law of Large Numbers", "body": "Insurance works because losses, while unpredictable individually, are predictable in aggregate."}},
            {"id": _id(), "type": "mcq", "order": 2, "content": {
                "question": "What does the law of large numbers help insurers do?",
                "options": ["Predict individual claims", "Predict aggregate losses accurately", "Eliminate risk entirely", "Avoid paying claims"],
                "correct": 1,
                "explanation": "It predicts the average, not the individual.",
            }},
            {"id": _id(), "type": "flashcard", "order": 3, "content": {
                "front": "Why do insurers need thousands of policyholders?",
                "back": "Larger pools make loss predictions statistically reliable — the Law of Large Numbers.",
            }},
        ],
    }
    m1["concepts"] = [c1, c2]

    m2 = {
        "id": _id(), "chapter_id": ch1["id"], "order": 2, "title": "Insurable Interest",
        "concepts": [
            {
                "id": _id(), "module_id": None, "order": 1,
                "title": "What is Insurable Interest?",
                "learning_objective": "Define insurable interest and why it matters.",
                "simple_explanation": "You must stand to lose something financially or emotionally for a policy to be valid. You can insure your own life or your spouse's — not a stranger's.",
                "key_takeaways": [
                    "Prevents wagering on lives/property",
                    "Required at the time of policy issue (life insurance)",
                    "Required at time of loss (property insurance)",
                ],
                "common_mistakes": ["Assuming you can insure anyone you know"],
                "xp_reward": 15,
                "lessons": [
                    {"id": _id(), "type": "intro", "order": 1, "content": {"heading": "Insurable Interest", "body": "No interest, no insurance. Let's see why this exists."}},
                    {"id": _id(), "type": "scenario", "order": 2, "content": {
                        "scene": "Sarah wants to buy a life insurance policy on a famous celebrity she has never met.",
                        "question": "Can she legally do this?",
                        "choices": [
                            {"text": "Yes, anyone can insure anyone", "correct": False, "feedback": "No — that would be gambling."},
                            {"text": "No, she has no insurable interest", "correct": True, "feedback": "Correct! She faces no financial loss from the celebrity's death."},
                            {"text": "Only if she pays double premium", "correct": False, "feedback": "Premium doesn't fix the lack of interest."},
                        ],
                    }},
                    {"id": _id(), "type": "mcq", "order": 3, "content": {
                        "question": "Insurable interest in life insurance must exist:",
                        "options": ["At time of claim", "At policy issue", "Continuously", "Never"],
                        "correct": 1,
                        "explanation": "For life insurance, it's required at issue — not at death.",
                    }},
                ],
            }
        ],
    }
    for c in m2["concepts"]:
        c["module_id"] = m2["id"]

    ch1["modules"] = [m1, m2]

    ch2 = {
        "id": _id(), "course_id": loma["id"], "order": 2,
        "title": "Life Insurance Products",
        "description": "Term, whole, universal — know the differences cold.",
        "modules": [
            {
                "id": _id(), "chapter_id": None, "order": 1, "title": "Term vs. Permanent",
                "concepts": [
                    {
                        "id": _id(), "module_id": None, "order": 1,
                        "title": "Term Life Insurance",
                        "learning_objective": "Identify the features of term life policies.",
                        "simple_explanation": "Term life covers you for a fixed period (10/20/30 years). Cheap, no cash value. If you outlive the term, coverage ends.",
                        "key_takeaways": ["Fixed period", "Lowest cost", "No cash value", "Death benefit only"],
                        "common_mistakes": ["Expecting cash value at term end"],
                        "xp_reward": 15,
                        "lessons": [
                            {"id": _id(), "type": "intro", "order": 1, "content": {"heading": "Term Life", "body": "Pure protection for a fixed window."}},
                            {"id": _id(), "type": "mcq", "order": 2, "content": {
                                "question": "What does a 20-year term life policy give you at year 21 if you're still alive?",
                                "options": ["Cash payout", "Free coverage", "Nothing — coverage ends", "Double benefit"],
                                "correct": 2,
                                "explanation": "Term policies have no value once the term ends.",
                            }},
                        ],
                    }
                ],
            }
        ],
    }
    for m in ch2["modules"]:
        m["chapter_id"] = ch2["id"]
        for c in m["concepts"]:
            c["module_id"] = m["id"]
    loma["chapters"] = [ch1, ch2]

    # ---------- CFA Level 1: Quantitative Methods ----------
    cfa = {
        "id": _id(), "slug": "cfa-l1-quant", "name": "CFA L1",
        "title": "Quantitative Methods", "certification": "CFA",
        "description": "Time value of money, statistics, and probability for CFA Level 1.",
        "color": "#2563EB", "icon": "TrendingUp", "order": 2,
        "chapters": [
            {
                "id": _id(), "course_id": None, "order": 1,
                "title": "Time Value of Money",
                "description": "PV, FV, and the magic of compounding.",
                "modules": [
                    {
                        "id": _id(), "chapter_id": None, "order": 1, "title": "Compounding",
                        "concepts": [
                            {
                                "id": _id(), "module_id": None, "order": 1,
                                "title": "Future Value Basics",
                                "learning_objective": "Compute the future value of a single cash flow.",
                                "simple_explanation": "FV = PV × (1 + r)^n. Money today grows to more tomorrow because of interest compounding.",
                                "key_takeaways": ["FV grows exponentially", "Higher r = faster growth", "Time is the biggest factor"],
                                "common_mistakes": ["Forgetting to compound (using simple interest)"],
                                "xp_reward": 20,
                                "lessons": [
                                    {"id": _id(), "type": "intro", "order": 1, "content": {"heading": "Compounding", "body": "The 8th wonder of the world — Einstein (allegedly)."}},
                                    {"id": _id(), "type": "mcq", "order": 2, "content": {
                                        "question": "$1,000 invested at 10% compounded annually grows to what in 2 years?",
                                        "options": ["$1,200", "$1,210", "$1,100", "$1,221"],
                                        "correct": 1,
                                        "explanation": "1000 × 1.1 × 1.1 = $1,210",
                                    }},
                                    {"id": _id(), "type": "flashcard", "order": 3, "content": {"front": "FV formula?", "back": "FV = PV × (1 + r)^n"}},
                                ],
                            }
                        ],
                    }
                ],
            }
        ],
    }
    cfa["chapters"][0]["course_id"] = cfa["id"]
    for m in cfa["chapters"][0]["modules"]:
        m["chapter_id"] = cfa["chapters"][0]["id"]
        for c in m["concepts"]:
            c["module_id"] = m["id"]

    # ---------- PMP: Project Foundations ----------
    pmp = {
        "id": _id(), "slug": "pmp-foundations", "name": "PMP",
        "title": "Project Management Foundations", "certification": "PMP",
        "description": "Core PMI principles, project lifecycle, and stakeholder mastery.",
        "color": "#10B981", "icon": "Briefcase", "order": 3,
        "chapters": [
            {
                "id": _id(), "course_id": None, "order": 1, "title": "Project Lifecycle",
                "description": "From initiation to closure.",
                "modules": [
                    {
                        "id": _id(), "chapter_id": None, "order": 1, "title": "The 5 Process Groups",
                        "concepts": [
                            {
                                "id": _id(), "module_id": None, "order": 1,
                                "title": "Initiating vs. Planning",
                                "learning_objective": "Differentiate initiating from planning activities.",
                                "simple_explanation": "Initiating defines the project (charter, stakeholders). Planning details HOW it will be done (scope, schedule, budget).",
                                "key_takeaways": ["Initiating: WHAT & WHO", "Planning: HOW & WHEN", "Charter is initiating; WBS is planning"],
                                "common_mistakes": ["Confusing charter with project plan"],
                                "xp_reward": 15,
                                "lessons": [
                                    {"id": _id(), "type": "intro", "order": 1, "content": {"heading": "Process Groups", "body": "PMI defines 5 groups: Initiating → Planning → Executing → Monitoring → Closing."}},
                                    {"id": _id(), "type": "mcq", "order": 2, "content": {
                                        "question": "Creating the project charter belongs to which process group?",
                                        "options": ["Planning", "Initiating", "Executing", "Closing"],
                                        "correct": 1,
                                        "explanation": "The charter authorizes the project — that's Initiating.",
                                    }},
                                    {"id": _id(), "type": "match", "order": 3, "content": {
                                        "instruction": "Match the deliverable to its process group",
                                        "pairs": [
                                            {"left": "Project Charter", "right": "Initiating"},
                                            {"left": "WBS", "right": "Planning"},
                                            {"left": "Status Reports", "right": "Monitoring"},
                                            {"left": "Lessons Learned", "right": "Closing"},
                                        ],
                                    }},
                                ],
                            }
                        ],
                    }
                ],
            }
        ],
    }
    pmp["chapters"][0]["course_id"] = pmp["id"]
    for m in pmp["chapters"][0]["modules"]:
        m["chapter_id"] = pmp["chapters"][0]["id"]
        for c in m["concepts"]:
            c["module_id"] = m["id"]

    return [loma, cfa, pmp]


def flatten_for_db(courses):
    """Flatten nested seed structure into separate collections."""
    out_courses, out_chapters, out_modules, out_concepts, out_lessons = [], [], [], [], []
    for course in courses:
        chapters = course.pop("chapters", [])
        out_courses.append(course)
        for ch in chapters:
            mods = ch.pop("modules", [])
            out_chapters.append(ch)
            for m in mods:
                concepts = m.pop("concepts", [])
                out_modules.append(m)
                for c in concepts:
                    lessons = c.pop("lessons", [])
                    out_concepts.append(c)
                    for lesson in lessons:
                        lesson["concept_id"] = c["id"]
                        out_lessons.append(lesson)
    return out_courses, out_chapters, out_modules, out_concepts, out_lessons


async def seed_courses(db):
    """Idempotent: only seeds if courses collection is empty."""
    existing = await db.courses.count_documents({})
    if existing > 0:
        return
    courses = build_seed()
    cs, chs, ms, cps, ls = flatten_for_db(courses)
    if cs:
        await db.courses.insert_many(cs)
    if chs:
        await db.chapters.insert_many(chs)
    if ms:
        await db.modules.insert_many(ms)
    if cps:
        await db.concepts.insert_many(cps)
    if ls:
        await db.lessons.insert_many(ls)
