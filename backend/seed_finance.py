"""Beginner finance tracks for FinLearn (ages 18-23): Money Basics, Stock Market, Bitcoin and Crypto.

Seeded separately from the LOMA course so the two never wipe each other.
All amounts are in rupees. Content is educational, not financial advice.
"""
import uuid

from seed_data import _id, _intro, _teach, _example, _flash, _mcq, _concept

FINANCE_SEED_VERSION = "f4-beginner-tracks"


def _choice(scene, question, choices):
    """Real-life decision lesson. Each choice: (text, verdict, feedback[, outcome]).

    verdict: "good" (best answer), "ok" (safe but not best), "bad" (wrong).
    outcome (optional): {"before": [label, value], "after": [label, value], "note": str}
    """
    out = []
    for ch in choices:
        text, verdict, feedback = ch[0], ch[1], ch[2]
        item = {"text": text, "verdict": verdict, "correct": verdict in ("good", "ok"), "feedback": feedback}
        if len(ch) > 3 and ch[3]:
            item["outcome"] = ch[3]
        out.append(item)
    return {"id": _id(), "type": "scenario", "content": {"scene": scene, "question": question, "choices": out}}


def _outcome(before, after, note):
    return {"before": list(before), "after": list(after), "note": note}


# ---------------------------------------------------------------------------
# MONEY BASICS
# ---------------------------------------------------------------------------

