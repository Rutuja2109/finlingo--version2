"""Recomputes every number quoted in Investment Analysis chapters 2 to 4 (bonds, equity valuation, portfolios)."""
import math

bad = 0


def ok(name, cond):
    global bad
    print(("OK  " if cond else "BAD ") + name)
    bad += 0 if cond else 1


def price(face, c, y, n):
    return sum(face * c / (1 + y) ** t for t in range(1, n + 1)) + face / (1 + y) ** n


def mac(face, c, y, n):
    p = price(face, c, y, n)
    return sum(t * face * c / (1 + y) ** t for t in range(1, n + 1)) / p + n * face / (1 + y) ** n / p


near = lambda a, b, tol=0.01: abs(a - b) <= tol

# ---- fixed income
ok("8% coupon, 5y, 10% yield: coupons 303.26 + principal 620.92 = 924.18", near(80 * ((1 - 1.1 ** -5) / .1), 303.26) and near(1000 / 1.1 ** 5, 620.92) and near(price(1000, .08, .10, 5), 924.18))
ok("annuity factor at 10% for 5 years is 3.7908", near((1 - 1.1 ** -5) / .1, 3.7908, 0.0001))
ok("current yield 8.66%", near(80 / 924.18 * 100, 8.66))
ok("at 6% the price is 1,084.25 (336.99 + 747.26)", near(price(1000, .08, .06, 5), 1084.25) and near(80 * (1 - 1.06 ** -5) / .06, 336.99) and near(1000 / 1.06 ** 5, 747.26))
ok("par bond at coupon yield", near(price(1000, .08, .08, 5), 1000))
ok("gain to par is 75.82", near(1000 - 924.18, 75.82))
ok("zero 3y at 7% = 816.30", near(1000 / 1.07 ** 3, 816.30))
ok("zero 5y modified duration 4.63; prices 680.58 and 649.93; fall 4.50%", near(5 / 1.08, 4.63) and near(1000 / 1.08 ** 5, 680.58) and near(1000 / 1.09 ** 5, 649.93) and near((1000 / 1.09 ** 5) / (1000 / 1.08 ** 5) - 1, -0.0450, 0.0001))
ok("10y 6% par bond modified duration about 7.4; 2y about 1.8; ratio about 4", near(mac(1000, .06, .06, 10) / 1.06, 7.36, 0.01) and near(mac(1000, .06, .06, 2) / 1.06, 1.83, 0.01) and near(7.36 / 1.83, 4.0, 0.1))
md = mac(1000, .08, .10, 5) / 1.10
ok("8% 5y bond at 10%: modified duration 3.89; actual fall at 11% is 3.79%; ~889.1", near(md, 3.89, 0.01) and near((price(1000, .08, .11, 5) / price(1000, .08, .10, 5) - 1) * 100, -3.79, 0.01) and near(price(1000, .08, .11, 5), 889.15, 0.05))
ok("expected loss 12,000 = 1.2% of 10 lakh; spread 2.3 leaves 1.1", near(.02 * .60 * 1e6, 12000) and near(.02 * .6 * 100, 1.2) and near(9.5 - 7.2, 2.3) and near(2.3 - 1.2, 1.1))
ok("credit mcq: 4% x 75% x 5,00,000 = 15,000", near(.04 * .75 * 5e5, 15000))
ok("duration mcq: 5 x 0.5 = 2.5", 5 * 0.5 == 2.5)

# ---- equity
ok("Gordon: D1 10.60, V0 212, at 12% 176.67 (16.7% lower)", near(10 * 1.06, 10.6) and near(10.6 / .05, 212) and near(10.6 / .06, 176.67) and near(176.67 / 212 - 1, -0.167, 0.001))
ok("implied r = 12/200 + 5% = 11%", near(12 / 200 + .05, .11, 1e-9))
ok("DDM mcq: 5.20 / 0.05 = 104", near(5 * 1.04 / (.09 - .04), 104))
ok("P/E 15, earnings yield 6.67%, implied 360", 300 / 20 == 15 and near(20 / 300 * 100, 6.67) and 18 * 20 == 360)
ok("PEG A 1.25, B 0.80", 15 / 12 == 1.25 and 20 / 25 == 0.8)
ok("P/E mcqs: 240/16=15 and 6.67%; 24/12=2", 240 / 16 == 15 and near(16 / 240 * 100, 6.67) and 24 / 12 == 2)
ok("DuPont 24%; g = 14.4%", near(.08 * 1.5 * 2, .24, 1e-9) and near(.24 * .6, .144, 1e-9))
ok("Company X and Y both 18% ROE", near(.12 * 1.0 * 1.5, .18, 1e-9) and near(.04 * 1.5 * 3.0, .18, 1e-9))
ok("CFO: g 6% at 30% retention; 12% at 60%", near(.2 * .3, .06, 1e-9) and near(.2 * .6, .12, 1e-9))
ok("DuPont mcq 25%; g mcq 9%", near(.05 * 2 * 2.5, .25, 1e-9) and near(.15 * .6, .09, 1e-9))

# ---- portfolio
sd = lambda rho: math.sqrt(.6 ** 2 * .2 ** 2 + .4 ** 2 * .1 ** 2 + 2 * .6 * .4 * rho * .2 * .1)
ok("60/40: return 9.6%; risk 16% at rho 1, 13.74% at 0.3 (variance 0.01888), 12.65% at 0", near(.6 * 12 + .4 * 6, 9.6) and near(sd(1), .16, 1e-6) and near(sd(.3) * 100, 13.74) and near(sd(.3) ** 2, .01888, 1e-6) and near(sd(0) * 100, 12.65))
ok("portfolio mcq 7%", .5 * 10 + .5 * 4 == 7)
ok("CAPM 13%, 11%, 14.5%; alpha +1", near(.07 + 1.2 * .05, .13, 1e-9) and near(.07 + .8 * .05, .11, 1e-9) and near(.07 + 1.5 * .05, .145, 1e-9) and near(14 - 13, 1))
ok("CAPM mcq 13.0%", near(6 + 1.4 * (11 - 6), 13.0))
e, b = 1e6 * .6 * 1.2, 1e6 * .4 * 1.05
ok("rebalance: 7,20,000 + 4,20,000 = 11,40,000; equity 63.2%; sell 36,000; bonds 4,56,000", e == 720000 and b == 420000 and near(e / (e + b) * 100, 63.2, 0.05) and near(e - .6 * (e + b), 36000) and near(b + 36000, 456000) and near(.6 * (e + b), 684000))
ok("rebalance mcq: sell 50,000", 300000 - .5 * 500000 == 50000)

print("\nFAILED: %d" % bad if bad else "\nALL PASSED")
raise SystemExit(1 if bad else 0)
