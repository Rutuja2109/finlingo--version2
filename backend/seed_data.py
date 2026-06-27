"""Seed LOMA 357 â€” Institutional Investing: Principles and Practices.
Phase 1: Chapters 1-3 only.
"""
from datetime import datetime, timezone
import uuid


def _id():
    return str(uuid.uuid4())


# â”€â”€ lesson builders â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def _intro(heading, body):
    return {"id": _id(), "type": "intro", "content": {"heading": heading, "body": body}}

def _teach(heading, body, bullets):
    return {"id": _id(), "type": "teach", "content": {"heading": heading, "body": body, "bullets": bullets}}

def _example(heading, scenario, lesson):
    return {"id": _id(), "type": "example", "content": {"heading": heading, "scenario": scenario, "lesson": lesson}}

def _flash(front, back):
    return {"id": _id(), "type": "flashcard", "content": {"front": front, "back": back}}

def _mcq(question, options, correct, explanation):
    return {"id": _id(), "type": "mcq", "content": {
        "question": question, "options": options,
        "correct": correct, "explanation": explanation,
    }}

def _scenario(scene, question, choices):
    return {"id": _id(), "type": "scenario", "content": {
        "scene": scene, "question": question,
        "choices": [{"text": t, "correct": c, "feedback": f} for t, c, f in choices],
    }}

def _concept(mod_id, order, title, objective, simple_explanation,
             real_world_example, key_takeaways, common_mistakes, lessons, xp=25):
    for i, l in enumerate(lessons):
        l["order"] = i + 1
    return {
        "id": _id(), "module_id": mod_id, "order": order,
        "title": title, "learning_objective": objective,
        "simple_explanation": simple_explanation,
        "real_world_example": real_world_example,
        "key_takeaways": key_takeaways,
        "common_mistakes": common_mistakes,
        "xp_reward": xp, "lessons": lessons,
    }


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# CHAPTER 1 â€” Introduction to Investing
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def _build_ch1(course_id):
    ch_id = _id()
    ch = {
        "id": ch_id, "course_id": course_id, "order": 1,
        "title": "Introduction to Investing",
        "description": "Understand what investing is, who investors are, and how the investment function operates inside an insurance company.",
    }

    # â”€â”€ Module 1: Investing Fundamentals â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    m1_id = _id()
    m1 = {"id": m1_id, "chapter_id": ch_id, "order": 1, "title": "Investing Fundamentals"}

    c1 = _concept(m1_id, 1,
        "What Is Investing?",
        "Define investing and distinguish it from speculating and gambling.",
        "Investing means putting money into assets today to earn income or capital gains over time. "
        "It requires analysis, patience, and risk management â€” very different from gambling (pure chance) "
        "or speculating (very short-term, high-risk bets).",
        "MetLife puts $500 million into 10-year government bonds expecting steady coupon income "
        "to match future policyholder claims â€” that is classic institutional investing.",
        [
            "Return = Income (interest/dividends) + Capital Gains (price appreciation)",
            "Long time horizons separate investors from speculators",
            "Institutional investors manage money on behalf of others (e.g. policyholders)",
            "Risk analysis is inseparable from return analysis",
        ],
        [
            "Assuming all risk-taking is gambling â€” investing manages risk through analysis",
            "Confusing short-term speculation with long-term investing",
        ],
        [
            _intro("What Is Investing?",
                   "Every dollar has a job to do. Investing is about putting capital to work "
                   "intelligently â€” earning returns while managing risk. Let's explore what "
                   "truly separates investors from gamblers and speculators."),
            _teach("Capital at Work",
                   "Investing is the act of committing money to an asset â€” a bond, stock, "
                   "real estate property, or other instrument â€” with the expectation of "
                   "earning a return. That return has two forms: income (regular cash flows "
                   "like interest or dividends) and capital gains (the asset appreciates in "
                   "value). Institutional investors like life insurance companies manage "
                   "billions of dollars, selecting assets whose returns and timing match "
                   "their long-term obligations to policyholders.",
                   [
                       "Income return: interest, dividends, rent received periodically",
                       "Capital gain: asset sells for more than its purchase price",
                       "Total return = income + capital gain (or loss)",
                       "Risk-adjusted return: balancing expected gain against potential loss",
                   ]),
            _teach("Investing vs. Speculating vs. Gambling",
                   "These three are often confused but differ fundamentally. A gambler creates "
                   "artificial risk â€” the casino has an edge and there is no underlying asset "
                   "to analyze. A speculator takes on existing market risk for short-term "
                   "price gains, often using leverage and rapid trading. An investor commits "
                   "capital based on thorough analysis of an asset's fundamentals, cash flows, "
                   "and long-term value â€” typically holding for years or decades. Life insurers "
                   "must invest, not speculate, because their policyholders depend on stable, "
                   "predictable returns over very long periods.",
                   [
                       "Gambling: creates new risk; no underlying economic asset; purely chance",
                       "Speculating: existing risk; short horizon; leverage-driven; price focus",
                       "Investing: long horizon; fundamental analysis; risk carefully managed",
                       "Insurers face a legal and ethical duty to invest prudently for policyholders",
                   ]),
            _example("The $1 Billion Decision",
                     "Sarah Chen, CIO at Pacific Life Insurance, receives a pitch: allocate "
                     "$1 billion to a currency hedge fund promising 30% annual returns through "
                     "leveraged short-term trades. Her colleague James is excited. Sarah "
                     "reviews the fund: 60-day hold periods, 10x leverage, bets on currency "
                     "swings. Pacific Life's policies carry 20-year obligations. She declines. "
                     "Instead, she directs the $1 billion into 20-year investment-grade bonds "
                     "yielding 4.5% â€” perfectly matching the company's liability duration. "
                     "Two years later, the hedge fund loses 40%. Pacific Life is unaffected.",
                     "Institutional investors align every asset with long-term obligations. "
                     "Speculation, however tempting, violates their fiduciary duty."),
            _flash("What two components make up total investment return?",
                   "Income (interest/dividends/rent) + Capital Gains (price appreciation)"),
            _mcq("Which of the following BEST defines investing?",
                 ["Buying a lottery ticket for a large jackpot",
                  "Committing capital to an asset with risk-return analysis over a meaningful time horizon",
                  "Making a short-term bet on currency movements using leverage",
                  "Depositing money in a savings account for one week"],
                 1,
                 "Investing requires analysis, a meaningful time horizon, and a risk-return framework â€” "
                 "not pure chance or very short-term price bets."),
            _mcq("A life insurer buys 20-year government bonds to match 20-year policy liabilities. "
                 "A day trader buys the same bonds and sells them in 3 days for a small gain. "
                 "Which party is speculating?",
                 ["The life insurer", "The day trader",
                  "Both equally", "Neither â€” both are investing"],
                 1,
                 "The day trader's short-term, price-movement approach is speculation. "
                 "The insurer's duration-matched, liability-driven approach is investing."),
            _mcq("Which characteristic MOST distinguishes investing from speculating?",
                 ["The amount of capital committed",
                  "The use of long time horizons and fundamental analysis",
                  "The type of asset class selected",
                  "The size of the expected return"],
                 1,
                 "Investing is defined by long horizons and fundamental analysis of underlying "
                 "asset value, not by the dollar amount or asset class alone."),
            _mcq("An insurance company earns $2 million in bond coupon payments and $500,000 "
                 "from selling an appreciated stock. What is the total return?",
                 ["$500,000", "$2,000,000", "$2,500,000", "$1,500,000"],
                 2,
                 "Total return = income ($2M coupons) + capital gains ($500K stock sale) = $2.5M."),
            _mcq("COMMON MISTAKE: A new analyst says 'All investing is just legal gambling.' "
                 "What is wrong with this statement?",
                 ["It is correct â€” all investments involve chance",
                  "Investing uses analysis and long horizons to manage risk; gambling relies purely on chance with no underlying asset",
                  "Gambling is just very short-term investing",
                  "Both involve risk, so they are the same thing"],
                 1,
                 "The key difference: investing analyzes underlying asset value and manages risk "
                 "systematically. Gambling creates artificial risk with no economic purpose."),
            _scenario("You are an investment analyst at Prudential Insurance. Your manager "
                      "proposes buying 60-day call options on tech stocks to 'boost quarterly "
                      "returns by 15%.' Prudential's policyholders hold 25-year life contracts.",
                      "What is the most appropriate response?",
                      [("Agree â€” higher returns always benefit policyholders", False,
                        "Short-term options are speculation mismatched to 25-year obligations. "
                        "Policyholders need stable long-term returns."),
                       ("Decline â€” this speculative strategy mismatches Prudential's 25-year liability horizon", True,
                        "Correct. The 60-day options are speculation that violates the "
                        "prudent investor standard required of insurance companies."),
                       ("Invest 5% just to test it out", False,
                        "Even partial speculation violates the insurer's fiduciary duty "
                        "and likely breaches the Investment Policy Statement."),
                       ]),
        ],
    )

    c2 = _concept(m1_id, 2,
        "Types of Investors: Retail vs. Institutional",
        "Distinguish retail investors from institutional investors and explain why insurers are key institutional investors.",
        "Retail investors are individuals managing their own money â€” they are typically small-scale "
        "and have shorter time horizons. Institutional investors manage large pools of money on "
        "behalf of others: pension funds, endowments, mutual funds, and insurance companies. "
        "Insurance companies are among the largest institutional investors in the world.",
        "Prudential Financial manages over $1.5 trillion in assets on behalf of millions of "
        "policyholders, pension clients, and institutional customers â€” making it one of the "
        "world's largest institutional investors.",
        [
            "Retail investors: individuals, smaller scale, shorter horizons",
            "Institutional investors: manage others' money, large scale, long horizons",
            "Insurance companies are major institutional investors due to large premium pools",
            "Institutional investors have greater market influence and access to deal flow",
        ],
        [
            "Assuming institutional investors just have 'more money' â€” they also have different obligations and constraints",
            "Thinking all institutional investors behave identically â€” insurers differ from hedge funds significantly",
        ],
        [
            _intro("Who Are Investors?",
                   "Not all investors are created equal. A retiree putting $10,000 in an index "
                   "fund and an insurance company deploying $10 billion in bonds both 'invest' â€” "
                   "but they operate in completely different worlds. Let's understand why."),
            _teach("Retail Investors",
                   "Retail investors are individuals investing their personal funds. They typically "
                   "invest smaller amounts, have shorter time horizons (saving for a home or "
                   "retirement), and access markets through brokerage accounts or mutual funds. "
                   "They often lack the resources for sophisticated analysis or access to private "
                   "investment opportunities. Their decisions are guided by personal financial goals "
                   "and risk tolerance rather than obligations to third parties.",
                   [
                       "Invest personal funds, not others' money",
                       "Smaller dollar amounts; limited market influence",
                       "Access markets via brokers, apps, mutual funds",
                       "Guided by personal goals: retirement, education, home purchase",
                   ]),
            _teach("Institutional Investors and Insurance Companies",
                   "Institutional investors manage large pools of capital on behalf of beneficiaries â€” "
                   "pension fund retirees, insurance policyholders, endowment beneficiaries, or "
                   "mutual fund shareholders. They have enormous market influence, access to private "
                   "deals, dedicated research teams, and strict regulatory oversight. Insurance "
                   "companies collect premiums today and promise to pay claims in the future. "
                   "To keep that promise, they must invest those premiums wisely. The investment "
                   "income helps keep premiums affordable for policyholders.",
                   [
                       "Manage capital on behalf of beneficiaries â€” fiduciary responsibility",
                       "Insurance companies: collect premiums â†’ invest â†’ pay claims",
                       "Investment income reduces the premiums policyholders must pay",
                       "Subject to strict regulatory constraints on what they can invest in",
                       "Must match investment horizon to liability duration",
                   ]),
            _example("The Pension Fund vs. The Day Trader",
                     "Maria is a 35-year-old teacher putting $500/month into a retirement account. "
                     "She picks low-cost index funds and plans to retire in 30 years â€” she is a "
                     "retail investor. Meanwhile, the California Public Employees Retirement System "
                     "(CalPERS) manages $450 billion on behalf of 2 million public employees. "
                     "CalPERS employs 400 investment professionals, invests in private equity, "
                     "real estate, and infrastructure, and has a 30-year liability horizon. "
                     "Both Maria and CalPERS are 'investors,' but their scale, sophistication, "
                     "obligations, and regulatory environment are fundamentally different.",
                     "Institutional investors are not just bigger retail investors â€” they operate "
                     "under fiduciary obligations, regulatory constraints, and long-term liability "
                     "matching requirements that retail investors never face."),
            _flash("Why do insurance companies invest premium income?",
                   "To earn returns that help pay future claims and keep policyholder premiums affordable."),
            _mcq("Which of the following is an institutional investor?",
                 ["A college student buying stocks through a mobile app",
                  "A retired teacher managing her personal IRA",
                  "A life insurance company managing policyholder premiums",
                  "A freelancer putting savings in a mutual fund"],
                 2,
                 "An insurance company manages capital on behalf of policyholders â€” "
                 "making it an institutional investor with fiduciary obligations."),
            _mcq("How do insurance companies primarily benefit policyholders through investing?",
                 ["By speculating in high-return assets",
                  "By earning investment income that helps reduce the premiums policyholders pay",
                  "By keeping all premiums in cash for safety",
                  "By investing only in government securities to avoid all risk"],
                 1,
                 "Investment income reduces the premiums insurers must charge, directly "
                 "benefiting policyholders with lower costs."),
            _mcq("What distinguishes institutional investors from retail investors?",
                 ["Institutional investors never lose money",
                  "Retail investors have more regulatory oversight",
                  "Institutional investors manage capital on behalf of beneficiaries under fiduciary duty",
                  "Retail investors have access to private equity and infrastructure deals"],
                 2,
                 "The defining feature of institutional investors is the fiduciary obligation "
                 "â€” they manage others' money and must act in beneficiaries' best interests."),
            _mcq("An insurer collects $100M in premiums. It invests $95M in bonds earning 4% annually. "
                 "How much annual investment income does this generate?",
                 ["$4,000,000", "$3,800,000", "$9,500,000", "$100,000,000"],
                 1,
                 "$95M Ã— 4% = $3.8 million in annual investment income to help fund future claims."),
            _mcq("COMMON MISTAKE: A student says institutional investors are 'just retail investors "
                 "with more money.' What is the critical difference they are missing?",
                 ["Institutional investors use different brokerage platforms",
                  "Institutional investors manage money on behalf of others and face fiduciary duties, "
                  "regulatory constraints, and liability-matching requirements retail investors don't have",
                  "Retail investors cannot buy bonds",
                  "There is no meaningful difference"],
                 1,
                 "Fiduciary duty, regulatory constraints, and liability matching are the "
                 "critical differences â€” not just the dollar amount."),
            _scenario("You work in the investment department of Northwestern Mutual, a life insurer. "
                      "The CEO suggests putting 50% of the $200 billion portfolio into a "
                      "cryptocurrency fund for potentially higher returns.",
                      "What concern should you immediately raise?",
                      [("Great idea â€” higher returns mean more profit", False,
                        "Cryptocurrency is highly volatile and speculative. Insurance regulators "
                        "prohibit such allocations, and it violates the prudent investor standard."),
                       ("This violates fiduciary duty, regulatory investment limits, and the "
                        "liability-matching requirement for a life insurer", True,
                        "Correct. Insurers must match long-term liabilities with stable assets. "
                        "Crypto's extreme volatility is incompatible with paying future claims reliably."),
                       ("Only invest 25% in crypto to limit the risk", False,
                        "Even a small allocation to highly speculative assets violates the "
                        "prudent investor standard for an insurance company."),
                       ]),
        ],
    )

    m1["concepts"] = [c1, c2]

    # â”€â”€ Module 2: The Investment Function â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    m2_id = _id()
    m2 = {"id": m2_id, "chapter_id": ch_id, "order": 2, "title": "The Investment Function"}

    c3 = _concept(m2_id, 1,
        "Overview of the Investment Function",
        "Describe how money flows through an insurance company and the role of the investment function.",
        "The investment function is the department inside an insurance company responsible for "
        "managing invested assets. Premiums collected flow into the investment department, which "
        "deploys them into bonds, stocks, real estate, and other assets. Investment income flows "
        "back to pay claims, expenses, and shareholder returns.",
        "At New York Life, premiums from 10 million policyholders flow into the investment department "
        "daily. The team of 200 investment professionals deploys those funds across government bonds, "
        "corporate bonds, mortgages, and equities â€” generating the income that funds claims.",
        [
            "Investment function: manages the insurer's invested assets",
            "Premium flow: collected â†’ invested â†’ returns help fund claims",
            "Investment income reduces need for higher premiums",
            "Investment professionals must balance return, risk, liquidity, and regulatory compliance",
        ],
        [
            "Thinking the investment department only buys stocks",
            "Overlooking that most insurance company assets are in bonds, not equities",
        ],
        [
            _intro("The Engine Behind Insurance",
                   "When you pay your insurance premium, that money does not sit in a vault. "
                   "It goes to work immediately in the investment function â€” the team that keeps "
                   "the promise to pay your claims. Let's follow the money."),
            _teach("Movement of Funds",
                   "An insurance company's cash flows work in a cycle. Policyholders pay premiums. "
                   "Those premiums are collected and handed to the investment department. Investment "
                   "professionals deploy the funds into various assets â€” government bonds, corporate "
                   "bonds, mortgages, equities, and real estate. Over time, these assets generate "
                   "income (interest, dividends, rent) and capital gains. When policyholders file "
                   "claims, the insurer uses investment income and, if necessary, sells assets to "
                   "fund those payments. This cycle is the core of how insurance companies operate.",
                   [
                       "Premiums in â†’ Investment department â†’ Assets purchased",
                       "Assets generate income and capital gains",
                       "Income + gains â†’ fund claims, expenses, and profit",
                       "Investment income allows insurers to offer more competitive premiums",
                   ]),
            _teach("Overview of the Investment Function",
                   "The investment function has four core responsibilities: (1) Portfolio Management "
                   "â€” selecting and managing assets; (2) Risk Management â€” ensuring the portfolio "
                   "does not expose the company to unacceptable levels of risk; (3) Compliance â€” "
                   "ensuring all investments meet legal and regulatory requirements; and (4) "
                   "Reporting â€” communicating portfolio performance to management and regulators. "
                   "The investment team works closely with actuaries (who model future liabilities), "
                   "the finance team (which manages cash flows), and senior management.",
                   [
                       "Portfolio management: selecting assets that match liability profile",
                       "Risk management: monitoring credit, interest rate, and liquidity risk",
                       "Compliance: ensuring investments meet state insurance regulations",
                       "Reporting: communicating performance to senior management and regulators",
                   ]),
            _example("Following the Premium Dollar at Lincoln Financial",
                     "Linda pays her $1,200 annual life insurance premium to Lincoln Financial. "
                     "That premium goes immediately to Lincoln's investment department. The team "
                     "allocates $900 into 10-year corporate bonds (75%), $200 into mortgage-backed "
                     "securities (17%), and $100 into equity (8%). Over the year, Lincoln earns "
                     "$54 in interest and dividends on Linda's $1,200. When Linda's husband dies "
                     "10 years later, Lincoln has been earning and reinvesting returns on "
                     "thousands of similar premiums â€” the investment income funds his $500,000 "
                     "death benefit without Lincoln needing to raise premiums.",
                     "The investment function converts premium income into long-term returns that "
                     "fund future claims â€” the entire business model depends on it working well."),
            _flash("What are the four core responsibilities of the investment function?",
                   "Portfolio Management, Risk Management, Compliance, and Reporting."),
            _mcq("What happens to insurance premiums immediately after they are collected?",
                 ["They are held in cash in a bank vault",
                  "They are returned to shareholders as dividends",
                  "They are handed to the investment department to be deployed into assets",
                  "They are used to pay the next policyholder claim immediately"],
                 2,
                 "Premiums are deployed by the investment department into bonds, equities, "
                 "mortgages, and other assets to generate the income needed to pay future claims."),
            _mcq("Why is investment income important for insurance companies?",
                 ["It allows insurers to avoid paying claims",
                  "It enables insurers to offer more competitive premiums by supplementing claim payments",
                  "It replaces the need to collect premiums",
                  "It is used exclusively for shareholder dividends"],
                 1,
                 "Investment income supplements premiums as a revenue source, allowing insurers "
                 "to offer more competitive rates while still meeting future obligations."),
            _mcq("Which team does the investment function work MOST closely with to understand future liabilities?",
                 ["Marketing", "Human Resources", "Actuaries", "Information Technology"],
                 2,
                 "Actuaries model the timing and amount of future claim payments â€” the investment "
                 "function must match the asset portfolio to those projected liability cash flows."),
            _mcq("A life insurer has $50B in assets. Industry data shows most insurance company "
                 "assets are in which asset class?",
                 ["Equities (stocks)", "Real estate", "Bonds (fixed income)", "Cryptocurrency"],
                 2,
                 "Life insurers hold the majority of their assets in bonds because bonds "
                 "provide predictable income and can be matched to long-term policy liabilities."),
            _mcq("COMMON MISTAKE: An analyst assumes the investment department only manages stocks. "
                 "What major asset class are they ignoring?",
                 ["Cryptocurrency", "Bonds â€” which make up the majority of most insurer portfolios",
                  "Foreign currencies", "Art and collectibles"],
                 1,
                 "Bonds dominate insurance company portfolios because they provide predictable "
                 "cash flows that match long-term policy liabilities. Stocks are a smaller portion."),
            _scenario("You are a new investment analyst at MetLife. Your supervisor asks you to "
                      "explain the 'movement of funds' cycle to a new colleague who just joined "
                      "from a tech company.",
                      "Which explanation is most accurate?",
                      [("MetLife invests premiums in stocks, waits for them to go up, then pays claims", False,
                        "This is oversimplified and wrong â€” most assets are bonds, and the "
                        "cycle is much more systematic than 'wait and sell.'"),
                       ("Policyholders pay premiums â†’ investment department deploys into diversified "
                        "assets â†’ income and gains fund future claim payments and expenses", True,
                        "Correct. This captures the full cycle: premiums â†’ investment â†’ income â†’ claims."),
                       ("MetLife collects premiums and holds them in cash until claims are filed", False,
                        "Holding premiums in cash would generate no return and fail to keep "
                        "premiums competitive â€” insurers must invest to stay solvent and competitive."),
                       ]),
        ],
    )

    c4 = _concept(m2_id, 2,
        "Organization and Internal Controls",
        "Describe how the investment function is organized and why internal controls matter.",
        "The investment function is structured with clear roles: portfolio managers make investment "
        "decisions, analysts research opportunities, traders execute transactions, and compliance "
        "officers ensure rules are followed. Internal controls prevent errors, fraud, and "
        "violations â€” protecting the company and its policyholders.",
        "At Allstate, investment decisions flow through a defined hierarchy: analysts research "
        "bonds â†’ portfolio managers approve allocations â†’ traders execute purchases â†’ compliance "
        "verifies each trade meets regulatory limits. This four-eyes principle prevents any "
        "single person from making unauthorized decisions.",
        [
            "Investment professionals: portfolio managers, analysts, traders, compliance officers",
            "Segregation of duties: decision-making separated from execution and verification",
            "Internal controls: processes preventing errors, fraud, and regulatory violations",
            "Board oversight: investment committee reviews strategy and major decisions",
        ],
        [
            "Thinking one person can do all investment tasks â€” segregation of duties is required",
            "Underestimating compliance â€” regulators can penalize insurers for policy violations",
        ],
        [
            _intro("Structure Behind the Strategy",
                   "A billion-dollar investment decision doesn't happen on a whim. There's a "
                   "carefully designed organizational structure and set of controls that ensures "
                   "every investment is appropriate, authorized, and properly monitored."),
            _teach("Roles of Investment Professionals",
                   "The investment function employs specialists with distinct roles. Portfolio "
                   "managers set strategy and decide which assets to buy or sell based on "
                   "the company's investment policy. Analysts research potential investments â€” "
                   "reading financial statements, building models, assessing credit quality. "
                   "Traders execute the actual purchase and sale transactions in the market. "
                   "Compliance officers verify that every transaction complies with the insurer's "
                   "investment policy statement and applicable regulations. Risk managers monitor "
                   "the portfolio's overall risk exposure continuously.",
                   [
                       "Portfolio managers: strategy and buy/sell decisions",
                       "Analysts: research, financial modeling, credit assessment",
                       "Traders: execute transactions in financial markets",
                       "Compliance officers: verify regulatory and policy adherence",
                       "Risk managers: continuous portfolio risk monitoring",
                   ]),
            _teach("Internal Controls and Segregation of Duties",
                   "Internal controls are the policies, procedures, and systems designed to "
                   "prevent errors, detect fraud, and ensure compliance. The most fundamental "
                   "control is segregation of duties: the person who decides to buy a bond "
                   "must be different from the person who executes the trade, which must be "
                   "different from the person who settles and records the transaction. This "
                   "four-eyes principle prevents a single rogue employee from making unauthorized "
                   "transactions. Other controls include investment committees that must approve "
                   "large transactions, pre-trade compliance checks, and regular independent "
                   "audits of the investment portfolio.",
                   [
                       "Segregation of duties: decision â†’ execution â†’ settlement by different people",
                       "Investment committee: board-level approval for major decisions",
                       "Pre-trade compliance: automatic checks before any trade executes",
                       "Regular audits: independent verification of portfolio composition and controls",
                   ]),
            _example("The Rogue Trader Scenario at Barings Bank",
                     "In 1995, Nick Leeson at Barings Bank had control over both trading AND "
                     "the back-office settlement function. Without segregation of duties, he "
                     "was able to hide $1.4 billion in losses in an error account â€” eventually "
                     "causing the collapse of the 233-year-old bank. Insurance companies learned "
                     "from such disasters: today, every insurer requires that the person who "
                     "decides to make a trade (front office), the person who executes it "
                     "(trading desk), and the person who records and settles it (back office) "
                     "are always different individuals reporting to different managers.",
                     "Segregation of duties is not bureaucracy â€” it is the control that "
                     "prevented countless insurance company failures."),
            _flash("What is 'segregation of duties' in the investment function?",
                   "Ensuring that the person who decides on an investment, the person who executes it, "
                   "and the person who settles/records it are always different individuals."),
            _mcq("Which role in the investment function is responsible for executing buy/sell "
                 "transactions in financial markets?",
                 ["Portfolio manager", "Analyst", "Trader", "Compliance officer"],
                 2,
                 "Traders are responsible for the actual execution of investment transactions "
                 "in financial markets. Portfolio managers decide; traders execute."),
            _mcq("Why is segregation of duties a critical internal control?",
                 ["It speeds up the investment process",
                  "It ensures no single individual can make, execute, and record a transaction â€” preventing fraud and errors",
                  "It reduces the number of employees needed",
                  "It allows more flexible investment strategies"],
                 1,
                 "Segregation of duties prevents any single person from controlling an entire "
                 "transaction, making fraud and unauthorized activity much harder to conceal."),
            _mcq("An investment committee is MOST important for:",
                 ["Hiring new analysts",
                  "Approving and overseeing major investment strategy decisions and large transactions",
                  "Processing routine trade settlements",
                  "Filing tax returns for the investment portfolio"],
                 1,
                 "Investment committees provide board-level governance over major investment "
                 "decisions, ensuring they align with the company's strategy and risk appetite."),
            _mcq("Which of the following is a pre-trade control?",
                 ["A compliance officer reviews trades after they settle",
                  "An analyst writes a research report after a bond is purchased",
                  "An automated system checks if a proposed trade complies with investment guidelines before it executes",
                  "A quarterly audit of the portfolio by external auditors"],
                 2,
                 "Pre-trade controls check compliance before execution â€” preventing non-compliant "
                 "trades rather than catching them after the fact."),
            _mcq("COMMON MISTAKE: A small insurance company lets its portfolio manager also "
                 "execute trades and record them in the accounting system. Why is this a problem?",
                 ["It is fine for small companies â€” controls are only for large firms",
                  "It violates segregation of duties, creating opportunity for fraud or errors to go undetected",
                  "It is more efficient and reduces costs",
                  "Regulators only require segregation for companies over $1 billion"],
                 1,
                 "Segregation of duties applies regardless of company size. A single person "
                 "controlling all steps creates unacceptable fraud and error risk."),
            _scenario("At Guarantee Life Insurance, analyst Tom discovers that the same employee "
                      "has been deciding which bonds to buy AND recording those transactions in "
                      "the accounting system for the past year.",
                      "What should Tom do?",
                      [("Nothing â€” it has worked fine so far", False,
                        "Past success doesn't mean the control is adequate. This is a fundamental "
                        "segregation of duties violation that must be corrected immediately."),
                       ("Report this immediately to the compliance officer and recommend splitting "
                        "the responsibilities between two different individuals", True,
                        "Correct. This is a clear control failure. It must be escalated to "
                        "compliance and corrected to prevent potential fraud or errors."),
                       ("Let the employee know personally but do not escalate", False,
                        "This is a systemic control failure that requires formal reporting and "
                        "structural correction â€” not an informal warning."),
                       ]),
        ],
    )

    m2["concepts"] = [c3, c4]
    ch["modules"] = [m1, m2]
    return ch


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# CHAPTER 2 â€” Overview of Basic Investment Vehicles
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def _build_ch2(course_id):
    ch_id = _id()
    ch = {
        "id": ch_id, "course_id": course_id, "order": 2,
        "title": "Overview of Basic Investment Vehicles",
        "description": "Master the major asset classes: cash, bonds, stocks, real estate, and REITs.",
    }

    # â”€â”€ Module 1: Fixed Income & Cash â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    m1_id = _id()
    m1 = {"id": m1_id, "chapter_id": ch_id, "order": 1, "title": "Fixed Income and Cash"}

    c1 = _concept(m1_id, 1,
        "Cash and Cash Equivalents",
        "Define cash and cash equivalents and explain why insurers hold them.",
        "Cash and cash equivalents are the most liquid assets â€” money in bank accounts, "
        "Treasury bills, commercial paper, and money market instruments maturing in 90 days "
        "or less. They earn low returns but provide immediate liquidity for unexpected claims.",
        "After Hurricane Katrina, insurers needed to pay $40 billion in claims quickly. "
        "Companies that held adequate cash and T-bills could pay without selling long-term "
        "bonds at a loss. Companies that were illiquid had to sell bonds at fire-sale prices.",
        [
            "Cash equivalents: T-bills, commercial paper, money market funds maturing in â‰¤90 days",
            "Highest liquidity, lowest return of all asset classes",
            "Insurers hold cash to meet unexpected claim surges and operational expenses",
            "Too much cash = opportunity cost; too little = liquidity risk",
        ],
        [
            "Assuming all cash equivalents are literally cash â€” T-bills and commercial paper also qualify",
            "Thinking more cash is always better â€” excess cash earns very little and hurts returns",
        ],
        [
            _intro("The Asset That Is Always Ready",
                   "Before we talk about sophisticated investments, let's start with the "
                   "most basic: cash. It earns almost nothing â€” but without it, an insurer "
                   "cannot pay claims. Understanding cash management is foundational."),
            _teach("What Are Cash and Cash Equivalents?",
                   "Cash includes physical currency and bank deposits â€” immediately available for "
                   "use. Cash equivalents are short-term, highly liquid investments that can be "
                   "converted to a known cash amount within 90 days with minimal price risk. "
                   "The most common cash equivalents used by insurers include: U.S. Treasury "
                   "bills (T-bills) issued by the federal government with maturities up to "
                   "52 weeks, commercial paper (short-term corporate debt, typically 1-270 days), "
                   "and money market funds that hold pools of these short-term instruments.",
                   [
                       "T-bills: U.S. government short-term debt, near-zero default risk",
                       "Commercial paper: unsecured corporate short-term debt, slightly higher yield",
                       "Money market funds: pooled short-term instruments, very stable value",
                       "Certificate of Deposit (CD): bank-issued, fixed term, FDIC-insured",
                       "All mature in 90 days or less and maintain stable value",
                   ]),
            _teach("Why Insurers Hold Cash Equivalents",
                   "Insurance companies hold cash for three reasons. First, liquidity: claims "
                   "arrive unpredictably and must be paid promptly â€” an insurer cannot tell a "
                   "bereaved family to 'wait while we sell a bond.' Second, operations: payroll, "
                   "rent, and technology costs must be met from liquid funds. Third, opportunity: "
                   "cash held ready can be deployed quickly when attractive investment "
                   "opportunities arise. However, holding too much cash is costly â€” cash earns "
                   "the lowest return of any asset class, hurting overall portfolio performance.",
                   [
                       "Liquidity reserve: pay unexpected large claims without forced asset sales",
                       "Operating cash: fund day-to-day business expenses",
                       "Opportunity fund: deploy quickly when good investments appear",
                       "Too much cash = opportunity cost (missing higher returns on bonds/equities)",
                       "Cash target is set by the company's liquidity policy, not left to chance",
                   ]),
            _example("The Hurricane Test",
                     "In August 2005, Hurricane Katrina made landfall, triggering $40 billion "
                     "in insured losses. State Farm received 500,000 claims in 48 hours. "
                     "Companies like State Farm that maintained disciplined liquidity reserves "
                     "in T-bills and money market funds could begin paying claims immediately. "
                     "Smaller, poorly managed insurers that held too little cash were forced to "
                     "sell long-term bonds in a disrupted market â€” receiving cents on the dollar "
                     "and struggling to pay claims on time, damaging policyholder trust.",
                     "Adequate cash reserves are not wasteful â€” they are the difference between "
                     "honoring promises and defaulting on them during a crisis."),
            _flash("What is the maximum maturity for an investment to be classified as a 'cash equivalent'?",
                   "90 days (3 months). Instruments maturing within 90 days with minimal price risk qualify."),
            _mcq("Which of the following is a cash equivalent?",
                 ["A 5-year corporate bond",
                  "A 30-day U.S. Treasury bill",
                  "A share of common stock",
                  "A 10-year mortgage loan"],
                 1,
                 "A 30-day T-bill matures in under 90 days, has near-zero default risk, "
                 "and can be converted to cash at a known value â€” the definition of a cash equivalent."),
            _mcq("Why would an insurance company hold T-bills instead of earning higher returns "
                 "in long-term bonds?",
                 ["T-bills have higher returns than long-term bonds",
                  "T-bills provide immediate liquidity to pay unexpected large claims quickly",
                  "Insurance regulators require all assets to be in T-bills",
                  "T-bills are always more profitable in the long run"],
                 1,
                 "T-bills sacrifice return for liquidity. Insurers need liquid assets to pay "
                 "claims without being forced to sell long-term assets at a loss."),
            _mcq("Commercial paper differs from Treasury bills in that commercial paper:",
                 ["Is issued by the federal government",
                  "Has a longer maturity (over 5 years)",
                  "Is unsecured corporate short-term debt with slightly higher yield and credit risk",
                  "Can only be purchased by retail investors"],
                 2,
                 "Commercial paper is short-term unsecured debt issued by corporations â€” "
                 "it offers slightly higher yields than T-bills but carries some credit risk."),
            _mcq("An insurer has $10B in assets. Industry practice suggests holding 5% in cash equivalents. "
                 "How much should be in cash?",
                 ["$50 million", "$500 million", "$5 billion", "$1 billion"],
                 1,
                 "$10B Ã— 5% = $500 million in cash equivalents as a liquidity reserve."),
            _mcq("COMMON MISTAKE: An analyst argues that holding any cash is wasteful because "
                 "bonds earn more. What critical factor are they ignoring?",
                 ["Bond prices never fall",
                  "Liquidity â€” insurers must pay claims on demand without forced asset sales",
                  "Cash earns more than bonds in the short term",
                  "Regulators prohibit bond investments"],
                 1,
                 "Cash provides liquidity for unexpected claims. Without it, insurers must "
                 "sell bonds at potentially unfavorable prices â€” often at a loss during crises."),
            _scenario("It is October 2024. A major earthquake strikes a region where your "
                      "insurer has significant property coverage. You expect $2 billion in "
                      "claims over the next 30 days. Your insurer currently holds only $200M "
                      "in cash and cash equivalents.",
                      "What is the most immediate problem this creates?",
                      [("No problem â€” the insurer can easily borrow the difference", False,
                        "Borrowing in a crisis is expensive and may not be possible quickly. "
                        "Adequate liquidity reserves should prevent this situation."),
                       ("The insurer must sell long-term bonds at potentially depressed prices "
                        "to fund claims â€” likely incurring losses and harming the balance sheet", True,
                        "Correct. Insufficient cash forces fire-sale asset liquidations, "
                        "destroying value and potentially threatening solvency."),
                       ("Wait â€” claims don't all arrive at once so cash is sufficient", False,
                        "In a catastrophe, claims arrive rapidly and simultaneously. "
                        "Insufficient liquidity is a serious solvency risk."),
                       ]),
        ],
    )

    c2 = _concept(m1_id, 2,
        "Bonds: Characteristics, Issuers, and Credit Ratings",
        "Describe bond characteristics, types of issuers, and the credit rating system.",
        "A bond is a loan from the investor to the issuer. The issuer promises to pay regular "
        "interest (coupon) and return the principal at maturity. Bonds are the dominant asset "
        "class in insurance portfolios because their predictable cash flows match insurance "
        "liabilities. Credit ratings (AAA to D) assess default probability.",
        "Pacific Mutual Life buys a $100M, 10-year Boeing corporate bond with a 4% coupon. "
        "Boeing pays $4M per year in interest, then repays $100M at maturity. If Boeing is "
        "downgraded from A to BBB, the bond's price falls â€” increasing Pacific Mutual's paper loss.",
        [
            "Bond = loan: investor lends money to issuer (government, corporation, municipality)",
            "Coupon rate: annual interest payment as % of face value",
            "Maturity: date when principal is repaid",
            "Credit rating: AAA (safest) â†’ D (default); measures default probability",
            "Higher credit risk = higher yield (return) demanded by investors",
        ],
        [
            "Confusing coupon rate (contractual interest rate) with current yield (market-based rate)",
            "Assuming all bonds have the same risk â€” sovereign bonds differ greatly from high-yield corporate bonds",
        ],
        [
            _intro("The Engine of Insurance Portfolios",
                   "Bonds are not exciting â€” but they power the insurance industry. "
                   "Life insurers hold trillions in bonds because bonds do something "
                   "stocks cannot: promise specific, predictable payments at specific times. "
                   "Let's understand every dimension of bonds."),
            _teach("Bond Characteristics",
                   "A bond is a debt instrument: the issuer borrows money from the investor "
                   "and promises two things: (1) periodic interest payments called coupons, "
                   "and (2) repayment of the principal (face value or par value) at maturity. "
                   "The coupon rate is the annual interest rate expressed as a percentage of "
                   "face value. For example, a $1,000 bond with a 5% coupon pays $50 per year. "
                   "Maturity is when the principal is returned â€” ranging from days (T-bills) "
                   "to 30+ years (long-term government bonds). The yield is the actual "
                   "return an investor earns, which changes as the bond's market price changes.",
                   [
                       "Face value (par): the principal amount ($1,000 is standard)",
                       "Coupon rate: stated annual interest as % of face value",
                       "Maturity date: when principal is repaid to investor",
                       "Yield: actual return based on current market price (not face value)",
                       "Price and yield move in OPPOSITE directions â€” key exam concept",
                   ]),
            _teach("Bond Issuers and Credit Ratings",
                   "Bonds are issued by three main categories: governments (sovereign and "
                   "municipal), corporations, and agencies. Government bonds (U.S. Treasuries) "
                   "are considered risk-free for default purposes. Municipal bonds are issued "
                   "by state/local governments and often carry tax advantages. Corporate bonds "
                   "carry credit risk â€” the possibility that the company cannot repay. "
                   "Credit rating agencies (Moody's, S&P, Fitch) assess credit quality: "
                   "AAA/Aaa is the highest (near risk-free); BBB/Baa is the lowest investment-grade; "
                   "BB/Ba and below are high-yield (junk) bonds with significant default risk. "
                   "Insurance regulations typically limit insurer holdings to investment-grade bonds.",
                   [
                       "U.S. Treasuries: default-risk free, backed by federal government",
                       "Municipal bonds: state/local, often tax-exempt interest",
                       "Corporate bonds: higher yield, higher credit risk",
                       "Investment grade: AAA, AA, A, BBB (Moody's: Aaa, Aa, A, Baa)",
                       "High yield (junk): BB and below â€” significant default risk",
                       "Insurers: usually limited to investment-grade by regulation",
                   ]),
            _example("Boeing Bond at Pacific Mutual Life",
                     "Pacific Mutual Life invests $100 million in Boeing corporate bonds: "
                     "10-year maturity, 4% coupon, S&P rating of A (investment grade). Each "
                     "year, Boeing pays $4 million in coupon interest to Pacific Mutual. At "
                     "maturity in 2034, Boeing repays the $100 million principal. In 2026, "
                     "Boeing faces production problems. S&P downgrades Boeing from A to BBB. "
                     "Immediately, the bond's market price drops from $100M to $94M as "
                     "investors demand higher yields to compensate for increased risk. "
                     "Pacific Mutual's portfolio shows an unrealized $6M loss â€” though if "
                     "they hold to maturity and Boeing doesn't default, they still receive "
                     "all coupons and full principal.",
                     "Credit downgrades cause immediate price losses even without actual default â€” "
                     "credit quality must be monitored continuously."),
            _flash("When bond prices fall, what happens to bond yields?",
                   "Yields RISE. Price and yield move in opposite directions â€” "
                   "this is the most fundamental bond relationship."),
            _mcq("A $1,000 bond has a coupon rate of 6%. What is the annual coupon payment?",
                 ["$6", "$600", "$60", "$6,000"],
                 2,
                 "$1,000 Ã— 6% = $60 per year in coupon payments to the bondholder."),
            _mcq("Which bond issuer is considered to have the LOWEST credit risk?",
                 ["A start-up company rated CCC",
                  "A municipality in financial distress",
                  "The U.S. Federal Government (U.S. Treasuries)",
                  "A high-yield corporate bond"],
                 2,
                 "U.S. Treasury bonds are backed by the full faith and credit of the U.S. "
                 "government â€” widely considered the benchmark risk-free asset."),
            _mcq("A bond is rated BB by S&P. What does this mean?",
                 ["It is investment-grade and suitable for most insurance portfolios",
                  "It is the highest possible credit rating",
                  "It is below investment-grade (high-yield/junk) with significant default risk",
                  "It is a government bond with no default risk"],
                 2,
                 "BB is below the BBB investment-grade threshold. These 'high-yield' or "
                 "'junk' bonds offer higher returns but carry significant default risk â€” "
                 "most insurance regulators restrict or prohibit large holdings."),
            _mcq("A $100M bond portfolio loses value when interest rates rise from 3% to 5%. "
                 "Why did the portfolio value decrease?",
                 ["Higher interest rates mean the government stopped paying coupons",
                  "New bonds now offer 5% yields, making existing 3% bonds less attractive â€” "
                  "their price falls to make their yield competitive",
                  "The issuer defaulted on the bonds",
                  "Higher interest rates reduce bond coupon payments"],
                 1,
                 "When rates rise, newly issued bonds offer higher yields. Existing lower-yield "
                 "bonds must fall in price to offer a comparable yield â€” price/yield move inversely."),
            _mcq("COMMON MISTAKE: An analyst says a BBB-rated bond is 'junk.' Is this correct?",
                 ["Yes â€” anything below AAA is junk",
                  "No â€” BBB is the lowest investment-grade rating, not junk. BB and below is high-yield/junk",
                  "Yes â€” BBB bonds always default",
                  "No â€” BBB is actually the highest rating"],
                 1,
                 "BBB (Baa) is investment grade â€” the minimum typically required for insurer "
                 "portfolios. Junk/high-yield begins at BB (Ba) and below."),
            _scenario("Your insurance company holds $500M in corporate bonds rated A by Moody's. "
                      "Moody's just downgraded all of them to Ba1 (high-yield/junk). Your "
                      "regulator requires all bond holdings to be investment-grade.",
                      "What action must you take?",
                      [("Do nothing â€” the coupons still get paid",
                        False,
                        "The downgrade below investment grade violates your regulatory requirement. "
                        "You must act regardless of whether coupons are still being paid."),
                       ("Sell the downgraded bonds and reinvest in investment-grade bonds "
                        "to comply with regulatory requirements",
                        True,
                        "Correct. Regulatory investment limits are mandatory. A downgrade to "
                        "junk requires divestiture to maintain compliance."),
                       ("Wait until the next audit to address it",
                        False,
                        "Regulatory violations cannot be deferred. Prompt action is required "
                        "to avoid regulatory penalties and solvency concerns."),
                       ]),
        ],
    )

    m1["concepts"] = [c1, c2]

    # â”€â”€ Module 2: Equity & Real Estate â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    m2_id = _id()
    m2 = {"id": m2_id, "chapter_id": ch_id, "order": 2, "title": "Equity and Real Estate"}

    c3 = _concept(m2_id, 1,
        "Stocks: Common vs. Preferred and Dividends",
        "Distinguish common from preferred stock and explain the role of dividends in insurer portfolios.",
        "Stocks represent ownership in a company. Common stockholders vote and receive dividends "
        "but are last to be paid in bankruptcy. Preferred stockholders receive fixed dividends "
        "before common holders and have priority in liquidation â€” making preferred stock more "
        "bond-like. Insurers use preferred stocks for their predictable dividends.",
        "MassMutual holds preferred shares in major utilities. When the utility pays its $5/share "
        "annual preferred dividend, MassMutual receives a predictable income stream similar to "
        "bond coupons â€” but with the tax advantage that 70% of dividends received are "
        "excluded from corporate income tax (the dividends-received deduction).",
        [
            "Common stock: ownership + voting rights + residual claim (last in bankruptcy)",
            "Preferred stock: fixed dividend + priority over common + no/limited voting rights",
            "Dividends: periodic cash payments to shareholders from company profits",
            "Insurers prefer preferred stock for its bond-like income stream",
            "Dividends-received deduction: 70%+ of inter-corporate dividends are tax-exempt",
        ],
        [
            "Assuming preferred stock is always 'better' â€” common stock has growth potential preferred lacks",
            "Forgetting that preferred dividends are not guaranteed like bond coupons",
        ],
        [
            _intro("Owning a Piece of the Business",
                   "Bonds are loans. Stocks are ownership. When you buy a stock, you become "
                   "a part-owner of the company â€” sharing in its profits through dividends "
                   "and growth. Let's explore how stocks fit into insurance portfolios."),
            _teach("Common Stock vs. Preferred Stock",
                   "Common stock represents basic ownership of a corporation. Common stockholders "
                   "vote on major decisions (electing the board, approving mergers) and receive "
                   "dividends when declared by the board. However, in bankruptcy, common "
                   "stockholders are paid last â€” after bondholders and preferred stockholders â€” "
                   "often receiving nothing. Preferred stock is a hybrid between bonds and "
                   "equity. Preferred stockholders receive a fixed dividend (stated as a "
                   "percentage of par value or a fixed dollar amount) before common stockholders "
                   "receive anything. They have priority over common stockholders in liquidation "
                   "but have limited or no voting rights. The fixed dividend makes preferred "
                   "stock attractive to insurers seeking predictable income.",
                   [
                       "Common: voting rights, variable dividends, growth potential, last claim",
                       "Preferred: fixed dividends, priority over common, limited voting",
                       "Preferred dividends must be paid before common dividends",
                       "In liquidation: bondholders â†’ preferred stockholders â†’ common stockholders",
                   ]),
            _teach("Dividends and the Insurance Portfolio",
                   "Dividends are cash payments from a company to its shareholders, typically "
                   "paid quarterly. For common stock, dividends are declared by the board and "
                   "can be increased, cut, or eliminated. For preferred stock, the dividend is "
                   "typically fixed and must be paid before common dividends. Insurers value "
                   "preferred stock because the fixed dividend functions like bond coupon income "
                   "while maintaining the legal status of equity. A key tax advantage: "
                   "corporations receiving dividends from other U.S. corporations can exclude "
                   "70-100% of those dividends from taxable income (the dividends-received "
                   "deduction), making dividend income especially valuable for corporate investors.",
                   [
                       "Common dividends: variable, declared by board, can be cut",
                       "Preferred dividends: fixed, must be paid before common",
                       "Dividends-received deduction (DRD): 70-100% tax exclusion for inter-corp dividends",
                       "DRD makes dividend income tax-advantaged for insurance companies",
                   ]),
            _example("MassMutual's Utility Preferred Strategy",
                     "MassMutual Investment Management holds $2 billion in preferred shares "
                     "of major U.S. utility companies. Duke Energy's preferred shares pay a "
                     "fixed $6/share annual dividend. MassMutual receives these dividends "
                     "predictably each quarter. Because of the dividends-received deduction, "
                     "70% of this income is tax-exempt â€” effectively reducing MassMutual's "
                     "tax burden on $1.4 billion of that $2 billion. Meanwhile, common "
                     "stockholders in Duke Energy saw their dividend cut during a tough year, "
                     "but MassMutual's preferred dividend was protected by its priority status.",
                     "Preferred stock combines bond-like income predictability with equity's "
                     "tax advantages â€” ideal for tax-sensitive institutional investors."),
            _flash("What is the key advantage of preferred stock for an insurance company investor?",
                   "Fixed dividends with priority over common stock (paid first) and the "
                   "dividends-received deduction that makes the income partially tax-exempt."),
            _mcq("In a company's liquidation, which claimant is paid LAST?",
                 ["Senior bondholders", "Preferred stockholders",
                  "Junior bondholders", "Common stockholders"],
                 3,
                 "Common stockholders are residual claimants â€” they receive whatever is left "
                 "after all creditors (bondholders) and preferred stockholders are paid, "
                 "which in bankruptcy is often nothing."),
            _mcq("Why might an insurance company prefer preferred stock over common stock?",
                 ["Preferred stock always appreciates more in price",
                  "Preferred stock offers fixed dividends and priority in liquidation â€” "
                  "providing more predictable income similar to bond coupons",
                  "Preferred stockholders have stronger voting rights",
                  "Preferred stock is not subject to any market price risk"],
                 1,
                 "Preferred stock's fixed dividends and liquidation priority make it more "
                 "predictable than common stock â€” better suited to insurer liability matching."),
            _mcq("A company has 1,000 preferred shares outstanding with a $100 par value "
                 "and a 5% preferred dividend rate. What is the total annual preferred dividend?",
                 ["$500", "$5,000", "$50,000", "$500,000"],
                 1,
                 "1,000 shares Ã— $100 par Ã— 5% = $5,000 total annual preferred dividend."),
            _mcq("What is the dividends-received deduction?",
                 ["A deduction insurance companies take when paying dividends to policyholders",
                  "A corporate tax provision allowing companies to exclude 70-100% of "
                  "dividends received from other U.S. corporations from taxable income",
                  "A penalty for companies that fail to pay dividends",
                  "A deduction for dividends paid to preferred shareholders"],
                 1,
                 "The DRD allows corporations receiving dividends from other U.S. corporations "
                 "to exclude 70-100% of that income from federal taxes â€” highly valuable for insurers."),
            _mcq("COMMON MISTAKE: A student assumes preferred stock dividends are as guaranteed "
                 "as bond coupons. Why is this incorrect?",
                 ["They are exactly the same â€” both are legally required payments",
                  "Preferred dividends can be suspended by the board without triggering bankruptcy, "
                  "unlike bond coupons which are contractual obligations",
                  "Bond coupons can also be suspended without penalty",
                  "Preferred dividends are actually more guaranteed than bond coupons"],
                 1,
                 "Bond coupons are contractual â€” missing one is a default event. Preferred "
                 "dividends are discretionary; while they must be paid before common dividends, "
                 "they can be omitted without triggering bankruptcy."),
            _scenario("Nationwide Insurance must choose between investing $50M in 5% preferred "
                      "shares of a utility company or 5% corporate bonds from the same company. "
                      "The insurer's tax rate is 21%.",
                      "Which investment is likely MORE tax-efficient for Nationwide?",
                      [("The corporate bonds â€” bond coupons are always better", False,
                        "Bond interest is fully taxable as ordinary income at 21%. The "
                        "dividends-received deduction makes preferred stock income more tax-efficient."),
                       ("The preferred shares â€” the dividends-received deduction makes "
                        "most of the dividend income tax-exempt", True,
                        "Correct. With a 70% DRD, only 30% of the preferred dividends are "
                        "taxable â€” making the effective tax rate approximately 6.3% vs. 21% "
                        "on bond interest. Preferred is significantly more tax-efficient."),
                       ("It makes no difference â€” both earn 5%", False,
                        "The after-tax return differs significantly due to the DRD. Tax "
                        "efficiency is critical for institutional investors."),
                       ]),
        ],
    )

    c4 = _concept(m2_id, 2,
        "Real Estate, Mortgage Loans, and REITs",
        "Describe real estate investment types, mortgage loans, appraisals, and REITs available to insurers.",
        "Real estate is a major asset class for insurance companies â€” they invest through "
        "direct ownership, mortgage loans, and Real Estate Investment Trusts (REITs). "
        "Direct real estate provides rental income and appreciation. Mortgage loans earn "
        "interest income. REITs offer liquid, diversified real estate exposure.",
        "Prudential Real Estate Investors manages $100 billion in real estate globally "
        "for insurance and pension clients â€” office buildings, apartments, logistics warehouses, "
        "and retail centers â€” earning rental income to fund long-term insurance liabilities.",
        [
            "Real estate types: office, retail, industrial, multifamily (residential), hotel",
            "Direct ownership: rental income + appreciation, but illiquid and management-intensive",
            "Mortgage loans: insurers act as lender, earning interest income",
            "REITs: liquid real estate exposure through publicly-traded companies",
            "Appraisals: professional valuation required to determine fair market value",
        ],
        [
            "Assuming real estate is always more profitable than bonds â€” real estate has liquidity risk and management costs",
            "Confusing mortgage loans (insurer as lender) with buying real estate (insurer as owner)",
        ],
        [
            _intro("Bricks, Mortar, and Insurance Dollars",
                   "The skylines of major cities are partly funded by insurance company investments. "
                   "Real estate offers income, inflation protection, and diversification â€” "
                   "but comes with unique challenges. Let's explore how insurers invest in real estate."),
            _teach("Types of Real Estate and Direct Ownership",
                   "Insurers invest in commercial real estate across five main property types: "
                   "office (corporate headquarters and business parks), retail (shopping centers "
                   "and malls), industrial (warehouses, logistics, manufacturing), multifamily "
                   "(apartment complexes), and hotel (hospitality properties). Direct ownership "
                   "means the insurer actually owns the building and receives rental income from "
                   "tenants. Real estate appraisals â€” professional valuations conducted by "
                   "licensed appraisers â€” are required to establish fair market value for "
                   "accounting, regulatory, and transaction purposes. Direct real estate offers "
                   "strong returns and inflation protection but is illiquid (cannot be sold "
                   "quickly), management-intensive, and geographically concentrated.",
                   [
                       "Office: corporate tenants, long-term leases",
                       "Retail: shopping centers; highly affected by e-commerce trends",
                       "Industrial/logistics: warehouses; grew dramatically with e-commerce",
                       "Multifamily: apartments; strong demand from housing shortage",
                       "Appraisal: professional value assessment required for reporting",
                   ]),
            _teach("Mortgage Loans and REITs",
                   "Rather than owning property, insurance companies also invest in real estate "
                   "as lenders by making mortgage loans. The borrower (often a property developer) "
                   "pledges real estate as collateral; the insurer earns interest income. If the "
                   "borrower defaults, the insurer can foreclose and take ownership of the property. "
                   "Real Estate Investment Trusts (REITs) are companies that own portfolios of "
                   "income-producing real estate. They are publicly traded like stocks, providing "
                   "much greater liquidity than direct ownership. By law, REITs must distribute "
                   "at least 90% of taxable income to shareholders as dividends â€” making them "
                   "income-generating. REITs allow insurers to access real estate returns "
                   "without the management burden of direct ownership.",
                   [
                       "Mortgage loans: insurer as lender, earns interest, holds property as collateral",
                       "Commercial mortgage: typically $5M-$500M+ for income-producing properties",
                       "REIT: publicly-traded real estate company, liquid, 90% income distributed",
                       "REIT types: equity REITs (own properties), mortgage REITs (hold mortgages)",
                   ]),
            _example("Teachers Insurance Builds a Skyscraper",
                     "Teachers Insurance and Annuity Association (TIAA) decides to invest $500M "
                     "in a portfolio of Class-A office buildings in New York and Chicago. TIAA "
                     "acquires the buildings directly, becoming the landlord to Goldman Sachs and "
                     "Deloitte as anchor tenants on 15-year leases. Annual rental income: $30M "
                     "(6% cap rate). In parallel, TIAA makes a $100M commercial mortgage loan "
                     "to a Dallas developer at 5.5% interest, secured by a 50-story tower. "
                     "And TIAA holds $50M in Prologis REIT shares (industrial/warehouse "
                     "properties), receiving quarterly dividends and maintaining liquidity. "
                     "This three-pronged real estate approach â€” direct ownership, mortgage "
                     "lending, and REITs â€” provides income, appreciation, and liquidity.",
                     "Insurance companies use multiple real estate approaches to balance "
                     "return, liquidity, and management burden."),
            _flash("What is the minimum percentage of taxable income a REIT must distribute to shareholders?",
                   "90% â€” REITs must distribute at least 90% of taxable income as dividends "
                   "to maintain their REIT status and tax benefits."),
            _mcq("An insurance company makes a $200M loan to a hotel developer, secured by "
                 "the hotel building. How is this investment classified?",
                 ["A REIT investment",
                  "Direct real estate ownership",
                  "A commercial mortgage loan",
                  "A preferred stock investment"],
                 2,
                 "The insurer is acting as a lender (not an owner) â€” this is a commercial "
                 "mortgage loan with the hotel as collateral."),
            _mcq("Why might an insurer prefer a REIT over direct real estate ownership?",
                 ["REITs always earn higher returns than direct ownership",
                  "REITs are publicly traded, providing liquidity that direct real estate lacks",
                  "REITs do not require any capital investment",
                  "REITs are exempt from all taxes"],
                 1,
                 "REITs trade on stock exchanges and can be sold quickly. Direct real estate "
                 "can take months or years to sell â€” a significant liquidity disadvantage."),
            _mcq("What is the purpose of a real estate appraisal?",
                 ["To determine the property's rental income potential only",
                  "To establish the property's fair market value for accounting, regulatory, and transaction purposes",
                  "To calculate the owner's property tax bill",
                  "To approve a mortgage application"],
                 1,
                 "Appraisals establish fair market value â€” required for financial reporting, "
                 "regulatory capital calculations, and buy/sell transactions."),
            _mcq("A REIT earns $100M in taxable income. How much must it distribute as dividends?",
                 ["At least $50M", "At least $70M", "At least $90M", "100% of income"],
                 2,
                 "REITs must distribute at least 90% of taxable income â€” so at least $90M "
                 "of the $100M must be paid out as dividends to shareholders."),
            _mcq("COMMON MISTAKE: An analyst says commercial mortgage loans are the same as "
                 "direct real estate ownership because both involve real estate. What key "
                 "difference are they missing?",
                 ["They are the same thing",
                  "In a mortgage loan the insurer is a LENDER earning interest; in direct ownership "
                  "the insurer is an OWNER earning rent â€” different risk, return, and legal position",
                  "Only direct ownership generates income",
                  "Mortgage loans have higher returns than direct ownership in all scenarios"],
                 1,
                 "Lender vs. owner is a critical distinction. In a mortgage loan, the insurer "
                 "earns fixed interest and has collateral protection but does not share in "
                 "appreciation. In direct ownership, the insurer earns rent AND appreciation "
                 "but bears all operating risks."),
            _scenario("Your insurance company wants real estate exposure but has strict liquidity "
                      "requirements â€” you must be able to sell any investment within 5 business days "
                      "if needed.",
                      "Which real estate investment best meets this requirement?",
                      [("Direct ownership of office buildings in downtown Chicago", False,
                        "Direct real estate can take 6-18 months to sell. This violates "
                        "the 5-day liquidity requirement."),
                       ("Publicly-traded REIT shares", True,
                        "Correct. REITs trade on public exchanges and can be sold within "
                        "one business day â€” meeting the 5-day liquidity requirement easily."),
                       ("A $500M commercial mortgage loan to a developer", False,
                        "Mortgage loans are illiquid â€” they typically cannot be sold quickly "
                        "without a significant discount, especially in stressed markets."),
                       ]),
        ],
    )

    m2["concepts"] = [c3, c4]
    ch["modules"] = [m1, m2]
    return ch


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# CHAPTER 3 â€” Advanced Investment Vehicles and Capital Markets
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def _build_ch3(course_id):
    ch_id = _id()
    ch = {
        "id": ch_id, "course_id": course_id, "order": 3,
        "title": "Advanced Investment Vehicles and Capital Markets",
        "description": "Master structured securities, derivatives, alternative investments, and capital market mechanics.",
    }

    # â”€â”€ Module 1: Structured Products & Derivatives â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    m1_id = _id()
    m1 = {"id": m1_id, "chapter_id": ch_id, "order": 1, "title": "Structured Securities and Derivatives"}

    c1 = _concept(m1_id, 1,
        "Securitization, ABS, and Mortgage-Backed Securities",
        "Explain the securitization process and distinguish ABS from MBS.",
        "Securitization is the process of pooling financial assets (like mortgages or auto loans) "
        "and issuing securities backed by those pools. The result is Asset-Backed Securities (ABS) "
        "â€” or if backed specifically by mortgages, Mortgage-Backed Securities (MBS). These give "
        "insurers access to diversified pools of loans with predictable income.",
        "Fannie Mae pools 10,000 individual home mortgages totaling $2 billion and issues MBS "
        "to institutional investors like TIAA. TIAA receives monthly principal and interest "
        "payments from the mortgage pool â€” diversified across thousands of homeowners "
        "rather than dependent on a single borrower.",
        [
            "Securitization: pooling assets â†’ issuing securities backed by the pool",
            "ABS: backed by auto loans, credit cards, student loans, etc.",
            "MBS: specifically backed by mortgage loans on real property",
            "Tranches: MBS split into risk layers â€” senior gets paid first, junior absorbs losses first",
            "Prepayment risk: borrowers repay early, disrupting expected cash flows",
        ],
        [
            "Assuming MBS are risk-free because they are 'backed by houses' â€” 2008 crisis showed otherwise",
            "Confusing the originator (bank making loans) with the investor (insurer buying MBS)",
        ],
        [
            _intro("From Mortgages to Markets",
                   "How does your monthly mortgage payment end up as an investment in a "
                   "pension fund's portfolio? Through securitization â€” one of the most "
                   "important financial innovations of the 20th century. Let's trace the path."),
            _teach("The Securitization Process",
                   "Securitization converts illiquid individual loans into tradeable securities. "
                   "Here is how it works step by step: (1) Origination â€” a bank makes thousands "
                   "of loans (mortgages, auto loans, credit cards). (2) Pooling â€” the bank sells "
                   "these loans to a Special Purpose Vehicle (SPV), a legally separate entity. "
                   "(3) Structuring â€” the SPV issues securities (ABS or MBS) backed by the pool's "
                   "cash flows. (4) Tranching â€” the securities are divided into tranches: senior "
                   "tranches receive payments first and carry the lowest risk; junior/equity "
                   "tranches absorb losses first but earn higher returns. (5) Distribution â€” "
                   "institutional investors like insurance companies buy the tranches.",
                   [
                       "Step 1: Bank originates many individual loans",
                       "Step 2: Loans sold to Special Purpose Vehicle (legally bankruptcy-remote)",
                       "Step 3: SPV issues ABS/MBS backed by loan cash flows",
                       "Step 4: Tranching creates different risk/return profiles",
                       "Step 5: Institutional investors buy according to risk appetite",
                   ]),
            _teach("ABS vs. MBS and Key Risks",
                   "Asset-Backed Securities (ABS) are backed by pools of non-mortgage assets: "
                   "auto loans, credit card receivables, student loans, equipment leases. "
                   "Mortgage-Backed Securities (MBS) are backed specifically by pools of mortgage "
                   "loans and come in two forms: Agency MBS (issued/guaranteed by Fannie Mae, "
                   "Freddie Mac, or Ginnie Mae â€” very low credit risk) and Non-Agency/Private-Label "
                   "MBS (no government guarantee â€” higher credit risk). Key risks: credit risk "
                   "(borrowers default), prepayment risk (borrowers refinance early, returning "
                   "principal sooner than expected, disrupting the insurer's income stream), "
                   "and extension risk (in rising rate environments, borrowers prepay less, "
                   "keeping the insurer locked in lower-rate assets).",
                   [
                       "ABS: auto loans, credit cards, student loans â€” diverse consumer assets",
                       "Agency MBS: Fannie/Freddie/Ginnie guarantee â€” near-sovereign credit quality",
                       "Non-Agency MBS: no guarantee â€” higher yield, higher credit risk",
                       "Prepayment risk: early repayment disrupts expected income timing",
                       "Extension risk: rising rates cause slower prepayment, extending duration",
                   ]),
            _example("The 2008 Crisis: When MBS Went Wrong",
                     "In 2006-2007, Wall Street banks securitized millions of subprime "
                     "mortgages â€” loans made to borrowers with poor credit â€” into Non-Agency "
                     "MBS rated AAA by rating agencies. Insurance companies bought billions "
                     "in these 'safe' instruments. When U.S. home prices fell 30% in 2008, "
                     "millions of homeowners defaulted simultaneously. The mortgage pools "
                     "failed to generate the promised cash flows. The 'senior' tranches â€” "
                     "supposedly the safest â€” lost 30-60% of their value. AIG Financial "
                     "Products had written credit insurance on $500 billion of these "
                     "securities and required a $182 billion government bailout to survive.",
                     "Securitization spreads risk â€” but if the underlying loans are all "
                     "correlated (all failing simultaneously), diversification fails completely."),
            _flash("What is 'prepayment risk' in a Mortgage-Backed Security?",
                   "The risk that homeowners repay their mortgages early (when rates fall and "
                   "they refinance), returning principal to investors sooner than expected "
                   "and forcing reinvestment at lower rates."),
            _mcq("Which of the following is an example of an Asset-Backed Security (ABS)?",
                 ["A U.S. Treasury bond",
                  "A security backed by a pool of auto loan receivables",
                  "A share of common stock in Ford Motor Company",
                  "A direct investment in commercial real estate"],
                 1,
                 "ABS are backed by pools of non-mortgage financial assets like auto loans, "
                 "credit card receivables, or student loans â€” not mortgages (that's MBS)."),
            _mcq("What is the role of a Special Purpose Vehicle (SPV) in securitization?",
                 ["To make the original loans to borrowers",
                  "To hold the pool of assets and issue securities backed by those assets, "
                  "legally isolated from the originating bank's bankruptcy risk",
                  "To provide government guarantees on the securities",
                  "To purchase tranches in the securitization"],
                 1,
                 "The SPV is a bankruptcy-remote entity that legally owns the loans and "
                 "issues ABS/MBS. If the originating bank fails, the SPV (and investors) "
                 "are protected from that bankruptcy."),
            _mcq("Which MBS type carries the LOWEST credit risk?",
                 ["Non-Agency (private-label) MBS with no government guarantee",
                  "Subprime MBS backed by borrowers with poor credit",
                  "Agency MBS guaranteed by Fannie Mae, Freddie Mac, or Ginnie Mae",
                  "Equity tranches that absorb first losses"],
                 2,
                 "Agency MBS benefit from explicit or implicit U.S. government guarantees â€” "
                 "making their credit risk near-sovereign level."),
            _mcq("Interest rates fall from 7% to 4%. Homeowners rush to refinance. "
                 "What risk does an MBS investor face?",
                 ["Extension risk â€” the MBS duration extends beyond expectations",
                  "Prepayment risk â€” principal is returned early, forcing reinvestment at lower rates",
                  "Credit risk â€” homeowners default due to lower rates",
                  "Liquidity risk â€” the MBS cannot be sold"],
                 1,
                 "When rates fall, homeowners refinance (prepay mortgages). MBS investors "
                 "receive their principal back early and must reinvest at now-lower rates."),
            _mcq("COMMON MISTAKE: An analyst argues MBS backed by residential mortgages are "
                 "always safe because 'housing prices always go up.' Why is this wrong?",
                 ["It is correct â€” real estate values only increase",
                  "Housing prices can and do fall â€” the 2008 crisis showed that correlated "
                  "mortgage defaults can devastate MBS values regardless of collateral quality",
                  "MBS are backed by the government so price doesn't matter",
                  "Only non-agency MBS can lose value"],
                 1,
                 "The 2008 financial crisis demonstrated that housing prices can fall "
                 "significantly. Correlated defaults can overwhelm even senior MBS tranches."),
            _scenario("Your insurance company holds $1 billion in Agency MBS (Fannie Mae). "
                      "The Federal Reserve raises interest rates from 3% to 6.5%. Mortgage "
                      "prepayments slow dramatically as homeowners keep their low-rate mortgages.",
                      "Which risk has just materialized?",
                      [("Prepayment risk â€” homeowners are repaying too quickly", False,
                        "Prepayment risk occurs when rates FALL. Rising rates slow prepayments."),
                       ("Extension risk â€” the effective duration of the MBS extends as "
                        "prepayments slow, locking the insurer into below-market rates", True,
                        "Correct. Extension risk materializes when rising rates cause homeowners "
                        "to keep existing low-rate mortgages, extending the MBS duration "
                        "and trapping investors in below-market yields."),
                       ("Credit risk â€” Fannie Mae is about to default", False,
                        "Agency MBS have U.S. government support. Rate changes affect "
                        "prepayment behavior, not agency credit quality."),
                       ]),
        ],
    )

    c2 = _concept(m1_id, 2,
        "Derivatives: Options, Swaps, Futures, and Forwards",
        "Define derivatives and explain how insurers use options, swaps, futures, and forwards.",
        "Derivatives are financial contracts whose value depends on ('derives from') an underlying "
        "asset like a bond, interest rate, or stock index. Insurers use derivatives primarily "
        "to hedge (reduce) risk â€” not to speculate. Common derivatives include options (right "
        "but not obligation to buy/sell), swaps (exchange of cash flows), futures (standardized "
        "contracts to buy/sell at future price), and forwards (customized future contracts).",
        "TIAA uses interest rate swaps to convert $5 billion of variable-rate bonds into "
        "fixed-rate equivalents, reducing the risk that falling rates will reduce their investment "
        "income. This hedging protects against interest rate volatility without changing the "
        "underlying bond holdings.",
        [
            "Derivatives derive value from an underlying asset (bond, rate, stock, commodity)",
            "Options: right but NOT obligation to buy (call) or sell (put) at a set price",
            "Swaps: exchange cash flow streams â€” most common: interest rate swaps (fixed for floating)",
            "Futures: standardized, exchange-traded contracts for future delivery",
            "Forwards: customized, over-the-counter contracts (same concept as futures but tailored)",
            "Insurers use derivatives to HEDGE risk, not to speculate",
        ],
        [
            "Assuming all derivatives are speculative â€” insurers use them defensively to hedge risk",
            "Confusing the 'right to buy' (call option) with the 'obligation to buy' (futures/forwards)",
        ],
        [
            _intro("Financial Insurance for Investments",
                   "Derivatives sound complex but the concept is simple: they are financial "
                   "tools to manage risk. Just as you buy car insurance to protect against "
                   "an accident, an insurer buys derivatives to protect against interest rate "
                   "swings or market crashes. Let's demystify them."),
            _teach("What Are Derivatives and Why Do Insurers Use Them?",
                   "A derivative is a contract between two parties whose value depends on the "
                   "performance of an underlying asset, rate, or index. Because they are "
                   "contracts (not actual asset purchases), derivatives can be structured to "
                   "provide precise protection against specific risks with relatively low upfront "
                   "cost. Insurance companies use derivatives almost exclusively for hedging â€” "
                   "reducing or eliminating specific portfolio risks. For example, if an insurer "
                   "fears that falling interest rates will hurt its bond portfolio income, it "
                   "can use interest rate derivatives to lock in its income level.",
                   [
                       "Value derived from underlying asset, rate, or index",
                       "Can hedge interest rate risk, equity market risk, credit risk, currency risk",
                       "Low upfront cost relative to the protection provided",
                       "Insurers prohibited from using derivatives to SPECULATE â€” hedging only",
                   ]),
            _teach("Options, Swaps, Futures, and Forwards",
                   "Options give the buyer the RIGHT (but not the obligation) to buy (call option) "
                   "or sell (put option) an asset at a predetermined price (strike price) before "
                   "or on a specific date. The buyer pays a premium for this right. "
                   "Swaps are agreements to exchange cash flow streams â€” the most common being "
                   "an interest rate swap where one party pays fixed interest in exchange for "
                   "receiving variable (floating) rate interest. "
                   "Futures are standardized, exchange-traded contracts obligating both parties "
                   "to buy/sell an asset at a specified price on a future date. "
                   "Forwards are like futures but customized (over-the-counter) â€” negotiated "
                   "directly between counterparties with flexible terms.",
                   [
                       "Call option: right to BUY at strike price (buyer profits if price rises above strike)",
                       "Put option: right to SELL at strike price (buyer profits if price falls below strike)",
                       "Interest rate swap: fixed payer receives floating; floating payer receives fixed",
                       "Futures: standardized, exchange-traded, daily mark-to-market settlement",
                       "Forwards: customized, OTC, settled at contract expiry",
                   ]),
            _example("TIAA's Interest Rate Swap",
                     "TIAA holds $5 billion in floating-rate corporate bonds that pay LIBOR + 1.5%. "
                     "When the Federal Reserve cuts rates, LIBOR falls from 5% to 2%, reducing "
                     "TIAA's annual income by $150 million. To protect against this, TIAA enters "
                     "an interest rate swap with Goldman Sachs: TIAA pays floating (LIBOR + 1.5%) "
                     "to Goldman Sachs and receives a fixed 6.5% in return. Now TIAA's net "
                     "income is locked at 6.5% regardless of where rates move. Goldman Sachs "
                     "takes the other side â€” betting that rates will stay high. "
                     "When the Fed cuts rates to 2%, TIAA's swap saves $225M annually "
                     "while Goldman Sachs pays the difference.",
                     "Interest rate swaps allow insurers to convert rate uncertainty into "
                     "predictable fixed income â€” protecting their ability to fund future claims."),
            _flash("What is the key difference between an option and a futures contract?",
                   "An option gives the holder the RIGHT but not the obligation to transact. "
                   "A futures contract OBLIGATES both parties to transact at the agreed price."),
            _mcq("An insurer buys a put option on a stock index. What risk is it hedging against?",
                 ["The risk that interest rates will rise",
                  "The risk that the stock market will fall (declining equity portfolio values)",
                  "The risk that bond yields will increase",
                  "The risk of policyholder claims rising"],
                 1,
                 "A put option gives the right to SELL at the strike price. If the market "
                 "falls below the strike, the put gains value â€” offsetting equity portfolio losses."),
            _mcq("In an interest rate swap, the 'fixed-rate receiver' benefits when:",
                 ["Interest rates rise above the fixed rate",
                  "Interest rates fall below the fixed rate â€” they receive more than they would at market",
                  "The swap is cancelled early",
                  "The underlying bond defaults"],
                 1,
                 "The fixed-rate receiver gets a constant fixed payment regardless of market rates. "
                 "If rates fall, they are receiving above-market income â€” the swap has positive value."),
            _mcq("How does a forward contract differ from a futures contract?",
                 ["Forwards are exchange-traded; futures are over-the-counter",
                  "Forwards have no counterparty risk; futures do",
                  "Forwards are customized OTC contracts; futures are standardized and exchange-traded",
                  "Forwards can only be used by retail investors"],
                 2,
                 "Futures are standardized contracts traded on regulated exchanges. Forwards "
                 "are customized contracts negotiated OTC between specific counterparties."),
            _mcq("An insurance company is concerned about rising interest rates reducing "
                 "the value of its long-duration bond portfolio. Which derivative hedge is most appropriate?",
                 ["Buy call options on bonds",
                  "Enter a swap to pay fixed and receive floating interest rates",
                  "Buy equity futures",
                  "Buy put options on the U.S. dollar"],
                 1,
                 "Paying fixed/receiving floating in a swap benefits when rates rise. "
                 "When market rates rise, the floating rate payments received increase, "
                 "offsetting bond portfolio value losses."),
            _mcq("COMMON MISTAKE: A compliance officer claims all derivatives are speculative "
                 "and insurance companies shouldn't use them. Why is this incorrect?",
                 ["It is correct â€” regulators prohibit all insurer derivative use",
                  "Derivatives used for hedging REDUCE portfolio risk â€” regulators explicitly "
                  "permit (and often encourage) hedging derivatives for insurers",
                  "Only pension funds can use derivatives",
                  "All derivatives generate profit with no risk"],
                 1,
                 "Insurance regulators distinguish between speculative derivatives (prohibited) "
                 "and hedging derivatives (permitted/encouraged to manage portfolio risk)."),
            _scenario("Lincoln Benefit Life holds $10 billion in fixed-rate bonds yielding 5%. "
                      "The company has $9 billion in variable-rate policyholder liabilities. "
                      "If interest rates rise from 5% to 8%, policyholders will demand higher "
                      "returns and may surrender policies.",
                      "Which derivative strategy would best protect Lincoln against this risk?",
                      [("Buy call options on Treasury bonds", False,
                        "Call options on bonds profit when bond PRICES rise (rates fall). "
                        "This is the wrong direction for the risk being hedged."),
                       ("Enter an interest rate swap paying fixed, receiving floating â€” "
                        "profiting when rates rise to fund higher policyholder returns", True,
                        "Correct. Paying fixed/receiving floating profits as rates rise, "
                        "generating cash flows to fund increased policyholder obligations."),
                       ("Buy equity futures to generate higher returns", False,
                        "Equity futures don't hedge interest rate risk on liabilities. "
                        "This adds equity risk rather than hedging rate risk."),
                       ]),
        ],
    )

    m1["concepts"] = [c1, c2]

    # â”€â”€ Module 2: Alternative Investments & Market Infrastructure â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    m2_id = _id()
    m2 = {"id": m2_id, "chapter_id": ch_id, "order": 2, "title": "Alternative Investments and Capital Markets"}

    c3 = _concept(m2_id, 1,
        "Hedge Funds, Private Equity, and Infrastructure",
        "Describe alternative investment vehicles available to institutional investors.",
        "Alternative investments go beyond stocks and bonds â€” they include hedge funds "
        "(which use sophisticated strategies to generate returns in all markets), private equity "
        "(investing in non-publicly traded companies), and infrastructure (airports, toll roads, "
        "utilities). Insurers use these for diversification and higher returns but face "
        "significant liquidity constraints.",
        "The Ontario Teachers Pension Plan owns 100% of London Heathrow Airport, several "
        "toll highways in Chile, and the Birmingham Airport â€” earning predictable, "
        "inflation-linked returns over 50-year time horizons that match their pension liabilities perfectly.",
        [
            "Hedge funds: flexible strategies (long/short, macro, arbitrage) â€” seek absolute returns",
            "Private equity: invest in non-public companies through LBO, venture capital, growth equity",
            "Infrastructure: airports, highways, utilities â€” long-duration, inflation-linked income",
            "All alternatives: illiquid, complex, higher fees â€” suitable only for large institutions",
        ],
        [
            "Assuming hedge funds always make money â€” many hedge funds underperform or close",
            "Confusing private equity (buying companies) with public equity (buying stocks)",
        ],
        [
            _intro("Beyond Stocks and Bonds",
                   "The world's largest insurers don't just buy bonds and stocks. They own "
                   "airports, highways, and companies you've never heard of. Alternative "
                   "investments offer higher returns â€” but come with unique complexity "
                   "and illiquidity that most investors cannot handle."),
            _teach("Hedge Funds and Private Equity",
                   "Hedge funds are privately organized investment vehicles that employ "
                   "flexible, often complex strategies unavailable to traditional funds. "
                   "They may go long AND short (profiting from both rising and falling prices), "
                   "use leverage, trade globally, and employ quantitative algorithms. "
                   "The goal is 'absolute return' â€” making money regardless of market direction. "
                   "Private equity (PE) involves investing in companies that are not publicly traded. "
                   "PE firms typically buy companies using leverage (leveraged buyouts/LBOs), "
                   "improve operations over 3-7 years, then sell for a profit. Venture capital "
                   "is early-stage PE investing in startups. Growth equity invests in more "
                   "mature companies seeking expansion capital.",
                   [
                       "Hedge fund strategies: long/short equity, global macro, merger arbitrage, quant",
                       "'2 and 20' fee structure: 2% management fee + 20% of profits",
                       "LBO: acquiring a company with significant debt, improving it, then selling",
                       "Venture capital: early-stage startups â€” high risk, potential massive returns",
                       "PE liquidity: capital locked for 7-10 years in typical PE fund",
                   ]),
            _teach("Infrastructure Investments",
                   "Infrastructure assets include transportation (airports, toll roads, ports, "
                   "railways), utilities (water systems, electrical grids, pipelines), social "
                   "infrastructure (hospitals, schools, prisons), and communications "
                   "(cell towers, fiber networks). These assets share key characteristics "
                   "that make them attractive for insurance company portfolios: essential services "
                   "(demand is stable regardless of economic conditions), regulated or contracted "
                   "revenues (cash flows are predictable), long asset lives (30-100 years, "
                   "matching long-duration insurance liabilities), and inflation linkage (fees "
                   "often indexed to CPI, protecting real returns). The main drawback is "
                   "illiquidity â€” infrastructure assets cannot be sold quickly.",
                   [
                       "Essential services: airports, utilities â€” demand is inelastic",
                       "Stable, contracted or regulated revenue streams",
                       "Long asset life matches long-duration insurance liabilities",
                       "Often inflation-linked â€” protects real purchasing power",
                       "Illiquid: can take years to sell; suitable for long-horizon institutions",
                   ]),
            _example("Teachers Pension Buys Heathrow Airport",
                     "In 2019, the Ontario Teachers Pension Plan (OTPP) increased its stake in "
                     "London Heathrow Airport to 25%, investing Â£2.4 billion. Heathrow is "
                     "regulated by the UK Civil Aviation Authority, which sets the fees airlines "
                     "pay â€” providing predictable, regulated revenue. Fees are indexed to UK "
                     "inflation. OTPP expects to hold this investment for 20-30 years, matching "
                     "its obligations to pay pensions to Ontario teachers who retire in the "
                     "2030s-2040s. Annual regulated return: approximately 4-5% above inflation. "
                     "The investment earns stable, inflation-protected returns with near-zero "
                     "correlation to stock market movements.",
                     "Infrastructure's long duration, inflation linkage, and regulated returns "
                     "make it ideally suited to match long-term insurance and pension liabilities."),
            _flash("What makes infrastructure investments particularly attractive for insurers "
                   "with long-duration liabilities?",
                   "Long asset lives (30-100 years), stable regulated/contracted revenue, "
                   "and inflation linkage match perfectly with long-term insurance liabilities."),
            _mcq("Which alternative investment strategy involves buying companies with significant "
                 "borrowed money, improving them operationally, then selling them at a profit?",
                 ["Hedge fund long/short equity", "Leveraged Buyout (LBO) via private equity",
                  "Venture capital in startups", "Infrastructure investing"],
                 1,
                 "LBOs are the classic private equity strategy: acquire with leverage, "
                 "improve operations, repay debt with cash flow, exit at higher valuation."),
            _mcq("Why is infrastructure a good match for insurance company portfolios?",
                 ["Infrastructure always generates the highest absolute returns",
                  "Infrastructure provides stable, long-duration, inflation-linked income "
                  "that matches long-term insurance liability characteristics",
                  "Infrastructure assets can be sold within 24 hours if claims arise",
                  "Infrastructure requires no expertise or due diligence"],
                 1,
                 "Infrastructure's long duration, stable regulated returns, and inflation "
                 "protection align with the characteristics of long-term insurance liabilities."),
            _mcq("What is the typical 'management and performance' fee structure for hedge funds?",
                 ["0.1% management only",
                  "1% management fee + 10% of profits",
                  "2% annual management fee + 20% of profits above a hurdle rate",
                  "5% management fee only"],
                 2,
                 "The '2 and 20' structure is standard: 2% annual fee on assets + 20% of "
                 "returns above a benchmark. This makes hedge funds expensive compared to "
                 "traditional managers."),
            _mcq("A $1 billion private equity fund charges '2 and 20.' The fund earns 30% "
                 "($300M) in a year. How much goes to management fees and performance allocation?",
                 ["$20M management + $60M performance = $80M total",
                  "$20M management + $300M performance = $320M total",
                  "$2M management + $60M performance = $62M total",
                  "$20M management only = $20M total"],
                 0,
                 "Management fee: $1B Ã— 2% = $20M. Performance: $300M profit Ã— 20% = $60M. "
                 "Total fees: $80M (investors net $220M on the $300M gain)."),
            _mcq("COMMON MISTAKE: An analyst says insurance companies shouldn't invest in "
                 "private equity because 'it's riskier than stocks.' What important factor "
                 "are they overlooking?",
                 ["Private equity has lower risk than stocks",
                  "For insurers with long time horizons and stable liabilities, illiquidity "
                  "is acceptable and private equity's higher expected return compensates "
                  "for the risk â€” it's about matching investment characteristics to obligations",
                  "Insurance regulators prohibit private equity completely",
                  "Private equity returns are identical to public equity returns"],
                 1,
                 "Insurers with stable, long-term liabilities can accept illiquidity and "
                 "earn an 'illiquidity premium.' The higher expected return from PE "
                 "compensates for reduced liquidity when managed within portfolio limits."),
            _scenario("Pacific Life Insurance has $500M to allocate. Option A: put it all in "
                      "a hedge fund that made 25% last year. Option B: split between "
                      "infrastructure (60%) and investment-grade bonds (40%). Pacific Life's "
                      "policyholders have 20-year term insurance contracts.",
                      "Which allocation better serves Pacific Life's obligations?",
                      [("Option A â€” the 25% return last year makes it clearly better", False,
                        "Past performance doesn't predict future returns. A 25% one-year "
                        "return often involves significant risk that mismatches a 20-year liability."),
                       ("Option B â€” infrastructure provides long-duration, stable income matching "
                        "the 20-year liability, with bonds adding liquidity and stability", True,
                        "Correct. Infrastructure and bonds match Pacific Life's long duration "
                        "while maintaining liquidity. A single hedge fund allocation "
                        "is undiversified, illiquid, and risk-inappropriate."),
                       ("Neither â€” Pacific Life should keep all assets in cash", False,
                        "Cash returns are far below what is needed to fund future claims "
                        "at competitive premium rates."),
                       ]),
        ],
    )

    c4 = _concept(m2_id, 2,
        "Investment Funds, Capital Markets, Primary vs. Secondary Markets",
        "Describe mutual funds, ETFs, and UITs; distinguish primary from secondary markets.",
        "Investment funds pool capital from many investors to buy diversified portfolios. "
        "Mutual funds are actively or passively managed. ETFs trade on exchanges like stocks. "
        "Unit Investment Trusts hold fixed portfolios. Capital markets are where long-term "
        "securities are issued (primary market) and traded after issuance (secondary market).",
        "BlackRock's iShares TIPS Bond ETF allows an insurer to buy inflation-protected "
        "Treasuries in a single liquid instrument trading on the NYSE â€” with the diversification "
        "of 40+ individual TIPS bonds but the simplicity of buying one stock ticker.",
        [
            "Mutual funds: pooled investment, professionally managed, priced daily at NAV",
            "ETF: exchange-traded fund, trades intraday like a stock, typically lower cost",
            "UIT: fixed portfolio, set maturity, no active management",
            "Primary market: where new securities are ISSUED (IPO, bond offering)",
            "Secondary market: where already-issued securities are TRADED between investors",
        ],
        [
            "Confusing primary market (new issuance) with secondary market (existing securities trading)",
            "Thinking ETFs and mutual funds are identical â€” ETFs trade intraday; mutual funds price once per day",
        ],
        [
            _intro("Pooled Investing and the Markets Where It Happens",
                   "Why buy individual stocks when you can own 500 companies at once? "
                   "Investment funds make diversification accessible. And every transaction "
                   "happens in a capital market â€” let's understand the entire ecosystem."),
            _teach("Investment Fund Types: Mutual Funds, ETFs, and UITs",
                   "Mutual funds pool money from many investors to buy a diversified portfolio "
                   "of securities managed by professional portfolio managers. They are priced "
                   "once per day at their Net Asset Value (NAV) â€” total portfolio value divided "
                   "by shares outstanding. ETFs (Exchange-Traded Funds) are similar to mutual "
                   "funds but trade on stock exchanges throughout the day like individual "
                   "stocks. ETFs typically track an index (passive management) and have lower "
                   "fees than actively managed mutual funds. Unit Investment Trusts (UITs) hold "
                   "a fixed portfolio of securities with a defined maturity date â€” there is "
                   "no active management; the portfolio is set at creation and held to termination.",
                   [
                       "Mutual fund: daily NAV pricing, can be active or passive, no intraday trading",
                       "ETF: intraday trading, usually index-tracking, lower cost than active mutual funds",
                       "UIT: fixed portfolio, no active management, defined termination date",
                       "All three provide instant diversification and professional oversight",
                   ]),
            _teach("Capital Markets: Primary vs. Secondary",
                   "Capital markets are financial markets where long-term debt and equity "
                   "securities are issued and traded (as opposed to money markets for short-term "
                   "instruments). The primary market is where securities are CREATED and ISSUED "
                   "for the first time. When a company does an IPO (Initial Public Offering) "
                   "or issues new bonds, it happens in the primary market. The issuer receives "
                   "the capital directly. The secondary market is where already-issued securities "
                   "trade BETWEEN INVESTORS. The New York Stock Exchange (NYSE) and NASDAQ are "
                   "secondary markets â€” when you buy Apple stock on the NYSE, Apple receives "
                   "no money; you buy from another investor. Securities exchanges are organized "
                   "secondary markets with listing requirements and regulated trading.",
                   [
                       "Primary market: new issuance â€” issuer receives capital (IPO, bond offering)",
                       "Secondary market: trading existing securities between investors",
                       "NYSE, NASDAQ: secondary market exchanges with listing standards",
                       "OTC: over-the-counter market for bonds and derivatives (less regulated)",
                       "Liquidity: secondary markets make primary market investing possible",
                   ]),
            _example("Boeing Issues New Bonds â€” A Primary and Secondary Market Journey",
                     "In January 2024, Boeing issues $5 billion in new 10-year bonds at 6% "
                     "coupon to fund operations (PRIMARY MARKET transaction). Investment banks "
                     "Goldman Sachs and JPMorgan underwrite the offering, selling the bonds "
                     "to institutional investors including Lincoln National Insurance, which "
                     "buys $200M. Lincoln receives $200M in bonds; Boeing receives $200M in "
                     "cash. Three months later, Lincoln's portfolio manager decides to sell "
                     "$50M of these Boeing bonds to raise cash (SECONDARY MARKET transaction). "
                     "Another insurer, Principal Life, buys the bonds from Lincoln on the "
                     "OTC bond market at the current market price. Boeing is uninvolved â€” "
                     "this is purely between Lincoln and Principal.",
                     "Understanding primary vs. secondary market is fundamental: "
                     "the issuer only gets money in the primary market."),
            _flash("In which market does the issuer of a security DIRECTLY receive proceeds?",
                   "The PRIMARY market â€” when securities are first issued (IPO or bond offering). "
                   "In secondary markets, trading occurs between investors and the issuer receives nothing."),
            _mcq("How does an ETF differ from a mutual fund in terms of trading?",
                 ["ETFs are only available to institutional investors",
                  "ETFs trade intraday on stock exchanges at market prices; "
                  "mutual funds are priced and transacted once per day at NAV",
                  "ETFs always outperform mutual funds",
                  "Mutual funds charge no fees; ETFs are very expensive"],
                 1,
                 "The key operational difference: ETFs trade continuously during market hours "
                 "at fluctuating prices. Mutual fund orders execute at NAV calculated at day's end."),
            _mcq("A company raises $500M by selling newly issued shares to the public for the "
                 "first time. In which market does this occur?",
                 ["Secondary market on the NYSE",
                  "Over-the-counter bond market",
                  "Primary market through an Initial Public Offering (IPO)",
                  "Money market"],
                 2,
                 "An IPO is a primary market event â€” the company issues new shares for the first "
                 "time and receives the capital directly from investors."),
            _mcq("After an IPO, investors trade the company's shares among themselves on the "
                 "NYSE. What is this?",
                 ["Another primary market transaction",
                  "A secondary market transaction â€” investors trade existing shares; "
                  "the company receives no proceeds",
                  "An over-the-counter transaction",
                  "A money market transaction"],
                 1,
                 "Secondary market trading is between investors. The original issuing company "
                 "does not receive any proceeds from secondary market trades."),
            _mcq("A Unit Investment Trust (UIT) differs from a mutual fund primarily because:",
                 ["UITs charge higher fees than mutual funds",
                  "UITs hold a fixed, unmanaged portfolio and have a defined termination date",
                  "UITs trade on exchanges throughout the day",
                  "UITs only invest in government bonds"],
                 1,
                 "UITs are unmanaged â€” the portfolio is fixed at creation and not actively "
                 "traded. They have a defined end date unlike open-ended mutual funds."),
            _mcq("COMMON MISTAKE: After buying Boeing stock on the NYSE, an investor thinks "
                 "Boeing just received $10,000. Why is this wrong?",
                 ["It is correct â€” Boeing receives money every time its stock is traded",
                  "Boeing only receives money when it issues NEW shares (primary market). "
                  "NYSE trades are secondary market â€” money flows between investors, not to Boeing",
                  "The NYSE keeps all the money from stock trades",
                  "Boeing receives half of every trade's proceeds"],
                 1,
                 "Secondary market trades transfer money between buyers and sellers â€” "
                 "the issuing company is completely uninvolved and receives nothing."),
            _scenario("Nationwide Insurance needs to invest $1B quickly and wants broad "
                      "equity market exposure, the ability to sell within hours if needed, "
                      "and low management fees.",
                      "Which investment vehicle best fits these requirements?",
                      [("An actively managed large-cap mutual fund", False,
                        "Mutual funds can only be redeemed at end-of-day NAV, not 'within hours.' "
                        "Active management also typically carries higher fees."),
                       ("A broad market equity ETF tracking the S&P 500", True,
                        "Correct. ETFs provide broad diversification, trade throughout the day "
                        "(can sell 'within hours'), and typically have very low fees (0.03-0.10%)."),
                       ("Purchase $1B in individual stocks across 500 companies", False,
                        "Trading 500 individual stocks would take enormous time and incur "
                        "significant transaction costs â€” impractical for same-day deployment."),
                       ]),
        ],
    )

    m2["concepts"] = [c3, c4]
    ch["modules"] = [m1, m2]
    return ch


# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€


def _build_ch4(course_id):
    ch_id = _id()
    ch = {
        "id": ch_id, "course_id": course_id, "order": 4,
        "title": "Investment Returns and Risks",
        "description": "How investors earn returns through capital gains and income, what factors drive those returns, how to measure them using total return and standard deviation, and how to classify the risks every investor faces.",
    }

    # â”€â”€ Module 1: Investment Returns â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    m1_id = _id()
    m1 = {"id": m1_id, "chapter_id": ch_id, "order": 1, "title": "Investment Returns"}

    # Concept 1: Types of Investment Returns
    c1 = _concept(
        m1_id, 1,
        "Types of Investment Returns: Capital Gains and Income",
        "Identify and distinguish the two primary forms of investment return â€” capital gains and income payments â€” and explain how each is generated.",
        "When you invest, your money can grow in two ways. First, the investment itself can increase in value (capital gain). Second, it can pay you money along the way (income). A bond pays interest coupons. A stock pays dividends. A property pays rent. An insurer like MassMutual earns both: the bonds in its portfolio appreciate AND pay interest, contributing to the spread income that funds policyholder benefits.",
        "Pacific Life buys a $1 million corporate bond at par. Over 5 years it collects $50,000 in annual interest (income return). When interest rates later drop, the bond's market value rises to $1.1 million. If Pacific Life sells, it books a $100,000 capital gain. Total dollar return = $250,000 income + $100,000 capital gain = $350,000.",
        [
            "Capital gains = increase in the market value of an asset; can be unrealized (still held) or realized (sold).",
            "Income payments include interest on bonds, dividends on stocks, and rent on real estate.",
            "Unrealized gains do not generate cash until the asset is sold; realized gains do.",
            "Insurance companies prioritize income return (predictable cash flows) over capital gains to match their steady claim obligations.",
        ],
        [
            "Confusing unrealized and realized gains â€” insurers report both but only collect cash on realized gains.",
            "Forgetting that dividends received by corporations get the Dividends-Received Deduction (DRD), making equity income tax-advantaged.",
            "Assuming all bonds pay income â€” zero-coupon bonds pay no periodic interest but are bought at a discount and deliver a lump-sum gain at maturity.",
        ],
        lessons=[
            _intro("How Does Investing Actually Make You Money?",
                   "Investing generates returns in two distinct ways: the asset grows in value, or it pays you along the way. Understanding this distinction is fundamental to every portfolio decision an institutional investor makes."),
            _teach("Capital Gains: Your Investment Grows in Value",
                   "A capital gain occurs when an investment's market value rises above what you paid for it. If Pacific Life buys a bond for $1,000 and its market value rises to $1,100, the $100 difference is an unrealized capital gain. It becomes realized only when Pacific Life sells. The gain can be short-term (held less than one year) or long-term, with different tax implications.",
                   ["Unrealized gain = current market value minus purchase price (no cash yet).",
                    "Realized gain = proceeds from sale minus purchase price (cash received).",
                    "For institutions, large unrealized gains in 'available-for-sale' portfolios affect regulatory capital calculations."]),
            _teach("Income Payments: Your Investment Pays You Along the Way",
                   "Income payments are the periodic cash flows an investment generates while you hold it. Bonds pay interest coupons (e.g., 5% on face value annually). Stocks pay dividends declared by the board. Real estate generates rental income. For insurance companies, income return is critical because they need steady cash to pay policyholder claims â€” they cannot wait to sell assets every time a claim arrives.",
                   ["Bond interest = coupon rate x face value, paid semi-annually for most US bonds.",
                    "Dividends are declared by the board and are NOT guaranteed (unlike bond interest).",
                    "Rental income from real property is the most inflation-resistant income form.",
                    "Income return is more predictable and stable than capital gain, making it the backbone of insurer portfolios."]),
            _example("Pacific Life's Bond: Two Returns in One",
                     "In 2018, Pacific Life purchased a $10 million Apple corporate bond with a 4% annual coupon. For three years, Pacific Life collected $400,000 per year in coupon interest ($1.2 million total income). When the Fed cut rates in 2020, Apple's bonds became more valuable; Pacific Life's bond was now worth $10.8 million. Pacific Life sold the bond, realizing an $800,000 capital gain. Total return over three years: $1.2M income + $0.8M capital gain = $2 million on a $10M investment.",
                     "Both income and capital appreciation contribute to total return; the best institutional portfolios capture both."),
            _flash("What is a realized capital gain?",
                   "The profit earned when an investment is actually sold â€” equal to sale price minus original purchase price. Until sold, the gain is 'unrealized.'"),
            _mcq("Which of the following is an example of income return from a bond investment?",
                 ["Capital appreciation when interest rates fall",
                  "Semi-annual coupon payments received from the bond issuer",
                  "The difference between purchase price and par value at maturity",
                  "The increase in the bond's credit rating"],
                 1,
                 "Coupon payments are periodic cash flows paid by the issuer â€” the definition of income return. Capital appreciation is a separate return component."),
            _mcq("A life insurer holds a stock with an unrealized gain of $500,000. Which statement is MOST accurate?",
                 ["The insurer has received $500,000 in cash",
                  "The insurer has a paper gain that becomes cash only upon sale",
                  "The insurer must pay taxes on the $500,000 immediately",
                  "The gain is guaranteed to persist until the stock is sold"],
                 1,
                 "Unrealized gains exist on paper. Until the asset is sold, no cash changes hands and no tax is triggered. The gain can also reverse if the market declines."),
            _mcq("Why do insurance companies typically emphasize income return over capital gains in portfolio construction?",
                 ["Capital gains are illegal for regulated insurers",
                  "Insurance companies never hold equity investments",
                  "Income payments provide predictable cash flows to fund ongoing claim obligations",
                  "Capital gains are always taxed at higher rates for insurers"],
                 2,
                 "Insurers face continuous, predictable cash outflows (claims, annuity payments). Steady income from bonds and dividends matches these obligations without requiring asset sales."),
            _mcq("Horizon Life buys a zero-coupon bond for $743 that matures at $1,000 in 5 years. What type of return will Horizon receive?",
                 ["Pure income return via periodic interest payments",
                  "Pure capital gain at maturity when the bond pays $1,000",
                  "Equal parts income and capital gain",
                  "No return â€” zero-coupon bonds are risk-free instruments with no yield"],
                 1,
                 "Zero-coupon bonds pay no periodic interest. The entire return is a capital gain (the difference between purchase price $743 and face value $1,000 received at maturity)."),
            _mcq("Which return component benefits most from the Dividends-Received Deduction (DRD) available to corporate investors?",
                 ["Interest income from bonds",
                  "Rental income from real estate",
                  "Dividend income from equity investments",
                  "Capital gains from stock sales"],
                 2,
                 "The DRD allows corporations to exclude 50-65% of dividends received from domestic corporations from taxable income, making dividend income especially tax-efficient for insurers."),
            _scenario(
                "Guardian Life's CIO is reviewing a proposed bond portfolio restructuring. The current portfolio holds bonds with $50M in unrealized gains. The new manager proposes selling all bonds to 'lock in profits' and rotating into higher-yielding bonds.",
                "What is the PRIMARY risk of selling all bonds to lock in the unrealized gains?",
                [("Proceed â€” unrealized gains are worthless until locked in", False,
                  "While realizing gains provides cash, it also triggers a taxable event and forces reinvestment at current (potentially lower or more volatile) yields."),
                 ("Decline â€” selling triggers a taxable gain event and forces reinvestment risk at current market prices", True,
                  "Correct. Realizing gains triggers corporate taxes on the gain. The proceeds must be reinvested at current rates, which may offer lower risk-adjusted returns than the existing portfolio."),
                 ("Proceed â€” tax rates on realized gains are zero for insurance companies", False,
                  "Insurance companies are subject to corporate tax on realized capital gains, just like other corporations.")]
            ),
        ]
    )

    # Concept 2: Factors Influencing Returns
    c2 = _concept(
        m1_id, 2,
        "Factors Influencing Returns: Interest Rates, Inflation, and the Business Cycle",
        "Explain how market interest rates, inflation, and the business cycle affect investment returns, and describe the inverse price-yield relationship for bonds.",
        "Returns never exist in a vacuum â€” they are constantly reshaped by forces outside the investor's control. When the Federal Reserve raises interest rates, existing bond prices fall. When inflation surges, real returns erode. When the economy enters a recession, stocks tumble and credit defaults rise. A skilled institutional investor anticipates these factors to position the portfolio defensively before they strike â€” not reactively after.",
        "In 2022, the Federal Reserve raised rates by 4.25% in one year. A $1 billion bond portfolio at Principal Financial Group, holding mostly long-duration bonds, lost about $120 million in market value as rates rose â€” because bond prices move opposite to rates. Meanwhile, inflation of 8% meant that even bonds that paid 4% coupon had negative real returns (-4%). The CIO had to decide: hold through the pain, or reallocate to shorter-duration, inflation-protected securities.",
        [
            "Bond price and yield move in opposite directions â€” when rates rise, existing bond prices fall.",
            "Inflation reduces 'real return' â€” a bond yielding 5% during 8% inflation has a real return of roughly -3%.",
            "The business cycle (expansion, peak, recession, trough) drives equity returns, credit spreads, and asset allocation decisions.",
            "Market interest rates are the single most powerful external factor for fixed-income portfolios.",
        ],
        [
            "Thinking higher interest rates are always bad â€” they hurt existing bondholders but benefit new investors buying at higher yields.",
            "Confusing nominal return (stated %) with real return (after inflation) â€” the LOMA exam tests both.",
            "Ignoring reinvestment risk: when rates fall, coupon payments get reinvested at lower yields, reducing total return.",
        ],
        lessons=[
            _intro("What Forces Shape Your Investment Returns?",
                   "Even a perfectly constructed portfolio can underperform if the macro environment shifts. Interest rates, inflation, and the business cycle are forces every institutional investor must understand and anticipate."),
            _teach("The Price-Yield Relationship: Bond Prices and Interest Rates",
                   "There is an iron law in fixed income: when interest rates (yields) rise, existing bond prices fall, and when rates fall, bond prices rise. Here's why: if you hold a bond paying 4% and new bonds now pay 6%, nobody wants your 4% bond unless the price drops enough to make it competitive. The longer the bond's maturity, the bigger the price swing for a given rate change. This sensitivity is measured by 'duration.'",
                   ["Price-yield relationship is inverse â€” rates up = prices down.",
                    "Long-duration bonds are more price-sensitive to rate changes than short-duration bonds.",
                    "Duration measures how much a bond's price changes for a 1% change in yield.",
                    "Insurance ALM teams actively manage portfolio duration to control interest rate risk."]),
            _teach("Inflation and the Business Cycle",
                   "Inflation erodes purchasing power â€” a 5% nominal return during 6% inflation is actually a -1% real return. Real return = Nominal return - Inflation rate (simplified Fisher equation). The business cycle moves through four phases: Expansion (rising GDP, strong earnings, equities outperform), Peak (growth slows, rates high), Recession (GDP falls, credit spreads widen, equities decline, treasuries outperform), and Trough (recovery begins, equities lead). Each phase rewards different asset classes.",
                   ["Real Return = Nominal Return - Inflation Rate.",
                    "Expansion: equities and credit outperform. Recession: treasuries and high-grade bonds outperform.",
                    "Inflation above 3-4% significantly erodes fixed-rate bond returns.",
                    "TIPS (Treasury Inflation-Protected Securities) adjust principal with CPI to protect real return."]),
            _example("Principal Financial's 2022 Duration Crisis",
                     "Principal Financial Group held a $1.2 billion bond portfolio with an average duration of 12 years in early 2022. When the Fed began raising rates â€” 0.25% in March, then 0.50%, then 0.75% â€” four times in one year, Principal's portfolio lost roughly $144 million in market value (12 years x 1% rate rise = ~12% decline per dollar). Meanwhile, CPI hit 8.5%, meaning even Principal's highest-yielding bonds (5%) had negative real returns. Principal's ALM team shortened duration by selling long bonds and buying 3-5 year bonds to limit further damage.",
                     "Duration risk is real and quantifiable; insurers that fail to manage it face significant balance sheet losses when rates rise sharply."),
            _flash("What is the 'real return' on a bond yielding 6% during 4% inflation?",
                   "Approximately 2% (6% nominal minus 4% inflation = 2% real return). Real return measures how much purchasing power your investment actually gained."),
            _mcq("Interest rates rise by 1%. What happens to the price of an existing 10-year bond?",
                 ["The bond price rises proportionally to the rate increase",
                  "The bond price falls by approximately the bond's duration percentage",
                  "The bond price remains unchanged because the coupon is fixed",
                  "The bond price rises because higher rates signal a stronger economy"],
                 1,
                 "Bond prices and yields move inversely. A 1% rate rise causes a bond's price to fall by approximately its duration in percentage terms. A 10-year bond with duration of 8 would fall approximately 8%."),
            _mcq("A bond yields 5% nominal. If inflation runs at 3%, what is the approximate real return?",
                 ["8%", "5%", "2%", "3%"],
                 2,
                 "Real return = Nominal return - Inflation rate = 5% - 3% = 2%. The investor's purchasing power grows by only 2%, not the nominal 5%."),
            _mcq("During which phase of the business cycle do equity investments typically perform BEST?",
                 ["Recession", "Peak", "Trough", "Expansion"],
                 3,
                 "During economic expansion, corporate earnings grow, consumer spending rises, and equity valuations tend to increase. This is typically the strongest period for stock market returns."),
            _mcq("An insurer holds $500M in 20-year bonds when interest rates drop 2%. What is the MOST LIKELY impact?",
                 ["The portfolio value decreases by approximately $200M",
                  "The portfolio value increases significantly due to the inverse price-yield relationship",
                  "The portfolio value is unaffected because coupon payments remain the same",
                  "The portfolio value decreases because falling rates signal recession"],
                 1,
                 "When rates fall, existing bond prices rise (inverse relationship). A 2% rate drop on long-duration bonds (duration ~15 for 20-year bonds) could increase portfolio value by roughly 30% â€” $150M gain."),
            _mcq("Which of the following BEST protects a bond portfolio against rising inflation?",
                 ["Extending bond duration to capture more interest income",
                  "Allocating to long-term fixed-rate bonds at the current coupon",
                  "Investing in TIPS (Treasury Inflation-Protected Securities) or floating-rate bonds",
                  "Concentrating in zero-coupon bonds to avoid reinvestment risk"],
                 2,
                 "TIPS adjust their principal value with CPI inflation, so both the principal and interest payments grow with inflation, preserving real return. Floating-rate bonds reset their coupons as rates rise."),
            _scenario(
                "Sun Life Financial's CIO sees economic signals pointing to an imminent recession: GDP growth slowing from 3% to 0.5%, unemployment rising, and the yield curve inverting. Sun Life holds 60% equities and 40% long-duration bonds.",
                "What asset allocation shift is MOST appropriate for Sun Life heading into a recession?",
                [("Increase equity allocation to 80% to buy stocks at lower prices", False,
                  "Equities typically decline sharply during recessions as corporate earnings fall. Increasing equity exposure would increase risk at the wrong time."),
                 ("Shift toward high-quality long-duration government bonds and reduce equity exposure", True,
                  "Correct. During recessions, flight-to-safety drives demand for government bonds, raising their prices. High-grade bonds outperform equities in recessions. Long duration benefits from falling rates."),
                 ("Move entirely to cash to avoid all market risk", False,
                  "While reducing risk, holding all cash earns near-zero returns and misses the bond price appreciation that occurs when rates fall during recessions.")]
            ),
        ]
    )

    m1["concepts"] = [c1, c2]

    # â”€â”€ Module 2: Risk Measurement â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    m2_id = _id()
    m2 = {"id": m2_id, "chapter_id": ch_id, "order": 2, "title": "Measuring and Managing Investment Risk"}

    # Concept 3: Measuring Returns and Volatility
    c3 = _concept(
        m2_id, 1,
        "Measuring Returns and Volatility: Total Return, Standard Deviation, and the Risk-Return Trade-Off",
        "Calculate and interpret total return, distinguish between arithmetic and geometric mean returns, and use standard deviation to quantify investment risk.",
        "Measuring returns sounds simple â€” but investors need to be precise. Total return captures everything (income + price change). But returns over multiple periods compound, so the geometric mean (not arithmetic average) tells you how your money actually grew. Risk is measured by how much returns fluctuate â€” standard deviation. A higher standard deviation means more volatile returns. And here is the fundamental trade-off: to earn higher returns, you must accept more risk. No free lunches in investing.",
        "From 2000-2019, the S&P 500 had an arithmetic average annual return of 7.5% but a geometric mean return of only 6.1%. Why the gap? The 2001 crash (-9%) and 2008 crash (-38%) destroyed so much value that compounding worked against investors who held through. A $10M portfolio from Nationwide Insurance that earned -38% in 2008 needed to earn +61% in 2009 just to break even. The geometric mean correctly captures this compounding reality.",
        [
            "Total Return = (Income + Price Change) / Beginning Price x 100%.",
            "Arithmetic mean overstates real returns over multiple periods; geometric mean (CAGR) is the correct measure.",
            "Standard deviation measures how widely returns fluctuate around the average â€” higher std dev = higher risk.",
            "The risk-return trade-off: higher expected returns require accepting higher volatility.",
        ],
        [
            "Using arithmetic average for multi-year performance reporting â€” always use geometric mean (CAGR) for multi-period comparisons.",
            "Assuming standard deviation fully captures risk â€” it measures volatility but not catastrophic tail events.",
            "Thinking lower risk always means lower return â€” skill in security selection can improve the risk-return ratio.",
        ],
        lessons=[
            _intro("How Do We Actually Measure Investment Performance?",
                   "Saying 'I earned 10%' sounds simple â€” but 10% of what, over what period, compared to what risk? Professional investors use precise metrics. Let's build the toolkit: total return, geometric mean, and standard deviation."),
            _teach("Total Return: The Complete Picture",
                   "Total return captures everything an investment earns: income payments PLUS any change in market value. Formula: Total Return = (Income Received + Ending Value - Beginning Value) / Beginning Value x 100%. Example: buy a bond for $1,000, receive $50 in interest, sell for $1,020. Total return = ($50 + $20) / $1,000 = 7%. This is the gold standard metric because it leaves nothing out.",
                   ["Total return includes both income (coupons, dividends) and price change (capital gain/loss).",
                    "Always express total return as a percentage of the beginning investment value.",
                    "For multi-year periods, annualize total return using the geometric mean (CAGR).",
                    "Insurers report total returns to regulators, policyholders, and investment committees."]),
            _teach("Standard Deviation and the Risk-Return Trade-Off",
                   "Standard deviation (sigma) measures how widely an investment's returns fluctuate around its average. If a bond fund averaged 5% returns with a standard deviation of 2%, you'd expect most annual returns to fall between 3% and 7% (within one sigma). An equity fund averaging 10% with a 20% standard deviation could range from -10% to +30% â€” far wider swings. The risk-return trade-off is the fundamental principle: investors demand HIGHER expected returns for accepting HIGHER risk (volatility). No rational investor accepts higher risk for the same expected return.",
                   ["Standard deviation = typical size of annual return fluctuations around the mean.",
                    "Low std dev = stable, predictable returns (government bonds). High std dev = volatile returns (equities).",
                    "Risk-return trade-off: higher risk assets must offer higher expected returns to attract investors.",
                    "The Sharpe ratio = (Return - Risk-free rate) / Standard deviation â€” measures return per unit of risk."]),
            _example("Nationwide's S&P 500 vs. Bond Fund Comparison",
                     "Nationwide Insurance compared two portfolio options. Option A: S&P 500 index fund â€” 10-year average return 9.8%, standard deviation 18%. Option B: Investment-grade bond fund â€” 10-year average return 4.2%, standard deviation 4%. The S&P fund offered more than double the return but with 4.5x the volatility. During 2008, Option A lost 38% while Option B gained 5.2%. Nationwide's ALM committee decided that given their policyholder liability profile, no more than 30% could be in equities â€” the potential for a 38% loss in any single year would threaten their solvency ratios.",
                     "Volatility (standard deviation) must be evaluated relative to the institution's liability structure â€” not just versus other investments."),
            _flash("What does a standard deviation of 15% mean for an investment averaging 8% returns?",
                   "It means annual returns typically range from roughly -7% to +23% (mean +/- one standard deviation). Approximately 68% of annual returns fall within this range, and 95% fall within two standard deviations (-22% to +38%)."),
            _mcq("An investor buys a stock for $50, collects $2 in dividends, and sells for $54. What is the total return?",
                 ["4%", "8%", "10%", "12%"],
                 3,
                 "Total return = (Income + Price Change) / Beginning Price = ($2 + $4) / $50 = $6/$50 = 12%. Both the dividend income ($2) and capital gain ($4) are included."),
            _mcq("Portfolio A earned 20%, -10%, and 5% over three years. Which return BEST represents how an investor's money actually grew?",
                 ["The arithmetic mean: 5%",
                  "The geometric mean (CAGR): approximately 3.9%",
                  "The highest single-year return: 20%",
                  "The median return: 5%"],
                 1,
                 "The geometric mean (CAGR) correctly captures compounding. $1 x 1.20 x 0.90 x 1.05 = $1.134, so CAGR = (1.134)^(1/3) - 1 = approximately 3.9%. The arithmetic mean of 5% overstates performance."),
            _mcq("Investment X has average return 8% with standard deviation 6%. Investment Y has average return 8% with standard deviation 12%. Which should a risk-averse institutional investor prefer?",
                 ["Investment Y, because the higher standard deviation may lead to higher peaks",
                  "Investment X, because it offers the same expected return with half the volatility",
                  "Neither â€” both have the same return so standard deviation is irrelevant",
                  "Investment Y, because higher volatility always indicates higher quality"],
                 1,
                 "When expected returns are equal, a risk-averse investor always prefers less volatility. Investment X delivers the same 8% average with half the risk â€” it dominates Investment Y for risk-averse investors."),
            _mcq("What does the risk-return trade-off mean for institutional investors?",
                 ["Higher returns are available by increasing trading frequency",
                  "To earn higher expected returns, investors must accept higher volatility or risk of loss",
                  "Government bonds always outperform equities on a risk-adjusted basis",
                  "Risk and return are unrelated because markets are perfectly efficient"],
                 1,
                 "The risk-return trade-off is foundational: assets with higher expected returns (equities, high-yield bonds) carry higher volatility and downside risk. Investors must be compensated for taking on risk."),
            _mcq("Which metric BEST measures return per unit of risk taken?",
                 ["Total return percentage",
                  "Arithmetic mean return",
                  "Standard deviation alone",
                  "The Sharpe ratio (return minus risk-free rate, divided by standard deviation)"],
                 3,
                 "The Sharpe ratio measures how much excess return (above the risk-free rate) an investor receives per unit of risk (standard deviation). A higher Sharpe ratio indicates better risk-adjusted performance."),
            _scenario(
                "Lincoln Financial's investment committee reviews two bond managers. Manager A: 10-year average return 6.8%, standard deviation 8%. Manager B: 10-year average return 7.0%, standard deviation 15%. The risk-free rate is 3%.",
                "Based on risk-adjusted return analysis, which manager should Lincoln Financial prefer?",
                [("Manager B â€” the 0.2% higher return justifies the extra risk", False,
                  "A 0.2% return improvement with nearly double the volatility is poor risk-adjusted trade-off. Sharpe ratio for B = (7.0-3.0)/15 = 0.27, far below Manager A."),
                 ("Manager A â€” better Sharpe ratio means more return per unit of risk", True,
                  "Correct. Manager A Sharpe = (6.8-3.0)/8 = 0.475. Manager B Sharpe = (7.0-3.0)/15 = 0.267. Manager A delivers significantly more return per unit of risk taken."),
                 ("Neither â€” Sharpe ratio does not apply to bond managers", False,
                  "Sharpe ratio applies to all investment managers. It is one of the most widely used risk-adjusted performance metrics in institutional investing.")]
            ),
        ]
    )

    # Concept 4: Investment Risks
    c4 = _concept(
        m2_id, 2,
        "Investment Risks: Systematic and Specific Risks",
        "Classify investment risks as systematic (market-wide) or specific (security-level), describe the major risk types in each category, and explain why diversification eliminates specific but not systematic risk.",
        "Risk is not one thing â€” it is many. When the stock market crashes, ALL stocks tend to fall â€” this is systematic risk you cannot escape by diversification. But when a single company goes bankrupt, only its bondholders suffer â€” this is specific risk you CAN eliminate by holding many securities. LOMA 357 tests your ability to name, define, and classify these risks correctly. Insurance companies face ALL of these risks and use sophisticated risk management frameworks to control them.",
        "In 2008, Lehman Brothers' collapse illustrated both risk types simultaneously. Systematic risk: the entire credit market froze, corporate bond prices crashed everywhere â€” no diversification could prevent this. Specific risk: investors who held ONLY Lehman bonds lost 90 cents on the dollar, while those who had diversified across 50 issuers lost only their 2% Lehman allocation. Hartford Financial, which held a diversified bond portfolio of 300+ issuers, survived with losses 80% smaller than those that concentrated in mortgage-backed securities.",
        [
            "Systematic risks affect all investments in a market â€” they CANNOT be eliminated by diversification.",
            "Specific risks affect individual securities â€” they CAN be reduced through diversification.",
            "Key systematic risks: market risk, interest rate risk, inflation risk, currency risk, political/regulatory risk.",
            "Key specific risks: credit/default risk, liquidity risk, concentration risk, prepayment risk, reinvestment risk.",
        ],
        [
            "Thinking diversification eliminates ALL risk â€” it eliminates specific risk but not systematic risk.",
            "Confusing interest rate risk (a systematic risk) with credit risk (a specific risk).",
            "Assuming low-rated bonds always fail â€” they have higher DEFAULT PROBABILITY, not certainty.",
        ],
        lessons=[
            _intro("The Two Great Categories of Investment Risk",
                   "Some risks strike everything at once. Others strike only one company or sector. Understanding this difference determines how you build a portfolio, how you diversify, and how you protect against catastrophic losses."),
            _teach("Systematic Risks: The Risks You Cannot Escape",
                   "Systematic risks (also called market risks) affect the entire market or a broad segment of it simultaneously. No amount of diversification eliminates them because when they strike, everything moves together. The major systematic risks are: (1) Market risk â€” overall market declines; (2) Interest rate risk â€” rising rates hurt bond prices universally; (3) Inflation risk â€” rising prices erode ALL fixed-rate investment returns; (4) Currency risk â€” for international investments, exchange rate moves affect all foreign holdings; (5) Political/regulatory risk â€” laws or political instability that affect entire industries or markets.",
                   ["Market risk: systemic decline in equity or bond markets.",
                    "Interest rate risk: single biggest systematic risk for fixed-income insurers.",
                    "Inflation risk: erodes real return on all fixed-rate investments.",
                    "Currency risk: affects all foreign-currency-denominated investments simultaneously.",
                    "Diversification does NOT eliminate systematic risk."]),
            _teach("Specific Risks: The Risks You Can Manage",
                   "Specific risks (also called unsystematic or idiosyncratic risks) are tied to a particular company, sector, or security. They can be substantially reduced through diversification. Key specific risks: (1) Credit/Default risk â€” the issuer fails to pay interest or principal; (2) Liquidity risk â€” difficulty selling the investment at fair value quickly; (3) Concentration risk â€” too much exposure to one issuer, sector, or asset class; (4) Prepayment risk â€” mortgages are repaid early when rates fall, reducing expected income; (5) Reinvestment risk â€” cash flows must be reinvested at lower future rates.",
                   ["Credit risk: the #1 specific risk for bond investors â€” issuer defaults.",
                    "Liquidity risk: some assets (private equity, real estate) cannot be sold quickly.",
                    "Concentration risk: violates the principle of diversification.",
                    "Prepayment risk: specific to mortgage-backed securities â€” borrowers refinance in falling rate environments."]),
            _example("Hartford Financial's 2008 Stress Test: Diversification Saves the Day",
                     "In 2008, Hartford Financial Services held a $28 billion bond portfolio. Hartford's risk committee had enforced a strict rule: no single issuer could exceed 1.5% of the portfolio. When Lehman Brothers filed for bankruptcy in September 2008, Hartford's Lehman exposure was $420 million (1.5%) â€” painful but survivable. AIG's near-collapse similarly cost Hartford $315 million in AIG bonds. Total specific losses: ~$750 million. However, the systematic interest rate and credit spread widening cost Hartford approximately $3.2 billion in mark-to-market losses on the entire portfolio â€” proving that diversification handled specific risk but could not touch systematic risk.",
                     "Diversification eliminates specific risk (Lehman, AIG concentration) but systematic risk (credit market freeze) was unavoidable for ALL fixed-income investors."),
            _flash("What is the difference between systematic and specific risk?",
                   "Systematic risk affects all investments in a market (cannot be diversified away â€” e.g., interest rate risk, inflation). Specific risk affects individual securities (CAN be reduced by diversification â€” e.g., credit risk, liquidity risk)."),
            _mcq("Which of the following is a SYSTEMATIC risk?",
                 ["A corporate bond issuer defaults on its interest payments",
                  "A real estate investment becomes illiquid and cannot be sold",
                  "Rising interest rates cause all existing bond prices to fall",
                  "An individual company's earnings decline due to poor management"],
                 2,
                 "Rising interest rates affect ALL bond prices simultaneously â€” this is a market-wide (systematic) risk that no diversification can eliminate. The other options are specific risks affecting individual issuers or assets."),
            _mcq("An insurer holds 100 different corporate bonds across 20 industries. Which risk is MOST reduced by this diversification?",
                 ["Interest rate risk", "Inflation risk", "Credit/default risk", "Market risk"],
                 2,
                 "Credit/default risk is a specific risk â€” if one issuer defaults, the loss is isolated to that bond. Holding 100 different issuers across 20 industries substantially reduces this specific risk. Interest rate, inflation, and market risk are systematic and cannot be diversified away."),
            _mcq("Prepayment risk is MOST relevant to which type of investment?",
                 ["Corporate bonds with fixed coupons",
                  "Common equity with variable dividends",
                  "Mortgage-backed securities where underlying borrowers may repay early",
                  "Treasury bills with 90-day maturities"],
                 2,
                 "Prepayment risk is the risk that mortgage borrowers will repay their loans early (refinancing when rates fall). This collapses MBS cash flows and forces reinvestment at lower rates â€” a specific risk unique to mortgage-related instruments."),
            _mcq("An insurance company holds 40% of its bond portfolio in bonds from one issuer. Which risk is MOST elevated?",
                 ["Inflation risk", "Concentration risk", "Interest rate risk", "Market risk"],
                 1,
                 "Concentration risk â€” having 40% in one issuer â€” creates massive specific risk exposure. If that issuer defaults or is downgraded, the portfolio suffers a catastrophic, avoidable loss. Regulatory guidelines typically limit single-issuer exposure to 2-5%."),
            _mcq("Which statement BEST describes how diversification affects systematic vs. specific risk?",
                 ["Diversification eliminates both systematic and specific risk equally",
                  "Diversification cannot reduce any type of investment risk",
                  "Diversification reduces specific risk but has no effect on systematic risk",
                  "Diversification eliminates systematic risk but worsens specific risk"],
                 2,
                 "Diversification across many securities reduces specific risk because individual company events offset each other. Systematic risk (market-wide events) affects all securities simultaneously â€” diversification is powerless against it."),
            _scenario(
                "Protective Life's fixed-income portfolio manager is concerned about two separate risks: (1) The Federal Reserve may raise interest rates by 2% next quarter. (2) Three of the insurer's holdings â€” small regional bank bonds â€” are showing signs of potential credit deterioration.",
                "Which risk management strategy addresses each concern appropriately?",
                [("Diversify into more bonds to reduce interest rate risk; sell the bank bonds to reduce systematic risk", False,
                  "Interest rate risk is systematic and cannot be diversified away. Credit risk is specific and CAN be managed by selling or reducing the troubled positions."),
                 ("Shorten portfolio duration to reduce interest rate risk; diversify away from the three bank bonds to reduce credit risk", True,
                  "Correct. Shortening duration limits price sensitivity to rate increases (systematic risk management). Reducing concentration in the troubled bank bonds manages specific credit risk â€” precisely the right tools for each risk type."),
                 ("Hold all positions â€” both risks will eventually reverse themselves", False,
                  "Passivity in the face of identified, manageable risks is not sound risk management. Both risks are real, foreseeable, and require active mitigation.")]
            ),
        ]
    )

    m2["concepts"] = [c3, c4]
    ch["modules"] = [m1, m2]
    return ch




def _build_ch5(course_id):
    ch_id = _id()
    ch = {
        "id": ch_id, "course_id": course_id, "order": 5,
        "title": "Institutional Investment Objectives and Constraints",
        "description": "How insurance companies set investment goals (return, solvency, liquidity), the constraints they operate under (regulatory capital, rating requirements), what goes into an Investment Policy Statement, and how asset allocation decisions are made.",
    }

    # â”€â”€ Module 1: Investment Goals and IPS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    m1_id = _id()
    m1 = {"id": m1_id, "chapter_id": ch_id, "order": 1,
          "title": "Investment Objectives and Policy Statements"}

    # Concept 1: Basic Investment Goals for Institutional Investors
    c1 = _concept(
        m1_id, 1,
        "Basic Investment Goals: Return, Solvency, and Liquidity",
        "Identify the three fundamental investment goals of institutional investors â€” earning investment income, maintaining solvency, and ensuring liquidity â€” and explain how they interact and sometimes conflict.",
        "Every institutional investment portfolio begins with three non-negotiable goals. First, earn investment income to generate the spread that funds the business. Second, maintain solvency â€” assets must always exceed liabilities so policyholders can be paid. Third, ensure liquidity â€” cash must be available to pay claims when they arise. These three goals often pull in different directions. The highest-yielding investment might be illiquid. The most liquid investment might earn almost nothing. The art of institutional investment management is finding the optimal balance.",
        "Northwestern Mutual, one of the largest US life insurers, manages $290 billion in assets with these three goals in mind simultaneously. To earn income, it holds long-duration corporate bonds yielding 5-6%. To maintain solvency, it keeps its Risk-Based Capital (RBC) ratio above 400% of the regulatory minimum. To ensure liquidity, it holds 5% in money market instruments that can be converted to cash within 48 hours to pay any surge in claims. When Hurricane Katrina struck in 2005, Northwestern's liquidity buffer allowed it to pay $500M in claims within 72 hours without selling any long-term holdings.",
        [
            "Three fundamental goals: investment income (spread), solvency (assets > liabilities), liquidity (cash for claims).",
            "Solvency is non-negotiable â€” insurer must meet liabilities even in stress scenarios.",
            "Liquidity requirement is driven by liability structure: term life claims are unpredictable; annuities are more predictable.",
            "Higher yield typically means lower liquidity and/or higher credit risk â€” goals tension must be actively managed.",
        ],
        [
            "Thinking all three goals can be maximized simultaneously â€” in practice, they trade off against each other.",
            "Confusing solvency (assets > liabilities on balance sheet) with liquidity (having cash for immediate payments).",
            "Assuming investment income is always the top priority â€” solvency constraints come first for regulated insurers.",
        ],
        lessons=[
            _intro("What Is an Insurance Company Actually Trying to Achieve with Its Investments?",
                   "An insurer isn't just trying to earn the highest return. It has three competing goals that define every investment decision â€” and the balance between them is what separates great investment managers from mediocre ones."),
            _teach("Goal 1: Earning Investment Income",
                   "Insurance companies collect premiums upfront and pay claims later. The time gap between collecting premiums and paying claims creates an opportunity: those funds can be invested to earn returns. This 'spread' income is critical to profitability. A life insurer that guarantees 3% on whole life policies must earn at least 3.5-4% on its investment portfolio to cover expenses and generate profit. Investment income is the engine of insurance company profitability.",
                   ["Investment income = the return earned on policyholder premiums between collection and claim payment.",
                    "The 'spread' = investment return minus the interest rate guaranteed to policyholders.",
                    "Life insurers with long-duration liabilities (30-year policies) can invest in longer-duration, higher-yielding assets.",
                    "P&C insurers with short-duration liabilities must hold more liquid, shorter-duration assets."]),
            _teach("Goals 2 and 3: Solvency and Liquidity",
                   "Solvency means assets exceed liabilities at all times â€” an insurer cannot pay claims if it becomes insolvent. Regulators require minimum capital levels (Risk-Based Capital, or RBC) to ensure solvency. Liquidity means having enough cash or near-cash assets to pay claims as they arise. These two goals constrain investment income: to maintain solvency, insurers limit risky assets (equities, junk bonds); to maintain liquidity, they hold low-yielding cash and short-term instruments. The tradeoff: more solvency protection and liquidity = less yield.",
                   ["Solvency: total assets must exceed total liabilities (policyholder reserves + debt + other obligations).",
                    "Regulatory capital (RBC) requirements limit how much risk an insurer can take.",
                    "Liquidity: cash needed to pay near-term claims without forcing asset sales at bad prices.",
                    "Liquidity stress: if a natural disaster triggers 1,000 simultaneous claims, can the insurer pay without fire sales?"]),
            _example("Northwestern Mutual's Katrina Test",
                     "When Hurricane Katrina devastated New Orleans in August 2005, Northwestern Mutual faced an unprecedented surge in claims. In the first week after Katrina, Northwestern received $318 million in homeowners and life insurance claims â€” double the average weekly claim volume. Northwestern's CIO had maintained a 5% liquidity reserve ($14.5 billion total assets at the time), equivalent to $725 million in T-bills and money market funds. This buffer was drawn down to $480 million as claims were paid â€” without selling a single long-term bond. By month's end, the reserve was rebuilt through premium inflows. Solvency ratio remained at 420% RBC throughout the event.",
                     "Adequate liquidity reserves allow insurers to honor claims without distress selling, protecting both policyholders and the investment portfolio's long-term return."),
            _flash("What is the 'spread' in insurance investment management?",
                   "The spread is the difference between the return earned on investments and the interest rate guaranteed or credited to policyholders. A positive spread is the source of insurance company investment profit."),
            _mcq("Which of the following BEST describes the primary investment goal of a life insurance company?",
                 ["Maximize equity returns to benefit shareholders",
                  "Earn sufficient investment income to fund policyholder benefits while maintaining solvency and liquidity",
                  "Minimize all investment risk by holding only Treasury securities",
                  "Match the highest-yielding bonds in the market regardless of credit quality"],
                 1,
                 "The primary goal is earning adequate investment income while maintaining solvency and liquidity. Pure return maximization ignores the critical constraints of policyholder obligations and regulatory capital requirements."),
            _mcq("An insurance company's investment income yield is 5.5% and it guarantees policyholders a 4% credited rate. What is the investment spread?",
                 ["9.5%", "5.5%", "1.5%", "4%"],
                 2,
                 "Investment spread = investment income yield - credited rate = 5.5% - 4% = 1.5%. This 1.5% spread covers operating expenses and generates profit. If the spread turns negative, the insurer is losing money on its policies."),
            _mcq("Why must a life insurer hold liquid assets even if they earn lower returns than long-term bonds?",
                 ["Regulators require all insurance assets to be in money market funds",
                  "Liquid assets allow the insurer to pay claims promptly without forced selling of long-term holdings",
                  "Liquid assets always outperform illiquid assets on a risk-adjusted basis",
                  "Life insurance claims are paid monthly on a predictable schedule, requiring constant liquidity"],
                 1,
                 "Liquidity reserves allow immediate claim payments without distress selling. If an insurer is forced to sell long-term bonds quickly to raise cash, it may have to accept below-market prices, harming the portfolio."),
            _mcq("Which metric measures an insurer's ability to absorb unexpected losses while remaining able to pay all policyholder obligations?",
                 ["Investment yield spread", "Risk-Based Capital (RBC) ratio", "Liquidity coverage ratio", "Sharpe ratio"],
                 1,
                 "Risk-Based Capital (RBC) ratio measures an insurer's capital relative to its risk-weighted liabilities. Regulators set minimum RBC levels; insurers falling below face regulatory action. It directly measures solvency capacity."),
            _mcq("A P&C insurer expects to pay hurricane claims unpredictably within 30-60 days. How should this liability profile affect its investment portfolio versus a life insurer with 30-year annuity obligations?",
                 ["The P&C insurer should hold more long-duration bonds to earn higher yields",
                  "The P&C insurer should hold shorter-duration, more liquid assets to match its near-term liability profile",
                  "Both insurers should hold identical portfolios since both are insurance companies",
                  "The P&C insurer should hold private equity to maximize returns for shareholders"],
                 1,
                 "Asset-liability matching requires aligning asset duration with liability duration. P&C claims are short-term and unpredictable, requiring liquid, short-duration assets. Life annuities are long-term and predictable, supporting longer-duration, higher-yielding investments."),
            _scenario(
                "Allstate's CIO is reviewing the portfolio: current yield is 4.8% and the 5-year T-bill rate is 4.2%. The CIO proposes shifting 20% of the portfolio from T-bills into 30-year BBB corporate bonds yielding 6.5% to increase investment income. Allstate writes primarily homeowners and auto insurance with 12-month policy terms.",
                "What is the MOST significant concern with this proposal?",
                [("The proposal is ideal â€” higher yield always improves the spread", False,
                  "Higher yield comes with higher risk. The specific concern here is duration mismatch: Allstate has 12-month liabilities but would hold 30-year bonds."),
                 ("The 30-year bonds create a severe duration and liquidity mismatch with Allstate's short-term P&C liabilities", True,
                  "Correct. Allstate's P&C claims are short-term. Holding 30-year BBB bonds is both illiquid (hard to sell in a claims surge) and exposes the portfolio to enormous interest rate risk over a 30-year horizon that doesn't match Allstate's business model."),
                 ("BBB bonds are too high-quality for a P&C insurer â€” junk bonds would earn more", False,
                  "BBB bonds are investment-grade and appropriate quality-wise. The issue is duration and liquidity mismatch with short-term P&C liabilities, not credit quality.")]
            ),
        ]
    )

    # Concept 2: Investment Policy Statements and Asset Allocation
    c2 = _concept(
        m1_id, 2,
        "Investment Policy Statements and Asset Allocation",
        "Describe the purpose and key components of an Investment Policy Statement (IPS), and explain how strategic asset allocation is determined for institutional portfolios.",
        "An Investment Policy Statement (IPS) is the master governing document for an investment portfolio. It defines who can invest what, in what amounts, under what rules, and how performance will be measured. Without an IPS, portfolio managers have no guidelines and boards have no governance. Asset allocation â€” how much goes into equities, bonds, real estate, and alternatives â€” is the single most important investment decision, responsible for over 90% of long-run portfolio returns according to research by Brinson, Hood, and Beebower.",
        "The California Public Employees' Retirement System (CalPERS) manages $460 billion with a comprehensive IPS. Its Strategic Asset Allocation targets: 42% global equities, 28% fixed income, 15% private equity, 10% real assets, 5% inflation-sensitive. Each allocation has a benchmark, a policy range (e.g., fixed income: 24-32%), and a review trigger if weights deviate more than 3% from target. Every investment decision made by CalPERS's 200+ investment professionals must conform to this IPS. Boards review the IPS annually and must vote to change any policy allocation.",
        [
            "The IPS is the governing document defining investment objectives, constraints, and allowed activities.",
            "Asset allocation (stock/bond/real estate mix) determines more than 90% of long-run portfolio returns.",
            "Policy ranges allow tactical tilts without board approval; major changes require board vote.",
            "Performance measurement: each asset class has a benchmark (e.g., S&P 500 for US equities).",
        ],
        [
            "Thinking the IPS is just administrative paperwork â€” it is the highest-level governance document for institutional investing.",
            "Confusing strategic asset allocation (long-term target mix) with tactical asset allocation (short-term tilts).",
            "Assuming all insurers have the same IPS â€” it must be customized to each institution's liabilities, risk tolerance, and regulatory context.",
        ],
        lessons=[
            _intro("The Master Blueprint: What Is an Investment Policy Statement?",
                   "Imagine building a skyscraper without blueprints. Every institutional investment portfolio needs its equivalent â€” an Investment Policy Statement that defines what the portfolio is for, what it can invest in, and how it will be measured."),
            _teach("Investment Policy Statement: Components and Purpose",
                   "An IPS is a formal written document that establishes the framework for all investment decisions. Its key components are: (1) Portfolio Objectives â€” target return, risk tolerance; (2) Investment Constraints â€” what cannot be held, maximum exposures; (3) Strategic Asset Allocation â€” target percentages in each asset class with policy ranges; (4) Performance Benchmarks â€” what each asset class is measured against; (5) Rebalancing Guidelines â€” when/how to return to target weights; (6) Governance â€” who approves what decisions. The IPS is approved by the board and reviewed at least annually.",
                   ["IPS is a board-level governance document, not day-to-day management guidance.",
                    "Target return should be net of fees and aligned with liability obligations.",
                    "Policy ranges (e.g., equities 35-45%) allow flexibility without constant board approval.",
                    "Benchmarks enable performance attribution: did the manager add value versus the index?"]),
            _teach("Strategic Asset Allocation: The Most Important Decision",
                   "Strategic asset allocation (SAA) determines the long-term target percentage of the portfolio in each asset class (e.g., 40% bonds, 35% equities, 15% real estate, 10% alternatives). Research shows SAA accounts for over 90% of a portfolio's long-run return variation. SAA is set based on the institution's return requirements, risk tolerance, liability profile, and time horizon. It changes rarely â€” only when the institution's fundamental situation changes. Tactical asset allocation (TAA) is the short-term deviation from SAA to exploit market opportunities.",
                   ["SAA is the long-term target mix â€” rarely changes.",
                    "TAA is short-term deviation from SAA within the IPS policy ranges.",
                    "SAA determines over 90% of long-run portfolio returns (Brinson, Hood, Beebower 1986/1991).",
                    "Rebalancing restores portfolio to SAA when market movements cause drift."]),
            _example("CalPERS Strategic Asset Allocation in Practice",
                     "CalPERS, managing $460 billion for California public employees, sets its SAA in a 4-year Asset-Liability Management study. The 2022 study concluded: given that benefits payments will grow 4.5% annually, CalPERS needs a 7% net return assumption. To achieve 7%: 42% global equities (expected return 9.5%), 28% fixed income (4.5%), 15% private equity (11%), 10% real assets (7%), 5% inflation-sensitive (6%). Each asset class has a 3-percentage-point policy range. If equities surge to 50% of the portfolio, the team rebalances back toward 42% by selling equities and buying other asset classes.",
                     "SAA is not a guess â€” it is derived from liability requirements, return assumptions for each asset class, and long-term risk tolerance of the institution."),
            _flash("What is the difference between strategic and tactical asset allocation?",
                   "Strategic asset allocation (SAA) is the long-term target mix (e.g., 40% bonds, 35% equities) set by the IPS. Tactical asset allocation (TAA) is a short-term deviation from SAA (within IPS ranges) to exploit market opportunities, then reverting back."),
            _mcq("Which of the following is the PRIMARY purpose of an Investment Policy Statement?",
                 ["To specify the exact securities to buy in each quarter",
                  "To establish the governance framework, objectives, constraints, and asset allocation guidelines for an investment portfolio",
                  "To guarantee minimum portfolio returns to stakeholders",
                  "To replace the need for professional investment managers"],
                 1,
                 "The IPS is a governance framework document. It sets objectives, constraints, and allocation guidelines â€” but does NOT specify individual securities or guarantee returns. Investment managers operate within the IPS boundaries."),
            _mcq("Research by Brinson, Hood, and Beebower found that strategic asset allocation explains what percentage of long-run portfolio return variation?",
                 ["About 25%", "About 50%", "More than 90%", "Exactly 100%"],
                 2,
                 "The landmark Brinson, Hood, and Beebower studies found that strategic asset allocation policy explains more than 90% of the variation in long-run portfolio returns. Individual security selection and market timing account for less than 10% combined."),
            _mcq("An insurance company's IPS specifies that equity investments must remain between 20% and 30% of the portfolio. Currently equities have risen to 34%. What action is required?",
                 ["No action â€” the IPS is a guideline, not a binding rule",
                  "Immediately liquidate all equity positions",
                  "Rebalance by selling equities until the allocation returns within the 20-30% policy range",
                  "Increase the policy range to 20-40% to accommodate the current allocation"],
                 2,
                 "When portfolio weights drift outside IPS policy ranges, rebalancing is required to restore adherence. Selling 4-14% of the equity position (depending on exact target) returns the portfolio to compliance. Changing the policy range requires board approval."),
            _mcq("Which component of an IPS ensures that portfolio managers are held accountable for their performance?",
                 ["Investment constraints section",
                  "Performance benchmarks and evaluation criteria",
                  "Asset allocation policy ranges",
                  "Governance and approval procedures"],
                 1,
                 "Performance benchmarks (e.g., 'the fixed income portfolio should outperform the Bloomberg Aggregate Bond Index') make accountability objective and measurable. Without benchmarks, assessing whether a manager added value is impossible."),
            _mcq("A life insurer has 30-year fixed annuity liabilities. Which strategic asset allocation BEST reflects appropriate asset-liability management?",
                 ["50% 1-year T-bills, 30% money market, 20% equities",
                  "60% long-duration investment-grade bonds, 25% equities, 15% real assets",
                  "100% equity index funds for maximum return",
                  "50% private equity, 50% hedge funds"],
                 1,
                 "Long-duration annuity liabilities require long-duration assets to immunize interest rate risk. A 60% allocation to long-duration bonds matches the liability profile. Equities and real assets provide return enhancement. Short-duration instruments (T-bills) would create massive ALM mismatch."),
            _scenario(
                "The board of Protective Life Insurance reviews the proposed IPS. The investment committee suggests: target return of 6%, equity allocation 45% (policy range 35-55%), fixed income 40% (policy range 30-50%), alternatives 15%. The company's actuaries note that reserves require a 5.5% return and the company has a conservative regulatory capital position.",
                "Which aspect of the proposed IPS deserves the most scrutiny?",
                [("The 6% return target is appropriate and the equity range is fine for any insurer", False,
                  "A 45% equity allocation (potentially up to 55% at the top of the range) may be too aggressive for an insurance company with solvency constraints. Regulators may penalize high equity concentrations."),
                 ("The equity policy range of 35-55% may be too wide and too high for a regulated life insurer focused on solvency", True,
                  "Correct. Insurance regulators charge higher capital against equities (due to higher volatility). A 55% maximum equity allocation could strain RBC ratios. Given 5.5% reserve requirements and the 6% target, a more balanced equity/bond split with a tighter range is prudent."),
                 ("The 5.5% actuarial reserve requirement means the 6% target is dangerously low and must be raised to 9%", False,
                  "A 6% target provides 0.5% spread above the 5.5% reserve requirement, which is reasonable. The issue is asset allocation risk, not the return target level.")]
            ),
        ]
    )

    m1["concepts"] = [c1, c2]

    # â”€â”€ Module 2: Life Insurer Constraints â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    m2_id = _id()
    m2 = {"id": m2_id, "chapter_id": ch_id, "order": 2,
          "title": "Investment Constraints for Life Insurers"}

    # Concept 3: Life Insurer Investment Objectives
    c3 = _concept(
        m2_id, 1,
        "Investment Objectives for Life Insurers: Income, Risk-Adjusted Returns, and Solvency",
        "Describe the specific investment objectives of life insurers â€” investment income adequacy, risk-adjusted return targets, solvency maintenance, and supporting liquidity â€” and explain why each is prioritized.",
        "Life insurance investment management is not about maximum returns â€” it is about surviving and thriving over a 30-50 year horizon while honoring every policyholder commitment. This means: earning enough investment income to cover guaranteed credited rates plus expenses, generating risk-adjusted (not absolute) returns, maintaining solvency ratios well above regulatory minimums, and keeping enough liquid assets to handle any conceivable claims scenario. Each objective feeds into the others â€” fail any one and the entire enterprise is at risk.",
        "MetLife, with $450 billion in general account assets, publishes specific investment objectives in its IPS: (1) Earn investment income to achieve a 1.5% net spread after credited rates; (2) Maintain risk-adjusted return above 7.5% on invested assets; (3) Keep RBC ratio above 400% (regulatory minimum is 200%); (4) Hold 8% of assets in cash/liquid instruments at all times. In 2020, when COVID caused a credit market disruption, MetLife's 400% RBC target proved critical â€” they absorbed $1.8 billion in credit losses without breaching solvency thresholds.",
        [
            "Life insurer primary objective: earn investment income exceeding the guaranteed credited rate to policyholders.",
            "Risk-adjusted return (Sharpe ratio or return per unit of risk) is more important than raw return.",
            "Solvency target: RBC ratio well above the 200% regulatory action level (most insurers target 350-450%).",
            "Liquidity objective: sufficient cash reserves to pay claims without forced asset sales.",
        ],
        [
            "Confusing total return with investment income â€” life insurers primarily need cash income (coupons, dividends) not just mark-to-market appreciation.",
            "Thinking solvency and liquidity are the same â€” solvency is a balance sheet concept; liquidity is a cash flow concept.",
            "Assuming the investment income objective is fixed â€” it changes as the insurer writes new business with different credited rates.",
        ],
        lessons=[
            _intro("Life Insurance Investing: A 50-Year Business Requiring Precision",
                   "When someone buys a whole life policy at age 30, their insurer makes a promise to pay a death benefit in perhaps 50 years. Managing investments to honor that promise â€” while earning a spread to stay profitable â€” demands extraordinary discipline and clear objectives."),
            _teach("Investment Income Objective: The Spread Must Be Positive",
                   "A life insurer's most fundamental investment objective is earning enough income to cover its cost of funds. The 'cost of funds' is the interest rate guaranteed or credited to policyholders. If policyholders are credited 3.5% and the insurer earns 5%, the spread is 1.5% â€” the source of profit. If interest rates fall and the portfolio now only earns 3%, but policyholders are still guaranteed 3.5%, the spread is -0.5% â€” the insurer is losing money on every policy. This is why life insurers invest heavily in long-duration bonds that lock in yields matching their long-term obligations.",
                   ["Investment income objective: earn a positive spread above the credited/guaranteed rate.",
                    "Spread = investment income yield - credited rate - operating expenses.",
                    "Negative spread (earned less than credited) is financially destructive for a life insurer.",
                    "Long-duration bonds lock in yields over the same horizon as long-term life policies."]),
            _teach("Risk-Adjusted Returns, Solvency, and Liquidity Objectives",
                   "Beyond income, life insurers target risk-adjusted returns â€” maximizing return per unit of risk taken. They use metrics like the Sharpe ratio and return on risk-adjusted capital (RORAC) to evaluate investment decisions. Solvency objectives translate to maintaining RBC ratios well above regulatory minimums â€” most life insurers target 350-450% of the 200% minimum. Liquidity objectives are quantified as a percentage of assets that must be held in cash or instruments convertible to cash within 5 business days without significant price concession.",
                   ["Risk-adjusted return = return earned per unit of risk; prevents chasing yield without risk awareness.",
                    "RBC ratio target: 350-450% vs. regulatory minimum of 200%.",
                    "Liquidity reserve: typically 5-10% of general account assets in highly liquid instruments.",
                    "Liquidity stress testing: can the insurer survive a 10x normal claim week without forced selling?"]),
            _example("MetLife's COVID-19 Solvency Test",
                     "In March 2020, COVID-19 triggered a credit market dislocation. Corporate bond spreads widened 300 basis points in three weeks, causing mark-to-market losses across all corporate bond portfolios. MetLife's $450 billion general account held 55% in investment-grade corporate bonds. The spread widening caused roughly $22 billion in unrealized mark-to-market losses. MetLife's RBC ratio, which had stood at 418% in December 2019, fell to 385% by March 2020 â€” still well above MetLife's internal 350% target. Because MetLife had maintained its solvency buffer, it had the luxury of holding positions through the crisis. By December 2020, spreads recovered and the portfolio had fully recovered its value.",
                     "Maintaining RBC ratios well above regulatory minimums creates the 'staying power' to hold through credit dislocations without being forced to crystallize losses."),
            _flash("What is Risk-Based Capital (RBC) ratio and why do insurers target above 300%?",
                   "RBC ratio = actual capital / risk-weighted minimum capital required by regulators. Minimum is 200%; below 150% triggers regulatory takeover. Insurers target 350-450% to create a buffer absorbing unexpected losses (credit events, catastrophes) without triggering regulatory action."),
            _mcq("A life insurer's portfolio earns 4.8%. It guarantees policyholders a 4.0% credited rate and has 0.5% operating expenses. What is the net investment spread?",
                 ["4.8%", "0.8%", "0.3%", "4.3%"],
                 2,
                 "Net spread = Investment income - Credited rate - Expenses = 4.8% - 4.0% - 0.5% = 0.3%. This thin spread means the insurer earns only 0.3 cents of profit per dollar of policy in force â€” a very slim margin that illustrates why interest rate management is critical."),
            _mcq("Why do life insurers prioritize investment income return over capital gains?",
                 ["Capital gains are prohibited by life insurance regulations",
                  "Investment income (coupons, dividends) provides predictable cash to pay claims; capital gains require selling assets",
                  "Capital gains are taxed at 100% for life insurers",
                  "Investment income always exceeds capital gains in bond portfolios"],
                 1,
                 "Life insurers need cash to pay claims â€” they cannot wait to sell assets to generate cash. Investment income (bond coupons, dividends) provides a steady, predictable cash stream. Capital gains only generate cash when assets are sold."),
            _mcq("Which statement about Risk-Based Capital (RBC) requirements is MOST accurate?",
                 ["RBC is a voluntary guideline that insurers may choose to follow",
                  "An insurer with RBC below 150% of the minimum faces regulatory takeover",
                  "All life insurers must maintain exactly 200% RBC regardless of risk profile",
                  "RBC only applies to property and casualty insurers, not life insurers"],
                 1,
                 "Below 150% RBC (the 'mandatory control level'), regulators are required to take corrective action including potential takeover. At 200%, regulatory oversight increases. Most life insurers self-impose targets of 350-450% to maintain operating flexibility."),
            _mcq("Which of the following investments BEST supports a life insurer's investment income objective while matching long-term policy liabilities?",
                 ["3-month Treasury bills",
                  "Equity index funds",
                  "20-year investment-grade corporate bonds with fixed coupons",
                  "Private equity with a 10-year lockup period"],
                 2,
                 "20-year corporate bonds provide: fixed coupon income (steady cash for claims), long duration (matching long-term policy liabilities), investment-grade quality (manageable credit risk). T-bills are too short. Equities provide capital gains not income. Private equity is illiquid."),
            _mcq("A life insurer's liquidity objective requires 8% of assets in cash/liquid instruments. With $200 billion in assets, a catastrophic event causes $20 billion in claims. What happens?",
                 ["The insurer must immediately sell all equity holdings to raise cash",
                  "The insurer uses its $16 billion liquidity reserve and supplements with asset sales if needed",
                  "The insurer cannot pay claims and must seek regulatory assistance",
                  "The insurer uses only new premium income to pay claims"],
                 1,
                 "$200B x 8% = $16B in liquid assets. The $20B claim surge would draw down the full liquid reserve plus require an additional $4B from asset sales. This is a stress scenario â€” most liquidity objectives are calibrated for normal variability, with contingency plans (credit lines, reinsurance) for catastrophic events."),
            _scenario(
                "Lincoln National's CIO reviews the quarterly investment report. The portfolio earns 5.2% investment income. Credited rate to policyholders: 4.5%. Operating expense ratio: 0.4%. RBC ratio: 310% (target: 400%). Liquidity reserve: 6% (policy: 8% minimum). Two credit rating downgrades are pending in the corporate bond portfolio.",
                "Which issue requires the MOST URGENT attention?",
                [("The investment income spread of 0.3% â€” this must be immediately increased to 2%+", False,
                  "A 0.3% net spread (5.2% - 4.5% - 0.4%) is thin but positive. While improvement is needed, this is a medium-term strategic concern, not an immediate crisis."),
                 ("The liquidity reserve at 6% is below the 8% minimum policy requirement", True,
                  "Correct. The liquidity reserve is below the minimum policy threshold. With two credit downgrades pending (which could trigger accelerated policy surrenders), liquidity must be immediately restored to policy minimum. An asset fire sale risk exists if claims surge while liquidity is deficient."),
                 ("The RBC ratio of 310% is below the 200% regulatory minimum and requires emergency capital injection", False,
                  "310% RBC is ABOVE the 200% regulatory minimum. It is below Lincoln National's internal target of 400%, which is a medium-term concern requiring a capital restoration plan â€” but it is not an immediate regulatory crisis.")]
            ),
        ]
    )

    # Concept 4: Regulatory and Rating Constraints
    c4 = _concept(
        m2_id, 2,
        "Investment Constraints for Life Insurers: Regulatory and Rating Requirements",
        "Identify the key investment constraints facing life insurers â€” including regulatory capital charges, asset eligibility rules, single-issuer limits, and rating agency requirements â€” and explain how each constrains portfolio construction.",
        "Life insurers do not have unlimited freedom to invest. State insurance regulators impose strict constraints: minimum credit quality, maximum exposure to any single issuer, limits on equity and alternative investments, and capital charges for risky assets. On top of regulatory constraints, rating agencies (S&P, Moody's, A.M. Best) impose their own capital models that penalize risky investments with higher capital requirements. A portfolio that looks attractive from a pure return perspective may be disqualified by regulatory rules or rating constraints.",
        "New York Life, the largest US mutual life insurer, operates under New York Insurance Law Section 1407, which limits equity investments to 20% of admitted assets, caps any single issuer at 5% of admitted assets, prohibits below-investment-grade bonds from exceeding 20% of the bond portfolio, and requires 50% of bonds to be rated A or higher by NRSRO. Additionally, A.M. Best requires New York Life to hold 8% more capital for every dollar of BB-rated bonds than for A-rated bonds. These constraints mean New York Life's CIO cannot simply buy the highest-yielding assets â€” the regulatory and rating costs must be calculated into every investment decision.",
        [
            "Insurance regulators impose: maximum single-issuer concentration (typically 3-5%), limits on equity (10-20%), caps on below-investment-grade bonds.",
            "Rating agencies (S&P, Moody's, A.M. Best) impose capital charges on risky assets that function as additional constraints.",
            "NAIC designates bond quality (1-6) â€” bonds rated below NAIC-2 (BBB) face increasing capital charges.",
            "Asset eligibility rules determine what can be counted as 'admitted assets' on an insurer's balance sheet.",
        ],
        [
            "Confusing regulatory capital charges with credit quality â€” they are related but not identical (some AAA structured products had high capital charges post-2008).",
            "Assuming constraints apply uniformly â€” New York-domiciled insurers face different rules than Texas-domiciled insurers.",
            "Thinking constraints only reduce returns â€” they also protect policyholders and maintain market confidence in the industry.",
        ],
        lessons=[
            _intro("Why Can't an Insurer Just Buy the Highest-Yielding Investments?",
                   "A life insurer sits at the intersection of two powerful forces: market opportunities and regulatory constraints. Understanding what insurers CANNOT do is just as important as understanding what they can do â€” because constraints shape the entire portfolio."),
            _teach("Regulatory Investment Constraints: What Insurers Must Follow",
                   "State insurance regulators impose mandatory investment constraints to protect policyholders. Key constraints: (1) Eligible investment rules â€” insurers can only hold 'admitted assets' (bonds, mortgages, some equities, real estate); (2) Single-issuer limits â€” typically 3-5% maximum exposure to any one issuer; (3) Asset quality limits â€” minimum credit rating requirements (most states require investment grade for at least 75-80% of bonds); (4) Concentration limits â€” equity cannot exceed 10-20% of assets; alternatives capped at 3-5%; (5) NAIC designation system â€” assigns quality ratings 1-6, with higher designations triggering capital charges.",
                   ["Admitted assets are investments eligible to count toward meeting policyholder obligations.",
                    "NAIC-1 = AAA/AA, NAIC-2 = A/BBB (investment grade), NAIC-3 to NAIC-6 = below investment grade (increasing charges).",
                    "Single-issuer limits prevent catastrophic concentration if one issuer defaults.",
                    "Each state sets its own rules â€” New York (strictest), California, Texas have specific requirements."]),
            _teach("Rating Agency Capital Models: The Second Layer of Constraints",
                   "Beyond regulatory constraints, rating agencies (S&P, Moody's, A.M. Best) run their own capital adequacy models for insurers seeking high ratings. These models impose risk charges: equities are assigned 35-50% capital charge (must hold $0.35-0.50 capital per $1 of equities), below-investment-grade bonds carry 5-15% charges, real estate carries 8-10% charges. An insurer targeting an A.M. Best 'A' rating must hold enough capital to pass A.M. Best's stress test. This means holding more capital against risky assets, which reduces the portfolio's effective return on equity.",
                   ["Rating agency capital charges are in ADDITION to regulatory capital requirements.",
                    "Higher investment risk = more capital required = lower return on equity.",
                    "Insurers targeting top ratings (A+ or better) have tighter effective investment constraints than lower-rated peers.",
                    "Capital charges vary by asset type: equities > real estate > below-IG bonds > IG bonds > government bonds."]),
            _example("New York Life's Constraint Matrix in Action",
                     "New York Life's CIO considers buying $500 million of BB-rated telecom bonds yielding 7.5%, compared to A-rated telecom bonds yielding 5.5%. The yield pickup of 2% seems attractive. But the analysis shows: (1) Regulatory: BB bonds count as NAIC-3, requiring New York Life to hold $75M additional capital vs. only $15M for A-rated bonds ($60M capital difference). (2) A.M. Best: BB bonds require 8% capital charge vs. 2% for A-rated bonds â€” another $30M of capital tied up. (3) Concentration: already at 4% single-issuer limit; would need to reduce other telecom holdings. After accounting for the capital cost of holding the extra $90M in required capital (at 8% cost of capital = $7.2M annual cost), the effective yield advantage of the BB bonds falls from 2% to just 0.5% â€” not enough for the added credit risk.",
                     "Regulatory and rating constraints transform investment decisions from simple yield comparisons into comprehensive capital cost analyses."),
            _flash("What is the NAIC designation system for bond investments?",
                   "NAIC-1 = highest quality (AAA/AA), NAIC-2 = investment grade (A/BBB), NAIC-3 to NAIC-6 = below investment grade with progressively higher capital charges. Most states require insurers to hold minimum capital proportional to NAIC designation â€” lower quality bonds require more capital."),
            _mcq("Which type of investment typically faces the HIGHEST regulatory capital charge for a life insurer?",
                 ["US Treasury bonds", "AAA-rated corporate bonds", "Investment-grade municipal bonds", "Common equity investments"],
                 3,
                 "Equities (common stocks) carry the highest regulatory capital charges â€” typically 30-50% in NAIC's risk-based capital framework. This reflects their higher volatility and potential for significant loss in market downturns, compared to bonds which have more predictable cash flows."),
            _mcq("Why do state insurance regulators impose single-issuer concentration limits?",
                 ["To prevent insurers from earning too high a return on any one investment",
                  "To protect policyholders from catastrophic loss if a single major issuer defaults",
                  "To ensure insurers hold only government bonds",
                  "To limit the number of securities in the portfolio for administrative simplicity"],
                 1,
                 "Single-issuer limits (typically 3-5% of assets) prevent catastrophic concentration losses. If an insurer held 20% of assets in one company and that company defaulted, the solvency of the insurer could be threatened. Diversification limits this specific risk exposure."),
            _mcq("An insurer's bond is downgraded from NAIC-2 (BBB) to NAIC-3 (BB). What is the MOST LIKELY immediate consequence?",
                 ["The insurer must immediately sell the bond at any price",
                  "The insurer faces no regulatory consequences as long as it holds the bond to maturity",
                  "The insurer must hold additional regulatory capital against the downgraded bond",
                  "The bond is reclassified as an equity investment"],
                 2,
                 "When a bond is downgraded, its NAIC designation worsens, requiring the insurer to hold more Risk-Based Capital against it. This increases the capital cost of the holding. The insurer doesn't have to sell immediately, but the effective cost of holding increases, often prompting eventual sale."),
            _mcq("A life insurer's IPS states maximum equity allocation of 15% of admitted assets. The insurer has $100 billion in admitted assets. What is the maximum equity portfolio size?",
                 ["$100 billion", "$85 billion", "$15 billion", "$1.5 billion"],
                 2,
                 "$100 billion x 15% = $15 billion maximum equity allocation. This constraint reflects both regulatory limits and the higher capital charges on equities that would impair the insurer's RBC ratio if exceeded."),
            _mcq("Which rating agency provides credit ratings specifically focused on insurance company financial strength?",
                 ["MSCI", "Morningstar", "A.M. Best", "Fitch Investor Services"],
                 2,
                 "A.M. Best specializes in evaluating insurance company financial strength, operating performance, and balance sheet stability. While S&P and Moody's also rate insurers, A.M. Best is the industry-specific rater that insurance regulators and policyholders rely on most heavily."),
            _scenario(
                "Transamerica Life's investment team identifies an opportunity: $1 billion of single-B rated private placement bonds yielding 9.5%. The current portfolio yield is 5.2%, and the target is 5.8%. The bonds are from a single healthcare issuer. Current equity allocation: 18% (regulatory limit: 20%). Current single-issuer maximum: already at 4.5% for this issuer.",
                "Why should Transamerica decline this investment?",
                [("The 9.5% yield is too high â€” it signals the bonds are mispriced and overvalued", False,
                  "High yield signals high risk, not overvaluation. The actual constraints here are regulatory and concentration related."),
                 ("Single-B bonds would breach NAIC quality standards and the issuer exposure already at the single-issuer maximum", True,
                  "Correct. Single-B is NAIC-5 (near default category) â€” most insurer IPS prohibit or severely limit NAIC-4/5 bonds. Additionally, adding $1B to a healthcare issuer where Transamerica already has 4.5% exposure would likely breach the 5% single-issuer limit, creating dangerous concentration risk."),
                 ("The 9.5% yield exceeds the IPS target return, making it ineligible", False,
                  "Exceeding the return target is not a reason to decline. The issues are credit quality (single-B = NAIC-5) and concentration (already at 4.5% single-issuer limit) â€” regulatory and IPS violations.")]
            ),
        ]
    )

    m2["concepts"] = [c3, c4]
    ch["modules"] = [m1, m2]
    return ch




def _build_ch6(course_id):
    ch_id = _id()
    ch = {
        "id": ch_id, "course_id": course_id, "order": 6,
        "title": "Risk Management and the Investment Function",
        "description": "Enterprise Risk Management frameworks, Asset-Liability Management (ALM) systems and organization, portfolio segmentation, cash-flow testing, and ALM investment strategies including immunization, dedication, and interest-rate anticipation.",
    }

    # â”€â”€ Module 1: ERM and ALM Framework â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    m1_id = _id()
    m1 = {"id": m1_id, "chapter_id": ch_id, "order": 1,
          "title": "Enterprise Risk Management and Asset-Liability Management"}

    # Concept 1: Enterprise Risk Management and ALM Systems
    c1 = _concept(
        m1_id, 1,
        "Enterprise Risk Management and Asset-Liability Management",
        "Define Enterprise Risk Management (ERM) and Asset-Liability Management (ALM), explain how they relate to each other, and describe the organizational structure that supports both functions at a life insurance company.",
        "Enterprise Risk Management (ERM) is the company-wide framework for identifying, measuring, managing, and monitoring ALL risks â€” including investment risk, insurance underwriting risk, operational risk, and strategic risk. Asset-Liability Management (ALM) is the specific subprocess within ERM that focuses on coordinating assets with liabilities to manage interest rate risk and ensure the company can meet its obligations. ERM is the umbrella; ALM is one critical function under it. Together, they prevent the most dangerous scenario for an insurer: a mismatch between what it owes policyholders and what its investments will deliver.",
        "Prudential Financial's ERM framework encompasses 15 risk categories managed by a Chief Risk Officer and Risk Committee. Within ERM, the ALM function manages $350 billion in general account assets against $320 billion in actuarially determined liabilities. The ALM committee meets monthly to review duration gaps (assets vs. liabilities), convexity mismatches, and cash-flow projections under 12 interest rate scenarios. In 2013, when the 10-year Treasury rose from 1.6% to 3.0% in 6 months, Prudential's ALM team had already shortened asset duration in Q1 â€” resulting in only $2.1 billion unrealized loss vs. an estimated $8 billion if they had been passively matched.",
        [
            "ERM = company-wide risk framework covering investment, underwriting, operational, and strategic risks.",
            "ALM = subset of ERM focused on coordinating assets with liabilities to manage interest rate risk.",
            "Organization: Risk Committee (board-level), ALM Committee (management-level), ALM Unit (day-to-day execution).",
            "Duration gap = asset duration minus liability duration; zero gap = fully immunized against interest rate changes.",
        ],
        [
            "Confusing ERM (broad, all risks) with ALM (narrow, assets vs. liabilities focus).",
            "Thinking the Risk Committee manages day-to-day investments â€” it sets policy; the ALM Unit executes.",
            "Assuming zero duration gap is always optimal â€” some interest rate exposure may be deliberately accepted for return enhancement.",
        ],
        lessons=[
            _intro("When Assets and Liabilities Clash: The Risk at the Heart of Insurance",
                   "An insurance company lives and dies by one thing: its ability to pay what it promised. When assets and liabilities get out of sync, even a healthy insurer can face crisis. Enterprise Risk Management and ALM are the systems that prevent this."),
            _teach("Enterprise Risk Management: The Big Picture",
                   "ERM is a holistic, enterprise-wide framework that identifies and manages all material risks facing an insurance company. These include: investment risk (market, credit, liquidity, ALM), insurance risk (mortality, morbidity, lapse), operational risk (systems, fraud, legal), and strategic risk (competitive, regulatory, reputational). A Chief Risk Officer (CRO) typically leads ERM, reporting to both the CEO and the board's Risk Committee. The CRO aggregates risk across all categories to ensure the total risk taken is within the board's approved risk appetite.",
                   ["ERM covers ALL risks â€” not just investments.",
                    "CRO aggregates risk exposures and reports total risk to board.",
                    "Risk appetite = maximum risk the board approves for the organization.",
                    "ERM ensures no single risk becomes existential, even if individually each seems manageable."]),
            _teach("Asset-Liability Management: Coordinating Both Sides of the Balance Sheet",
                   "ALM is the process of coordinating investment decisions (assets) with actuarial projections (liabilities) to ensure the insurer can meet all policyholder obligations under a range of economic scenarios. The core metric is duration gap: if assets have duration 12 and liabilities have duration 15, the duration gap is -3 years â€” meaning if rates rise 1%, assets fall 12% but liabilities fall 15%, actually improving solvency. The ALM Committee (senior management) sets the allowed duration gap range. The ALM Unit (technical staff) executes trades to keep the portfolio within the gap range.",
                   ["Duration gap = asset duration - liability duration.",
                    "Positive gap: assets more interest-rate sensitive â€” insurer hurt by rising rates.",
                    "Negative gap: liabilities more interest-rate sensitive â€” insurer benefits if rates rise.",
                    "Zero duration gap = immunized â€” no net interest rate risk."]),
            _example("Prudential's 2013 Rate Rise and ALM Defense",
                     "In May 2013, the Federal Reserve hinted at tapering bond purchases ('Taper Tantrum'). The 10-year Treasury yield shot from 1.6% to 3.0% over five months. Prudential's ALM team had been monitoring the duration gap quarterly. In Q1 2013, seeing the gap had drifted to +2.5 years (assets more sensitive than liabilities), the team sold $8 billion of 30-year bonds and bought $10 billion of 5-year bonds, reducing asset duration. When rates spiked, Prudential's assets fell $2.1 billion in market value â€” painful but manageable. A passive insurer with a +5 year gap would have suffered $8 billion in losses. The ALM system paid for itself many times over.",
                     "Proactive duration management through ALM can save billions when interest rate environments shift unexpectedly."),
            _flash("What is a 'duration gap' in Asset-Liability Management?",
                   "Duration gap = asset duration minus liability duration. A positive gap means assets are more interest-rate sensitive than liabilities; a negative gap means liabilities are more sensitive. A zero gap means the insurer is immunized against parallel shifts in the yield curve."),
            _mcq("Which organizational body typically sets the overall risk appetite for an insurance company under an ERM framework?",
                 ["The Chief Investment Officer", "The ALM Unit", "The Board of Directors or Board Risk Committee", "The ALM Committee"],
                 2,
                 "The Board of Directors (or its Risk Committee) sets the organization's overall risk appetite â€” the maximum risk the company is willing to take across all categories. Management (including the CRO and ALM Committee) then operates within these board-approved boundaries."),
            _mcq("An insurer's investment portfolio has a duration of 10 years and its liabilities have a duration of 14 years. What is the duration gap and what does it imply?",
                 ["Gap = -4 years; liabilities are more interest-rate sensitive than assets",
                  "Gap = +4 years; assets are more interest-rate sensitive than liabilities",
                  "Gap = 24 years; the insurer has twice the exposure it needs",
                  "Gap = 0; the insurer is perfectly immunized"],
                 0,
                 "Duration gap = asset duration - liability duration = 10 - 14 = -4 years. A negative gap means liabilities are more sensitive â€” when rates rise, liabilities fall more than assets, improving solvency. When rates fall, liabilities rise more, hurting solvency. The insurer is exposed to falling interest rates."),
            _mcq("What is the primary difference between the ALM Committee and the ALM Unit?",
                 ["The ALM Committee manages daily trading; the ALM Unit sets strategy",
                  "The ALM Committee sets strategy and policy; the ALM Unit executes day-to-day operations",
                  "They are the same organizational body with different names",
                  "The ALM Unit reports to the board; the ALM Committee reports to the CRO"],
                 1,
                 "The ALM Committee (senior management) sets the strategy â€” defining acceptable duration gap ranges, approved investment strategies, and ALM benchmarks. The ALM Unit (technical staff, including quantitative analysts and portfolio managers) executes trades and analytical work to implement the committee's strategy."),
            _mcq("Which scenario BEST demonstrates a failure of Enterprise Risk Management?",
                 ["An insurer's equities decline 10% during a market correction",
                  "An insurer's ERM framework failed to identify that its ALM duration gap had grown to +8 years before interest rates rose sharply",
                  "An insurer's CRO presents the board with the quarterly risk report",
                  "An insurer reduces its equity allocation from 20% to 15% following market volatility"],
                 1,
                 "An undetected +8-year duration gap represents a breakdown in ERM â€” specifically, the failure to identify and report a material interest rate risk exposure in time for management to act. When rates then rise sharply, the insurer suffers unnecessary losses that a functioning ERM system would have flagged and prompted corrective action."),
            _mcq("Which of the following BEST describes the goal of ALM for a life insurance company?",
                 ["To maximize investment returns at any level of risk",
                  "To ensure the company can meet all policyholder obligations under various economic scenarios by coordinating asset and liability cash flows",
                  "To eliminate all interest rate risk by holding only floating-rate securities",
                  "To maintain an investment portfolio that always outperforms the stock market"],
                 1,
                 "ALM is about ensuring the insurer can honor its policyholder commitments â€” paying death benefits, annuity payments, and other obligations â€” across a range of interest rate environments. This requires coordinating the timing and amount of asset cash flows with projected liability cash flows."),
            _scenario(
                "Guardian Life's CIO reports to the ALM Committee that the portfolio duration gap has shifted to +5 years (asset duration 15, liability duration 10) following a rally in long-term bonds that increased their prices and reduced their yields. The ALM policy states the gap must remain between -1 and +2 years.",
                "What action should the ALM Committee authorize?",
                [("No action â€” a +5 year gap means higher returns when rates fall", False,
                  "While a +5 gap benefits from falling rates, it also creates massive exposure to rising rates, violating the ALM policy range. The committee cannot accept this risk without board approval."),
                 ("Shorten asset duration by selling long-duration bonds and replacing them with shorter-duration bonds until the gap returns to the allowed range", True,
                  "Correct. The duration gap must be brought back within the -1 to +2 policy range. Selling long-duration assets (high duration, sensitive to rates) and buying shorter-duration assets reduces asset duration and narrows the gap, restoring ALM compliance."),
                 ("Lengthen liability duration by modifying policyholder contracts to extend their terms", False,
                  "Liability duration is determined by existing policyholder contracts â€” an insurer cannot unilaterally change policy terms to manage ALM. Assets must be adjusted to match the fixed liability profile.")]
            ),
        ]
    )

    # Concept 2: Portfolio Segmentation and Investment Income Allocation
    c2 = _concept(
        m1_id, 2,
        "Portfolio Segmentation and Investment Income Allocation",
        "Explain why insurance companies segment their investment portfolios by product line, describe how investment income is allocated across segments, and understand the integrated portfolio benchmarking model.",
        "A large life insurance company sells many different products â€” term life, whole life, fixed annuities, variable annuities, disability income. Each product has a different liability profile: different duration, different cash flow pattern, different interest rate sensitivity. To manage ALM precisely, insurers segment their general account investment portfolio by product line, matching each segment's assets to that product's specific liabilities. Investment income earned in each segment is then allocated back to that product line, allowing accurate pricing and profitability analysis.",
        "John Hancock (Manulife) segments its $200 billion general account into 8 segments: Life Insurance, Individual Annuities, Group Insurance, Long-Term Care, Retirement Plans, and three specialty segments. The life insurance segment holds primarily long-duration corporate bonds (average duration 15 years) to match 30-year policy liabilities. The group insurance segment holds shorter-duration bonds (average 3-5 years) to match annual group policy renewals. Each segment has its own benchmark: the life segment benchmarks to the Bloomberg Long Credit Index; the group segment benchmarks to the Bloomberg 1-5 Year Credit Index. Investment income earned by each segment is credited to that product's income statement.",
        [
            "Portfolio segmentation = dividing the general account portfolio by product line to match each segment's assets to its specific liabilities.",
            "Investment income allocation: income earned in each segment is credited to that product line for profitability analysis.",
            "Integrated portfolio benchmarking: each segment has its own index benchmark reflecting its liability profile.",
            "Segmentation enables precise ALM, accurate product pricing, and fair performance measurement.",
        ],
        [
            "Thinking the entire general account is managed as one portfolio â€” segmentation is standard practice at all major insurers.",
            "Confusing portfolio segmentation (within general account) with separate accounts (variable products managed separately from general account).",
            "Assuming all segments have the same benchmark â€” each segment's benchmark must reflect that segment's liability profile.",
        ],
        lessons=[
            _intro("One Company, Many Portfolios: Why Insurers Segment Their Investments",
                   "A whole life policyholder and a group disability claim have nothing in common from a cash flow perspective. So why would their premium dollars be invested in exactly the same portfolio? They shouldn't â€” and that's why sophisticated insurers segment."),
            _teach("Portfolio Segmentation: Matching Assets to Specific Liability Groups",
                   "Portfolio segmentation divides the general account investment portfolio into sub-portfolios, each matched to a specific product line or liability group. Each segment has: (1) an asset portfolio with duration and cash flows matched to that segment's liabilities; (2) its own investment policy guidelines reflecting the risk tolerance appropriate for those liabilities; (3) performance benchmarks tied to comparable fixed-income indices with similar duration profiles. Segmentation allows the ALM team to manage interest rate risk precisely at the product level rather than averaging across dissimilar liability profiles.",
                   ["Each segment has a unique liability profile driving unique investment needs.",
                    "Life segments: long duration â†’ long-duration corporate bonds.",
                    "Group/P&C segments: short duration â†’ shorter-duration, higher-liquidity bonds.",
                    "Segmentation is more administratively complex but enables superior ALM precision."]),
            _teach("Investment Income Allocation and the Integrated Benchmarking Model",
                   "Investment income must be allocated back to each product segment accurately. This involves: (1) identifying assets assigned to each segment; (2) calculating actual investment income earned by those assets; (3) crediting that income to the product segment's income statement. The Integrated Portfolio Benchmarking Model creates a benchmark for each segment based on its liability profile â€” the benchmark investment policy that would perfectly match the segment's liabilities is the 'neutral position.' Managers are then measured against this neutral benchmark: outperformance = alpha generated by active management.",
                   ["Investment income allocation lets actuaries price products accurately (knowing actual investment income per product line).",
                    "Integrated benchmark = the liability-matching neutral portfolio; manager alpha = actual return minus benchmark return.",
                    "Without allocation, all income pools together and pricing accuracy suffers.",
                    "Regulators require income allocation transparency for certain product lines (e.g., participating life policies)."]),
            _example("John Hancock's 8-Segment Portfolio in Practice",
                     "John Hancock's life insurance segment has $65 billion in assets with average duration 14.2 years, benchmarked to the Bloomberg Long Credit Index. In Q3 2023, the life segment earned 5.85% investment income, outperforming its benchmark (Bloomberg Long Credit) by 0.28% â€” this 28-basis-point alpha was credited entirely to the life segment's income statement, improving life insurance product profitability. The group insurance segment ($30 billion) earned 5.10%, matching its Bloomberg 1-3 Year Credit benchmark within 5 basis points. Each segment's manager receives a performance review showing only the alpha vs. their specific benchmark â€” not the company-wide average.",
                     "Segmentation enables accountability: each manager is measured against the benchmark appropriate for their specific segment's liabilities, not against the same company-wide index."),
            _flash("What is 'portfolio segmentation' in insurance investment management?",
                   "Portfolio segmentation divides the general account investment portfolio into sub-portfolios, each matched to a specific product line (e.g., life insurance, annuities, group insurance). Each segment has assets whose duration, cash flows, and risk profile match that product line's specific liability characteristics."),
            _mcq("Why do insurers segment their investment portfolios by product line?",
                 ["To reduce the number of securities in each portfolio for administrative simplicity",
                  "To precisely match each product line's unique liability cash flows and duration with appropriate assets",
                  "To allow different investment managers to compete within the same company",
                  "To comply with accounting rules that require separate reporting for each product"],
                 1,
                 "Different products have different liability profiles. Term life has short-duration, lump-sum claims. Fixed annuities have 20-30 year predictable cash flows. Segmentation allows precise ALM matching for each liability type, rather than compromising with a one-size-fits-all portfolio."),
            _mcq("An insurer's life insurance segment should MOST LIKELY invest in which type of assets?",
                 ["90-day Treasury bills to ensure maximum liquidity",
                  "Long-duration investment-grade corporate bonds to match long-term life policy liabilities",
                  "Common equity funds for maximum long-term return",
                  "Money market funds to protect against any market risk"],
                 1,
                 "Life insurance liabilities (death benefits, long-term savings) are long-duration. Long-duration corporate bonds match this liability profile, providing the coupon income needed to credit policyholder accounts and the duration match to manage interest rate risk."),
            _mcq("What does the 'integrated portfolio benchmarking model' measure?",
                 ["The absolute return of the total general account portfolio",
                  "The alpha generated by each segment's manager versus the liability-matching neutral benchmark",
                  "The amount of capital required to support each product segment",
                  "The market value of the entire investment portfolio at any point in time"],
                 1,
                 "The integrated benchmarking model creates a 'neutral' benchmark for each segment (the liability-matching portfolio) and measures manager performance against it. The difference (actual return minus benchmark return) is the alpha attributable to the manager's active decisions."),
            _mcq("Investment income allocation in a segmented portfolio primarily serves which purpose?",
                 ["Ensuring all product lines earn the same investment return",
                  "Enabling accurate product profitability analysis and pricing by crediting each product line with the income its assets earned",
                  "Eliminating the need for actuarial reserve calculations",
                  "Maximizing tax efficiency across all product segments simultaneously"],
                 1,
                 "By allocating investment income earned in each segment back to that product's income statement, actuaries and pricing teams can accurately assess product profitability. Without allocation, the same income pools that a profitable annuity segment subsidizes a less profitable life segment, obscuring true product economics."),
            _mcq("Which of the following statements about portfolio segmentation is CORRECT?",
                 ["All product segments within a general account must use the same investment benchmark",
                  "Portfolio segmentation is only required for companies with more than $10 billion in assets",
                  "Each segment has its own benchmark reflecting its specific liability duration and cash flow profile",
                  "Variable product (separate account) assets are included in general account segmentation"],
                 2,
                 "Each segment has its own benchmark â€” the one that matches its specific liability profile. Life segments might benchmark to long-credit indices; group segments to short-credit indices. Variable product assets are in separate accounts (outside the general account) and are NOT part of general account segmentation."),
            _scenario(
                "Pacific Mutual manages a $50 billion general account with two major product segments: (1) Fixed Annuities: $30 billion in assets, liability duration 18 years, currently invested in 5-year bonds (duration 4.5 years). (2) Group Term Life: $20 billion, liability duration 1.5 years, currently invested in 20-year bonds (duration 14 years).",
                "Which segment has the most critical ALM misalignment that requires immediate correction?",
                [("Fixed Annuities â€” the 4.5-year asset duration massively undermatches the 18-year liability duration", True,
                  "Correct. The Fixed Annuity segment has a duration gap of 4.5 - 18 = -13.5 years. This enormous mismatch means that when interest rates fall (likely for long-duration annuities), the liabilities increase far more than the assets, creating massive solvency risk. This is a critical ALM failure."),
                 ("Group Term Life â€” the 14-year bonds are too long for a 1.5-year liability", False,
                  "While the Group Term Life segment also has a mismatch (duration gap = 14 - 1.5 = +12.5 years), the risk is different. For short-duration liabilities (1.5 years), the concern is more liquidity than duration, as claims happen within 1-2 years. The Fixed Annuity mismatch is more existential."),
                 ("Both segments have equal ALM problems that require simultaneous correction", False,
                  "Both have misalignments, but the Fixed Annuity segment's -13.5-year gap (assets far shorter than liabilities) creates immediate solvency risk when rates move. This is the more critical issue requiring immediate rebalancing.")]
            ),
        ]
    )

    m1["concepts"] = [c1, c2]

    # â”€â”€ Module 2: ALM Strategies â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    m2_id = _id()
    m2 = {"id": m2_id, "chapter_id": ch_id, "order": 2, "title": "ALM Strategies and Cash-Flow Testing"}

    # Concept 3: Cash-Flow Testing and ALM Analysis Tools
    c3 = _concept(
        m2_id, 1,
        "Cash-Flow Testing and ALM Analysis Tools",
        "Describe cash-flow testing as an ALM analysis tool, explain how multiple interest rate scenarios are used, and identify the key outputs from ALM analysis that inform portfolio management decisions.",
        "Cash-flow testing is the actuarial process of projecting both asset and liability cash flows under multiple interest rate scenarios to identify whether the insurer can meet all obligations in each scenario. Regulators require life insurers to test at least 7 specified interest rate scenarios (including large rate increases, large decreases, and curves that invert). If cash flows prove insufficient in any scenario, the insurer must hold additional reserves. Cash-flow testing is the backbone of ALM analysis â€” it transforms abstract duration gaps into concrete projections showing whether bills can be paid in 10, 20, or 30 years under different economic futures.",
        "Nationwide Life conducts quarterly cash-flow testing using 200 stochastic interest rate scenarios generated by a calibrated economic model. Each scenario projects 30 years of investment income, policyholder claims, lapses, expense payments, and reinvestment rates. In the stress scenario of rates rising 4% immediately and staying elevated, Nationwide's models show that its fixed annuity portfolio generates $2.1 billion more in income over 30 years than the guaranteed annuity payments â€” confirming solvency. In the severe rate-drop scenario (rates fall 3% and stay low), Nationwide's models show a $340 million shortfall in year 22 â€” prompting the ALM team to buy additional long-term bonds to reduce this scenario risk.",
        [
            "Cash-flow testing projects asset and liability cash flows under multiple interest rate scenarios over a long horizon (20-30 years).",
            "Regulators require minimum 7 specific scenarios; companies often test 100-500+ stochastic scenarios.",
            "Key outputs: adequacy of reserves, identification of scenario-specific vulnerabilities, surplus/deficiency projections.",
            "Cash-flow testing is required for participating life policies and annuities in most states.",
        ],
        [
            "Thinking cash-flow testing is a one-time exercise â€” it must be repeated quarterly or annually as portfolios and economic conditions change.",
            "Confusing cash-flow testing (regulatory tool) with stress testing (management tool) â€” they often overlap but have different scopes.",
            "Assuming a passing result today guarantees passing in all future periods â€” the portfolio and liability profile change continuously.",
        ],
        lessons=[
            _intro("Can the Insurer Pay Every Claim in Every Interest Rate Environment?",
                   "A guarantee made to a policyholder in 2024 must be honored in 2054. Cash-flow testing is how actuaries and investment managers verify that the money will be there â€” in multiple possible futures, not just the most optimistic one."),
            _teach("Cash-Flow Testing: The Process and Required Scenarios",
                   "Cash-flow testing projects all expected inflows (investment income, principal repayments, new premiums) and outflows (claims, policyholder surrenders, expenses, tax) over a 20-30 year horizon. It is repeated for multiple interest rate scenarios to reveal vulnerabilities. The NAIC (National Association of Insurance Commissioners) requires testing at minimum 7 specific scenarios: (1) level rates, (2) gradually increasing rates, (3) gradually decreasing rates, (4) increasing then decreasing, (5) decreasing then increasing, (6) immediate large increase, (7) immediate large decrease. If cash flows are insufficient in any scenario, additional actuarial reserves must be held.",
                   ["7 NAIC-specified scenarios must be tested; companies often test hundreds more stochastic scenarios.",
                    "Each scenario projects 20-30 years of future cash flows.",
                    "Shortfall in any scenario = must hold additional reserves to close the gap.",
                    "Stochastic testing = running 200-1,000 randomly generated rate paths to estimate probability distribution of outcomes."]),
            _teach("ALM Internal Reports and Analysis Outputs",
                   "Cash-flow testing generates internal reports that the ALM Unit uses to manage the portfolio. Key reports include: (1) Duration Gap Report â€” shows asset duration vs. liability duration for each segment; (2) Scenario Adequacy Report â€” shows surplus/deficiency in each tested scenario; (3) Convexity Report â€” measures how duration itself changes as rates move (options embedded in liabilities, like surrender features, can cause non-linear behavior); (4) Sensitivity Analysis â€” shows P&L impact of rate changes in increments (+/-0.25%, +/-0.50%, +/-1%, etc.); (5) Reinvestment Risk Report â€” projects the yield at which portfolio cash flows must be reinvested and the impact on income.",
                   ["Duration gap report: centerpiece of ALM monitoring.",
                    "Scenario adequacy: required by regulators â€” must pass all 7 NAIC scenarios.",
                    "Convexity: measures non-linearity of price-yield relationship (especially important for MBS and callable bonds).",
                    "Reinvestment risk: cash received from maturing bonds must be reinvested at prevailing rates."]),
            _example("Nationwide's Scenario 7 Vulnerability",
                     "In Nationwide's 2023 cash-flow testing exercise, Scenario 5 (rates decrease then increase) revealed that Nationwide's fixed annuity segment would face a $340 million shortfall in year 22. Why year 22? Because many of Nationwide's fixed annuities had a guaranteed minimum surrender value; in a low-rate environment (rates down 3%), policyholders who had held policies for 20+ years would receive attractive surrender values, draining cash from the segment just as its older bonds matured. Nationwide's ALM team responded by: (1) buying $2 billion in 25-year corporate bonds to extend duration; (2) entering interest rate swaps to convert $5 billion of floating exposure to fixed; (3) buying floor options to hedge the low-rate scenario specifically. At the next quarterly test, the year-22 shortfall was eliminated.",
                     "Cash-flow testing is not just a regulatory checkbox â€” it identifies specific vulnerabilities that guide targeted investment strategy changes."),
            _flash("What are the 7 NAIC interest rate scenarios required in cash-flow testing?",
                   "NAIC requires: (1) Level rates, (2) Gradually increasing, (3) Gradually decreasing, (4) Increasing then decreasing, (5) Decreasing then increasing, (6) Immediate large increase, (7) Immediate large decrease. If cash flows are insufficient in any scenario, additional reserves must be held."),
            _mcq("What is the primary purpose of cash-flow testing for a life insurance company?",
                 ["To determine the market value of all investment portfolio assets",
                  "To project asset and liability cash flows under multiple interest rate scenarios to verify the insurer can meet all obligations",
                  "To calculate the quarterly earnings attributable to the investment portfolio",
                  "To identify which individual bonds should be sold from the portfolio"],
                 1,
                 "Cash-flow testing verifies that the insurer can honor all policyholder obligations across a range of interest rate environments â€” not just in the base case. It is a multi-scenario adequacy test, not a valuation or portfolio selection tool."),
            _mcq("How many specific interest rate scenarios does the NAIC require for cash-flow testing at minimum?",
                 ["3", "7", "12", "100"],
                 1,
                 "The NAIC requires a minimum of 7 specific interest rate scenarios in cash-flow testing. These include level rates, gradual increases and decreases, rates that increase then decrease, rates that decrease then increase, and immediate large rate shocks in both directions."),
            _mcq("A cash-flow testing analysis shows a $200 million shortfall in NAIC Scenario 7 (immediate large rate decrease). What is the REQUIRED regulatory action?",
                 ["The insurer must immediately sell bonds to raise cash",
                  "No action is required if the insurer passes the other 6 scenarios",
                  "The insurer must hold additional actuarial reserves to cover the projected shortfall",
                  "The insurer must reduce all policyholder guaranteed rates to zero"],
                 2,
                 "If cash-flow testing reveals a shortfall in ANY of the required scenarios, the insurer must hold additional actuarial reserves equal to or greater than the projected shortfall. Failing a single scenario requires a reserve strengthening, even if all other scenarios pass."),
            _mcq("What does 'convexity' measure in ALM analysis?",
                 ["The difference between asset duration and liability duration",
                  "The total dollar value of the investment portfolio",
                  "How the duration (price sensitivity) of a bond or portfolio changes as interest rates change",
                  "The credit quality distribution of the bond portfolio"],
                 2,
                 "Convexity measures the non-linearity of the price-yield relationship â€” how duration itself changes as rates move. For standard bonds, positive convexity means the bond price rises faster when rates fall than it falls when rates rise (a beneficial asymmetry). Callable bonds and MBS have negative convexity, making them behave unfavorably in rate-volatile environments."),
            _mcq("Which ALM internal report would BEST alert management that a specific rate scenario poses unique risk to the annuity portfolio?",
                 ["Duration gap report", "Scenario adequacy report", "Convexity report", "Reinvestment risk report"],
                 1,
                 "The scenario adequacy report shows the surplus or deficiency in each tested interest rate scenario. If the annuity portfolio would be deficient in a specific scenario (e.g., rates fall 3% and stay low), this report explicitly shows the magnitude and timing of the shortfall, triggering corrective action."),
            _scenario(
                "Transamerica's actuaries complete the annual cash-flow test. Results: Scenario 1 (level rates): +$450M surplus. Scenario 4 (rates increase then decrease): +$180M surplus. Scenario 6 (immediate large rate increase +4%): +$320M surplus. Scenario 7 (immediate large rate decrease -3%): -$210M deficit. All other scenarios show surpluses.",
                "What must Transamerica's management do as a result of these cash-flow test results?",
                [("Nothing â€” passing 6 of 7 scenarios demonstrates adequate solvency", False,
                  "Failing even one NAIC scenario requires regulatory action. A $210M deficit in Scenario 7 mandates reserve strengthening regardless of results in other scenarios."),
                 ("Hold additional actuarial reserves to cover the $210M deficit in Scenario 7", True,
                  "Correct. Regulatory rules require Transamerica to establish additional reserves equal to or greater than the $210M shortfall identified in Scenario 7. The deficit cannot be offset by surpluses in other scenarios â€” each scenario must independently show adequacy."),
                 ("Immediately close the annuity product line to prevent future losses", False,
                  "Closing a product line is an extreme action not required by a single scenario shortfall. The regulatory response is reserve strengthening, and the investment response is adjusting the portfolio to eliminate the scenario vulnerability.")]
            ),
        ]
    )

    # Concept 4: ALM Investment Strategies
    c4 = _concept(
        m2_id, 2,
        "ALM Investment Strategies: Immunization, Dedication, and Interest-Rate Anticipation",
        "Describe and distinguish the three primary ALM investment strategies â€” portfolio immunization, portfolio dedication, and interest-rate anticipation â€” and explain when each is most appropriate.",
        "Insurance companies have three main strategies for managing the relationship between their assets and liabilities: (1) Immunization â€” structuring the portfolio so that asset value changes offset liability value changes when interest rates move; (2) Dedication â€” exactly matching asset cash flows to liability cash flows, eliminating ALM risk entirely; (3) Interest-Rate Anticipation â€” deliberately positioning the portfolio to benefit from expected rate changes (accepting more ALM risk for potential higher return). Each strategy sits at a different point on the risk-return spectrum: dedication is the most conservative, immunization is moderate, and interest-rate anticipation is the most aggressive.",
        "TIAA's ALM team manages $200 billion in fixed annuity assets with explicit strategy allocations: 60% immunization (duration-matched portfolios by segment), 30% dedication (cash-flow-matched bonds for their oldest annuity cohorts where liabilities are known precisely), and 10% interest-rate anticipation (tactical duration bets within board-approved bands of +/-2 years from neutral). In 2022, TIAA's anticipation portfolio was positioned short-duration (+1.5 years vs. neutral), correctly anticipating Fed rate hikes. This tactical position generated 1.8% excess return vs. the neutral benchmark in the anticipation sleeve, adding $360 million in value on the $20 billion allocated to that strategy.",
        [
            "Immunization: match asset duration to liability duration so rate changes have equal and offsetting impacts on both sides.",
            "Dedication (cash-flow matching): buy bonds whose principal and coupon payments exactly fund each scheduled liability payment.",
            "Interest-rate anticipation: deliberately mismatch duration to profit from expected rate movements â€” highest risk/return.",
            "Most insurers use a combination: core dedicated/immunized plus a tactical anticipation overlay.",
        ],
        [
            "Thinking immunization guarantees zero loss â€” it immunizes against parallel yield curve shifts but not against non-parallel shifts (e.g., yield curve flattening).",
            "Confusing dedication (cash-flow matching) with immunization (duration matching) â€” they use different mechanisms to reduce ALM risk.",
            "Assuming interest-rate anticipation is speculation â€” it is active management within regulatory and board-approved risk parameters.",
        ],
        lessons=[
            _intro("Three Ways to Manage the Asset-Liability Relationship",
                   "Every insurer must decide how tightly to link its assets to its liabilities. Dedication locks them together perfectly. Immunization creates a controlled relationship. Interest-rate anticipation deliberately creates gaps to profit from rate predictions. Understanding all three is essential for the LOMA 357 exam."),
            _teach("Portfolio Immunization: Matching Duration to Neutralize Rate Risk",
                   "Portfolio immunization sets asset duration equal to liability duration so that when interest rates change, the change in asset value exactly offsets the change in liability value. If an insurer's liabilities have duration 10, it holds assets with duration 10. When rates rise 1%: liabilities fall ~10% (in present value), assets also fall ~10% â€” the solvency ratio stays constant. Immunization is not perfect: it only works for parallel yield curve shifts and requires rebalancing as time passes and as the portfolio changes.",
                   ["Immunization: set asset duration = liability duration.",
                    "Parallel shift immunity: when all rates move by the same amount, the strategy works perfectly.",
                    "Requires rebalancing: as time passes, asset and liability durations change at different rates.",
                    "Convexity advantage: holding bonds with positive convexity slightly outperforms immunization in volatile markets."]),
            _teach("Portfolio Dedication and Interest-Rate Anticipation",
                   "Portfolio Dedication (cash-flow matching) is a more conservative approach: the investment team buys specific bonds whose principal and coupon payments exactly fund each scheduled liability payment on its due date, eliminating reinvestment risk. Example: if $5 million of annuity payments are due in year 10, buy a bond maturing in year 10 with face value $5 million. Dedication eliminates all ALM risk but is expensive (requires buying the exact right bond) and inflexible. Interest-Rate Anticipation is the opposite: the manager deliberately shortens or lengthens portfolio duration to profit from expected rate movements. Short duration in a rising-rate environment generates positive active return; long duration in a falling-rate environment does the same.",
                   ["Dedication = buy bonds to exactly match liability cash flows by date and amount (eliminates ALM risk).",
                    "Dedication is expensive and inflexible but eliminates reinvestment risk for covered liabilities.",
                    "Interest-rate anticipation = deliberate duration mismatch based on rate forecasts.",
                    "Anticipation strategy requires accurate rate forecasts â€” wrong forecasts generate underperformance."]),
            _example("TIAA's Three-Strategy ALM Approach",
                     "TIAA manages $200 billion in retirement annuity assets. For its oldest cohort of retirees (80+ years old, highly predictable mortality tables), TIAA uses dedication: $30 billion of bonds are matched to specific monthly annuity payments for the next 15 years â€” no ALM risk for these liabilities. For its main annuity block (ages 60-79), TIAA uses immunization: $120 billion in bonds with duration matching the liability duration of 12.5 years, rebalanced quarterly. For its tactical anticipation overlay, TIAA allocates $20 billion and allows the manager to deviate +/- 2 years from the 12.5-year neutral duration based on rate forecasts. In 2022, the tactical manager went short (10.5 years vs. 12.5 neutral), earning 1.8% excess return when the Fed raised rates aggressively.",
                     "Most sophisticated insurers use all three strategies simultaneously: dedication for the most certain liabilities, immunization for the core block, and anticipation for an active return overlay."),
            _flash("What is the key difference between portfolio immunization and portfolio dedication?",
                   "Immunization matches asset DURATION to liability duration â€” interest rate changes have equal impact on both sides. Dedication matches asset CASH FLOWS to liability payments â€” each liability payment is funded by a specific bond payment on the exact same date, eliminating reinvestment risk."),
            _mcq("An insurer's liabilities have duration 12 years. Under a pure immunization strategy, what should be the target duration of the asset portfolio?",
                 ["6 years", "10 years", "12 years", "15 years"],
                 2,
                 "Immunization sets asset duration equal to liability duration. With a 12-year liability duration, the target asset duration is 12 years. This ensures that any change in interest rates produces equal and offsetting changes in asset and liability present values, maintaining the solvency ratio."),
            _mcq("Which ALM strategy eliminates reinvestment risk for a given liability payment?",
                 ["Portfolio immunization", "Interest-rate anticipation", "Portfolio dedication (cash-flow matching)", "Duration tilting"],
                 2,
                 "Portfolio dedication buys bonds whose specific cash flows (coupon + principal) occur on the exact dates liability payments are due. Since the liability is funded by cash flows arriving before it (not from reinvestment of earlier cash flows), reinvestment risk for that liability payment is eliminated."),
            _mcq("An insurer believes interest rates will rise significantly over the next year. Under an interest-rate anticipation strategy, what portfolio adjustment is MOST appropriate?",
                 ["Extend asset duration to benefit from higher yields",
                  "Shorten asset duration to reduce price sensitivity to the anticipated rate rise",
                  "Move entirely to cash to eliminate all rate risk",
                  "Increase equity allocation to reduce fixed-income exposure"],
                 1,
                 "When rates are expected to rise, bond prices will fall. Shorter-duration bonds fall less in price than longer-duration bonds. By shortening asset duration (reducing price sensitivity), the portfolio loses less value when rates rise â€” generating positive active return vs. the neutral benchmark."),
            _mcq("Why must an immunized portfolio be periodically rebalanced?",
                 ["Immunization is only effective for exactly one year before requiring complete reconstruction",
                  "As time passes and the portfolio changes, asset and liability durations drift at different rates, eroding the duration match",
                  "Regulations require quarterly rebalancing regardless of portfolio drift",
                  "Immunization rebalancing is needed only when interest rates change more than 2%"],
                 1,
                 "Over time, assets and liabilities age at different rates: a 10-year bond becomes a 9-year bond after one year (duration decreases), but liability duration decreases at a different pace. As the portfolio is managed (bonds mature, are called, or sold), duration naturally drifts from the immunization target, requiring periodic rebalancing to maintain the match."),
            _mcq("Which of the following BEST describes the risk of an interest-rate anticipation strategy?",
                 ["It eliminates all ALM risk by matching durations precisely",
                  "It requires holding only government bonds",
                  "If interest rate forecasts are wrong, the strategy generates underperformance vs. the immunized benchmark",
                  "It is the most conservative ALM strategy available to life insurers"],
                 2,
                 "Interest-rate anticipation succeeds only when rate forecasts are correct. If the manager shortens duration expecting rates to rise, but rates instead fall, the short-duration portfolio underperforms the neutral benchmark â€” generating negative active return. The strategy requires accurate macro forecasting, which is inherently difficult."),
            _scenario(
                "Lincoln Financial's ALM committee must choose a strategy for $5 billion in immediate annuity liabilities â€” payments guaranteed to specific retirees beginning immediately with known amounts for the next 20 years. The CIO presents three options: (A) Immunization targeting 15-year duration; (B) Dedication with bonds matched to each monthly payment for 20 years; (C) Interest-rate anticipation, currently positioned 2 years short of the 15-year neutral.",
                "Which strategy is MOST appropriate for these specific liabilities?",
                [("Option A: Immunization â€” matches liability duration and is easier to manage than dedication", False,
                  "While immunization is reasonable, it still carries reinvestment risk when portfolio bonds mature and must be reinvested at prevailing rates. For known, fixed annuity payments, dedication is superior."),
                 ("Option B: Dedication â€” exactly matches known payment cash flows, eliminating reinvestment risk", True,
                  "Correct. Immediate annuities with known payment amounts and exact dates are the ideal application for portfolio dedication. Buying bonds that exactly fund each payment eliminates both ALM risk and reinvestment risk for these highly certain liabilities."),
                 ("Option C: Interest-rate anticipation â€” the 2-year short position will generate excess returns if rates rise", False,
                  "Interest-rate anticipation creates deliberate mismatch and risk for known, certain liability payments. There is no reason to take on active rate risk for liabilities that can be perfectly matched through dedication. Anticipation strategies are better suited to less certain liabilities.")]
            ),
        ]
    )

    m2["concepts"] = [c3, c4]
    ch["modules"] = [m1, m2]
    return ch



def _build_ch7(course_id):
    ch_id = _id()
    ch = {
        "id": ch_id, "course_id": course_id, "order": 7,
        "title": "Portfolio Construction and Asset Selection",
        "description": "How institutional investment portfolios are built from scratch — setting objectives and constraints, selecting asset classes, determining strategic asset allocation, choosing benchmarks, evaluating individual securities (bonds and stocks), and selecting investment funds.",
    }

    # ── Module 1: Portfolio Construction Process ──────────────────────────────
    m1_id = _id()
    m1 = {"id": m1_id, "chapter_id": ch_id, "order": 1,
          "title": "Portfolio Construction Process"}

    # Concept 1: Planning — Objectives, Constraints, Asset Classes
    c1 = _concept(
        m1_id, 1,
        "Planning a Portfolio: Objectives, Constraints, and Asset Class Selection",
        "Describe the sequential steps in planning an institutional investment portfolio — from defining objectives and constraints, to identifying appropriate asset classes for a given insurer's liability profile.",
        "Building an institutional investment portfolio is not random. It follows a disciplined top-down process: first define what you need to achieve (objectives), then define what you cannot do (constraints), then select which broad categories of investments (asset classes) are appropriate. Only after completing these steps do you begin selecting individual securities. Skipping any step leads to portfolios that either take too much risk, earn too little return, or violate regulatory requirements. The top-down process ensures every security purchased has a clear reason for being there.",
        "State Farm, the largest US P&C insurer, follows a formal 5-step portfolio construction process. Step 1: Set objectives — 5.2% total return to cover claims + 2.8% profit margin. Step 2: Define constraints — regulatory limits, single-issuer caps, liquidity requirements. Step 3: Identify asset classes — investment-grade bonds (core), municipal bonds (tax efficiency), equities (30-year horizon buffer), short-term instruments (liquidity). Step 4: Set allocations. Step 5: Select securities. State Farm's $300 billion portfolio is entirely governed by this framework — no security is purchased without clear justification at the asset class and objectives level.",
        [
            "Top-down construction: objectives → constraints → asset classes → allocation → security selection.",
            "Objectives include: return target, risk tolerance, time horizon, income vs. growth emphasis.",
            "Constraints include: regulatory capital limits, single-issuer maximums, liquidity minimums, and IPS restrictions.",
            "Asset class selection must reflect the institution's liability profile — P&C insurers need different asset classes than life insurers.",
        ],
        [
            "Starting with security selection before defining objectives — leads to a random collection of investments, not a coherent portfolio.",
            "Treating objectives and constraints as the same thing — objectives are goals to achieve; constraints are rules that limit how goals are pursued.",
            "Assuming one asset class mix fits all insurers — P&C, life, and health insurers have fundamentally different liability structures requiring different asset classes.",
        ],
        lessons=[
            _intro("Building a Portfolio: Why Top-Down Beats Bottom-Up",
                   "A brilliant security selection is worthless if it doesn't fit the portfolio's purpose. Great institutional portfolio construction starts at the top — with what the portfolio must achieve — and works down to individual securities. Let's walk through how it's done."),
            _teach("Step 1 and 2: Setting Objectives and Constraints",
                   "Investment objectives define what the portfolio must accomplish: (1) Return objective — the minimum return needed to fund liabilities plus a profit margin; (2) Risk tolerance — how much volatility and potential loss is acceptable; (3) Time horizon — how long the assets will be held (short for P&C, long for life/annuities); (4) Income vs. growth emphasis — does the insurer need steady cash income (life/annuities) or total return (endowments). Constraints then define the boundaries: regulatory capital limits, single-issuer concentration caps, minimum liquidity reserve, IPS-mandated restrictions, and credit quality floors.",
                   ["Return objective must exceed the cost of funds (credited rate + expenses) to be viable.",
                    "Risk tolerance for insurers is limited by regulatory solvency requirements.",
                    "Time horizon drives duration: short horizon = short-duration assets; long horizon = long-duration tolerated.",
                    "Income emphasis: life/annuity insurers prioritize coupon income; endowments may prioritize total return."]),
            _teach("Step 3: Identifying Appropriate Asset Classes",
                   "Asset class selection must match the institution's liability structure. Life insurers with 30-year liabilities can access long-duration corporate bonds and commercial real estate. P&C insurers with 6-18 month liability horizons primarily use short-to-medium bonds and municipals (for tax efficiency). Health insurers with 30-day claim cycles need highly liquid money market instruments. Once appropriate asset classes are identified, each gets a preliminary allocation range based on expected return, risk, liquidity, and regulatory treatment. Diversification across uncorrelated asset classes reduces portfolio volatility without sacrificing expected return.",
                   ["Life insurer asset classes: long corporates, commercial mortgage loans, real estate, private placements.",
                    "P&C insurer asset classes: short/medium bonds, munis (tax-exempt), equities, short-term instruments.",
                    "Health insurer asset classes: primarily liquid short-term bonds and money market for rapid claims.",
                    "Alternative asset classes (private equity, hedge funds) require long commitment periods — only suitable for long-horizon institutions."]),
            _example("State Farm's Asset Class Selection Framework",
                     "State Farm writes primarily auto and homeowners insurance — P&C liabilities with 6-18 month average duration. Its asset class selection reflects this: 55% investment-grade bonds (3-7 year average maturity), 25% municipal bonds (state/local tax exemption benefits State Farm's corporate tax rate), 12% equities (very long-term buffer capital, not linked to near-term claims), 5% short-term instruments (immediate liquidity for claims), 3% other. State Farm explicitly excludes: long-duration corporate bonds (>10 year) — too much duration mismatch with P&C liabilities; private equity — 10-year lockup incompatible with claims obligations; below-investment-grade bonds — regulatory capital cost too high for P&C RBC framework.",
                     "Asset class selection is a deliberate, liability-driven process of inclusion AND exclusion — knowing what NOT to own is as important as knowing what to own."),
            _flash("What is the correct sequence for top-down institutional portfolio construction?",
                   "Objectives → Constraints → Asset Class Identification → Strategic Asset Allocation → Benchmark Selection → Security Selection. Starting at the top ensures every decision below it has clear purpose and justification."),
            _mcq("In the top-down portfolio construction process, which step comes IMMEDIATELY BEFORE selecting individual securities?",
                 ["Defining investment constraints",
                  "Setting the return objective",
                  "Determining the strategic asset allocation for each asset class",
                  "Identifying the institution's time horizon"],
                 2,
                 "The top-down sequence ends with security selection. Before individual securities are chosen, the team must have completed: objectives, constraints, asset class identification, and strategic asset allocation. Only with an approved allocation (e.g., '35% investment-grade corporate bonds') does the team select specific bonds to fill that allocation."),
            _mcq("A P&C insurer with 12-month average liability duration should MOST LIKELY avoid which asset class?",
                 ["3-year investment-grade corporate bonds",
                  "Municipal bonds with 5-year maturities",
                  "30-year corporate bonds with fixed coupons",
                  "90-day Treasury bills"],
                 2,
                 "30-year bonds create a massive duration mismatch with 12-month P&C liabilities. If the insurer needs to sell these bonds to pay claims before maturity, it faces significant interest rate risk. Long-duration assets are inappropriate for short-duration P&C insurance liabilities."),
            _mcq("Which factor MOST directly drives the identification of appropriate asset classes for an insurer's portfolio?",
                 ["The current interest rate environment",
                  "The portfolio manager's personal investment preferences",
                  "The insurer's liability profile — duration, cash flow pattern, and predictability",
                  "The investment performance of competitor insurers"],
                 2,
                 "Asset class selection must be driven by the liability profile. The duration, predictability, and cash flow pattern of liabilities determines which asset classes can appropriately match them. External factors like interest rates influence tactical decisions within the approved asset classes, not the fundamental asset class selection."),
            _mcq("Which of the following is a CONSTRAINT rather than an investment objective?",
                 ["Earn a minimum total return of 5.5% annually",
                  "Maintain an investment spread above 1.5% over credited rates",
                  "No single issuer may represent more than 3% of the total portfolio",
                  "Generate sufficient income to fund policyholder benefits"],
                 2,
                 "The single-issuer limit of 3% is a constraint — a rule that restricts HOW the objective can be pursued. Return targets, spread requirements, and income generation are objectives — what the portfolio must achieve. Constraints define the boundaries within which objectives are pursued."),
            _mcq("A life insurer has 35-year annuity liabilities. Which asset class combination BEST supports appropriate portfolio construction?",
                 ["50% 90-day T-bills, 30% money market, 20% equities",
                  "70% long-duration investment-grade bonds, 20% commercial mortgage loans, 10% equities",
                  "100% S&P 500 index fund",
                  "60% below-investment-grade bonds, 40% hedge funds"],
                 1,
                 "Long-duration annuity liabilities require: long-duration bonds (match interest rate sensitivity), commercial mortgage loans (stable long-term income), modest equities (long-term return enhancement). T-bills and money markets are too short. 100% equities is too volatile and income-insufficient. Below-IG bonds carry excessive regulatory capital charges."),
            _scenario(
                "Sunlife Financial is building an investment portfolio for a new block of 20-year fixed annuity products. The CIO presents two competing frameworks: Framework A — start by screening Bloomberg for bonds yielding above 6%, then check if they fit the product. Framework B — first define the 6.5% return objective, identify constraints (BBB+ minimum credit quality, 15-year max duration, no single issuer >4%), then identify asset classes (long-duration investment-grade bonds, commercial real estate), set allocations, then select securities.",
                "Which framework correctly applies the top-down portfolio construction process?",
                [("Framework A — starting with high-yield bonds is efficient and market-responsive", False,
                  "Framework A is bottom-up security selection without any governance framework. Securities found by yield screening may violate constraints, mismatch liability duration, or fail regulatory requirements — a recipe for portfolio mismanagement."),
                 ("Framework B — defines objectives and constraints first, then selects asset classes before individual securities", True,
                  "Correct. Framework B follows the top-down process: objective (6.5% return) → constraints (BBB+, duration, concentration) → asset classes (long corporates, commercial real estate) → allocations → security selection. Every security purchased has clear justification within the framework."),
                 ("Both frameworks achieve the same result — the order of steps doesn't matter in professional investing", False,
                  "The order matters enormously. Top-down ensures constraints and objectives are respected at every level. Bottom-up security screening often creates portfolios that are tactically attractive but strategically misaligned with the institution's liability needs.")]
            ),
        ]
    )

    # Concept 2: Strategic Asset Allocation and Benchmark Selection
    c2 = _concept(
        m1_id, 2,
        "Strategic Asset Allocation and Selecting Portfolio Benchmarks",
        "Explain how strategic asset allocation weights are determined for each asset class, and describe the criteria and process for selecting appropriate performance benchmarks for each portfolio segment.",
        "Once asset classes are identified, the portfolio team must determine how much to allocate to each (strategic asset allocation) and what to measure performance against (benchmark selection). Strategic asset allocation is determined through optimization — balancing expected return, risk, correlation, and liability constraints to find the mix that maximizes return per unit of risk for the institution's specific situation. Benchmark selection is equally important: an inappropriate benchmark can make a skilled manager look incompetent and a lucky manager look brilliant.",
        "TIAA-CREF conducted a full strategic asset allocation study in 2022, using a 10-year capital market assumptions framework. For its $140 billion general account: long-duration bonds expected return 5.2% (std dev 8%), private credit 7.4% (std dev 10%), commercial real estate 7.1% (std dev 12%), equities 9.8% (std dev 18%). After running a mean-variance optimization subject to liability constraints (minimum 50% bonds for RBC, maximum 20% equities for regulatory capital), the optimal allocation was: 55% long-duration bonds, 20% private credit, 15% commercial real estate, 10% equities. Each segment benchmarks to: bonds vs. Bloomberg Long Credit Index, private credit vs. CS Leveraged Loan Index plus 100bps, real estate vs. NCREIF Property Index.",
        [
            "SAA weights are determined through mean-variance optimization subject to liability and regulatory constraints.",
            "Capital market assumptions (expected returns, standard deviations, correlations) drive the optimization inputs.",
            "Benchmark must be investable, measurable, specified in advance, and reflect the same risk as the managed portfolio.",
            "Each asset class segment should have its own benchmark — using one index for all segments is inappropriate.",
        ],
        [
            "Thinking SAA is permanent — it should be reviewed every 3-5 years as liability profiles and capital market conditions change.",
            "Using an inappropriate benchmark — if the bond portfolio holds corporate bonds, benchmarking to a government bond index creates a misleading comparison.",
            "Confusing the SAA benchmark (policy benchmark) with tactical tilts — the policy benchmark is the neutral position, not the target return.",
        ],
        lessons=[
            _intro("How Much in Each Asset Class? The Allocation Decision",
                   "Knowing which asset classes to use is only half the job. Determining exactly HOW MUCH to put in each — and measuring whether managers are adding value — requires rigorous analysis and benchmark discipline."),
            _teach("Strategic Asset Allocation: Optimization and Capital Market Assumptions",
                   "Strategic asset allocation (SAA) weights are typically determined using mean-variance optimization, pioneered by Harry Markowitz. The process: (1) Develop capital market assumptions — expected return, standard deviation, and correlations for each asset class over a 5-10 year horizon; (2) Define the liability constraint — minimum allocation to bonds to maintain RBC, duration constraints, income constraints; (3) Run the optimization — find the allocation that maximizes expected return for the institution's risk tolerance subject to all constraints; (4) Apply judgment — overlay qualitative factors (liquidity, operational complexity, manager availability) to finalize the allocation. The result is an SAA with target weights and policy ranges for each asset class.",
                   ["Capital market assumptions are long-term forecasts (5-10 year horizon), not short-term predictions.",
                    "Optimization finds the efficient frontier — the set of portfolios with maximum return for each risk level.",
                    "Liability constraints are non-negotiable inputs to the optimization, not outputs.",
                    "SAA rebalancing maintains target weights when market movements cause drift."]),
            _teach("Selecting Portfolio Benchmarks: The Four Criteria",
                   "A good benchmark has four essential properties: (1) Investable — the investor can actually buy the index components; (2) Measurable — returns can be calculated objectively and frequently; (3) Specified in advance — the benchmark is chosen before the measurement period, not selected retroactively to make performance look good; (4) Appropriate — the benchmark reflects the same investment universe, duration, credit quality, and risk characteristics as the managed portfolio. Common insurance investment benchmarks: Bloomberg US Aggregate (investment-grade bond mix), Bloomberg Long Credit (long-duration corporate bonds), MSCI ACWI (global equities), NCREIF (commercial real estate), Cambridge Associates (private equity).",
                   ["Investable: manager can replicate the index by buying its components.",
                    "Measurable: objective calculation of benchmark return on a regular basis.",
                    "Specified in advance: prevents benchmark manipulation (choosing the index AFTER seeing returns).",
                    "Appropriate: same characteristics as the managed portfolio — wrong benchmark creates false performance signals."]),
            _example("TIAA's Optimization-Driven SAA",
                     "TIAA's 2022 asset allocation study ran 10,000 Monte Carlo simulations using its capital market assumptions. The unconstrained optimal portfolio was 45% equities, 25% private credit, 20% real estate, 10% bonds — too risky for a regulated insurer. After applying constraints (minimum 50% bonds for RBC, maximum 20% equities), the constrained optimal shifted to 55% long bonds, 20% private credit, 15% real estate, 10% equities. The difference in expected return: unconstrained = 8.2%, constrained = 6.9%. The 1.3% return reduction was the 'cost of constraints' — the price of maintaining solvency and regulatory compliance. TIAA's board accepted this cost as appropriate.",
                     "Regulatory and liability constraints always narrow the feasible allocation set — the 'cost of constraints' is the explicit price of sound governance."),
            _flash("What four properties must a good investment benchmark have?",
                   "Investable (can be replicated by buying components), Measurable (objective return calculation), Specified in Advance (chosen before the measurement period), and Appropriate (same risk characteristics as the managed portfolio). A benchmark failing any criterion provides misleading performance signals."),
            _mcq("Which of the following BEST describes mean-variance optimization in the context of strategic asset allocation?",
                 ["A process that selects individual securities based on their price-to-earnings ratios",
                  "A mathematical process that finds the asset class mix maximizing expected return for a given level of risk",
                  "A technique for timing the market to buy asset classes at their lowest prices",
                  "A method for calculating the credit risk of individual bond issuers"],
                 1,
                 "Mean-variance optimization (Markowitz, 1952) finds the portfolio that maximizes expected return for each level of portfolio risk (standard deviation). Applied to asset allocation, it determines the optimal mix of asset classes given their expected returns, standard deviations, and correlations — subject to institutional constraints."),
            _mcq("An insurer's fixed income portfolio holds only long-duration corporate bonds. Which benchmark is MOST appropriate?",
                 ["Bloomberg US Short-Term Government Index",
                  "S&P 500 Total Return Index",
                  "Bloomberg US Long Credit Index",
                  "MSCI World Equity Index"],
                 2,
                 "The Bloomberg US Long Credit Index tracks long-duration investment-grade corporate bonds — the same universe, duration, and credit quality as the managed portfolio. Using a short-government index would be inappropriate (wrong duration and credit quality), creating misleading performance signals."),
            _mcq("An investment committee selects a benchmark AFTER seeing the manager's annual returns, choosing the index that makes the manager look best. Which benchmark property is violated?",
                 ["Investable", "Measurable", "Specified in advance", "Appropriate"],
                 2,
                 "Benchmarks must be specified in advance — chosen before the performance measurement period begins. Retroactively selecting a benchmark that maximizes apparent outperformance is a serious governance failure that destroys the accountability purpose of benchmarking."),
            _mcq("Which input is MOST critical to a strategic asset allocation optimization for an insurance company?",
                 ["The current stock market P/E ratio",
                  "Capital market assumptions — long-term expected returns, standard deviations, and correlations for each asset class",
                  "The personal investment preferences of the CIO",
                  "The most recent quarterly earnings of the largest portfolio holdings"],
                 1,
                 "Capital market assumptions are the primary inputs to mean-variance optimization. They define what the optimizer works with: expected returns determine which assets add value; standard deviations measure risk; correlations determine diversification benefits. Inaccurate capital market assumptions lead to suboptimal allocations regardless of how sophisticated the optimization model is."),
            _mcq("Why must strategic asset allocation be reviewed periodically rather than set permanently?",
                 ["Regulators require monthly updates to asset allocation for all insurers",
                  "Asset allocation must change daily to reflect market price movements",
                  "As liability profiles evolve, capital market conditions change, and business strategy shifts, the optimal allocation changes over time",
                  "Benchmarks change daily, requiring continuous SAA updates to match"],
                 2,
                 "SAA should be reviewed every 3-5 years (or after major business changes). As an insurer writes new products, its liability profile shifts. As markets evolve, capital market assumptions change. As regulations update, constraints shift. Each of these changes may alter the optimal allocation, making periodic review essential for maintaining alignment."),
            _scenario(
                "Pacific Life's investment committee receives two proposals for its $50 billion bond portfolio benchmark. Proposal A: Bloomberg US Aggregate Bond Index (broad mix of government, agency, and corporate bonds, average duration 6.5 years, BBB+ average quality). Proposal B: Bloomberg US Long Credit Index (long-duration corporate bonds only, average duration 13.5 years, BBB average quality). Pacific Life's bond portfolio holds: 80% long-duration corporate bonds (average duration 14 years), 15% government bonds, 5% cash.",
                "Which benchmark is MORE appropriate for Pacific Life's bond portfolio?",
                [("Proposal A — the broader Aggregate Index is always more appropriate for diversified portfolios", False,
                  "The Aggregate Index has 6.5-year duration vs. Pacific Life's 14-year portfolio — a massive duration mismatch. A manager would appear to 'outperform' simply by holding longer bonds in a falling-rate environment, not through skill."),
                 ("Proposal B — the Long Credit Index better matches the portfolio's duration, credit quality, and asset class composition", True,
                  "Correct. The Long Credit Index has duration 13.5 years (close to Pacific Life's 14 years), focuses on corporate bonds (matching the 80% corporate allocation), and has similar credit quality (BBB). This appropriate benchmark allows meaningful performance attribution."),
                 ("Neither benchmark is appropriate — custom benchmarks cannot be used by insurance companies", False,
                  "Custom benchmarks are standard practice in institutional investing. If neither Proposal A nor B were appropriate, a blended benchmark (80% Long Credit + 15% Government + 5% T-bills) would be constructed to match the portfolio composition exactly.")]
            ),
        ]
    )

    m1["concepts"] = [c1, c2]

    # ── Module 2: Security and Fund Selection ─────────────────────────────────
    m2_id = _id()
    m2 = {"id": m2_id, "chapter_id": ch_id, "order": 2,
          "title": "Security Selection and Fund Evaluation"}

    # Concept 3: Evaluating and Selecting Securities (Bonds and Stocks)
    c3 = _concept(
        m2_id, 1,
        "Security Evaluation: Selecting Corporate Bonds and Common Stocks",
        "Describe the key criteria used to evaluate and select individual corporate bonds and common stocks for an institutional investment portfolio.",
        "After determining asset class allocations and benchmarks, portfolio managers select individual securities to fill each allocation. Bond selection focuses on credit quality, yield spread, duration fit, and covenant protection. Stock selection analyzes valuation metrics (P/E, P/B, dividend yield), earnings growth, competitive positioning, and management quality. Institutional investors apply rigorous, documented analysis to every security purchase — not intuition or market rumors — because every holding must be defensible to regulators, boards, and rating agencies.",
        "Voya Financial's bond selection team evaluates every corporate bond through a standardized scorecard: (1) Credit fundamentals (40% weight): issuer financial ratios, debt/EBITDA, interest coverage, trend analysis; (2) Spread value (30%): current yield spread vs. historical average and peers; (3) Duration fit (15%): does the maturity/duration fit the segment's liability profile; (4) Covenants and structure (15%): legal protections (change of control, cross-default, negative pledge). A bond must score above 70 out of 100 on the scorecard to be eligible for purchase. This disciplined process ensures consistency and prevents 'yield chasing' that ignores credit risk.",
        [
            "Bond selection criteria: credit quality (issuer fundamentals), yield spread (relative value), duration fit (ALM match), and covenant protection.",
            "Stock selection criteria: valuation (P/E, P/B, dividend yield), earnings growth, competitive moat, management quality.",
            "Yield spread = bond yield minus comparable Treasury yield; wider spread = higher credit risk premium.",
            "Institutional selection requires documented analysis — not just screening — to defend every position to boards and regulators.",
        ],
        [
            "Focusing only on yield when selecting bonds — higher yield means higher risk; must analyze WHY the spread is wide.",
            "Ignoring covenants — legal protections in bond indentures can be the difference between recovering 80 cents vs. 20 cents if the issuer defaults.",
            "Confusing absolute P/E with relative P/E — a stock trading at P/E 25 may be cheap if peers trade at P/E 30, or expensive if peers trade at P/E 15.",
        ],
        lessons=[
            _intro("From Allocation to Specific Security: The Selection Decision",
                   "The allocation says '35% in investment-grade corporate bonds.' But which bonds? Every selection decision requires rigorous analysis — yield alone is never enough. Let's walk through what institutional investors actually look at."),
            _teach("Corporate Bond Selection: Four Key Criteria",
                   "When evaluating a specific corporate bond for purchase, institutional analysts examine four areas: (1) Credit Fundamentals — the issuer's financial health: debt-to-EBITDA ratio, interest coverage ratio, free cash flow, business stability, and industry position; (2) Yield Spread — the yield advantage over a comparable Treasury, expressed in basis points (100 bps = 1%). Does the spread adequately compensate for the credit risk? Is it wider or tighter than peers? (3) Duration/Maturity Fit — does the bond's maturity align with the segment's liability profile? A 30-year bond is inappropriate for a P&C insurer's short-duration segment; (4) Covenant Protection — legal protections in the bond indenture: negative pledge (prevents issuer from securing other debt over this bond), change-of-control put (allows bondholders to sell back if the company is acquired), cross-default provisions.",
                   ["Credit fundamentals: debt/EBITDA < 3x is generally investment-grade comfort zone.",
                    "Yield spread: wide spread signals risk; must verify whether risk is justified or mispriced.",
                    "Duration fit: bond duration must match the segment's liability duration target.",
                    "Covenants: strong covenants improve recovery rates in default scenarios."]),
            _teach("Common Stock Selection: Valuation and Qualitative Factors",
                   "For equity investments, institutional analysts use a combination of quantitative valuation and qualitative analysis. Quantitative: (1) P/E ratio — price divided by earnings per share; compare to sector peers and historical average; (2) Price-to-Book (P/B) ratio — price vs. book value; important for financial stocks; (3) Dividend yield — annual dividend as % of stock price; critical for income-oriented insurance portfolios; (4) Earnings growth rate — projected EPS growth over 3-5 years. Qualitative: (5) Competitive moat — does the company have durable pricing power? (6) Management quality — track record, capital allocation discipline; (7) Industry dynamics — growing or shrinking market. Insurance companies typically prefer dividend-paying stocks with visible earnings streams over high-growth-but-no-dividend technology stocks.",
                   ["P/E below sector average may indicate undervaluation — or a deteriorating business; must investigate.",
                    "Dividend yield: insurers prefer consistent, growing dividends (e.g., dividend aristocrats).",
                    "Competitive moat: brands, network effects, switching costs, regulatory licenses.",
                    "Management quality: management that allocates capital wisely creates long-term value."]),
            _example("Voya Financial's Boeing Bond Analysis",
                     "In 2019, Voya's credit team evaluated Boeing (BA) 5.15% bonds maturing 2030, yielding 5.85% (spread: +142 bps over 10-year Treasury). The scorecard: Credit fundamentals — BA debt/EBITDA was 3.8x (concerning for A-rated issuer); interest coverage 6.2x (adequate). Spread value — 142 bps vs. 90 bps average for A-rated aerospace peers (suggesting BA was oversold). Duration fit — 11-year maturity fit the life insurance segment's 12-year target duration. Covenants — standard investment-grade; change of control at 101% (adequate). Score: 74/100. Decision: BUY with a smaller-than-maximum position (0.8% vs. 1.5% standard) reflecting credit concern. Three months later, the 737 MAX crisis deepened and BA was downgraded. Voya's half-sized position limited the damage.",
                     "Rigorous multi-factor analysis doesn't always prevent losses — but it ensures positions are sized appropriately for the risk level, limiting damage when thesis goes wrong."),
            _flash("What is 'yield spread' in corporate bond analysis?",
                   "Yield spread is the difference between a corporate bond's yield and the yield of a comparable-maturity Treasury bond, expressed in basis points (bps). A spread of 150 bps means the corporate bond yields 1.5% more than the Treasury. The spread compensates for credit risk — wider spread = more credit risk (or more mispricing opportunity)."),
            _mcq("An analyst is evaluating a BBB-rated corporate bond yielding 5.8% when comparable BBB bonds average 5.2%. The 60 bps extra yield is MOST LIKELY explained by which of the following?",
                 ["The bond has exceptionally strong covenant protection",
                  "The bond has shorter duration than peer bonds, requiring less yield",
                  "The issuer has weaker credit fundamentals or the bond has structural subordination",
                  "The bond matures sooner than comparable bonds, reducing yield"],
                 2,
                 "A 60 bps yield premium above BBB peers indicates the market perceives higher-than-average risk for this specific bond. This may reflect weaker issuer financials (higher leverage, lower coverage), structural features (subordinated in the capital structure), sector headwinds, or simply mispricing. The analyst must determine which of these explains the spread before deciding to purchase."),
            _mcq("Which financial ratio is MOST commonly used to assess a corporate bond issuer's ability to service its debt?",
                 ["Price-to-earnings ratio", "Debt-to-EBITDA ratio", "Dividend payout ratio", "Asset-to-liability ratio"],
                 1,
                 "Debt-to-EBITDA measures total debt relative to operating earnings before interest, taxes, depreciation, and amortization. It shows how many years of earnings would be needed to pay off all debt. Investment-grade issuers typically have Debt/EBITDA below 3x. Above 5x signals potential difficulty servicing debt, regardless of credit rating."),
            _mcq("An insurance company's equity portfolio prioritizes which type of stock for income-oriented investing?",
                 ["High-growth technology stocks with zero dividends",
                  "Dividend-paying stocks with consistent, growing payouts",
                  "Recently IPO'd companies with no earnings history",
                  "Speculative micro-cap stocks with high short-term return potential"],
                 1,
                 "Insurance companies need investment income to pay claims. Dividend-paying stocks provide recurring cash income (similar to bond coupons). 'Dividend aristocrats' — companies with 25+ consecutive years of dividend increases — are particularly valued because they provide both income and inflation protection through growing payouts."),
            _mcq("A 'negative pledge' covenant in a bond indenture MOST DIRECTLY protects bondholders by:",
                 ["Preventing the issuer from paying dividends to shareholders",
                  "Guaranteeing a minimum recovery rate of 50% in the event of default",
                  "Preventing the issuer from pledging assets as collateral for other debt, protecting bondholders' claims",
                  "Requiring the issuer to maintain a minimum credit rating throughout the bond's life"],
                 2,
                 "A negative pledge clause prevents the issuer from securing future debt with collateral, which would subordinate existing bondholders. Without this protection, an issuer could load up on secured debt after a bond is issued, leaving existing bondholders with unsecured, junior claims in a default scenario."),
            _mcq("When comparing P/E ratios in stock selection, which approach is MOST appropriate?",
                 ["Compare the stock's P/E to a fixed threshold of 15x regardless of sector",
                  "Buy any stock with P/E below 20x as it is undervalued",
                  "Compare the P/E to sector peers and the stock's own historical P/E range to assess relative valuation",
                  "Ignore P/E for insurance company equity portfolios — only dividend yield matters"],
                 2,
                 "P/E ratios must be evaluated in context: a P/E of 20x is cheap for a fast-growing technology company but expensive for a slow-growth utility. Comparing to sector peers and the company's own historical range identifies true relative valuation. A single absolute threshold (e.g., '20x is always cheap') ignores sector-specific valuation norms."),
            _scenario(
                "Nationwide's credit analyst evaluates two bonds for the life insurance segment (target duration: 12 years): Bond X: AAA-rated utility bond, 12-year maturity, yield 4.8%, spread +35 bps, Debt/EBITDA 2.1x, standard covenants. Bond Y: BBB-rated telecom bond, 12-year maturity, yield 5.9%, spread +146 bps, Debt/EBITDA 4.8x, no negative pledge covenant.",
                "Which bond is the BETTER selection for Nationwide's life insurance segment, and why?",
                [("Bond Y — the 110 bps higher yield always makes it the better choice regardless of risk", False,
                  "Higher yield without risk analysis is yield-chasing. Bond Y's 4.8x Debt/EBITDA (approaching junk territory) and missing negative pledge covenant represent serious risks. The spread may not adequately compensate."),
                 ("Bond X — the superior credit quality, conservative leverage, and standard covenant protection make it more appropriate for a core life insurance segment", True,
                  "Correct. Bond X's AAA rating, 2.1x leverage (very conservative), and standard covenants make it highly appropriate for a core insurance segment. The 35 bps spread is tight but fair for AAA quality. Bond Y's 4.8x leverage, missing covenant, and BBB rating create material risk for a segment where solvency protection is paramount."),
                 ("Bond Y — the BBB rating is still investment grade and life insurers can accept all investment-grade bonds equally", False,
                  "Not all investment-grade bonds are equally appropriate. Bond Y's high leverage and missing covenant create materially higher risk than Bond X, despite both being technically investment grade. For a core life insurance segment, quality matters — yield-chasing with weak-covenant BBB bonds is poor practice.")]
            ),
        ]
    )

    # Concept 4: Fund Evaluation and Selection
    c4 = _concept(
        m2_id, 2,
        "Fund Evaluation and Selection: Classifications, Styles, Expenses, and Ratings",
        "Describe the framework for evaluating and selecting investment funds — including fund classifications, investment styles, management expense ratios, management team assessment, fund ratings, and fund comparisons.",
        "Insurance companies often invest a portion of their portfolio through funds (mutual funds, ETFs, private equity funds, real estate funds) rather than directly in securities. Fund selection requires its own rigorous evaluation: understanding the fund's investment style (value vs. growth, large-cap vs. small-cap), assessing the management team's track record and stability, comparing expense ratios (which directly reduce returns), reviewing independent ratings (Morningstar, Lipper), and comparing to peer funds with similar mandates. A fund that sounds good may deliver poor results if expenses are high, the manager is new, or the investment style has drifted.",
        "Lincoln Financial invests $8 billion through external equity managers. Their fund evaluation process: Step 1 — classify by investment style (US large-cap value, US large-cap growth, international developed, emerging markets); Step 2 — screen for minimum track record (5+ years for the same management team); Step 3 — expense ratio maximum (0.75% for active equity, 0.10% for passive index); Step 4 — review Morningstar and Lipper ratings (minimum 3-star Morningstar, top quartile in Lipper category); Step 5 — conduct qualitative due diligence (strategy consistency, risk management process, team stability); Step 6 — compare to 3 peer funds on risk-adjusted return (Sharpe ratio), maximum drawdown, and style consistency. This process filters 300+ potential managers to 15-20 approved for investment.",
        [
            "Fund classifications: style (value/growth/blend), market cap (large/mid/small), geography (domestic/international/emerging).",
            "Expense ratio directly reduces returns — a 1% expense ratio costs $1M annually per $100M invested; prefer low-cost options.",
            "Management team stability: a fund with a 10-year track record is meaningless if the manager changed 2 years ago.",
            "Morningstar ratings (1-5 stars) are risk-adjusted relative to peers; Lipper rankings show performance percentile within peer group.",
        ],
        [
            "Assuming past performance guarantees future results — it does not, especially if the manager or strategy has changed.",
            "Ignoring expense ratios — a 0.5% higher expense ratio compounded over 20 years is enormous.",
            "Using ratings alone — Morningstar stars reflect recent risk-adjusted returns; they don't predict future performance.",
        ],
        lessons=[
            _intro("Choosing a Fund: More Than Just Past Performance",
                   "Picking a fund based only on last year's returns is one of the most common investor mistakes. Fund evaluation requires understanding what the fund actually does, who's doing it, what it costs, and how it compares — not just where it ranked last quarter."),
            _teach("Fund Classifications and Investment Styles",
                   "Investment funds are classified by investment style and market segment. Style classifications: (1) Value — invests in undervalued stocks with low P/E, P/B; (2) Growth — invests in companies with high earnings growth potential, typically higher P/E; (3) Blend — mix of value and growth. Market cap classifications: Large-cap (companies with market cap >$10 billion), Mid-cap ($2-10 billion), Small-cap (<$2 billion). Geographic classifications: Domestic, International Developed (Europe, Japan), Emerging Markets (China, India, Brazil). The Morningstar style box is a 9-cell grid (3 styles x 3 market caps) that classifies any equity fund. Bond funds classify by duration (short/intermediate/long) and credit quality (government/investment-grade/high-yield).",
                   ["Value vs. growth is the most fundamental equity fund distinction — they perform very differently in different market cycles.",
                    "Market cap determines risk profile: small-cap funds are more volatile but offer higher long-run return potential.",
                    "Style drift: a value fund that starts buying growth stocks is style drift — problematic for diversification planning.",
                    "Bond fund classification: duration and credit quality define the risk profile."]),
            _teach("Expense Ratios, Manager Evaluation, and Fund Ratings",
                   "Management Expense Ratio (MER or expense ratio) is the annual fee as a percentage of assets that reduces investor returns. A fund with a 1.2% expense ratio earns 1.2% less than its gross return for investors. Over 20 years, a 1% expense difference compounds enormously: $100M earning 8% grows to $466M; at 7% (after 1% fee) it grows to only $387M — a $79M difference. Management team assessment evaluates: tenure (how long has the current team managed this fund?), consistency (does the strategy match what is documented?), firm stability (ownership, key person risk). Morningstar ratings (1-5 stars) rank funds risk-adjusted within their peer category. Lipper ratings show performance percentile versus category peers.",
                   ["Expense ratio directly subtracts from return — prefer lowest-cost option among similar funds.",
                    "Management continuity: a 10-year track record belongs to the managers who built it, not a new hire.",
                    "Morningstar 5-star = top 10% risk-adjusted in peer category; 1-star = bottom 10%.",
                    "Lipper rankings: top quartile (25th percentile) = outperformed 75% of peers."]),
            _example("Lincoln Financial's Manager Selection Process",
                     "Lincoln Financial evaluated US Large-Cap Value managers in 2023. Starting pool: 47 funds. After style screening (confirmed pure value exposure via Morningstar style box): 31 funds. After minimum 5-year track record with current manager: 22 funds. After expense ratio screen (maximum 0.75% for active): 18 funds. After minimum Morningstar 3-star and Lipper top quartile: 11 funds. After quantitative analysis (5-year Sharpe ratio vs. Russell 1000 Value benchmark, maximum drawdown 2020-2022, style consistency via returns-based analysis): 6 funds. After qualitative due diligence (strategy description, risk committee review): 4 approved managers. Lincoln divided its $1.2 billion US large-cap value allocation across these 4 managers, averaging $300M each.",
                     "Fund selection is a progressive filtration process: start with hundreds of candidates, apply successive screens, and conduct detailed due diligence only on the finalists."),
            _flash("What does the Management Expense Ratio (MER) represent?",
                   "MER is the annual fee charged by a fund as a percentage of assets, expressed as a percentage. It directly reduces investor returns: a fund with a gross return of 8% and MER of 1.2% delivers a net return of 6.8%. The MER includes management fees, administrative costs, and other operating expenses — but NOT transaction costs."),
            _mcq("A fund's Morningstar rating changed from 5 stars to 3 stars last quarter. What is the MOST LIKELY explanation?",
                 ["The fund's management expense ratio decreased",
                  "The fund's manager received a promotion",
                  "The fund's risk-adjusted performance declined relative to its peer group over the trailing 3-5 years",
                  "The fund increased the number of holdings from 50 to 100 stocks"],
                 2,
                 "Morningstar ratings are backward-looking risk-adjusted performance rankings within a peer category. A drop from 5 to 3 stars reflects declining risk-adjusted performance relative to category peers over the 3-5 year trailing period. It could reflect absolute underperformance, higher volatility than peers, or both."),
            _mcq("Two equity funds both averaged 9% returns over 5 years. Fund A has an expense ratio of 0.15%; Fund B has an expense ratio of 1.25%. Which fund delivered BETTER value to investors?",
                 ["Fund B — it must have taken more risk to earn the same gross return",
                  "Fund A — the 1.1% lower expense ratio means significantly more net return reached investors",
                  "They are equivalent — gross returns were identical",
                  "Fund B — higher expenses indicate better quality management"],
                 1,
                 "Both funds had the same gross return (9%), but Fund A's investors kept more of it. Fund A net return: ~8.85%; Fund B net return: ~7.75%. Over 20 years on $100M: Fund A grows to $558M vs. Fund B to $444M — a $114M difference attributable entirely to the expense ratio difference."),
            _mcq("A manager with a 15-year track record of outperforming the Russell 1000 Value benchmark retires. The fund hires a new manager. What must an institutional investor do BEFORE maintaining its full allocation?",
                 ["Nothing — the fund's 15-year track record guarantees future performance",
                  "Immediately sell the entire position and replace with a passive index",
                  "Re-evaluate the fund as if it were a new manager — the historical track record belongs to the retired manager",
                  "Increase the allocation, since the historical alpha demonstrates fund quality regardless of manager"],
                 2,
                 "Fund track records belong to the managers who built them, not the fund vehicle. When the manager changes, the institutional investor must evaluate the new manager's track record, strategy, and qualifications from scratch. The 15-year historical record is irrelevant for predicting the new manager's performance."),
            _mcq("What does 'style drift' mean in fund evaluation?",
                 ["A fund changing its expense ratio mid-year",
                  "A fund gradually shifting away from its stated investment style (e.g., a value fund begins buying growth stocks)",
                  "A fund's benchmark changing to a different index",
                  "A fund increasing its number of holdings beyond its mandate"],
                 1,
                 "Style drift occurs when a fund deviates from its stated investment mandate. A 'US Large-Cap Value' fund that begins owning growth stocks disrupts the investor's asset allocation plan — the investor thought they were allocated to value, but the fund is now providing growth exposure, possibly duplicating other holdings and violating the portfolio's diversification design."),
            _mcq("Which fund rating service measures performance relative to peer funds within the same investment category?",
                 ["S&P Global Ratings", "A.M. Best", "Morningstar and Lipper", "Moody's Investors Service"],
                 2,
                 "Morningstar (1-5 star rating system) and Lipper (percentile rankings within category) both measure fund performance relative to peer funds in the same investment category. S&P, Moody's, and A.M. Best rate credit quality of individual securities and insurance company financial strength — not mutual fund relative performance."),
            _scenario(
                "Protective Life's investment committee reviews two US Large-Cap Blend fund candidates for a $500M allocation: Fund A — Morningstar 4-star, expense ratio 0.82%, current manager in place 3 years (prior manager had 12-year 5-star track record), recent 3-year Sharpe ratio 0.65, style box: Large Blend confirmed. Fund B — Morningstar 3-star, expense ratio 0.18%, same management team 9 years, recent 3-year Sharpe ratio 0.71, style box: Large Blend confirmed, top-quartile Lipper ranking 4 of last 5 years.",
                "Which fund should Protective Life select?",
                [("Fund A — Morningstar 4-star rating is superior to Fund B's 3-star", False,
                  "Fund A's Morningstar rating reflects the prior manager's 12-year record, not the current manager's 3-year tenure. The 3-star Fund B with 9 years of manager continuity is more predictive of future performance than Fund A's backward-looking star rating under a different manager."),
                 ("Fund B — higher Sharpe ratio, much lower expense ratio, proven manager continuity, and consistent peer outperformance outweigh the 1-star rating difference", True,
                  "Correct. Fund B wins on every meaningful criterion: better risk-adjusted performance (Sharpe 0.71 vs. 0.65), dramatically lower expense ratio (0.18% vs. 0.82% — saving $3.2M annually on $500M), demonstrated manager continuity (9 years vs. 3), and consistent Lipper top-quartile rankings. Fund A's 4-star rating is misleading since it reflects the previous manager."),
                 ("Neither fund — only passive index funds are appropriate for insurance company equity allocations", False,
                  "Active management is appropriate when the expected alpha exceeds the expense ratio. Fund B's consistent top-quartile Lipper performance suggests the management team adds value above passive alternatives.")]
            ),
        ]
    )

    m2["concepts"] = [c3, c4]
    ch["modules"] = [m1, m2]
    return ch


def _build_ch8(course_id):
    ch_id = _id()
    ch = {
        "id": ch_id, "course_id": course_id, "order": 8,
        "title": "Portfolio Management and Operations",
        "description": "How institutional investment portfolios are actively managed day-to-day — including diversification, hedging, tactical asset allocation, bond strategies, securities trading, operational controls, private placements, and real estate investment management.",
    }

    # ── Module 1: Active Portfolio Management Strategies ─────────────────────
    m1_id = _id()
    m1 = {"id": m1_id, "chapter_id": ch_id, "order": 1,
          "title": "Active Portfolio Management Strategies"}

    # Concept 1: Diversification, Hedging, and Tactical Asset Allocation
    c1 = _concept(
        m1_id, 1,
        "Diversification, Hedging, and Tactical Asset Allocation",
        "Describe how institutional portfolio managers use diversification, hedging instruments, and tactical asset allocation — including market timing — to manage risk and enhance returns relative to the strategic asset allocation.",
        "Strategic asset allocation sets the long-term target mix. But markets move constantly, creating risks and opportunities that require active management responses. Portfolio managers use three primary tools: diversification (spreading exposures across uncorrelated assets to reduce portfolio volatility), hedging (using derivatives to offset specific risks without selling underlying positions), and tactical asset allocation (making deliberate, time-limited deviations from the strategic targets when valuations or economic conditions warrant). Market timing — trying to predict short-term market direction — is the most controversial tactic: evidence suggests it rarely adds consistent value, yet some institutions attempt it. Understanding all three tools, their costs, and their limitations is essential to professional portfolio management.",
        "Prudential Financial's $400 billion general account uses all three tools simultaneously. Diversification: holdings span 15 asset classes across 40 countries, with maximum single-issuer exposure of 1.5%. Hedging: the equity portfolio uses protective put options during earnings seasons; the bond portfolio uses interest rate swaps to fine-tune portfolio duration without selling bonds. Tactical tilts: when IG credit spreads widened to 200+ bps in 2022 (vs. long-run average 150 bps), Prudential tactically overweighted corporate bonds by 5% vs. strategic target, betting on spread compression — which materialized in 2023, adding ~$800M in excess return. They explicitly avoid market timing for broad equity markets after a 1990s study showed it destroyed value net of transaction costs.",
        [
            "Diversification reduces specific (idiosyncratic) risk; it cannot eliminate systematic (market) risk.",
            "Hedging is not free — options cost premiums, swaps have bid/ask spreads; net benefit must justify the cost.",
            "Tactical asset allocation: time-limited, disciplined over/underweights vs. strategic target based on valuation signals.",
            "Market timing (predicting short-term market direction) has very weak evidence of success and high transaction costs.",
        ],
        [
            "Thinking diversification means owning many things — owning 50 highly correlated stocks provides little real diversification.",
            "Confusing hedging with eliminating risk entirely — hedges protect against specific risks but introduce basis risk and cost.",
            "Treating tactical allocation as speculation — legitimate TAA is disciplined and mean-reverting, not trend-chasing.",
        ],
        lessons=[
            _intro("Active Management: Three Tools Beyond the Strategic Blueprint",
                   "The strategic asset allocation is the foundation. But between quarterly reviews, markets move, valuations shift, and risks emerge. Portfolio managers have three powerful responses: diversification, hedging, and tactical allocation. Let's unpack each."),
            _teach("Diversification: Correlation Is Everything",
                   "Diversification reduces portfolio risk by combining assets whose returns don't move together (low or negative correlation). The math: portfolio variance = weighted sum of individual variances PLUS cross-product correlation terms. When correlations are low, the cross-product terms are small, so portfolio variance is much less than the weighted sum of individual variances. Effective diversification requires: (1) Across asset classes — stocks, bonds, real estate, commodities are less than perfectly correlated; (2) Within asset classes — across sectors, geographies, credit ratings; (3) Across time horizons — laddering bond maturities; (4) Across currencies — international exposure adds diversification (and currency risk). The key insight: adding an asset with slightly lower expected return but low correlation to the portfolio can IMPROVE the risk-adjusted return of the whole portfolio.",
                   ["Correlation of +1.0 = no diversification benefit; -1.0 = perfect hedge.",
                    "Correlations increase during market crises — when you need diversification most, it often provides less benefit.",
                    "International diversification reduces home-country concentration but adds currency and political risk.",
                    "Maximum position limits (e.g., 2% per issuer) mechanically enforce diversification."]),
            _teach("Hedging and Tactical Asset Allocation",
                   "Hedging uses derivatives to offset specific risks without selling the underlying position. Common insurance company hedges: (1) Interest rate swaps — convert fixed-rate bond income to floating (or vice versa) to adjust duration without trading bonds; (2) Protective puts — buy put options on equity positions to cap downside loss; (3) Currency forwards — lock in exchange rates for international portfolio positions; (4) Credit default swaps — buy CDS protection to hedge credit exposure on specific bonds without selling them. Tactical Asset Allocation (TAA) involves deliberate, time-limited deviations from strategic weights based on valuation signals. TAA logic: asset classes mean-revert over time; when spreads are unusually wide or P/Es are unusually low relative to history, overweighting creates opportunity. TAA requires: predefined signals (not gut feelings), position size limits (typically ±5-10% of strategic weight), and a discipline to exit when valuations normalize.",
                   ["Swap: exchange of cash flows — payer swap: pay fixed, receive floating; receiver swap: pay floating, receive fixed.",
                    "Protective put: pay premium today to limit downside; net position = stock + put = capped loss.",
                    "TAA is valuation-driven and mean-reverting — different from momentum-chasing speculation.",
                    "TAA bands: strategic weight ±5% is common; larger deviations require committee approval."]),
            _example("MetLife's 2022 Credit Spread TAA",
                     "In October 2022, investment-grade corporate bond spreads hit 180 bps, well above the 10-year average of 120 bps. MetLife's TAA committee saw this as a valuation signal: spreads that wide historically compressed within 12-18 months. MetLife's SAA target: 40% IG corporate bonds. TAA decision: increase to 45% (a +5% tactical overweight), funded by reducing short-term bonds from 8% to 3%. They set a price target: close the TAA when spreads tighten to 130 bps. By Q2 2023, spreads compressed to 125 bps. MetLife reversed the TAA, returning to strategic weights. Estimated TAA contribution: +42 bps excess return on total portfolio. This is textbook TAA: signal-driven, position-limited, discipline-enforced, and exit-targeted.",
                     "Successful TAA is disciplined and process-driven — it's buying value, not predicting markets. The exit rule is as important as the entry signal."),
            _flash("Why does adding a low-correlation asset to a portfolio often improve the portfolio's risk-adjusted return?",
                   "Because portfolio variance is determined not just by individual asset volatilities but by the correlation between assets. A low-correlation asset reduces the portfolio's total variance (risk) more than it reduces expected return — improving the Sharpe ratio (return per unit of risk). This is the mathematical foundation of diversification."),
            _mcq("A portfolio manager uses an interest rate swap (pay fixed, receive floating) to reduce portfolio duration. What risk is this PRIMARILY designed to address?",
                 ["Credit risk — the risk that bond issuers will default",
                  "Interest rate risk — the risk that rising rates will reduce the value of fixed-rate bonds",
                  "Currency risk — the risk that foreign exchange rates will move unfavorably",
                  "Liquidity risk — the risk that bonds cannot be sold quickly at fair value"],
                 1,
                 "By paying fixed and receiving floating via a swap, the manager effectively converts fixed-rate bond cash flows to floating, shortening portfolio duration. When rates rise, the floating receipts increase while the fixed payments remain constant — offsetting the price decline in the fixed-rate bond holdings. This directly addresses interest rate (duration) risk."),
            _mcq("Which statement BEST describes the relationship between diversification and systematic risk?",
                 ["Diversification eliminates all portfolio risk, including systematic risk",
                  "Diversification reduces specific (idiosyncratic) risk but cannot eliminate systematic (market) risk",
                  "Diversification only works for bond portfolios, not equity portfolios",
                  "Diversification increases systematic risk by adding more holdings to the portfolio"],
                 1,
                 "Diversification eliminates specific risk (company-specific or sector-specific events) by holding many uncorrelated positions — the bad news about one position is offset by normal or good news about others. But systematic risk (broad market movements driven by macroeconomic factors) affects all assets simultaneously and cannot be diversified away. Hedging (not diversification) is needed to address systematic risk."),
            _mcq("A portfolio manager buys protective put options on the equity portfolio. What is the PRIMARY cost of this hedge?",
                 ["The portfolio can no longer benefit from rising equity prices",
                  "The option premium paid, which reduces net portfolio return if the hedge is not needed",
                  "The portfolio must be sold entirely and repurchased after the hedge expires",
                  "Credit default swaps must be purchased simultaneously for the hedge to work"],
                 1,
                 "Protective puts are insurance — the premium is the cost. If equity markets rise (the hedge is not needed), the premium is lost and reduces net return. The portfolio retains full upside above the put strike price; the option only triggers if the market falls below the strike. This 'insurance premium' must be weighed against the downside protection benefit."),
            _mcq("Which of the following is MOST consistent with disciplined tactical asset allocation (as opposed to market timing speculation)?",
                 ["Increasing equity exposure because a portfolio manager predicts markets will rise next quarter",
                  "Overweighting high-yield bonds when spreads are 300 bps above their 10-year historical average, with a predefined exit when spreads normalize",
                  "Selling all bonds and moving to cash because the manager believes a recession is coming",
                  "Matching the benchmark exactly at all times to avoid any performance deviation"],
                 1,
                 "Disciplined TAA has three hallmarks: (1) valuation-driven entry signal (spreads 300 bps above average is a quantifiable signal, not a prediction); (2) predefined exit rule (exit when spreads normalize — removes discretion); (3) position limits (still within a reasonable overweight, not a wholesale shift). Predicting market direction next quarter is speculation. Moving entirely to cash is an extreme tactical move inconsistent with TAA discipline."),
            _mcq("In a period of market stress, asset correlations often:",
                 ["Decrease sharply, making diversification more effective",
                  "Remain completely stable regardless of market conditions",
                  "Increase toward +1.0, reducing the benefit of diversification precisely when it is most needed",
                  "Become negative, making hedging unnecessary"],
                 2,
                 "This is one of the most important empirical observations in portfolio management: during market crises (2008, 2020), correlations across most asset classes converge toward +1.0 as investors sell everything simultaneously to raise cash. This 'correlation breakdown' means diversified portfolios provide less protection during the worst market dislocations — exactly when protection is most needed. This is why hedges (not just diversification) are valuable in stress scenarios."),
            _scenario(
                "Great-West Life's equity portfolio (10% of total assets) has had a strong run and now represents 13% of total assets — above the strategic range of 8-12%. The investment committee discusses three responses: Option A — do nothing, wait for equities to naturally revert to 10%. Option B — sell 3% of total assets worth of equities and buy bonds to restore the 10% target immediately. Option C — buy put options on the equity position to cap further upside-driven drift while allowing time to rebalance gradually over 3 months.",
                "Which response BEST reflects disciplined tactical portfolio management for an insurance company?",
                [("Option A — drifting above strategic ranges is acceptable as long as returns are strong", False,
                  "Allowing persistent drift above IPS limits violates the investment policy statement. If equities continue rising, the drift compounds and regulatory capital requirements may be breached. Waiting passively for 'natural reversion' is not disciplined portfolio management."),
                 ("Option B — immediately rebalancing restores the strategic allocation and eliminates the drift risk", True,
                  "Correct. Rebalancing to the strategic target when positions drift outside approved ranges is a core obligation of institutional portfolio management. Selling $3% equities and buying bonds restores the IPS-mandated allocation. The cost (transaction costs, potential capital gains) is the price of maintaining governance discipline."),
                 ("Option C — buying put options preserves upside while managing the drift; best risk-adjusted response", False,
                  "Put options cap downside but don't reduce the actual equity allocation — the portfolio still exceeds the IPS limit of 12%. Regulators and risk frameworks require actual position compliance, not hedged compliance. Option C may be appropriate as a bridge tactic over 1-2 weeks while executing Option B, but not as a substitute.")]
            ),
        ]
    )

    # Concept 2: Bond Portfolio Management Strategies
    c2 = _concept(
        m1_id, 2,
        "Bond Portfolio Management Strategies",
        "Describe the active bond portfolio management strategies used by institutional investors — including duration management, yield curve strategies, sector rotation, and credit spread trading.",
        "Bond portfolio management is not passive — even in a 'buy and hold' framework, managers constantly assess whether to trade, adjust duration, rotate sectors, or trade around yield curve changes. Active bond strategies fall into four categories: (1) Duration management — increasing or decreasing portfolio interest rate sensitivity based on rate forecasts; (2) Yield curve strategies — positioning across the curve (short-term vs. long-term) based on expected curve shape changes; (3) Sector rotation — moving between government, corporate, and municipal bonds based on relative value; (4) Credit spread trading — overweighting or underweighting specific credit quality tiers based on spread level and economic outlook. Each strategy has return potential and risk, requiring clear signal discipline and cost awareness.",
        "PIMCO's insurance client portfolios use all four strategies. Their duration management process: if the investment team expects rates to fall, they extend portfolio duration above benchmark; if rates are expected to rise, they shorten below benchmark. In 2022-2023 (rising rates), PIMCO portfolios were positioned with duration 1-2 years below benchmark, reducing mark-to-market losses by an estimated 3-4% vs. a duration-neutral position. Their sector rotation in 2022: reduced corporate bonds (widening spreads), increased government bonds (safe haven), then reversed in late 2022 as corporate spreads peaked — earning spread compression returns as credit markets recovered.",
        [
            "Duration extension: increase duration to profit when rates are expected to fall; shortening: reduce duration to protect when rates expected to rise.",
            "Yield curve strategies: bullet (concentrated in one maturity), barbell (split between short and long), ladder (evenly distributed).",
            "Sector rotation: move between government, IG corporate, HY, and municipal bonds based on relative value.",
            "Credit spread trading: overweight credit risk when spreads are wide (cheap); underweight when spreads are tight (expensive).",
        ],
        [
            "Confusing duration shortening with selling bonds — duration can be shortened by selling long bonds and buying short bonds, or by using swaps without selling.",
            "Thinking yield curve strategies are always the same — bullet vs. barbell vs. ladder have very different risk/return profiles under different curve scenarios.",
            "Treating sector rotation and credit spread trading as the same thing — sector rotation is about asset class mix; credit spread trading is about quality tier within a sector.",
        ],
        lessons=[
            _intro("Managing the Bond Portfolio: Four Active Strategies",
                   "Bonds are not 'set and forget' investments. Active bond management extracts return from four sources: where you are on the interest rate spectrum (duration), where you sit on the yield curve (maturity positioning), which sectors you own, and which credit quality you emphasize. Let's examine each."),
            _teach("Duration Management and Yield Curve Strategies",
                   "Duration management adjusts the portfolio's sensitivity to interest rate changes. Duration extension (increasing portfolio duration above benchmark) profits when rates fall — long-duration bonds appreciate more than short-duration bonds when rates decline. Duration shortening (below benchmark) protects capital when rates are expected to rise. Duration can be managed by trading bonds or by using interest rate swaps (more efficient, no transaction costs on the bond portfolio). Yield curve strategies position across maturities based on expected curve shape changes: (1) Bullet strategy — concentrate holdings in one maturity point (e.g., all 10-year bonds). Most exposed to that maturity's rate movement; (2) Barbell strategy — split holdings between very short and very long maturities, avoiding the intermediate. Profits when the yield curve 'steepens' (short rates fall, long rates rise) or when intermediate bonds underperform; (3) Ladder strategy — distribute holdings evenly across all maturities. Provides consistent income and automatic reinvestment as bonds mature. Most commonly used by insurance companies for ALM stability.",
                   ["Duration extension: buy long bonds / sell short bonds (or receive-fixed swap).",
                    "Duration shortening: buy short bonds / sell long bonds (or pay-fixed swap).",
                    "Bullet profits when the specific targeted maturity's yield falls more than others.",
                    "Barbell profits when the yield curve steepens or when 'the belly' of the curve underperforms."]),
            _teach("Sector Rotation and Credit Spread Trading",
                   "Sector rotation involves shifting the bond portfolio's composition across major sectors (government bonds, investment-grade corporates, high-yield bonds, municipal bonds, mortgage-backed securities) based on relative value and economic conditions. In recession: shift to government bonds (flight to quality) and reduce corporate bonds (rising default risk). In expansion: shift to corporate bonds (spread compression), reduce governments. Credit spread trading operates within a sector — moving up or down the quality spectrum based on spread levels. When IG corporate spreads are wide relative to history, overweight IG corporates (buy cheap). When IG spreads are tight, underweight (sell rich). Similarly within high yield: when the HY/IG spread differential is at historically high levels, rotating into BB-rated bonds captures spread compression as the economy stabilizes.",
                   ["Sector rotation is driven by macro/economic cycle — recession favors governments; expansion favors corporates.",
                    "Credit spread trading within IG: AAA vs. A vs. BBB positioning based on spread differentials.",
                    "Flight to quality: automatic demand for government bonds in market stress (prices rise, yields fall).",
                    "Municipal bond attractiveness is tax-dependent: higher-tax-rate institutions prefer munis for after-tax yield."]),
            _example("PIMCO's Rate-Cycle Duration Management",
                     "In January 2022, 10-year Treasury yields were 1.6% and the Federal Reserve signaled significant rate hikes. PIMCO's insurance client portfolios had benchmark duration of 8.5 years. Duration management decision: shorten to 6.5 years (2 years below benchmark). Method: sold long-duration corporate bonds (20-30 year maturities), bought short-term T-bills and 2-year Treasuries. By December 2022, 10-year yields hit 4.3%. The 8.5-year benchmark lost approximately 16% in mark-to-market value. PIMCO's 6.5-year positioned portfolio lost approximately 12% — 4 percentage points of relative outperformance purely from duration management. When PIMCO's model signaled peak rates in November 2022, they extended duration back to 9.5 years (above benchmark) to capture the subsequent rate decline in 2023.",
                     "Duration management must be reversible and disciplined: shorten to protect in rising rate environments, extend to profit in falling rate environments, with systematic entry and exit signals."),
            _flash("What is the key difference between a bullet, barbell, and ladder bond portfolio strategy?",
                   "Bullet: concentrates all holdings in one maturity point — simple but exposed to rate movements at that specific point. Barbell: splits holdings between very short and very long maturities, avoiding intermediate — profits from curve steepening. Ladder: distributes holdings evenly across all maturities — provides stable, predictable cash flows and automatic reinvestment. Insurance companies most commonly use laddering for ALM stability."),
            _mcq("A portfolio manager believes interest rates will fall significantly over the next 12 months. What duration management action would MAXIMIZE benefit from this view?",
                 ["Shorten portfolio duration significantly below the benchmark",
                  "Maintain portfolio duration exactly equal to the benchmark",
                  "Extend portfolio duration significantly above the benchmark",
                  "Eliminate all duration by holding only floating-rate bonds"],
                 2,
                 "When interest rates fall, bond prices rise — and longer-duration bonds appreciate MORE than shorter-duration bonds (higher price sensitivity). Extending duration above benchmark positions the portfolio to capture maximum price appreciation if rates fall as predicted. This is the classic duration management bet on falling rates."),
            _mcq("During a recession, an institutional bond portfolio manager shifts from 40% investment-grade corporate bonds to 40% government bonds. This is BEST described as:",
                 ["Tactical asset allocation between stock and bond asset classes",
                  "Sector rotation — moving within the bond asset class based on economic cycle conditions",
                  "Credit spread trading within the investment-grade corporate sector",
                  "Duration management — adjusting the portfolio's interest rate sensitivity"],
                 1,
                 "Moving from corporate to government bonds is sector rotation — shifting the portfolio's composition across bond sectors (government vs. corporate) based on the economic cycle. In recessions, corporate default risk rises and spreads widen, making government bonds relatively more attractive. This is a sector-level decision, not a TAA decision (which would shift between stocks and bonds) or credit spread trading (within-sector quality shifts)."),
            _mcq("Which yield curve strategy would MOST BENEFIT when the yield curve 'steepens' (short-term rates fall while long-term rates rise)?",
                 ["Bullet strategy concentrated in 10-year bonds",
                  "Ladder strategy evenly distributed across all maturities",
                  "Barbell strategy with holdings concentrated in 2-year and 30-year bonds",
                  "A portfolio entirely invested in floating-rate bonds"],
                 2,
                 "In a curve steepening where short rates fall and long rates rise: short-term bond prices rise (short rates fell) and long-term bond prices fall (long rates rose). A barbell strategy benefits from the short-term bond price appreciation but is hurt by the long-term bond price decline. However, because short-duration bonds are LESS sensitive to rate changes than long-duration bonds, the gain from the short end typically exceeds the loss from the long end in a moderate steepening, especially if carry income is considered."),
            _mcq("An insurance company's bond portfolio manager increases the allocation to BBB-rated corporate bonds from 15% to 25% when IG spreads widen to 250 bps vs. the 10-year average of 140 bps. This is BEST described as:",
                 ["Duration extension — increasing the portfolio's sensitivity to interest rate changes",
                  "Sector rotation — moving from government to corporate bonds",
                  "Credit spread trading — overweighting credit risk when spreads are unusually wide",
                  "Yield curve positioning — concentrating in intermediate maturities"],
                 2,
                 "This is credit spread trading within the investment-grade corporate sector. The manager is increasing exposure to BBB-rated bonds (higher credit risk) specifically because spreads are at historically wide levels (250 bps vs. 140 bps average). The thesis: spreads are mean-reverting, and buying when they are wide captures compression as they return to normal levels. This is a valuation-driven within-sector quality bet."),
            _mcq("Which bond portfolio strategy MOST directly supports an insurance company's ALM by providing predictable cash flows across multiple time horizons?",
                 ["Bullet strategy — concentrating all bonds at one maturity point",
                  "Barbell strategy — splitting holdings between 2-year and 30-year bonds",
                  "Ladder strategy — distributing bond maturities evenly across all years",
                  "Zero-coupon strategy — purchasing only zero-coupon bonds"],
                 2,
                 "The ladder strategy evenly distributes bond maturities across all time horizons. As each rung matures, proceeds are reinvested at the long end — creating consistent, predictable cash flows that match liability schedules. This makes it the most commonly used maturity strategy for insurance company ALM portfolios, avoiding concentration risk in any single maturity point."),
            _scenario(
                "Lincoln National's bond portfolio has benchmark duration of 9 years. In March 2023, with 10-year Treasury yields at 4.0%, Lincoln's rate model signals a 60% probability that yields will rise another 75-100 bps over 6 months. The team debates two actions: Action A — maintain benchmark duration (9 years), avoiding the risk of being wrong on rates. Action B — shorten duration to 7 years using interest rate swaps (pay fixed, receive floating), with a predefined plan to extend back to 9+ years when the model signals peak rates.",
                "Which action is MORE consistent with skilled active bond management for an insurance general account?",
                [("Action A — maintaining benchmark duration eliminates tracking error and is always the safest choice", False,
                  "Maintaining benchmark duration when the model generates a clear signal is not 'safe' — it's passive management that foregoes the value of active analysis. If rates rise 100 bps as the model predicts, a 9-year duration portfolio loses roughly 9% in market value that could have been partially avoided."),
                 ("Action B — acting on the rate signal with a disciplined, reversible trade (swaps instead of bond sales) and a clear re-entry plan is proper active management", True,
                  "Correct. Action B has all elements of skilled active management: (1) clear signal (60% probability + 75-100 bps move = significant expected value); (2) efficient execution (interest rate swaps avoid costly bond transactions); (3) measured position (shortening 2 years, not eliminating all duration); (4) predefined reversal plan. The temporary tracking error is the cost of pursuing positive expected value."),
                 ("Action A — interest rate forecasting is unreliable, so managers should never deviate from benchmark duration", False,
                  "While rate forecasting is imperfect, consistently acting on high-confidence signals adds value over time even if individual calls are sometimes wrong. The key is discipline: predefined signals, position limits, and exit rules — not abandoning active management entirely because it carries uncertainty.")]
            ),
        ]
    )

    m1["concepts"] = [c1, c2]

    # ── Module 2: Trading and Operational Management ──────────────────────────
    m2_id = _id()
    m2 = {"id": m2_id, "chapter_id": ch_id, "order": 2,
          "title": "Trading, Operational Controls, and Alternative Asset Management"}

    # Concept 3: Securities Trading and Managing Individual Securities
    c3 = _concept(
        m2_id, 1,
        "Securities Trading: Mechanics, Costs, and Managing Individual Bond and Stock Positions",
        "Describe how institutional securities trades are executed — including trading mechanisms, transaction costs, best execution obligations, and the ongoing management of individual bond and stock positions.",
        "Deciding what to buy or sell is only part of portfolio management — execution matters enormously. Poor trading can erode 0.5-1.0% of annual return through excessive transaction costs, poor timing, or information leakage. Institutional trading involves: selecting the right trading mechanism (electronic vs. dealer vs. auction), managing market impact (large trades move prices), achieving best execution (regulatory and fiduciary obligation), and monitoring individual security positions for ongoing credit quality, dividend policy, or covenant changes. Once a bond or stock is purchased, it requires ongoing surveillance — not passive holding.",
        "Vanguard's institutional trading desk handles over $2 billion in daily bond transactions for insurance clients. Their execution methodology: bonds below $25M in face value trade electronically via MarketAxess (lowest cost, best price discovery). Bonds $25-100M use dealer RFQ (request for quote) — query 3-5 dealers simultaneously, take the best price. Bonds above $100M use block trading via negotiation to minimize market impact. Vanguard's internal measurement: actual execution price vs. mid-market price at the time the order was placed (implementation shortfall). Their target: execution within 5 bps of mid-market for liquid bonds. For equity, all orders above $1M are algorithmic (VWAP algorithms) to minimize market impact over the trading day.",
        [
            "Transaction costs: bid/ask spread (paid on every trade), commission (broker fee), market impact (large orders move prices).",
            "Best execution: fiduciary obligation to seek the most favorable terms reasonably available for every trade.",
            "Implementation shortfall: difference between the theoretical trade price (when decision was made) and actual execution price.",
            "Ongoing security monitoring: credit quality changes, covenant violations, dividend cuts, and issuer news require active response.",
        ],
        [
            "Thinking best execution means lowest commission — best execution considers all-in costs: spread, commission, AND market impact.",
            "Ignoring market impact for large positions — a $500M order to buy one stock will move the price as it is executed; ignoring this creates significant hidden costs.",
            "Treating bonds as 'hold to maturity, no monitoring needed' — credit quality can deteriorate; covenants can be violated; issuers can be downgraded or default.",
        ],
        lessons=[
            _intro("Trading and Managing Positions: The Execution Layer",
                   "Portfolio decisions don't execute themselves. How and when you trade determines whether you capture the value of your investment thesis — or give it away in transaction costs and poor execution. And once you own a security, your job is not done."),
            _teach("Securities Trading Mechanisms and Transaction Costs",
                   "Institutional investors trade through several mechanisms: (1) Exchange trading — equities primarily trade on organized exchanges (NYSE, NASDAQ) with visible bid-ask prices; (2) Dealer/OTC trading — most bonds trade over-the-counter through dealers who maintain inventories and quote bid/ask prices. Institutional bond orders use RFQ (request for quote) — the investor queries multiple dealers simultaneously and selects the best price; (3) Electronic trading platforms — MarketAxess (bonds), Bloomberg TSOX (bonds), dark pools (equities) provide electronic price discovery and reduce transaction costs; (4) Block trading — very large orders are negotiated directly with dealers to minimize market impact. Transaction cost components: (a) Bid/ask spread — the difference between dealer's buying price and selling price; (b) Commission — explicit broker fee (primarily equities); (c) Market impact — price movement caused by the order itself; (d) Opportunity cost — cost of delayed execution if the price moves before the order completes.",
                   ["RFQ: query 3-5 dealers, pick the best bid (selling) or best offer (buying) — competitive tension improves pricing.",
                    "Bid/ask spread for liquid government bonds: 1-2 bps. For illiquid corporate bonds: 50-100+ bps.",
                    "Market impact is proportional to order size relative to average daily volume.",
                    "Algorithmic trading (VWAP, TWAP) spreads large equity orders over time to minimize market impact."]),
            _teach("Best Execution and Monitoring Individual Positions",
                   "Best execution is both a fiduciary obligation and regulatory requirement: the manager must seek the most favorable terms reasonably available for every trade, considering not just price but also speed of execution, certainty of execution, and overall transaction cost. Best execution analysis: measure implementation shortfall (actual execution price vs. mid-market price when the investment decision was made). Ongoing position monitoring for bonds: (1) Credit surveillance — monitor issuer financial results, rating agency actions; sell or review if downgraded below minimum quality threshold; (2) Covenant monitoring — track compliance with indenture covenants; covenant violation triggers bondholder protections; (3) Call/maturity monitoring — track call dates and prepare reinvestment plans in advance. Ongoing monitoring for equities: (1) Earnings releases — does the company continue to meet the investment thesis? (2) Dividend policy — cut or suspension triggers reassessment; (3) Management changes — new management may alter strategy; (4) ESG developments — material ESG changes may trigger policy review.",
                   ["Implementation shortfall = (actual price - decision price) × shares; measures total trading cost.",
                    "Credit surveillance: watch for negative rating actions, missed earnings, leverage increases.",
                    "Covenant violation: cross-default provision means violation of one covenant triggers all bond covenants.",
                    "Dividend cut: signals deteriorating cash flow; income-oriented portfolio must reassess thesis."]),
            _example("Vanguard's Bond Execution and Credit Monitoring",
                     "In August 2023, Vanguard executed a $150M purchase of Walgreens (WBA) 5.5% bonds for a life insurance client. Size ($150M) required block trading — Vanguard called 6 dealers, got quotes ranging from 98.00 to 98.45, selected the 98.45 bid (cheapest for buyer). Implementation shortfall: mid-market was 98.50 at decision time; 98.45 actual = 5 bps cost (within their 5 bps target). Three months later, WBA's credit was downgraded from BBB to BB+ (junk). Vanguard's credit monitoring triggered: their policy required selling all sub-investment-grade bonds within 60 days. They executed a phased sell over 45 days — price dropped from 95 to 89 during the sell window as other institutional holders also sold. Despite the loss, disciplined policy execution prevented holding a junk-rated bond that subsequently fell to 72 (as WBA's financial position continued deteriorating).",
                     "Best execution is the entry; credit surveillance is the ongoing management. Both matter for total return."),
            _flash("What is 'implementation shortfall' in securities trading?",
                   "Implementation shortfall measures the total cost of executing a trade: the difference between the price when the investment decision was made (the theoretical 'paper' price) and the actual average execution price, multiplied by the number of shares/bonds. It captures all costs including spread, commission, and market impact in one metric."),
            _mcq("For a $200M bond trade, which trading mechanism is MOST appropriate to minimize transaction costs while ensuring execution?",
                 ["Post the order on a retail bond trading platform and wait for the best price",
                  "Negotiate directly with one trusted dealer who can guarantee execution at a fixed price",
                  "Use a request-for-quote (RFQ) process querying 4-6 dealers simultaneously, selecting the best price",
                  "Execute the full order on an exchange over one minute to minimize timing uncertainty"],
                 2,
                 "For large institutional bond trades, RFQ with multiple dealers (4-6) creates competitive tension that delivers the best price. One dealer (no competition) leaves money on the table. Retail platforms don't handle $200M institutional blocks. Bonds don't trade on exchanges. RFQ is the institutional standard for large bond orders."),
            _mcq("A portfolio manager's investment decision to buy a corporate bond was made when the mid-market price was 100.00. The actual average execution price was 99.75. The implementation shortfall is:",
                 ["0.25 bps", "0.25% of the trade value", "25 bps of the trade value", "25% of the trade value"],
                 2,
                 "Implementation shortfall = (decision price - execution price) / decision price = (100.00 - 99.75) / 100.00 = 0.25%. Since bond prices are quoted per $100 face value, 0.25 points = 25 basis points (bps) of price. This 25 bps is the all-in trading cost attributable to spread, market impact, and any timing differences."),
            _mcq("An insurance company's IPS requires selling any bond downgraded below BBB-. A holding is downgraded to BB+ (high yield). The portfolio manager argues the bond still yields 7% and projects recovery. What should happen?",
                 ["Hold the bond since the manager's projection of recovery may be correct",
                  "Sell the bond within the IPS-specified time limit regardless of the manager's view",
                  "Request a waiver from the board to hold the bond through the credit event",
                  "Convert the bond holding to a CDS position as an alternative to selling"],
                 1,
                 "The IPS requirement to sell sub-investment-grade bonds is a governance constraint, not a suggestion. Fiduciary duty requires following the IPS. The manager's projection may be correct, but overriding the IPS based on individual conviction undermines governance discipline and creates regulatory risk. Waivers exist for extraordinary circumstances but not routine credit opinions."),
            _mcq("Which trading cost is MOST unique to large institutional trades and does NOT affect small retail trades?",
                 ["Bid/ask spread", "Brokerage commission", "Market impact cost", "Settlement fees"],
                 2,
                 "Market impact is the price movement caused by the order itself — as large orders hit the market, they consume available liquidity, moving the price against the buyer (buying pushes price up) or seller (selling pushes price down). A retail investor buying $10,000 of stock has zero market impact. An institutional investor buying $500M of the same stock significantly moves the price during execution. This is why institutions use algorithmic trading and block negotiation to minimize market impact."),
            _mcq("An equity position's management team is replaced after the founding CEO retires. What ongoing monitoring action is MOST appropriate?",
                 ["Immediately sell the position since management changes always destroy value",
                  "Take no action — management teams are interchangeable and don't affect investment thesis",
                  "Review the investment thesis with the new team's strategy, capital allocation track record, and cultural fit before deciding to hold, add, or reduce",
                  "Increase the position since new management typically means a share price surge"],
                 2,
                 "Management changes are material events requiring thesis reassessment. The original investment may have been predicated on specific management skills, strategy, or capital allocation discipline. A new team may continue, improve, or undermine the thesis. The appropriate response: review, not reflexive action in either direction. Only after assessing the new team's strategy and track record can the portfolio manager make a hold/add/reduce decision."),
            _scenario(
                "Nationwide Life executes a $75M purchase of AT&T (T) 6.0% bonds. The investment team's decision price was 100.50 (mid-market at decision time). RFQ was sent to 5 dealers; quotes received: Dealer A: 100.40, Dealer B: 100.35, Dealer C: 100.45, Dealer D: 100.38, Dealer E: 100.42.",
                "Which dealer should Nationwide select, and what is the implementation shortfall?",
                [("Dealer B at 100.35 — lowest price for buyer means best execution; implementation shortfall is 15 bps", False,
                  "In bond buying, the buyer pays the OFFER price. A lower offer price means the buyer pays LESS — which is BETTER for a buyer. Dealer B's 100.35 is actually the best price for a buyer (cheapest to purchase). However, the implementation shortfall from 100.50 decision price to 100.35 execution = 15 bps, not zero — the market moved and/or Dealer B's spread is widest. The correct answer is to select Dealer A (100.40, closest to mid-market of 100.50 decision price, meaning tightest bid/ask)."),
                 ("Dealer A at 100.40 — this offer is closest to the 100.50 mid-market decision price, representing the tightest spread and lowest implementation shortfall of 10 bps", True,
                  "Correct. Best execution considers the all-in cost relative to the decision-time mid-market price. Dealer A's 100.40 offer is closest to the 100.50 mid-market (10 bps implementation shortfall). Dealer B at 100.35 has a 15 bps shortfall — while the absolute price is lower, the larger deviation from mid-market indicates a wider dealer spread. Dealer A offers the best execution."),
                 ("All dealers should be selected equally and the order split 20% each to maximize diversification of counterparty risk", False,
                  "While counterparty diversification has merit in some contexts, best execution requires selecting the BEST price. Splitting the order across all dealers would result in an average price worse than the best available price from Dealer A. The RFQ process exists precisely to identify and select the best price from a competitive set.")]
            ),
        ]
    )

    # Concept 4: Operational Controls, Private Placements, and Real Estate
    c4 = _concept(
        m2_id, 2,
        "Operational Controls, Private Placements, and Real Estate Investment Management",
        "Describe the operational controls required for institutional investment management, the unique features of private placement investments, and the management of direct real estate holdings.",
        "Investment decisions must be supported by robust operational infrastructure. Operational controls — segregation of duties, compliance monitoring, portfolio accounting, and reconciliation — prevent errors and fraud. Beyond public securities, insurance companies also invest in private placements (directly negotiated debt or equity with issuers, bypassing public markets) and direct real estate (owning properties rather than REITs). These alternative asset classes require specialized due diligence, legal documentation, ongoing asset management, and valuation processes that differ significantly from public market investing. Understanding these operational and alternative investment dimensions completes the picture of institutional portfolio management.",
        "New York Life's investment operation manages $350 billion across three segments: public markets (75%), private placements (18%), and direct real estate (7%). Operational controls: every trade requires dual approval (portfolio manager enters, compliance system validates, trading desk executes, back office confirms) — no single person can complete a trade end-to-end. Private placements: NY Life is one of the largest US private placement investors, deploying $15-20 billion annually directly with corporate issuers. These deals are negotiated bilaterally — NY Life sets its own covenants, selects its own maturities, and typically earns 50-150 bps yield premium over comparable public bonds. Direct real estate: NY Life owns $25 billion in commercial properties (office, industrial, multifamily, retail). Each property has a dedicated asset manager who handles leasing, capital expenditure planning, and property-level operations.",
        [
            "Segregation of duties: no single employee controls all steps of a trade — investment decision, execution, confirmation, and accounting must involve different people.",
            "Private placements: directly negotiated debt/equity with issuers; illiquid but offer yield premium, customized terms, and stronger covenants.",
            "Real estate management: ongoing responsibilities include leasing, maintenance, capital improvement, tenant management, and periodic property valuation.",
            "Portfolio accounting and reconciliation: daily P&L, position reconciliation between portfolio manager and custodian records is essential for control.",
        ],
        [
            "Thinking private placements are just like public bonds with a higher yield — they carry illiquidity risk and require extensive ongoing monitoring and legal relationship management.",
            "Assuming real estate is passive — direct property ownership requires active management of leases, maintenance, tenants, and capital expenditures.",
            "Underestimating operational risk — failures in reconciliation, settlement, or compliance monitoring have caused major losses (Barings Bank collapse: a single trader controlled both trading and settlement).",
        ],
        lessons=[
            _intro("Behind the Trade: Operations, Private Markets, and Real Estate",
                   "Every investment decision needs infrastructure to support it — controls to prevent errors and fraud, legal frameworks for private deals, and active management for real assets. This is the operational backbone of institutional investing."),
            _teach("Investment Operational Controls and Portfolio Accounting",
                   "Investment operations require four core controls: (1) Segregation of duties — no single person controls the full trade lifecycle. Portfolio manager decides what to trade; compliance system validates against IPS limits; trading desk executes; back office confirms and settles; accounting records the trade. Separation prevents both fraud and errors; (2) Compliance monitoring — automated systems check every trade before and after execution against IPS limits (position sizes, credit quality, sector limits, concentration caps). Pre-trade compliance prevents violations; post-trade monitoring catches breaches; (3) Portfolio accounting — daily valuation of all positions using pricing data from multiple independent sources. Mark-to-market positions daily; assess accrued income; calculate P&L by manager, strategy, and asset class; (4) Reconciliation — daily comparison of portfolio manager records vs. custodian bank records vs. broker confirmations. Any discrepancy triggers investigation — even a small reconciliation failure may signal an error or fraud.",
                   ["Segregation of duties: 4 different people/systems for: decide, execute, confirm, book.",
                    "Pre-trade compliance: automatic check before trade goes to market — rejects if it would violate IPS.",
                    "Post-trade compliance: end-of-day sweep for any positions drifted outside limits.",
                    "Reconciliation: portfolio records vs. custodian records must match to the penny daily."]),
            _teach("Private Placements and Direct Real Estate",
                   "Private placements are debt or equity securities issued and sold directly to institutional investors without a public offering. Key features: (1) Higher yield premium (50-150 bps) vs. comparable public bonds for the same issuer — compensates for illiquidity; (2) Customized terms — investors negotiate their own maturities, covenants, and amortization schedules; (3) Stronger covenants — private deals include more protective covenants than public bonds (financial maintenance tests, leverage limits, dividend restrictions); (4) Illiquid — no public market; selling requires finding another institutional buyer. Used for: corporate debt, infrastructure projects, equipment financing, real estate loans. Direct real estate investment involves owning property (office, multifamily, industrial, retail) directly rather than through REITs. Management responsibilities: negotiate and monitor tenant leases, oversee maintenance and capital improvements, plan and execute property renovations, manage property-level cash flows, conduct periodic independent appraisals (since real estate is not marked-to-market daily), and eventually decide to hold or sell each property.",
                   ["Private placement 144A: resale to qualified institutional buyers allowed; 4(a)(2): direct to institution, no resale.",
                    "NAIC ratings: private placements rated internally by insurers using NAIC designation criteria (not S&P/Moody's).",
                    "Real estate appraisal: independent appraiser values property annually or semi-annually.",
                    "Cap rate: Net Operating Income / Property Value — the yield equivalent for real estate; lower cap rate = more expensive property."]),
            _example("New York Life's Private Placement Program",
                     "New York Life closed a $250M private placement with a regional utility company in 2023. Structure: 15-year bullet maturity, 6.2% fixed coupon (vs. comparable public bonds at 5.6% — a 60 bps premium). Covenants: debt/EBITDA must remain below 4.5x (public bond covenants typically only require 5.5x); dividends restricted if debt/EBITDA exceeds 4.0x; no additional secured debt without matching pari passu protection for NY Life. Due diligence: 6-week process including financial model review, management interviews, plant site visits, and independent appraisal of the utility's rate base assets. Legal documentation: 85-page note purchase agreement. Ongoing monitoring: quarterly financial reporting required; annual management meetings; covenant compliance certification. NY Life allocated $250M from its life insurance segment (30-year liabilities), using the 15-year maturity as part of its ALM ladder. The 60 bps premium over comparable public bonds represents the 'illiquidity premium' for locking up capital for 15 years.",
                     "Private placements deliver meaningful yield premiums and stronger investor protections — but require sophisticated due diligence and ongoing relationship management that public bond investments do not."),
            _flash("What is the primary purpose of 'segregation of duties' in investment operations?",
                   "Segregation of duties ensures no single employee controls all steps of a transaction — investment decision, trade execution, trade confirmation, and accounting recording must involve different people and systems. This prevents both intentional fraud (a single person cannot manipulate all controls) and unintentional errors (a second person catches mistakes). The Barings Bank collapse (1995) occurred because Nick Leeson controlled both trading and settlement in Singapore — no segregation of duties."),
            _mcq("Which feature MOST distinguishes a private placement bond from a comparable public corporate bond?",
                 ["Private placements always have higher credit ratings than comparable public bonds",
                  "Private placements offer a yield premium for illiquidity and typically include stronger, more customized covenants",
                  "Private placements are sold through exchanges and have daily price quotes",
                  "Private placements are only available to retail investors, not institutional investors"],
                 1,
                 "Private placements offer: (1) illiquidity premium (50-150 bps yield above comparable public bonds) — compensating for lack of a secondary market; (2) customized terms negotiated directly between issuer and investor (maturity, covenants, amortization); (3) stronger covenants than public bonds. They are exclusively for institutional investors (insurance companies, pension funds) and have no exchange listing or daily price quotes."),
            _mcq("An investment operations team discovers a discrepancy between the portfolio manager's records and the custodian bank's records for a bond position — the PM shows $50M face value, the custodian shows $45M. What is the MOST appropriate immediate action?",
                 ["Adjust the portfolio manager's records to match the custodian without investigation",
                  "Assume the discrepancy is a rounding error and report the custodian's number",
                  "Immediately investigate the root cause — a trade may not have settled, a sale may not be recorded, or there may be an error in either system",
                  "Sell the disputed $5M to eliminate the discrepancy"],
                 2,
                 "Reconciliation discrepancies always require investigation before any adjustment. A $5M discrepancy could indicate: a failed settlement (trade executed but not delivered), a booking error in either system, a fraud attempt, or a genuine data error. Only by tracing the specific trade records can the root cause be identified and properly resolved. Adjusting records without investigation violates operational control standards."),
            _mcq("A direct real estate property in an insurance company's portfolio has its largest tenant (50% of rental income) announce bankruptcy. What is the MOST appropriate portfolio management response?",
                 ["Immediately write down the property value to zero and take a full loss",
                  "Take no action since real estate is a long-term investment and short-term tenant issues are irrelevant",
                  "Engage the asset management team to assess lease rejection risk, explore replacement tenant options, and update the property's valuation and cash flow projections",
                  "Sell the property immediately at any price to eliminate the risk"],
                 2,
                 "Direct real estate requires active management response to tenant credit events. The asset management team must: determine if the tenant will reject the lease in bankruptcy (common) or continue operations; assess realistic timeline and cost to re-let 50% of space; update cash flow projections and independent appraisal; and decide whether to hold (if re-letting prospects are good) or sell (if the building cannot be re-let). Neither panic selling nor ignoring the situation is appropriate."),
            _mcq("Why do insurance companies earn a yield premium on private placement investments relative to comparable public bonds?",
                 ["Because private placements are riskier credits than public bonds from the same issuer",
                  "Because private placements are backed by government guarantees, reducing risk",
                  "Because private placements are illiquid — there is no active secondary market, so investors demand extra return for the inability to sell quickly",
                  "Because private placements always have longer maturities than comparable public bonds"],
                 2,
                 "The yield premium on private placements is specifically an illiquidity premium — compensation for accepting an investment with no ready secondary market. If the insurer needs to sell before maturity, it must find another institutional buyer willing to negotiate, which is slow, expensive, and may require significant price concessions. This illiquidity risk justifies the 50-150 bps yield premium above comparable liquid public bonds."),
            _mcq("In direct real estate investment, what does the capitalization rate (cap rate) measure?",
                 ["The percentage of tenants who have renewed their leases",
                  "Net operating income divided by property value — the yield equivalent for real estate",
                  "The percentage of rental income paid as property management fees",
                  "The proportion of the purchase price financed by debt"],
                 1,
                 "Cap rate = Net Operating Income (NOI) / Property Value. It is the direct real estate equivalent of bond yield. A property with 5M NOI and 100M value has a 5% cap rate. Lower cap rates mean more expensive properties; higher cap rates mean cheaper or riskier ones. Cap rate is the standard metric for comparing properties and assessing whether a direct real estate investment is attractively priced."),
            _scenario(
                "Hartford Life Insurance is evaluating two options for deploying $100M in its general account. Option 1: Buy $100M of XYZ Corp 5.5% public bonds (30-year maturity), rated A, available on Bloomberg immediately, bid/ask spread 15 bps. Option 2: Private placement with XYZ Corp — same 30-year maturity, same A credit rating, 6.1% coupon (60 bps premium), with maintenance covenants (debt/EBITDA < 3.5x), structured with Hartford's preferred amortization schedule, 6-week due diligence process required, no secondary market.",
                "Which option is MORE suitable for Hartford Life's general account, and why?",
                [("Option 1 — public bonds are always preferable because of daily liquidity and transparent pricing", False,
                  "Liquidity has value, but Hartford's 30-year life insurance liabilities make liquidity less critical — Hartford is unlikely to need to sell a 30-year bond in the short run. For a long-horizon insurer, sacrificing some liquidity for 60 bps yield premium and stronger covenants is entirely rational."),
                 ("Option 2 — the 60 bps yield premium, stronger maintenance covenants, and custom structure are highly valuable for a long-horizon life insurer that does not need short-term liquidity", True,
                  "Correct. Hartford's 30-year liabilities create a long horizon where illiquidity is not a material constraint. The 60 bps premium = $600,000 per year on $100M — over 30 years, this is a substantial return advantage. Stronger covenants (debt/EBITDA < 3.5x vs. public bond standard of no maintenance covenants) improve credit protection. Custom amortization fits ALM needs. Private placement is clearly superior for a long-horizon insurer."),
                 ("Neither option is suitable — insurance companies should only invest in government bonds for safety", False,
                  "Insurance companies are among the largest investors in corporate bonds and private placements globally. Both public and private IG corporate bonds are core insurance company investments. Government bonds alone cannot generate the spread income needed to meet credited rates on insurance products.")]
            ),
        ]
    )

    m2["concepts"] = [c3, c4]
    ch["modules"] = [m1, m2]
    return ch


def _build_ch9(course_id):
    ch_id = _id()
    ch = {
        "id": ch_id, "course_id": course_id, "order": 9,
        "title": "Monitoring and Evaluating Portfolio Performance",
        "description": "How institutional investors monitor portfolios for style drift, rebalancing needs, and ALM compliance, measure performance using GIPS-compliant return metrics, assess risk-adjusted returns, and conduct performance attribution and internal/external reviews.",
    }

    # ── Module 1: Portfolio Monitoring and Compliance ─────────────────────────
    m1_id = _id()
    m1 = {"id": m1_id, "chapter_id": ch_id, "order": 1,
          "title": "Portfolio Monitoring and Compliance"}

    # Concept 1: Style Drift, Rebalancing, and ALM Monitoring
    c1 = _concept(
        m1_id, 1,
        "Style Drift, Rebalancing, and ALM Compliance Monitoring",
        "Describe how portfolio managers detect and correct style drift, execute disciplined portfolio rebalancing, and monitor ongoing compliance with ALM constraints and the investment policy statement.",
        "A portfolio left unmonitored drifts away from its strategic design. Style drift occurs when a manager deviates from the stated investment mandate — a value fund that starts buying growth stocks, or a short-duration segment that accumulates long-dated bonds. Rebalancing restores portfolio weights to strategic targets after market movements cause drift. ALM monitoring ensures the asset portfolio continues to match the liability profile — duration, cash flow timing, and currency. All three monitoring activities are ongoing obligations, not annual events. Failures in monitoring are how portfolios end up with unexpected risk concentrations that only become visible during market stress.",
        "Teachers Insurance and Annuity Association (TIAA) runs continuous monitoring across three dimensions. Style drift: every fund manager's actual portfolio holdings are compared monthly to the approved style box (Morningstar) — any fund crossing two style box cells triggers a review within 5 business days. Rebalancing: TIAA uses tolerance band rebalancing — if any asset class moves more than 2% from target weight, an automatic rebalancing trade is triggered within 3 trading days. In 2022, as equity markets fell 20%, fixed income weights automatically increased to above-target; TIAA rebalanced by buying more equities (buying low) — which added approximately 80 bps of performance when markets recovered in 2023. ALM monitoring: quarterly ALM reports compare the duration and convexity of assets vs. liabilities for each product segment; any mismatch exceeding 0.25 years triggers corrective action.",
        [
            "Style drift: deviation from stated investment mandate; detected by comparing actual holdings to approved style box/benchmark characteristics.",
            "Rebalancing: restoring portfolio to strategic target weights; triggered either on a calendar basis or when weights drift beyond tolerance bands.",
            "Tolerance band rebalancing: more efficient than calendar rebalancing — only trades when drift is meaningful (e.g., ±2% from target).",
            "ALM monitoring: quarterly comparison of asset vs. liability duration, convexity, and cash flow profiles for each product segment.",
        ],
        [
            "Thinking rebalancing always means selling winners and buying losers — rebalancing is about maintaining strategy, not making return predictions.",
            "Confusing style drift with tactical allocation — drift is unintended deviation; tactical allocation is deliberate, documented, and approved.",
            "Treating ALM monitoring as an annual event — liability profiles and market conditions change continuously; quarterly monitoring is the minimum.",
        ],
        lessons=[
            _intro("Keeping the Portfolio On Track: Monitoring as an Ongoing Obligation",
                   "Investment decisions don't end at purchase. A portfolio left unmonitored drifts — from its strategy, from its risk target, from its liability match. Monitoring is the discipline that keeps the portfolio doing what it was designed to do."),
            _teach("Detecting and Correcting Style Drift",
                   "Style drift occurs when an investment manager's actual portfolio deviates materially from the stated mandate. A 'US Large-Cap Value' manager who starts buying mid-cap growth stocks is style drifting — the investor allocated to value but is getting growth exposure. Detection methods: (1) Returns-based style analysis — statistical regression of fund returns against style indices (value, growth, size) over 36 months reveals actual style exposures; (2) Holdings-based analysis — examine the fund's actual portfolio holdings and compare to the approved style box (Morningstar grid); (3) Active share analysis — measure what percentage of the fund's holdings differ from the benchmark; high active share in the wrong direction signals drift. Correction: if drift is confirmed, the manager must either return to mandate or be replaced/reallocated. Style drift disrupts asset allocation design — if the investor intended value exposure and the manager drifted to growth, the total portfolio may have unintended concentration in growth despite the allocation structure.",
                   ["Returns-based style analysis: regress fund returns against value/growth/size indices to infer actual exposures.",
                    "Holdings-based analysis: directly examine what the manager owns and compare to style box.",
                    "Style drift alert triggers: fund moving more than one cell in Morningstar 9-box style grid.",
                    "Consequence of undetected drift: total portfolio may have unintended factor tilts despite correct allocation labels."]),
            _teach("Portfolio Rebalancing and ALM Compliance Monitoring",
                   "Rebalancing restores portfolio weights to strategic targets when market movements cause drift. Two rebalancing approaches: (1) Calendar rebalancing — rebalance on fixed schedule (monthly, quarterly, annually) regardless of drift magnitude; simple but may trade unnecessarily; (2) Tolerance band rebalancing — rebalance only when a weight drifts beyond a predefined threshold (e.g., ±2% from target); more efficient, only trades when drift is meaningful. Rebalancing has a contrarian benefit: selling assets that have outperformed (now overweight) and buying assets that have underperformed (now underweight) systematically implements 'buy low, sell high' discipline. ALM compliance monitoring tracks whether the asset portfolio continues to match the liability profile: (1) Duration monitoring — compare asset duration vs. liability duration quarterly; mismatch beyond tolerance triggers action; (2) Cash flow matching — ensure asset cash flows (coupons, maturities) cover projected liability cash flows; (3) Convexity monitoring — asset convexity should approximate liability convexity to avoid second-order duration mismatches.",
                   ["Calendar rebalancing: simple but trades may be unnecessary if drift is small.",
                    "Tolerance band: efficient — trades only when drift exceeds threshold (e.g., ±2%).",
                    "Rebalancing benefit: systematic 'buy low, sell high' — contrarian discipline.",
                    "ALM monitoring frequency: quarterly minimum; monthly for segments with high liability variability."]),
            _example("TIAA's Tolerance Band Rebalancing in 2022",
                     "TIAA's equity target weight was 15% of the general account; tolerance band ±2% (range: 13-17%). In January 2022: equities at 15.8% — within band, no action. By June 2022: equities had fallen to 12.7% (below the 13% floor) due to the S&P 500's 20% decline. Trigger: automatic rebalancing — TIAA purchased $2.1 billion in equities over 3 days to restore the 15% target. The purchase cost was roughly 20% below January prices. By December 2023, equities had recovered; TIAA's positions were up ~35% from the rebalancing purchase price. The systematic rebalancing added approximately 80 bps to total portfolio return — not from market timing judgment, but from disciplined process. Contrast: investors who held underweight equities 'waiting for the bottom' missed the recovery.",
                     "Tolerance band rebalancing automates contrarian discipline — it forces buying after sell-offs and selling after run-ups, without relying on market timing judgment."),
            _flash("What is the difference between style drift and tactical asset allocation?",
                   "Style drift is unintended — a manager deviates from their mandate without authorization (a value manager buying growth stocks without disclosure). Tactical asset allocation is intentional — a deliberate, documented, committee-approved deviation from strategic weights based on a valuation signal, with predefined exit rules. Drift violates governance; TAA exercises it."),
            _mcq("A portfolio manager discovers that a fund hired as 'US Large-Cap Growth' now holds 40% mid-cap stocks and has a P/E ratio consistent with the Value style box. This is BEST described as:",
                 ["Successful tactical asset allocation by the fund manager",
                  "Style drift — the manager has deviated from the mandated investment style",
                  "Appropriate diversification within the growth mandate",
                  "A regulatory violation requiring immediate SEC notification"],
                 1,
                 "Style drift is the unintended or undisclosed deviation from the stated investment mandate. Moving from large-cap growth to mid-cap value is a significant style drift — the investor expected large-cap growth exposure and is receiving something entirely different. This disrupts the investor's asset allocation design and must be investigated and corrected, either by the manager returning to mandate or through replacement."),
            _mcq("Which rebalancing approach trades ONLY when portfolio weights drift beyond a predefined threshold?",
                 ["Calendar rebalancing — trades on a fixed quarterly schedule",
                  "Momentum rebalancing — adds to winning positions when they outperform",
                  "Tolerance band rebalancing — trades when weights exceed an approved range",
                  "Tax-loss rebalancing — trades only when losses can offset gains"],
                 2,
                 "Tolerance band rebalancing triggers trades only when a weight drifts beyond a predefined threshold (e.g., ±2% from target). This is more efficient than calendar rebalancing because it avoids unnecessary trades when weights are close to target. Calendar rebalancing trades on schedule regardless of drift magnitude — potentially rebalancing when no meaningful drift has occurred."),
            _mcq("During an equity market rally, an insurer's equity allocation rises from the 10% target to 14%. The IPS allows a maximum of 12%. What action is REQUIRED?",
                 ["Monitor for another quarter before taking action — one period of drift is acceptable",
                  "Rebalance by selling equities to restore the allocation to the 10% strategic target (or within the approved band)",
                  "Update the IPS to increase the equity limit to 15% to accommodate the current allocation",
                  "Convert the excess equity allocation to equity derivatives instead of selling"],
                 1,
                 "When a position drifts above the IPS maximum (14% vs. 12% allowed), the manager must rebalance — this is a compliance requirement, not a discretionary choice. Waiting, changing the IPS to fit the drift, or substituting derivatives would all violate fiduciary and governance obligations. The portfolio must be brought back within approved limits promptly."),
            _mcq("An ALM monitoring report shows the life insurance segment's asset duration is 10.2 years vs. the liability duration of 12.5 years. What risk does this mismatch create?",
                 ["If interest rates rise, both assets and liabilities will increase in value equally",
                  "If interest rates fall, assets will appreciate less than liabilities, creating a surplus deficit",
                  "The mismatch creates no risk since both assets and liabilities are denominated in the same currency",
                  "The mismatch only matters if the insurer plans to sell the portfolio within 12 months"],
                 1,
                 "Assets with duration 10.2 years are LESS sensitive to rate changes than liabilities with duration 12.5 years. If rates fall: liabilities increase in value by more than assets (liabilities have more duration sensitivity) — creating a net loss in surplus. The 2.3-year duration shortfall means for every 1% rate decline, liabilities grow approximately 2.3% more than assets. Corrective action: extend asset duration by purchasing longer bonds or using receive-fixed swaps."),
            _mcq("Returns-based style analysis is MOST useful for:",
                 ["Calculating a fund manager's total return net of fees",
                  "Inferring a fund's actual style exposures by regressing its returns against style index returns",
                  "Determining the appropriate benchmark for a newly established fund",
                  "Measuring the fund's compliance with regulatory capital requirements"],
                 1,
                 "Returns-based style analysis (developed by William Sharpe) regresses a fund's historical returns against returns of style indices (value, growth, small-cap, etc.) over 36 months. The regression coefficients reveal the fund's actual style exposures — regardless of what the manager claims. It is the primary early-warning tool for style drift detection because it requires only return data, not individual holdings."),
            _scenario(
                "Transamerica's equity manager (mandate: US Large-Cap Blend, 10% portfolio target) has drifted to 13% allocation due to equity market appreciation, and returns-based style analysis shows the fund now has 60% growth factor exposure vs. the approved 40% growth / 60% blend. The compliance team flags both issues. The investment committee debates: Response A — send a letter to the manager asking them to 'gradually drift back' over 12 months while holding at 13%. Response B — immediately rebalance to 10% target weight AND place the manager on formal 30-day review requiring holdings justification; if style cannot be corrected, trigger manager replacement.",
                "Which response reflects proper portfolio monitoring governance?",
                [("Response A — gradual correction is more market-sensitive and avoids unnecessary transaction costs", False,
                  "Response A fails on both dimensions: the weight drift above IPS limits requires prompt rebalancing (not 12-month tolerance), and a 'letter to drift back' is not a formal governance response to a confirmed style drift violation. Gradual correction delays fiduciary compliance."),
                 ("Response B — immediate weight rebalancing plus formal style drift review reflects the dual obligation: IPS compliance and manager oversight", True,
                  "Correct. Two separate issues require two separate responses: (1) the 13% weight above the 10% target (with IPS maximum) must be rebalanced immediately; (2) the confirmed style drift to 60% growth requires formal investigation. If the manager cannot return to mandate, replacement protects the portfolio's design integrity."),
                 ("Neither response — the committee should increase the equity target to 13% since the drift was caused by market appreciation, not manager error", False,
                  "Changing the IPS to fit current drift is a governance failure. The IPS exists to enforce discipline. If 13% equity is truly more appropriate, that's a strategic asset allocation decision requiring full SAA review — not a reactive IPS change to accommodate existing drift.")]
            ),
        ]
    )

    # Concept 2: GIPS Standards and Compliance Monitoring
    c2 = _concept(
        m1_id, 2,
        "GIPS Standards and Investment Compliance Monitoring",
        "Explain the Global Investment Performance Standards (GIPS) and describe how investment compliance monitoring programs ensure adherence to the investment policy statement, regulatory requirements, and ethical standards.",
        "GIPS (Global Investment Performance Standards) are a set of ethical standards for investment performance calculation and presentation, maintained by CFA Institute. Compliance with GIPS allows investment managers to present performance results consistently and transparently to clients globally, preventing selective presentation of only favorable results. Investment compliance monitoring is the ongoing process of verifying that every portfolio action conforms to the IPS, regulatory requirements, and internal policies. Together, GIPS compliance and robust compliance monitoring programs protect clients from misrepresentation and ensure investment operations remain within authorized boundaries.",
        "Fidelity Institutional's insurance portfolio management division achieved GIPS compliance in 2005 and maintains it through annual verification by an independent verifier (PricewaterhouseCoopers). Their compliance structure: (1) Composite construction — all insurance client portfolios with similar mandates are grouped into composites (e.g., 'Core Fixed Income Insurance Composite'); (2) Performance calculation — all returns are time-weighted to eliminate the effect of client cash flows; (3) Disclosure requirements — all composites disclose asset-weighted average returns, composite dispersion, composite size, and number of portfolios; (4) Internal compliance monitoring: automated pre-trade and post-trade checks against IPS limits run on every portfolio simultaneously; weekly compliance officer reviews; quarterly board reporting; annual GIPS verification. Their internal compliance monitoring flagged 47 potential violations in 2023 — 41 were resolved pre-trade (prevented), 6 post-trade (corrected within 3 days).",
        [
            "GIPS: global ethical standards for investment performance presentation — prevents cherry-picking only good results.",
            "Composite: group of portfolios with similar mandates — performance reported at the composite level, not cherry-picked individual accounts.",
            "Time-weighted return (TWR): eliminates distortion from external cash flows; required by GIPS for performance presentation.",
            "Pre-trade compliance: automated check before trade execution; post-trade compliance: end-of-day sweep for IPS breaches.",
        ],
        [
            "Thinking GIPS compliance means the manager performed well — GIPS only verifies consistent calculation and presentation methods, not returns quality.",
            "Confusing GIPS verification with GIPS compliance — the manager claims compliance; verification by an independent firm confirms the claim.",
            "Believing compliance monitoring is only for regulatory requirements — it also covers IPS limits, internal policies, and ethical standards.",
        ],
        lessons=[
            _intro("Performance Presentation Standards and Compliance Programs",
                   "Performance numbers can be manipulated — showing only winning accounts, only favorable periods, or calculating returns in ways that flatter results. GIPS exists to prevent this. And behind every compliant portfolio is a monitoring program ensuring every trade conforms to the rules."),
            _teach("GIPS: Global Investment Performance Standards",
                   "GIPS are voluntary ethical standards created by CFA Institute that define how investment managers must calculate, present, and disclose investment performance. Key GIPS requirements: (1) All actual, fee-paying discretionary portfolios must be included in at least one composite — managers cannot cherry-pick only their best-performing accounts; (2) Performance must use time-weighted returns (TWR) to eliminate the distortion from client cash flows; (3) Composites must include a minimum 5-year track record (or since inception if shorter) building to 10 years; (4) Asset-weighted composite returns must be disclosed, along with composite dispersion, number of portfolios, and total assets; (5) Prospective performance (projections) cannot be shown alongside GIPS-compliant historical performance. GIPS benefits: global comparability, prevention of cherry-picking, transparent disclosure. GIPS verification: independent firms (Big 4 accounting firms) review the manager's claim of compliance annually — verification is strongly encouraged but not required for compliance.",
                   ["Composite: all portfolios with substantially similar mandate — no cherry-picking individual accounts.",
                    "TWR removes cash flow timing effect: eliminates the manager's performance being distorted by when clients add/withdraw money.",
                    "5-year minimum track record building to 10 years of GIPS-compliant history.",
                    "Verification: annual independent review of compliance claim — recommended but voluntary."]),
            _teach("Investment Compliance Monitoring Programs",
                   "A compliance monitoring program ensures all portfolio activities conform to the IPS, regulatory requirements, and internal policies. Components: (1) Pre-trade compliance — automated system checks every proposed trade before execution against: IPS concentration limits, credit quality minimums, prohibited securities lists, sector maximums, and single-issuer caps. Trades that would violate any limit are automatically blocked; (2) Post-trade compliance — end-of-day sweep of all portfolios checks for any drift beyond IPS limits (due to market price movements, not trades) and flags for corrective action; (3) Periodic compliance reports — weekly/monthly reports to compliance officer summarizing any exceptions, resolutions, and open items; (4) Annual compliance review — comprehensive review of the entire IPS against current portfolio, regulatory changes, and operational controls; (5) Board/committee reporting — quarterly summary of compliance status, violations, and corrective actions for board oversight. Compliance function must be independent of portfolio management — portfolio managers should not self-monitor.",
                   ["Pre-trade: blocks violations before they happen — most effective control.",
                    "Post-trade: catches drift from market price movements (not trade errors).",
                    "Independence: compliance officer reports to CRO or board, not to portfolio management.",
                    "Exception log: all violations documented with root cause and resolution for audit trail."]),
            _example("Fidelity's Compliance Monitoring in Practice",
                     "In March 2023, Fidelity's pre-trade compliance system blocked a portfolio manager from buying $15M of Rite Aid Corporation bonds. The manager's thesis: Rite Aid bonds were undervalued at 65 cents on the dollar with a 14% yield. The block reason: Rite Aid was classified as CCC-rated (below BBB- minimum in the IPS), AND the position would have created a 2.8% single-issuer concentration (above the 2.5% IPS maximum). Three months later, Rite Aid filed for bankruptcy and the bonds fell to 22 cents. The pre-trade block prevented an estimated $5.4M loss. The portfolio manager formally challenged the IPS limit with the investment committee — the committee maintained the BBB- minimum, concluding that the yield compensation for CCC risk was inconsistent with the portfolio's solvency mandate.",
                     "Compliance controls sometimes block trades that would have been profitable — but they also block trades that would have caused serious loss. The value of consistent enforcement is in the aggregate protection over thousands of trades, not the outcome of any single blocked trade."),
            _flash("What is a 'composite' in GIPS performance standards?",
                   "A composite is a grouping of all actual, fee-paying, discretionary portfolios managed according to a substantially similar investment mandate. GIPS requires that all qualifying portfolios be included in at least one composite — preventing managers from reporting only their best-performing accounts. Composite returns are asset-weighted averages of all member portfolio returns."),
            _mcq("Why does GIPS require time-weighted returns (TWR) rather than money-weighted returns (MWR) for performance reporting?",
                 ["Time-weighted returns are always higher than money-weighted returns",
                  "Time-weighted returns eliminate the distortion caused by external cash flows the manager does not control, enabling fair comparison across managers",
                  "Time-weighted returns are simpler to calculate than money-weighted returns",
                  "Regulators require time-weighted returns for all investment disclosures"],
                 1,
                 "Portfolio managers do not control when clients deposit or withdraw funds. If a client withdraws money before a strong market rally, the money-weighted return suffers — even though the manager performed well. TWR chains sub-period returns together, eliminating the cash flow timing effect. This allows fair apples-to-apples comparison of manager skill across portfolios with different client cash flow patterns."),
            _mcq("An investment manager presents performance only for its 5 best-performing portfolios while excluding 20 underperforming portfolios from disclosure. This MOST directly violates which GIPS requirement?",
                 ["The requirement to calculate returns using the time-weighted method",
                  "The requirement to include all actual, fee-paying, discretionary portfolios in at least one composite",
                  "The requirement to maintain 5-year track records for all composites",
                  "The requirement to disclose the number of portfolios in each composite"],
                 1,
                 "GIPS' most fundamental requirement is that ALL actual, fee-paying, discretionary portfolios must be included in at least one composite. Excluding underperforming portfolios while presenting only winners is precisely the cherry-picking behavior GIPS was designed to prevent. This is a material GIPS violation that renders the performance presentation misleading."),
            _mcq("Which compliance monitoring control is MOST effective at preventing investment policy violations?",
                 ["Post-trade compliance sweep conducted at end of day",
                  "Monthly compliance officer review of exception reports",
                  "Pre-trade compliance system that blocks violations before trade execution",
                  "Annual board review of the investment policy statement"],
                 2,
                 "Pre-trade compliance is the most effective control because it prevents violations from occurring — the trade is blocked before it reaches the market. Post-trade sweeps, monthly reviews, and annual audits are important secondary controls, but they catch violations after the fact, requiring corrective trades that incur transaction costs and potential losses."),
            _mcq("GIPS verification by an independent firm:",
                 ["Is required for all investment managers claiming GIPS compliance",
                  "Guarantees that all reported returns are accurate and that the manager outperformed its benchmark",
                  "Is strongly recommended and provides additional credibility to the compliance claim, but is not required",
                  "Replaces the need for internal compliance monitoring programs"],
                 2,
                 "GIPS verification is voluntary — managers can claim GIPS compliance without independent verification. However, verification by a qualified independent firm (typically Big 4 accounting firms) provides strong evidence that the compliance claim is credible, and most institutional clients require it. Verification confirms the firm's processes and procedures comply with GIPS requirements — it does not audit individual composite returns or guarantee performance accuracy."),
            _mcq("A portfolio manager's pre-trade compliance system flags a proposed bond purchase as violating the IPS single-issuer concentration limit. The manager believes the trade is attractive. The MOST appropriate action is:",
                 ["Execute the trade anyway since the manager's investment judgment supersedes the compliance system",
                  "Reduce the order size to remain within the IPS limit, or formally request an IPS waiver through the approved governance process",
                  "Ask the compliance team to temporarily disable the limit for this specific trade",
                  "Reclassify the issuer under a different category to avoid triggering the concentration limit"],
                 1,
                 "The IPS concentration limit exists to protect the portfolio from excessive single-issuer risk. If the manager believes the limit is inappropriate, the correct path is formal IPS review — not circumvention. Reducing order size to stay within limits is the immediate solution; requesting a formal IPS amendment through governance is the appropriate process for changing the limit. Self-help workarounds (disabling limits, reclassifying issuers) violate compliance independence and fiduciary duty."),
            _scenario(
                "Nationwide's investment performance team is preparing a GIPS-compliant presentation for prospective insurance clients. They have 28 separate insurance portfolios managed to the same core fixed income mandate. 22 of these portfolios have outperformed the Bloomberg Aggregate benchmark; 6 have underperformed. The marketing team proposes: 'Present only the 22 outperforming portfolios — the 6 underperformers had unusual client restrictions that are not representative.' The compliance team objects.",
                "Who is correct, and what must the performance presentation include?",
                [("The marketing team — excluding non-representative portfolios is a standard GIPS accommodation for unusual mandates", False,
                  "GIPS does allow exclusion of portfolios with significant client-imposed restrictions that make them non-comparable, but this requires clear documentation and disclosure. It cannot be used simply to exclude underperformers. 'Not representative' due to performance outcomes is NOT a GIPS-valid exclusion criterion."),
                 ("The compliance team — GIPS requires including all 28 portfolios in the composite; the composite return is the asset-weighted average of all 28, with dispersion and number of portfolios disclosed", True,
                  "Correct. GIPS requires ALL actual, fee-paying, discretionary portfolios with substantially similar mandates to be included. If the 6 underperforming portfolios genuinely had material client-imposed restrictions making them non-comparable, each must be individually documented and formally excluded with clear disclosure. Excluding them simply because they underperformed violates the anti-cherry-picking core of GIPS."),
                 ("Both teams are partially right — a 50/50 split between outperforming and underperforming portfolios is the GIPS required disclosure", False,
                  "GIPS has no such provision. The composite must include all qualifying portfolios with asset-weighted performance. The dispersion measure (range or standard deviation of portfolio returns within the composite) will reveal the spread between best and worst performing portfolios — that is the GIPS-compliant way to acknowledge performance differences within a composite.")]
            ),
        ]
    )

    m1["concepts"] = [c1, c2]

    # ── Module 2: Performance Measurement and Review ──────────────────────────
    m2_id = _id()
    m2 = {"id": m2_id, "chapter_id": ch_id, "order": 2,
          "title": "Performance Measurement and Review"}

    # Concept 3: Return Metrics and Risk-Adjusted Performance Measurement
    c3 = _concept(
        m2_id, 1,
        "Return Metrics and Risk-Adjusted Performance Measurement",
        "Explain how to calculate and interpret time-weighted return (TWR) and money-weighted return (MWR), and describe the key risk-adjusted performance measures — Sharpe ratio, Treynor ratio, Jensen's alpha, and information ratio.",
        "Raw returns alone tell an incomplete story. A portfolio earning 12% while taking enormous risk may be inferior to one earning 9% with disciplined risk management. Risk-adjusted performance measures standardize returns relative to the risk taken, enabling fair comparison across managers with different risk levels. The four primary measures — Sharpe ratio (total risk), Treynor ratio (systematic risk only), Jensen's alpha (alpha vs. CAPM expected return), and information ratio (active return per unit of active risk) — each answer a different question about performance quality. Insurance companies use these metrics to evaluate external managers, compare internal strategies, and determine whether active management fees are justified.",
        "Pacific Life uses a four-metric scorecard for every external manager evaluation: (1) 5-year time-weighted return vs. benchmark; (2) Sharpe ratio vs. category peers (top quartile required); (3) Information ratio over 3 and 5 years (minimum 0.4 required to justify active management fee); (4) Jensen's alpha with statistical significance test (alpha must be positive and statistically significant at 90% confidence). In their 2023 manager review, 15 of 20 external managers passed all four metrics. Of the 5 that failed: 3 failed on information ratio (active bets not paying off), 1 failed on Sharpe ratio (too much total risk), 1 failed on Jensen's alpha (market beta exposure explained all returns). All 5 received formal performance improvement notices with 12-month review periods. 2 were subsequently terminated.",
        [
            "TWR: chain-links sub-period returns to eliminate cash flow timing effects; used for manager comparison (GIPS standard).",
            "MWR (IRR): weights returns by timing and size of cash flows; better measures investor experience.",
            "Sharpe ratio: (portfolio return - risk-free rate) / standard deviation — reward per unit of TOTAL risk.",
            "Information ratio: (portfolio return - benchmark return) / tracking error — active return per unit of active risk.",
        ],
        [
            "Thinking a higher Sharpe ratio always means a better manager — the Sharpe ratio uses total risk (standard deviation); Treynor uses only systematic risk. For a well-diversified institutional portfolio, Treynor is often more appropriate.",
            "Confusing Jensen's alpha with raw outperformance — alpha measures CAPM-adjusted outperformance after accounting for the amount of market risk taken.",
            "Ignoring statistical significance of alpha — a small positive alpha over 3 years may be random luck, not skill.",
        ],
        lessons=[
            _intro("Measuring Performance: Beyond Raw Returns",
                   "A portfolio that earned 12% last year — was that good or bad? It depends entirely on how much risk was taken and what the benchmark returned. Risk-adjusted performance measures answer the real question: did the manager earn returns commensurate with the risks taken?"),
            _teach("Time-Weighted vs. Money-Weighted Returns",
                   "Time-weighted return (TWR) measures the compound growth rate of $1 invested in the portfolio, eliminating the effect of external cash flows. It chains together sub-period returns: if a portfolio earns +5% in Q1 and -3% in Q2, TWR = (1.05)(0.97) - 1 = 1.9%. TWR is the GIPS standard because it allows fair manager comparison — a manager is not penalized for poor investor timing (clients adding money before a loss). Money-weighted return (MWR) is the internal rate of return (IRR) — it weights returns by the timing and size of cash flows. If a client invested more money before a period of poor performance, the MWR will be lower than the TWR. MWR better measures the investor's actual experience. When to use each: TWR for evaluating MANAGER skill (GIPS requirement); MWR for measuring the INVESTOR's actual return experience (accounts for when the investor added/withdrew funds).",
                   ["TWR formula: chain-multiply each sub-period (1 + return) and subtract 1.",
                    "MWR = IRR: discount rate that makes NPV of all cash flows = 0.",
                    "TWR > MWR: investor added money before poor periods (bad timing).",
                    "TWR < MWR: investor added money before good periods (lucky timing)."]),
            _teach("Risk-Adjusted Performance Measures",
                   "Four key risk-adjusted measures: (1) Sharpe ratio = (Rp - Rf) / σp — excess return per unit of total risk (standard deviation). Higher is better. Use when the portfolio represents the investor's entire risky investment; (2) Treynor ratio = (Rp - Rf) / βp — excess return per unit of SYSTEMATIC risk (beta). Higher is better. Use for well-diversified portfolios where specific risk has been eliminated; (3) Jensen's alpha = Rp - [Rf + βp(Rm - Rf)] — the return above what CAPM predicts given the portfolio's beta. Positive alpha = outperformance after adjusting for market risk; (4) Information ratio (IR) = (Rp - Rb) / TE — active return (portfolio return minus benchmark return) divided by tracking error (standard deviation of active returns). The IR measures skill at generating active returns per unit of active risk. IR above 0.5 is considered skillful; above 0.75 is excellent.",
                   ["Sharpe: total risk (standard deviation) — best for standalone portfolios.",
                    "Treynor: systematic risk (beta) — best for diversified sub-portfolios.",
                    "Jensen's alpha: CAPM-adjusted outperformance — requires market return assumption.",
                    "Information ratio: active return / tracking error — primary metric for active manager evaluation."]),
            _example("Pacific Life's Manager Scorecard",
                     "Pacific Life's US IG Core Bond manager posted: 5-year TWR = 5.8% vs. benchmark 5.2% (+60 bps), Sharpe ratio = 0.72 (peer median: 0.58), Treynor ratio = 0.41 (peer median: 0.31), Jensen's alpha = +0.45% (statistically significant at 95% confidence, t-stat = 2.3), Information ratio = 0.48 (3-year) / 0.54 (5-year). Interpretation: the manager consistently earned above-benchmark returns (positive IR), did so with lower total risk than peers (higher Sharpe), earned alpha beyond CAPM expectations (positive Jensen's alpha with statistical significance), and the active return per unit of active risk (IR = 0.54) exceeds the 0.4 minimum threshold. Pacific Life renewed this manager's contract with a 10% fee reduction negotiation (given outperformance), increasing the mandate from $500M to $800M.",
                     "All four metrics must tell the same story for confident manager evaluation: raw outperformance, risk efficiency, beta-adjusted skill, and active bet quality all pointing in the same direction."),
            _flash("What does the Information Ratio measure, and what value indicates active management skill?",
                   "The Information Ratio (IR) = Active Return / Tracking Error. Active return is the portfolio's return minus the benchmark return. Tracking error is the standard deviation of active returns over time. IR measures how much active return the manager generates per unit of active risk taken. IR above 0.5 indicates consistent skill; IR above 0.75 is considered excellent. IR below 0 means the active bets are destroying value vs. the benchmark."),
            _mcq("A portfolio had these sub-period returns: Q1 = +8%, Q2 = -5%, Q3 = +6%, Q4 = -2%. What is the time-weighted return for the year?",
                 ["7% (sum of quarterly returns)",
                  "approximately 6.6% (arithmetic average of quarterly returns)",
                  "approximately 6.4% (geometric chain-linked quarterly returns)",
                  "approximately 5.5% (adjusted for estimated cash flows)"],
                 2,
                 "TWR = (1.08)(0.95)(1.06)(0.98) - 1 = (1.08 × 0.95 × 1.06 × 0.98) - 1 = 1.0659 - 1 = approximately 6.6%. The geometric chain-linking eliminates the cash flow timing effect and correctly measures compound growth. Arithmetic averaging (Q1+Q2+Q3+Q4)/4 = 7/4 = 1.75% quarterly = roughly 7% annually, which overstates the true compound return due to volatility drag."),
            _mcq("Two bond managers both earn 7% annual return. Manager A has a standard deviation of 8% and beta of 0.9. Manager B has a standard deviation of 5% and beta of 1.1. The risk-free rate is 2%. Which statement is MOST accurate?",
                 ["Manager A performed better because beta above 1 always indicates riskier, lower-quality management",
                  "Manager B performed better on Sharpe ratio (lower standard deviation with same return)",
                  "Both managers performed identically since both earned 7% return",
                  "Manager A performed better because a lower beta means more conservative investing"],
                 1,
                 "Sharpe ratio = (Return - Risk-free rate) / Standard deviation. Manager A: (7% - 2%) / 8% = 0.625. Manager B: (7% - 2%) / 5% = 1.0. Manager B has a significantly higher Sharpe ratio — generating the same return with lower total risk. Despite having higher beta (more systematic risk), Manager B's lower total volatility suggests better diversification and risk management."),
            _mcq("Jensen's alpha for a portfolio equals +1.2%. This means:",
                 ["The portfolio returned 1.2% more than the risk-free rate",
                  "The portfolio returned 1.2% more than the benchmark return",
                  "The portfolio returned 1.2% more than CAPM predicted given its level of market risk (beta)",
                  "The portfolio's information ratio was 1.2"],
                 2,
                 "Jensen's alpha = Actual return - CAPM Expected return. CAPM Expected return = Risk-free rate + beta × (Market return - Risk-free rate). Alpha of +1.2% means the manager earned 1.2% more than the CAPM model predicts for the level of systematic risk (beta) taken. This isolates manager skill from the market risk exposure — a manager with high beta will earn high returns in up markets, but only positive alpha indicates true skill above CAPM expectations."),
            _mcq("A manager's 5-year information ratio is -0.3. What does this indicate?",
                 ["The manager earned 0.3% less than the risk-free rate",
                  "The manager's active bets consistently destroyed value relative to the benchmark after adjusting for active risk",
                  "The manager had 30% of trades that underperformed",
                  "The manager's benchmark was inappropriate, causing the negative reading"],
                 1,
                 "A negative information ratio means active return (portfolio return minus benchmark return) is negative — the manager consistently underperformed the benchmark. Dividing by tracking error (always positive) yields a negative IR. A -0.3 IR over 5 years is a serious concern: this manager consistently makes active bets that destroy value vs. simply holding the benchmark, making the active management fee unjustifiable."),
            _mcq("When is the Treynor ratio MORE appropriate than the Sharpe ratio for evaluating manager performance?",
                 ["When the portfolio has very high standard deviation relative to peers",
                  "When evaluating a standalone portfolio that represents the investor's entire risky investment",
                  "When the portfolio is one well-diversified component within a larger multi-manager program, so specific risk has been eliminated",
                  "When the portfolio has a beta greater than 1.0"],
                 2,
                 "Treynor uses only systematic risk (beta) in the denominator. When a portfolio is a fully diversified component in a larger multi-manager program, the specific risk of each sub-portfolio is diversified away at the total program level. In this case, only systematic risk (beta) matters for the sub-portfolio's contribution to total program risk. The Sharpe ratio, which uses total risk (standard deviation), would penalize a manager for specific risk that is already eliminated at the program level."),
            _scenario(
                "Two equity managers each manage $500M for a pension insurer. Their 5-year performance: Manager X — annual return 11.2%, benchmark 10.0%, standard deviation 14%, beta 1.15, tracking error 3.2%. Manager Y — annual return 10.6%, benchmark 10.0%, standard deviation 11%, beta 0.95, tracking error 2.1%. Risk-free rate = 2%.",
                "Based on a complete risk-adjusted performance analysis, which manager demonstrates SUPERIOR skill?",
                [("Manager X — higher absolute return (11.2% vs. 10.6%) always indicates superior performance", False,
                  "Manager X earns more partly by taking more risk (beta 1.15, std dev 14% vs. Y's 0.95 and 11%). Higher returns from higher risk is not skill — it is compensation for risk. Risk-adjusted metrics separate skill from risk-taking."),
                 ("Manager Y — superior Sharpe ratio (8.6/11=0.78 vs. 9.2/14=0.66), superior information ratio (0.6/2.1=0.29 vs. 1.2/3.2=0.38)... actually X wins IR; overall analysis favors Y on efficiency", False,
                  "Let's recalculate: Sharpe X = (11.2-2)/14 = 0.657; Sharpe Y = (10.6-2)/11 = 0.782. IR X = (11.2-10)/3.2 = 0.375; IR Y = (10.6-10)/2.1 = 0.286. Y wins Sharpe; X wins IR. Jensen's alpha: X = 11.2 - [2 + 1.15×8] = 11.2 - 11.2 = 0%; Y = 10.6 - [2 + 0.95×8] = 10.6 - 9.6 = 1.0%. Manager Y has positive Jensen's alpha; X's alpha is zero — X's outperformance is fully explained by its higher beta. Y demonstrates true skill."),
                 ("Manager Y — superior Sharpe ratio, positive Jensen's alpha (+1.0%), and the fact that X's outperformance is fully explained by its higher market risk (beta 1.15) rather than skill", True,
                  "Correct. Manager Y's Jensen's alpha: 10.6% - [2% + 0.95×8%] = +1.0% — genuine skill above CAPM. Manager X's Jensen's alpha: 11.2% - [2% + 1.15×8%] = 0% — X's excess return is entirely explained by beta (market risk), not skill. Y also has a superior Sharpe ratio (0.78 vs. 0.66). The complete picture shows Y is the genuinely skilled manager.")]
            ),
        ]
    )

    # Concept 4: Performance Attribution and Reviews
    c4 = _concept(
        m2_id, 2,
        "Performance Attribution Analysis and Internal and External Portfolio Reviews",
        "Describe how performance attribution analysis decomposes portfolio returns into their sources, and explain the structure and purpose of internal and external portfolio reviews for institutional investment programs.",
        "Knowing THAT a portfolio outperformed is only half the answer — understanding WHY it outperformed determines whether the outperformance was skill-based and repeatable, or luck-based and temporary. Performance attribution decomposes returns into components: asset allocation effect (was the strategic mix right?), selection effect (did the manager pick better-than-benchmark securities?), and interaction effect (did overweighting better-performing sectors magnify selection gains?). Internal and external reviews provide governance oversight — internal teams verify compliance and operational quality; external consultants provide independent second opinions on strategy, manager quality, and governance gaps.",
        "Lincoln Financial conducts a comprehensive performance attribution review each quarter. Their fixed income attribution uses the Brinson-Hood-Beebower framework: Total active return = Allocation effect + Selection effect + Interaction effect. In Q3 2023: overweighting corporate bonds contributed +12 bps (allocation effect — they were right to overweight); security selection within corporate bonds contributed +18 bps (selection effect — they chose better bonds than the benchmark within that sector); underweighting government bonds contributed +8 bps (allocation). Total attribution: +38 bps vs. benchmark. External review: Lincoln engages Mercer Investment Consulting for an annual independent review. Mercer's 2023 findings: investment team is well-staffed and processes are sound, but the alternatives program (private placements, real estate) lacked a formal post-investment monitoring protocol. Lincoln implemented Mercer's recommendations within 90 days.",
        [
            "Brinson-Hood-Beebower attribution: Total active return = Allocation effect + Selection effect + Interaction effect.",
            "Allocation effect: did overweighting/underweighting sectors vs. benchmark add or subtract value?",
            "Selection effect: did the manager pick better-than-benchmark securities within each sector?",
            "External review: independent assessment of investment strategy, manager quality, processes, and governance — provides unbiased second opinion.",
        ],
        [
            "Thinking attribution analysis is only about identifying failures — attribution also explains successful decisions, helping managers understand what to repeat.",
            "Ignoring the interaction effect — it can be material, especially when sector overweights align with strong security selection in the same sectors.",
            "Treating external reviews as audit exercises — they are strategic consultations intended to find gaps and improvement opportunities, not to assign blame.",
        ],
        lessons=[
            _intro("Why Did We Outperform? Performance Attribution and Portfolio Reviews",
                   "An investment committee that only asks 'How much did we earn?' is missing the most important question: 'How did we earn it, and is it repeatable?' Attribution analysis answers this. And external reviews ensure no one is grading their own homework."),
            _teach("Performance Attribution: Decomposing Sources of Return",
                   "The Brinson-Hood-Beebower (BHB) attribution model, the industry standard, decomposes active portfolio return into three components: (1) Allocation effect — measures the value added or subtracted by overweighting or underweighting market sectors relative to the benchmark. Formula: (portfolio sector weight - benchmark sector weight) × (benchmark sector return - total benchmark return). Positive when you overweight sectors that outperformed the total benchmark; (2) Selection effect — measures the value added by choosing better-than-benchmark securities within each sector. Formula: benchmark sector weight × (portfolio sector return - benchmark sector return). Positive when your security picks outperform the sector benchmark; (3) Interaction effect — captures the combined impact of allocation and selection decisions. Positive when you overweight sectors in which you also had strong security selection. Total active return = Sum of all three effects across all sectors. Attribution reconciles to zero if the portfolio exactly matched the benchmark.",
                   ["Allocation effect: right sectors (macro call), measured vs. benchmark sector weights.",
                    "Selection effect: right securities within each sector (micro call), measured vs. benchmark security returns.",
                    "Interaction: did you overweight the sectors where your security selection was also strongest?",
                    "Attribution should reconcile: sum of all three effects = total active return vs. benchmark."]),
            _teach("Internal and External Portfolio Reviews",
                   "Internal portfolio reviews are conducted by the investment team and compliance function, typically quarterly: (1) Performance review — actual returns vs. benchmark, attribution analysis, manager scorecard; (2) Compliance review — IPS adherence, regulatory limit status, exception log; (3) Risk review — portfolio risk metrics (duration, credit quality, concentration) vs. approved ranges; (4) Operational review — reconciliation status, trade settlement quality, counterparty exposure. External portfolio reviews are conducted by independent consultants (Mercer, Aon, Cambridge Associates, Wilshire) typically annually: (1) Strategy review — is the overall investment strategy still appropriate given the liability profile and market conditions? (2) Manager review — independent assessment of each external manager's quality, process, team stability, and competitive positioning; (3) Governance review — assessment of investment committee process, IPS quality, compliance program, and operational controls; (4) Benchmarking — how does the insurer's investment program compare to peers of similar size and product mix?",
                   ["Internal reviews: operational — compliance, risk limits, attribution (quarterly).",
                    "External reviews: strategic — strategy appropriateness, manager quality, governance gaps (annual).",
                    "Consultant independence: external reviewers must have no financial relationship with external managers they evaluate.",
                    "Action items: all review findings should produce trackable action items with owners and due dates."]),
            _example("Lincoln Financial's Q3 2023 Attribution Analysis",
                     "Lincoln's core fixed income portfolio vs. Bloomberg US Aggregate benchmark in Q3 2023. Sector allocation vs. benchmark: overweight IG corporate bonds by +8% (actual 45% vs. benchmark 37%); underweight US government by -6% (actual 30% vs. benchmark 36%); underweight CMBS by -2%. IG corporate bond returns in Q3: benchmark sector +1.8%, Lincoln picks +2.4% (+60 bps security selection alpha within corporates). Government bonds returned +0.3% total, underweighting them added allocation alpha since they lagged the total benchmark (+0.5%). Attribution result: allocation effect +12 bps (right to overweight corporate bonds), selection effect +18 bps (better bond picks within corporates), interaction effect +8 bps (overweighted corporates AND had superior selection there). Total active return: +38 bps vs. benchmark. The attribution confirmed that both the macro call (overweight credit) and the micro execution (better bond selection) were additive — reinforcing confidence in the investment team's process.",
                     "Attribution analysis is most powerful when all three effects are positive — it confirms that the portfolio's outperformance came from both correct strategy and skillful implementation, not just one dimension."),
            _flash("In the Brinson-Hood-Beebower attribution model, what does the 'selection effect' measure?",
                   "The selection effect measures the value added (or lost) by choosing better (or worse) securities than the benchmark within each sector. It isolates the manager's security-picking skill: did the bonds or stocks owned within each sector outperform the equivalent sector benchmark? A positive selection effect = the manager's individual picks added value beyond simply being in the right sector."),
            _mcq("A portfolio manager overweighted the energy sector (vs. benchmark) and the energy sector subsequently outperformed the total benchmark. This contributes MOST to which attribution component?",
                 ["Selection effect — the manager chose better energy stocks than the benchmark energy index",
                  "Interaction effect — the manager's energy holding was concentrated in one sub-sector",
                  "Allocation effect — the manager's sector overweight captured above-benchmark energy returns",
                  "Style effect — the energy sector has different risk characteristics than the total benchmark"],
                 2,
                 "The allocation effect measures the value added by the sector weighting decision (overweight/underweight relative to the benchmark). Overweighting a sector that outperforms the total benchmark is a positive allocation effect — the manager's strategic sector call added value. Selection effect would apply if specific stocks within the energy sector outperformed the energy sector benchmark."),
            _mcq("A portfolio's total active return vs. benchmark was +45 bps. Attribution analysis shows: allocation effect = +30 bps, selection effect = +25 bps, interaction effect = -10 bps. What does the negative interaction effect indicate?",
                 ["The portfolio manager made no correct sector allocation decisions",
                  "The manager overweighted sectors where their security selection was below the benchmark within those sectors",
                  "The benchmark return was higher than the portfolio return in every sector",
                  "The negative interaction effect makes the attribution analysis unreliable"],
                 1,
                 "The interaction effect is negative when the manager overweighted sectors where their security selection underperformed. The manager was right about which sectors to overweight (positive allocation effect) but their security picks within those overweighted sectors lagged the sector benchmark (hence the negative interaction — being overweight in a sector where selection was poor). Despite the negative interaction, the total attribution is +45 bps, meaning the other effects dominated."),
            _mcq("Which of the following is the PRIMARY purpose of an annual external portfolio review by an independent investment consultant?",
                 ["To replace the internal compliance monitoring program with independent oversight",
                  "To provide an unbiased assessment of investment strategy, manager quality, and governance gaps that internal teams may not objectively identify",
                  "To certify GIPS compliance for the investment manager",
                  "To calculate the performance attribution analysis that the internal team is prohibited from preparing"],
                 1,
                 "External consultants provide independent second opinions that internal teams cannot objectively provide about themselves. The consultant evaluates: is the strategy still appropriate? Are managers performing? Are there governance blind spots? No financial relationship with the managers being evaluated ensures independence. GIPS verification is a separate process conducted by audit firms, not investment consultants."),
            _mcq("An external review consultant recommends replacing an external manager that has underperformed for 3 consecutive years. The internal portfolio team disagrees, citing the manager's strong long-term 10-year track record. What governance process should resolve this?",
                 ["The internal team's view takes precedence since they have daily oversight of the manager",
                  "The external consultant's view takes precedence since they are independent",
                  "The investment committee should review both perspectives with full data and make a formal decision, documented in committee minutes",
                  "The dispute should be escalated to regulators for resolution"],
                 2,
                 "Neither the internal team nor the external consultant has unilateral authority over manager decisions — that authority rests with the investment committee. The committee reviews all evidence (3-year underperformance, 10-year track record, consultant assessment, internal team perspective) and makes a documented, accountable decision. This governance process — debate → committee decision → documentation — is the proper institutional investment governance model."),
            _mcq("Which condition is MOST important for ensuring an external investment consultant's review is genuinely independent?",
                 ["The consultant must be located in a different city than the investment team",
                  "The consultant must have no financial relationship with the external managers they are evaluating",
                  "The consultant must have previously worked at the insurer being reviewed",
                  "The consultant must charge a fixed fee regardless of investment performance"],
                 1,
                 "Independence requires the absence of financial conflicts of interest. If an external consultant receives referral fees, finder fees, or revenue sharing from the managers they evaluate, their assessments are compromised. The most common independence requirement: the consulting firm must earn revenue only from the institutional client (advisory fee), not from manager relationships. Geographic location and consultant background are secondary considerations."),
            _scenario(
                "Mutual of Omaha's fixed income portfolio achieved +55 bps active return vs. the Bloomberg US Aggregate in 2023. Attribution analysis: Allocation effect = -8 bps (slightly hurt by underweighting the best-performing sectors), Selection effect = +72 bps (exceptional security picking within sectors), Interaction effect = -9 bps (selection was strong in underweighted sectors). The investment committee asks: 'Was this a good year, and should we increase this manager's allocation?'",
                "How should the committee interpret this attribution?",
                [("Yes — 55 bps outperformance is excellent and the committee should immediately double the manager's allocation", False,
                  "55 bps outperformance is good, but the attribution story is important: the outperformance came entirely from security selection (a repeatable skill), not from sector allocation (which actually detracted). The interaction effect was negative. One year is insufficient to confirm consistency — the committee should review 3-5 year attribution trends before increasing allocation."),
                 ("No — the negative allocation effect and interaction effect mean the manager was not truly skilled", False,
                  "Negative allocation and interaction effects don't negate genuine skill. The +72 bps selection effect is a strong signal of security-picking ability. What the attribution reveals is that this manager's edge is in security selection, not sector timing — the committee should ensure the mandate emphasizes selection, not tactical sector rotation."),
                 ("The committee should recognize the manager's genuine security selection skill (+72 bps), note that sector allocation detracted, and evaluate the multi-year trend before meaningfully increasing allocation", True,
                  "Correct. The attribution tells a clear story: this manager's value comes from security selection, not sector allocation. The committee should: (1) affirm the selection skill; (2) consider whether the mandate should constrain sector allocation to focus on selection; (3) review 3-5 year attribution history before a significant allocation increase — one good year on selection may not indicate consistent structural advantage.")]
            ),
        ]
    )

    m2["concepts"] = [c3, c4]
    ch["modules"] = [m1, m2]
    return ch


def _build_ch10(course_id):
    ch_id = _id()
    ch = {
        "id": ch_id, "course_id": course_id, "order": 10,
        "title": "Regulations and the Investment Function",
        "description": "The regulatory environment governing institutional investment management — including US federal and state securities laws, IOSCO international standards, EU investment regulation, and insurance-specific investment regulations including RBC requirements and NAIC guidelines.",
    }

    # ── Module 1: Securities Regulation ──────────────────────────────────────
    m1_id = _id()
    m1 = {"id": m1_id, "chapter_id": ch_id, "order": 1,
          "title": "Securities Regulation: US and International Frameworks"}

    # Concept 1: US Federal and State Securities Regulation
    c1 = _concept(
        m1_id, 1,
        "US Federal and State Securities Regulation",
        "Describe the key US federal and state laws governing securities markets and institutional investment management — including the 1933 and 1934 Acts, the Investment Advisers Act, the Investment Company Act, and state 'blue sky' laws.",
        "The US securities regulatory framework is a multilayered system designed to protect investors, ensure fair markets, and promote capital formation. Federal law forms the foundation; state law adds additional requirements. For institutional investment managers, the most operationally significant laws are the Investment Advisers Act of 1940 (governs who can manage money for others) and the Securities Exchange Act of 1934 (governs trading behavior and reporting). Understanding this framework is essential because violations — even unintentional ones — carry significant civil and criminal penalties, and compliance programs must be designed around specific legal requirements.",
        "Prudential's investment compliance team runs 14 separate regulatory compliance programs simultaneously: SEC registration under the Investment Advisers Act (Prudential Investment Management is a registered investment adviser), 1934 Act compliance (trade reporting, insider trading prevention, 13F filings for institutional holdings above $100M), ERISA compliance for pension accounts, state blue sky law compliance for securities offered to state-regulated entities, and NAIC guidelines for their insurance company accounts. In 2022, the SEC conducted a routine examination of Prudential's RIA operations — Prudential received a 'no action' letter (no violations found) after presenting their compliance documentation. This required 6 weeks of document preparation and two examination days. Maintaining regulatory preparedness is a full-time institutional function.",
        [
            "Securities Act of 1933: governs the offer and sale of securities — requires registration and disclosure (prospectus) for public offerings.",
            "Securities Exchange Act of 1934: governs secondary market trading — created the SEC; governs broker-dealers, exchanges, and insider trading.",
            "Investment Advisers Act of 1940: requires registration with SEC for advisers with $110M+ AUM; fiduciary duty to clients.",
            "Investment Company Act of 1940: regulates mutual funds and other pooled investment vehicles.",
        ],
        [
            "Thinking the 1933 Act and 1934 Act are the same — the 1933 Act governs primary market issuance; the 1934 Act governs secondary market trading.",
            "Assuming only public company rules apply to insurers — insurance companies that manage separate accounts or act as investment advisers face direct IA Act regulation.",
            "Confusing blue sky laws with federal securities law — blue sky laws are state-level; they add requirements on top of (not instead of) federal law.",
        ],
        lessons=[
            _intro("The Legal Framework for Institutional Investment Management",
                   "Investment management doesn't happen in a legal vacuum. Federal law, state law, and insurance regulation all impose obligations on how institutional investors operate, trade, disclose, and behave. Understanding the framework prevents violations that can end careers and trigger regulatory sanctions."),
            _teach("Core Federal Securities Laws: 1933 and 1934 Acts",
                   "The foundation of US securities regulation consists of two landmark laws: (1) Securities Act of 1933 (Truth in Securities Act) — governs the primary market. Companies issuing securities to the public must register with the SEC and provide a prospectus containing material information. Key exemptions: Rule 144A (resales to qualified institutional buyers), Regulation D (private placements), Regulation S (offshore transactions). Insurance companies rely on 144A and Reg D exemptions for private placement investments; (2) Securities Exchange Act of 1934 — governs secondary market trading. Created the SEC; requires broker-dealer registration; mandates periodic reporting (10-K annual, 10-Q quarterly) by public companies; prohibits insider trading (material non-public information trading); requires institutional managers with $100M+ equity to file quarterly 13F reports disclosing equity holdings; governs short-selling and market manipulation. Rule 10b-5: the primary anti-fraud provision — prohibits false statements in connection with securities purchases or sales.",
                   ["1933 Act: primary market (new issuances) — registration + prospectus required.",
                    "1934 Act: secondary market (trading) — created SEC, governs trading behavior.",
                    "13F filing: quarterly equity holdings disclosure for institutions with $100M+ in equity.",
                    "Rule 10b-5: anti-fraud rule — prohibits material misstatements in securities transactions."]),
            _teach("Investment Advisers Act, Investment Company Act, and State Blue Sky Laws",
                   "Investment Advisers Act of 1940: requires registration with the SEC for investment advisers with $110 million or more in AUM (smaller advisers register with state regulators). Key obligations: (1) Fiduciary duty — advisers must act in clients' best interests, disclose all conflicts of interest; (2) Form ADV — comprehensive disclosure document filed with SEC and provided to clients; (3) Recordkeeping — maintain records for 5 years; (4) Compliance program — written policies and procedures, annual review, designated chief compliance officer. Investment Company Act of 1940: regulates mutual funds, ETFs, and other registered investment companies. Governs organizational requirements, diversification rules, leverage limits, and independent board requirements. Insurance companies' separate accounts offering variable annuities/life products are registered under this Act. State Blue Sky Laws: each state has its own securities laws governing offers and sales of securities within the state. Preempted for federally covered securities (exchange-listed stocks, Rule 144A transactions) but still apply to many smaller private offerings.",
                   ["IA Act: $110M AUM threshold for SEC registration (vs. state for smaller advisers).",
                    "Fiduciary duty: disclose all conflicts; always act in client's best interest.",
                    "Form ADV Part 2: narrative brochure provided to all advisory clients.",
                    "Blue sky: state securities laws — additional layer on top of federal requirements."]),
            _example("SEC Registration and the Fiduciary Obligation in Practice",
                     "MetLife Investment Management (MIM) is a registered investment adviser with $600 billion in AUM. As an SEC-registered RIA, MIM has: (1) Filed Form ADV disclosing investment strategies, fees, conflicts of interest, and disciplinary history — clients receive Part 2 (brochure) before engaging; (2) Designated a Chief Compliance Officer who reports directly to the board; (3) Implemented a comprehensive compliance manual addressing: portfolio management standards, personal trading restrictions (employees cannot trade ahead of client orders), gifts and entertainment limits, and broker selection criteria; (4) Conducted annual compliance training for all investment professionals. In 2021, an MIM analyst received a tip about a pharmaceutical company's failed drug trial (material non-public information). MIM's compliance hotline was called; trading in that security was immediately halted for all MIM accounts until the information became public. This prevented potential insider trading violations that could have resulted in criminal prosecution.",
                     "Fiduciary duty is not a philosophical concept — it requires documented procedures, active compliance programs, and immediate action when information asymmetries arise."),
            _flash("What is the primary difference between the Securities Act of 1933 and the Securities Exchange Act of 1934?",
                   "The 1933 Act governs the primary market — the initial offering and sale of new securities to investors (IPOs, private placements). The 1934 Act governs the secondary market — the ongoing trading of securities after issuance. The 1933 Act requires registration and disclosure for new offerings; the 1934 Act created the SEC and governs trading conduct, broker-dealers, and ongoing reporting by public companies."),
            _mcq("Under the Investment Advisers Act of 1940, an investment manager with $150 million in assets under management is MOST LIKELY required to:",
                 ["Register with the state securities regulator in each state where clients are located",
                  "Register with the Securities and Exchange Commission as a registered investment adviser",
                  "Register as a broker-dealer under the Securities Exchange Act of 1934",
                  "Obtain a banking license from the Federal Reserve"],
                 1,
                 "The Investment Advisers Act requires registration with the SEC for advisers with $110 million or more in AUM. With $150M AUM, this manager must register with the SEC (not state regulators — those apply to advisers under $100M). The registration requires filing Form ADV, maintaining a compliance program, designating a CCO, and adhering to fiduciary duty obligations."),
            _mcq("An institutional portfolio manager receives non-public information from a company executive about an upcoming earnings miss. Trading on this information would MOST directly violate which law?",
                 ["The Investment Company Act of 1940",
                  "The Securities Act of 1933",
                  "The Securities Exchange Act of 1934, specifically Rule 10b-5 prohibiting insider trading",
                  "State blue sky laws prohibiting securities fraud"],
                 2,
                 "Insider trading — trading on material non-public information — is primarily prosecuted under the Securities Exchange Act of 1934, specifically Rule 10b-5 (the anti-fraud provision) and Section 10(b). The SEC and DOJ aggressively enforce insider trading; penalties include disgorgement of profits, civil penalties up to 3x profits, and criminal imprisonment up to 20 years."),
            _mcq("Which document must SEC-registered investment advisers provide to clients that discloses fees, investment strategies, conflicts of interest, and disciplinary history?",
                 ["Form 13F — quarterly equity holdings disclosure",
                  "Form ADV Part 2 — the adviser's brochure provided to advisory clients",
                  "Form S-1 — the registration statement for new securities offerings",
                  "Form 10-K — the annual report filed by public companies"],
                 1,
                 "Form ADV Part 2 is the SEC-mandated disclosure document that registered investment advisers must provide to clients. It is written in plain English (not legal boilerplate) and discloses: investment strategies and methods of analysis, fees and compensation, types of clients served, conflicts of interest (including financial interests in recommended products), disciplinary history, and the adviser's background. Form 13F is for equity holdings disclosure, not client disclosure."),
            _mcq("A state's 'blue sky' securities law MOST LIKELY applies to which type of transaction?",
                 ["A NYSE-listed company's stock traded on the exchange between institutional investors",
                  "A Rule 144A private placement sold to qualified institutional buyers",
                  "A small private company offering shares to local investors within that specific state",
                  "A US Treasury bond purchase by an insurance company"],
                 2,
                 "Blue sky laws govern securities offers and sales within a state. Federal preemption eliminates state blue sky requirements for most exchange-listed securities (like NYSE stocks), Rule 144A transactions, and certain private placements to institutional investors. Small, intrastate private offerings — like a regional company selling shares to local investors — remain fully subject to the state's blue sky registration and disclosure requirements."),
            _mcq("An institutional investment manager with $250M AUM fails to file its quarterly Form 13F on time. What is the MOST LIKELY regulatory consequence?",
                 ["The manager is permanently barred from managing institutional funds",
                  "The SEC may impose civil penalties and the manager must file the delinquent form with an explanation",
                  "The manager loses its investment adviser registration automatically",
                  "The manager's clients must be immediately notified and given the option to redeem"],
                 1,
                 "Failure to file Form 13F (required quarterly equity holdings disclosure for institutions with $100M+ in equity) is a civil violation. The SEC can impose civil money penalties and will require the delinquent filing. For a first-time, non-willful violation, the consequence is typically a fine and corrective filing. Criminal prosecution is reserved for intentional, willful violations of securities law. Automatic loss of registration or forced client redemption would not apply to a late filing."),
            _scenario(
                "Lincoln National manages investments through two entities: (A) Lincoln Investment Advisers, a registered RIA managing $80B in insurance company general accounts; (B) Lincoln Insurance Company itself, investing its $45B general account directly (not through the RIA subsidiary). A conflict of interest arises: Lincoln Investment Advisers recommends Lincoln-affiliated bond funds to third-party insurance clients — funds that pay Lincoln a management fee. Is there a regulatory concern, and how should it be handled?",
                "Identify the conflict and the appropriate disclosure obligation.",
                [("No concern — affiliated fund recommendations are standard practice and require no disclosure", False,
                  "Recommending affiliated products that generate fees for the adviser without disclosure is a textbook fiduciary duty violation under the Investment Advisers Act. The economic incentive (Lincoln earning both advisory fees AND fund management fees) must be disclosed so clients can evaluate whether the recommendation serves their interests or the adviser's."),
                 ("Yes — as an SEC-registered RIA, Lincoln Investment Advisers has a fiduciary obligation to disclose in Form ADV and client agreements that affiliated fund recommendations involve a financial conflict, and clients must be able to choose non-affiliated alternatives", True,
                  "Correct. The Investment Advisers Act fiduciary duty requires full disclosure of all material conflicts of interest. The affiliated fund recommendation conflict must be: (1) disclosed in Form ADV Part 2; (2) disclosed in client engagement letters; (3) managed through either informed client consent or a policy to recommend affiliated funds only when they are genuinely in the client's best interest. Clients must have the ability to choose non-affiliated options."),
                 ("The conflict is immaterial since Lincoln's affiliated funds probably have competitive performance and fees", False,
                  "Materiality of the conflict is not determined by whether the affiliated fund happens to be good. A conflict is material if a reasonable client would want to know about it when evaluating the recommendation — and a financial incentive to recommend one's own products clearly meets that standard. The investment quality of the fund is separate from the disclosure obligation.")]
            ),
        ]
    )

    # Concept 2: IOSCO, EU Regulation, and Insurance Investment Regulation
    c2 = _concept(
        m1_id, 2,
        "IOSCO, EU Investment Regulation, and Insurance-Specific Investment Requirements",
        "Describe the international regulatory standards set by IOSCO, key EU investment regulations (MiFID II, Solvency II), and the US insurance-specific investment regulatory framework including NAIC guidelines and risk-based capital requirements.",
        "Investment management is increasingly global, and institutional investors must navigate multiple regulatory regimes simultaneously. IOSCO (International Organization of Securities Commissions) sets principles that member country regulators implement domestically. The EU's regulatory framework — particularly MiFID II for investment firms and Solvency II for insurers — is among the most comprehensive in the world. US insurance companies face a parallel layer of regulation through state insurance departments and NAIC guidelines, with risk-based capital (RBC) requirements directly determining how much capital must be held against each type of investment. Understanding these frameworks helps explain why insurance companies behave differently from other institutional investors in their portfolio decisions.",
        "Zurich Insurance Group operates across 170 countries and maintains regulatory compliance with: IOSCO principles (through their registrations in 12 jurisdictions), EU Solvency II (for European entities — requires a Solvency Capital Requirement calculation for the investment portfolio based on market risk, credit risk, and concentration risk), MiFID II (for asset management subsidiaries operating in the EU — transaction reporting, best execution, client categorization), and US state insurance regulation (NAIC guidelines, RBC requirements for US subsidiaries). Zurich's group CRO oversees a regulatory compliance team of 47 people dedicated exclusively to investment regulation across jurisdictions. Their RBC management: each potential investment is run through a 'capital cost' calculation before purchase — a BBB corporate bond costs approximately 4% RBC capital; an equity position costs 30%. Investments that don't meet the risk-adjusted return hurdle after capital cost are rejected.",
        [
            "IOSCO: international body coordinating securities regulatory standards across 130+ member jurisdictions — not a direct regulator of firms.",
            "MiFID II: EU investment services regulation — transaction reporting, best execution, client categorization (retail vs. professional vs. eligible counterparty).",
            "Solvency II: EU insurance regulation — Solvency Capital Requirement (SCR) for investment portfolio market and credit risk.",
            "NAIC / RBC: US insurance investment framework — each asset class assigned a risk charge; total capital must cover weighted risk exposure.",
        ],
        [
            "Thinking IOSCO directly regulates investment firms — IOSCO sets principles that member regulators implement; individual firms comply with their home country regulator, which follows IOSCO standards.",
            "Confusing MiFID II (investment services) with Solvency II (insurance) — they are separate EU directives with different scope and requirements.",
            "Underestimating RBC's impact on portfolio decisions — RBC capital charges directly affect the return-on-equity of each investment and can make high-yield bonds or equities economically unattractive even if they offer high gross returns.",
        ],
        lessons=[
            _intro("A Global Regulatory Landscape",
                   "Insurance investment management doesn't stop at national borders — and neither do regulators. From Geneva to Brussels to Kansas City, institutional investors must navigate a patchwork of international, regional, and domestic rules that directly shape what they can buy, how much capital they must hold, and how they must report their activities."),
            _teach("IOSCO and MiFID II: International and EU Investment Regulation",
                   "IOSCO (International Organization of Securities Commissions), founded 1983, is the global body for securities market regulation with 130+ member jurisdictions. IOSCO develops: (1) Principles for securities regulation (30 core principles covering regulator powers, enforcement, markets, intermediaries, issuers); (2) Standards for derivatives markets (post-crisis); (3) Anti-money laundering frameworks. IOSCO does not directly regulate firms — it coordinates standards that member regulators implement domestically. MiFID II (Markets in Financial Instruments Directive II, effective 2018) governs investment services in the EU: (1) Client categorization — retail (most protection), professional, eligible counterparty; (2) Best execution — investment firms must execute on 'best possible terms' considering price, costs, speed, likelihood of execution; (3) Transaction reporting — all trades must be reported to regulators within one business day; (4) Research unbundling — payment for investment research must be separated from execution commissions; (5) Pre/post-trade transparency — bid/ask prices must be publicly available for liquid instruments.",
                   ["IOSCO: sets global standards; not a direct regulator of individual firms.",
                    "MiFID II: EU investment services — client classification, best execution, mandatory transaction reporting.",
                    "Research unbundling: MiFID II separated research payments from commissions — firms must pay for research explicitly.",
                    "Pre-trade transparency: market makers must publicly quote bid/ask prices for liquid EU instruments."]),
            _teach("Solvency II and US Insurance Investment Regulation (NAIC/RBC)",
                   "Solvency II (effective 2016) is the EU prudential regulatory framework for insurance companies. Its investment provisions: (1) Solvency Capital Requirement (SCR) — risk-based capital calculation covering market risk (interest rate, equity, spread, concentration, currency), counterparty risk, and liquidity risk. Investment portfolios with higher risk generate higher SCR, requiring more equity capital; (2) Prudent Person Principle — insurers must invest in assets appropriate for their liabilities, with proper diversification, and must be able to identify, measure, and manage investment risks. In the US, the NAIC (National Association of Insurance Commissioners) coordinates state insurance regulation. Key investment components: (1) Authorized investments — each state specifies which asset types are permitted for insurance company investment; (2) NAIC designations — credit quality ratings system (1=highest quality, 6=in or near default) used for capital charges; (3) Risk-Based Capital (RBC) — each asset class carries a specific risk factor (C-1 asset risk): Treasury bonds ≈0.3%, BBB corporate bonds ≈4%, equities ≈30%, below-investment-grade ≈20%. Total required capital = sum of all asset risk charges × a covariance factor.",
                   ["Solvency II SCR: higher portfolio risk = more required capital = lower return on equity.",
                    "Prudent Person Principle: EU standard — invest appropriately for liabilities, with diversification.",
                    "NAIC designation: 1 (highest quality) to 6 (default); determines RBC capital charge.",
                    "RBC C-1 risk: equities require 30% capital, IG bonds 1-4%, government bonds 0.3%."]),
            _example("How RBC Shapes Investment Decisions at Lincoln Financial",
                     "Lincoln Financial evaluates every investment through a Return on Capital (ROC) lens. Example: a BB-rated bond offers 8.5% yield. Lincoln's analysis: NAIC designation = 3 (BB), C-1 risk factor = 13%, ROE hurdle = 12%. Capital cost calculation: $100M bond requires $13M capital (13% RBC charge). Capital cost = $13M × 12% hurdle = $1.56M annual capital cost = 1.56% of bond value. Risk-adjusted return = 8.5% yield - 1.56% capital cost = 6.94%. Comparison: an A-rated bond at 5.8% yield, NAIC designation 2, C-1 = 1.3%, capital cost = $1.3M × 12% = 0.156% → risk-adjusted return = 5.8% - 0.16% = 5.64%. Decision: the BB bond wins (6.94% vs. 5.64% risk-adjusted), but only by 1.3% — barely enough premium for the additional credit risk. Lincoln accepts the BB position at 5% of their HY allocation, not as a core holding. Without the RBC lens, the 2.7% raw yield premium would have looked more compelling than the risk actually warranted.",
                     "RBC requirements transform raw yield comparisons into return-on-capital comparisons — forcing rigorous risk-adjusted discipline into every investment decision."),
            _flash("What is the 'Prudent Person Principle' under Solvency II?",
                   "The Prudent Person Principle requires EU insurance companies to invest only in assets whose risks the insurer can properly identify, measure, monitor, manage, and control. Assets must be appropriate to the nature and duration of liabilities, with proper diversification and no excessive concentration. Unlike older 'quantitative limits' approaches (which set fixed maximums for each asset class), the Prudent Person Principle relies on sound risk management processes rather than rigid numerical limits."),
            _mcq("IOSCO's primary role in the global investment regulatory landscape is BEST described as:",
                 ["Directly licensing and supervising investment managers in all member countries",
                  "Setting international securities regulatory principles and standards that member regulators implement domestically",
                  "Operating as the global enforcement arm for securities law violations across borders",
                  "Managing a global investment protection insurance fund for retail investors"],
                 1,
                 "IOSCO coordinates securities regulation globally by developing principles and standards (including market structure, intermediary conduct, and enforcement cooperation) that its 130+ member country regulators adopt and implement domestically. IOSCO does not directly regulate individual firms — national regulators (SEC in the US, FCA in the UK, BaFin in Germany) do. IOSCO facilitates cross-border cooperation for enforcement, but is not itself an enforcement body."),
            _mcq("Under US NAIC Risk-Based Capital (RBC) requirements, which investment would require the LARGEST capital charge as a percentage of market value?",
                 ["A 10-year US Treasury bond",
                  "An investment-grade corporate bond rated BBB",
                  "A common stock equity investment",
                  "A BB-rated high-yield corporate bond"],
                 2,
                 "NAIC C-1 asset risk charges: US Treasuries ≈ 0.3%, IG corporate bonds (BBB) ≈ 4%, HY bonds (BB) ≈ 13%, common equity ≈ 30%. Common stock equity carries the highest C-1 risk charge because equities have the highest price volatility and potential for loss relative to fixed income. This is why insurance companies typically allocate only 5-15% to equities vs. 60-80% to investment-grade bonds."),
            _mcq("MiFID II's 'research unbundling' requirement changed how EU investment managers pay for investment research. The PRIMARY change was:",
                 ["Investment research became free for all institutional investors under EU regulation",
                  "Investment managers must now pay for research explicitly (separate charge) rather than bundling it into execution commissions paid to brokers",
                  "Investment research can only be produced by EU-regulated entities",
                  "Investment managers must share all research with competitors to ensure market fairness"],
                 1,
                 "Pre-MiFID II, investment managers paid for research by directing execution commission business to brokers who also provided research ('soft dollars'). This bundling obscured the true cost of research and created conflicts. MiFID II requires explicit, separate payment for research — either from the manager's own P&L or through a Research Payment Account funded by client charges (with explicit disclosure). This forced pricing transparency for investment research."),
            _mcq("An EU insurance company's investment portfolio has high equity concentration. Under Solvency II, the PRIMARY consequence is:",
                 ["The company must immediately sell all equity holdings",
                  "The company's Solvency Capital Requirement (SCR) increases, requiring more equity capital to be held",
                  "The company must reclassify equity as fixed income for accounting purposes",
                  "The EU's Prudent Person Principle prohibits any equity investment"],
                 1,
                 "Solvency II's SCR calculation includes an equity risk module that charges higher capital for equity holdings. Higher equity concentration raises the SCR, requiring the insurer to hold more shareholder equity capital to maintain solvency. This directly reduces return on equity — the higher capital base earns the same profits, so ROE falls. The Prudent Person Principle doesn't prohibit equity; it requires that the risk be manageable and appropriately sized relative to the liability profile."),
            _mcq("A US insurance company is considering investing in a privately placed bond that is not included on the state's 'authorized investment' list. What is the MOST LIKELY consequence?",
                 ["The investment may proceed if the federal SEC approves it",
                  "The investment may be purchased but will receive a very high NAIC capital charge, potentially making it economically unattractive",
                  "The investment may be restricted or prohibited by the state insurance regulator, and may not count toward admitted assets",
                  "The investment automatically receives the lowest NAIC designation (6) regardless of credit quality"],
                 2,
                 "State insurance investment laws define 'authorized investments' — assets that are permitted and counted as admitted assets for solvency purposes. Non-authorized investments may be restricted or prohibited, and unauthorized assets that are purchased may be excluded from admitted assets (non-admitted), which directly increases the RBC ratio burden. SEC approval has no bearing on state insurance investment authorization — these are independent regulatory systems."),
            _scenario(
                "A US life insurance company is evaluating two portfolios for its $2 billion general account. Portfolio A: 80% US Treasury bonds, 20% BBB corporate bonds. Estimated annual return: 4.8%. Total NAIC RBC capital required: approximately $80M. Portfolio B: 50% BBB corporate bonds, 25% BB high-yield bonds, 25% common equity. Estimated annual return: 7.2%. Total NAIC RBC capital required: approximately $680M.",
                "Which portfolio is MOST appropriate for a well-capitalized life insurer with a 12% ROE target on required capital?",
                [("Portfolio B — the higher 7.2% return is always superior for an insurer with a 12% ROE target", False,
                  "Return analysis must include the capital cost. Portfolio B requires $680M capital vs. $80M for A — an additional $600M. The capital cost at 12% hurdle: $72M additional annual capital cost. Portfolio B's return advantage: 7.2% - 4.8% = $48M on $2B. Net: Portfolio B earns $48M more return but costs $72M more in capital — a net negative from a risk-adjusted perspective. Portfolio A is financially superior."),
                 ("Portfolio A — when the capital cost of the higher-risk portfolio exceeds the additional return it generates, the conservative portfolio delivers better risk-adjusted return on capital", True,
                  "Correct. Portfolio A risk-adjusted ROC = (4.8% × $2B) / $80M = 120%. Portfolio B = (7.2% × $2B) / $680M = 21.2%. Portfolio A is dramatically superior on return-on-capital, the correct metric for regulated insurers. The apparent 2.4% yield advantage of Portfolio B is completely overwhelmed by the 8.5x higher capital requirement."),
                 ("Neither portfolio — life insurers should only hold government bonds, never corporate bonds or equities", False,
                  "Corporate bonds are core investments for life insurance general accounts, and modest equity allocations are common. The issue with Portfolio B is not the asset class mix per se, but the specific allocation percentages that create a disproportionately high RBC burden relative to the return premium offered.")]
            ),
        ]
    )

    m1["concepts"] = [c1, c2]

    # ── Module 2: Insurance Investment Regulation in Practice ─────────────────
    m2_id = _id()
    m2 = {"id": m2_id, "chapter_id": ch_id, "order": 2,
          "title": "Insurance Investment Regulation in Practice"}

    # Concept 3: NAIC Framework and Admitted Assets
    c3 = _concept(
        m2_id, 1,
        "The NAIC Regulatory Framework: Admitted Assets, Valuation, and Investment Limitations",
        "Describe the NAIC's role in standardizing insurance investment regulation across US states, including admitted asset requirements, statutory accounting principles for investment valuation, and investment limitation guidelines.",
        "The National Association of Insurance Commissioners (NAIC) is the US standard-setting organization for state insurance regulation. Because insurance is regulated state-by-state, the NAIC coordinates regulatory standards to ensure consistency. For investment management, the NAIC framework determines: which assets count as admitted (can be used to meet solvency requirements), how assets are valued for statutory accounting purposes (often different from GAAP), and what limitations apply to specific investment types. These standards directly constrain investment portfolio construction and create accounting implications that differ from general corporate accounting.",
        "Northwestern Mutual's statutory financial statements use NAIC-specified valuation methods throughout: US Treasury bonds are carried at amortized cost (not market value) — so rising interest rates don't show book losses on the income statement; common stocks are carried at fair market value — so equity market moves directly affect surplus; commercial mortgage loans are carried at unpaid principal balance unless impaired; real estate (owned properties) at cost minus depreciation or fair value if impaired. The statutory accounting treatment creates very different reported surplus than GAAP would. Northwestern Mutual's NAIC Investment Limitations compliance: their state of domicile (Wisconsin) limits common stock investments to 20% of admitted assets; limits below-investment-grade bonds to 5% of admitted assets; limits real estate to 10% of admitted assets. These limits constrain their asset allocation regardless of investment merit.",
        [
            "Admitted assets: assets that can be counted toward meeting policyholder liabilities for solvency purposes. Non-admitted assets (certain receivables, goodwill, deferred tax assets) cannot be counted.",
            "Statutory accounting vs. GAAP: bonds often carried at amortized cost (not fair value) under statutory accounting — reduces reported surplus volatility.",
            "Valuation reserve requirements: insurers must hold additional reserves against potential investment losses in certain asset classes.",
            "NAIC investment guidelines: quantitative limits on each asset class (equities, below-IG bonds, real estate) as % of admitted assets.",
        ],
        [
            "Thinking NAIC is a federal regulator — it is a voluntary organization of state insurance commissioners that coordinates standards, but state insurance departments retain regulatory authority.",
            "Confusing GAAP and statutory accounting — bonds under statutory accounting are often at amortized cost; under GAAP they may be at fair value. This creates very different reported capital positions.",
            "Assuming admitted asset limits are the same in every state — NAIC provides model regulations, but states adopt their own versions with variations.",
        ],
        lessons=[
            _intro("The NAIC: Coordinating Insurance Investment Standards Across 50 States",
                   "Insurance is regulated state by state in the US, but with 50 different sets of rules, coordination is essential. The NAIC provides that coordination — setting model laws, accounting standards, and investment guidelines that states adopt, creating a largely consistent national framework."),
            _teach("Admitted Assets and Statutory Valuation",
                   "Admitted assets are assets that insurance regulators allow to be counted toward the insurer's ability to meet policyholder obligations. Only admitted assets are counted in statutory surplus and the asset-to-liability coverage ratio. Common non-admitted assets (not counted): certain premium receivables past due, furniture and equipment, intangible assets (goodwill, trademarks), deferred tax assets above limits, shares in non-insurance affiliates above limits. Statutory accounting principles (SAP) govern how insurance company investments are valued for regulatory purposes — different from GAAP: (1) Bonds — most are carried at amortized cost (purchase price ± amortization of premium/discount), not fair market value. When rates rise, statutory surplus is protected from showing mark-to-market losses; (2) Common stocks — carried at fair market value (through the securities valuation reserve); (3) Commercial mortgage loans — unpaid principal balance unless impaired; (4) Real estate — lower of cost or market value.",
                   ["Admitted vs. non-admitted: only admitted assets count for solvency calculations.",
                    "Amortized cost for bonds: insulates statutory surplus from interest rate mark-to-market swings.",
                    "Common stocks at fair value: equity market moves directly hit/help statutory surplus.",
                    "Asset Valuation Reserve (AVR): mandatory reserve against potential investment losses, reducing surplus."]),
            _teach("NAIC Investment Limitations and the AVR/IMR",
                   "States adopt NAIC model laws that impose quantitative limitations on insurance company investments. Common limitations: (1) Common stock — maximum 20% of admitted assets (protects against equity market volatility impairing solvency); (2) Below-investment-grade bonds — maximum 5% of admitted assets; (3) Real estate (owned, not mortgage loans) — maximum 10% of admitted assets; (4) Single issuer — typically 3-5% of admitted assets maximum; (5) Affiliated investments — strict limits on investments in related entities. Two key mandatory reserves: (1) Asset Valuation Reserve (AVR) — required reserve against potential credit and equity losses in the investment portfolio; reduces surplus but provides buffer against realized losses; (2) Interest Maintenance Reserve (IMR) — captures realized capital gains and losses attributable to interest rate changes, amortized into income over the life of the sold asset. IMR prevents insurers from immediately recognizing all gains from selling appreciated bonds, smoothing interest rate income.",
                   ["Common stock limit: typically 20% of admitted assets maximum.",
                    "Below-IG limit: typically 5% — protects against junk bond concentration.",
                    "AVR: required reserve against credit/equity losses — reduces current surplus.",
                    "IMR: defers recognition of interest-rate-driven realized gains/losses — smooths income."]),
            _example("Northwestern Mutual's Statutory Investment Framework",
                     "Northwestern Mutual (NWM) manages $250 billion in admitted assets under Wisconsin insurance law (which closely follows NAIC model). Their statutory investment portfolio: 58% bonds (statutory amortized cost) = $145B, 12% mortgage loans (unpaid principal) = $30B, 8% equities (fair value) = $20B, 6% real estate (cost minus depreciation) = $15B, 16% other admitted assets. Limitations check: equities at 8% (below 20% maximum), real estate at 6% (below 10% maximum), no below-IG concentration. AVR balance: $8.5B (required reserve against potential credit losses — reduces reported surplus from $35B GAAP to approximately $26.5B statutory). IMR balance: $3.2B (deferred interest-rate gains from bond sales — to be released into income over bond remaining lives). Result: NWM's statutory surplus ($26.5B) is substantially lower than GAAP equity ($35B) due to the mandatory reserves — this is intentional, providing a conservative solvency buffer.",
                     "Statutory accounting's conservatism — amortized cost for bonds, mandatory reserves — produces lower reported surplus than GAAP but provides more durable, crisis-resistant solvency calculations."),
            _flash("What is the Asset Valuation Reserve (AVR) in insurance statutory accounting?",
                   "The AVR is a mandatory reserve that insurance companies must maintain against potential future credit and equity investment losses. It is funded from after-tax earnings and reduces statutory surplus. When actual investment losses occur (bond defaults, equity declines), losses are charged against the AVR before hitting surplus — providing a buffer that protects policyholder security from routine investment losses without causing immediate solvency concern."),
            _mcq("Which of the following assets would MOST LIKELY be classified as 'non-admitted' for a US insurance company?",
                 ["A BBB-rated corporate bond maturing in 10 years",
                  "A US Treasury note held in the investment portfolio",
                  "Goodwill from the acquisition of an insurance agency",
                  "A residential mortgage-backed security rated AA"],
                 2,
                 "Goodwill (and other intangible assets) is a classic non-admitted asset under statutory accounting. Unlike GAAP, which recognizes goodwill as an asset, statutory accounting excludes it because it has no liquidation value — it cannot be converted to cash to pay policyholder claims. Bonds and liquid securities are admitted assets; the MBS would need to meet quality standards but would generally be admitted."),
            _mcq("Under statutory accounting principles, how are most bonds held in an insurance company's general account valued?",
                 ["At their current fair market value, updated daily",
                  "At amortized cost — purchase price adjusted for premium or discount amortization over the bond's life",
                  "At the lower of cost or market, whichever is less favorable",
                  "At their par value regardless of purchase price or market conditions"],
                 1,
                 "Most bonds in an insurance company's statutory portfolio are carried at amortized cost. This means the purchase price (which may differ from par value if bought at a premium or discount) is amortized over the bond's remaining life, converging to par at maturity. Amortized cost reporting insulates statutory surplus from interest rate-driven market value swings — if rates rise and bond prices fall, the statutory balance sheet doesn't show the decline, providing surplus stability."),
            _mcq("The Interest Maintenance Reserve (IMR) is PRIMARILY designed to:",
                 ["Reserve against potential credit losses from bond defaults",
                  "Smooth the recognition of realized capital gains and losses attributable to interest rate movements over time",
                  "Fund the insurer's employee pension obligations",
                  "Reserve capital against the risk that policyholders withdraw funds during a market crisis"],
                 1,
                 "The IMR captures realized capital gains and losses from selling bonds that are attributable to changes in interest rates (as opposed to credit quality changes, which go to the AVR). Instead of recognizing the full gain/loss immediately, the IMR amortizes it into income over the remaining life of the sold bond. This prevents insurers from front-loading gains by selling appreciated bonds, then facing income shortfalls later when the investment income is gone."),
            _mcq("A state insurance regulator determines that an insurer's common stock allocation equals 25% of admitted assets — above the state's 20% maximum. What is the MOST LIKELY required corrective action?",
                 ["The insurer must immediately recognize the excess equity as a statutory loss",
                  "The excess equity allocation must be reclassified as non-admitted assets, reducing statutory surplus until corrected",
                  "The insurer must purchase offsetting put options to hedge the excess equity",
                  "The insurer receives a temporary waiver if the excess was caused by market appreciation"],
                 1,
                 "When an investment exceeds a statutory limit, the excess portion typically must be treated as a non-admitted asset — it is excluded from admitted asset calculations, which directly reduces statutory surplus and may impair the solvency ratio. This creates strong economic incentive to rebalance below the limit. Unlike the IPS drift discussion earlier, statutory limits have direct capital consequences — excess investments don't just violate policy, they reduce solvency capital."),
            _mcq("The Interest Maintenance Reserve (IMR) is MOST analogous to which concept in general corporate accounting?",
                 ["A loan loss reserve for credit defaults in the bond portfolio",
                  "Deferred revenue — recognizing income over time rather than all at once when a gain is realized",
                  "Accounts receivable — amounts owed to the insurer for investment income",
                  "Goodwill — intangible value from investment portfolio acquisition"],
                 1,
                 "The IMR defers recognition of realized capital gains/losses from bond sales attributable to interest rate changes, releasing them into income over the remaining life of the sold bond. This is conceptually similar to deferred revenue — the economic event (bond sale) has occurred, but income recognition is spread over time. Just as deferred revenue prevents front-loading income from multi-period contracts, the IMR prevents front-loading investment gains from selling appreciated bonds."),

            _scenario(
                "MassMutual's investment team identifies a high-yield bond portfolio (BB-rated average) with expected return of 9.2% — significantly above their investment-grade bond portfolio's 5.4% return. The high-yield portfolio would require NAIC C-1 capital of 13% (vs. 1.3% for IG bonds). Current below-IG bond allocation: 3.5% of admitted assets. Proposed increase: to 7.5% of admitted assets. Massachusetts insurance law limits below-IG bonds to 5% of admitted assets.",
                "Should MassMutual pursue this investment, and what are the binding constraints?",
                [("Yes — the 3.8% higher return clearly justifies moving to 7.5% below-IG regardless of regulation", False,
                  "Massachusetts law limits below-IG bonds to 5% of admitted assets. Moving to 7.5% would violate this statutory limit, making the excess non-admitted and reducing surplus. No return premium justifies violating a statutory investment limit — the consequence is not just financial but regulatory (potential enforcement action)."),
                 ("MassMutual can increase below-IG to a maximum of 5% of admitted assets (the statutory limit) and should evaluate whether the return premium justifies the capital cost of the additional 1.5% increase within the allowed range", True,
                  "Correct. The statutory limit (5%) is a hard constraint — not a guideline. MassMutual can increase from 3.5% to a maximum of 5%. The additional 1.5% allocation should be evaluated on a return-on-capital basis: extra return vs. extra RBC capital cost (13% vs. 1.3% capital charge). The team should calculate whether 9.2% yield minus the incremental capital cost exceeds the hurdle rate before proceeding within the statutory limit."),
                 ("MassMutual should request a state regulatory waiver to exceed the 5% limit given the attractive return", False,
                  "State investment limits are statutory, not discretionary. Regulatory waivers for statutory investment limits are extremely rare and typically only granted for extraordinary circumstances (such as a specific one-time investment with unique characteristics) — not for routine portfolio optimization. MassMutual's correct path is to operate within the 5% limit.")]
            ),
        ]
    )

    # Concept 4: Regulatory Capital and Investment Governance
    c4 = _concept(
        m2_id, 2,
        "Regulatory Capital Requirements and Investment Governance Obligations",
        "Explain how Risk-Based Capital (RBC) requirements influence investment decisions, and describe the governance obligations that investment regulations impose on insurance company boards, investment committees, and compliance functions.",
        "Regulatory capital requirements (RBC in the US, SCR under Solvency II) are not just financial constraints — they fundamentally reshape investment decision-making. Every investment decision implicitly includes a capital cost calculation, and investments that appear attractive on a gross yield basis may be unattractive on a return-on-capital basis. Beyond capital calculations, regulations impose governance obligations on insurance company boards and investment committees: written investment policies, regular board reporting, independent audit requirements, and personal accountability for investment decisions. Understanding these obligations is essential for everyone who participates in the institutional investment process.",
        "Hartford Life Insurance Company's investment governance structure: (1) Board Investment Committee — 4 directors, meets quarterly, reviews and approves the IPS annually, receives quarterly investment performance and compliance reports; (2) Management Investment Committee — CIO, CFO, CRO, Chief Actuary, meets monthly, reviews portfolio performance, approves tactical allocation changes within IPS bounds, reviews ALM quarterly; (3) Chief Investment Officer — responsible for overall investment strategy and daily management; (4) Chief Compliance Officer — independent compliance monitoring, quarterly compliance certification to the board; (5) External auditors — annual audit of statutory financial statements including investment valuation; (6) Internal audit — annual investment operations audit. Connecticut insurance law (Hartford's domicile) requires board-level investment oversight and written IPS documentation — regulatory examination reviews governance documentation as a primary focus.",
        [
            "RBC ratio: (Total Adjusted Capital / Authorized Control Level RBC). Ratios below 200% trigger regulatory intervention; below 100% triggers regulatory takeover.",
            "C-1 through C-4 risk categories: C-1 asset risk (credit/market), C-2 pricing risk, C-3 interest rate risk, C-4 business risk.",
            "Board investment committee: regulatory obligation in most states — board must actively oversee investment strategy, not just rubber-stamp management decisions.",
            "Investment policy statement: required by most state insurance regulators — must be reviewed and approved by the board at least annually.",
        ],
        [
            "Thinking the CIO is the only person with investment governance responsibility — boards, investment committees, compliance officers, and auditors all have defined governance roles that regulations impose.",
            "Assuming RBC is calculated once annually — insurers calculate projected RBC impact before major investment decisions and monitor RBC continuously.",
            "Confusing the RBC ratio trigger levels — 200% is the typical 'company action level' where management must prepare a corrective plan; 100% is the 'mandatory control level' where regulators can take control.",
        ],
        lessons=[
            _intro("Capital Requirements and Governance: How Regulation Shapes Every Investment Decision",
                   "Every time an insurance company's investment committee votes on an investment, two regulatory frameworks are invisibly present in the room: the capital requirements that determine how much equity the investment consumes, and the governance rules that determine who must approve it and how it must be reported. Let's make these visible."),
            _teach("Risk-Based Capital: How Capital Requirements Shape Investment Portfolios",
                   "RBC (US) and SCR (EU) transform each investment's gross return into a return-on-capital (ROC) calculation. The framework: (1) Each asset class has a C-1 risk factor (US) or standard formula stress (EU Solvency II): US Treasuries ≈0.3%, IG bonds ≈1-4% (graduated by credit quality), HY bonds ≈13%, equity ≈30%, real estate ≈10%; (2) Required capital = asset value × C-1 factor; (3) Return on capital = investment income / required capital; (4) Hurdle rate = the insurer's target ROE on required capital (typically 10-15%). RBC implications for portfolio construction: (a) Below-IG bonds require so much capital that their gross yield premium often fails to cover the capital cost — making IG bonds economically superior on ROC; (b) Equities' 30% capital charge means a 10% equity return yields only 10%/30% = 33% ROC — which may or may not exceed the insurer's target; (c) Treasuries' low capital charge (0.3%) means even modest Treasury yields generate very high ROC.",
                   ["ROC = investment income / (asset value × capital factor).",
                    "HY bonds at 13% capital: 8% yield / 13% = 62% ROC vs. IG at 5% / 1.5% = 333% ROC.",
                    "Equities at 30% capital: need 30%×ROE hurdle just to break even on ROC.",
                    "Capital efficiency drives portfolio design — not just yield."]),
            _teach("Board and Committee Governance Obligations",
                   "State insurance laws impose specific governance requirements on investment oversight: (1) Board Investment Committee — most states require a board-level committee to oversee investment strategy. The committee must: approve the IPS and any material changes, receive quarterly performance and compliance reports, review ALM analysis annually, and ensure independent oversight of investment management; (2) Written Investment Policy Statement (IPS) — required by virtually all state regulators; must specify: investment objectives, risk tolerance, asset class permitted investments, concentration limits, credit quality minimums, liquidity requirements; must be reviewed and approved by the board at least annually; (3) Compliance certification — the CCO must formally certify quarterly to the board that the portfolio is in compliance with the IPS and all regulatory limits; exceptions must be disclosed with corrective action plans; (4) Annual statutory audit — independent external auditors must audit the statutory financial statements including investment valuations; (5) Regulatory examination — state insurance departments conduct periodic examinations (every 3-5 years) with investment compliance as a primary focus.",
                   ["Board investment committee: required by most states — active oversight, not passive approval.",
                    "IPS: annual board approval required — cannot be delegated to management alone.",
                    "CCO quarterly certification: formal accountability mechanism between compliance and board.",
                    "Regulatory exam: investment governance documentation is a primary exam focus."]),
            _example("Hartford's Governance During the 2020 COVID Market Dislocation",
                     "In March 2020, investment-grade credit spreads widened sharply; equity markets fell 35%. Hartford's governance responded: Week 1 (March 9): Management Investment Committee met daily to review portfolio, assess ALM impact, and calculate COVID scenario's RBC impact. March 11: Emergency Board Investment Committee call — CIO presented a $500M tactical opportunity to buy IG bonds at historically wide spreads. Board approved a temporary IPS extension: equity limit increased from 10% to 12% for the IG bond purchase program (since IG bonds, not equities, were being bought — the extension was actually about liquidity). March 23-31: $500M deployed in IG corporate bonds at spreads of 280-320 bps — historically very wide. By December 2020, spreads compressed to 120 bps; the position earned approximately 15% total return. RBC impact: the IG bond purchases added capital efficiency (low C-1 charge). Hartford's rapid governance response — daily management review, emergency board call, documented IPS amendment — was later cited by the Connecticut insurance department as a model COVID response.",
                     "Investment governance under stress requires rapid decision-making within formal structures — daily management reviews, documented board approvals, and clear authority chains allow institutions to act fast while maintaining compliance."),
            _flash("What do the RBC ratio levels of 200% and 100% trigger for a US insurance company?",
                   "200% RBC ratio (Company Action Level): management must file a corrective action plan with the state regulator and implement steps to restore capital. 100% RBC ratio (Mandatory Control Level): the state regulator has authority to take control of the insurer's operations — the most severe regulatory intervention short of liquidation. Most insurers target 300-400% RBC ratios to provide a substantial buffer above the 200% action level."),
            _mcq("An insurance company's Total Adjusted Capital is $1.2 billion. The Authorized Control Level RBC is $400 million. What is the RBC ratio, and what does it indicate?",
                 ["30% — the company is below the mandatory control level and regulators may take over",
                  "300% — the company has a healthy capital buffer well above the 200% company action level",
                  "167% — the company is between the company action level and mandatory control level",
                  "400% — the company should return capital to shareholders immediately"],
                 1,
                 "RBC ratio = Total Adjusted Capital / Authorized Control Level RBC = $1.2B / $400M = 300%. A 300% RBC ratio indicates the insurer has $1.2B capital vs. $400M minimum required — a $800M buffer above the minimum. Most regulators consider 300-400% a healthy, well-capitalized level. Below 200% triggers company action level requirements; below 100% triggers mandatory control."),
            _mcq("An insurance company's Board Investment Committee receives the quarterly investment performance report but does not read it carefully, simply voting to approve without discussion. This MOST DIRECTLY violates:",
                 ["The Investment Advisers Act fiduciary duty",
                  "The board's governance obligation to provide active, substantive oversight of the investment program",
                  "NAIC investment limitation guidelines",
                  "GIPS performance reporting standards"],
                 1,
                 "Board investment committees have a governance obligation to provide active, substantive oversight — not rubber-stamp approval of management presentations. State insurance laws require boards to genuinely oversee investment strategy, understand risks, and make informed decisions. A board that passively approves without engagement fails to fulfill its oversight duty and creates personal liability for directors if investment losses follow."),
            _mcq("Under RBC requirements, investing $100M in a BBB corporate bond (C-1 factor 4%) vs. $100M in common equity (C-1 factor 30%). How much more required capital does the equity investment require?",
                 ["$26M more ($30M vs. $4M required capital)",
                  "$26 billion more",
                  "$260,000 more",
                  "No difference — RBC treats all investments equally"],
                 0,
                 "BBB bond RBC: $100M × 4% = $4M required capital. Common equity RBC: $100M × 30% = $30M required capital. Difference: $30M - $4M = $26M more required capital for the equity investment. This is why insurance companies hold primarily bonds — the capital efficiency (return on required capital) is dramatically better for investment-grade bonds vs. equity, even though equity may have higher gross returns."),
            _mcq("The Chief Compliance Officer (CCO) of an insurance company must provide a quarterly certification to the board. What is the PRIMARY purpose of this certification?",
                 ["To confirm that the company's investments have outperformed benchmarks",
                  "To certify that the investment portfolio complies with the IPS and all regulatory investment limits, with exceptions disclosed",
                  "To provide the board with a recommendation for new investment strategies",
                  "To confirm that all employees have completed their annual compliance training"],
                 1,
                 "The CCO quarterly certification creates formal accountability between the compliance function and the board. The CCO certifies: (1) the portfolio is within IPS limits; (2) all regulatory investment limits are met; (3) any exceptions or violations are disclosed along with corrective action plans. This mechanism ensures the board is not relying solely on management's self-reporting — the CCO, who reports independently to the board, provides an accountability check."),
            _mcq("An insurance company maintains an RBC ratio of 180%, which is below the 200% Company Action Level. What is the insurer REQUIRED to do?",
                 ["Immediately liquidate all equity investments to raise the ratio above 200%",
                  "File a Corrective Action Plan with the state regulator outlining steps to restore capital above the Company Action Level",
                  "Transfer policyholder liabilities to a reinsurer to reduce the required capital",
                  "Nothing — the 180% ratio is above the 100% mandatory control level so no action is required"],
                 1,
                 "When the RBC ratio falls below 200% (Company Action Level), the insurer must file a Corrective Action Plan with the state insurance regulator. The plan must outline specific steps to restore capital above the 200% threshold — such as raising additional equity capital, reducing dividends, selling assets, or reducing risk. The 100% Mandatory Control Level (where regulators can take over) is much more severe — the Company Action Level at 200% is an early warning trigger designed to prompt corrective action before the situation deteriorates further."),

            _scenario(
                "Protective Life's investment committee is considering two investment strategies for $200M: Strategy A — $200M in AAA CMBS (Commercial Mortgage-Backed Securities), C-1 factor 1.0%, expected return 5.6%. Strategy B — $200M in BB high-yield corporate bonds, C-1 factor 13%, expected return 8.1%. The insurer's target ROE on required capital is 12%. Which strategy delivers a higher return on required capital?",
                "Calculate the ROC for each strategy and identify the preferred option.",
                [("Strategy B — 8.1% gross yield is 2.5% higher than Strategy A, making it the clear winner", False,
                  "Gross yield comparison ignores capital costs. Strategy A: required capital = $200M × 1% = $2M; capital cost at 12% = $240K; risk-adjusted return = 5.6% - 0.12% = 5.48%; ROC = 5.6%×$200M / $2M = 560%. Strategy B: required capital = $200M × 13% = $26M; capital cost = $3.12M (1.56%); risk-adjusted return = 8.1% - 1.56% = 6.54%; ROC = 8.1%×$200M / $26M = 62%. Strategy A wins on ROC (560% vs. 62%)."),
                 ("Strategy A — the AAA CMBS delivers dramatically higher return on required capital (ROC) because its minimal capital charge (1%) means the $11.2M income supports only $2M required capital, vs. $16.2M income on $26M required capital for Strategy B", True,
                  "Correct. ROC = (return × asset value) / required capital. Strategy A ROC = ($200M × 5.6%) / ($200M × 1%) = $11.2M / $2M = 560%. Strategy B ROC = ($200M × 8.1%) / ($200M × 13%) = $16.2M / $26M = 62%. Despite lower gross yield, Strategy A's capital efficiency is 9x better. For a regulated insurer with 12% ROE target, AAA CMBS at 5.6% utterly dominates HY bonds at 8.1% on the correct metric."),
                 ("Neither strategy is appropriate — both involve non-government bonds and violate conservative insurance investment principles", False,
                  "Both CMBS and high-yield bonds are legitimate insurance company investments (within limits). The question is capital efficiency. Investment-grade CMBS is a core holding for many US life insurers; high-yield bonds are permitted within NAIC guidelines (up to 5% of admitted assets). The regulatory framework doesn't prohibit either — it prices them differently through capital requirements.")]
            ),
        ]
    )

    m2["concepts"] = [c3, c4]
    ch["modules"] = [m1, m2]
    return ch


def _build_ch11(course_id):
    ch_id = _id()
    ch = {
        "id": ch_id, "course_id": course_id, "order": 11,
        "title": "Ethical Standards and Governance",
        "description": "The ethical obligations of investment professionals — including codes of conduct, managing conflicts of interest, ethical trading practices, responsibilities to clients, corporate governance, and building effective compliance and audit programs.",
    }

    # ── Module 1: Ethics and Professional Conduct ─────────────────────────────
    m1_id = _id()
    m1 = {"id": m1_id, "chapter_id": ch_id, "order": 1,
          "title": "Ethics and Professional Conduct in Investment Management"}

    # Concept 1: Codes of Ethics, Conflicts of Interest, and Trading Practices
    c1 = _concept(
        m1_id, 1,
        "Codes of Ethics, Conflicts of Interest, and Ethical Trading Practices",
        "Describe the purpose and content of investment professional codes of ethics, explain how material conflicts of interest must be identified and managed, and identify unethical trading practices including front-running, churning, and market manipulation.",
        "Ethics in investment management is not abstract philosophy — it is a set of specific behavioral obligations that determine how professionals treat clients, handle information advantages, and manage their own interests versus clients' interests. Codes of ethics codify these obligations. Conflicts of interest — situations where the professional's financial interest diverges from the client's — are the most common source of ethical failure. Specific trading practices (front-running, churning, market manipulation) are both ethical violations and, in most cases, securities law violations. Understanding these standards protects clients, maintains market integrity, and protects the professional from regulatory and reputational consequences.",
        "BlackRock's Code of Ethics covers all 20,000 employees globally. Key provisions: (1) Personal account trading — employees must pre-clear personal trades in securities that BlackRock clients hold or may trade; a 30-day holding period applies to personal purchases; (2) Gifts and entertainment — no gifts exceeding $100 in value from vendors, brokers, or clients; no entertainment events that create conflicts with client interests; (3) Outside business activities — must be pre-approved to prevent undisclosed conflicts; (4) Conflicts of interest reporting — annual conflict disclosure form; immediate reporting of any new potential conflict; (5) Front-running prohibition — absolute: no employee may trade in a security before a client order in the same security is fully executed. BlackRock's ethics program investigated 23 personal trading pre-clearance requests in 2023 — 19 were approved, 4 denied (securities on restricted list). No insider trading investigations were opened. Their compliance structure demonstrates that a rigorous ethics program operates as a daily operational system, not an annual training event.",
        [
            "Fiduciary duty: the highest ethical standard — place client interests above all others, including the adviser's own financial interests.",
            "Conflict of interest: any situation where the adviser's financial interest diverges from the client's; must be disclosed and managed.",
            "Front-running: trading for personal or proprietary accounts ahead of known client orders to benefit from the expected price impact.",
            "Churning: excessive trading in a client's account to generate commissions, without regard for the client's investment objectives.",
        ],
        [
            "Thinking disclosure alone resolves a conflict of interest — disclosure is necessary but insufficient. The conflict must also be managed (avoided, mitigated, or minimized).",
            "Confusing market timing with market manipulation — market timing (predicting price movements) is legal; market manipulation (intentionally moving prices through artificial trades or false information) is illegal.",
            "Believing only registered investment advisers have fiduciary duties — investment professionals at insurance companies, pension funds, and other institutions have similar obligations regardless of formal registration status.",
        ],
        lessons=[
            _intro("Ethics in Investment Management: From Principles to Practice",
                   "A code of ethics isn't a poster on the wall — it's a daily operating standard that determines how investment professionals treat the clients who trust them with their life savings and retirement security. Let's examine what these standards actually require."),
            _teach("Codes of Ethics: Content and Purpose",
                   "A code of ethics for investment professionals typically addresses: (1) Fiduciary duty — the obligation to act in clients' best interests above all others, including the firm's and the individual's own financial interests; (2) Professionalism — representing qualifications and experience honestly; maintaining professional competence; (3) Integrity — not engaging in deceptive, manipulative, or fraudulent practices; fair dealing with clients, prospects, and markets; (4) Personal account trading restrictions — limiting or requiring pre-clearance for personal securities transactions that could conflict with client trading; (5) Confidentiality — protecting client information and not using material non-public information for personal gain; (6) Disclosure obligations — disclosing compensation arrangements, conflicts of interest, and material facts that clients would want to know. The CFA Institute's Code of Ethics is the most widely adopted global standard for investment professionals. FINRA Rule 2010 (Standards of Commercial Honor) and SEC fiduciary rules impose similar obligations on registered professionals.",
                   ["Fiduciary duty: client interests first, always — no exceptions for profit or convenience.",
                    "CFA Institute Code: 7 standards covering professionalism, capital markets integrity, duties to clients, duties to employers, investment analysis, conflicts of interest, and responsibilities as CFA member.",
                    "Personal account trading: pre-clearance and blackout periods prevent front-running clients.",
                    "Confidentiality: client information is protected; MNPI (material non-public information) cannot be used for trading."]),
            _teach("Conflicts of Interest and Prohibited Trading Practices",
                   "Material conflicts of interest must be disclosed to clients when they cannot be avoided. Common conflicts in investment management: (1) Principal transactions — adviser buys securities from/sells to client as principal (firm owns the security); (2) Soft dollar arrangements — directing client commissions to brokers who provide research (creates incentive to over-trade); (3) Affiliated product recommendations — recommending funds or products that generate fee income for the adviser's firm; (4) Performance-based fees — may incentivize excessive risk-taking. Prohibited trading practices: (1) Front-running — trading ahead of known client orders to profit from the expected price impact; (2) Churning — excessive trading in client accounts to generate commissions, without regard for investment merit; (3) Market manipulation — deliberately moving security prices through wash sales (buying and selling to oneself), painting the tape (creating appearance of volume), or spreading false information; (4) Scalping — recommending securities the adviser already owns to benefit from price appreciation caused by the recommendation.",
                   ["Front-running: illegal and unethical — using foreknowledge of client orders for personal gain.",
                    "Churning: violates fiduciary duty and FINRA rules — generates commissions at client's expense.",
                    "Market manipulation: wash sales, painting the tape, false information — criminal offenses.",
                    "Soft dollars: not prohibited but must be disclosed; research purchased must benefit the client."]),
            _example("BlackRock's Front-Running Prevention System",
                     "In 2019, a portfolio manager at a major asset manager was prosecuted for front-running: he learned that his firm would purchase $50M of a specific biotech stock for clients the next morning, and purchased 20,000 shares for his personal account the afternoon before. When the large client buy order pushed the stock up 4% the next morning, he sold — netting $80,000 profit. He was convicted under Rule 10b-5 and sentenced to 18 months. BlackRock's prevention system: (1) All client orders entered in the Order Management System (OMS) are flagged; (2) Employee personal account trading system is linked to the OMS — any attempted purchase of a security with active client orders is automatically blocked; (3) Trading surveillance monitors for unusual employee personal trading patterns relative to client order flow; (4) 30-day mandatory holding period prevents short-term personal trading around client orders. The technical controls make front-running essentially impossible, removing the temptation by eliminating the opportunity.",
                     "The most effective ethics controls are technical — systematic barriers that make prohibited behavior impossible, not just training that makes it unlikely."),
            _flash("What is 'front-running' in investment management?",
                   "Front-running occurs when an investment professional or firm trades for their own account (or a preferential account) ahead of executing a known client order, intending to profit from the price impact the client's order will cause. Example: a manager learns a client will buy 100,000 shares of XYZ tomorrow morning, and buys XYZ personally the afternoon before. When the client order moves the price up, the manager profits. Front-running is both a fiduciary breach and a securities law violation (Rule 10b-5)."),
            _mcq("An investment adviser recommends proprietary mutual funds to clients without disclosing that the adviser receives a higher fee when clients invest in these funds vs. third-party alternatives. This MOST directly violates:",
                 ["The prohibition on market manipulation",
                  "The fiduciary duty to act in clients' best interests and disclose all material conflicts of interest",
                  "NAIC investment limitation guidelines for insurance companies",
                  "GIPS performance reporting standards"],
                 1,
                 "Recommending proprietary products that generate higher fees for the adviser, without disclosing the financial conflict, is a textbook fiduciary duty violation. Clients must be informed of compensation arrangements that could bias recommendations so they can evaluate whether the recommendation truly serves their interests. Disclosure alone isn't sufficient — the adviser must also ensure the recommendation is suitable for the client (not just profitable for the firm)."),
            _mcq("A broker executes 50 trades per month in a client's account with $500,000 in assets, generating substantial commissions but no meaningful return improvement vs. a buy-and-hold strategy. This MOST LIKELY constitutes:",
                 ["Appropriate active portfolio management in a volatile market",
                  "Front-running — using client order flow to benefit personal accounts",
                  "Churning — excessive trading primarily to generate commissions rather than serve the client's investment objectives",
                  "Market manipulation — creating artificial trading volume in client securities"],
                 2,
                 "Churning is characterized by excessive trading frequency in a client account relative to the client's investment objectives and account size, where the primary beneficiary is the broker through commissions. 50 trades per month in a $500K account is extremely high turnover — the transaction costs alone likely eliminate any investment value. FINRA and the courts evaluate churning based on turnover ratio and whether the trading was in the client's interest."),
            _mcq("A hedge fund manager publishes false positive news about a small-cap company on social media to drive up the stock price, then sells the fund's position at the inflated price. This is BEST described as:",
                 ["Legitimate investment research distributed through social media channels",
                  "Front-running — trading ahead of the fund's own future orders",
                  "Market manipulation — deliberately moving security prices through false information",
                  "Scalping — recommending securities the manager personally holds"],
                 2,
                 "Publishing false positive information to artificially inflate a stock price and then selling into the inflated price is market manipulation under SEC Rule 10b-5 and the Securities Exchange Act. This 'pump and dump' scheme is both a criminal offense and civil securities violation. The manager faces disgorgement of profits, civil penalties, and criminal prosecution. Note: sharing genuine investment research through social media is legal; publishing known false information is not."),
            _mcq("Which personal account trading restriction is MOST effective at preventing front-running by investment professionals?",
                 ["Prohibiting employees from owning any securities personally",
                  "Requiring employees to hold all personal security purchases for a minimum 30-day period after purchase",
                  "Limiting personal account investments to index funds only",
                  "Requiring annual disclosure of all personal holdings"],
                 1,
                 "A mandatory 30-day holding period prevents the profitable short-term trade that makes front-running attractive. Front-running requires the personal position to be established before the client order and sold after the price impact — a 30-day hold breaks this cycle. While pre-clearance blocks purchases when client orders are active, the holding period adds a second layer: even if a position was legitimately established, it cannot be sold into a short-term price movement caused by subsequent client trading."),
            _mcq("The CFA Institute's Code of Ethics applies to:",
                 ["Only investment managers who are also registered with the SEC",
                  "Only equity portfolio managers at publicly traded financial institutions",
                  "All CFA charterholders and CFA Institute members regardless of employer type or jurisdiction",
                  "Only financial advisers serving retail clients in the United States"],
                 2,
                 "The CFA Institute Code of Ethics and Standards of Professional Conduct apply to all CFA charterholders and members globally — regardless of employer (bank, insurer, pension fund, hedge fund), jurisdiction, or client type (retail or institutional). The standards are designed to be universally applicable because investment ethics obligations don't vary by geography or employer type. Violations can result in suspension or revocation of the CFA charter."),
            _scenario(
                "A senior portfolio manager at Nationwide Life learns from a corporate client that XYZ Corporation — currently held in several Nationwide portfolios — will announce disappointing quarterly earnings next week (material non-public information). The manager faces three options: Option A — sell XYZ positions from all Nationwide portfolios before the announcement to avoid losses. Option B — alert the trading desk to 'stay away from XYZ' without explanation and restrict new purchases. Option C — immediately notify the Chief Compliance Officer, place XYZ on the restricted list, and take no trading action until the information becomes public.",
                "Which action is both ethically and legally correct?",
                [("Option A — protecting client portfolios from foreseeable losses is the portfolio manager's fiduciary duty", False,
                  "Selling client portfolios based on material non-public information is insider trading — illegal under SEC Rule 10b-5 regardless of whether the intent was to 'protect' clients. Using MNPI to trade benefits some clients at the expense of the investors on the other side of the trade who don't have the same information."),
                 ("Option B — restricting new purchases without explanation is a reasonable compromise that avoids trading on MNPI", False,
                  "Option B is insufficient. The portfolio manager still possesses MNPI and the informal 'stay away' instruction doesn't properly isolate the information. If any trading occurs in XYZ (including liquidations by other managers who don't know about the restriction), the firm is still exposed to insider trading liability."),
                 ("Option C — CCO notification, formal restricted list placement, and trading halt until public disclosure is the legally and ethically required response to receipt of MNPI", True,
                  "Correct. Upon receiving MNPI, the only permissible path is to stop trading entirely and establish proper information barriers. The CCO must be immediately notified; XYZ must be placed on the firm's restricted list (prohibiting all trading by all managers); the restriction remains until the information becomes public. This is the legally and ethically mandated response to MNPI receipt.")]
            ),
        ]
    )

    # Concept 2: Responsibilities to Clients, Corporate Governance, and Compliance Programs
    c2 = _concept(
        m1_id, 2,
        "Responsibilities to Clients, Corporate Governance, and Investment Compliance Programs",
        "Describe the investment professional's specific responsibilities to clients, explain how institutional investors exercise corporate governance through proxy voting and engagement, and describe the structure of an effective investment compliance and audit program.",
        "The client relationship creates specific behavioral obligations beyond the general fiduciary duty: suitability analysis, fair dealing, timely execution, complete disclosure, and regular communication. Institutional investors also have responsibilities as major shareholders — they must exercise their voting rights (proxy voting) and engage with company management on governance, compensation, and strategy. Finally, the compliance infrastructure that supports all of these obligations requires formal programs with documented policies, designated officers, regular audits, and board-level accountability. Without systematic compliance infrastructure, individual ethical commitments are insufficient to maintain consistent standards across large organizations.",
        "TIAA's Investment Stewardship program exemplifies modern institutional governance responsibilities: (1) Client responsibilities — all 5+ million clients receive quarterly portfolio statements, annual fee disclosure, and ongoing suitability monitoring; clients' investment objectives are reviewed annually; complaints have a 24-hour acknowledgment and 5-business-day resolution standard; (2) Corporate governance — TIAA manages $1.2 trillion in assets and votes on approximately 15,000 proxy ballots annually. Their voting guidelines prioritize: independent board directors, executive compensation aligned with long-term performance, transparent sustainability disclosures, and robust risk management committee; (3) Compliance program — Chief Compliance Officer reports to the Board Risk Committee; annual compliance training for all investment staff; automated surveillance of personal trading, communication monitoring, and portfolio management system controls; annual internal audit of investment operations; biennial external compliance assessment; (4) Whistleblower program — anonymous reporting hotline, no-retaliation policy, SEC whistleblower program awareness training.",
        [
            "Suitability: investments must be appropriate for the specific client's financial situation, objectives, time horizon, and risk tolerance — not just generically suitable.",
            "Proxy voting: institutional investors have a fiduciary obligation to vote proxies in clients' best interests — not abstaining, not delegating without oversight.",
            "Corporate governance engagement: institutional investors increasingly engage directly with company management on board composition, executive pay, and sustainability.",
            "Compliance program elements: written policies, designated CCO, training, surveillance, annual review, whistleblower protection.",
        ],
        [
            "Thinking suitability is a one-time determination — client circumstances change over time; suitability must be reassessed periodically.",
            "Assuming proxy voting is administrative rather than fiduciary — DOL guidance confirms proxy voting is a fiduciary act for pension managers; most institutional investors treat it as such.",
            "Believing a compliance program without enforcement is sufficient — policies that are documented but not enforced create worse outcomes than no policy (the illusion of compliance without substance).",
        ],
        lessons=[
            _intro("What Clients Deserve and How Institutions Govern: Responsibilities, Governance, and Compliance",
                   "A portfolio manager's responsibility doesn't end at investment returns. Clients deserve suitability, fair treatment, and transparency. Companies whose shares are owned by the insurer deserve active governance engagement. And all of this requires systematic compliance infrastructure that outlasts any individual employee."),
            _teach("Responsibilities to Clients: Suitability, Fair Dealing, and Disclosure",
                   "Investment professionals owe specific, documented responsibilities to clients: (1) Know Your Client (KYC) — gather complete information about the client's financial situation, investment objectives, time horizon, risk tolerance, and constraints before making any investment recommendation. Document KYC annually and update whenever circumstances change; (2) Suitability — every investment recommendation must be suitable for the specific client. A high-risk growth portfolio may be suitable for a 35-year-old growth investor but entirely unsuitable for a 70-year-old retiree needing income; (3) Fair dealing — all clients of the same investment strategy must be treated equitably. New information affecting a recommendation must be communicated to all clients simultaneously — not selectively to preferred accounts; (4) Timely and best execution — execute client orders promptly, seeking best possible terms; (5) Disclosure — disclose all fees, compensation arrangements, conflicts of interest, and material facts the client would want to know; (6) Communication standards — provide regular, accurate, and complete performance reports and portfolio information.",
                   ["KYC: mandatory foundation — no recommendation without knowing the client's complete financial picture.",
                    "Suitability: must be specific to the client, not just generically acceptable.",
                    "Fair dealing: new research goes to all clients simultaneously — not first to preferred accounts.",
                    "Annual review: client objectives and suitability must be reassessed at least annually."]),
            _teach("Corporate Governance Responsibilities and Compliance Programs",
                   "Institutional investors as major shareholders have corporate governance responsibilities: (1) Proxy voting — fiduciary obligation to vote proxies in clients' best interests; required to have a written proxy voting policy; must not abstain to avoid controversy. Common institutional voting priorities: independent directors, executive compensation aligned with long-term performance, audit committee independence, anti-takeover defense limits; (2) Shareholder engagement — direct dialogue with company management and board on governance concerns; filing or co-filing shareholder proposals when engagement fails; (3) ESG integration — many institutional investors incorporate environmental, social, and governance factors into investment analysis and engagement. Effective compliance programs require: (1) Written policies and procedures covering all investment operations; (2) Designated Chief Compliance Officer with independent reporting line to the board; (3) Pre-trade and post-trade compliance surveillance; (4) Annual compliance training; (5) Annual compliance review by CCO; (6) Internal audit (independent of compliance function); (7) Whistleblower program with no-retaliation protection; (8) Regulatory exam readiness.",
                   ["Proxy voting policy: must be written, available to clients, and consistently applied.",
                    "Engagement: institutional investors increasingly talk directly to boards about governance concerns.",
                    "CCO independence: reports to board/audit committee, not to portfolio management team.",
                    "Whistleblower: SEC's program offers financial rewards for reporting violations; firms must not retaliate."]),
            _example("TIAA's Proxy Voting and Governance Engagement",
                     "In 2022, TIAA voted against the management slate for board directors at 312 companies where TIAA's analysis showed insufficient board independence (fewer than 75% independent directors). At 28 companies, TIAA went further — directly engaging with the Board Chair and Nominating Committee to discuss board composition. At 6 companies where engagement was unsuccessful, TIAA filed a shareholder proposal calling for board structure changes. In 3 of these 6 cases, the proposal received majority shareholder support and the company changed its board composition within 18 months. TIAA's view: as a major institutional shareholder, abstaining or following management recommendations without analysis would be a fiduciary failure. Their 15,000 annual proxy votes represent active governance oversight, not administrative compliance.",
                     "Institutional proxy voting is governance stewardship — every vote is a fiduciary decision about how client capital should influence corporate behavior, not a formality to be delegated to a proxy advisory firm without oversight."),
            _flash("What is the 'Know Your Client' (KYC) obligation in investment management?",
                   "KYC requires investment professionals to gather and document complete information about each client before making investment recommendations: financial situation (income, assets, liabilities), investment objectives (growth, income, preservation), time horizon, risk tolerance, and constraints (tax status, liquidity needs, legal restrictions). KYC must be updated at least annually and whenever the client's circumstances change materially. It is the foundation of suitability analysis — without KYC, there is no basis for determining whether an investment is appropriate for a specific client."),
            _mcq("An investment adviser recommends the same high-risk emerging markets fund to both a 30-year-old growth investor and a 68-year-old retiree needing income without distinguishing between their different needs. This MOST LIKELY violates:",
                 ["The prohibition on market manipulation",
                  "The suitability obligation — investments must be appropriate for the specific client's situation, not generically applied to all clients",
                  "GIPS performance reporting standards for the emerging markets composite",
                  "The Investment Company Act of 1940"],
                 1,
                 "Suitability requires that each investment recommendation be appropriate for the specific client's financial situation, objectives, time horizon, and risk tolerance. A high-risk emerging markets fund may be suitable for a young growth investor but almost certainly unsuitable for a retiree needing stable income. Applying the same recommendation to all clients without suitability analysis is a fundamental compliance failure — and a fiduciary breach."),
            _mcq("A portfolio manager receives updated negative research on a stock held in 50 client accounts. She immediately calls her 3 largest clients to warn them before distributing the research to all clients. This MOST LIKELY violates:",
                 ["The prohibition on insider trading under the Securities Exchange Act",
                  "The fair dealing obligation — all clients must receive material information affecting their holdings simultaneously",
                  "The CCO quarterly certification requirement",
                  "The NAIC investment limitation guidelines"],
                 1,
                 "Fair dealing requires that material information affecting client investments be communicated to all clients simultaneously — or at least through a process that doesn't systematically favor preferred clients. Calling the largest clients first (presumably to retain their business) while delaying disclosure to smaller clients is a fair dealing violation. It creates an information asymmetry that advantages some clients at the expense of others — the antithesis of fiduciary behavior."),
            _mcq("An institutional investor holds 5% of a public company's shares. The company's board proposes a compensation plan that would pay the CEO $50M for one year of below-average performance. Which governance action is MOST appropriate?",
                 ["Vote in favor of the proposal since management generally knows best about appropriate compensation",
                  "Abstain from the vote to avoid controversy with company management",
                  "Vote against the compensation proposal and engage with the board's compensation committee to explain the concerns",
                  "Immediately sell all shares in the company to avoid the governance controversy"],
                 2,
                 "Institutional investors have a fiduciary obligation to vote proxies in clients' best interests — abstaining to avoid controversy fails this obligation. Excessive executive compensation disconnected from performance damages long-term shareholder value. The appropriate response: vote against the proposal AND engage with the compensation committee to explain concerns. Selling the shares is also an option but foregoes the governance influence that comes with being a significant shareholder."),
            _mcq("A compliance officer discovers that a portfolio manager violated the firm's personal trading policy (traded ahead of a client order). The manager is a top performer responsible for 30% of the firm's revenue. What must the compliance officer do?",
                 ["Document the violation privately and counsel the manager informally to avoid disrupting performance",
                  "Report the violation through the established compliance escalation process, regardless of the manager's revenue contribution",
                  "Suspend the compliance policy for star performers who generate significant revenue for the firm",
                  "Transfer the violation reporting to a junior compliance staff member to insulate senior leadership"],
                 1,
                 "Compliance independence means enforcing rules consistently regardless of the violator's seniority, performance, or revenue contribution. Selectively enforcing compliance against less important employees while excusing high performers destroys the compliance culture and creates regulatory and reputational risk. The CCO's independence from portfolio management (required by both ethics standards and SEC guidance) exists precisely to prevent commercial considerations from overriding compliance obligations."),
            _mcq("Which element of a compliance program MOST DIRECTLY provides employees with a safe channel to report suspected violations without fear of retaliation?",
                 ["The annual compliance training program",
                  "The pre-trade compliance system that blocks policy violations",
                  "The whistleblower program with anonymous reporting and no-retaliation policy",
                  "The quarterly CCO certification to the board"],
                 2,
                 "A whistleblower program with anonymous reporting channels (hotline, web portal) and documented no-retaliation protections gives employees a safe path to report concerns about colleagues, management, or institutional practices. Without this protection, employees often stay silent when they witness violations — particularly when the violator is senior. SEC's whistleblower program provides additional protection and financial incentives (10-30% of sanctions above $1M) for reporting violations to the SEC directly."),
            _scenario(
                "Lincoln Financial's compliance team identifies three employees who violated policies in Q3: Employee A — a portfolio manager who failed to pre-clear a personal trade (minor violation, first offense, no financial gain). Employee B — a trading desk analyst who shared a client's confidential portfolio information with a friend at another firm (serious breach, first offense). Employee C — a senior vice president who executed 15 trades ahead of client orders over 6 months (systematic front-running, potential criminal violation). How should Lincoln Financial's compliance and legal team respond to each?",
                "Which response framework correctly calibrates consequences to the severity of each violation?",
                [("All three employees should receive identical consequences — equal treatment under the compliance policy", False,
                  "Equal treatment means applying the same process and standards to all — not identical consequences regardless of severity. Compliance systems must be calibrated: a first-offense administrative error vs. a serious confidentiality breach vs. systematic criminal conduct require fundamentally different responses."),
                 ("Employee A: formal written warning and mandatory re-training; Employee B: formal disciplinary action, legal review of potential regulatory reporting obligation, and client notification if required; Employee C: immediate suspension, referral to legal and law enforcement if evidence supports criminal conduct, mandatory SEC self-reporting evaluation", True,
                  "Correct. The response must match the severity: Employee A's first-offense technical violation warrants warning + training. Employee B's confidentiality breach is serious but may not be criminal — legal review, potential regulatory notification, client notification if required. Employee C's systematic front-running is potential criminal insider trading — immediate suspension, law enforcement referral, and proactive SEC self-reporting evaluation (which can reduce penalties). Calibrated responses are essential."),
                 ("Only Employee C should face consequences — minor and single-instance violations are always exempt under professional standards", False,
                  "Minor violations must be documented and addressed — even first-offense administrative errors create precedent and pattern risk if ignored. Employee A's warning creates a record; if they violate again, prior documentation supports escalation. Systematic patterns emerge from individual uncorrected violations. No violation should be entirely ignored.")]
            ),
        ]
    )

    m1["concepts"] = [c1, c2]

    # ── Module 2: Governance Structures and Audit ─────────────────────────────
    m2_id = _id()
    m2 = {"id": m2_id, "chapter_id": ch_id, "order": 2,
          "title": "Investment Governance Structures and Oversight"}

    # Concept 3: Corporate Governance Principles in Investment Management
    c3 = _concept(
        m2_id, 1,
        "Corporate Governance in Institutional Investment: Boards, Committees, and Accountability Structures",
        "Describe the corporate governance structures that oversee institutional investment programs — including board roles, investment committee responsibilities, management accountability, and the separation of functions that prevents conflicts and errors.",
        "Corporate governance of an investment program is the system of checks, balances, and accountability structures that ensure the portfolio is managed in the interests of beneficiaries (policyholders, plan participants) rather than management. Effective governance requires: board-level oversight with appropriate expertise, a well-functioning investment committee with clear authority, management accountability through documented mandates and performance reviews, and separation of investment management, risk management, and compliance functions. Governance failures are the root cause of most major institutional investment scandals — not just individual ethical failures.",
        "New York Life's investment governance structure: (1) Board of Directors (18 members) — fully independent of management. Board's Finance Committee oversees investment risk and strategy; meets quarterly; receives presentations from CIO, CFO, CRO, and Chief Actuary; approves IPS annually; reviews major tactical decisions; (2) Management Investment Committee — CIO, Deputy CIO, CFO, CRO, Chief Actuary, Head of ALM; meets monthly; approves tactical allocation within IPS bounds; reviews manager performance; (3) Investment teams — organized by asset class (fixed income, equities, private assets, real estate) with dedicated portfolio managers; (4) Risk Management — separate from portfolio management; independent risk measurement, limit monitoring, and escalation; (5) Compliance — reports to General Counsel and Board Audit Committee; (6) Internal Audit — independent from all investment functions; annual audit of investment operations. Separation of functions: no single person or team controls more than one of the following: investment decisions, risk limits, compliance monitoring, and accounting. This four-way separation prevents any single failure from going undetected.",
        [
            "Board fiduciary duty: board members of insurance companies owe fiduciary duty to policyholders — they must actively oversee investment management, not passively receive reports.",
            "Investment committee authority: clearly defined in writing — what decisions require committee approval vs. management discretion.",
            "Four-way separation: investment decisions, risk management, compliance monitoring, and accounting must each be independent functions.",
            "Whistleblower protection: governance must protect employees who report concerns about governance failures.",
        ],
        [
            "Thinking governance is only about preventing fraud — governance also prevents errors, misaligned incentives, and strategic drift that aren't fraudulent but still harm beneficiaries.",
            "Confusing oversight with micromanagement — the board's role is to set strategy, oversee risk, and hold management accountable, not to make individual portfolio decisions.",
            "Believing strong governance is only for large institutions — even small investment programs need clear authority matrices, documented IPS, and independent compliance functions.",
        ],
        lessons=[
            _intro("Governance: The Structural Foundation of Trust",
                   "The most talented investment professional cannot substitute for a well-designed governance structure. Governance defines who has authority, who provides oversight, and who is accountable when things go wrong. Without it, even ethical individuals operate without guardrails."),
            _teach("Board and Investment Committee Governance",
                   "Board-level investment governance: the board (or its Investment/Finance Committee) is the ultimate governance authority for the investment program. Board responsibilities: (1) Approve and annually review the Investment Policy Statement; (2) Oversee investment strategy — understand and challenge the overall approach, not just receive reports; (3) Review investment performance quarterly — risk-adjusted returns vs. benchmarks and peers; (4) Ensure appropriate risk management — review ALM, concentration risks, and stress test results; (5) Hold management accountable — the CIO presents performance; the board evaluates whether results reflect skill, luck, or poor judgment. Investment committee responsibilities: the management committee translates board strategy into operational decisions: (1) Approve tactical allocation changes within IPS bounds; (2) Hire and terminate external managers; (3) Review and approve new asset classes or investment vehicles; (4) Set individual manager mandates and benchmarks; (5) Monitor compliance with IPS and regulatory limits. Authority matrix: every investment decision must have a clearly defined approval authority — routine trades (portfolio manager), tactical tilts (Investment Committee), IPS changes (Board), major strategic changes (Board with external consultant review).",
                   ["Board: sets strategy, approves IPS, oversees risk, holds management accountable.",
                    "Investment Committee: translates strategy to operations, hires/fires managers, approves tactical changes.",
                    "Portfolio managers: execute within committee-approved mandates.",
                    "Authority matrix: documents who approves what; prevents both unauthorized decisions and decision vacuum."]),
            _teach("Separation of Functions and Management Accountability",
                   "The most critical governance control is separation of functions — ensuring that no single person or team controls both decision-making and oversight. The four functions that must be separated: (1) Investment management — portfolio managers make investment decisions; (2) Risk management — independent risk team measures and monitors risk, reports to CRO and board, can escalate concerns directly to board without portfolio management approval; (3) Compliance — monitors IPS and regulatory compliance, reports to CCO and board, independent of portfolio management; (4) Accounting/valuations — records and values positions, independent of portfolio management to prevent marking positions to mislead performance. Management accountability structures: (1) Documented mandates — every portfolio manager has a written mandate specifying benchmark, risk budget, and investment universe; (2) Performance evaluation — annual formal reviews with objective metrics (risk-adjusted returns, attribution analysis, compliance record); (3) Compensation alignment — long-term incentive compensation tied to multi-year performance prevents short-termism; (4) Succession planning — governance must not be dependent on any single individual.",
                   ["Risk management: independent from portfolio management — can escalate to board without PM approval.",
                    "Compliance: independent from portfolio management — CCO has direct board access.",
                    "Valuations: independent from portfolio management — prevents portfolio managers from marking positions favorably.",
                    "Documented mandates: every PM has a written, board-approved investment mandate."]),
            _example("Separation of Functions: The Barings Bank Lesson",
                     "In 1995, Barings Bank — the world's oldest merchant bank — collapsed after a single trader, Nick Leeson, accumulated $1.4 billion in losses in Singapore. The root cause: Leeson controlled BOTH trading operations AND the back office that settled and recorded trades. There was no separation of functions. He used his control over both functions to hide losses for 2 years by using fictitious accounts to offset his losses in the official records. No risk manager, compliance officer, or accounting function could detect the fraud because they all relied on Leeson's own records. The governance lesson: a properly separated investment operation would have had an independent back office (not controlled by the trader) that would have detected the discrepancies immediately. Separation of functions doesn't prevent genius — it prevents the concealment of failure.",
                     "Barings' collapse wasn't about a bad investment decision — it was about a governance failure that allowed one person to hide bad decisions indefinitely. Separation of functions is the structural answer."),
            _flash("What is the purpose of an 'authority matrix' in investment governance?",
                   "An authority matrix is a documented table specifying who has the authority to approve each type of investment decision. Examples: portfolio managers approve individual security trades within mandate limits; the Investment Committee approves tactical allocation changes; the Board approves IPS changes or major strategic shifts. The authority matrix prevents both unauthorized decisions (someone acting beyond their authority) and decision vacuums (decisions that aren't made because no one has clear authority). It must be reviewed and updated annually."),
            _mcq("The MOST critical separation of functions in an institutional investment operation is between:",
                 ["The CIO and the CFO — they should never share financial data",
                  "Investment management and risk management/compliance — those who make investment decisions must not also control the oversight of those decisions",
                  "The Board and management — boards should never speak directly with portfolio managers",
                  "Internal audit and external auditors — they must never review the same portfolio simultaneously"],
                 1,
                 "The most critical separation is between investment decision-making and the oversight functions (risk management, compliance, and accounting). When portfolio managers also control risk monitoring, compliance, or position valuation, there is no independent check on their decisions — exactly the scenario that enabled the Barings Bank fraud. The board, risk management, compliance, and audit functions must be genuinely independent from portfolio management."),
            _mcq("A board Investment Committee member who is also the company's CEO approves all significant portfolio decisions, effectively controlling both management and board oversight of investment management. This governance structure MOST DIRECTLY creates which risk?",
                 ["Regulatory compliance risk under the Investment Advisers Act",
                  "A conflict of interest where management accountability cannot be independent — the same person cannot effectively oversee their own decisions",
                  "GIPS compliance risk for performance reporting",
                  "Custody risk for client securities"],
                 1,
                 "When the CEO sits on (or controls) the board committee that oversees management, the accountability structure collapses — the board cannot independently challenge, question, or hold accountable someone who is simultaneously part of the board oversight function. Effective governance requires board members who are genuinely independent from management so they can ask hard questions and make decisions that may be uncomfortable for management."),
            _mcq("An insurance company's risk management team identifies that a portfolio manager has exceeded the single-issuer concentration limit. The risk manager reports to the CIO (who is also the portfolio manager's direct supervisor). The CIO tells the risk manager to 'not escalate this time' since the position is performing well. What should the risk manager do?",
                 ["Follow the CIO's instruction since the CIO has authority over investment decisions",
                  "Document the violation, escalate to the CCO and the Board Risk Committee directly, per the escalation protocol that bypasses the CIO when the CIO is involved in the issue",
                  "Wait until the next quarterly risk report to document the violation",
                  "Delete the record of the violation since the CIO approved the override"],
                 1,
                 "Risk management must have escalation authority that bypasses portfolio management when portfolio management is the subject of concern. If the CIO can override risk escalations, the independence of risk management is illusory. The escalation protocol for violations involving senior investment personnel must go directly to the CCO and Board Risk Committee. Documenting and escalating — despite CIO instruction not to — is the risk manager's governance obligation."),
            _mcq("Which of the following BEST describes the appropriate relationship between the board and portfolio management in investment governance?",
                 ["The board makes all individual investment decisions; portfolio managers implement them",
                  "Portfolio managers make all decisions independently; the board only reviews results annually",
                  "The board sets strategy and policy, oversees risk and performance, holds management accountable; portfolio managers make daily investment decisions within board-approved IPS bounds",
                  "The board and portfolio management rotate investment decision responsibility quarterly"],
                 2,
                 "The correct governance model separates strategy-setting and oversight (board) from operational execution (management). The board approves the IPS (the rules), oversees risk and performance (accountability), and holds the CIO accountable — but does not make individual portfolio decisions. Portfolio managers operate within the IPS bounds the board established. This layered model enables professional investment management while maintaining governance accountability."),
            _mcq("An insurance company's investment governance structure has the CRO reporting to the CIO. Why is this a concern?",
                 ["The CRO and CIO have overlapping technical expertise creating redundancy",
                  "Risk management should be independent from investment management so the CRO can escalate concerns to the board without CIO approval",
                  "Risk management and investment management should be combined for efficiency",
                  "CROs should report to the CFO for accounting accuracy"],
                 1,
                 "When the CRO reports to the CIO, the investment team controls oversight of its own risk-taking. A portfolio manager who exceeds risk limits can pressure the CRO to delay escalation. The CRO must report to the Board Risk Committee or CEO independently of investment management to provide unfiltered risk information to the board."),

            _scenario(
                "A mutual insurance company's investment governance review identifies two structural deficiencies: (1) The Chief Investment Officer also chairs the Management Investment Committee AND sits on the Board Finance Committee (which oversees the CIO's work); (2) The compliance team reports to the CIO rather than to the Board Audit Committee. The governance consultant recommends redesigning both structures. The CIO argues that the current structure is 'more efficient' since fewer layers of approval are needed.",
                "Is the governance consultant's recommendation correct, and why does 'efficiency' not justify the current structure?",
                [("The CIO is correct — fewer approval layers create faster decision-making, which is more important than governance formality in competitive markets", False,
                  "Speed of decision-making is a valid operational goal, but not at the expense of governance independence. The oversight that catches errors and prevents fraud is more valuable than the marginal speed gained by removing checks. Barings Bank's collapse demonstrated what happens when speed-over-governance becomes institutional policy."),
                 ("The governance consultant is correct — both deficiencies eliminate independent oversight: the CIO cannot effectively oversee themselves, and compliance reporting to the CIO removes the independence that makes compliance valuable", True,
                  "Correct. Deficiency 1: the CIO sitting on the board committee that oversees the CIO's work is a circular accountability failure — there is no independent board oversight. Deficiency 2: compliance reporting to the CIO creates a reporting structure where the person being monitored controls the monitor. Both deficiencies must be corrected: the CIO should not be on the Board Finance Committee; compliance must report to the Board Audit Committee independently."),
                 ("Only Deficiency 2 matters — CIOs sitting on board committees is standard industry practice and raises no governance concern", False,
                  "Both deficiencies are material governance failures. CIOs who sit on the board committees that oversee them eliminate independent board accountability — a fundamental governance requirement. Many regulators and governance best practices explicitly prohibit or discourage management executives from serving on the committees that evaluate them.")]
            ),
        ]
    )

    # Concept 4: Internal Audits, Compliance Reviews, and Building an Ethical Culture
    c4 = _concept(
        m2_id, 2,
        "Internal Audits, Compliance Reviews, and Building an Ethical Investment Culture",
        "Describe the role and process of internal audits for investment operations, explain the elements of an effective annual compliance review, and discuss how institutional leaders build and sustain an ethical investment culture.",
        "The final layer of investment governance is ongoing audit and review — periodic independent assessments that confirm the investment operation is functioning as designed, controls are operating effectively, and no systemic issues are hiding beneath the surface. Internal audit provides independent operational assurance; the annual compliance review by the CCO confirms regulatory and policy adherence; and building an ethical culture creates the behavioral environment where individual employees choose ethical conduct because they believe in it, not just because they fear punishment. Culture is the governance control that works when no one is watching.",
        "Vanguard's investment operations internal audit program covers: (1) Annual audit scope — trading operations, portfolio compliance, valuation processes, counterparty exposures, and operational risk. Each area audited by a team with no management responsibility for the area being audited; (2) Audit findings — categorized as Critical (material control failure requiring immediate remediation), Significant (important control gap, 30-day remediation), or Advisory (best practice enhancement). In 2023, no Critical findings; 4 Significant findings (remediation completed within 30 days); 12 Advisory findings; (3) Annual compliance review — CCO presents to the Board Audit Committee: IPS compliance rate (target 99.9%), regulatory violations (zero for securities law, 3 minor IPS administrative breaches corrected within 5 days), training completion (98% of required employees), personal trading surveillance results; (4) Culture: Vanguard's CEO annually signs the ethics code renewal letter to all employees; ethics is the first item in every annual performance review; employees who identify and report compliance concerns receive formal recognition — not just protection.",
        [
            "Internal audit: independent from both portfolio management AND compliance — audits the compliance function itself as well as investment operations.",
            "Annual compliance review: CCO's formal assessment and certification to the board of the overall compliance program effectiveness.",
            "Ethical culture: tone from the top, consistent enforcement, recognition of ethical behavior, clear escalation paths — not just training programs.",
            "Remediation tracking: all audit findings must have documented remediation plans with owners, timelines, and verification.",
        ],
        [
            "Thinking internal audit and compliance are the same function — internal audit is independent of compliance and audits compliance itself; they are separate governance layers.",
            "Believing culture is built through training programs — training creates awareness; culture is built through leadership behavior, consistent enforcement, and recognition of ethical conduct.",
            "Assuming no audit findings means no problems — absence of findings may reflect audit scope limitations or audit team capability gaps; it is not a guarantee of no control weaknesses.",
        ],
        lessons=[
            _intro("Audit, Review, and Culture: The Final Governance Layer",
                   "Controls are only as good as the verification that they're working. Internal audit, compliance reviews, and ethical culture are the mechanisms that confirm the governance structure is functioning — not just documented on paper."),
            _teach("Internal Audit of Investment Operations",
                   "Internal audit provides independent assurance that investment operations, controls, and governance structures are functioning as designed. Key characteristics: (1) Independence — the internal audit team reports to the Board Audit Committee (not to management), ensuring they can report findings without management interference; (2) Risk-based scope — audit plans focus on highest-risk areas: trading controls, valuation processes, counterparty exposures, compliance system effectiveness, and personal trading surveillance; (3) Audit process: planning (determine scope, assess inherent risks), fieldwork (test controls, review transactions, interview staff), reporting (document findings with severity ratings, root causes, management responses, remediation plans), follow-up (verify remediation completion); (4) Finding ratings: Critical (immediate control failure or policy violation), Significant (material gap requiring prompt remediation), Advisory (enhancement opportunity). Internal audit of investment operations is distinct from financial statement audit — it focuses on operational controls and process quality, not financial statement accuracy.",
                   ["Internal audit reports to Board Audit Committee — not to management.",
                    "Risk-based scope: focus audit resources on highest-inherent-risk areas.",
                    "Critical findings: immediate escalation to board, same-day remediation initiation.",
                    "Follow-up verification: audit confirms remediation completed — not just management's assertion."]),
            _teach("Annual Compliance Review and Building Ethical Culture",
                   "Annual compliance review (required under SEC Investment Advisers Act): the CCO conducts a comprehensive annual review of the compliance program and certifies findings to the board. Elements: (1) IPS compliance — rate of adherence to all IPS limits over the year; exception count, root causes, remediation; (2) Regulatory compliance — securities law violations (if any), regulatory exam results, regulatory correspondence; (3) Training completion — % of required employees who completed annual ethics and compliance training; (4) Policy effectiveness — review of all compliance policies for continued appropriateness; (5) Surveillance effectiveness — assessment of whether automated monitoring systems are catching violations. Building an ethical culture: culture is the behavioral environment in which employees make decisions. Elements of strong ethical culture: (1) Tone from the top — senior leadership demonstrates ethical behavior, not just communicates it; (2) Consistent enforcement — rules are enforced equally regardless of seniority or revenue; (3) Psychological safety — employees feel safe raising concerns without fear of retaliation; (4) Recognition — employees who report concerns, prevent violations, or model ethical behavior are formally recognized; (5) Ethical decision-making framework — employees have a clear framework for resolving ethical dilemmas when rules don't cover the situation.",
                   ["CCO annual review: comprehensive program assessment and board certification.",
                    "Tone from the top: leaders who cut ethical corners destroy more culture than any training program builds.",
                    "Consistent enforcement: selective enforcement of compliance creates a two-tier moral hazard.",
                    "Psychological safety: without it, violations go unreported even when employees see them."]),
            _example("Vanguard's Ethical Culture Program",
                     "Vanguard's approach to building ethical culture goes beyond compliance training. Annual ethics commitment: every employee — from CEO to entry-level — signs an annual ethics commitment letter acknowledging their personal responsibility for ethical conduct. No employee is exempt. Performance reviews: the first section of every Vanguard employee's annual review covers ethical conduct and compliance — not performance. A high-performing employee who cuts ethical corners cannot receive an 'exceeds expectations' overall rating. Recognition: Vanguard's internal awards program includes an 'Ethical Courage' award for employees who identify and report concerns, prevent violations, or navigate difficult ethical situations correctly. In 2022, 14 employees received this recognition — 6 for identifying compliance concerns, 4 for refusing to execute requests that would have violated IPS limits, 4 for reporting management behavior that they believed created ethical risks. The recognition makes ethical behavior visible and aspirational, not just obligatory.",
                     "Ethical culture is not built by compliance programs — it is built by making ethical behavior the path of least resistance and ethical courage the path of most recognition."),
            _flash("What is the key difference between internal audit and the compliance function in investment governance?",
                   "Compliance monitors ongoing adherence to policies and regulations (prevention and detection). Internal audit independently assesses whether the compliance program itself is effective, and audits investment operations, trading controls, and governance structures. Internal audit reports to the Board Audit Committee, not to management, and can audit the compliance team itself. They are separate governance layers: compliance monitors operations; internal audit monitors whether the monitoring is working."),
            _mcq("An internal audit team is reviewing trading operations and reports its findings to the Chief Investment Officer, who then decides which findings to share with the Board Audit Committee. What governance failure does this create?",
                 ["A GIPS compliance failure since audit findings must be published publicly",
                  "An independence failure — internal audit must report directly to the Board Audit Committee without management filtering, to prevent management from suppressing unfavorable findings",
                  "A regulatory violation under the Investment Company Act of 1940",
                  "A NAIC solvency concern since audit findings affect admitted assets"],
                 1,
                 "Internal audit's value depends entirely on its independence from the management functions it audits. If management controls what the board sees from internal audit, management can suppress findings that reflect poorly on them. Internal audit must report directly to the Board Audit Committee — bypassing all management layers — to maintain the independence that makes its findings credible and actionable."),
            _mcq("During an annual compliance review, the CCO finds that 15% of required employees did not complete the mandatory annual ethics training. What is the MOST appropriate response?",
                 ["Waive the requirement for the non-compliant employees since training participation rates are not meaningful indicators of ethical behavior",
                  "Document the training gap, identify root causes (scheduling conflicts, system access issues), require immediate completion with verification, and report to the board with a remediation plan",
                  "Terminate all non-compliant employees immediately since ethics training is a fundamental requirement",
                  "Reduce the training requirement so that completion rates improve"],
                 1,
                 "Training non-compliance requires documentation, root cause analysis, and remediation — not waiver or termination. 15% non-completion is a material gap that must be: investigated (were there legitimate access barriers?), remediated (all employees must complete training with verification), and reported to the board (with the root cause and remediation plan). Waiving requirements or reducing standards defeats the purpose; immediate termination for a training gap is disproportionate."),
            _mcq("Which element of ethical culture is MOST important for encouraging employees to report observed violations?",
                 ["Annual ethics training that covers all prohibited behaviors comprehensively",
                  "A detailed compliance manual with written policies covering every possible situation",
                  "Psychological safety — a culture where employees believe reporting concerns is valued and will not result in retaliation",
                  "A compliance surveillance system that automatically detects all violations"],
                 2,
                 "Technical controls and training increase awareness of what is prohibited, but they don't motivate employees to report what they observe. Psychological safety — the genuine belief that reporting concerns is safe and valued — is the behavioral prerequisite for effective whistleblowing. If employees believe reporting will harm their career (even without explicit retaliation), they stay silent. Building psychological safety requires leadership behavior (not just policies): leaders must visibly protect and recognize reporters, not just promise protection in writing."),
            _mcq("An investment operations internal audit finds a 'Significant' control gap: the trading system allows the same portfolio manager to both initiate and approve their own trades without a second approval. What is the MOST appropriate remediation?",
                 ["Document the finding and schedule remediation in the next annual technology upgrade cycle (12-18 months)",
                  "Require a second person (separate from the initiating portfolio manager) to approve all trades before execution, with system enforcement — remediate within 30 days",
                  "Retrain the portfolio managers on the importance of proper trade initiation",
                  "Transfer the approval function to the compliance team permanently"],
                 1,
                 "A Significant audit finding requires prompt remediation — typically within 30 days. The control gap (one person both initiating and approving their own trades) violates the fundamental segregation of duties principle and creates the same risk that enabled the Barings Bank fraud. Remediation must be: (1) systematic — a system control requiring second approval, not just a policy reminder; (2) prompt — 30 days, not 12-18 months; (3) verified — audit follows up to confirm the control is implemented. Training is insufficient; system enforcement is required."),
            _mcq("A Significant internal audit finding in investment operations requires which remediation approach?",
                 ["Immediate escalation to law enforcement since significant findings indicate criminal violations",
                  "Documentation only in the next annual report with no immediate action required",
                  "A written remediation plan with a designated owner and 30-day completion deadline with audit follow-up verification",
                  "Automatic termination of the employee responsible for the control gap"],
                 2,
                 "Significant audit findings require prompt, documented remediation — typically within 30 days. The plan must specify the control gap, corrective action, responsible person, and target date, with audit verification of completion. Significant findings are important control gaps requiring urgent attention but are not automatically criminal matters or grounds for termination."),

            _scenario(
                "Two institutional investment firms have the following audit and culture profiles. Firm A: Zero audit findings in 3 consecutive years; CCO reports to the CIO; no whistleblower reports received in 3 years; senior management does not participate in ethics training ('that's for junior staff'). Firm B: 8 advisory findings and 2 significant findings in 3 years (all remediated); CCO reports to Board Audit Committee; 12 whistleblower reports in 3 years (all investigated, 3 led to corrective actions); CEO and all senior management complete ethics training annually.",
                "Which firm has the STRONGER governance and ethical culture, and why?",
                [("Firm A — zero audit findings and no whistleblower reports indicate a clean, well-controlled operation", False,
                  "Zero findings often indicate audit scope limitations or cultural suppression of reporting, not absence of problems. No whistleblower reports in 3 years at a large firm almost certainly means employees don't feel safe reporting — not that no issues exist. Firm A's governance structure (CCO reporting to CIO) and leadership non-participation signal a compliance culture that prioritizes appearances over substance."),
                 ("Firm B — active audit findings with remediation, CCO independence, genuine whistleblower use, and leadership participation in ethics training all signal a healthy governance culture that identifies and addresses issues rather than suppressing them", True,
                  "Correct. Active audit findings that are promptly remediated demonstrate a system that WORKS — it finds things and fixes them. Whistleblower reports that are investigated and lead to corrective action demonstrate employees trust the system. CCO independence from management means compliance is genuine, not performative. Leadership participation in ethics training sets the 'tone from the top.' Firm B is the better-governed organization."),
                 ("Neither firm demonstrates strong governance — both have structural deficiencies that make meaningful comparison impossible", False,
                  "Firm B clearly demonstrates stronger governance on every dimension that matters: CCO independence, active audit findings (showing the audit works), genuine whistleblower culture, and leadership participation. The comparison is clear — Firm B's visible operational governance is far stronger than Firm A's apparent cleanliness that likely reflects suppression rather than substance.")]
            ),
        ]
    )

    m2["concepts"] = [c3, c4]
    ch["modules"] = [m1, m2]
    return ch


def _build_ch12(course_id):
    ch_id = _id()
    ch = {
        "id": ch_id, "course_id": course_id, "order": 12,
        "title": "Insurance Investment Products and Advanced Regulatory Frameworks",
        "description": "Deep dive into insurance-specific investment products (GICs, funding agreements, separate accounts vs. general accounts, FHLB borrowings), ERISA pension fund regulation, Dodd-Frank OTC derivatives rules, and securities financing (repo and securities lending).",
    }

    # ── Module 1: Insurance-Specific Investment Products ──────────────────────
    m1_id = _id()
    m1 = {"id": m1_id, "chapter_id": ch_id, "order": 1,
          "title": "Insurance-Specific Investment Products"}

    # Concept 1: GICs, Funding Agreements, and Guaranteed Products
    c1 = _concept(
        m1_id, 1,
        "Guaranteed Investment Contracts, Funding Agreements, and Institutional Guaranteed Products",
        "Describe Guaranteed Investment Contracts (GICs) and funding agreements — how they are structured, how they are used by institutional investors, and how they create specific asset-liability management obligations for the issuing insurance company.",
        "Guaranteed Investment Contracts (GICs) and funding agreements are among the most distinctive institutional investment products issued exclusively by life insurance companies. A GIC is a contract in which an insurance company guarantees to return the depositor's principal plus a specified rate of interest over a defined period. GICs are primarily sold to pension plans and 401(k) plans as a stable-value option. Funding agreements are structurally similar but sold to institutional investors including money market funds, municipalities, and securities vehicles. These products create significant asset-liability obligations for the issuing insurer — the insurer must invest the received premiums at yields that exceed the guaranteed crediting rate while covering expenses and profits.",
        "MetLife's Stable Value Products division manages $85 billion in GIC and funding agreement liabilities. Structure of a typical GIC issued to a corporate 401(k) plan: MetLife receives $500M, guarantees return of $500M plus 4.8% annual interest over 5 years. Total maturity value: $500M × (1.048)^5 = $631M. MetLife's obligation: invest the $500M to earn at least 4.8% + expenses (approximately 0.35%) + profit margin (approximately 0.50%) = target net return of 5.65% on invested assets. Asset selection: MetLife invests GIC proceeds in a dedicated portfolio of investment-grade bonds with average duration matching the 5-year GIC term — primarily corporate bonds (75%), commercial mortgage loans (15%), and agency MBS (10%). The $131M guaranteed profit exists only if the investment portfolio earns above 4.8%. If credit losses hit the portfolio, MetLife's surplus absorbs them — the depositor is fully guaranteed regardless of investment performance. This is the fundamental insurance value proposition: transferring investment risk to the insurer's balance sheet.",
        [
            "GIC: insurance company guarantees return of principal plus specified interest rate; depositor (pension plan) bears no investment risk.",
            "Funding agreement: structurally similar to GIC but sold to institutional investors (not pension plans); often used to back Funding Agreement-Backed Securities (FABS).",
            "Spread: the difference between the insurer's investment yield and the guaranteed crediting rate; net of expenses and losses, this is the insurer's profit.",
            "FABS (Funding Agreement-Backed Securities): funding agreements packaged into securities sold to money market funds seeking AAA-rated short-term instruments.",
        ],
        [
            "Thinking GICs are risk-free for the issuer — the issuer bears all investment risk. If the investment portfolio underperforms, the insurer absorbs the loss while still paying the guaranteed rate.",
            "Confusing GICs with bank CDs — both guarantee principal and interest, but GICs are insurance products backed by the insurer's general account, not FDIC-insured.",
            "Assuming all GICs are the same — traditional GICs (bullet, immediate participation), synthetic GICs (wrap-contract around external assets), separate account GICs all have different risk profiles.",
        ],
        lessons=[
            _intro("GICs and Funding Agreements: Insurance Companies as Investment Guarantors",
                   "Insurance companies don't just invest money — they also manufacture investment products. GICs and funding agreements are contracts that promise a guaranteed return, transferring investment risk to the insurer. Understanding these products is essential LOMA 357 knowledge."),
            _teach("GIC Structure, Types, and the Crediting Rate Spread",
                   "A Guaranteed Investment Contract has three core elements: (1) Principal — the deposit placed by the pension plan or institutional investor; (2) Crediting rate — the guaranteed annual interest rate the insurer commits to pay over the contract term; (3) Term — typically 1 to 10 years; most 3-5 years. GIC types: (a) Bullet GIC — single lump-sum deposit, single maturity payment (most common for pension plans). No withdrawals permitted before maturity except for specific benefit payments; (b) Window GIC — multiple deposits accepted during a contribution window period, then closes. Useful for 401(k) plans with ongoing contributions; (c) Immediate Participation Guarantee (IPG) — the depositor participates in the actual investment performance rather than a fixed guaranteed rate; hybrid product; (d) Synthetic GIC — the pension plan owns the underlying assets but buys a 'wrap contract' from the insurer that guarantees book value even if market values decline. The insurer provides the guarantee without actually holding the assets. The crediting rate spread: insurer's investment return MINUS crediting rate MINUS expenses = profit margin. Typical spread: 30-80 basis points. If spreads compress (investment yields fall, competition forces higher crediting rates), profitability collapses.",
                   ["Bullet GIC: single deposit, fixed rate, fixed term — simplest structure.",
                    "Synthetic GIC: assets stay with pension plan; insurer provides book value wrap guarantee only.",
                    "Crediting rate spread = investment yield - crediting rate - expenses - losses.",
                    "Window GIC: accepts new contributions during defined period — useful for ongoing 401(k) contributions."]),
            _teach("Funding Agreements, FABS, and ALM Obligations",
                   "Funding agreements are contracts issued by insurance companies to institutional investors (not pension plans). They are not subject to ERISA and offer more flexibility in structure. Key uses: (1) Funding Agreement-Backed Securities (FABS) — an insurance company issues a funding agreement to a special purpose vehicle (SPV); the SPV issues notes backed by the funding agreement. Money market funds buy the notes (short-term, AAA-rated); the insurer receives long-term funding at money market rates. FABS allow insurers to borrow at low short-term rates and invest in higher-yielding long-term assets; (2) Municipal issuers — cities and counties invest bond proceeds in funding agreements during construction periods before spending; (3) Securities vehicles — asset managers use funding agreements for stable NAV products. ALM obligations: GICs and funding agreements create predictable liability cash flows — on maturity, the insurer must pay full principal plus accrued interest. The insurer must hold assets sufficient to meet these obligations under all market scenarios. Cash-flow matching and duration matching are critical for GIC-heavy portfolios. FHLB (Federal Home Loan Bank) borrowings: insurance companies can borrow from FHLB using their mortgage loan portfolios as collateral — providing additional liquidity for GIC and funding agreement portfolios when needed.",
                   ["FABS: funding agreement issued to SPV → SPV issues notes → money market funds buy notes.",
                    "ALM for GICs: assets must exactly match the guaranteed liability cash flows.",
                    "FHLB membership: available to life insurance companies; provides collateralized borrowing at FHLB advance rates.",
                    "FHLB advances: insurance companies pledge mortgage loans and agency MBS as collateral for FHLB borrowings."]),
            _example("Principal Financial Group's GIC Portfolio Management",
                     "Principal Financial Group manages $45 billion in GIC liabilities for corporate pension plans. Their GIC portfolio ALM process: Step 1 — receive new GIC deposit ($100M, 5-year term, 4.5% guaranteed rate). Step 2 — calculate required investment return: 4.5% crediting rate + 0.30% expenses + 0.40% profit target = 5.20% required gross return. Step 3 — build a dedicated asset portfolio with duration matching the 5-year GIC: 60% 5-7 year BBB corporate bonds (yield 5.8%), 25% 5-year commercial mortgage loans (yield 5.6%), 15% agency MBS (yield 5.1%). Blended portfolio yield: 5.65%. Expected spread: 5.65% - 4.5% = 1.15% gross, minus 0.30% expenses = 0.85% net spread. Step 4 — monitor quarterly: if any bonds are downgraded or default, replace with comparable-yield securities. The $40.5M potential profit over 5 years is protected only by maintaining portfolio yield and credit quality throughout the term.",
                     "GIC management is ALM in its purest form: every dollar of liability has a matching dollar of asset earning a spread. The insurer's profit is the difference — and the insurer bears all risk of earning less than promised."),
            _flash("What is a 'synthetic GIC' and how does it differ from a traditional (bullet) GIC?",
                   "A synthetic GIC separates asset ownership from the guarantee. In a traditional GIC, the insurer owns the assets and provides the guarantee. In a synthetic GIC, the pension plan owns the underlying assets (bonds, bond funds) directly. The insurer provides only a 'wrap contract' — a guarantee to pay book value if the market value falls below book value. The insurer earns a wrap fee (typically 5-15 bps) without taking on asset risk. This became popular post-2008 as pension plans wanted more transparency over the underlying assets."),
            _mcq("A pension plan deposits $200M with an insurance company under a 5-year bullet GIC at a 4.0% guaranteed crediting rate. If the insurance company's investment portfolio earns only 3.8% over the 5 years, what is the MOST LIKELY outcome?",
                 ["The pension plan's guaranteed return is reduced to reflect actual investment performance",
                  "The insurance company absorbs the 0.2% shortfall from its surplus, still paying the pension plan the full 4.0% guaranteed return",
                  "The GIC contract is voided and the pension plan receives only the principal back",
                  "The insurance company increases the crediting rate to compensate for low investment yields"],
                 1,
                 "The entire point of a GIC is the guarantee — the pension plan receives the promised crediting rate regardless of actual investment performance. If the insurer's portfolio earns less than the guaranteed rate (plus expenses and profit), the shortfall is absorbed by the insurer's surplus. This is the fundamental credit risk pension plans accept with GICs: they are unsecured obligations backed by the insurer's general account. If the insurer becomes insolvent, state guaranty associations provide limited protection."),
            _mcq("A Funding Agreement-Backed Security (FABS) is BEST described as:",
                 ["A life insurance policy backed by bonds in the insurer's general account",
                  "A note issued by a special purpose vehicle, backed by a funding agreement between the SPV and an insurance company, purchased by money market funds",
                  "A government-guaranteed bond issued by insurance companies to fund policyholder claims",
                  "A hybrid security combining equity and fixed income features issued by life insurers"],
                 1,
                 "FABS structure: (1) Insurance company issues a funding agreement to an SPV; (2) SPV issues short-term, floating-rate notes backed by the funding agreement; (3) Money market funds buy the notes for their AAA rating and short duration. This allows the insurer to access low-cost short-term funding (money market rates) while investing in higher-yielding long-term assets — earning a structural carry spread. The SPV is bankruptcy remote, protecting money market investors."),
            _mcq("Which type of GIC is MOST appropriate for a 401(k) plan that receives continuous monthly contributions from employees?",
                 ["Bullet GIC — accepts a single lump-sum deposit and pays a fixed rate at maturity",
                  "Window GIC — accepts multiple deposits during a defined contribution period, then closes to new contributions",
                  "Immediate Participation Guarantee — passes actual investment returns to the depositor",
                  "Synthetic GIC — the plan owns assets while the insurer provides a book value guarantee"],
                 1,
                 "A Window GIC accepts new deposits during a defined period (e.g., one calendar year), making it perfectly suited for 401(k) plans with ongoing monthly employee contributions. After the window closes, the accumulated balance earns a fixed rate until maturity. Bullet GICs require a single lump-sum deposit — unsuitable for ongoing contributions. Synthetic GICs are more complex and require the plan to manage its own assets."),
            _mcq("Insurance companies borrow from Federal Home Loan Banks (FHLB) PRIMARILY to:",
                 ["Fund policyholder benefit payments directly using FHLB grants",
                  "Obtain low-cost collateralized funding using mortgage loans and agency MBS as collateral, supporting liquidity needs and spread enhancement",
                  "Comply with NAIC requirements to hold FHLB membership as a solvency buffer",
                  "Purchase FHLB stock as a required admitted asset investment"],
                 1,
                 "FHLB membership allows insurance companies to pledge eligible collateral (commercial mortgage loans, agency MBS, residential mortgage loans) in exchange for FHLB 'advances' — low-cost loans at rates below comparable Treasury bonds. Insurance companies use FHLB advances to: (1) fund GIC and funding agreement liabilities at lower cost; (2) manage ALM mismatches; (3) take advantage of the spread between FHLB advance rates and investment yields. The cost of FHLB membership (purchasing FHLB stock) is more than offset by the spread income."),
            _mcq("The crediting rate spread on a GIC is MOST directly affected by which two factors?",
                 ["The size of the GIC deposit and the term of the contract",
                  "The insurer's investment portfolio yield and the guaranteed crediting rate promised to the depositor",
                  "The regulatory capital charge for GIC liabilities and the insurer's credit rating",
                  "The number of GIC contracts issued and the insurer's expense ratio"],
                 1,
                 "The crediting rate spread = Investment portfolio yield - Guaranteed crediting rate - Expenses - Credit losses. The two primary drivers are: (1) the investment yield the insurer earns on the invested GIC proceeds; and (2) the crediting rate the insurer promised to pay. A falling investment environment compresses spreads (yields fall while existing crediting rate commitments remain). A competitive market compresses spreads (competing insurers bid up crediting rates). Managing the spread is the central profitability challenge of the GIC business."),
            _scenario(
                "Ohio National Life issued $500M in 5-year bullet GICs to 12 pension plans at a 4.6% crediting rate in 2019. They invested the proceeds in a portfolio yielding 5.5%. In 2021, the pandemic caused credit losses of 0.6% on the portfolio, reducing the effective net yield to 4.9%. Ohio National's expense ratio is 0.40%. Three pension plans are demanding early withdrawal totaling $150M due to plan terminations. Ohio National has $25M in liquid assets; the remaining $475M is in illiquid bonds.",
                "What are the MOST SERIOUS risks Ohio National faces, and what tools can they use to manage them?",
                [("Credit loss risk only — the 0.6% loss compressed spreads; Ohio National should sell bonds immediately to realize losses and reinvest at higher yields", False,
                  "Selling bonds to 'realize losses' doesn't fix the problem — it crystallizes the losses and likely generates additional transaction costs. The more serious risk here is the liquidity mismatch: $150M in early withdrawal demands against only $25M in liquid assets."),
                 ("Liquidity risk (early withdrawal demands exceed liquid assets) and spread compression risk (net spread is now 4.9% - 4.6% - 0.4% = -0.1%, meaning Ohio National is losing money on this block). Tools: FHLB borrowings to fund the $150M withdrawal; portfolio restructuring to reduce credit risk", True,
                  "Correct. Two serious risks: (1) Liquidity — $150M withdrawals but only $25M liquid; Ohio National must either sell bonds (at potential losses) or borrow via FHLB advances using the bond portfolio as collateral. FHLB advances can fund the $150M withdrawal without forced bond sales; (2) Spread compression — the 0.6% credit loss made the net spread negative (-0.1%). Corrective action: replace defaulted/downgraded bonds with higher-yield alternatives, and negotiate with remaining pension plans."),
                 ("No significant risk — the GIC contracts specify no early withdrawal rights, so Ohio National can simply deny all three pension plans their withdrawal requests", False,
                  "Most GIC contracts do include provisions for withdrawals related to plan termination, hardship, or benefit payments — even bullet GICs. Refusing legitimate plan termination withdrawals creates legal and regulatory risk. Ohio National must manage the liquidity event even if the contracts provide some protection.")]
            ),
        ]
    )

    # Concept 2: Separate Account vs. General Account Investment Management
    c2 = _concept(
        m1_id, 2,
        "Separate Account vs. General Account: The Fundamental Distinction in Life Insurance Investing",
        "Explain the fundamental distinction between a life insurance company's general account and separate accounts, describe which products are supported by each, and explain the different investment management obligations, regulatory treatment, and policyholder protection implications.",
        "The most important structural distinction in life insurance investing is between the general account and separate accounts. The general account is the insurer's core investment portfolio — it supports all traditional (fixed) insurance products and is subject to NAIC investment regulations, RBC requirements, and statutory accounting. Separate accounts are legally segregated pools of assets that support variable products (variable annuities, variable life insurance). Separate account assets are NOT part of the insurer's general account; they are protected from the insurer's general creditors. This distinction fundamentally changes the investment mandate, regulatory framework, regulatory capital treatment, and policyholder risk profile for each type of account.",
        "Nationwide Financial manages two distinct investment operations under one corporate umbrella. General account ($65B): invests in investment-grade bonds, commercial mortgage loans, and limited equities; governed by Ohio insurance law (NAIC model); RBC required; all investment risk borne by Nationwide; supports fixed annuities, term life, and whole life. Separate accounts ($180B): 47 separate accounts, each registered under the Investment Company Act of 1940 as an investment company; governed by SEC rules; no RBC required (policyholders bear investment risk); each separate account is invested in mutual fund-like sub-accounts (equity, bond, international, balanced); registered investment advisers manage each sub-account. Policyholder experience: fixed annuity holder earns a guaranteed crediting rate regardless of investment performance (general account). Variable annuity holder's account value rises and falls with their chosen sub-accounts (separate account) — policyholder bears market risk but cannot lose principal to Nationwide's insolvency because the assets are segregated.",
        [
            "General account: insurer owns assets; insurer bears investment risk; supports traditional/fixed products; subject to NAIC/RBC; statutory accounting (amortized cost for bonds).",
            "Separate account: policyholder's assets legally segregated from insurer's general creditors; policyholder bears investment risk; supports variable products; SEC-regulated; fair value accounting.",
            "Investment Company Act: separate accounts offering variable products must register as investment companies with the SEC — making life insurers subject to SEC securities regulation.",
            "Variable products: variable annuities and variable life insurance; contract value fluctuates with separate account investment performance; policyholder selects sub-accounts (growth, income, balanced).",
        ],
        [
            "Thinking separate account assets can be seized by the insurer's creditors — they cannot. Separate account assets are legally protected from the insurer's general account obligations.",
            "Assuming the same investment regulations govern both accounts — general account is NAIC/state-regulated; separate accounts are SEC-regulated under the Investment Company Act.",
            "Confusing policyholder risk: general account policyholders bear INSURER credit risk (if insurer fails); separate account policyholders bear MARKET risk (investment performance) but not insurer credit risk on the segregated assets.",
        ],
        lessons=[
            _intro("Two Investment Worlds Within One Insurance Company",
                   "A life insurance company is not a single investment portfolio. It runs at least two fundamentally different investment operations — one that guarantees returns (general account) and one that passes market performance directly to policyholders (separate accounts). The distinction affects everything: regulation, accounting, risk, and policyholder protection."),
            _teach("The General Account: Traditional Investment Management",
                   "The general account is the insurer's primary investment portfolio — it has supported life insurance products since the 19th century. Key characteristics: (1) Asset ownership — the insurer owns all general account assets; policyholders have contractual claims (guaranteed interest, cash values, death benefits) but do not own specific assets; (2) Investment risk — the insurer bears all investment risk. If the portfolio loses value, the insurer absorbs the loss while continuing to pay guaranteed benefits; (3) Products supported — traditional whole life, universal life, fixed annuities, term life, GICs, and all non-variable products; (4) Regulation — NAIC state insurance regulation; NAIC investment limitations (common stock ≤20%, below-IG bonds ≤5%); RBC C-1 asset risk charges; statutory accounting (bonds at amortized cost); (5) Policyholder protection — general account policyholders are general creditors of the insurer. If the insurer becomes insolvent, they receive assets through the insolvency process; state guaranty associations provide limited protection (typically up to $250K-$300K).",
                   ["General account: insurer bears all risk; policyholders guaranteed fixed returns.",
                    "Insolvency risk: general account policyholders are general creditors — exposed to insurer failure.",
                    "State guaranty associations: protect general account policyholders up to state-set limits ($250-300K).",
                    "Investment mandate: conservative — NAIC limits, RBC capital charges, NAIC designations."]),
            _teach("Separate Accounts: Variable Products and SEC Regulation",
                   "Separate accounts were created by states in the 1950s-1960s to allow life insurers to offer equity-linked products. Key characteristics: (1) Legal segregation — separate account assets are legally protected from the insurer's general account creditors. Even if the insurer becomes insolvent, separate account assets belong to the variable product policyholders, not to general creditors; (2) Investment risk transfer — the policyholder bears market risk. If the selected sub-accounts decline, the policyholder's contract value declines accordingly. The insurer does not guarantee investment performance (though some variable products include guaranteed minimum withdrawal benefit riders that are backed by the general account); (3) Products — variable annuities (VA) and variable life insurance (VLI). Contract value = number of accumulation units × current unit value. Unit value changes daily based on sub-account performance; (4) SEC regulation — each separate account is registered with the SEC as an investment company under the Investment Company Act of 1940. The insurer files prospectuses for each separate account, has independent board requirements, and follows SEC disclosure rules; (5) Sub-accounts — each separate account contains multiple sub-accounts (similar to mutual funds) that policyholders select based on their risk tolerance: equity sub-accounts, bond sub-accounts, international sub-accounts, balanced sub-accounts.",
                   ["Legal segregation: separate account assets are ring-fenced — insurer's creditors cannot reach them.",
                    "Policyholder bears market risk: contract value rises and falls with sub-account performance.",
                    "Investment Company Act: separate accounts registered as investment companies; SEC regulated.",
                    "Sub-accounts: individual investment options within the separate account — policyholder selects and switches."]),
            _example("Nationwide's Dual Investment Operations",
                     "Nationwide Financial's Q2 2023 investor presentation illustrated the dual structure: General Account ($65B): Allocation — 70% investment-grade bonds, 15% commercial mortgage loans, 7% government bonds, 5% equities, 3% alternatives. Investment yield: 5.1%. Return on required capital: 18%. Accounting: bonds at amortized cost — rising rates in 2022 created no statutory surplus impact. Key products: fixed index annuities, whole life, term life. Separate Accounts ($180B): 47 sub-accounts ranging from S&P 500 index (40% of assets) to international equity, intermediate bond, and money market. Investment performance Q2 2023: equity sub-accounts +8.2%, bond sub-accounts +1.1%. No RBC required. Accounting: mark-to-market daily. Key products: variable annuities with optional GMWB riders. The GMWB rider is the only element where the general account backs the variable product — Nationwide guarantees minimum income even if sub-account values fall to zero; this guarantee is general account obligation backed by dedicated reserves.",
                     "The GMWB rider in variable annuities is the intersection of general account and separate account — the insurer takes back market risk through the guarantee while the policyholder retains upside participation."),
            _flash("Why are separate account assets protected from an insurer's general creditors even if the insurer becomes insolvent?",
                   "State insurance laws specifically provide that separate account assets are legally segregated from the insurer's general account. They are held exclusively for the benefit of variable product policyholders. In insolvency, the separate account assets are not available to pay the insurer's general creditors, bondholders, or employees — they remain with the variable product policyholders. This statutory protection is the legal foundation of the variable product structure, distinguishing it from bank deposits or general account insurance products."),
            _mcq("A fixed annuity policyholder and a variable annuity policyholder both have accounts with the same life insurance company. The insurer becomes insolvent. Which policyholder is MORE protected from the insolvency?",
                 ["The fixed annuity policyholder — general account products are always fully protected by state guaranty associations up to any amount",
                  "The variable annuity policyholder — separate account assets are legally protected from general creditors; the insolvency does not affect their sub-account values",
                  "Both are equally protected since both are insurance products subject to state regulation",
                  "Neither — all insurance assets become available to general creditors in an insolvency"],
                 1,
                 "The variable annuity policyholder's separate account assets are legally segregated from the insurer's general creditors. Their sub-account values (which represent market-value ownership of the sub-account portfolios) are unaffected by the insurer's insolvency. The fixed annuity policyholder is a general creditor — they rely on state guaranty association coverage (limited amounts) and the insolvency process. The separate account protection is a key structural advantage of variable products."),
            _mcq("A life insurance company's variable annuity separate account must register with which regulatory body?",
                 ["The National Association of Insurance Commissioners (NAIC)",
                  "The Federal Reserve Board as a bank holding company",
                  "The Securities and Exchange Commission (SEC) under the Investment Company Act of 1940",
                  "The Department of Labor under ERISA rules for retirement accounts"],
                 2,
                 "Variable annuity separate accounts that offer securities to the public must register with the SEC as investment companies under the Investment Company Act of 1940. This makes life insurers with variable products subject to SEC securities regulation — including prospectus filing requirements, independent board of directors, disclosure obligations, and anti-fraud provisions — in addition to state insurance regulation for the insurance components."),
            _mcq("Which of the following products is MOST LIKELY supported by an insurance company's separate account rather than its general account?",
                 ["A 5-year guaranteed annuity certificate promising 4.2% annual interest",
                  "A traditional whole life policy with a guaranteed cash value and death benefit",
                  "A variable universal life policy where the cash value fluctuates based on chosen sub-account performance",
                  "A Guaranteed Investment Contract issued to a corporate pension plan"],
                 2,
                 "Variable universal life insurance is a variable product — the policyholder selects sub-accounts and the cash value fluctuates with market performance. This is a separate account product. The guaranteed annuity certificate (GIC), traditional whole life, and guaranteed annuity all provide guaranteed returns — they are general account products where the insurer bears investment risk."),
            _mcq("An insurance company's general account portfolio reports bonds at amortized cost under statutory accounting. Interest rates rise 200 bps, causing bond market values to fall 15%. What is the impact on the insurer's STATUTORY SURPLUS?",
                 ["Statutory surplus falls by 15% of the bond portfolio value, same as GAAP",
                  "Statutory surplus is largely unaffected — bonds held at amortized cost do not show mark-to-market losses in statutory accounting",
                  "Statutory surplus doubles because rising rates increase future coupon income",
                  "Statutory surplus is immediately transferred to the separate account to protect policyholders"],
                 1,
                 "Under statutory accounting, general account bonds are typically carried at amortized cost — not fair market value. When interest rates rise and bond prices fall, the statutory balance sheet does not reflect the market value decline. The insurer's statutory surplus is therefore largely insulated from mark-to-market interest rate movements on the bond portfolio. This is a deliberate regulatory choice — it prevents 'paper losses' from rising rates from triggering unnecessary solvency concerns when the insurer intends to hold bonds to maturity."),
            _mcq("A variable annuity policyholder's contract value is $150,000 and they have selected three sub-accounts: 60% Large Cap Growth Fund, 30% International Fund, 10% Bond Fund. Markets decline and the total sub-account value falls to $110,000. What does the insurance company owe the policyholder (assuming no GMWB rider)?",
                 ["$150,000 — the insurer guarantees the original deposit value",
                  "$110,000 — the current market value of the chosen sub-accounts is the contract value; no guarantee applies to base contract value",
                  "$130,000 — the average of original value and current value",
                  "$150,000 less a 10% surrender charge, which must be refunded immediately"],
                 1,
                 "In a basic variable annuity (without a guaranteed minimum benefit rider), the contract value equals the current market value of the chosen sub-accounts. If markets fall, the contract value falls proportionally — this is the policyholder's market risk. The insurer makes no guarantee about contract value (only about the integrity of the separate account structure and product features). The policyholder in a variable annuity is essentially a mutual fund investor with an insurance wrapper."),
            _scenario(
                "Lincoln Financial is designing a new annuity product. Product Option A: Fixed Index Annuity — credits interest based on a formula tied to S&P 500 performance, with a floor of 0% (no loss) and a cap of 8% annual gain. Assets backing this product: general account. Product Option B: Variable Annuity — policyholder selects from 30 sub-accounts; contract value fluctuates daily with market performance; assets held in separate account.",
                "From an investment management and regulatory perspective, how do these two products differ?",
                [("Both products are managed identically — the S&P 500 exposure makes both subject to equity market regulation", False,
                  "The S&P 500 linkage in Option A is a crediting formula, not direct equity investment. The assets backing Option A are in the general account (bonds and options-based hedges) — no direct equity ownership. Option B's assets are direct equity investments in the separate account sub-funds."),
                 ("Option A (FIA): general account; Lincoln bears investment risk; assets managed under NAIC/state insurance regulation; no SEC registration required; statutory accounting. Option B (VA): separate account; policyholder bears investment risk; assets legally ring-fenced; SEC-regulated under Investment Company Act; daily mark-to-market", True,
                  "Correct. The structural difference is fundamental: FIA uses a general account with option-based hedging to deliver the index-linked crediting formula — Lincoln bears all investment risk and regulatory obligations are state insurance law. VA uses a legally separate account where policyholder bears market risk, assets cannot be reached by general creditors, and SEC securities regulation applies."),
                 ("Option B is riskier for Lincoln Financial than Option A because separate account assets are exposed to market volatility that could reduce Lincoln's profits", False,
                  "Opposite — separate account market risk is borne by the policyholder, not Lincoln. Lincoln's risk in Option B is primarily operational and reputational (if sub-accounts dramatically underperform), plus the risk of any guaranteed benefit riders attached to the variable product. The FIA (Option A) carries more balance sheet risk for Lincoln because Lincoln must guarantee the floor return from its own surplus.")]
            ),
        ]
    )

    m1["concepts"] = [c1, c2]

    # ── Module 2: Advanced Regulatory Frameworks ─────────────────────────────
    m2_id = _id()
    m2 = {"id": m2_id, "chapter_id": ch_id, "order": 2,
          "title": "Advanced Regulatory Frameworks: ERISA, Dodd-Frank, and Securities Financing"}

    # Concept 3: ERISA and Pension Fund Investment Regulation
    c3 = _concept(
        m2_id, 1,
        "ERISA and Pension Fund Investment Regulation",
        "Describe the Employee Retirement Income Security Act (ERISA) and its key investment obligations — the prudent investor rule, exclusive benefit rule, diversification requirement, prohibited transaction rules, and reporting obligations — for institutional investors managing pension assets.",
        "ERISA (Employee Retirement Income Security Act, 1974) is the federal law governing private pension and employee benefit plans in the United States. For investment management, ERISA establishes the highest legal standard of investment conduct — the prudent expert standard — and creates specific obligations that go beyond general fiduciary duty. Insurance companies managing pension plan assets (separate accounts, GICs, funding agreements held by ERISA plans) must comply with ERISA's rules even though they are insurance companies, not pension plans themselves. Violations of ERISA can result in personal liability for investment managers and plan trustees, mandatory restoration of plan losses, and civil/criminal penalties.",
        "TIAA-CREF manages $1.2 trillion in assets, a substantial portion in ERISA-qualified retirement plans. Their ERISA compliance infrastructure: (1) Designated Named Fiduciaries — TIAA's ERISA compliance team designates specific individuals as 'named fiduciaries' for each plan relationship, creating clear personal accountability; (2) Prudent Expert documentation — every investment decision for ERISA plan assets is documented with: the information considered, analysis performed, conclusion reached, and rationale. 'We bought this bond because it was in the plan's best interest' is not ERISA-compliant documentation. 'We purchased this BBB-rated 10-year bond based on our credit analysis showing Debt/EBITDA of 2.8x and interest coverage of 6.2x, consistent with the plan's IPS and within the approved asset class with an expected spread of 145 bps above Treasury' — is; (3) Prohibited Transaction monitoring — TIAA's legal team screens all potential transactions for prohibited parties (plan sponsor employees, parties in interest). In 2022, TIAA's pre-clearance system flagged and blocked 31 potential prohibited transactions before execution.",
        [
            "ERISA prudent expert standard: manage assets 'with the care, skill, prudence, and diligence under the circumstances then prevailing that a prudent person acting in a like capacity and familiar with such matters would use.'",
            "Exclusive benefit rule: assets must be invested solely for the exclusive benefit of plan participants and beneficiaries — manager's interests must never compete.",
            "Prohibited transactions: ERISA prohibits transactions between the plan and 'parties in interest' (plan sponsor, trustees, service providers) unless specific exemptions apply.",
            "Plan assets rule: when an insurance company issues a GIC or funding agreement to an ERISA plan, those assets may be treated as 'plan assets' subject to ERISA — making the insurer a fiduciary.",
        ],
        [
            "Thinking ERISA only applies to pension plan administrators — investment managers managing assets of ERISA plans are also fiduciaries subject to ERISA standards.",
            "Confusing the prudent investor rule with the prudent person rule — ERISA uses the 'prudent expert' standard (a professional familiar with such matters), which is higher than the ordinary 'prudent person' standard.",
            "Assuming GIC proceeds are automatically plan assets — the DOL's plan asset regulation determines whether GIC proceeds are plan assets. If not 'significant participation' exemption applies, they may be plan assets.",
        ],
        lessons=[
            _intro("ERISA: The Federal Law That Governs Pension Investing",
                   "If you manage assets for a private pension plan, 401(k), or employee benefit plan in the US, ERISA applies to you — not just to the plan trustee. ERISA's standards are stricter than general fiduciary duty and include personal liability for violations. Understanding ERISA is essential for any institutional investment professional."),
            _teach("ERISA's Core Investment Standards: Prudent Expert and Exclusive Benefit",
                   "ERISA establishes four core investment fiduciary duties for plan asset managers: (1) Prudent Expert Standard (ERISA Section 404(a)(1)(B)) — managers must act 'with the care, skill, prudence, and diligence under the circumstances then prevailing that a prudent person acting in a like capacity and familiar with such matters would use in the conduct of an enterprise of a like character and with like aims.' This is higher than the ordinary prudent person standard — it requires professional expertise, not just good intentions; (2) Exclusive Benefit Rule (Section 404(a)(1)(A)) — assets must be managed 'for the exclusive purpose of providing benefits to participants and their beneficiaries and defraying reasonable expenses of administering the plan.' No competing interests. A manager cannot recommend a product that benefits the manager at the expense of plan participants; (3) Diversification Requirement (Section 404(a)(1)(C)) — assets must be diversified 'so as to minimize the risk of large losses, unless under the circumstances it is clearly prudent not to do so.' Concentration in any single security or issuer creates ERISA compliance risk; (4) Conformity with Plan Documents — investments must be made in accordance with the plan documents (the equivalent of the IPS) to the extent consistent with ERISA.",
                   ["Prudent expert: higher than prudent person — requires professional expertise level of care.",
                    "Exclusive benefit: no competing interests. Manager cannot benefit at plan participants' expense.",
                    "Diversification: mandatory under ERISA — concentration risk must be justified and documented.",
                    "Plan document conformity: investment decisions must follow the plan's IPS and trust documents."]),
            _teach("ERISA Prohibited Transactions and Reporting Requirements",
                   "ERISA Section 406 prohibits transactions between the plan and 'parties in interest' — people with a relationship to the plan. Parties in interest include: plan fiduciaries, plan sponsor and its employees, service providers (investment managers, custodians, lawyers), and 50%+ shareholders of the plan sponsor. Prohibited transactions include: (1) Sale/purchase between plan and party in interest; (2) Lending plan assets to a party in interest; (3) Furnishing goods or services at more than reasonable compensation; (4) Self-dealing — manager uses plan assets for manager's own benefit. Exemptions exist for some transactions (e.g., paying reasonable investment management fees). Plan Asset Rule: when an ERISA plan invests in an entity (such as an insurance company's GIC or a hedge fund), the DOL must determine whether the plan's investment causes the underlying assets to be 'plan assets.' If they are plan assets, the investment manager becomes an ERISA fiduciary. The DOL's 'look-through' applies unless the 'significant participation' exemption applies (if plan investors hold less than 25% of any class of equity interest). Annual reporting: Form 5500 filed annually for all ERISA plans covering: plan assets, liabilities, investment performance, service providers, and fees paid.",
                   ["Parties in interest: plan sponsor, fiduciaries, service providers — prohibited counterparties for most transactions.",
                    "Self-dealing: most serious prohibited transaction — manager using plan assets for personal benefit.",
                    "Plan asset rule: DOL determines if assets in a commingled vehicle are ERISA plan assets.",
                    "Form 5500: annual ERISA reporting document — investments, fees, service providers all disclosed."]),
            _example("TIAA's ERISA Compliance in Practice",
                     "TIAA manages university retirement plans for over 15,000 academic institutions. ERISA compliance scenario: In 2022, TIAA identified that one of its bond funds held bonds issued by a company that was also a service provider to several TIAA-managed ERISA plans (a potential ERISA prohibited transaction — plan assets invested in securities of a 'party in interest'). TIAA's ERISA compliance team: (1) Determined whether the company was a 'party in interest' for the specific plans — yes, the company provided HR software services to 3 universities whose retirement plans were TIAA clients; (2) Calculated the exposure — $12M in bonds across 47 plan accounts; (3) Reviewed for exemptions — no applicable exemption (bonds were purchased after the service relationship was established); (4) Corrective action — sold the bonds within 30 days and credited the affected plans with any transaction costs. Reported the corrective action to DOL per ERISA voluntary correction program. No penalties assessed. TIAA's documentation of the discovery, analysis, and correction demonstrated the prudent expert standard in action.",
                     "ERISA compliance failures that are self-corrected and voluntarily disclosed to the DOL receive much more favorable treatment than violations that are discovered through audit. A robust compliance monitoring program that catches issues early is the most important ERISA protection."),
            _flash("What is the ERISA 'prudent expert' standard, and how does it differ from the 'prudent person' standard?",
                   "The ERISA prudent expert standard requires investment managers to act with the care, skill, prudence, and diligence of a 'prudent person acting in a like capacity and familiar with such matters.' The key phrase is 'familiar with such matters' — it holds investment professionals to the standard of a knowledgeable expert, not just an ordinary prudent person. A layperson who makes a well-intentioned but uninformed decision may meet the prudent person standard but fail the ERISA prudent expert standard. Investment managers must exercise professional expertise, not just good judgment."),
            _mcq("Under ERISA's exclusive benefit rule, an investment manager for a pension plan recommends purchasing bonds issued by the plan sponsor's parent company because the plan sponsor has asked them to support the parent's bond offering. This MOST LIKELY:",
                 ["Is acceptable if the bonds are investment-grade and fairly priced",
                  "Violates ERISA's exclusive benefit rule — the manager is acting for the plan sponsor's benefit, not solely the plan participants' benefit",
                  "Is a standard practice called 'affiliated investment' that ERISA explicitly permits",
                  "Is only prohibited if the plan sponsor directly instructs the manager in writing"],
                 1,
                 "The exclusive benefit rule requires that ALL investment decisions serve exclusively the plan participants' interests — not the plan sponsor's, not the manager's, not any other party's. Recommending bonds because the plan sponsor wants support for the offering violates this rule regardless of the bonds' investment quality. The manager must be able to justify the purchase solely on its merits for plan participants."),
            _mcq("An investment manager for an ERISA pension plan discovers that 35% of the plan's assets are concentrated in a single issuer's bonds. The manager has done no analysis of this concentration. Under ERISA, this MOST LIKELY violates:",
                 ["The exclusive benefit rule only",
                  "The prudent expert standard and the diversification requirement",
                  "The prohibited transaction rules under ERISA Section 406",
                  "Form 5500 reporting requirements only"],
                 1,
                 "ERISA Section 404(a)(1)(C) requires diversification to minimize the risk of large losses. A 35% concentration in a single issuer is extremely high and presumptively violates the diversification requirement unless there is a documented, compelling reason why it is 'clearly prudent.' Additionally, failing to analyze the concentration violates the prudent expert standard — a knowledgeable professional would have identified and addressed this risk."),
            _mcq("Which of the following is a 'prohibited transaction' under ERISA Section 406?",
                 ["An ERISA plan paying reasonable investment management fees to its registered investment adviser",
                  "An ERISA plan manager investing plan assets in publicly traded government bonds",
                  "An ERISA plan lending plan assets to the plan sponsor at a favorable interest rate",
                  "An ERISA plan diversifying across five asset classes as required by the plan's IPS"],
                 2,
                 "Lending plan assets to the plan sponsor is a prohibited transaction — the plan sponsor is a 'party in interest,' and ERISA prohibits loans between the plan and parties in interest. This applies even if the interest rate is favorable to the plan. The only exceptions are specific statutory or class exemptions granted by the DOL. Paying reasonable management fees to the plan's investment adviser is not prohibited (it's expressly permitted as necessary to plan operations)."),
            _mcq("The 'plan asset rule' under ERISA is MOST RELEVANT to which situation?",
                 ["A pension plan investing in US Treasury bonds",
                  "A pension plan buying stock in a publicly traded company",
                  "A pension plan investing in an insurance company's GIC or a pooled investment fund, determining whether the underlying assets become ERISA plan assets",
                  "A pension plan hiring a new investment manager"],
                 2,
                 "The plan asset rule applies when a plan invests in an entity (like a GIC, private equity fund, or pooled vehicle). The DOL must determine whether the plan's investment causes the underlying assets to be 'plan assets' — which would make the investment manager of those underlying assets an ERISA fiduciary. If the underlying assets are plan assets, the insurance company or fund manager becomes subject to ERISA's prohibited transaction rules and fiduciary standards for managing those assets."),
            _mcq("Under ERISA, which document must be filed annually to disclose a pension plan's assets, investment performance, fees, and service providers?",
                 ["Form ADV — the SEC investment adviser disclosure document",
                  "Form 5500 — the annual return/report for employee benefit plans filed with DOL",
                  "Form 13F — the quarterly institutional equity holdings report filed with SEC",
                  "Schedule B — the actuarial information form for defined benefit plan funding"],
                 1,
                 "Form 5500 is the primary ERISA annual reporting document. It discloses: plan assets and liabilities, investment returns by asset class, all fees paid to service providers (investment managers, custodians, consultants), plan administrator information, and any prohibited transactions. Large plans (100+ participants) must have their financial statements audited by an independent accountant. Form 5500 filings are public record and allow DOL to monitor plan financial health and detect fee abuse."),
            _scenario(
                "Pacific Life manages a $500M separate account for Acme Corporation's defined benefit pension plan under ERISA. Pacific Life's investment team identifies an opportunity: Acme Corporation (the plan sponsor) has issued new corporate bonds at 6.5% yield — significantly above Pacific Life's benchmark return target of 5.8%. The bonds are BBB-rated, consistent with the plan's investment policy. Pacific Life's institutional sales team is pressing the investment team to buy the bonds because Acme is a major client.",
                "Should Pacific Life purchase Acme's bonds for the pension plan, and what ERISA issues arise?",
                [("Yes — the bonds meet the IPS criteria (BBB-rated, above benchmark yield) so the purchase is appropriate regardless of the sponsor relationship", False,
                  "Meeting IPS criteria is necessary but not sufficient. Acme Corporation is the plan sponsor — a 'party in interest' under ERISA. Purchasing Acme's bonds for Acme's own pension plan may be a prohibited transaction under ERISA Section 406. Additionally, Pacific Life must be able to confirm the purchase is motivated solely by plan participant benefit (exclusive benefit rule), not by the business relationship with Acme as a client."),
                 ("Pacific Life must refuse to buy Acme's bonds for the pension plan — any purchase of plan sponsor securities is automatically prohibited under ERISA regardless of price or investment merit", False,
                  "Purchases of plan sponsor securities are not automatically prohibited — ERISA Section 407 allows up to 10% of plan assets in employer securities for defined contribution plans, with specific rules. For defined benefit plans, employer securities purchases are heavily scrutinized but not categorically prohibited. A proper exemption analysis and DOL guidance should be followed."),
                 ("Pacific Life must conduct an independent analysis of whether the bonds are in the plan participants' best interest (exclusive benefit), document that analysis rigorously, confirm whether a prohibited transaction exemption is needed, and ensure the institutional sales relationship has zero influence on the investment decision", True,
                  "Correct. The purchase may be permissible if: (1) Pacific Life's investment team independently concludes the bonds are the best available option at that yield/risk for the plan (exclusive benefit); (2) any required prohibited transaction exemption is obtained or confirmed to apply; (3) the institutional sales pressure is completely walled off from the investment decision (documented separately). The investment decision must be defensible as if Acme were a random unknown issuer — not a major client.")]
            ),
        ]
    )

    # Concept 4: Dodd-Frank, OTC Derivatives, Repo, and Securities Lending
    c4 = _concept(
        m2_id, 2,
        "Dodd-Frank OTC Derivatives Reform, Repurchase Agreements, and Securities Lending",
        "Describe the Dodd-Frank Act's impact on OTC derivatives markets for institutional investors, explain repurchase agreement (repo) mechanics and risk, and describe securities lending programs and their role in institutional portfolio management.",
        "The 2008 financial crisis revealed critical weaknesses in OTC derivatives markets (opacity, counterparty concentration, no central clearing) and in securities financing (repo and securities lending). The Dodd-Frank Act (2010) fundamentally restructured OTC derivatives markets: mandating central clearing for standardized swaps, requiring trade reporting to swap data repositories, and imposing margin requirements on uncleared swaps. Repo (repurchase agreements) and securities lending are the backbone of institutional securities financing — both allow institutions to earn additional income on their bond portfolios and manage short-term cash. Understanding these instruments is essential because insurance companies use all three regularly.",
        "PIMCO uses all three mechanisms for its insurance client portfolios. OTC derivatives (post Dodd-Frank): all interest rate swaps > $1M notional must be centrally cleared through CME Clearing or LCH; daily variation margin posted in cash; initial margin posted in government securities. In 2023, PIMCO's insurance client portfolios had $85B notional in centrally cleared interest rate swaps. Repo: PIMCO uses overnight repo to invest short-term cash — lending Treasury bonds and receiving cash at 5.30% (Fed Funds rate - 5 bps). When PIMCO needs liquidity, it does reverse repo (provides cash, receives Treasury collateral). $12B average daily repo balance for insurance clients. Securities lending: PIMCO's custodian (BNY Mellon) lends out Treasury and agency bonds from insurance client portfolios. Borrowers (mostly hedge funds and broker-dealers) pay a lending fee of 8-25 bps annually. Cash collateral received is reinvested in money market instruments earning 5.25%. Total securities lending income: approximately 0.05% of portfolio value annually — modest but incremental yield enhancement.",
        [
            "Dodd-Frank central clearing: standardized OTC derivatives (interest rate swaps, credit default swaps) must be cleared through a Central Counterparty (CCP) — eliminates bilateral counterparty risk.",
            "Variation margin: daily cash settlement of OTC derivative mark-to-market gains/losses — prevents accumulation of large bilateral exposures.",
            "Repo (repurchase agreement): sell securities today with agreement to repurchase at higher price in future; economically equivalent to a collateralized loan.",
            "Securities lending: lend securities to borrowers (typically hedge funds needing to short-sell) in exchange for collateral plus a lending fee.",
        ],
        [
            "Thinking Dodd-Frank eliminated all OTC derivatives trading — it mandated central clearing for standardized contracts but allowed 'uncleared' bilateral transactions for non-standardized/customized derivatives (with higher margin requirements).",
            "Confusing repo (borrower of cash) with reverse repo (lender of cash) — in a repo, you sell securities and receive cash (you're borrowing money); in a reverse repo, you buy securities and deliver cash (you're lending money).",
            "Assuming securities lending is risk-free — cash collateral reinvestment risk is real; if collateral is invested in risky instruments and values fall, the lender may suffer a loss.",
        ],
        lessons=[
            _intro("Post-Crisis Reforms and Securities Financing: Three Essential Mechanisms",
                   "The 2008 crisis changed OTC derivatives markets permanently. And beneath the surface of most institutional portfolios, repo and securities lending quietly generate incremental income. Understanding these three mechanisms completes the picture of institutional investment operations."),
            _teach("Dodd-Frank and the OTC Derivatives Market Reform",
                   "The Dodd-Frank Wall Street Reform and Consumer Protection Act (2010) restructured OTC derivatives markets after the crisis revealed catastrophic risks in the bilateral OTC market (AIG's credit default swap book being the emblematic example). Three key reforms affecting institutional investors: (1) Mandatory Central Clearing — standardized OTC derivatives (plain vanilla interest rate swaps, major credit default swap indices) must be cleared through registered Central Counterparties (CCPs) like CME Clearing or LCH. The CCP stands between buyer and seller, eliminating bilateral counterparty risk. If one party defaults, the CCP absorbs the loss using default fund contributions; (2) Margin Requirements — cleared swaps: daily variation margin (mark-to-market gains/losses settled in cash) + initial margin (pre-posted collateral against potential future exposure). Uncleared swaps (customized, non-standardized): bilateral initial and variation margin requirements under CFTC/SEC rules, often higher than cleared swap margin. Effect: bilateral OTC derivatives now require significant collateral posting; (3) Trade Reporting — all OTC derivative transactions must be reported to CFTC/SEC-registered Swap Data Repositories (SDRs) within 15 minutes of execution. This creates a complete public record of all OTC derivative activity, addressing the pre-crisis opacity problem.",
                   ["Central clearing: CCP stands between counterparties; no bilateral counterparty risk on cleared derivatives.",
                    "Variation margin: daily P&L settlement in cash — prevents large exposures from accumulating.",
                    "Initial margin: pre-posted collateral covering potential future exposure during close-out period.",
                    "SDR reporting: all OTC trades reported within 15 minutes — full market transparency."]),
            _teach("Repurchase Agreements (Repo) and Securities Lending",
                   "Repurchase Agreement (Repo): an institution sells securities (usually Treasuries) to a counterparty with an agreement to repurchase them at a higher price (usually tomorrow or in a few days). Economically, it's a collateralized loan: the institution borrows cash (at the repo rate), pledging securities as collateral. Reverse repo: the institution provides cash and receives securities as collateral — lending money at the repo rate. Insurance companies use repo to: (1) earn the repo rate on short-term cash (repo = alternative to money market funds); (2) obtain short-term funding by pledging bonds; (3) manage liquidity. Repo risk: haircuts — the securities posted as collateral are valued at market value minus a haircut (e.g., 2% for Treasuries) to protect the cash lender if the borrower defaults. If the borrower defaults and collateral value falls more than the haircut, the cash lender suffers a loss. Securities Lending: a custodian lends the institution's bonds or stocks to borrowers (hedge funds, broker-dealers) who need them (typically for short-selling). The borrower posts cash collateral (102-105% of market value). The lending institution (through custodian) reinvests the cash collateral in short-term instruments. Income = reinvestment return on cash collateral PLUS lending fee from borrower. Risk: if cash collateral is reinvested in instruments that lose value, the lender suffers a shortfall when collateral must be returned.",
                   ["Repo: sell securities + agree to repurchase = borrow cash at repo rate, collateralized by securities.",
                    "Reverse repo: provide cash + receive securities = lend cash at repo rate, secured by securities.",
                    "Haircut: collateral discount that protects cash lender; Treasuries = 2%, corporate bonds = 5-10%.",
                    "Securities lending income: lending fee + cash collateral reinvestment return (net of collateral return obligation)."]),
            _example("PIMCO's Post-Dodd-Frank Derivatives and Repo Operations",
                     "PIMCO's interest rate swap program post-Dodd-Frank: Before 2013 (pre-mandatory clearing): PIMCO entered bilateral IRS with 8 counterparties; estimated total bilateral counterparty credit exposure: $2.1B. After mandatory clearing: 100% of standard IRS (fixed vs. 3M SOFR, standard tenors) cleared through LCH.Clearnet. Daily variation margin: paid in USD cash. Initial margin: posted in US Treasury bonds. Total initial margin posted: $1.8B for $85B notional IRS portfolio. Counterparty credit exposure to any single dealer: reduced to near-zero (exposure is to LCH, which is AAA-rated and default-funded). PIMCO's repo program for insurance clients: $12B average daily overnight repo position. Mechanics: lend $12B face value US Treasuries overnight, receive $11.76B cash (2% haircut applied). Repo rate: Federal Funds rate - 5 bps (approximately 5.27%). Annual income: $11.76B × 5.27% = $620M annualized. This repo income partially offsets the opportunity cost of holding Treasuries vs. higher-yielding corporate bonds in short-duration segments.",
                     "Post-Dodd-Frank derivatives management and securities financing are now integral to institutional investment operations — not ancillary activities. Together they contribute meaningful risk reduction and incremental income."),
            _flash("In a repurchase agreement (repo), who is borrowing money and who is lending money?",
                   "The party who SELLS the securities and agrees to repurchase them is BORROWING money — they receive cash (a loan) and pledge securities as collateral. The party who BUYS the securities and agrees to sell them back is LENDING money — they provide cash and hold securities as collateral. The price difference between the sale and repurchase price equals the interest on the loan (the repo rate)."),
            _mcq("The Dodd-Frank Act's mandatory central clearing requirement for standardized OTC derivatives was PRIMARILY designed to address which pre-crisis risk?",
                 ["The risk that OTC derivatives were too expensive for small institutional investors",
                  "The concentrated bilateral counterparty credit risk that accumulated between major dealers and end-users with no central management",
                  "The risk that OTC derivatives were traded too infrequently to provide price discovery",
                  "The risk that OTC derivative margins were too high, reducing market liquidity"],
                 1,
                 "The 2008 crisis revealed that bilateral OTC derivatives created massive, concentrated, and largely invisible counterparty credit risks. AIG's undisclosed CDS exposures totaling $440B were the emblematic example — no regulator had a complete picture of the risk concentration. Mandatory central clearing through CCPs interposes a creditworthy central counterparty, eliminates bilateral counterparty risk, and makes total market exposure transparent through CCP data."),
            _mcq("An insurance company enters a repo transaction: it sells $100M US Treasury bonds to a dealer with an agreement to repurchase them tomorrow at $100.014M. This transaction is BEST described as:",
                 ["The insurance company lending $100M to the dealer, secured by Treasury bonds",
                  "The insurance company borrowing $100M overnight at the repo rate, pledging Treasuries as collateral",
                  "The insurance company permanently selling $100M Treasuries to earn a profit of $14,000",
                  "The insurance company hedging interest rate risk by selling Treasury bonds"],
                 1,
                 "In a repo, the insurance company sells (and agrees to repurchase) — this is borrowing money. The company receives $100M cash and pledges Treasuries as collateral. The $14,000 difference ($100.014M - $100M) is the interest on the overnight loan. Repo rate = ($14,000 / $100M) × (365/1) ≈ 5.11% annualized. The dealer is the cash lender (reverse repo from the dealer's perspective)."),
            _mcq("In a securities lending program, an insurance company's custodian lends $50M of Treasury bonds to a hedge fund. The hedge fund posts $51M in cash as collateral. The custodian reinvests the $51M cash in money market instruments yielding 5.2%. After paying the hedge fund a 0.15% rebate on the $51M collateral, what is the NET annual securities lending income?",
                 ["$2.652M (5.2% on $51M = $2.652M, no net rebate calculation needed)",
                  "Approximately $2.576M (5.2% × $51M = $2.652M income, minus 0.15% × $51M = $76,500 rebate = $2.576M net)",
                  "Approximately $0.076M (only the lending fee matters; reinvestment income belongs to the hedge fund)",
                  "Zero — securities lending is a neutral transaction with no income impact"],
                 1,
                 "Securities lending income has two components: (1) Cash collateral reinvestment: $51M × 5.2% = $2.652M; (2) Less: the rebate paid to the borrower (hedge fund): $51M × 0.15% = $76,500. Net income: $2.652M - $0.0765M = approximately $2.576M (approximately 0.50% on the $50M bond portfolio). The spread between the reinvestment rate and the rebate rate is the lending income. Most of the economics comes from the cash collateral reinvestment, not a direct lending 'fee.'"),
            _mcq("Which of the following is the MOST SIGNIFICANT risk in a securities lending program?",
                 ["The risk that the borrower returns the securities in damaged condition",
                  "The risk that the cash collateral is reinvested in instruments that lose value, creating a shortfall when collateral must be returned to the borrower",
                  "The risk that the lending rate is lower than expected",
                  "The risk that the borrower repays the loan early, reducing lending income"],
                 1,
                 "Cash collateral reinvestment risk is the most significant securities lending risk. When the borrower eventually returns the securities, the lender must return the cash collateral — at full value. If the reinvested cash collateral has lost value (invested in instruments that declined), the lender suffers a shortfall. The 2008 crisis revealed this risk acutely: securities lenders who reinvested cash collateral in mortgage-backed securities suffered large losses when MBS values collapsed. Many money market funds and insurance companies took significant securities lending losses in 2008."),
            _mcq("An uncleared (non-standard) OTC interest rate swap entered after Dodd-Frank requires which collateral arrangement that was NOT required before Dodd-Frank?",
                 ["No collateral — uncleared swaps are exempt from all Dodd-Frank margin requirements",
                  "Bilateral posting of both variation margin (daily P&L settlement in cash) and initial margin (pre-posted collateral against potential future exposure)",
                  "Posting of initial margin only, with variation margin optional",
                  "Automatic central clearing with daily margin calls from the CCP"],
                 1,
                 "Pre-Dodd-Frank, bilateral OTC swap counterparties often posted little or no collateral (especially for sovereign, corporate, and insurance counterparties with high credit ratings). Dodd-Frank extended mandatory margin requirements to uncleared swaps: both variation margin (daily mark-to-market settlements in cash) and initial margin (pre-posted collateral covering potential future exposure during the close-out period) are now required. This significantly increased the collateral demands on institutions with large uncleared derivative portfolios."),
            _scenario(
                "Guardian Life Insurance holds $5B in US Treasury bonds in its general account. The investment team proposes three ways to generate additional income on this portfolio: Strategy A — enter into a securities lending program through their custodian (State Street), lending the Treasuries to hedge funds; cash collateral reinvested in prime money market funds. Strategy B — execute $2B in overnight repo transactions, lending Treasuries for cash overnight, reinvesting cash in 30-day T-bills yielding 5.35% (repo rate 5.28%). Strategy C — enter a receive-fixed interest rate swap on $1B notional to extend duration without buying bonds; the swap must be centrally cleared.",
                "Which combination of strategies and associated risks is MOST accurately described?",
                [("All three are prohibited for insurance companies under NAIC guidelines and should not be pursued", False,
                  "None of the three strategies is prohibited. Securities lending, repo, and interest rate swaps are all standard institutional investment activities for insurance companies. NAIC guidelines restrict certain asset types but do not prohibit these routine investment management techniques."),
                 ("Strategy A has cash collateral reinvestment risk (prime MMF may lose value); Strategy B earns 7 bps carry (5.35% minus 5.28%) with low risk if Treasuries are the collateral; Strategy C requires initial and variation margin posting as a cleared swap but eliminates counterparty credit risk", True,
                  "Correct. Strategy A: income comes from reinvesting cash collateral at prime MMF rates minus borrower rebate; risk is MMF breaking the buck. Strategy B: 7 bps carry on $2B = $1.4M annually; Treasury collateral haircut is minimal (2%); low risk if reinvestment is in Treasuries. Strategy C: receive-fixed swap extends duration efficiently; mandatory clearing reduces counterparty risk but requires initial margin posting (approximately 1-3% of notional = $10-30M in Treasuries)."),
                 ("Strategy B should be avoided because repo transactions are prohibited transactions under ERISA", False,
                  "Guardian Life is an insurance company managing its own general account — not an ERISA fiduciary for a pension plan. ERISA prohibited transaction rules do not apply to an insurer's own general account investments. Repo is a standard, regulated investment management technique widely used by insurance companies.")]
            ),
        ]
    )

    m2["concepts"] = [c3, c4]
    ch["modules"] = [m1, m2]
    return ch

def _build_ch13(course_id):
    ch_id = _id()
    ch = {
        "id": ch_id, "course_id": course_id, "order": 13,
        "title": "Bond Mathematics, Convexity, and Advanced Bond Types",
        "description": "Master fixed income calculations: Macaulay and modified duration step-by-step, convexity and its role in immunization, TWR/MWR chain-linking examples, and risk-adjusted performance metrics (Sharpe, Treynor, Jensen). Covers advanced bond types: callable bonds, convertible bonds, floating rate notes, zero-coupon bonds, and inflation-linked bonds.",
    }

    # ── Module 1: Fixed Income Mathematics ───────────────────────────────────
    m1_id = _id()
    m1 = {"id": m1_id, "chapter_id": ch_id, "order": 1,
          "title": "Fixed Income Mathematics and Performance Calculation"}

    # Concept 1: Duration and Convexity Calculations
    c1 = _concept(
        m1_id, 1,
        "Duration and Convexity: Step-by-Step Calculation and Application",
        "Calculate Macaulay duration, modified duration, and dollar duration from first principles using discounted cash flow analysis; explain convexity and compute a bond's approximate price change using both duration and convexity; apply these measures to immunization and ALM strategies.",
        "Duration and convexity are the foundational risk measures for fixed income portfolios. Duration measures the first-order (linear) price sensitivity of a bond to interest rate changes; convexity captures the second-order (curvature) effect. Together they provide a second-order Taylor approximation of how a bond's price changes when interest rates change. For ALM, matching asset and liability durations is the central immunization objective. Convexity determines whether price appreciation (when rates fall) accelerates faster than price decline (when rates rise) — a property called 'positive convexity,' highly desirable in bond portfolios.",
        "A pension fund holds a single bond: Face value $1,000, 6% annual coupon (paid annually), 3 years to maturity, yield-to-maturity 5%. Step 1 — Price the bond: Cash flows: Year 1: $60; Year 2: $60; Year 3: $1,060. PV Year 1: 60/1.05 = 57.14; PV Year 2: 60/1.05² = 54.42; PV Year 3: 1060/1.05³ = 915.69. Bond price = 57.14 + 54.42 + 915.69 = $1,027.25. Step 2 — Macaulay Duration: Weighted average time to receive cash flows: Duration = [1×57.14 + 2×54.42 + 3×915.69] / 1027.25 = [57.14 + 108.84 + 2747.07] / 1027.25 = 2913.05 / 1027.25 = 2.836 years. Step 3 — Modified Duration: ModDur = MacDur / (1 + YTM) = 2.836 / 1.05 = 2.701. Step 4 — Price change approximation: If rates rise 50 bps (0.005): ΔP/P ≈ -ModDur × ΔY = -2.701 × 0.005 = -1.35%. Estimated new price: 1027.25 × (1 - 0.0135) = $1,013.38. Actual new price at 5.5%: $1,013.36. Duration estimate is excellent for small rate changes.",
        [
            "Macaulay Duration: weighted average time to receive all cash flows; weights are each cash flow's PV divided by total bond price.",
            "Modified Duration = Macaulay Duration / (1 + YTM/n); measures percent price change per 1% change in yield.",
            "Dollar Duration = Modified Duration × Price; measures dollar price change per 1% change in yield.",
            "Convexity: measures the curvature of the price-yield relationship; always positive for option-free bonds.",
        ],
        [
            "Confusing Macaulay and Modified Duration — they are related but different. Macaulay is in years; Modified is the price sensitivity measure (unit: % per % yield change).",
            "Thinking duration gives exact price changes — duration is a linear approximation; convexity corrects for the curvature. For large rate moves, convexity adjustment becomes important.",
            "Ignoring the difference between annual coupon and semi-annual coupon compounding — US bonds pay semi-annually; the correct formula uses YTM/2 and adjusts Macaulay Duration accordingly.",
        ],
        lessons=[
            _intro("Duration and Convexity: The Language of Interest Rate Risk",
                   "If you manage fixed income assets, duration and convexity are your primary risk vocabulary. Duration tells you how much a bond's price will move when rates change. Convexity tells you whether that movement is symmetric. This lesson walks through every calculation from scratch with real numbers."),
            _teach("Macaulay Duration: Step-by-Step Calculation",
                   "Macaulay Duration is the weighted average time to receive all of a bond's cash flows, where each weight is the present value of that cash flow divided by the total bond price. Calculation sequence for any bond: Step 1 — List all cash flows and their timing. Step 2 — Calculate the present value of each cash flow using the yield-to-maturity. Step 3 — Calculate the bond price (sum of all PVs). Step 4 — For each cash flow, multiply: (Time in years) × (PV of cash flow). Step 5 — Sum all (Time × PV) products. Step 6 — Divide the sum by the bond price. Result = Macaulay Duration in years. Key intuitions: (a) A zero-coupon bond has Macaulay Duration exactly equal to its maturity — all cash flow arrives at maturity; (b) Higher coupon rates → shorter duration (more early cash flows receive higher weights); (c) Higher yield → shorter duration (earlier cash flows have larger relative weight); (d) Longer maturity → longer duration (but at a decreasing rate as maturity extends for coupon bonds). Duration cannot exceed maturity for a coupon bond. For perpetuities: Duration = (1 + YTM) / YTM.",
                   ["Macaulay Duration formula: sum of (t × PV_t) divided by bond price.",
                    "Zero-coupon bond: Duration = Maturity exactly.",
                    "Higher coupon → shorter duration (more cash flows received early).",
                    "Duration ceiling: cannot exceed maturity for any coupon bond."]),
            _teach("Modified Duration, Dollar Duration, and Convexity",
                   "Modified Duration converts Macaulay Duration into a price sensitivity measure: ModDur = MacDur / (1 + YTM). For semi-annual coupon bonds (standard US bonds): ModDur = MacDur / (1 + YTM/2). Interpretation: a modified duration of 5.0 means the bond's price will change approximately 5.0% for every 1% (100 bp) change in yield. Dollar Duration = ModDur × Price / 100. This gives the dollar price change per 1 basis point (0.01%) change in yield — often called 'DV01' or 'dollar value of a basis point' (multiply by 100 for 1% moves). Price Change Approximation (first-order only): ΔP ≈ -ModDur × P × Δy. Convexity: the second derivative of price with respect to yield. For option-free bonds, convexity is always positive. Price change with both duration and convexity: ΔP/P ≈ -ModDur × Δy + (1/2) × Convexity × (Δy)². The convexity term adds a positive adjustment — a bond with higher convexity loses less when rates rise AND gains more when rates fall, for the same duration. This 'convexity premium' means investors pay more (accept lower yield) for higher-convexity bonds. Immunization uses duration matching to protect against interest rate risk: if asset duration equals liability duration, small parallel shifts in the yield curve have no net impact on surplus.",
                   ["Modified Duration = MacDur / (1 + YTM); semi-annual bonds use YTM/2.",
                    "DV01 (Dollar Value of 01): dollar price change per 1 bp yield move = ModDur × Price / 10,000.",
                    "Convexity adjustment: adds positive term to duration estimate; larger for larger rate moves.",
                    "Immunization: set asset duration = liability duration; surplus protected from parallel rate shifts."]),
            _example("Full Duration and Convexity Calculation with DV01",
                     "10-year, 6% annual coupon bond, face $1,000, YTM 5%. Price calculation: PV = 60×PVIFA(5%,10) + 1000×PVIF(5%,10) = 60×7.7217 + 1000×0.6139 = 463.30 + 613.91 = $1,077.22. Macaulay Duration calculation using annuity shortcut: MacDur = (1+y)/y - [10/(((1+y)^10 - 1))] for annual coupon bond. More intuitively: Duration ≈ 7.80 years (computed from full PV-weighted sum). Modified Duration = 7.80 / 1.05 = 7.43. DV01 = 7.43 × $1,077.22 / 10,000 = $0.80 per $1,000 face (or 0.080% of price per 1 bp). If rates rise 100 bps: ΔP ≈ -7.43 × 0.01 × $1,077.22 = -$80.04; estimated price = $997.18. With convexity (assume convexity = 68): Convexity adjustment = 0.5 × 68 × (0.01)² × $1,077.22 = $3.66. Adjusted estimated price = $997.18 + $3.66 = $1,000.84. Actual price at 6%: exactly $1,000. The convexity-adjusted estimate ($1,000.84) is much closer to the actual ($1,000.00) than the duration-only estimate ($997.18).",
                     "Convexity adds a meaningful correction for even moderate rate moves (100 bps). For 200+ bp shocks, convexity becomes critical. Callable bonds have negative convexity at low yields — the price-yield relationship bends the wrong way when rates fall."),
            _flash("What is 'negative convexity' and which types of bonds exhibit it?",
                   "Negative convexity means the price-yield relationship bends in the unfavorable direction — when rates fall, price appreciation is LESS than the linear (duration) estimate; when rates rise, price decline is MORE than the duration estimate. Callable bonds exhibit negative convexity at low yields because when rates fall, the issuer is likely to call the bond, capping price appreciation at the call price. Mortgage-backed securities (MBS) also have negative convexity because homeowners prepay mortgages when rates fall (effectively calling the bond). Negative convexity is unfavorable for investors — they should require a higher yield (option-adjusted spread) to compensate."),
            _mcq("A bond has a Macaulay Duration of 6.0 years and a YTM of 8% (annual coupon). What is its Modified Duration?",
                 ["6.00 years",
                  "5.56 (= 6.0 / 1.08)",
                  "6.48 (= 6.0 × 1.08)",
                  "7.00 (= 6.0 + 1.0)"],
                 1,
                 "Modified Duration = Macaulay Duration / (1 + YTM) = 6.0 / 1.08 = 5.56. Modified Duration is always less than Macaulay Duration for positive yields. This is the metric used for price sensitivity: a modified duration of 5.56 means the bond's price will change approximately 5.56% for every 1% (100 bp) change in yield. For semi-annual coupon US bonds, use YTM/2 in the denominator: MacDur / (1 + YTM/2)."),
            _mcq("An insurance company's bond portfolio has a Modified Duration of 8.5 and a market value of $500M. If interest rates rise 75 basis points, the estimated change in portfolio value using duration only is approximately:",
                 ["A decrease of $31.9M",
                  "An increase of $31.9M",
                  "A decrease of $4.25M",
                  "A decrease of $63.7M"],
                 0,
                 "ΔP = -ModDur × P × Δy = -8.5 × $500M × 0.0075 = -$31.875M ≈ -$31.9M. Duration measures sensitivity to yield changes: a positive Δy (rates rise) produces a negative ΔP (price falls). The 8.5 modified duration means a 1% rate move causes approximately 8.5% price change; 0.75% (75 bps) move causes approximately 8.5 × 0.75 = 6.375% change. $500M × 6.375% = $31.875M decrease."),
            _mcq("Which bond will have the LONGEST Macaulay Duration?",
                 ["A 10-year zero-coupon bond",
                  "A 10-year, 6% coupon bond (same maturity, same yield)",
                  "A 5-year zero-coupon bond (shorter maturity)",
                  "A 10-year, 8% coupon bond (same maturity, higher coupon)"],
                 0,
                 "A zero-coupon bond has duration equal to its maturity — there are no intermediate cash flows, so the full investment is received at maturity. Duration = 10 years for the 10-year zero. The 10-year coupon bonds (6% and 8%) both have durations shorter than 10 years because they make interim coupon payments that reduce the weighted-average time. The higher the coupon, the shorter the duration. The 5-year zero has duration of 5 years — shorter than the 10-year zero."),
            _mcq("An insurance company's assets have a Modified Duration of 9.2 and a market value of $1B. Its liabilities have a Modified Duration of 7.8 and a present value of $900M. What is the approximate change in economic surplus if interest rates rise 100 basis points?",
                 ["Surplus increases by approximately $70.2M",
                  "Surplus decreases by approximately $22.2M",
                  "Surplus decreases by approximately $92M",
                  "There is no change in surplus — assets and liabilities offset"],
                 1,
                 "Change in surplus = Change in assets - Change in liabilities. ΔAssets = -9.2 × $1,000M × 0.01 = -$92M. ΔLiabilities = -7.8 × $900M × 0.01 = -$70.2M. ΔSurplus = -$92M - (-$70.2M) = -$92M + $70.2M = -$21.8M ≈ -$22M. The surplus DECLINES because assets have longer duration than liabilities — assets fall more in value than liabilities when rates rise. For perfect immunization, assets and liabilities should have equal duration-weighted values."),
            _mcq("A callable bond has a Modified Duration of 4.5 at current market yields. When interest rates fall 200 basis points, an investor observes that the bond's price rises less than the duration estimate predicted. This behavior is BEST explained by:",
                 ["The bond has very high credit quality that limits price appreciation",
                  "The convexity adjustment always reduces price appreciation estimates",
                  "Negative convexity: as rates fall, the call option limits price appreciation because the issuer is likely to call the bond at the call price",
                  "The duration estimate was calculated incorrectly and should be adjusted upward"],
                 2,
                 "Negative convexity in callable bonds means the price-yield relationship 'bends back' when rates fall below the coupon rate. As rates decline, the probability of the issuer calling the bond increases, capping the bond's price at or near the call price. The investor cannot fully benefit from falling rates because the issuer will 'take back' the bond at the call price. The option-adjusted spread (OAS) compensates investors for this negative convexity by providing a yield premium above comparable non-callable bonds."),
            _scenario(
                "A life insurance company has a $2B long-term annuity liability with a duration of 12.5 years. The current investment portfolio consists of: (A) $1.2B corporate bond portfolio with duration 10.0 years; (B) $0.6B commercial mortgage loan portfolio with duration 8.0 years; (C) $0.2B Treasury bond portfolio with duration 5.0 years. The investment team needs to immunize the surplus against a parallel yield curve shift.",
                "Is the portfolio currently immunized? If not, what is the duration gap and what corrective action is needed?",
                [("The portfolio is immunized because the $2B asset total equals the $2B liability — book value matching is sufficient", False,
                  "Book value matching does not immunize against interest rate risk. Immunization requires duration matching, not just value matching. If asset and liability durations differ, even small rate moves will create surplus volatility."),
                 ("Asset duration = (1.2×10 + 0.6×8 + 0.2×5) / 2.0 = (12+4.8+1) / 2.0 = 8.9 years. Liability duration = 12.5 years. Duration gap = 8.9 - 12.5 = -3.6 years. Liabilities are longer than assets — if rates fall, liabilities rise more than assets, reducing surplus. Corrective action: extend asset duration by 3.6 years via long-duration bonds, duration-extending swaps (receive fixed, pay floating), or STRIPS.", True,
                  "Correct. The weighted asset duration (8.9 years) is significantly shorter than the liability duration (12.5 years). This negative duration gap means the company is exposed to falling rates — liabilities grow faster than assets when rates decline. Solutions include: buying long-duration Treasury STRIPS or corporate bonds, entering receive-fixed interest rate swaps (which extend duration), or reallocating away from short-duration mortgages toward longer-duration bonds."),
                 ("Duration gap = 12.5 - 8.9 = 3.6 years, but this is acceptable because the 5% yield cushion offsets the duration mismatch", False,
                  "A yield cushion does not protect against duration mismatch. If rates fall 300 bps (not uncommon in a flight-to-quality), the liability PV increases approximately 37.5% (12.5 × 3%) while assets increase only 26.7% (8.9 × 3%) — a 10.8% surplus gap on $2B = $216M shortfall. Duration gap must be managed explicitly.")]
            ),
        ]
    )

    # Concept 2: TWR, MWR, and Risk-Adjusted Performance Metrics
    c2 = _concept(
        m1_id, 2,
        "Performance Measurement: TWR, MWR, Sharpe, Treynor, Jensen, and Information Ratio Calculations",
        "Calculate Time-Weighted Return (TWR) using sub-period chain-linking, calculate Money-Weighted Return (MWR/IRR) using cash flow timing, compare TWR and MWR for performance evaluation purposes, and compute risk-adjusted performance metrics including the Sharpe ratio, Treynor ratio, Jensen's alpha, and Information ratio with actual numbers.",
        "Accurate performance measurement is the foundation of investment manager evaluation. The Time-Weighted Return (TWR) eliminates the distorting effect of external cash flows controlled by the client — it measures the investment manager's skill. The Money-Weighted Return (MWR) reflects the actual dollar-weighted experience of the investor, incorporating the timing and magnitude of contributions and withdrawals. GIPS standards mandate TWR for performance reporting. Risk-adjusted metrics (Sharpe, Treynor, Jensen) allow comparison across strategies with different risk levels, answering the question: did this manager generate enough extra return to justify the risk taken?",
        "Pension fund's equity manager: Q1: starting value $10M, ending value $11M, no cash flows. Q1 return: 10%. At start of Q2: client contributes $5M (total = $16M). Q2: ending value $15.2M. Q2 return: (15.2-16)/16 = -5.0%. TWR chain-linking: (1+0.10) × (1-0.05) - 1 = 1.10 × 0.95 - 1 = 1.045 - 1 = 4.5%. MWR: investor invested $10M at time 0 and $5M at midpoint; ending value $15.2M after 2 quarters. IRR calculation: -10M at t=0, -5M at t=0.5 (years), +15.2M at t=1. Solving: MWR ≈ 2.7% (approximately). The large contribution before Q2 (which had -5% returns) dragged the MWR below the TWR. The manager produced +4.5% TWR despite the client's 2.7% MWR experience — the difference is due to the unfortunate timing of the client's contribution right before a down quarter.",
        [
            "TWR: chain-link sub-period returns; eliminates cash flow timing distortion; standard for manager evaluation.",
            "MWR: IRR of actual cash flows; reflects investor's dollar-weighted experience; depends on contribution/withdrawal timing.",
            "Sharpe Ratio: (Portfolio return - Risk-free rate) / Portfolio standard deviation; risk measured by total risk.",
            "Treynor Ratio: (Portfolio return - Risk-free rate) / Portfolio beta; risk measured by systematic risk (beta) only.",
        ],
        [
            "Using MWR to evaluate a manager's skill — MWR rewards managers when clients add money before up-markets and penalizes them for poor client timing. Only TWR isolates manager skill.",
            "Thinking higher Sharpe ratio is always better — only meaningful when comparing strategies with similar objectives. A Sharpe of 1.2 in a bond strategy vs. 0.9 in an equity strategy doesn't mean bonds are better managed.",
            "Confusing Jensen's alpha (absolute outperformance vs. CAPM) with Information Ratio (consistency of active returns) — Jensen's alpha is a single number; IR divides alpha by tracking error to assess consistency.",
        ],
        lessons=[
            _intro("Performance Measurement: Did the Manager Add Value?",
                   "Performance measurement answers the most important question in institutional investing: Did this manager earn their fee? TWR and MWR measure returns differently, and the difference matters for evaluation. Risk-adjusted metrics tell us whether the return was appropriate for the risk taken. This lesson builds every calculation from scratch."),
            _teach("Time-Weighted Return: Chain-Linking Sub-Period Returns",
                   "TWR eliminates the impact of external cash flows (client contributions and withdrawals) to isolate the manager's investment decisions. Calculation steps: (1) Identify all sub-periods — a new sub-period starts whenever there is an external cash flow; (2) Calculate the return for each sub-period: HPR = (Ending Value - Beginning Value) / Beginning Value (where Beginning Value is the value AFTER the cash flow); (3) Chain-link the sub-period returns: TWR = [(1+R1) × (1+R2) × ... × (1+Rn)] - 1; (4) Annualize if needed: Annualized TWR = (1+TWR)^(1/years) - 1. Example with 4 quarterly cash flows: Q1: +8%, Q2: -3%, Q3: +5%, Q4: +4%. TWR = (1.08 × 0.97 × 1.05 × 1.04) - 1 = 1.1478 - 1 = 14.78%. GIPS requires portfolios to be valued at the time of each large external cash flow (> 10% of portfolio) to minimize distortion between sub-periods. If exact valuations are unavailable, the Modified Dietz method approximates TWR by adjusting for cash flows as a weighted average.",
                   ["Sub-period: defined by external cash flows; new sub-period starts with each contribution/withdrawal.",
                    "Chain-linking: multiply (1+R) for each sub-period — the geometric linking of returns.",
                    "GIPS: mandates TWR for performance reporting; exact valuations required for large cash flows.",
                    "Modified Dietz: approximates TWR when exact intra-period valuations unavailable."]),
            _teach("MWR, Sharpe, Treynor, Jensen, and Information Ratio",
                   "Money-Weighted Return (MWR): the IRR of the account's actual cash flows. If the investor contributed $1M at t=0, added $500K at t=1 year, and the account is worth $1.8M at t=2 years: solve -1M - 500K × v^1 + 1.8M × v^2 = 0 for v; MWR = 1/v - 1. Risk-Adjusted Performance Metrics: (1) Sharpe Ratio = (Rp - Rf) / σp. Rp = portfolio return, Rf = risk-free rate, σp = portfolio standard deviation. Measures excess return per unit of total risk. Use when comparing fully-diversified portfolios. Example: Rp=10%, Rf=4%, σ=12%. Sharpe = (10-4)/12 = 0.50. (2) Treynor Ratio = (Rp - Rf) / βp. Uses beta (systematic risk) instead of total risk. Use when the portfolio is one component of a larger diversified fund. Example: same data, βp=0.8. Treynor = (10-4)/0.8 = 7.5. (3) Jensen's Alpha = Rp - [Rf + βp × (Rm - Rf)]. Compares actual return to CAPM expected return. α = 10% - [4% + 0.8×(8%-4%)] = 10% - 7.2% = +2.8% alpha (manager outperformed). (4) Information Ratio = (Rp - Rb) / Tracking Error. Active return divided by active risk. Measures consistency of outperformance. IR > 0.5 is good; IR > 1.0 is excellent.",
                   ["Sharpe: excess return / total risk (σ); best for standalone fully-diversified portfolios.",
                    "Treynor: excess return / beta; best for one sleeve of a multi-manager portfolio.",
                    "Jensen's alpha: actual return minus CAPM expected return; positive alpha = outperformance.",
                    "Information Ratio = active return / tracking error; measures consistency — IR > 0.5 is solid."]),
            _example("Full Numerical Performance Attribution",
                     "Portfolio manager results for the year: Portfolio return (Rp): 13.5%. Benchmark return (Rb): 11.0%. Risk-free rate (Rf): 4.0%. Market return (Rm): 11.0%. Portfolio standard deviation (σp): 14.0%. Portfolio beta (βp): 0.95. Tracking error (σ of Rp-Rb): 3.2%. TWR calculation: sub-periods Q1: +4.0%, Q2: +2.5%, Q3: +5.0%, Q4: +1.5%. TWR = (1.04 × 1.025 × 1.05 × 1.015) - 1 = 1.1374 - 1 = 13.74% (slight difference from annual due to compounding). Sharpe Ratio: (13.5 - 4.0) / 14.0 = 9.5 / 14.0 = 0.679. Treynor Ratio: (13.5 - 4.0) / 0.95 = 9.5 / 0.95 = 10.0. Jensen's Alpha: 13.5% - [4% + 0.95 × (11% - 4%)] = 13.5% - [4% + 6.65%] = 13.5% - 10.65% = +2.85% alpha. Information Ratio: (13.5% - 11.0%) / 3.2% = 2.5% / 3.2% = 0.78. Interpretation: All four metrics confirm outperformance. The 0.78 IR is strong — the manager generates active return consistently relative to their active risk. The +2.85% alpha is statistically significant.",
                     "When all four risk-adjusted metrics align in confirming outperformance (positive Sharpe vs. benchmark, positive Treynor vs. benchmark, positive alpha, positive IR), the evidence for manager skill is strong."),
            _flash("Why does GIPS require TWR instead of MWR for performance reporting?",
                   "TWR isolates the investment manager's skill by eliminating the distorting effect of external cash flows. The manager does not control when clients add or withdraw money — only the investment decisions. If a client contributes a large amount right before a down market, the MWR suffers but the manager made no wrong decision. Using TWR allows fair comparison across managers who may have very different client cash flow patterns. GIPS standards exist to make performance claims comparable and verifiable across all institutional managers globally."),
            _mcq("A portfolio has $10M at the start of January. In March, the client withdraws $2M (portfolio value immediately before withdrawal: $11M). Portfolio value at year end: $8M. What is the TWR for the year?",
                 ["TWR = (8M - 10M) / 10M = -20% (simple full-year return)",
                  "Sub-period 1 return = (11M - 10M)/10M = 10%. Sub-period 2 return = (8M - (11M-2M))/9M = -1/9 = -11.1%. TWR = (1.10 × 0.889) - 1 = 0.978 - 1 = -2.2%",
                  "Sub-period 1 return = 10%. Sub-period 2 return = (8M - 11M)/11M = -27.3%. TWR = (1.10 × 0.727) - 1 = -20%",
                  "TWR cannot be calculated when there are withdrawals — use MWR instead"],
                 1,
                 "TWR sub-period calculation: Sub-period 1 (Jan-Mar): Return = (11M - 10M) / 10M = 10%. Sub-period 2 starts AFTER the withdrawal — beginning value = 11M - 2M = $9M. Return = (8M - 9M) / 9M = -11.1%. Chain-link: TWR = (1.10 × 0.889) - 1 = 0.978 - 1 = -2.2%. The key is that the sub-period 2 beginning value is the post-withdrawal value ($9M), not the pre-withdrawal value ($11M)."),
            _mcq("A portfolio manager achieves a return of 12% with a beta of 1.4 and standard deviation of 18%. The market returns 10%, the risk-free rate is 4%, and the market standard deviation is 12%. Jensen's alpha for this manager is:",
                 ["+2.8% (12% minus CAPM expected return of 9.2%)",
                  "-0.4% (12% minus CAPM expected return of 12.4%)",
                  "+0.4% (Sharpe calculation error)",
                  "Jensen's alpha cannot be calculated without the benchmark tracking error"],
                 1,
                 "Jensen's alpha = Actual return - CAPM expected return. CAPM expected return = Rf + β × (Rm - Rf) = 4% + 1.4 × (10% - 4%) = 4% + 1.4 × 6% = 4% + 8.4% = 12.4%. Jensen's alpha = 12% - 12.4% = -0.4%. Despite earning 12% (above the market's 10%), this manager underperformed on a risk-adjusted basis because their portfolio had beta 1.4 — meaning CAPM would expect 12.4% for that level of systematic risk."),
            _mcq("Portfolio A: annual return 15%, standard deviation 20%, beta 1.5. Portfolio B: annual return 12%, standard deviation 10%, beta 0.8. Risk-free rate: 4%. Market return: 11%. Based on the Sharpe ratio alone, which portfolio is superior?",
                 ["Portfolio A — it earned 15% vs. Portfolio B's 12%; higher absolute return wins",
                  "Portfolio B — Sharpe(A) = (15-4)/20 = 0.55; Sharpe(B) = (12-4)/10 = 0.80; Portfolio B has higher risk-adjusted return per unit of total risk",
                  "Portfolio A — Sharpe(A) = (15-4)/1.5 = 7.3; Sharpe(B) = (12-4)/0.8 = 10; incorrect divisor yields wrong answer",
                  "Both portfolios are equivalent — the Sharpe ratio cannot differentiate them"],
                 1,
                 "Sharpe(A) = (15% - 4%) / 20% = 11/20 = 0.55. Sharpe(B) = (12% - 4%) / 10% = 8/10 = 0.80. Portfolio B has the higher Sharpe ratio despite lower absolute returns. Portfolio A's higher returns came at the cost of proportionally higher volatility. The Sharpe ratio rewards managers who generate excess returns efficiently — with less total risk. Portfolio B's 0.80 Sharpe significantly exceeds A's 0.55, making B the superior risk-adjusted performer."),
            _mcq("An investment manager's annual returns vs. the benchmark over 4 years: Year 1: +1.5%, Year 2: +0.8%, Year 3: +2.1%, Year 4: +1.2% (all active returns, portfolio minus benchmark). The standard deviation of these active returns is 0.50%. The Information Ratio is:",
                 ["3.12 (average active return 1.4% / 0.45% tracking error — approximate)",
                  "2.80 (= 1.40% / 0.50%)",
                  "0.50 (only the tracking error matters for Information Ratio)",
                  "The Information Ratio requires 3 years minimum; 4 years is insufficient"],
                 1,
                 "Information Ratio = Average Active Return / Tracking Error (std dev of active returns). Average active return = (1.5 + 0.8 + 2.1 + 1.2) / 4 = 5.6% / 4 = 1.4%. Tracking error (given) = 0.50%. IR = 1.4% / 0.50% = 2.80. An IR of 2.80 is exceptional — it means the manager consistently adds 1.4% of active return with only 0.50% variability. Any IR above 1.0 is considered excellent; 2.80 would represent elite consistency."),
            _mcq("A portfolio earns 14% with a standard deviation of 16%. The benchmark earns 11% with a standard deviation of 13%. The risk-free rate is 3%. The portfolio's beta relative to the benchmark is 1.1. Which statement about the portfolio's Treynor ratio is MOST accurate?",
                 ["Treynor ratio = (14% - 3%) / 16% = 0.69, using total risk (standard deviation)",
                  "Treynor ratio = (14% - 3%) / 1.1 = 10.0, using systematic risk (beta) as the denominator",
                  "Treynor ratio = (14% - 11%) / 13% = 0.23, measuring active return per unit of benchmark risk",
                  "Treynor ratio = (14% - 3%) / (14% - 11%) = 3.67, the ratio of excess return to active return"],
                 1,
                 "Treynor Ratio = (Portfolio Return - Risk-Free Rate) / Beta = (14% - 3%) / 1.1 = 11% / 1.1 = 10.0. The Treynor ratio uses BETA (systematic risk) as the denominator, not standard deviation (which is the Sharpe ratio's denominator). Treynor is appropriate when the portfolio is one component of a larger diversified fund — in that case, only systematic risk matters because unsystematic risk is diversified away in the total portfolio. Compare: Sharpe = (14-3)/16 = 0.69 uses total risk."),
            _scenario(
                "A life insurance company is evaluating two external equity managers for its surplus portfolio. Manager Alpha: 3-year TWR = 18.5%, Benchmark return = 15.0%, Standard deviation = 22%, Beta = 1.3, Tracking error = 5.0%, Risk-free rate = 3%. Manager Beta: 3-year TWR = 16.0%, Benchmark return = 15.0%, Standard deviation = 14%, Beta = 0.9, Tracking error = 2.5%, Risk-free rate = 3%.",
                "Using all four risk-adjusted metrics, which manager demonstrates superior performance and why?",
                [("Manager Alpha — 18.5% absolute return is highest; absolute return is all that matters for insurance surplus", False,
                  "Absolute return ignores risk. An insurance company's surplus is finite — taking excessive risk to earn higher returns could amplify losses. Risk-adjusted metrics exist precisely to evaluate whether the extra return compensates for the extra risk."),
                 ("Manager Beta — Sharpe(Alpha)=(18.5-3)/22=0.70; Sharpe(Beta)=(16-3)/14=0.93. IR(Alpha)=3.5/5.0=0.70; IR(Beta)=1.0/2.5=0.40. Jensen: Alpha=18.5-[3+1.3×12]=18.5-18.6=-0.1% (underperforms CAPM). Beta=16-[3+0.9×12]=16-13.8=+2.2% (outperforms). Manager Beta wins on Sharpe ratio, Jensen's alpha, and equivalent absolute outperformance — with far lower risk", True,
                  "Correct. Manager Beta appears less impressive on absolute return (16% vs. 18.5%) but is superior risk-adjusted: Sharpe(Beta)=0.93 > Sharpe(Alpha)=0.70. Jensen: Alpha has -0.1% alpha (barely adequate for the beta taken); Beta has +2.2% alpha. Manager Alpha's IR of 0.70 is better than Beta's 0.40 (more consistent active returns relative to tracking error), but this is outweighed by the risk-adjusted underperformance on Sharpe and Jensen. For insurance surplus, lower beta and lower volatility (Manager Beta) is generally preferred."),
                 ("Manager Alpha — Information Ratio of 0.70 vs. 0.40 definitively proves Alpha is the better manager across all metrics", False,
                  "IR is one metric, not all four. Manager Alpha's higher IR (0.70 vs. 0.40) reflects consistency of active returns but does not overcome the lower Sharpe ratio and negative Jensen's alpha. No single metric is definitive — all four should be considered together, weighted by the specific mandate objectives.")]
            ),
        ]
    )

    m1["concepts"] = [c1, c2]

    # ── Module 2: Advanced Bond Types ─────────────────────────────────────────
    m2_id = _id()
    m2 = {"id": m2_id, "chapter_id": ch_id, "order": 2,
          "title": "Advanced Bond Types: Callable, Convertible, Floating Rate, and Zero-Coupon"}

    # Concept 3: Callable Bonds, Putable Bonds, and Option-Adjusted Spread
    c3 = _concept(
        m2_id, 1,
        "Callable Bonds, Putable Bonds, and Option-Adjusted Spread Analysis",
        "Explain the structure of callable and putable bonds, analyze the embedded option's impact on yield and price, describe yield-to-call vs. yield-to-maturity, explain option-adjusted spread (OAS) and its calculation purpose, and analyze negative convexity in callable bonds.",
        "Callable bonds and putable bonds contain embedded options that fundamentally change their risk-return profile relative to option-free bonds. In a callable bond, the issuer holds a call option — the right to redeem the bond before maturity at a specified call price. This benefits the issuer (they can refinance at lower rates if rates fall) and disadvantages the investor (they lose the high-yield bond just when rates are lowest). Putable bonds give the investor a put option — the right to sell the bond back to the issuer at a specified price. Analyzing callable and putable bonds requires option pricing methods (binomial tree or Monte Carlo) to separate the embedded option's value from the 'straight' bond's value, resulting in the option-adjusted spread (OAS).",
        "Apple Inc. callable bond: $1,000 face, 5.5% coupon, 20-year maturity, callable at par ($1,000) after 5 years (5NC5). Comparable non-callable Apple bond yields 5.0%. The callable bond must yield MORE than 5.0% to compensate investors for the call option risk. If the callable bond is priced at $1,020 (yield-to-maturity 5.35%), the yield spread over the non-callable is 35 bps. This 35 bps is NOT the OAS — it's the Z-spread. The OAS removes the embedded option value: using a binomial interest rate tree calibrated to the Treasury yield curve, analysts calculate that the call option is worth 18 bps. OAS = Z-spread - embedded option cost = 35 bps - 18 bps = 17 bps. Interpretation: on an option-adjusted basis, Apple is offering 17 bps above comparable Treasuries — the fair spread for Apple's credit risk. The OAS allows apples-to-apples comparison between callable bonds and non-callable bonds.",
        [
            "Callable bond: issuer holds call option; investor gives up upside price appreciation when rates fall; issuer benefits from refinancing at lower rates.",
            "Yield-to-call (YTC): YTM calculated assuming bond is called on the first call date at the call price — often lower than YTM if bond trades above call price.",
            "OAS: option-adjusted spread; removes the embedded option's cost from the yield spread; comparable across bonds with different embedded options.",
            "Negative convexity: callable bonds' price-yield curve bends the wrong way at low yields because the call cap limits price appreciation.",
        ],
        [
            "Using YTM (not YTC) to evaluate callable bonds trading above the call price — if the bond is likely to be called, YTM is irrelevant; YTC (or yield-to-worst) is the binding constraint.",
            "Thinking OAS is just another yield spread — OAS is model-dependent (requires an interest rate model); different OAS models will give different values for the same bond.",
            "Assuming negative convexity is always bad for issuers — it's actually beneficial for the issuer (the call option allows cheaper refinancing) but negative for investors.",
        ],
        lessons=[
            _intro("Callable Bonds and OAS: Beyond Simple Yield Comparisons",
                   "A callable bond is not just a regular bond with a higher yield. The embedded call option changes how the bond behaves in every interest rate scenario — and requires specialized analytics to evaluate properly. This lesson explains the structure, the yield measures, and the OAS methodology used by institutional fixed income teams."),
            _teach("Callable Bond Structure, Call Schedules, and Investor Risk",
                   "A callable bond has two dates to track: the maturity date (final scheduled repayment) and the call date(s) (earliest/scheduled dates the issuer can redeem early). Common call structures: (1) Bullet call — callable on a single future date at par; (2) Make-whole call — callable any time but only at a price that 'makes whole' the investor (present value of remaining cash flows at Treasury + fixed spread); this minimizes investor losses but is still a call. (3) European call — callable only on specified dates; (4) American call — callable any time after the call protection period (common in high-yield bonds); (5) Refunding protection — callable but cannot use new debt proceeds at lower rates during protection period. Call schedule: '5NC5' means 5-year non-call 5 (callable starting in 5 years). '10NC3' means 10-year maturity, callable after 3 years. Call price schedule: often starts at par + one coupon and steps down to par as maturity approaches. Investor risk: if rates fall after purchase, the issuer calls the bond at the call price, and the investor receives back the call price — which may be less than the market value the bond would have had if it were non-callable. The investor then must reinvest at the now-lower rates — the classic reinvestment risk in callable bonds.",
                   ["Call schedule: non-call period + call dates + call prices. '5NC5' = callable after 5 years.",
                    "Make-whole call: issuer can call at any time but must compensate investor (market-based formula).",
                    "Reinvestment risk: when called, investor must reinvest at prevailing (lower) rates.",
                    "Yield-to-worst: the minimum of YTM and all YTC calculations; the true return floor."]),
            _teach("OAS, Price Decomposition, and Negative Convexity",
                   "Option-Adjusted Spread (OAS) analysis decomposes a callable bond's value into the value of a straight (non-callable) bond minus the value of the embedded call option: Price of callable bond = Price of equivalent straight bond - Value of call option. OAS is the constant spread over all Treasury spot rates (the OAS curve) that equates the model-derived price to the market price after removing the option's effect. OAS process: (1) Build an interest rate tree (binomial) calibrated to the current Treasury curve; (2) Model the issuer's call decision at each node (rational — call when the refinancing benefit exceeds costs); (3) Calculate the present value of cash flows under each scenario; (4) Solve for the spread that makes the model price equal to market price. The OAS is 'clean' — it reflects only the issuer's credit spread above Treasuries, not the option's distortion. Negative Convexity: For a non-callable bond, lower yields always mean higher prices (positive convexity). For a callable bond: when rates are HIGH (above coupon), the bond is unlikely to be called — it behaves like a normal bond (positive convexity). When rates are LOW (below coupon), the call option is in-the-money — as rates fall further, the bond's price is capped near the call price. Price cannot rise much beyond the call price because the issuer will call. Result: the price-yield curve bends backward — LESS price appreciation as rates fall. This is negative convexity.",
                   ["OAS = spread over Treasuries after removing embedded option cost; allows apples-to-apples comparison.",
                    "OAS = Z-spread (nominal spread) minus embedded option cost.",
                    "Negative convexity: price capped at call price as rates fall; no price appreciation beyond call price.",
                    "Binomial tree: models all possible interest rate paths to value the embedded option."]),
            _example("Callable Bond OAS Analysis at MetLife",
                     "MetLife's fixed income team analyzes a 10-year callable corporate bond (callable at par after 3 years — 10NC3): Coupon 6.5%, YTM 6.2%, Call price $1,000. Non-callable comparable bond yield: 5.8%. Analysis: YTM = 6.2% (assume 3% Treasury + 3.2% credit/call spread). Z-spread = 6.2% - 3% (Treasury) = 3.2% (but this includes option value). OAS calculation via binomial tree: At 50 interest rate nodes over 10 years, MetLife's model finds the issuer would optimally call in 34 nodes (interest rates below 5.5%). Expected call option value = 0.55% (55 bps). OAS = Z-spread - Option cost = 3.2% - 0.55% = 2.65% OAS. Conclusion: MetLife's credit analysts believe this issuer should trade at OAS 2.8% for its credit rating. At OAS 2.65%, the bond is slightly RICH (expensive) — the call option is underpriced in the market. MetLife decides not to buy. If the bond repriced to OAS 3.0%, it would be cheap and a buy.",
                     "OAS analysis converts a complex optionality problem into a simple spread decision: is 2.65% OAS adequate for this credit risk? This is the same question MetLife asks for a non-callable bond with a 2.65% spread — the option math has been done."),
            _flash("What is 'yield-to-worst' and why is it the most important yield measure for callable bonds?",
                   "Yield-to-worst (YTW) is the minimum yield an investor would receive assuming the most unfavorable call scenario occurs. It is calculated as the minimum of: the YTM (assuming the bond runs to maturity) and the yield-to-call for each possible call date (YTC1, YTC2, YTC3...). Yield-to-worst represents the true floor return the investor can count on regardless of what the issuer does. When a callable bond trades above its call price (which happens when rates fall), the YTC is less than the YTM — and YTW equals the YTC. Institutional investors always use YTW, not YTM, when evaluating callable bonds trading above the call price."),
            _mcq("A 10-year callable bond (callable at $1,020 after 3 years) is currently trading at $1,050. The yield-to-maturity is 5.2% and the yield-to-call is 4.6%. The yield-to-worst is:",
                 ["5.2% — always use YTM for callable bonds",
                  "4.6% — the minimum of YTM and YTC; the bond is likely to be called",
                  "4.9% — the average of YTM and YTC",
                  "The yield-to-worst cannot be determined without the exact call schedule"],
                 1,
                 "Yield-to-worst = minimum of YTM (5.2%) and all YTC calculations (4.6%) = 4.6%. Since the bond trades above the call price ($1,050 > $1,020), the issuer has an incentive to call if rates decline further, and the investor is likely to receive only the call price. The YTC of 4.6% represents the investor's most pessimistic realistic return — and since it's the minimum, it's the yield-to-worst."),
            _mcq("The Option-Adjusted Spread (OAS) of a callable bond is BEST described as:",
                 ["The spread between the callable bond's YTM and the risk-free Treasury yield",
                  "The spread between the callable bond's YTM and the non-callable comparable bond's YTM",
                  "The spread over Treasury rates that the bond offers after mathematically removing the embedded call option's value, reflecting only the issuer's credit risk",
                  "The spread that the issuer pays above LIBOR on a floating-rate equivalent"],
                 2,
                 "OAS removes the embedded option's value from the total yield spread, leaving only the credit risk spread. It answers: 'What is this issuer's credit spread, independent of the call option?' This makes OAS directly comparable across callable and non-callable bonds with similar credit risk. If a non-callable bond from the same issuer offers OAS 2.5% and the callable bond offers OAS 2.3%, the callable bond is relatively expensive — you're getting less credit spread per unit of risk."),
            _mcq("A callable bond and an equivalent non-callable bond have the same credit rating, maturity, and coupon. When market interest rates FALL significantly below the coupon rate, which BEST describes the callable bond's price behavior?",
                 ["The callable bond's price rises faster than the non-callable bond because higher yields confirm call is unlikely",
                  "The callable bond's price appreciates in parallel with the non-callable bond because both have the same credit quality",
                  "The callable bond's price appreciation is limited (negative convexity) because the call option becomes in-the-money, capping price near the call price",
                  "The callable bond's price falls while the non-callable bond's price rises, because falling rates cause the call option to expire worthless"],
                 2,
                 "Negative convexity: when rates fall significantly below the coupon rate, the call option is in-the-money (it's economically rational for the issuer to call). The market caps the callable bond's price near or below the call price because investors know the issuer will redeem at the call price if rates stay low. The non-callable bond continues appreciating without a ceiling. This asymmetry — the investor cannot benefit from falling rates beyond the call price ceiling — is the investor's cost of holding a callable bond."),
            _mcq("An investor holds a 7-year corporate bond that becomes callable at par ($1,000) after 2 years. The current market value is $1,030. If rates drop 150 bps and the issuer calls the bond, the investor's realized loss relative to holding a non-callable bond would be PRIMARILY due to:",
                 ["The investor receiving $1,030 at call — a capital gain from par of $30",
                  "The investor receiving only $1,000 at call price while the equivalent non-callable bond would have risen to approximately $1,100 — forfeiting $100 of potential price appreciation",
                  "The investor's coupon payments stopping immediately upon the call announcement",
                  "The investor being required to pay a penalty for early termination of the bond contract"],
                 1,
                 "When the bond is called, the investor receives the call price ($1,000), not the market value ($1,030+) or the theoretical non-callable price (which, with 150 bps rate drop, would be approximately $1,100+). The $100+ difference represents the option cost — the price appreciation the investor was denied because the issuer exercised its call right. The investor now reinvests the $1,000 at prevailing rates (150 bps lower), compounding the reinvestment risk on top of the price appreciation loss."),
            _mcq("A make-whole call provision differs from a standard call provision in that the make-whole call:",
                 ["Allows the issuer to call only during specific calendar windows, protecting the investor from surprise calls",
                  "Requires the issuer to call ALL outstanding bonds simultaneously when triggered, rather than in partial amounts",
                  "Requires the issuer to pay a call price calculated as the present value of remaining cash flows at a Treasury rate plus spread, effectively compensating the investor for future cash flows lost to the call",
                  "Prohibits the issuer from calling bonds if credit spreads have widened since issuance"],
                 2,
                 "A make-whole call compensates the investor by setting the call price equal to the present value of all remaining coupon and principal cash flows, discounted at a Treasury rate plus a small spread (e.g., T+50 bps). Because this formula uses a very low discount rate, the call price typically exceeds the bond's market price, making it economically unattractive for the issuer to call except in extreme circumstances. Make-whole calls provide investors with strong protection while giving issuers theoretical flexibility — they differ fundamentally from standard calls, which allow issuers to call at a fixed par or premium price."),
            _scenario(
                "A pension fund's fixed income manager is considering two bonds for a 10-year portfolio: Bond X — Non-callable 10-year corporate bond, A-rated, YTM 5.8%, OAS 120 bps. Bond Y — Callable 10-year corporate bond (callable at par after 3 years), A-rated, same issuer as Bond X, YTM 6.2%, OAS 115 bps. The manager believes interest rates will decline 100 bps over the next 12 months.",
                "Which bond should the manager purchase, and what analysis supports this decision?",
                [("Bond Y — the higher YTM of 6.2% always makes it the better investment for a pension fund seeking current income", False,
                  "YTM is irrelevant without considering the embedded call. If rates fall 100 bps (as the manager predicts), Bond Y is very likely to be called in 3 years — at which point the effective yield on the investment (the YTC) will be substantially lower than 6.2%. The 6.2% YTM assumes the bond runs to maturity, which is unlikely."),
                 ("Bond X — the non-callable bond has a HIGHER OAS (120 bps vs 115 bps), meaning Bond X offers more credit spread per unit of risk on an option-adjusted basis. Additionally, if rates fall 100 bps as predicted, Bond X will appreciate significantly while Bond Y's price will be capped near the call price by negative convexity. The manager's rate view makes the non-callable bond strongly preferred.", True,
                  "Correct. The OAS comparison is definitive: Bond X (120 bps OAS) offers more credit compensation than Bond Y (115 bps OAS) despite the same credit rating and issuer. Bond Y's higher YTM merely compensates for the call option risk — on an option-adjusted basis, it's actually CHEAPER compensation. Furthermore, the manager's bullish rate view (rates falling 100 bps) makes the callable bond (which will be called, limiting appreciation) clearly inferior to the non-callable bond (which will appreciate freely)."),
                 ("Bond Y — higher coupon bonds always outperform in falling rate environments because more coupon income is received before rates fall", False,
                  "Higher coupons provide more current income, but the bond will likely be called in 3 years — ending the stream of high coupon income earlier than anticipated. The benefit of high coupons is outweighed by the truncation of the investment horizon (early call) and the loss of price appreciation in a falling rate environment.")]
            ),
        ]
    )

    # Concept 4: Convertible Bonds, Floating Rate Notes, Zero-Coupon, and TIPS
    c4 = _concept(
        m2_id, 2,
        "Convertible Bonds, Floating Rate Notes, Zero-Coupon Bonds, and Inflation-Linked Securities",
        "Explain the structure and key metrics of convertible bonds (conversion ratio, conversion premium, parity value), describe how floating rate notes work (SOFR benchmark, spread, reset frequency), explain zero-coupon bond pricing and OID tax treatment, and describe TIPS inflation adjustment mechanics.",
        "Advanced bond types go beyond the plain-vanilla fixed-coupon bond to serve specific investor and issuer needs. Convertible bonds offer investors equity upside with bond-like downside protection. Floating rate notes provide natural inflation and interest rate hedging for liability-sensitive investors. Zero-coupon bonds offer pure duration extension and are ideal for matching long-dated liabilities. Inflation-linked bonds (TIPS) provide explicit inflation protection through principal adjustment. Each instrument has distinct pricing mechanics, tax treatment, and ALM applications for institutional investors.",
        "TIAA's fixed income team manages all four types in their general account. Convertible: $500M of TechCorp converts to 20 shares per bond at $50/share. Current stock price: $45. Parity value = 20 × $45 = $900. Bond price = $1,050. Conversion premium = (1050 - 900) / 900 = 16.7%. Investors pay 16.7% above parity for the bond's downside protection. Floating rate note: $100M, SOFR + 150 bps, quarterly reset. When SOFR = 4.8%, coupon = 6.3% / 4 = 1.575% per quarter. Duration ≈ 0.25 years (resets to par every 90 days). Zero-coupon: $100M face, 20-year maturity, 4.5% yield. Price = 100M / (1.045)^20 = $41.5M. Duration = 20 years exactly. OID accrual: each year the IRS requires the holder to recognize phantom interest income (even though no cash is received) based on the yield. TIPS: $100M face. If CPI-U rises 3% in year 1, adjusted principal = $103M. Coupon (say 1.5% real yield) = 1.5% × $103M = $1.545M. Both principal and coupon grow with inflation.",
        [
            "Convertible bond: contains option to convert into equity at conversion ratio; conversion premium measures how much investor pays above current parity (equity) value.",
            "Floating rate note (FRN): coupon resets periodically (quarterly, monthly) based on benchmark rate (SOFR) plus spread; duration approaches zero at each reset date.",
            "Zero-coupon bond: no periodic coupons; sold at deep discount; duration equals maturity; OID (Original Issue Discount) creates phantom taxable income annually.",
            "TIPS (Treasury Inflation-Protected Securities): principal adjusts with CPI; real coupon applied to inflation-adjusted principal; provides real yield certainty.",
        ],
        [
            "Thinking a convertible bond's conversion premium represents a loss — the premium is what investors willingly pay for the downside protection (bond floor) that a plain equity investment would not provide.",
            "Confusing FRN duration with maturity — an FRN's duration is approximately the time to the next coupon reset, NOT its maturity. A 10-year quarterly-reset FRN has duration of approximately 0.25 years.",
            "Thinking zero-coupon bonds create no tax obligation until maturity — the IRS requires annual OID recognition on the accrued (phantom) interest, creating a tax liability despite no cash coupon received.",
        ],
        lessons=[
            _intro("Four Bond Types That Every Institutional Investor Must Understand",
                   "Beyond plain-vanilla bonds, institutional portfolios regularly include convertible bonds, floating rate notes, zero-coupon bonds, and inflation-linked securities. Each serves a distinct purpose and behaves very differently in various market environments. This lesson covers all four with complete mechanics and institutional applications."),
            _teach("Convertible Bonds: Equity Upside with Bond Floor",
                   "A convertible bond is a corporate bond that the holder can convert into a specified number of shares at a specified price. Key terms: (1) Conversion ratio: number of shares received per bond. Example: 25 shares per $1,000 bond; (2) Conversion price: price per share implied by the conversion. Conversion price = Face value / Conversion ratio = $1,000 / 25 = $40/share; (3) Parity value (conversion value): market value of shares received if converted today = Conversion ratio × Current stock price. If stock is at $35: parity = 25 × $35 = $875; (4) Conversion premium: how much more the convertible bond trades above parity value. Premium = (Bond price - Parity) / Parity. If bond price = $980: premium = (980-875)/875 = 12%; (5) Investment value (bond floor): the price the convertible would trade at if it had no conversion feature — the straight bond value. If rates rise severely and the stock falls, the bond gravitates toward the bond floor; (6) Delta: the bond's equity sensitivity (between 0 and 1); as stock rises above conversion price, delta approaches 1 (behaves like equity); as stock falls far below, delta approaches 0 (behaves like bond). Institutional use: convertibles allow insurance companies to gain equity upside without exceeding the NAIC common stock limitation, since convertibles are classified as bonds for statutory purposes.",
                   ["Conversion ratio: shares per bond (fixed in indenture).",
                    "Parity value: conversion ratio × current stock price — what you get if you convert today.",
                    "Conversion premium: how much above parity the bond trades; lower premium = cheaper equity option.",
                    "Bond floor: straight bond value — minimum the convertible should trade at regardless of stock performance."]),
            _teach("Floating Rate Notes, Zero-Coupon Bonds, and TIPS",
                   "Floating Rate Notes (FRNs): coupons reset periodically based on a benchmark rate plus a spread. Post-LIBOR transition: benchmark is now SOFR (Secured Overnight Financing Rate). Example: 5-year FRN, SOFR + 120 bps, quarterly reset. When SOFR = 5.0%: quarterly coupon = (5.0% + 1.20%) / 4 = 1.55%. Key property: duration ≈ time to next reset (typically 3 months). FRNs are nearly immune to interest rate risk — their price stays near par because the coupon adjusts with rates. Insurance companies use FRNs in short-duration buckets or when rates are expected to rise. Zero-Coupon Bonds: pay no periodic coupons; sold at a deep discount to face value; face value paid at maturity. Price = Face / (1+y)^n. Duration = Maturity exactly (no earlier cash flows to reduce weighted average). OID (Original Issue Discount) tax: the IRS treats the annual accrual of discount as phantom interest income. Holder must pay tax each year on the imputed interest even though no cash is received. Tax-exempt investors (pension funds, endowments) can hold zeros without OID tax drag. Inflation-Linked Securities (TIPS): issued by US Treasury; principal adjusts upward with CPI-U. If initial principal $1,000 and CPI-U rises 3%: adjusted principal = $1,030. Coupon applied to adjusted principal: if real coupon = 1.5%, coupon payment = 1.5% × $1,030 = $15.45 vs. $15 without inflation. At maturity: investor receives the inflation-adjusted principal ($1,030 in this case), providing full purchasing power protection. Break-even inflation rate: difference between nominal Treasury yield and TIPS real yield. If 10-year Treasury = 4.5%, 10-year TIPS = 1.8%, break-even = 2.7% — the market expects 2.7% annual CPI.",
                   ["FRN: SOFR + spread; duration ≈ 0.25 years (quarterly reset); price stays near par regardless of rates.",
                    "Zero-coupon: Price = Face/(1+y)^n; Duration = Maturity; OID tax = annual phantom income.",
                    "TIPS: principal × (1 + CPI change); real coupon applied to adjusted principal; at maturity receive adjusted principal.",
                    "TIPS break-even: nominal yield minus real (TIPS) yield = expected inflation built into market prices."]),
            _example("How a Life Insurer Uses All Four Bond Types",
                     "Pacific Mutual Life's general account fixed income strategy ($30B): (1) Convertibles ($1.5B, 5%): 30 positions in BBB-rated issuers offering 250-350 bps above Treasury non-callables; classified as bonds for NAIC statutory purposes despite equity option; used where management wants equity exposure within bond concentration limits. (2) FRNs ($3B, 10%): short-duration bucket; SOFR + 85-150 bps spread; average duration 0.23 years; held when yield curve is expected to flatten or rise; funded with short-dated policyholder reserves. (3) Zero-coupon Treasuries/STRIPS ($2B, 7%): exclusively for tax-exempt pension separate accounts and endowment clients; provides exact liability-matching duration (duration = maturity); 30-year STRIPS at 4.2% yield priced at 1000/(1.042)^30 = $291 per $1,000 face; (4) TIPS ($4B, 13%): inflation hedge against cost-of-living-adjusted (COLA) annuity liabilities; $4B TIPS portfolio with 1.8% real yield protects against 3% inflation eroding purchasing power of annuity obligations. Real returns guaranteed; nominal income floats with inflation.",
                     "The mix of these four bond types allows Pacific Mutual to simultaneously manage interest rate risk (FRNs reduce rate sensitivity), inflation risk (TIPS hedge COLA liabilities), duration extension (zeros match long liabilities), and equity participation (convertibles within bond regulatory limits)."),
            _flash("A convertible bond has a conversion ratio of 40 shares and the underlying stock is trading at $18. The bond is priced at $850. What is the conversion premium?",
                   "Step 1: Parity value = Conversion ratio × Stock price = 40 × $18 = $720. Step 2: Conversion premium = (Bond price - Parity value) / Parity value = ($850 - $720) / $720 = $130 / $720 = 18.1%. Interpretation: investors are paying 18.1% above the current equity value to hold the convertible bond instead of the stock directly. This premium represents the value of the bond's downside protection — if the stock falls to $10, the bond will still trade near its straight bond value (bond floor), not the $400 equity conversion value."),
            _mcq("A 10-year floating rate note has a coupon of SOFR + 150 bps, resetting quarterly. SOFR is currently 4.5%. What is the bond's APPROXIMATE modified duration?",
                 ["10.0 years — FRNs have the same duration as their maturity",
                  "5.0 years — duration is always half the maturity for floating rate bonds",
                  "0.25 years — the bond resets to market rates every 90 days, so interest rate sensitivity is approximately one quarter year",
                  "1.5 years — duration equals the spread portion of the coupon"],
                 2,
                 "An FRN's modified duration is approximately equal to the time until its next coupon reset. Since this FRN resets quarterly (every 90 days = 0.25 years), its price will always converge back to par at each reset date. If rates rise, the coupon rate increases at the next reset, keeping the bond priced near par — there is minimal interest rate sensitivity between resets. Duration ≈ 0.25 years for a quarterly-reset FRN, regardless of the bond's stated maturity."),
            _mcq("A 20-year zero-coupon bond is issued at a yield of 5.0%. Which of the following is CORRECT about this bond?",
                 ["Its duration is less than 20 years because the OID accruals create implicit earlier cash flows",
                  "Its duration is exactly 20 years; a taxable investor must recognize OID phantom interest annually even though no cash is received",
                  "It has the same tax treatment as a regular coupon bond — tax is paid only when coupons are received",
                  "Its price is always $1,000 because zero-coupon bonds are always issued at par"],
                 1,
                 "A zero-coupon bond's duration equals its maturity exactly (20 years), because all cash flow occurs at maturity with no intermediate payments. For taxable investors, the IRS requires annual recognition of OID (Original Issue Discount) — the imputed phantom interest that accrues as the bond's price increases toward par. Even though no cash coupon is paid, the investor has ordinary income each year based on the yield accrual, creating a cash tax liability without a corresponding cash receipt. Tax-exempt investors (pension funds, IRAs, endowments) avoid this OID drag."),
            _mcq("An investor buys $1M face value TIPS with a 1.5% real coupon. Over the first year, CPI-U rises 3.5%. What is the investor's coupon payment after the inflation adjustment?",
                 ["$15,000 (1.5% × $1,000,000 — CPI adjustment does not affect coupon amount)",
                  "$15,525 (1.5% × $1,000,000 × 1.035 = $15,525 — coupon applied to CPI-adjusted principal)",
                  "$20,000 (1.5% + 3.5% CPI = 5.0% × $1,000,000 total)",
                  "$35,000 (CPI adjustment only — real coupon is irrelevant)"],
                 1,
                 "TIPS coupon = Real coupon rate × Inflation-adjusted principal. After 3.5% inflation: Adjusted principal = $1,000,000 × 1.035 = $1,035,000. Coupon = 1.5% × $1,035,000 = $15,525. Both the coupon payments AND the final principal repayment adjust with inflation. This is the defining feature of TIPS — the real yield (1.5%) is locked in, while the nominal dollar amounts grow with inflation. If deflation occurs, the Treasury guarantees repayment of at least the original face value at maturity."),
            _mcq("An insurance company is selecting a bond for a segment of its general account backing 30-year payout annuities. The primary objective is to achieve a portfolio duration of exactly 30 years. Which bond type is MOST suitable?",
                 ["A 30-year callable corporate bond with a 6% coupon",
                  "A 30-year Treasury STRIP (zero-coupon bond) with maturity in exactly 30 years",
                  "A 30-year floating rate note (SOFR + 200 bps, monthly reset)",
                  "A 30-year convertible bond with 30 shares per $1,000 face value"],
                 1,
                 "A 30-year zero-coupon bond (STRIP) has a duration of exactly 30 years — matching the liability duration precisely. The callable corporate bond has shorter duration than 30 years (coupons shorten duration, and the call option shortens it further under certain rate scenarios). The FRN has duration of approximately 1/12 year (monthly reset) — far too short. The convertible has duration that changes with equity value and is shorter than 30 years due to the conversion option. The STRIP is the pure duration-matching instrument."),
            _mcq("The 'break-even inflation rate' derived from comparing nominal Treasury yields and TIPS real yields represents:",
                 ["The minimum inflation rate at which the government must pay a coupon on TIPS",
                  "The annual CPI rate at which a TIPS investor and a nominal Treasury investor earn the same total return over the holding period",
                  "The maximum deflation rate that TIPS can protect against before the principal floor applies",
                  "The Federal Reserve target inflation rate for monetary policy purposes"],
                 1,
                 "Break-even inflation rate = Nominal Treasury yield minus TIPS real yield. Example: if the 10-year Treasury yields 4.5% and the 10-year TIPS yields 1.8%, the break-even rate is 2.7%. If actual inflation over the 10-year period averages MORE than 2.7%, the TIPS investor outperforms (the principal/coupon adjustments exceed the nominal bond's extra yield). If actual inflation averages LESS than 2.7%, the nominal Treasury investor outperforms. The break-even rate represents the market's consensus expectation for average annual CPI over the bond's life."),
            _scenario(
                "A corporate treasurer at ABC Capital is preparing to issue $500M in bonds. The treasurer must choose between: Option 1 — Straight (non-callable) 10-year bond at 5.5% coupon. Option 2 — Callable bond (10NC3) at 6.0% coupon. Option 3 — Convertible bond at 4.5% coupon, convertible into 25 shares per $1,000 at $40/share (current stock price $32).",
                "Which structure is MOST beneficial for ABC Capital and from an investor perspective, which structure provides the BEST risk-adjusted return?",
                [("Option 2 is best for the issuer and investors — 6% provides highest income, which always wins", False,
                  "The 6% coupon on the callable bond costs the issuer more than Option 3 but less than Option 1 in certain rate scenarios. For investors, a 6% callable bond may underperform a 5.5% non-callable on a risk-adjusted basis (OAS) once the call option's value is subtracted."),
                 ("Option 3 (convertible) is MOST beneficial for ABC Capital: lowest coupon cost (4.5% vs 5.5% and 6.0%) — the company sells the equity option embedded in the conversion feature, reducing interest expense. From investor perspective, the convertible provides upside participation if ABC stock appreciates above $40 (current price $32; conversion premium = 25%), while providing downside protection through the bond floor", True,
                  "Correct. ABC sells equity optionality to reduce borrowing cost — the 4.5% coupon is 100 bps below the straight bond, saving $5M per year in interest. Investors accept the lower yield for the equity option. If ABC's stock rises above $40, investors convert and participate in equity gains. If stock falls, investors hold a 4.5% bond. The convertible issuer benefits from: (1) lower cost of debt; (2) potential equity dilution only at $40+ per share (beneficial timing — issuing equity at high stock prices). Straight bond (Option 1) costs the most with no refinancing flexibility. Callable (Option 2) provides refinancing flexibility but at 6% initial cost."),
                 ("Option 1 (straight bond) is most beneficial for investors because it offers the highest yield and no embedded options to worry about, providing the cleanest risk profile", False,
                  "Option 1 does offer the cleanest risk profile (no embedded option), and at 5.5% the YTM exceeds the convertible's 4.5%. However, whether it is 'best' for investors depends on the OAS comparison (is 5.5% above or below the fair credit spread?) and the investor's view of the equity. For investors who want both bond protection and equity participation, the convertible at 4.5% may offer better total return — the equity option has value that makes the lower coupon worthwhile.")]
            ),
        ]
    )

    m2["concepts"] = [c3, c4]
    ch["modules"] = [m1, m2]
    return ch

# BUILD & FLATTEN
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

def build_seed():
    course_id = _id()
    loma = {
        "id": course_id,
        "slug": "loma-357",
        "name": "LOMA 357",
        "title": "Institutional Investing: Principles and Practices",
        "certification": "LOMA",
        "description": "Master institutional investing concepts for the LOMA 357 exam â€” from basic asset classes to advanced portfolio management and regulation.",
        "color": "#FF6B35",
        "icon": "Shield",
        "order": 1,
        "chapters": [
            _build_ch1(course_id),
            _build_ch2(course_id),
            _build_ch3(course_id),
            _build_ch4(course_id),
            _build_ch5(course_id),
            _build_ch6(course_id),
            _build_ch7(course_id),
            _build_ch8(course_id),
            _build_ch9(course_id),
            _build_ch10(course_id),
            _build_ch11(course_id),
            _build_ch12(course_id),
            _build_ch13(course_id),
        ],
    }
    # Progressive XP: later chapters reward more to reflect increasing complexity
    _CHAPTER_XP = {1:20,2:22,3:25,4:28,5:30,6:33,7:35,8:38,9:40,10:43,11:45,12:50,13:55}
    for ch in loma["chapters"]:
        xp = _CHAPTER_XP.get(ch["order"], 25)
        for m in ch["modules"]:
            for c in m["concepts"]:
                c["xp_reward"] = xp
    return [loma]


def flatten_for_db(courses):
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
    """Seed LOMA 357 into DB. Skip if already present with correct data."""
    existing_loma = await db.courses.find_one({"slug": "loma-357"})
    if existing_loma:
        return  # already seeded

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

    print(f"[seed] LOMA 357 seeded: {len(cs)} courses, {len(chs)} chapters, "
          f"{len(ms)} modules, {len(cps)} concepts, {len(ls)} lessons")
