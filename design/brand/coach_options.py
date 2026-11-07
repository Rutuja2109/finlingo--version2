"""Mock-ups: 10 'finance coach' mascot logo options. Output: design/store/out/options8.png"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "design/store"))
from make_assets import Cdp  # noqa: E402

INK = "#1C1C2E"
SKIN = "#F2C29B"


def whistle(x, y, s=1):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-9" y="-3.5" width="14" height="7" rx="3" fill="#FBBF24"/>'
            '<circle cx="4" cy="1" r="7" fill="#F59E0B"/><circle cx="4" cy="1" r="2.4" fill="#92400E"/></g>')


def cord(x1, x2, y1, y2, mx=50):
    return f'<path d="M{x1} {y1}L{mx} {y2}L{x2} {y1}" fill="none" stroke="#fff" stroke-width="2.2" stroke-linejoin="round"/>'


def face(cx=50, cy=47, glasses=True, col=INK):
    g = "".join(f'<circle cx="{cx + dx}" cy="{cy}" r="7" fill="none" stroke="{col}" stroke-width="2"/>' for dx in (-9, 9)) if glasses else ""
    return (f'<circle cx="{cx - 9}" cy="{cy}" r="2.6" fill="{col}"/><circle cx="{cx + 9}" cy="{cy}" r="2.6" fill="{col}"/>{g}'
            f'<path d="M{cx - 6} {cy + 12}Q{cx} {cy + 18} {cx + 6} {cy + 12}" stroke="{col}" stroke-width="2.4" fill="none" stroke-linecap="round"/>')


def man(shirt="#1E3A8A", hair="#3B2A20", skin=SKIN):
    return (f'<path d="M12 100Q14 73 50 71Q86 73 88 100Z" fill="{shirt}"/><path d="M41 71L50 84 59 71z" fill="#fff"/>{cord(40, 60, 72, 93)}{whistle(50, 93)}'
            f'<rect x="43" y="60" width="14" height="14" fill="{skin}"/><circle cx="28" cy="48" r="4.5" fill="{skin}"/><circle cx="72" cy="48" r="4.5" fill="{skin}"/>'
            f'<circle cx="50" cy="46" r="22" fill="{skin}"/><path d="M27 44Q26 22 50 22Q74 22 73 44Q64 32 50 34Q36 32 27 44Z" fill="{hair}"/>{face()}')


def woman():
    return ('<path d="M22 60Q18 22 50 20Q82 22 78 60L80 80Q50 86 20 80Z" fill="#2B1B17"/><path d="M12 100Q14 73 50 71Q86 73 88 100Z" fill="#FF6B35"/>'
            '<path d="M41 71L50 84 59 71z" fill="#fff"/>' + cord(40, 60, 72, 93) + whistle(50, 93)
            + '<rect x="43" y="60" width="14" height="14" fill="#E9B48C"/><circle cx="50" cy="46" r="21" fill="#F2C29B"/>'
            '<path d="M29 42Q30 24 50 24Q70 24 71 42Q58 34 50 36Q40 34 29 42Z" fill="#2B1B17"/>'
            '<path d="M26 46Q24 18 50 18Q76 18 74 46" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round"/>'
            '<rect x="21" y="42" width="7" height="12" rx="3" fill="#fff"/><path d="M24 54Q26 66 42 64" fill="none" stroke="#fff" stroke-width="2"/>'
            + face(glasses=False))


def bull(shirt="#fff"):
    return (f'<path d="M20 100Q24 80 50 78Q76 80 80 100Z" fill="{shirt}"/><path d="M45 79L50 92 55 79z" fill="#FF6B35"/>'
            '<path d="M27 38Q8 38 10 14Q22 26 34 30Z" fill="#F5F5F4" stroke="#D6D3D1" stroke-width="1.5"/>'
            '<path d="M73 38Q92 38 90 14Q78 26 66 30Z" fill="#F5F5F4" stroke="#D6D3D1" stroke-width="1.5"/>'
            '<ellipse cx="22" cy="48" rx="9" ry="5" transform="rotate(20 22 48)" fill="#A16207"/><ellipse cx="78" cy="48" rx="9" ry="5" transform="rotate(-20 78 48)" fill="#A16207"/>'
            '<ellipse cx="50" cy="48" rx="27" ry="25" fill="#C68642"/><ellipse cx="50" cy="63" rx="17" ry="12" fill="#F9C9A8"/>'
            '<circle cx="43" cy="63" r="2.2" fill="#92400E"/><circle cx="57" cy="63" r="2.2" fill="#92400E"/>'
            '<path d="M44 70Q50 75 56 70" stroke="#92400E" stroke-width="2" fill="none" stroke-linecap="round"/>'
            f'<circle cx="38" cy="44" r="3.4" fill="{INK}"/><circle cx="62" cy="44" r="3.4" fill="{INK}"/>'
            f'<path d="M31 37L44 40M69 37L56 40" stroke="{INK}" stroke-width="2.6" stroke-linecap="round"/>' + cord(38, 62, 80, 95) + whistle(50, 95, .9))


def owl():
    return ('<ellipse cx="50" cy="58" rx="31" ry="34" fill="#B45309"/><path d="M24 34L22 16 38 28zM76 34L78 16 62 28z" fill="#92400E"/>'
            '<ellipse cx="50" cy="70" rx="20" ry="20" fill="#FDE68A"/><circle cx="37" cy="48" r="12" fill="#fff"/><circle cx="63" cy="48" r="12" fill="#fff"/>'
            f'<circle cx="38" cy="49" r="5.5" fill="{INK}"/><circle cx="62" cy="49" r="5.5" fill="{INK}"/><circle cx="40" cy="47" r="1.8" fill="#fff"/><circle cx="64" cy="47" r="1.8" fill="#fff"/>'
            '<path d="M44 56L56 56 50 66z" fill="#F59E0B"/><path d="M22 24L50 12 78 24 50 36z" fill="#1E2A6B"/>'
            '<path d="M72 26V38" stroke="#FBBF24" stroke-width="2.2"/><circle cx="72" cy="40" r="2.8" fill="#FBBF24"/>' + cord(40, 60, 76, 88) + whistle(50, 90, .9))


def fox():
    return ('<path d="M50 86L16 52 22 18 40 36Q50 32 60 36L78 18 84 52Z" fill="#F97316"/><path d="M22 18L30 38 40 36zM78 18L70 38 60 36z" fill="#7C2D12"/>'
            '<path d="M50 86L26 58Q38 64 50 63Q62 64 74 58Z" fill="#fff"/>'
            f'<circle cx="50" cy="76" r="4.4" fill="{INK}"/><circle cx="38" cy="54" r="3" fill="{INK}"/><circle cx="62" cy="54" r="3" fill="{INK}"/>'
            f'<circle cx="38" cy="54" r="8" fill="none" stroke="{INK}" stroke-width="2.2"/><circle cx="62" cy="54" r="8" fill="none" stroke="{INK}" stroke-width="2.2"/>'
            f'<path d="M46 54H54" stroke="{INK}" stroke-width="2"/>')


def bunny_coach():
    ears = "".join(f'<ellipse cx="{x}" cy="22" rx="9.5" ry="19" transform="rotate({r} {x} 22)" fill="#fff"/>'
                   f'<ellipse cx="{x}" cy="24" rx="4.5" ry="12" transform="rotate({r} {x} 24)" fill="#FDA4AF"/>' for x, r in ((35, -9), (65, 9)))
    eyes = "".join(f'<circle cx="{x}" cy="55" r="9" fill="none" stroke="{INK}" stroke-width="2.4"/><circle cx="{x}" cy="55" r="4.6" fill="{INK}"/>'
                   f'<circle cx="{x + 1.6}" cy="53.4" r="1.5" fill="#fff"/>' for x in (38, 62))
    return (ears + '<circle cx="50" cy="56" r="29" fill="#fff"/>' + eyes
            + '<ellipse cx="50" cy="66" rx="3.6" ry="2.8" fill="#F472B6"/><path d="M45 71Q50 76 55 71" stroke="#1C1C2E" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
            '<path d="M22 40Q50 28 78 40" stroke="#E5484D" stroke-width="6" fill="none" stroke-linecap="round"/>' + cord(36, 64, 84, 94) + whistle(50, 94, .9))


def bear():
    return ('<circle cx="25" cy="30" r="10" fill="#92400E"/><circle cx="75" cy="30" r="10" fill="#92400E"/><circle cx="25" cy="30" r="5" fill="#F9C9A8"/><circle cx="75" cy="30" r="5" fill="#F9C9A8"/>'
            '<circle cx="50" cy="54" r="29" fill="#92400E"/><ellipse cx="50" cy="64" rx="14" ry="11" fill="#F9C9A8"/><ellipse cx="50" cy="60" rx="5" ry="3.6" fill="#1C1C2E"/>'
            f'<circle cx="38" cy="48" r="3.4" fill="#fff"/><circle cx="62" cy="48" r="3.4" fill="#fff"/><circle cx="38.6" cy="48.4" r="1.8" fill="{INK}"/><circle cx="62.6" cy="48.4" r="1.8" fill="{INK}"/>'
            f'<path d="M44 69Q50 74 56 69" stroke="{INK}" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
            '<path d="M24 38Q24 18 50 18Q76 18 76 38Z" fill="#E5484D"/><path d="M60 36Q84 36 86 42Q70 44 60 40Z" fill="#B91C1C"/>' + cord(38, 62, 82, 94) + whistle(50, 94, .9))


def tile(bg, body):
    return (f'<div class="t" style="background:{bg}"><svg viewBox="0 0 100 100"><defs><linearGradient id="gold" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="#FDE68A"/><stop offset="1" stop-color="#E0A800"/></linearGradient></defs>{body}</svg></div>')


O = "linear-gradient(135deg,#FF7A3D,#FF5A1F)"
WH = ('<circle cx="42" cy="58" r="22" fill="url(#gold)"/><circle cx="42" cy="58" r="8" fill="#8A5A00"/>'
      '<rect x="52" y="40" width="36" height="16" rx="6" fill="url(#gold)" transform="rotate(-10 52 48)"/>'
      '<circle cx="38" cy="34" r="6" fill="none" stroke="#FBBF24" stroke-width="3"/>')
opts = [
    ("1 Man coach, orange", tile(O, man())),
    ("2 Woman coach, navy", tile("#151A30", woman())),
    ("3 Bull coach (market)", tile("#151A30", bull())),
    ("4 Bull coach, green", tile("linear-gradient(135deg,#065F46,#10B981)", bull())),
    ("5 Owl coach", tile("linear-gradient(135deg,#4338CA,#7C3AED)", owl())),
    ("6 Fox coach", tile("linear-gradient(135deg,#0F766E,#14B8A6)", fox())),
    ("7 Lumi bunny coach", tile(O, bunny_coach())),
    ("8 Man coach + coin", tile("#0B3D2E", '<circle cx="50" cy="50" r="40" fill="url(#gold)"/><g transform="translate(10 8) scale(.8)">' + man("#151A30") + "</g>")),
    ("9 Whistle + coin", tile("#151A30", WH)),
    ("10 Bear coach", tile("#FBBF24", bear())),
]
cells = "".join(f'<div class="c"><b>{n}</b>{t}<div class="s">{t}</div></div>' for n, t in opts)
html = ('<!doctype html><meta charset=utf-8><style>body{margin:0;background:#f4f4f5;font:700 15px sans-serif;width:1160px}'
        '.g{display:grid;grid-template-columns:repeat(5,1fr);gap:26px 18px;padding:22px}.t{border-radius:22%;overflow:hidden;width:190px;height:190px;display:grid;place-items:center}'
        '.t svg{width:100%;height:100%}.c b{display:block;margin-bottom:6px}.s{margin-top:8px}.s .t{width:48px;height:48px}</style>'
        f'<div class="g">{cells}</div>')
p = ROOT / "design/brand/out/options8.html"
p.write_text(html, encoding="utf-8")
b = Cdp()
try:
    b.size(1160, 640, 1)
    b.go(p.as_uri(), 2)
    b.shot("options8.png")
finally:
    b.close()