def _money_chapter(course_id):
    ch_id = _id()
    ch = {
        "id": ch_id, "course_id": course_id, "order": 1,
        "title": "Your first salary",
        "description": "Make your money last the month, build a safety cushion, and stay out of the credit card trap.",
    }
    m_id = _id()
    m = {"id": m_id, "chapter_id": ch_id, "order": 1, "title": "Everyday money"}

    c1 = _concept(m_id, 1,
        "Where does your money go?",
        "Split your income into needs, wants and savings, and pay yourself first.",
        "Every rupee has a job before it reaches you. Needs (rent, food, travel) come first, wants (ordering in, "
        "movies, new sneakers) come next, and savings should be paid to you first, not what is left on the 30th.",
        "Priya gets her first salary of ₹25,000. On day one she moves ₹5,000 into savings, then spends the rest "
        "knowing the important part is already done.",
        ["Needs, wants and savings are three different buckets.",
         "Pay yourself first: move savings out the day salary arrives.",
         "A simple starting split is 50% needs, 30% wants, 20% savings. Adjust it to your life.",
         "Tiny daily UPI spends add up faster than big purchases."],
        ["Saving whatever is left at month end (it is usually nothing).",
         "Treating small UPI payments as 'not real spending'.",
         "Setting a savings target so strict you give up in week two."],
        [
            _intro("Salary day!", "It is the 1st and ₹25,000 just landed. By the 20th most people ask, 'Where did it all go?' Let's make sure you never have to."),
            _teach("Three buckets for every rupee",
                   "Think of your salary as three buckets. Needs are things you cannot skip: rent, food, travel, phone recharge. Wants are things that make life fun but are optional: ordering in, concerts, new gadgets. Savings are money you keep for later. The trick is the order. Most people fill needs, then wants, and savings get whatever is left, which is usually zero.",
                   ["Needs: rent, groceries, commute, bills", "Wants: eating out, subscriptions, shopping", "Savings: emergency fund, goals, investing", "Starter rule: 50 / 30 / 20"]),
            _example("The ₹150 coffee",
                     "Karan buys a ₹150 coffee on his way to work, five days a week, paying by UPI so it never feels like cash leaving. He also orders dinner twice a week for ₹300 each. At the end of the month he checks his statement and finds about ₹5,400 went on those two habits alone: ₹3,000 on coffee and ₹2,400 on dinners.",
                     "Small, frequent spends are the ones you do not notice. Check your UPI history once a month."),
            _flash("What does 'pay yourself first' mean?", "Move your savings out on salary day, before you spend on anything else."),
            _choice("Priya's first salary of ₹25,000 just arrived. Rent and bills are ₹11,000. A friend is already planning a weekend trip for ₹6,000 and she wants to go.",
                    "What should Priya do on salary day?",
                    [("Pay the bills, go on the trip, and save whatever is left on the 30th", "bad",
                      "'Save what is left' almost always means saving nothing. After rent, bills and the trip she has ₹8,000 for a whole month of food and travel, and savings become the thing that gets cut.",
                      _outcome(("Savings goal", 5000), ("Saved by the 30th", 500), "She planned to save ₹5,000 and managed ₹500 because savings came last.")),
                     ("Move ₹5,000 to savings right away, pay the bills, and fit the trip into her wants money", "good",
                      "Right. Paying yourself first means the important part is already safe. She can still enjoy the trip, but she has to fit it into what is left after needs and savings. That is the whole skill: spend on purpose.",
                      _outcome(("Savings goal", 5000), ("Saved by the 30th", 5000), "Goal met, rent paid, and she still got her weekend away.")),
                     ("Skip the trip and every fun thing this month and save ₹15,000", "ok",
                      "Disciplined, but hard to keep up. Cutting every want usually ends with a binge a few weeks later. Savings that fit your real life last longer than savings that feel like punishment.")]),
            _teach("Make saving automatic",
                   "Willpower is a weak system. A better one is automation. Set a standing instruction so a fixed amount moves from your salary account to a separate savings account on the day salary arrives. Keep that account in a different app so it is out of sight. You will quickly adjust to living on the rest.",
                   ["Open a separate savings account", "Set an auto-transfer for salary day", "Increase it by ₹500 each time your pay rises"]),
            _choice("Arjun earns ₹18,000 a month. He is always short by the 22nd and does not know why. He has never looked at where the money goes.",
                    "What is the best first step?",
                    [("Take a cheaper phone plan and hope it fixes things", "ok",
                      "A good habit but a random guess. Without knowing where the money goes, you might cut the wrong thing. Look first, then decide."),
                     ("Go through last month's UPI and card history and tag each spend as need, want or savings", "good",
                      "Right. You cannot fix what you cannot see. Ten minutes with your statement usually shows two or three habits that eat most of the leak."),
                     ("Ask his parents for money every month to cover the gap", "bad",
                      "This hides the problem instead of solving it, and next month will look the same. The gap is a clue that spending needs a closer look.")]),
            _mcq("Which of these is a 'need'?", ["Monthly metro pass to reach work", "Ordering dessert every night", "A new pair of limited-edition sneakers", "A game subscription"], 0,
                 "A metro pass to reach work is a need because without it you cannot earn your income. The others are wants, however fun they are."),
            _mcq("Priya earns ₹25,000. Using the 50/30/20 starter rule, how much goes to savings?", ["₹2,500", "₹5,000", "₹12,500", "₹7,500"], 1,
                 "20% of ₹25,000 is ₹5,000. 50% (₹12,500) is needs and 30% (₹7,500) is wants."),
        ], xp=25)

    c2 = _concept(m_id, 2,
        "The emergency fund",
        "Explain why a cash cushion matters and where to keep it.",
        "An emergency fund is money set aside only for surprises: a broken phone, a medical bill, a lost job. "
        "It is not an investment. Its job is to stop a bad day from turning into debt.",
        "Karan's laptop dies two weeks before his project deadline. With ₹30,000 saved he just buys a new one and starts rebuilding the fund. Without it, he would have borrowed on a credit card.",
        ["Aim for 3 to 6 months of essential expenses.",
         "Keep it somewhere safe and easy to reach, like a savings account.",
         "It is for emergencies, not sales or trips.",
         "Start small: even ₹5,000 helps."],
        ["Investing the emergency fund in stocks or crypto.",
         "Dipping into it for wants.",
         "Waiting until you can save a 'big' amount before starting."],
        [
            _intro("The surprise bill", "Life sends surprises at the worst time: a phone that dies, a hospital visit, a job that ends. The question is not if, but who pays when it happens: your savings or a lender?"),
            _teach("What is an emergency fund?",
                   "An emergency fund is a small pile of cash you do not touch until something unexpected and necessary happens. The usual target is three to six months of your essential costs: rent, food, travel, bills. If those cost ₹15,000 a month, the target is ₹45,000 to ₹90,000. That sounds like a lot, so start with one month, or even ₹5,000, and build up.",
                   ["Target: 3 to 6 months of essentials", "Keep it in a savings account you can reach fast", "Do not invest it: you need it to be there, not to grow"]),
            _example("Two friends, one broken phone",
                     "Riya and Dev both have phones that die the same week. Riya has ₹6,000 saved in a savings account, so she buys a basic replacement for ₹5,500 and carries on. Dev has no cushion, so he buys a ₹30,000 phone on a credit card because he needs it for work, pays only the minimum, and is still paying for it a year later with interest.",
                     "A small cushion turns a crisis into an inconvenience."),
            _flash("How big should an emergency fund be?", "About 3 to 6 months of your essential expenses. Start with whatever you can and build up."),
            _choice("Karan's laptop dies two weeks before his project deadline. A new one costs ₹30,000. He has ₹35,000 saved in his emergency fund and a credit card with a ₹50,000 limit.",
                    "How should Karan pay?",
                    [("Put it on the credit card and pay the minimum each month", "bad",
                      "Credit cards charge around 3% a month, roughly 36 to 42% a year, on unpaid balances. Paying the minimum means a ₹30,000 laptop can cost far more over time, and he has savings that exist for exactly this.",
                      _outcome(("Laptop price", 30000), ("Cost after a year of minimum payments (rough)", 40000), "A rough picture: interest alone can add around a third on top over a year.")),
                     ("Use his emergency fund, then start refilling it from next month's salary", "good",
                      "Right. This is exactly what the fund is for. He avoids interest completely, and the plan to rebuild means he is ready for the next surprise.",
                      _outcome(("Laptop price", 30000), ("Total cost paid", 30000), "No interest, no stress. He then tops the fund back up over a few months.")),
                     ("Borrow from a friend and promise to repay next month", "ok",
                      "Better than a high-interest loan, but it puts a friendship on the line if the repayment slips. The fund exists so you do not have to ask.")]),
            _teach("Where to keep it",
                   "The right place for an emergency fund is boring on purpose: a savings account, or a liquid fund your bank or broker offers. You want the money to be there when you need it, with almost no chance of losing value. A share portfolio can fall 20% in a bad month, which is exactly when you may need to withdraw.",
                   ["Savings account: safest and fastest", "Not stocks or crypto: prices can drop when you need cash", "Keep it separate so you do not spend it by mistake"]),
            _choice("Aisha has saved ₹40,000. Her monthly essentials are about ₹13,000. A reel says a hot stock will 'double by December' and she is tempted to put it all in.",
                    "Where should her first ₹40,000 go?",
                    [("All of it into the hot stock, because it might double", "bad",
                      "'Might double' also means 'might halve'. If an emergency hits during a dip, she would have to sell at a loss, or borrow. The first job for this money is safety."),
                     ("About 3 months of essentials (₹39,000) stays in a savings account as her emergency fund", "good",
                      "Right. ₹39,000 covers three months of essentials. Safety first, then investing. Once the fund is built, extra money can go toward growth."),
                     ("Keep it as cash at home in a drawer", "ok",
                      "It is there when she needs it, but cash at home can be lost, stolen or spent on impulse, and it earns nothing. A savings account is just as reachable and earns interest.")]),
            _mcq("Which is the BEST place for an emergency fund?", ["A savings account", "A single stock", "Cryptocurrency", "A friend's business"], 0,
                 "An emergency fund must be safe and quickly available. A savings account does both. Stocks, crypto and a friend's business can lose value or be hard to withdraw exactly when you need the money."),
            _mcq("Aman spends ₹12,000 a month on essentials. What is a 3-month emergency fund target?", ["₹12,000", "₹24,000", "₹36,000", "₹72,000"], 2,
                 "3 x ₹12,000 = ₹36,000. Six months would be ₹72,000, a longer-term goal."),
        ], xp=25)

    c3 = _concept(m_id, 3,
        "Credit cards and EMIs",
        "Understand how credit card interest and 'no-cost EMI' really work.",
        "A credit card is a short loan, not free money. Pay the full bill by the due date and it costs nothing. "
        "Pay only the minimum and interest of around 3% a month kicks in.",
        "Rahul swipes ₹40,000 on a card, then pays only the minimum. One month of interest at 3.5% adds about ₹1,400 to what he owes, and it keeps growing.",
        ["Pay your full bill by the due date to avoid interest.",
         "Interest on unpaid balances is often around 36 to 42% a year.",
         "Minimum due keeps you in debt, it does not clear it.",
         "'No-cost EMI' usually still has a cost, just hidden somewhere else."],
        ["Paying only the minimum due.",
         "Using a card to buy things you cannot afford now.",
         "Treating EMI as 'small' without adding up the total."],
        [
            _intro("Swipe now, pay later?", "The card in your wallet feels like free money for 40 days. It is not. It is a loan, and how you repay it decides whether it is a helpful tool or an expensive trap."),
            _teach("How a credit card really works",
                   "When you swipe, the bank pays the shop and you owe the bank. If you pay the whole bill by the due date, you pay no interest. If you pay anything less, even the 'minimum due', interest starts on the unpaid amount, usually around 3% a month. That is roughly 36 to 42% a year. For comparison, a savings account pays a few percent a year.",
                   ["Pay in full: zero interest", "Pay minimum: interest on the rest, about 3% a month", "Missed payments also lower your credit score"]),
            _example("The ₹40,000 shopping weekend",
                     "Rahul buys a phone and some clothes for ₹40,000 on his new credit card. When the bill arrives he sees 'Minimum due: ₹2,000' and pays only that. Next month the bill shows he owes about ₹39,400, which looks like he is making progress, but that includes around ₹1,400 of interest. If he keeps adding new purchases, the balance barely moves.",
                     "The minimum due is built to keep you paying interest for a long time."),
            _flash("What does paying only the 'minimum due' do?", "Keeps the account in good standing but charges interest on the rest, so the debt shrinks very slowly."),
            _choice("Rahul's credit card bill is ₹40,000. The due date is tomorrow. He has ₹40,000 in his bank account but it was meant for a weekend trip with friends.",
                    "What should Rahul do?",
                    [("Pay just the minimum (₹2,000) and go on the trip", "bad",
                      "The unpaid ₹38,000 starts charging interest at about 3.5% a month. The trip becomes more expensive than it looks.",
                      _outcome(("Bill", 40000), ("Owed after one month if left unpaid", 41400), "About ₹1,400 of interest in one month, roughly 42% a year.")),
                     ("Pay the full ₹40,000 and plan a cheaper trip", "good",
                      "Right. Paying in full means zero interest, and the card did its job as a convenience, not a loan. He can still have fun on a smaller budget.",
                      _outcome(("Bill", 40000), ("Owed after payment", 0), "No interest, no stress, and a clean record.")),
                     ("Pay half (₹20,000) and keep the rest for the trip", "ok",
                      "Better than the minimum, but the other ₹20,000 still charges around 3.5% a month. If he can pay in full, he should.")]),
            _teach("'No-cost EMI' is not free",
                   "A shop offers a ₹60,000 phone on 'no-cost EMI' for 6 months. It sounds free, but a 'no-cost' plan usually works one of two ways: the interest is hidden inside the price (so you lose a cash discount), or there are processing fees and taxes on the interest. Always compare the total you will pay with the cash price, and only buy if the monthly amount fits your budget without strain.",
                   ["Total paid = EMI x months + any fees", "Ask: what is the discount if I pay in full?", "An EMI you can barely afford is a warning sign"]),
            _choice("Meera wants a ₹60,000 phone. The shop offers 'no-cost EMI' of ₹10,000 for 6 months. Her take-home pay is ₹28,000 and rent plus essentials already take ₹20,000.",
                    "What should Meera do?",
                    [("Buy it now. It says no-cost, so there is nothing to worry about", "bad",
                      "₹10,000 a month on top of ₹20,000 of essentials leaves her ₹-2,000 short every month. 'No-cost' describes the interest, not whether she can afford it."),
                     ("Check the total cost against the cash price, then buy a cheaper phone that fits her budget", "good",
                      "Right. If a purchase makes you short every month, it is too expensive regardless of the EMI label. A phone at half the price keeps her budget healthy."),
                     ("Take the EMI but ask her parents to cover the shortfall", "ok",
                      "It might work in the short term, but she is building a habit of buying beyond her income. It is a safety net, not a plan.")]),
            _mcq("You pay only the 'minimum due' on your credit card bill. What happens to the rest of the balance?", ["It is forgiven", "It is charged interest", "It is paid by the bank", "It disappears after 30 days"], 1,
                 "Any unpaid balance keeps accruing interest, usually around 3% a month. The minimum due only keeps your account in good standing."),
            _mcq("Which habit keeps a credit card cost-free?", ["Paying the full bill by the due date", "Paying the minimum due", "Paying whenever you remember", "Using it only for big purchases"], 0,
                 "Paying the entire statement balance by the due date means you pay no interest."),
        ], xp=25)

    m["concepts"] = [c1, c2, c3]
    ch["modules"] = [m]
    return ch


