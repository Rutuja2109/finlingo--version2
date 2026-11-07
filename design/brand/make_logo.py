"""FinLearn logo from design/brand/source-logo.webp -> Android icons, splash, store icon, in-app image.
Run: python design/brand/make_logo.py   (needs Pillow)"""
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RES = ROOT / "frontend/android/app/src/main/res"
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
CREAM = (254, 249, 248)
src = Image.open(HERE / "source-logo.webp").convert("RGB")
N = src.width


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
    save(flat(), d / "ic_launcher_foreground.png", fg)
(RES / "values/ic_launcher_background.xml").write_text(
    '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#FEF9F8</color>\n</resources>')
for f in RES.glob("drawable*/splash.png"):
    w, h = Image.open(f).size
    bg = Image.new("RGBA", (w, h), CREAM + (255,))
    k = int(min(w, h) * 0.42)
    bg.alpha_composite(shaped("round").resize((k, k), Image.LANCZOS), ((w - k) // 2, (h - k) // 2))
    bg.convert("RGB").save(f)
print("done")
