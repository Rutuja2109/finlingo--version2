"""Insurance Basics, chapter 2: "When it's time to claim". Rupees. Regulations (IRDAI) change; lessons describe how things
usually work and point learners to their policy documents. Educational, not advice.
Figures are checked in tests/check_more_chapters.py."""
from seed_data import _id, _intro, _teach, _example, _flash, _mcq, _concept
from seed_finance import _choice, _outcome
from seed_money_more import _chat, _swipe, _slider, _match

CHAPTER_KEY = "when-its-time-to-claim"
NOTE = "Rules and policy terms differ by insurer and change over time, so always read your own policy document."


def build_insurance_chapter_two(course_id):
    ch_id = _id()
    ch = {"id": ch_id, "course_id": course_id, "order": 2, "key": CHAPTER_KEY,
          "title": "When it's time to claim",
          "description": "How a health claim really works, whether your cover is big enough, and what to buy at each stage of life."}
    m_id = _id()
    m = {"id": m_id, "chapter_id": ch_id, "order": 1, "title": "Insurance in real life"}

    # ---------------------------------------------------------------- 1. claims
    c1 = _concept(m_id, 1,
        "How a health claim really works",
        "Know the steps of a cashless or reimbursement claim and why claims get rejected.",
        "A policy is only as good as its claim. In a cashless claim the insurer pays the hospital directly after approving it. "
        "In a reimbursement claim you pay first and the insurer pays you back. Most rejections come from avoidable mistakes. " + NOTE,
        "Rhea needs planned surgery. She picks a network hospital, the hospital sends a pre-authorisation request to the insurer, "
        "and the insurer approves it. At discharge she pays only the non-covered items. Had she gone to a non-network hospital, she would have paid first and claimed later.",
        ["Cashless: the insurer pays a network hospital directly after pre-approval.",
         "Reimbursement: you pay, then claim with bills and documents.",
         "Most rejections come from non-disclosure, waiting periods, exclusions and missing papers.",
         "Tell the insurer early, and keep every document."],
        ["Hiding an existing illness when buying.",
         "Going to a non-network hospital and expecting cashless.",
         "Throwing away bills and discharge papers."],
        [
            _intro("The day you need it", "You pay premiums for years hoping never to use them. The day you do, how smoothly the claim goes matters more than anything on the brochure. " + NOTE),
            _chat("Rhea's surgery", "Rhea asks Lumi before a planned operation", [
                ("friend", "Rhea", "My doctor says I need surgery next month. How do I use my health insurance?"),
                ("lumi", "Lumi", "First, check if the hospital is in your insurer's network. If it is, you can usually go cashless."),
                ("friend", "Rhea", "What does cashless mean?"),
                ("lumi", "Lumi", "The hospital sends a request called pre-authorisation. If the insurer approves, it pays the hospital directly. You pay only for items not covered."),
                ("friend", "Rhea", "And if it is not a network hospital?"),
                ("lumi", "Lumi", "Then you pay first and claim later with bills, the discharge summary and other papers. It is called reimbursement."),
                ("friend", "Rhea", "Do I need to tell the insurer early?"),
                ("lumi", "Lumi", "Yes. For planned treatment, inform them in advance. For emergencies, inform as soon as you can, usually within a day or so."),
            ], "Plan early, use network hospitals if you can, and keep every paper."),
            _match("Match the term to its meaning", [
                ("Cashless claim", "Insurer pays a network hospital directly"),
                ("Reimbursement", "You pay first, then the insurer repays you"),
                ("Pre-authorisation", "Insurer's approval before planned treatment"),
                ("Waiting period", "Time before certain illnesses are covered"),
            ]),
            _teach("Why claims get rejected",
                   "Most rejections are not about the insurer being unfair. They come from non-disclosure, where you did not mention an existing illness; claiming for something in the waiting period; treatment that is excluded in the policy; or missing or late paperwork. Current IRDAI rules limit waiting periods for pre-existing diseases to a maximum of three years and bar many rejections after five years of continuous cover, except for fraud. Always read your policy's exclusions and waiting periods.",
                   ["Non-disclosure of illnesses is the top avoidable reason", "Waiting periods delay cover for some illnesses", "Exclusions: some treatments are never covered", "Keep bills, reports and the discharge summary"]),
            _example("The ten-second lie",
                     "Aman skips the question on the form about his past asthma, so his premium looks lower. Two years later he is hospitalised for a related problem. The insurer finds the earlier records and rejects the claim for non-disclosure. A few seconds of dishonesty on the form cost him the entire bill.",
                     "Tell the truth on the form. A slightly higher premium is far cheaper than a rejected claim."),
            _swipe("Claims: myth or fact?", [
                ("In a cashless claim, the insurer pays a network hospital directly.", "fact", "That is what cashless means, after pre-authorisation."),
                ("It is safe to hide an existing illness to get a lower premium.", "myth", "Non-disclosure is a top reason for rejection, and it can be found later."),
                ("You should keep all bills and the discharge summary after treatment.", "fact", "They are needed for reimbursement and as proof."),
                ("Every treatment is covered from day one.", "myth", "Waiting periods and exclusions apply to many conditions."),
            ]),
            _choice("Aman has a past asthma diagnosis. The agent says, 'Just leave it off the form. Nobody checks.'",
                    "What is the right move?",
                    [("Declare it honestly and accept the terms the insurer offers", "good",
                      "Right. A declared condition may add a waiting period or cost, but a hidden one can sink a future claim. This is education, not advice.",
                      _outcome(("Hospital bill later", 300000), ("Claim paid if hidden condition found", 0), "A rejected claim could leave him paying the whole ₹3,00,000 himself.")),
                     ("Leave it off to get a lower premium", "bad", "If the insurer finds it later, the claim can be rejected and the policy cancelled."),
                     ("Leave it off but tell the agent verbally", "bad", "Only what is written on the proposal form counts. Verbal promises protect nobody.")]),
            _choice("Rhea is in a medical emergency and is taken to the nearest hospital, which is not in her insurer's network.",
                    "What should she or her family do?",
                    [("Inform the insurer as soon as possible, keep all bills and papers, and file a reimbursement claim", "good",
                      "Right. Without a network, cashless may not work, but reimbursement still can. Keep every receipt, report and the discharge summary.",
                      _outcome(("Hospital bill paid upfront", 200000), ("Reimbursed if covered", 200000), "She pays first, then claims it back, subject to the policy terms.")),
                     ("Do nothing because only network hospitals count", "bad", "Non-network treatment can usually still be claimed, subject to the policy."),
                     ("Wait until she feels better to tell the insurer", "bad", "Late intimation can complicate the claim. Inform early.")]),
            _mcq("What does 'cashless' mean in a health claim?", ["You pay nothing ever", "The insurer pays the network hospital directly after approval", "The hospital is free", "You pay in cash only"], 1,
                 "In a cashless claim the insurer settles with a network hospital, and you pay only items not covered."),
            _mcq("Which is a common reason a claim is rejected?", ["Keeping bills", "Not disclosing a pre-existing illness", "Using a network hospital", "Paying the premium on time"], 1,
                 "Non-disclosure of existing conditions is one of the most common avoidable reasons for rejection."),
            _flash("Claims, in one line", "Be honest on the form, use network hospitals, inform early, keep every paper."),
        ], xp=30)

    # ---------------------------------------------------------------- 2. adequacy
    c2 = _concept(m_id, 2,
        "Is your cover big enough?",
        "See how rising medical costs shrink your cover, and how top-ups and portability help.",
        "Hospital bills rise faster than ordinary prices, so a ₹5 lakh cover that felt big years ago can fall short. "
        "A super top-up adds a large cover at a low premium, and you can switch insurers through portability. " + NOTE,
        "Dev has ₹5 lakh of cover and gets a ₹12 lakh bill. The base policy pays ₹5 lakh and he pays ₹7 lakh. With a ₹20 lakh super top-up that starts after ₹5 lakh, "
        "the top-up pays the extra ₹7 lakh and he pays almost nothing.",
        ["Medical costs often rise faster than general prices, estimated by many at around 10% a year.",
         "A super top-up pays once a bill passes a set amount (the deductible).",
         "Top-ups usually cost far less than a bigger base policy.",
         "Portability lets you switch insurers and keep credit for waiting periods."],
        ["Staying with a small cover for years without reviewing it.",
         "Assuming the employer's cover is enough.",
         "Letting a policy lapse and losing waiting-period credit."],
        [
            _intro("Is ₹5 lakh enough?", "A few years ago ₹5 lakh sounded huge. Then someone you know spent ₹12 lakh on a few weeks in hospital. Costs have a way of growing." + " " + NOTE),
            _chat("The ₹12 lakh bill", "Dev asks Lumi about cover", [
                ("friend", "Dev", "My dad's hospital bill was ₹12 lakh and his policy was ₹5 lakh. Who paid the rest?"),
                ("lumi", "Lumi", "Your family did. A cover only pays up to its limit, so ₹5 lakh paid and the other ₹7 lakh came from savings."),
                ("friend", "Dev", "Can I get a bigger policy cheaply?"),
                ("lumi", "Lumi", "A super top-up often can. It starts paying only after your base cover is used, so it costs much less than a big base policy."),
                ("friend", "Dev", "How does it work in that case?"),
                ("lumi", "Lumi", "Base ₹5 lakh covers the first ₹5 lakh. A ₹20 lakh super top-up with a ₹5 lakh deductible then covers the next ₹7 lakh."),
                ("friend", "Dev", "So I would pay almost nothing?"),
                ("lumi", "Lumi", "Apart from non-covered items. It is a useful tool to look into. Check the terms."),
            ], "A super top-up can add big cover cheaply. Review your cover as costs rise."),
            _slider("What could treatment cost later?", "Move the sliders to see how a bill that costs this much today might look in future, at an assumed rate of medical inflation.", "inflation",
                    [("price", "Treatment cost today", 100000, 2000000, 50000, 300000, "₹", ""), ("years", "After how many years", 1, 20, 1, 10, "", " yrs"), ("rate", "Medical inflation per year", 4, 15, 1, 10, "", "%")],
                    "Medical costs tend to rise faster than ordinary prices. A cover bought long ago can quietly become too small."),
            _teach("Top-ups and portability",
                   "A top-up or super top-up adds extra cover on top of your base policy. A top-up pays when a single bill passes the deductible, and a super top-up pays when all bills in a year add up past it. Because it only steps in after the deductible, the premium is much lower than a bigger base policy. Portability lets you move your policy to another insurer at renewal while keeping credit for the waiting periods you have already served. Always check the terms before you switch.",
                   ["Base policy pays first", "Super top-up pays after the deductible", "Much cheaper than a bigger base policy", "Portability keeps waiting-period credit"]),
            _example("Who pays what",
                     "A hospital bill is ₹12,00,000. Without any top-up, a ₹5,00,000 policy pays ₹5,00,000 and the family pays ₹7,00,000. With a ₹20,00,000 super top-up whose deductible is ₹5,00,000, the base policy pays ₹5,00,000 and the top-up pays the remaining ₹7,00,000, so the family pays almost nothing, apart from items the policy does not cover.",
                     "A top-up is one of the cheapest ways to protect against a big bill."),
            _swipe("Cover size: myth or fact?", [
                ("Hospital costs usually rise faster than general inflation.", "fact", "Many estimates put medical inflation at around 10% a year, higher than ordinary prices."),
                ("A super top-up pays from the first rupee of the bill.", "myth", "It pays only after the deductible is crossed."),
                ("You can switch insurers and keep credit for waiting periods.", "fact", "That is portability. Check the terms and apply before renewal."),
                ("Employer health cover is always enough and always yours.", "myth", "It is usually limited and ends if you leave the job."),
            ]),
            _choice("Dev, 24, has only his employer's ₹5 lakh group cover. A friend suggests buying his own ₹5 lakh base cover plus a ₹20 lakh super top-up.",
                    "Why is this a sensible idea to explore?",
                    [("His employer's cover ends if he leaves, and big bills can cross ₹5 lakh, while a top-up adds cover cheaply", "good",
                      "Right. A policy of his own continues across jobs, and a super top-up covers rare, very large bills at low cost. Compare plans and read the terms. This is education, not advice.",
                      _outcome(("Bill", 1200000), ("Family pays with ₹5 lakh cover only", 700000), "Without a top-up he would pay ₹7 lakh himself.")),
                     ("It is wasteful because he is young and healthy", "ok", "Healthy people still have accidents and emergencies. Cover bought young also starts waiting periods early."),
                     ("He should rely on savings for any big bill", "bad", "One large bill can wipe out years of savings.")]),
            _choice("Neha's policy is five years old and she is unhappy with her insurer's service. She worries about losing the waiting periods she has already served.",
                    "What option should she look into?",
                    [("Portability: moving to another insurer at renewal while keeping credit for waiting periods, after checking terms", "good",
                      "Right. Portability exists for exactly this. Apply well before the renewal date and compare the new policy's terms."),
                     ("Cancel the policy and buy a fresh one", "bad", "A fresh policy restarts waiting periods, so she could lose cover for illnesses she has already waited out."),
                     ("Stop paying and rely on savings", "bad", "Lapsing loses all the credit she has built up.")]),
            _mcq("A ₹12 lakh bill, ₹5 lakh base cover and a ₹20 lakh super top-up with a ₹5 lakh deductible. How much does the super top-up pay?", ["₹5 lakh", "₹7 lakh", "₹12 lakh", "₹20 lakh"], 1,
                 "The base policy pays the first ₹5 lakh. The top-up pays the remaining ₹7 lakh, which is above the deductible."),
            _mcq("What does portability let you do?", ["Carry your policy to another country", "Switch insurers and keep waiting-period credit", "Pay premiums in instalments", "Cancel and get a refund"], 1,
                 "Portability lets you move to another insurer while keeping credit for waiting periods already served."),
            _flash("Cover size, in one line", "Bills keep rising. A cheap super top-up can cover the big ones."),
        ], xp=30)

    # ---------------------------------------------------------------- 3. life stages
    c3 = _concept(m_id, 3,
        "What to buy at each stage of life",
        "Decide which insurance matters most when you are a student, in a first job, or have dependents.",
        "You do not need every policy at once. A student mostly needs to be covered by a family floater. In a first job, own health cover and personal accident cover matter. "
        "Term insurance becomes important once someone depends on your income. " + NOTE,
        "Zoya, 22, is on her parents' family floater. She starts a job and her employer gives group health cover, but she also buys a personal accident policy and a small own health plan. "
        "She will add term insurance when she has people depending on her.",
        ["Students are usually covered under a parent's family floater.",
         "In a first job, own health cover keeps working if you change jobs.",
         "Personal accident cover is cheap and helps if you cannot work.",
         "Buy term insurance when someone depends on your income."],
        ["Buying life insurance with no dependents.",
         "Relying only on employer cover.",
         "Buying travel or gadget insurance by default without checking the need."],
        [
            _intro("Not everything, not now", "Insurance sellers will happily offer you ten policies. You need a few, at the right time. Let's work out which." + " " + NOTE),
            _chat("What do I actually need?", "Zoya asks Lumi at 22", [
                ("friend", "Zoya", "I just got my first job. An agent says I need life insurance, health, accident, travel and mobile cover. Do I?"),
                ("lumi", "Lumi", "Let's think about who depends on your income. Anyone?"),
                ("friend", "Zoya", "No, I live with my parents and I am not married."),
                ("lumi", "Lumi", "Then life insurance can wait. What you need most is health cover that stays with you if you change jobs."),
                ("friend", "Zoya", "My company gives group cover."),
                ("lumi", "Lumi", "Good, but it usually ends when you leave. A small policy of your own is a smart add. A cheap personal accident policy can also help."),
                ("friend", "Zoya", "And when do I think about term insurance?"),
                ("lumi", "Lumi", "When someone relies on your income, like a spouse, children or parents. Until then, skip it."),
            ], "Buy what you need now. Add term cover when someone depends on you."),
            _match("Match the life stage to the insurance priority", [
                ("Student", "Covered under a parent's family floater"),
                ("First job, no dependents", "Own health cover and personal accident cover"),
                ("Married or with children", "Term insurance plus a family health floater"),
                ("Parents retired", "Health cover for them, with a larger sum and a top-up"),
            ]),
            _teach("A simple order of priority",
                   "First, health insurance, because one hospital bill can wipe out years of savings. Second, personal accident cover if you earn an income, because it is cheap and helps if an injury stops you working. Third, term life insurance once anyone depends on your income, with cover that replaces several years of it. Fourth, specific cover such as vehicle and travel insurance when you need them. Skip policies that mix insurance and investment, which usually cost more and give less of both.",
                   ["1. Health cover", "2. Personal accident cover", "3. Term life cover when dependents exist", "4. Vehicle, travel and other cover when needed"]),
            _example("Cheap protection",
                     "A personal accident policy can cost only a few hundred to a couple of thousand rupees a year for a large sum insured, depending on the insurer and your occupation. If an injury keeps Zoya from working for months, it can pay a lump sum or income benefit. It is not a substitute for health or term cover, but it fills a gap cheaply.",
                     "Small, targeted cover can protect against big income shocks."),
            _swipe("Life stages: myth or fact?", [
                ("A single person with no dependents usually does not need a large term policy.", "fact", "Term insurance exists to replace income for people who rely on it."),
                ("Employer health cover continues even after you leave the job.", "myth", "Group cover usually ends when employment ends, so your own policy matters."),
                ("Insurance-plus-investment plans are the best of both worlds.", "myth", "They tend to cost more and give less of each. Term cover plus separate investing is usually simpler and cheaper."),
                ("Health insurance should be a priority before life insurance for a single young person.", "fact", "A hospital bill can arrive at any age and hit savings directly."),
            ]),
            _choice("Zoya, 22, single and living with her parents, is told by an agent to buy a ₹1 crore life insurance policy 'for her future'.",
                    "What is the smarter question to ask?",
                    [("'Who depends on my income?' If nobody, health and accident cover matter more than life cover right now", "good",
                      "Right. Term insurance protects dependents. Without any, the money is better used for health cover and investing. This is education, not advice."),
                     ("Buy it because it is cheap when you are young", "ok", "It is cheaper while young, but buying with no dependents can waste money. You can buy later when needed, subject to health."),
                     ("Buy it because it also gives a maturity benefit", "bad", "Plans with maturity benefits usually cost much more and return less. A plain term plan is simpler.")]),
            _choice("Arjun, 27, just got married, and his wife depends on his salary. He has only his employer's health cover and no life cover.",
                    "What should he look at first?",
                    [("A term insurance plan big enough to replace his income, and his own health policy that goes with him", "good",
                      "Right. Now that someone depends on his income, term cover matters, and personal health cover gives continuity across jobs.",
                      _outcome(("Annual income", 800000), ("Typical cover he might look at, 10 to 15 times income", 8000000), "Many people aim for 10 to 15 times annual income as a starting guide. Calculate your own needs.")),
                     ("Nothing, because marriage does not change risk", "bad", "It changes risk a lot. Someone now depends on his income."),
                     ("Buy an endowment plan so he gets his money back", "bad", "Endowment plans cost more and give less cover than term plus separate saving.")]),
            _mcq("What mainly decides whether you need term life insurance?", ["Your age", "Whether anyone depends on your income", "Your job title", "Your city"], 1,
                 "Term insurance exists to replace income for people who depend on it."),
            _mcq("Why should a person in a job still consider their own health policy?", ["Employer cover is unlimited", "Employer cover usually ends when you leave the job", "It is cheaper than group cover", "It is required by law"], 1,
                 "Group cover usually stops when you leave, so your own policy gives continuity."),
            _flash("Life stages, in one line", "Health first, accident next, term when someone depends on you."),
        ], xp=30)

    m["concepts"] = [c1, c2, c3]
    ch["modules"] = [m]
    return ch