# ---------------------------------------------------------------------------
# STOCK MARKET
# ---------------------------------------------------------------------------

def _stock_chapter(course_id):
    ch_id = _id()
    ch = {
        "id": ch_id, "course_id": course_id, "order": 1,
        "title": "Own a slice of a business",
        "description": "Learn what a share is, how a monthly SIP works, and why spreading your money protects you.",
    }
    m_id = _id()
    m = {"id": m_id, "chapter_id": ch_id, "order": 1, "title": "Stock market basics"}

    c1 = _concept(m_id, 1,
        "What is a share?",
        "Explain what owning a share means and why a low price is not the same as a bargain.",
        "A share is a tiny slice of ownership in a company. If the business does well, your slice can become more valuable. "
        "If it does badly, it can lose value.",
        "Neha buys one share of a large company. She now owns a small part of it. If the company grows its profits, other investors may pay more for her share.",
        ["A share is part ownership of a company.",
         "You can earn from the price going up and from dividends.",
         "A low price does not mean cheap. Look at the business.",
         "Prices move on results, news and mood."],
        ["Judging a stock by its share price alone.",
         "Following tips from social media or chat groups.",
         "Investing money you will need within a year."],
        [
            _intro("You can own a piece of a company", "Every company you use, from your phone network to the biscuits you buy, can be owned in tiny slices by people like you. Those slices are called shares."),
            _teach("What a share really is",
                   "When a company needs money to grow, it can sell small pieces of ownership called shares. If you buy one, you own a small part of that business. Your share can gain value if the company earns more and others want to buy in. Some companies also pay a dividend, a small payout of profits. But prices also fall when results disappoint or investors get nervous.",
                   ["Share = a small part of ownership", "Earn from price rising and from dividends", "You can lose money if the price falls"]),
            _example("Two stocks, same ₹8 price?",
                     "Neha's cousin tells her about a stock priced at ₹8. 'It is so cheap, ₹8000 gets you 1000 shares!' Meanwhile another stock costs ₹2,500 per share. Neha realises the ₹8 price tells her nothing. The ₹8 company might be tiny and losing money, while the ₹2,500 company might be a giant that earns a lot. What matters is what the whole company is worth and what it earns, not the price of one share.",
                     "A low price per share does not mean good value."),
            _flash("Is a ₹8 share cheaper than a ₹2,500 share?", "Not necessarily. What matters is the company's value and earnings, not the price of one share."),
            _choice("Neha's cousin sends her a message: 'Buy this ₹8 stock today! It will be ₹80 soon. I already put in ₹20,000.' She has ₹15,000 saved.",
                    "What should Neha do?",
                    [("Put in her ₹15,000 now so she does not miss the jump", "bad",
                      "A promise like 'it will be ₹80 soon' is a tip, not research, and cheap penny stocks are easy to manipulate. Putting in money you cannot afford to lose is what turns a tip into a disaster.",
                      _outcome(("Neha's savings", 15000), ("If the stock halves", 7500), "Half the price means half the money gone, and tiny stocks can fall much further.")),
                     ("Look up what the company does, whether it earns profit, and why the price is so low, and only invest an amount she can afford to lose", "good",
                      "Right. Check the business before the price. If she cannot find a clear reason the company is worth owning, she can skip it. The skill is asking questions, not chasing a number.",
                      _outcome(("Neha's savings", 15000), ("If she invests ₹1,000 and it halves", 14500), "A small test costs little even if it goes wrong, and she learns how it feels.")),
                     ("Ignore it and do nothing", "ok",
                      "Safe, and a perfectly fine choice. But you can also use tips as practice: look the company up and see what you learn.")]),
            _teach("Why prices move",
                   "A share price changes because buyers and sellers keep changing their minds. Good results, a new product or lower interest rates can push prices up. Bad news, a scandal or fear about the economy can push them down. In the short term, mood moves prices as much as facts. Over many years, a company's earnings matter most. That is why experienced investors think in years, not days.",
                   ["Short term: news and mood", "Long term: earnings and growth", "Only invest money you will not need soon"]),
            _choice("Dev invested ₹5,000 in a large company's shares. The next week the price falls 8% after a bad market day. He checks the app every hour and cannot sleep.",
                    "What is the healthiest response?",
                    [("Sell everything immediately before it falls more", "bad",
                      "Selling after a drop locks in the loss. If the company is still healthy, short-term dips are normal. Panic-selling is how people turn temporary falls into permanent ones."),
                     ("Remember why he invested, check the company is still doing fine, and stop checking the app every hour", "good",
                      "Right. Prices wobble. If the reasons you bought still hold and the money is for the long term, a dip is just noise. Checking constantly makes it feel worse."),
                     ("Invest another ₹5,000 immediately because it is on sale", "ok",
                      "Adding to a good company at a lower price can work, but doing it in a panic, or with money you need, is risky. Decide with a plan, not a feeling.")]),
            _mcq("What does owning a share mean?", ["You own a small part of the company", "You have lent money to the government", "You are guaranteed profit", "You work for the company"], 0,
                 "A share represents part ownership of a company. It carries risk and no guarantee of profit."),
            _mcq("A stock costs ₹8. Another costs ₹2,500. Which is the better investment?", ["The ₹8 stock, because it is cheaper", "The ₹2,500 stock, because it costs more", "You cannot tell from the price alone", "Neither, shares are always bad"], 2,
                 "The price of one share says nothing about value. You need to know what the whole company is worth and how it earns money."),
        ], xp=25)

    c2 = _concept(m_id, 2,
        "SIP and index funds",
        "Explain how a monthly SIP in an index fund lets you invest small amounts steadily.",
        "A SIP (systematic investment plan) puts a fixed amount into an investment every month. "
        "An index fund spreads that money across a whole list of big companies, like the Nifty 50, so you do not have to pick winners.",
        "Arjun starts a ₹1,000 monthly SIP in a Nifty 50 index fund. When the market dips he automatically buys more units for the same ₹1,000.",
        ["SIP = a fixed amount invested on a schedule.",
         "An index fund tracks a list of companies, like the Nifty 50.",
         "Regular investing means you buy more when prices are low.",
         "Time in the market matters more than timing the market."],
        ["Stopping a SIP the first time markets fall.",
         "Waiting for the 'perfect' time to start.",
         "Choosing funds only by last year's returns."],
        [
            _intro("Start with ₹500", "You do not need lakhs to begin. Many funds let you start a SIP with just ₹500 a month. The magic is not the amount, it is the habit."),
            _teach("Mutual funds, index funds and SIPs",
                   "A mutual fund collects money from many people and invests it in a basket of shares. An index fund is a simple type that just copies a list of companies, like the Nifty 50, which is the 50 largest companies on the National Stock Exchange. Because nobody is picking and trading, costs are low. A SIP is simply how you pay in: a fixed amount every month, taken automatically.",
                   ["Mutual fund: a pooled basket run by a fund house", "Index fund: copies a list like the Nifty 50, low cost", "SIP: invest a fixed amount every month"]),
            _example("What happens when markets fall",
                     "Arjun invests ₹1,000 each month. In month 1 a unit costs ₹100, so he gets 10 units. In month 2 the market dips and a unit costs ₹80, so the same ₹1,000 buys 12.5 units. In month 3 it is back to ₹100 and he gets 10 more. Because he kept going through the dip, his average cost per unit ended lower than the usual price. Over the three months he put in ₹3,000 and holds 32.5 units, worth ₹3,250 at ₹100 a unit.",
                     "A steady SIP buys more units when prices are low, which smooths out the ups and downs."),
            _flash("What is a SIP?", "A systematic investment plan: investing a fixed amount on a regular schedule, usually every month."),
            _choice("Arjun started a ₹1,000 monthly SIP in a Nifty 50 index fund. After two months the market falls 10% and his ₹2,000 shows as ₹1,800. His friend says, 'Stop it now before you lose more.'",
                    "What should Arjun do?",
                    [("Stop the SIP and withdraw what is left", "bad",
                      "Stopping after a fall locks in the loss and means he misses buying units cheaply. Markets have always had dips, and long-term investors who stayed invested were rewarded for riding them out, though there is never a guarantee.",
                      _outcome(("Invested so far", 2000), ("After withdrawing at the dip", 1800), "A paper loss became a real ₹200 loss, and he stopped buying at lower prices.")),
                     ("Keep the SIP running as planned", "good",
                      "Right. A SIP is designed for exactly this. When prices dip, his ₹1,000 buys more units. Staying consistent and investing only money he will not need soon is the whole plan.",
                      _outcome(("Invested so far", 2000), ("Still invested, buying more units", 1800), "Same paper loss for now, but each new instalment buys more units at the lower price.")),
                     ("Pause for a few months and restart after the market recovers", "ok",
                      "Understandable, but timing the bottom is guesswork. Pausing often means missing the cheap months. If he is truly worried, a smaller SIP is better than stopping.")]),
            _teach("Why index funds suit beginners",
                   "Picking individual shares is hard, even for experts. An index fund spreads your money across many companies automatically, so one bad company cannot sink you. Fees are low, which matters because fees quietly reduce your returns every year. For a first investment, an index fund through a regulated platform is a sensible, boring choice, and boring is good.",
                   ["Spread across many companies", "Low fees", "No need to guess which stock wins", "Use a regulated platform"]),
            _choice("Kavya earns ₹30,000 a month and has a 3-month emergency fund. She wants to start investing ₹3,000 a month. Her college group is raving about a single stock from a reel.",
                    "Where should she start?",
                    [("Put the full ₹3,000 each month into the stock from the reel", "bad",
                      "One stock chosen from a reel is a bet on a single company, and she has no way to check whether the reel is honest. If it falls, all of her money falls."),
                     ("Start a ₹3,000 monthly SIP in a low-cost Nifty 50 index fund", "good",
                      "Right. It is diversified, cheap and automatic. She has already built her emergency fund, so she is in the right position to take some risk."),
                     ("Keep all of it in a savings account instead", "ok",
                      "Safe, and fine for short-term goals. But for money she will not need for five years or more, savings interest may not keep up with rising prices, so some investing makes sense.")]),
            _mcq("What is an index fund?", ["A fund that copies a list of companies like the Nifty 50", "A bank deposit", "A tip from an expert", "A loan to a company"], 0,
                 "An index fund holds the same companies as an index and aims to match its performance at low cost."),
            _mcq("The market falls in the month after you start a SIP. What does your next ₹1,000 instalment buy?", ["Fewer units than before", "The same number of units", "More units than before", "Nothing"], 2,
                 "When the price per unit is lower, the same ₹1,000 buys more units. That is one reason regular investing smooths out volatility."),
        ], xp=25)

    c3 = _concept(m_id, 3,
        "Don't put all your eggs in one basket",
        "Explain diversification and spot tips and schemes that sound too good to be true.",
        "Diversification means spreading your money across different investments so one failure does not wipe you out. "
        "It is also the best defence against 'guaranteed returns' schemes, which are almost always scams.",
        "Meera has ₹10,000. If she puts it all into one stock and it halves, she is left with ₹5,000. Spread across five stocks, the same halving costs her only ₹1,000.",
        ["Spread money across several investments.",
         "One investment failing should not ruin you.",
         "'Guaranteed' high returns are a red flag.",
         "Check that advisors and platforms are registered with SEBI."],
        ["Putting everything in one stock or one trend.",
         "Trusting 'sure-shot tips' on Telegram or Instagram.",
         "Investing because everyone else seems to be."],
        [
            _intro("The Telegram group", "A channel with 40,000 members posts 'sure-shot tips' every morning. They show screenshots of huge profits. Before you join, learn the one rule that protects every investor: do not put all your eggs in one basket."),
            _teach("What is diversification?",
                   "Diversification just means owning different things so that no single failure hurts too much. That could be many companies through an index fund, different kinds of investments such as shares and safer options, and different time horizons. It does not remove risk, but it turns one big gamble into many small ones. Two other beginner defences: never invest in anything you do not understand, and be very careful with any promise of 'guaranteed' returns.",
                   ["Spread across companies and types of investments", "It reduces damage, it does not remove risk", "Guaranteed high returns do not exist in real investing"]),
            _example("Five baskets vs one",
                     "Meera and Rohit each invest ₹10,000. Meera buys one stock. Rohit splits his money across five different companies, ₹2,000 each. A year later, Meera's stock falls by half after a scandal. Rohit's weakest company also falls by half, but the other four hold steady. Meera is left with ₹5,000, while Rohit still has ₹9,000.",
                     "Spreading your money limits how much any one failure can cost you."),
            _flash("Name two red flags of an investment scam.", "Guaranteed or very high returns, and pressure to act fast or to recruit friends."),
            _choice("Meera has ₹10,000 to invest and is deciding between putting it all in one company she likes, or spreading it. Suppose the one company she likes falls 50% over the year.",
                    "What is the smarter plan?",
                    [("All ₹10,000 in the one company she likes most", "bad",
                      "Liking a company is not the same as it being safe. If that single company stumbles, she bears the whole loss.",
                      _outcome(("Starting money", 10000), ("If her one stock halves", 5000), "One bad outcome cost her half of everything.")),
                     ("Spread it across several different companies, for example through an index fund", "good",
                      "Right. If one falls, the others help cushion it. This is why index funds are popular with beginners: diversification is built in.",
                      _outcome(("Starting money", 10000), ("If one of five halves", 9000), "The same bad event cost only ₹1,000 because the money was spread out.")),
                     ("Hold it all as cash and never invest", "ok",
                      "No chance of losing to a stock fall, but rising prices slowly eat the value of cash. A mix of safe money and diversified investing usually works better for long-term goals.")]),
            _teach("Spotting too-good-to-be-true",
                   "Real investments go up and down. Anyone who promises a fixed high return, such as 10% a week, is either lying or running a scheme that pays early investors with new investors' money, and it collapses when the new money stops. Warning signs: guaranteed returns, urgency ('only today'), pressure to bring friends, screenshots instead of audited records, and advisors who are not registered. In India, you can check whether an advisor or platform is registered on the SEBI website.",
                   ["Guaranteed high returns = red flag", "Urgency and pressure = red flag", "Check SEBI registration before sending any money"]),
            _choice("A Telegram group messages Ishaan: 'Join our VIP plan. We guarantee 10% a week. Minimum ₹10,000, only 5 spots left today!' Several screenshots show big profits.",
                    "What should Ishaan do?",
                    [("Join with ₹10,000 before the spots run out", "bad",
                      "A guaranteed 10% a week would turn ₹10,000 into more than ₹14 lakh in a year. No real investment does this, and urgency is a classic pressure tactic. Screenshots are easy to fake."),
                     ("Try with ₹2,000 first to see if it is real", "bad",
                      "Small 'tests' are how these schemes build trust before asking for more, and the first payouts are often real, paid from other people's deposits. A fake scheme with a small amount is still a scam."),
                     ("Ignore it, check that the group's advisor is not on the SEBI registered list, and report the channel", "good",
                      "Right. Guaranteed returns, urgency and screenshots are the three classic signs. Checking the SEBI register and reporting the channel protects you and others.")]),
            _mcq("Which of these is a red flag for an investment scam?", ["A guaranteed 10% return every week", "A fund that tracks the Nifty 50", "A registered advisor on the SEBI list", "A fund with a low fee"], 0,
                 "No real investment can guarantee high returns. Promises of fixed, high returns are the clearest sign of a scam."),
            _mcq("Rohit splits ₹10,000 equally across five stocks. One falls 50%. About how much does he lose overall?", ["₹1,000", "₹2,000", "₹5,000", "₹10,000"], 0,
                 "Each stock holds ₹2,000. A 50% fall on one of them loses ₹1,000, which is 10% of his total."),
        ], xp=25)

    m["concepts"] = [c1, c2, c3]
    ch["modules"] = [m]
    return ch


