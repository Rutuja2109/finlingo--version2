"""Taxes Made Simple, chapter 2: "Smarter with tax". Rupees. Tax rules change with every Budget and the Income Tax Act is being
renumbered, so lessons describe ideas, give dated examples, and send learners to the official portal. Not tax advice.
Figures are checked in tests/check_more_chapters.py."""
from seed_data import _id, _intro, _teach, _example, _flash, _mcq, _concept
from seed_finance import _choice, _outcome
from seed_money_more import _chat, _swipe, _match

CHAPTER_KEY = "smarter-with-tax"
NOTE = "Rules change every Budget, so check incometax.gov.in or a professional for your own case."


def build_tax_chapter_two(course_id):
    ch_id = _id()
    ch = {"id": ch_id, "course_id": course_id, "order": 2, "key": CHAPTER_KEY,
          "title": "Smarter with tax",
          "description": "Legal ways to cut tax, deadlines and late fees, and what changes when you earn on the side."}
    m_id = _id()
    m = {"id": m_id, "chapter_id": ch_id, "order": 1, "title": "Keep more of what you earn"}

    # ---------------------------------------------------------------- 1. saving tax
    c1 = _concept(m_id, 1,
        "Saving tax the legal way",
        "Understand deductions like 80C and 80D, and when they actually help.",
        "A deduction lowers the income your tax is calculated on. Under the old tax regime, you can claim deductions such as 80C (up to ₹1.5 lakh) "
        "for savings like PPF or ELSS, and 80D for health insurance. Under the new regime most of these are not available, so the right choice depends on your numbers.",
        "Kabir, in the 20% slab of the old regime, puts ₹1,50,000 into 80C options. His taxable income falls by ₹1,50,000, so he saves about ₹30,000 in tax "
        "(a little more with cess), without spending money he would not have saved anyway.",
        ["A deduction lowers the income your tax is worked out on.",
         "80C allows up to ₹1.5 lakh for options like EPF, PPF, ELSS and term insurance premiums, under the old regime.",
         "80D gives a deduction for health insurance premiums, under the old regime.",
         "Do not buy a product only to save tax. Buy it because it fits your goals."],
        ["Buying a poor product only to save tax.",
         "Forgetting that most deductions do not apply in the new regime.",
         "Locking money into long lock-ins you may need."],
        [
            _intro("Pay less, legally", "Tax saving is not tricks. It is using rules the government has set to encourage saving, insurance and home ownership. " + NOTE),
            _chat("Kabir and the deductions", "Kabir asks Lumi about saving tax", [
                ("friend", "Kabir", "My dad says I should put ₹1.5 lakh in '80C' to save tax. What is that?"),
                ("lumi", "Lumi", "80C is a rule that lets you deduct up to ₹1.5 lakh of certain savings from your taxable income, but only in the old regime."),
                ("friend", "Kabir", "What counts?"),
                ("lumi", "Lumi", "EPF, PPF, ELSS mutual funds, a 5-year tax-saver deposit, term insurance premiums and a few more."),
                ("friend", "Kabir", "And does the saving equal ₹1.5 lakh?"),
                ("lumi", "Lumi", "No. The deduction lowers your taxable income. If you are in the 20% slab, you save about 20% of ₹1.5 lakh, around ₹30,000."),
                ("friend", "Kabir", "So I should buy whatever qualifies?"),
                ("lumi", "Lumi", "Not just anything. Pick what fits your goals, and check which regime gives you the lower tax."),
            ], "A deduction cuts the income you are taxed on. It does not give you the whole amount back."),
            _match("Match the 80C option to a key feature", [
                ("PPF", "Government-backed savings with a 15-year lock-in"),
                ("ELSS fund", "Equity mutual fund with a 3-year lock-in"),
                ("Tax-saver FD", "Bank deposit with a 5-year lock-in"),
                ("Term insurance premium", "Pure life cover; the premium can qualify"),
            ]),
            _teach("How a deduction works",
                   "Tax is worked out on your taxable income. A deduction lowers that income before tax is charged. If your slab rate is 20%, every ₹1,00,000 deducted saves about ₹20,000 in tax, plus a little cess. So the benefit depends on your slab. Under the new regime, which is the default, most deductions like 80C and 80D are not available, but the tax rates are lower. Compare both before you choose.",
                   ["Deduction x slab rate = tax saved", "80C: up to ₹1.5 lakh (old regime)", "80D: health insurance premium (old regime)", "New regime: lower rates, fewer deductions"]),
            _example("The ₹30,000 saving",
                     "Kabir invests ₹1,50,000 in eligible 80C options. In the 20% slab, his tax falls by 20% of ₹1,50,000, which is ₹30,000, and with 4% cess about ₹31,200. He still owns the investments. The tax saving is a bonus, not the reason to choose them.",
                     "Choose the investment for its job in your plan. The tax saving is a side benefit."),
            _swipe("Saving tax: myth or fact?", [
                ("A deduction lowers the income on which tax is worked out.", "fact", "That is how deductions work. The tax saved depends on your slab rate."),
                ("If I invest ₹1.5 lakh in 80C, I get ₹1.5 lakh back from the taxman.", "myth", "You save only the tax on that amount, such as about ₹30,000 at a 20% slab."),
                ("80C and 80D deductions are available in the new regime as well.", "myth", "Most such deductions are available only in the old regime. Check your regime."),
                ("A lock-in means you cannot withdraw the money for some years.", "fact", "PPF, ELSS and tax-saver FDs all lock your money for a fixed time."),
            ]),
            _choice("Kabir is in the 20% slab of the old regime. A friend urges him to buy a ₹1,50,000 insurance-cum-investment plan 'to save tax'. He has no need for the cover and the plan locks money for 15 years.",
                    "What is the smartest approach?",
                    [("Choose the 80C options that fit his goals and flexibility, such as EPF, PPF or an ELSS, and skip products he does not need", "good",
                      "Right. A deduction is a reason to prefer a good product, not to buy a poor one. Check lock-ins, costs and whether it matches his goals. This is education, not advice.",
                      _outcome(("Tax saved on ₹1.5 lakh at 20%", 30000), ("Money locked in the plan", 150000), "The saving is real, but he must still be happy with where the ₹1.5 lakh sits.")),
                     ("Buy it, because the tax saving makes it worth it", "bad", "A poor product with a long lock-in can cost far more than the tax it saves."),
                     ("Skip all tax planning because it is too complicated", "ok", "Skipping is safe but can cost money. Many options like EPF may already be counting toward 80C.")]),
            _choice("Aisha earns ₹9 lakh. She claims almost no deductions and wonders whether to stay in the default new regime or switch.",
                    "What is the best way to decide?",
                    [("Work out her tax under both regimes with her real deductions, and pick the lower", "good",
                      "Right. The new regime has lower rates but fewer deductions. Whoever has many deductions may do better in the old one, and others in the new one. Use the tax calculator on the official portal."),
                     ("Always pick the old regime because it has more deductions", "bad", "More deductions only help if you actually have them."),
                     ("Always pick the new regime because it is the default", "ok", "It suits many people, but it is not always lowest for everyone. Compare.")]),
            _mcq("Roughly how much tax does a ₹1,00,000 deduction save in the 20% slab?", ["₹1,00,000", "₹20,000", "₹2,000", "Nothing"], 1,
                 "20% of ₹1,00,000 is ₹20,000, plus a little cess. A deduction saves tax only on that amount."),
            _mcq("Which is a typical feature of an ELSS fund?", ["No lock-in", "3-year lock-in", "Guaranteed returns", "Bank guarantee"], 1,
                 "ELSS funds invest in shares and have a 3-year lock-in."),
            _flash("Deductions, in one line", "They lower the income you are taxed on. Choose products for their purpose, not just the saving."),
        ], xp=30)

    # ---------------------------------------------------------------- 2. deadlines
    c2 = _concept(m_id, 2,
        "Deadlines, late fees and refunds",
        "Know the key dates, what late filing costs, and how refunds work.",
        "Most individuals who do not need an audit must file their return by 31 July each year. Filing late costs a fee, "
        "and a refund only arrives after you file and verify. " + NOTE,
        "Rohan forgets to file and does it in December. He pays a late fee of ₹5,000 (or ₹1,000 if his income is up to ₹5 lakh) and may owe interest on any unpaid tax.",
        ["The usual deadline for most salaried individuals is 31 July.",
         "Late filing carries a fee: ₹5,000, or ₹1,000 if total income is up to ₹5 lakh.",
         "A late (belated) return can usually be filed until 31 December.",
         "You must e-verify the return, usually within 30 days, or it is treated as not filed."],
        ["Missing the deadline because 'no tax is due'.",
         "Filing but forgetting to e-verify.",
         "Ignoring a mismatch between Form 16 and AIS."],
        [
            _intro("Don't miss the date", "A return filed on time costs nothing extra. A return filed late costs money, even if you owe no tax. " + NOTE),
            _chat("Rohan forgot", "Rohan asks Lumi in December", [
                ("friend", "Rohan", "I forgot to file my return. The due date was 31 July. Am I in trouble?"),
                ("lumi", "Lumi", "You can still file a belated return, usually until 31 December, but there is a late fee."),
                ("friend", "Rohan", "How much?"),
                ("lumi", "Lumi", "₹5,000, or ₹1,000 if your total income is up to ₹5 lakh. Plus interest if tax was unpaid."),
                ("friend", "Rohan", "Even though my employer already deducted tax?"),
                ("lumi", "Lumi", "Yes, the late fee can apply even if no extra tax is due. And you must e-verify after filing."),
                ("friend", "Rohan", "Okay. I will file today and set a reminder for next July."),
            ], "File by the due date, and e-verify. Late filing costs money even when no tax is due."),
            _match("Match the date or fee", [
                ("Usual due date for most individuals", "31 July"),
                ("Belated return usually allowed until", "31 December"),
                ("Late fee if income is up to ₹5 lakh", "₹1,000"),
                ("Late fee if income is above ₹5 lakh", "₹5,000"),
            ]),
            _teach("The dates and fees to know",
                   "For most individuals without an audit, the filing due date is 31 July after the financial year ends. Miss it and you can still file a belated return until 31 December, but you pay a late fee: ₹5,000, or ₹1,000 if your total income is up to ₹5 lakh. If you owe tax, interest of 1% a month can also apply. After filing, you must verify the return, usually within 30 days, through Aadhaar OTP, net banking or another method.",
                   ["Due date: usually 31 July", "Belated return: usually until 31 December", "Late fee: ₹5,000, or ₹1,000 for income up to ₹5 lakh", "E-verify within 30 days or the return is invalid"]),
            _example("A refund that waited",
                     "Neha's employer deducted too much tax, so she is owed a refund of ₹8,000. She files in July but never e-verifies. Months later she wonders why no refund has come. An unverified return is treated as not filed, so no refund is processed. She had to file again and verify.",
                     "Filing is only half the job. Verification completes it, and the refund follows after."),
            _swipe("Deadlines: myth or fact?", [
                ("If no tax is due, I can file whenever I like.", "myth", "A late fee can apply even if no tax is due, and some benefits like carrying forward losses need on-time filing."),
                ("A return must be e-verified after filing.", "fact", "Without verification it is treated as not filed and refunds will not come."),
                ("A belated return can usually be filed until 31 December.", "fact", "That is the usual outer limit, with the late fee applied."),
                ("The late fee is the same for everyone.", "myth", "It is ₹5,000 generally, but ₹1,000 if total income is up to ₹5 lakh."),
            ]),
            _choice("Rohan earns ₹4,50,000 a year and files on 20 December instead of 31 July.",
                    "What late fee applies, as the rules are understood now?",
                    [("₹1,000, because his total income is up to ₹5 lakh", "good",
                      "Right. The late fee is ₹1,000 for total income up to ₹5 lakh and ₹5,000 above that. Always check current rules.",
                      _outcome(("Late fee for income up to ₹5 lakh", 1000), ("Late fee above ₹5 lakh", 5000), "Rohan pays the lower fee because his income is under ₹5 lakh.")),
                     ("₹5,000 for everyone", "bad", "The lower fee applies to total income up to ₹5 lakh."),
                     ("Nothing, because there is no tax due", "bad", "The fee can apply regardless of tax due.")]),
            _choice("Neha filed her return on time and is waiting for a refund. It has been 3 months and nothing has come.",
                    "What is the first thing to check?",
                    [("Whether she e-verified the return, and the refund status on the portal", "good",
                      "Right. An unverified return is not processed. Check the status on the portal and the bank account details linked for refunds.",
                      _outcome(("Refund owed", 8000), ("Refund paid if not verified", 0), "No verification, no refund.")),
                     ("File a new return immediately without checking anything", "bad", "Check the status first. Filing a duplicate can complicate things."),
                     ("Ignore it, because refunds never come", "bad", "Refunds do come once the return is verified and processed.")]),
            _mcq("What is the usual last date to file for most individuals without an audit?", ["31 March", "31 July", "31 October", "31 December"], 1,
                 "The normal due date is 31 July. A belated return can usually be filed later with a fee."),
            _mcq("What happens if you do not e-verify your return?", ["It is treated as filed and the refund comes", "It is treated as not filed", "The tax is waived", "Nothing"], 1,
                 "An unverified return is treated as not filed, so a refund will not be processed."),
            _flash("Deadlines, in one line", "File by 31 July, e-verify within 30 days, and put a reminder in your phone."),
        ], xp=30)

    # ---------------------------------------------------------------- 3. side income
    c3 = _concept(m_id, 3,
        "Side income and advance tax",
        "Understand how freelance or side income is taxed and when to pay in advance.",
        "If you earn from freelancing or a side business, no employer deducts tax for you. Tax on a large enough bill must be paid in advance, "
        "in instalments through the year, and some freelancers can use a simplified 'presumptive' method. " + NOTE,
        "Ananya earns ₹6,00,000 a year from freelance design. If she qualifies for the presumptive scheme for professionals, only 50% of her receipts, ₹3,00,000, "
        "is treated as profit, and she must pay advance tax if her tax is ₹10,000 or more.",
        ["Freelance income is taxable, and there may be no employer TDS.",
         "Advance tax is due in instalments if your tax bill is ₹10,000 or more.",
         "The instalments fall on 15 June, 15 September, 15 December and 15 March.",
         "A simplified presumptive method exists for some freelancers, with conditions."],
        ["Assuming small side income is invisible to the taxman.",
         "Skipping advance tax and paying interest.",
         "Mixing personal and business money so records are a mess."],
        [
            _intro("No employer, no TDS", "When you work for a company, tax is deducted before the money reaches you. When you freelance, nobody does that for you, so you have to plan for tax yourself."),
            _chat("Ananya's freelance year", "Ananya asks Lumi", [
                ("friend", "Ananya", "I started freelancing. Clients pay me in full. Who deducts my tax?"),
                ("lumi", "Lumi", "Some clients deduct a small TDS, but many do not. Either way the income is taxable and it is on you to report it."),
                ("friend", "Ananya", "And if I owe a lot, do I wait until July next year?"),
                ("lumi", "Lumi", "If your tax for the year will be ₹10,000 or more, you generally pay advance tax in instalments during the year."),
                ("friend", "Ananya", "When?"),
                ("lumi", "Lumi", "15 June, 15 September, 15 December and 15 March, paying about 15%, 45%, 75% and 100% cumulatively."),
                ("friend", "Ananya", "That sounds like a lot to track."),
                ("lumi", "Lumi", "Put the dates in your phone. Many freelancers also move 20 to 30% of each payment to a separate account for tax."),
            ], "Freelancers must plan for tax themselves. Set aside a share of every payment."),
            _match("Match the advance tax date to the cumulative share due", [
                ("15 June", "15% of the year's tax"),
                ("15 September", "45% of the year's tax"),
                ("15 December", "75% of the year's tax"),
                ("15 March", "100% of the year's tax"),
            ]),
            _teach("Advance tax in plain words",
                   "Advance tax means paying income tax during the year rather than in one lump after it. If your total tax bill for the year, after TDS, will be ₹10,000 or more, you pay it in four instalments: by 15 June, 15 September, 15 December and 15 March. Missing instalments can lead to interest. Some small professionals and businesses can choose a presumptive scheme, which treats a fixed share of receipts as profit, such as 50% for eligible professionals under Section 44ADA, and then pay in a single instalment by 15 March. Conditions and limits apply.",
                   ["Needed if tax for the year is ₹10,000 or more", "Four instalments: 15 Jun, 15 Sep, 15 Dec, 15 Mar", "Interest applies if you underpay", "Presumptive scheme: simplified, with conditions"]),
            _example("The ₹40,000 tax bill",
                     "Ananya expects a tax bill of ₹40,000 for the year. By 15 June she should have paid 15%, which is ₹6,000. By 15 September, 45% in total, which is ₹18,000, so another ₹12,000. By 15 December, 75%, ₹30,000, another ₹12,000. By 15 March, all ₹40,000, another ₹10,000.",
                     "Small, regular payments are easier than one giant bill."),
            _swipe("Side income: myth or fact?", [
                ("Freelance income is taxable even if no employer deducts TDS.", "fact", "All income is taxable. TDS is just a way of collecting early."),
                ("Small side income does not need to be reported.", "myth", "Income of any size is reportable. Check the thresholds for your case."),
                ("Advance tax can be needed if your yearly tax is ₹10,000 or more.", "fact", "That is the usual threshold, after TDS. Missing instalments can bring interest."),
                ("Moving a share of each client payment into a separate account helps with tax time.", "fact", "A tax pot means the money is ready and not spent."),
            ]),
            _choice("Ananya has just been paid ₹50,000 by a client with no TDS. She feels rich and wants to spend it all on a new phone.",
                    "What is the wiser move?",
                    [("Set aside a share for tax, such as 20 to 30%, before spending the rest", "good",
                      "Right. Nobody has deducted tax, so the tax bill is still hers. A tax pot means she is not scrambling in March.",
                      _outcome(("Payment received", 50000), ("Share to set aside at 25%", 12500), "She can spend the other ₹37,500 without worry. The percentage depends on her real tax rate.")),
                     ("Spend everything and deal with tax when asked", "bad", "Tax is due whether or not she has the money. Interest and stress can follow."),
                     ("Hide the payment so it is not reported", "bad", "Income must be reported. Hiding it is illegal and risky, because banks and clients report payments too.")]),
            _choice("Raman, a freelancer, expects a ₹40,000 tax bill. He plans to pay it all in one go next July.",
                    "What is the likely problem?",
                    [("Advance tax instalments are due during the year, so paying late can add interest", "good",
                      "Right. With a bill of ₹10,000 or more, tax is due in instalments through the year. Paying everything next July can attract interest. Some presumptive-scheme taxpayers pay in one instalment by 15 March.",
                      _outcome(("Total tax", 40000), ("Due by 15 March", 40000), "The full amount is due by 15 March, not the next July.")),
                     ("None, because he can pay any time before July", "bad", "That date is for filing, but advance tax is due earlier when the bill is large."),
                     ("None, because freelancers never pay advance tax", "bad", "Freelancers with sizeable tax generally do.")]),
            _mcq("When is advance tax generally needed?", ["Never", "If your yearly tax is ₹10,000 or more", "Only for salaried people", "Only above ₹10 lakh"], 1,
                 "If your yearly tax, after TDS, is ₹10,000 or more, you generally pay advance tax in instalments."),
            _mcq("By 15 September, how much of the year's tax should generally be paid in total?", ["15%", "45%", "75%", "100%"], 1,
                 "The cumulative schedule is 15% by 15 June, 45% by 15 September, 75% by 15 December and 100% by 15 March."),
            _flash("Advance tax, in one line", "If you owe ₹10,000 or more in a year, pay in four instalments."),
        ], xp=30)

    m["concepts"] = [c1, c2, c3]
    ch["modules"] = [m]
    return ch
