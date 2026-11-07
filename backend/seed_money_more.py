"""Money Basics, chapter 2: "Plan it and grow it". Uses the interactive lesson types (chat, swipe, slider, budget).

Added to the live course without touching chapter 1 (so learners keep their progress). Rupees throughout; the figures
are illustrations at assumed rates, never promises of returns. Maths is checked in tests/check_money_more.py.
"""
from seed_data import _id, _intro, _teach, _example, _flash, _mcq, _concept
from seed_finance import _choice, _outcome

CHAPTER_KEY = "plan-it-and-grow-it"


def _chat(title, scene, messages, takeaway):
    return {"id": _id(), "type": "chat", "content": {
        "title": title, "scene": scene, "takeaway": takeaway,
        "messages": [{"who": w, "name": n, "text": t} for (w, n, t) in messages]}}


def _swipe(instruction, cards):
    return {"id": _id(), "type": "swipe", "content": {
        "instruction": instruction, "cards": [{"text": t, "answer": a, "why": y} for (t, a, y) in cards]}}


def _slider(title, intro, kind, controls, takeaway):
    return {"id": _id(), "type": "slider", "content": {
        "title": title, "intro": intro, "kind": kind, "takeaway": takeaway,
        "controls": [{"key": k, "label": lb, "min": mn, "max": mx, "step": st, "value": v, "prefix": pf, "suffix": sf}
                     for (k, lb, mn, mx, st, v, pf, sf) in controls]}}


def _budget(title, intro, income, start, takeaway):
    return {"id": _id(), "type": "budget", "content": {"title": title, "intro": intro, "income": income, "start": start, "takeaway": takeaway}}