# ---------------------------------------------------------------------------
# BITCOIN AND CRYPTO
# ---------------------------------------------------------------------------

def _crypto_chapter(course_id):
    ch_id = _id()
    ch = {
        "id": ch_id, "course_id": course_id, "order": 1,
        "title": "Crypto without the hype",
        "description": "Understand what Bitcoin is, how to handle hype and FOMO, and how to keep your coins safe from scams.",
    }
    m_id = _id()
    m = {"id": m_id, "chapter_id": ch_id, "order": 1, "title": "Bitcoin basics"}

    c1 = _concept(m_id, 1,
        "What is Bitcoin?",
        "Describe Bitcoin simply and explain why its price swings so much.",
        "Bitcoin is digital money that runs on a network of computers, not a bank. Only 21 million can ever exist. "
        "Its price is set by buyers and sellers, so it can jump or crash quickly.",
        "Ananya sees a headline that Bitcoin rose 18% in one day. That sounds exciting, but a coin that can rise 18% in a day can also fall that much, so it is not a savings account.",
        ["Bitcoin is digital money with no company or bank behind it.",
         "Only 21 million will ever exist.",
         "Prices are set by buyers and sellers and swing a lot.",
         "It is high risk, so never use emergency money."],
        ["Treating Bitcoin like a savings account.",
         "Thinking a big rise means it will keep rising.",
         "Investing money you cannot afford to lose."],
        [
            _intro("Money that no bank runs", "Bitcoin started in 2009 as an experiment: money that anyone can send to anyone, with no bank in the middle. Today it is also one of the most volatile things you can buy."),
            _teach("How Bitcoin works, in plain words",
                   "Bitcoin is a digital currency kept on a shared record called a blockchain. Thousands of computers around the world agree on who owns what, so no single bank or company controls it. The software limits the total number of coins to 21 million, which some people see as a reason it could hold value. But nobody guarantees its price. It depends on how many people want to buy it versus sell it, and that mood can change overnight.",
                   ["Digital money on a shared record (blockchain)", "No bank or company in charge", "Supply capped at 21 million coins", "Price depends on demand, with no guarantee"]),
            _example("A wild week",
                     "In one week, Bitcoin's price rose 18% on Monday after positive news, then fell 12% on Thursday after a rumour about a new rule, then rose again on Sunday. Someone who put ₹10,000 in on Monday morning would have seen ₹11,800, then ₹10,400 and then more. Those numbers are made up for illustration, but real weeks like that happen. A savings account never behaves this way.",
                     "Big swings in both directions are normal for Bitcoin. That is volatility, and it is risk."),
            _flash("Why is Bitcoin called 'volatile'?", "Its price can rise or fall a lot in short periods, because it is set only by buyers and sellers."),
            _choice("Ananya has ₹30,000 saved as her emergency fund. She sees 'Bitcoin up 18% today!' on her feed and several friends say they are buying.",
                    "What should Ananya do with her emergency fund?",
                    [("Move the full ₹30,000 into Bitcoin to catch the rise", "bad",
                      "The emergency fund exists to be safe and available. If Bitcoin falls 30% in a week, her cushion shrinks to ₹21,000 just when she may need it.",
                      _outcome(("Emergency fund", 30000), ("If Bitcoin then falls 30%", 21000), "A third of her safety net gone in a week.")),
                     ("Keep the emergency fund in a savings account. If she still wants to try Bitcoin, use only a small amount of spare money", "good",
                      "Right. Safety first, curiosity second. Spare money you can afford to lose is the only money that belongs in something this volatile.",
                      _outcome(("Emergency fund", 30000), ("After a 30% Bitcoin fall", 30000), "Her safety net is untouched. Only the small spare amount moves.")),
                     ("Buy because her friends are buying", "bad",
                      "Everyone buying is not a reason. Prices often peak when excitement is highest, and she would be risking money without a plan.")]),
            _teach("Bitcoin is not a savings account",
                   "People hear 'digital gold' and imagine a safe store of value. In practice, Bitcoin has had falls of 50% or more several times. It has also risen a lot, which is why it gets attention, but nobody can promise which way it goes next. A useful rule for beginners: only put in money you could lose completely without it hurting your life, and keep it a small part of what you own.",
                   ["It can fall 50% or more", "It can also rise a lot, but there is no promise", "Only spare money, only a small part of your savings"]),
            _choice("Sam is 21 and has ₹5,000 of spare money after building an emergency fund. He is curious about Bitcoin but nervous.",
                    "How should Sam approach it?",
                    [("Buy a small amount (say ₹1,000), learn how it works, and accept he might lose it all", "good",
                      "Right. A small amount lets him learn how prices move and how wallets work, without risking money he needs. The limit he sets in advance is what protects him."),
                     ("Put in the full ₹5,000 to make the gains worthwhile", "bad",
                      "Larger amounts do not make it safer, they just raise the stakes. If it drops, a bigger share of his spare money is gone."),
                     ("Avoid it entirely and never learn about it", "ok",
                      "A fine choice if it does not interest him. But understanding it helps him spot hype and scams, even if he never buys.")]),
            _mcq("What is the maximum number of Bitcoin that can ever exist?", ["21 million", "21 billion", "Unlimited", "1 million"], 0,
                 "Bitcoin's software caps the supply at 21 million coins."),
            _mcq("Which statement about Bitcoin is TRUE?", ["Its price is guaranteed by a bank", "Its price can swing sharply up or down", "It cannot lose value", "It is safer than a savings account"], 1,
                 "Bitcoin's price is set by buyers and sellers and can swing sharply. No bank or government guarantees it."),
        ], xp=25)

    c2 = _concept(m_id, 2,
        "The group chat tip",
        "Recognise FOMO and use position sizing to protect yourself from hype.",
        "FOMO (fear of missing out) makes people buy at the top and panic at the bottom. "
        "A calm plan with a small, fixed amount beats chasing hype every time.",
        "Rohan, 20, gets ₹12,000 stipend. His group chat urges him to put it all into a coin that will '10x by Friday'. He keeps rent safe and puts in only ₹1,000.",
        ["Hype is not research. Ask who gains if you buy.",
         "Cover needs first. Risk only money you can lose.",
         "A good decision can still lose. Judge the plan, not the luck.",
         "Decide the amount before you look at the price."],
        ["Going all-in because everyone else is.",
         "Adding more money to a falling price to 'win it back'.",
         "Judging a decision only by whether it made money."],
        [
            _intro("Last chance, bro!", "It is 11:42 pm. Your phone buzzes again: 'This coin will 10x by Friday. Everyone is buying.' Your heart speeds up. That feeling has a name, and learning to spot it is the most useful money skill you can have."),
            _teach("What is FOMO?",
                   "FOMO means fear of missing out. When prices are rising and everyone around you is excited, your brain says you will regret not joining. But the people shouting about a coin often benefit from more buyers, either because they hold it already or because they are paid to promote it. A good habit: before you act on a tip, ask who gains if you buy, then decide how much you can afford to lose before you look at the price.",
                   ["Ask: who gains if I buy?", "Decide the amount first, then act", "Keep rent, food and emergency money out of it"]),
            _example("Good decision, bad luck",
                     "Two friends each hear the same tip. Zoya puts in ₹500 from her spare money. Mihir puts in his entire month's salary. The coin happens to double. Mihir feels like a genius, Zoya feels she should have put in more. Two months later the coin falls 80%. Zoya loses ₹400 and shrugs. Mihir loses most of his salary and cannot pay rent. Looking back, Zoya's decision was better even when the coin was doubling, because her plan protected her either way.",
                     "A decision can be good and still lose, or be reckless and still win. Judge the plan, not the outcome."),
            _flash("What question should you ask before acting on a hot tip?", "Who gains if I buy, and how much can I afford to lose?"),
            _choice("Rohan is 20. His first stipend of ₹12,000 just landed. Rent of ₹5,000 is due next week. At 11:42 pm his college group chat blows up: 'Bro this new coin will 10x by Friday. Everyone is buying. Last chance!'",
                    "What should Rohan do?",
                    [("Put all ₹12,000 in right now before it is too late", "bad",
                      "That is FOMO. The people shouting '10x by Friday' cannot know that. If they are promoting the coin, your money is how they make theirs. All-in on one unknown coin is the fastest way to lose a month of stipend.",
                      _outcome(("Wallet before", 12000), ("If the coin crashes 70% by Friday", 3600), "₹12,000 becomes ₹3,600, and rent is due.")),
                     ("Keep rent and food money safe. Put in only ₹1,000 that he can afford to lose, after checking who is promoting it", "good",
                      "Smart move. You split money into buckets: needs first, risky money small and last. You also asked who gains from the hype. Even if the coin had gone up, this is still the better decision. A good decision and a lucky result are not the same thing.",
                      _outcome(("Wallet before", 12000), ("After the same 70% crash", 11300), "Only ₹700 lost. Rent is safe and he can still pay it.")),
                     ("Ignore it completely and leave everything in the wallet", "ok",
                      "Safe, but not the best. You lost nothing, and that is fine. But idle money loses value to rising prices, and you skipped a chance to learn how risk works with a tiny amount. The goal is not to avoid risk. It is to size it.",
                      _outcome(("Wallet before", 12000), ("After the crash", 12000), "Nothing lost, nothing learned."))]),
            _teach("The plot twist: what to do when it falls",
                   "The hardest moment is not buying, it is the day the price drops. Two opposite mistakes are common: panic-selling at the bottom, and borrowing or using essential money to buy more and 'win it back'. A calm response is to go back to your plan. Is the reason you bought still true? Is the amount still one you can afford to lose? If so, do nothing, and do not add money you need.",
                   ["Do not panic-sell just because the number is red", "Never add essential money to a falling price", "Return to your written plan and your limit"]),
            _choice("Monday morning. The coin is down 30%. Rohan's ₹1,000 is now worth ₹700. The group chat is panicking. Rent is still due Friday.",
                    "What now?",
                    [("Panic and sell everything now", "bad",
                      "Selling only because the price dropped turns a paper loss into a real loss. Prices go up and down. Ask whether your original reason still holds, not how scary the red number looks."),
                     ("Use the rent money to buy more and 'average down'", "bad",
                      "Never put money you need for essentials into a falling price. If it keeps dropping, you lose the rent money too. Averaging down only works with money you can truly afford to lose."),
                     ("Check why he bought, stick to his ₹1,000 limit, and do not add more", "good",
                      "Exactly right. You decide with a plan, not with emotion. A ₹1,000 loss stings, but it does not break your month. That is what limiting your position size buys you: calm and control.")]),
            _mcq("A friend says a coin will '10x by Friday'. What is the best first question to ask?", ["Who gains if I buy?", "How fast can I buy?", "How many friends are buying?", "Can I borrow to buy more?"], 0,
                 "Hype often benefits the people promoting it. Asking who gains helps you separate information from persuasion."),
            _mcq("Which amount belongs in a high-risk coin?", ["Rent money", "Your emergency fund", "Spare money you could lose without harm", "A loan"], 2,
                 "Only money you can afford to lose completely belongs in something this volatile. Essentials, emergency funds and borrowed money do not."),
        ], xp=25)

    c3 = _concept(m_id, 3,
        "Scams and staying safe",
        "Protect your crypto from phishing, fake giveaways and 'support' scams.",
        "In crypto there is no bank to reverse a payment. Your seed phrase is the password to your coins, and anyone who gets it can take everything. "
        "Most losses come from scams, not from market falls.",
        "A stranger messages Priya claiming to be 'wallet support' and asks for her seed phrase to 'fix a problem'. She never shares it and blocks them.",
        ["Never share your seed phrase or private key with anyone.",
         "Nobody legitimate will ask for it.",
         "No one doubles your crypto. Giveaways asking you to send first are scams.",
         "Transfers cannot be reversed, so double-check everything."],
        ["Clicking links in DMs or emails.",
         "Storing a seed phrase in a screenshot or cloud note.",
         "Trusting a verified-looking account without checking."],
        [
            _intro("Where the real losses happen", "More people lose crypto to scams than to market crashes. The good news is that most scams use the same few tricks, so learning them keeps you safe."),
            _teach("Your seed phrase is everything",
                   "A crypto wallet is protected by a seed phrase, usually 12 or 24 words, that works like a master password. Whoever has it controls the coins, and a transfer cannot be undone. So: never share it, never type it into a website, never store it in a screenshot, email or cloud note. Write it on paper and keep it somewhere safe. Real support teams will never ask for it.",
                   ["Never share your seed phrase", "Never type it on a website or in a chat", "Store it offline, on paper, in a safe place"]),
            _example("The helpful stranger",
                     "Priya posts in a crypto forum asking why a transfer is slow. Within minutes, an account with the wallet company's logo messages her: 'We see a problem with your wallet. Verify your seed phrase here to restore access.' The link looks real and the message sounds urgent. Priya checks the wallet company's official site, which says clearly: 'We will never ask for your seed phrase.' She blocks the account.",
                     "Urgency plus a request for secrets is the signature of a scam."),
            _flash("Who should you share your seed phrase with?", "Nobody. Not support, not friends, not any website."),
            _choice("A message arrives on Instagram from 'Wallet Support Team': 'Your wallet may be compromised. To secure it, verify your 12-word seed phrase at this link within 30 minutes or your funds will be frozen.'",
                    "What should you do?",
                    [("Enter the seed phrase quickly so your funds are not frozen", "bad",
                      "The 30-minute deadline is designed to make you panic. The moment you enter your seed phrase, the scammer controls your wallet and can empty it, and transfers cannot be undone."),
                     ("Click the link just to look, without entering anything", "bad",
                      "Fake sites can steal information or install harmful software with a single click, and looking can lead to entering. The safest move is not to engage with it."),
                     ("Ignore and block it. Never share the seed phrase, and only contact support through the wallet's official app or website", "good",
                      "Right. Real support never asks for your seed phrase. Using only official channels you opened yourself keeps you safe from fake accounts.")]),
            _teach("Too-good-to-be-true giveaways",
                   "A popular scam is the fake giveaway: 'Send 0.1 Bitcoin to this address and we will send 0.2 back', often attached to a famous person's name or a hacked verified account. No one doubles your crypto. The same applies to 'guaranteed' trading bots, 'staking' platforms with fixed huge returns and romance-plus-investment chats. Check twice, send once, because crypto payments cannot be reversed.",
                   ["No one doubles your crypto", "Send-first giveaways are scams", "Fixed huge returns are a red flag", "Crypto transfers cannot be reversed"]),
            _choice("A video shows a famous founder saying: 'To celebrate, send 0.1 BTC to this address in the next hour and we will send back 0.2 BTC. Limited giveaway!'",
                    "What is the right call?",
                    [("Send a small amount, like 0.01 BTC, to test it", "bad",
                      "There is no giveaway. Even a small send is money gone forever, and it marks you as someone who responds, so more scams follow."),
                     ("Send the full 0.1 BTC to get the doubled amount", "bad",
                      "Nobody gives away double what you send. The video was edited or the account hacked, and the address belongs to a scammer."),
                     ("Ignore it, report the video, and remember that real giveaways never ask you to send first", "good",
                      "Right. No legitimate giveaway needs you to pay first. Reporting it helps protect others.")]),
            _mcq("Who should you give your wallet's seed phrase to?", ["Wallet support, if they ask", "Nobody", "A friend you trust", "Any website that asks"], 1,
                 "Your seed phrase is the master key to your coins. Nobody legitimate will ever ask for it, so you share it with no one."),
            _mcq("A crypto transfer is sent to the wrong address. What can usually be done?", ["The bank can reverse it", "Nothing, crypto transfers cannot be reversed", "The wallet can cancel it within 24 hours", "The government will refund it"], 1,
                 "Crypto transfers are final. That is why you must double-check addresses and avoid sending to strangers."),
        ], xp=25)

    m["concepts"] = [c1, c2, c3]
    ch["modules"] = [m]
    return ch


