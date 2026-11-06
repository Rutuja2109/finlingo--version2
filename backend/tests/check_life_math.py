"""Recomputes every number quoted in the Taxes and Insurance lessons (new regime FY 2026-27, old regime, capital gains)."""
bad = 0


def ok(name, cond):
    global bad
    print(("OK  " if cond else "BAD ") + name)
    bad += 0 if cond else 1


NEW = [(400000, 0), (800000, .05), (1200000, .10), (1600000, .15), (2000000, .20), (2400000, .25), (10**12, .30)]


def new_tax(taxable):
    t, lo = 0.0, 0
    for hi, r in NEW:
        if taxable > lo:
            t += (min(taxable, hi) - lo) * r
        lo = hi
    return t


def old_tax(taxable):
    t = 0.0
    for lo, hi, r in [(250000, 500000, .05), (500000, 1000000, .20), (1000000, 10**12, .30)]:
        if taxable > lo:
            t += (min(taxable, hi) - lo) * r
    return t


cess = lambda t: t * 1.04
ok("taxable 8,00,000 -> 20,000 before rebate", new_tax(800000) == 20000)
ok("salary 15L: taxable 14.25L, tax 93,750, cess 3,750, total 97,500", new_tax(1425000) == 93750 and cess(93750) == 97500)
ok("salary 10L: taxable 9.25L, tax before rebate 32,500 (20,000 + 12,500), under the 60,000 rebate", new_tax(925000) == 32500 and new_tax(925000) <= 60000)
ok("salary 12.75L: taxable 12L, tax exactly 60,000 = the rebate", new_tax(1200000) == 60000)
ok("salary 9L: taxable 8.25L is under 12L (Sana)", 900000 - 75000 == 825000)
ok("Aman old regime: taxable 8L -> 72,500, cess 2,900, total 75,400", old_tax(800000) == 72500 and round(cess(old_tax(800000)) - old_tax(800000)) == 2900 and round(cess(old_tax(800000))) == 75400)
ok("Aman: new regime taxable 9.25L is nil after rebate", new_tax(925000) <= 60000)
d = cess(new_tax(1625000)) - cess(new_tax(1525000))
ok("Meera 16L -> 17L: taxable 15.25L tax 1,08,750; 16.25L tax 1,25,000", new_tax(1525000) == 108750 and new_tax(1625000) == 125000)
ok("Meera: extra tax with cess is 16,900 and she keeps 83,100", round(d) == 16900 and 100000 - round(d) == 83100)
ok("Riya LTCG: 1,75,000 - 1,25,000 = 50,000 x 12.5% = 6,250, cess 250, total 6,500", (175000 - 125000) * .125 == 6250 and 6250 * .04 == 250)
ok("Riya STCG: 40,000 x 20% = 8,000, cess 320, total 8,320", 40000 * .20 == 8000 and 8000 * .04 == 320)
ok("Dev crypto: 70,000 - 50,000 = 20,000 x 30% = 6,000, cess 240, total 6,240 (31.2%)", 20000 * .30 == 6000 and 6000 * .04 == 240 and round(6240 / 20000 * 100, 1) == 31.2)
fv = 40000 * ((1.10 ** 20 - 1) / 0.10)
ok("Plan B: 40,000 a year for 20 years at 10% is about 22.9 lakh", abs(fv - 2291000) < 2000)
ok("Plan B cover is 20 times Plan A (1 crore vs 5 lakh)", 10000000 / 500000 == 20 and 10000 + 40000 == 50000)
ok("Aarav: 10x and 15x of 8 lakh = 80 lakh to 1.2 crore", 8 * 10 == 80 and 8 * 15 == 120)
ok("room rent: 3,000 / 6,000 = 50% of 2,00,000 = 1,00,000", 200000 * 3000 / 6000 == 100000)
print("\nFAILED: %d" % bad if bad else "\nALL PASSED")
raise SystemExit(1 if bad else 0)
