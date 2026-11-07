"""FinLearn logo from design/brand/source-logo.webp -> Android icons, splash, store icon, in-app image.
Run: python design/brand/make_logo.py   (needs Pillow)"""
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RES = ROOT / "frontend/android/app/src/main/res"
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
CREAM = (254, 249, 248)
N = 1254


def draw_master():
    """Simplified FinLearn mark: three rising white bars and a gold arrow on an orange tile (reads at icon size)."""
    k = 4; n = N * k; u = n / 100
    top, bot = (255, 120, 40), (255, 90, 90)
    g = Image.new("RGB", (n // 8, n // 8))
    px = g.load()
    for y in range(g.height):
        for x in range(g.width):
            t = (x + y) / (g.width + g.height)
            px[x, y] = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
    im = g.resize((n, n), Image.BILINEAR).convert("RGBA")
    d = ImageDraw.Draw(im)
    for x0, y0 in [(22, 62), (42, 53), (62, 44)]:
        d.rounded_rectangle([x0 * u, y0 * u, (x0 + 17) * u, 84 * u], 5 * u, fill=(255, 255, 255))
    gold = (255, 214, 10)
    pts = [(20, 52), (36, 44), (50, 37), (64, 29)]
    d.line([(x * u, y * u) for x, y in pts], fill=gold, width=int(8 * u), joint="curve")
    d.ellipse([(20 - 4) * u, (52 - 4) * u, (20 + 4) * u, (52 + 4) * u], fill=gold)
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    L = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5; dx, dy = (x2 - x1) / L, (y2 - y1) / L
    tip = (x2 + dx * 15, y2 + dy * 15)
    d.polygon([(tip[0] * u, tip[1] * u), ((x2 - dy * 11) * u, (y2 + dx * 11) * u), ((x2 + dy * 11) * u, (y2 - dx * 11) * u)], fill=gold)
    return im.resize((N, N), Image.LANCZOS).convert("RGB")


if (HERE / "out/tile-master.png").exists():  # Lumi-face logo (design/brand/make_lumi_logo notes in TASKS)
    src = Image.open(HERE / "out/tile-master.png").convert("RGB")
    FG = Image.open(HERE / "out/fg-master.png").convert("RGBA")
else:
    src = draw_master(); FG = None


def mask(shape, size=N):
    m = Image.new("L", (size * 2, size * 2), 0)
    d = ImageDraw.Draw(m)
    if shape == "circle": d.ellipse([0, 0, size * 2 - 1, size * 2 - 1], fill=255)
    else: d.rounded_rectangle([0, 0, size * 2 - 1, size * 2 - 1], int(size * 2 * 0.235), fill=255)
    return m.resize((size, size), Image.LANCZOS)


def shaped(shape):
    im = src.convert("RGBA"); im.putalpha(mask(shape)); return im


def flat():  # square, corners filled (black corner pixels replaced by cream)
    bg = Image.new("RGB", src.size, CREAM)
    bg.paste(src, (0, 0), mask("round"))
    return bg


def save(im, path, size):
    path.parent.mkdir(parents=True, exist_ok=True)
    im.resize((size, size), Image.LANCZOS).save(path)


save(flat(), OUT / "icon-512.png", 512)
save(shaped("round"), OUT / "logo-rounded.png", 512)
save(shaped("round"), ROOT / "frontend/src/assets/logo.png", 256)
for dens, px, fg in [("mdpi", 48, 108), ("hdpi", 72, 162), ("xhdpi", 96, 216), ("xxhdpi", 144, 324), ("xxxhdpi", 192, 432)]:
    d = RES / f"mipmap-{dens}"
    save(shaped("round"), d / "ic_launcher.png", px)
    save(shaped("circle"), d / "ic_launcher_round.png", px)
    save(FG if FG is not None else flat(), d / "ic_launcher_foreground.png", fg)
(RES / "values/ic_launcher_background.xml").write_text(
    '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#FF6B35</color>\n</resources>')
for f in RES.glob("drawable*/splash.png"):
    w, h = Image.open(f).size
    bg = Image.new("RGBA", (w, h), CREAM + (255,))
    k = int(min(w, h) * 0.42)
    bg.alpha_composite(shaped("round").resize((k, k), Image.LANCZOS), ((w - k) // 2, (h - k) // 2))
    bg.convert("RGB").save(f)
print("done")