# ---------------------------------------------------------------------------
# BUILD + SEED
# ---------------------------------------------------------------------------

def build_finance_courses():
    courses = []

    cid = _id()
    courses.append({
        "id": cid, "slug": "money-basics", "seed_version": FINANCE_SEED_VERSION,
        "name": "Money Basics", "title": "Money Basics: Your First Salary and Beyond",
        "certification": "Beginner",
        "description": "Budgeting, emergency funds and credit cards, learned through everyday situations.",
        "color": "#10B981", "icon": "Wallet", "order": -3,
        "chapters": [_money_chapter(cid)],
    })

    sid = _id()
    courses.append({
        "id": sid, "slug": "stock-market-basics", "seed_version": FINANCE_SEED_VERSION,
        "name": "Stock Market", "title": "Stock Market: Shares, SIPs and Smart Habits",
        "certification": "Markets",
        "description": "What shares are, how a monthly SIP works, and how to avoid tips and scams.",
        "color": "#2563EB", "icon": "TrendingUp", "order": -2,
        "chapters": [_stock_chapter(sid)],
    })

    kid = _id()
    courses.append({
        "id": kid, "slug": "bitcoin-and-crypto", "seed_version": FINANCE_SEED_VERSION,
        "name": "Bitcoin and Crypto", "title": "Bitcoin and Crypto: Without the Hype",
        "certification": "Crypto",
        "description": "Understand Bitcoin, handle FOMO, and keep your coins safe from scams.",
        "color": "#F59E0B", "icon": "Bitcoin", "order": -1,
        "chapters": [_crypto_chapter(kid)],
    })
    return courses


