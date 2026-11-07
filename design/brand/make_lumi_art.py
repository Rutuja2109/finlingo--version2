"""Splash screens and the Play Store feature graphic: logo tile + Lumi. Needs Edge, websocket-client, Pillow, node.
Run after make_logo.py:  python design/brand/make_lumi_art.py"""
import base64, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "design/store"))
from make_assets import Cdp  # noqa: E402

lib = Path(tempfile.mkdtemp()) / "l.mjs"
lib.write_text((ROOT / "frontend/src/lib/lumiSvg.js").read_text(encoding="utf-8"), encoding="utf-8")
LUMI = subprocess.run(["node", "-e", f'import("{lib.as_uri()}").then(m=>process.stdout.write(m.lumiMarkup("cheer")))'],
                      capture_output=True, text=True, check=True).stdout
tile = "data:image/png;base64," + base64.b64encode((HERE / "out/logo-rounded.png").read_bytes()).decode()
CREAM = "#FEF9F8"

splash = f"""<!doctype html><meta charset=utf-8><style>html,body{{margin:0;width:1200px;height:1200px;background:{CREAM};overflow:hidden}}
.w{{position:relative;width:1200px;height:1200px}}img{{position:absolute;left:300px;top:240px;width:600px;height:600px;filter:drop-shadow(0 18px 30px rgba(255,107,53,.35))}}
svg{{position:absolute;left:420px;top:600px;width:360px;height:360px}}
p{{position:absolute;left:0;right:0;top:880px;margin:0;text-align:center;font:900 96px Outfit,sans-serif;color:#1C1C2E;letter-spacing:-2px}}</style>
<link rel=stylesheet href="https://fonts.googleapis.com/css2?family=Outfit:wght@900&display=swap">
<div class=w><img src="{tile}"><p>FinLearn</p></div>"""
(HERE / "out/splash.html").write_text(splash, encoding="utf-8")

feat = (ROOT / "design/store/feature.html").read_text(encoding="utf-8")
import re
feat = re.sub(r'<img src="[^"]*">', f'<div class="art"><img src="{tile}"></div>', feat)
feat = feat.replace("img{width:340px;height:340px;flex:none;margin-left:auto}",
    ".art{position:relative;width:400px;height:400px;flex:none;margin-left:auto}.art img{position:absolute;left:0;top:10px;width:270px;height:270px;filter:drop-shadow(0 12px 20px rgba(0,0,0,.25))}"
    ".art svg{position:absolute;right:-10px;bottom:-30px;width:250px;height:250px}")
(HERE / "out/feature.html").write_text(feat, encoding="utf-8")

b = Cdp()
try:
    b.size(1200, 1200, 1); b.go((HERE / "out/splash.html").as_uri(), 4); b.shot("splash-master.png")
    b.size(1024, 500, 1); b.go((HERE / "out/feature.html").as_uri(), 4); b.shot("feature-1024x500.png")
finally:
    b.close()
import os
# Cdp.shot writes into design/store/out; move the results next to the other brand art and into the app.
store_out = ROOT / "design/store/out"
master = Image.open(store_out / "splash-master.png").convert("RGB")
(HERE / "out/splash-master.png").write_bytes((store_out / "splash-master.png").read_bytes())
for f in (ROOT / "frontend/android/app/src/main/res").glob("drawable*/splash.png"):
    w, h = Image.open(f).size
    bg = Image.new("RGB", (w, h), (254, 249, 248))
    k = min(w, h)
    bg.paste(master.resize((k, k), Image.LANCZOS), ((w - k) // 2, (h - k) // 2))
    bg.save(f)
print("done")