def build_money_chapter_two(course_id):
    ch_id = _id()
    ch = {"id": ch_id, "course_id": course_id, "order": 2, "key": CHAPTER_KEY,
          "title": "Plan it and grow it",
          "description": "Plan every month, then let time do the heavy lifting: budgets, compounding and why prices keep rising."}
    m_id = _id()
    m = {"id": m_id, "chapter_id": ch_id, "order": 1, "title": "Plan, grow, protect"}

    # ------------------------------------------------------------------ 1. budget
    c1 = _concept(m_id, 1,
        "Plan your month",
        "Build a simple monthly budget and stick to it without feeling punished.",
        "A budget is not a punishment. It is a plan that tells your money where to go before it disappears. "
        "Start with your income, set aside savings first, then cap needs and wants.",
        "Meera earns ₹30,000. Last month it was gone by the 18th. This month she decides on day one: ₹6,000 saved, "
        "₹15,000 for needs, ₹9,000 for fun. The 18th comes and she still has money for both.",
        ["A budget is a plan made before you spend, not a record of what you already spent.",
         "Savings come first, then needs, then wants.",
         "Small UPI spends are the usual leak, so review them once a month.",
         "50/30/20 is a starting point. Change it to fit your life and income."],
        ["Making a budget so strict that you quit it in two weeks.",
         "Ignoring small, frequent spends because each one is tiny.",
         "Never reviewing it, so the plan and real life drift apart."],
        [
            _intro("Where did it all go?", "Meera earns ₹30,000 a month. By the 18th she is checking her balance and sighing. Let's build her a plan that actually works."),
            _chat("Meera's empty wallet", "A chat after work", [
                ("friend", "Meera", "Lumi, I earn ₹30,000 and by the 18th it's gone. Where does it go?!"),
                ("lumi", "Lumi", "Let's find out. Did you ever write down what you spend?"),
                ("friend", "Meera", "Not really. I just pay by UPI. It never feels like real money."),
                ("lumi", "Lumi", "That is the trap. Tapping a phone feels lighter than handing over cash, so small spends sneak up."),
                ("friend", "Meera", "So I should stop spending?"),
                ("lumi", "Lumi", "No! A budget is a plan, not a punishment. You decide where each rupee goes before the month starts."),
                ("friend", "Meera", "Okay. Where do I start?"),
                ("lumi", "Lumi", "Start with your savings, then your needs, then what is left is guilt-free fun money."),
            ], "Decide where money goes before you spend it, not after."),
            _teach("Tell every rupee what to do",
                   "A budget has four steps. One: write your income. Two: move savings out first. Three: list your needs and give them a limit. Four: whatever is left is your wants money, and you can spend it without guilt. Do this on salary day and check it once a week, not every day, so it stays light.",
                   ["Income in, savings out first", "Needs get a fixed limit", "What is left is guilt-free wants money", "Review once a week, adjust once a month"]),
            _budget("Split Meera's salary", "Meera earns ₹30,000. Drag the sliders to split her money. Needs and wants start too high, so savings are squeezed.", 30000, {"needs": 65, "wants": 30}, "Most people start near 50% needs, 30% wants and 20% savings. Your numbers will differ, and that is fine."),
            _swipe("Budget myth or fact?", [
                ("A budget is only for people who earn very little.", "myth", "Everyone with an income benefits from a plan. Higher earners who never plan often still end the month with nothing left."),
                ("Paying yourself first means moving savings out before you spend.", "fact", "That is exactly it. Savings that wait until the end of the month usually never happen."),
                ("Small UPI payments hardly matter.", "myth", "They matter a lot because they are frequent. ₹150 a day is about ₹4,500 a month."),
                ("50/30/20 is a starting point, not a strict law.", "fact", "It is a handy first draft. If rent eats half your pay, you adjust and still keep savings in the plan."),
            ]),
            _example("The ₹4,500 leak",
                     "Aman checked his UPI history. He found ₹150 a day on snacks and cold drinks, about ₹4,500 a month. He did not quit them. He halved them and moved the saved ₹2,250 into a separate savings account on salary day.",
                     "You rarely need to give things up. Trimming the biggest leak a little, and saving the difference automatically, works better than a dramatic cut."),
            _choice("Meera's friend invites her to a ₹3,000 birthday dinner on the 20th. Her wants money for the month is already used up.",
                    "What is the smartest way to handle it?",
                    [("Pay by credit card and sort it out next month", "bad",
                      "This turns one dinner into a debt that costs interest. If the card bill is not cleared in full, you pay a lot extra on top of ₹3,000.",
                      _outcome(("The dinner", 3000), ("If unpaid for a year", 4533), "At around 3.5% a month, ₹3,000 can grow to about ₹4,500 in a year.")),
                     ("Move ₹1,500 from next month's wants, split the bill with friends, and skip one outing", "good",
                      "A budget is a plan you can bend on purpose. She still goes, she pays from her own money, and she decides what to give up in return."),
                     ("Say no to the invitation without explaining", "ok",
                      "It protects the budget but may cost a friendship moment. Telling friends you are on a plan is usually fine, and cheaper options exist.")]),
            _choice("Ravi is a freelancer. Some months he earns ₹40,000, others only ₹15,000. He does not know how to budget.",
                    "What is a sensible way to budget uneven income?",
                    [("Plan around his best month and hope", "bad", "In a ₹15,000 month the plan collapses and the gap goes on a credit card. Plans built on the best case tend to fail."),
                     ("Plan around his lowest usual month, and put any extra into savings", "good", "Right. Needs and a base saving are covered even in a poor month, and the good months quietly build a cushion."),
                     ("Skip budgeting because the income is uneven", "ok", "Uneven income is the reason to plan, not skip. The plan just has to start from the lowest number.")]),
            _mcq("Meera earns ₹30,000. Using the 50/30/20 starter rule, how much is for wants?", ["₹6,000", "₹9,000", "₹15,000", "₹3,000"], 1,
                 "30% of ₹30,000 is ₹9,000. 50% (₹15,000) is needs and 20% (₹6,000) is savings."),
            _mcq("What does 'pay yourself first' mean?", ["Buy yourself something nice first", "Move your savings out on salary day before spending", "Pay your friends back before bills", "Save only what is left at month end"], 1,
                 "Pay yourself first means the savings leave your spending account right away, so they are safe from the rest of the month."),
            _flash("A budget, in one line", "A plan for your money made before you spend it, so you decide where it goes."),
        ], xp=30)

    # ------------------------------------------------------------------ 2. compounding
    c2 = _concept(m_id, 2,
        "Compounding: your money's snowball",
        "See how time makes small amounts grow, and why starting early matters most.",
        "Compounding means you earn returns on your money and then also on the returns you already earned. "
        "Like a snowball rolling downhill, the longer it rolls, the faster it grows.",
        "Asha invests ₹3,000 a month from age 22 to 32 and then stops. Bala starts at 32 and invests ₹3,000 a month until 52. "
        "At an assumed 10% a year, Asha has about ₹45 lakh at 52 and Bala about ₹23 lakh, even though Bala put in twice as much.",
        ["Compounding is returns earning returns.",
         "Time matters more than amount: start early, even with a small sum.",
         "Rule of 72: divide 72 by the yearly rate to estimate the years it takes to double.",
         "Compounding also works against you on debt, such as unpaid credit card bills."],
        ["Waiting to start until you can invest a 'big' amount.",
         "Taking money out early and breaking the snowball.",
         "Treating an assumed rate as a promise. Real returns move up and down."],
        [
            _intro("The snowball", "Imagine rolling a tiny snowball down a long hill. At first it barely grows. Near the bottom it is huge. That is compounding, and it rewards those who start early."),
            _chat("Two friends, one big difference", "Riya asks Lumi about starting to invest", [
                ("friend", "Riya", "I'm 22. My friend says I should invest ₹3,000 a month. I'll start when I earn more at 32."),
                ("lumi", "Lumi", "Let me show you two people. Asha invests ₹3,000 a month from 22 to 32, then stops. Bala starts at 32 and invests ₹3,000 a month for 20 years."),
                ("friend", "Riya", "Bala invests for twice as long. So Bala wins, right?"),
                ("lumi", "Lumi", "At an assumed 10% a year, Asha ends with about ₹45 lakh at age 52. Bala has about ₹23 lakh."),
                ("friend", "Riya", "What?! Asha put in only ₹3.6 lakh. Bala put in ₹7.2 lakh!"),
                ("lumi", "Lumi", "Asha's money had 10 extra years to snowball. Time beat the amount."),
                ("friend", "Riya", "Okay. I'm starting this month, even with a small amount."),
            ], "Starting early, even small, usually beats starting late and big. Rates are assumed, never guaranteed."),
            _teach("Interest on interest",
                   "If you invest ₹10,000 and it grows 8% in a year, you have ₹10,800. Next year the 8% is earned on ₹10,800, not just the original ₹10,000. That extra bit is compounding. It looks tiny in year one and huge after twenty. Returns are not guaranteed in the real world, but the pattern shows why patience pays.",
                   ["Year 1: ₹10,000 becomes ₹10,800", "Year 2: you earn on ₹10,800", "The gap between 'simple' and 'compound' grows every year", "Real returns vary; rates here are examples"]),
            _slider("Play with time", "Drag the sliders. Watch what happens when you give your money more years.", "growth",
                    [("monthly", "Invest every month", 500, 20000, 500, 5000, "₹", ""), ("years", "For how many years", 1, 40, 1, 10, "", " yrs"), ("rate", "Assumed yearly growth", 4, 15, 1, 10, "", "%")],
                    "Add years before you add rupees. Ten more years usually changes the result more than doubling the monthly amount."),
            _example("₹10,000 and patience",
                     "A one-time ₹10,000 growing at an assumed 8% a year becomes about ₹21,589 in 10 years, about ₹46,610 in 20 years and about ₹1,00,627 in 30 years. The second ten years adds more than the first ten.",
                     "The curve bends upward. Most of the growth comes late, which is why staying invested matters."),
            _swipe("Compounding: myth or fact?", [
                ("You need a lot of money to start investing.", "myth", "Many plans let you start with a few hundred rupees a month. The habit and the years matter more than the starting amount."),
                ("Starting 10 years earlier can beat investing double the amount later.", "fact", "That is what Asha and Bala showed. The early money had more time to snowball."),
                ("Compounding means you only earn on what you put in.", "myth", "That is simple interest. Compounding also earns on the returns you have already made."),
                ("Compounding works against you on unpaid credit card debt.", "fact", "Interest is charged on the unpaid balance including earlier interest, so debt can snowball too."),
                ("If you wait long enough, a high return is guaranteed.", "myth", "Assumed rates are examples. Markets rise and fall, and no one can promise a rate."),
            ]),
            _choice("Riya is 22 and can spare ₹3,000 a month, but her friend says to wait until she earns more at 32.",
                    "What is the smartest move?",
                    [("Wait until 32 so she can invest a bigger amount", "bad",
                      "Waiting costs her the years that do the heavy lifting. A late start needs far bigger amounts to catch up.",
                      _outcome(("Saved by 32", 0), ("If she had started with ₹1,000 a month", 206552), "At an assumed 10%, even ₹1,000 a month from 22 to 32 becomes about ₹2 lakh.")),
                     ("Start now with an amount she will not miss, and raise it as her pay grows", "good",
                      "Right. A small start builds the habit and gives the money time. Raising it later makes it even stronger."),
                     ("Skip all fun for years and put in her entire salary", "ok",
                      "Strong effort, but unsustainable. Plans you can keep up for decades beat dramatic ones you drop in a few months.")]),
            _choice("Neha owes ₹20,000 on her credit card, which charges around 3.5% a month. She plans to pay only the minimum for a while.",
                    "Why is this risky?",
                    [("The interest compounds, so the debt grows faster and faster", "good",
                      "Yes. At around 3.5% a month, ₹20,000 can turn into about ₹30,000 in a year if unpaid. Compounding is great for savings and costly for debt.",
                      _outcome(("Owed today", 20000), ("After a year unpaid", 30221), "3.5% a month compounds to about 51% in a year.")),
                     ("It is not risky because the minimum is small", "bad", "A small minimum feels harmless but most of it goes to interest, so the balance barely falls."),
                     ("It only matters if she buys more things", "ok", "New purchases make it worse, but even with no new spending the unpaid balance keeps growing.")]),
            _mcq("Using the rule of 72, about how many years does money take to double at 8% a year?", ["4 years", "9 years", "12 years", "18 years"], 1,
                 "72 divided by 8 is 9. It is a quick estimate, not an exact figure."),
            _mcq("Which gives compounding the most help?", ["A bigger starting amount only", "More time invested", "Checking the price daily", "Withdrawing gains each year"], 1,
                 "Time is the key ingredient. Leaving money invested lets returns earn returns."),
            _flash("Compounding in one line", "Your returns earn returns, so growth speeds up over time."),
        ], xp=30)

    # ------------------------------------------------------------------ 3. inflation
    c3 = _concept(m_id, 3,
        "Inflation: the silent thief",
        "Understand why prices rise and why money sitting idle slowly loses value.",
        "Inflation is the slow rise in prices. The same ₹100 buys less each year, so money that earns nothing quietly loses what it can buy.",
        "A snack that costs ₹100 today could cost about ₹179 in 10 years at 6% inflation. ₹1,00,000 kept idle for those 10 years "
        "would still be ₹1,00,000 on paper but buy only about ₹56,000 worth of things.",
        ["Inflation means things cost more over time.",
         "Idle cash loses buying power even though the number stays the same.",
         "To keep up, your money should earn at least about the inflation rate over time.",
         "Your income should grow too, or you slowly get poorer."],
        ["Thinking money is 'safe' just because the balance does not fall.",
         "Ignoring inflation when planning goals 10 or 20 years away.",
         "Taking more risk than you can handle just to beat inflation."],
        [
            _intro("Why was it cheaper before?", "Ask your parents what a movie ticket cost when they were young. Prices crept up all those years. That creeping is inflation."),
            _chat("The chai that got dearer", "Lumi and Kabir talk about prices", [
                ("friend", "Kabir", "My dad says chai was ₹2 when he was in college. Now it's ₹20!"),
                ("lumi", "Lumi", "That is inflation: prices rise a little every year and add up."),
                ("friend", "Kabir", "But the ₹100 in my drawer still says ₹100."),
                ("lumi", "Lumi", "The note stays the same. What it can buy shrinks. With 6% inflation, in 10 years you'd need about ₹179 to buy what ₹100 buys today."),
                ("friend", "Kabir", "So the money in my drawer is quietly losing power?"),
                ("lumi", "Lumi", "Yes. Not from falling in number, but from buying less. That is why idle cash is not as safe as it feels."),
            ], "Money that earns nothing loses buying power every year."),
            _teach("Why things get dearer",
                   "Prices rise when many people want things and supply cannot keep up, when it costs more to make or transport goods, and when the amount of money in the economy grows. Governments and central banks try to keep it low and steady. In recent years India's inflation has often been around 4 to 6% a year, though it changes from year to year.",
                   ["Demand rises faster than supply", "Production and transport costs go up", "Central banks aim to keep it steady", "A few percent a year compounds a lot over a decade"]),
            _slider("What will it cost later?", "Move the sliders to see what today's prices turn into, and what idle money can still buy.", "inflation",
                    [("price", "Price or savings today", 1000, 200000, 1000, 100000, "₹", ""), ("years", "After how many years", 1, 30, 1, 10, "", " yrs"), ("rate", "Inflation per year", 2, 10, 1, 6, "", "%")],
                    "Over 10 years at 6%, prices go up about 79%. Your money has to grow at least that fast just to stand still."),
            _example("The idle ₹1,00,000",
                     "Dev keeps ₹1,00,000 in a cupboard for 10 years. At 6% inflation, things that cost ₹1,00,000 today will cost about ₹1,79,000. His cupboard cash buys only about ₹55,800 worth of what it bought before.",
                     "The note did not shrink. The shop prices grew. That gap is the price of leaving money idle."),
            _swipe("Inflation: myth or fact?", [
                ("If my bank balance never falls, my money is safe from every risk.", "myth", "The number may stay the same, but if prices rise, it buys less. That hidden loss is inflation risk."),
                ("Inflation makes things cost more over time.", "fact", "That is the definition. A little each year adds up over many years."),
                ("Cash in a cupboard earns interest.", "myth", "Cash at home earns nothing, so it loses buying power every year."),
                ("Your income should grow at least as fast as prices.", "fact", "If prices rise 6% and your pay rises 3%, you can afford less each year."),
                ("Prices fall every year in India.", "myth", "Over long periods prices have mostly risen, with different speeds in different years."),
            ]),
            _choice("Dev has ₹1,00,000 saved for a goal 10 years away. He keeps it in a cupboard because it feels safest.",
                    "What is the best thing he can learn from inflation?",
                    [("Keep it at home. The number will never fall", "bad",
                      "True, but at 6% inflation it would buy only about ₹56,000 worth in 10 years. Zero risk of the number falling is not zero risk of losing value.",
                      _outcome(("Cash today", 100000), ("Buying power after 10 years", 55839), "Idle money loses roughly 44% of what it can buy over 10 years at 6% inflation.")),
                     ("Put it somewhere that earns interest or returns, matched to when he needs it", "good",
                      "Right. Money that earns about the inflation rate or more keeps its buying power. Safer options such as a bank deposit for near goals and long-term options for far goals fit different timelines. This is education, not advice."),
                     ("Spend it all now before prices rise", "ok", "Spending before prices rise is one response, but it means giving up the goal. The aim is to keep the money's power for the goal.")]),
            _choice("Priya earns ₹30,000. Her company gives a 3% raise, but prices have risen 6% this year.",
                    "What has really happened to her pay?",
                    [("She is better off because the number went up", "bad", "₹30,900 sounds higher, but with prices up 6% it buys less than her old ₹30,000 did.",
                      _outcome(("Salary", 30000), ("Buying power after raise", 29151), "A 3% raise against 6% inflation is a small pay cut in real terms.")),
                     ("Her pay fell in real terms, so she should ask for more or look for growth", "good", "Right. Raises should be compared with inflation. Below it, you are slowly getting poorer even as the number rises."),
                     ("Nothing has changed", "ok", "Her rupee amount rose, but her ability to buy things went down.")]),
            _mcq("At 6% inflation, about how much will an item costing ₹100 today cost in 10 years?", ["₹106", "₹160", "₹179", "₹250"], 2,
                 "100 growing at 6% for 10 years is about ₹179, because the rise compounds every year."),
            _mcq("Why is idle cash 'not entirely safe'?", ["Banks lose it", "Inflation reduces what it can buy", "It becomes illegal", "It earns too much interest"], 1,
                 "The number stays the same, but prices rise, so you can buy less. That is the hidden loss."),
            _flash("Inflation in one line", "Prices rise over time, so the same money buys less."),
        ], xp=30)

    m["concepts"] = [c1, c2, c3]
    ch["modules"] = [m]
    return ch