async def _delete_course_tree(db, course_id):
    chapters = await db.chapters.find({"course_id": course_id}, {"id": 1}).to_list(500)
    chapter_ids = [c["id"] for c in chapters]
    modules = await db.modules.find({"chapter_id": {"$in": chapter_ids}}, {"id": 1}).to_list(2000)
    module_ids = [m["id"] for m in modules]
    concepts = await db.concepts.find({"module_id": {"$in": module_ids}}, {"id": 1}).to_list(5000)
    concept_ids = [c["id"] for c in concepts]
    await db.lessons.delete_many({"concept_id": {"$in": concept_ids}})
    await db.concepts.delete_many({"id": {"$in": concept_ids}})
    await db.modules.delete_many({"id": {"$in": module_ids}})
    await db.chapters.delete_many({"id": {"$in": chapter_ids}})
    await db.courses.delete_one({"id": course_id})


async def seed_finance_courses(db):
    """Add or refresh the beginner tracks without touching LOMA content."""
    from seed_data import flatten_for_db
    from seed_cfa import build_cfa_course  # imported here to avoid a circular import
    from seed_life import build_life_courses
    from seed_hindi import build_hindi_course

    # Beginner tracks use negative orders so they always list first; LOMA and other courses keep their own order.

    # The pre-rebrand "loma-357" copy duplicates "institutional-investing-101". Hide (never delete) the stale one
    # so learners see a single course; the flag is reversible and no progress data is touched.
    if await db.courses.find_one({"slug": "institutional-investing-101"}):
        await db.courses.update_many({"slug": "loma-357"}, {"$set": {"hidden": True}})

    to_build = []
    # Remove an earlier working title of the quant course (it never shipped, so no learner data is affected).
    for old_slug in ("cfa-l1-quant-methods",):
        old = await db.courses.find_one({"slug": old_slug})
        if old:
            await _delete_course_tree(db, old["id"])

    # Each course carries its own seed_version, so updating one course never re-seeds (and re-ids) the others.
    for course in build_finance_courses() + [build_cfa_course()] + build_life_courses() + [build_hindi_course()]:
        existing = await db.courses.find_one({"slug": course["slug"]})
        if existing and existing.get("seed_version") == course["seed_version"]:
            continue
        if existing:
            await _delete_course_tree(db, existing["id"])
        to_build.append(course)

    if not to_build:
        return

    cs, chs, ms, cps, ls = flatten_for_db(to_build)
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
    print(f"[seed] Finance tracks seeded: {len(cs)} courses, {len(cps)} concepts, {len(ls)} lessons")
