"""python build.py <lang>  -> reads tr/<lang>.txt (key=value per line), validates against en.json, writes locales/<lang>.json"""
import json, re, sys, os

LOC = r'C:\Users\Admin\finlingo-version2\frontend\src\i18n\locales'
TR = r'C:\Users\Admin\AppData\Local\Temp\tr'
lang = sys.argv[1]
en = json.load(open(os.path.join(LOC, 'en.json'), encoding='utf8'))
flat_en = {f'{ns}.{k}': v for ns, d in en.items() if ns != 'explainerAdmin' for k, v in d.items()}

PLURAL = re.compile(r'^(.*)_(zero|one|two|few|many|other)$')
tr = {}
for i, line in enumerate(open(os.path.join(TR, f'{lang}.txt'), encoding='utf8').read().split('\n')):
    if not line.strip() or '=' not in line:
        continue
    k, v = line.split('=', 1)
    tr[k.strip()] = v

tokens = lambda s: sorted(re.findall(r'\{\{\s*\w+\s*\}\}|</?\w+>', s))
errors, missing = [], []
for k, src in flat_en.items():
    m = PLURAL.match(k)
    got = tr.get(k)
    if got is None:
        # a plural form that this language does not need can be absent; everything else must exist
        if m and any(x.startswith(m.group(1) + '_') for x in tr):
            continue
        missing.append(k)
        continue
    strip = (lambda t: [x for x in t if 'count' not in x]) if m else (lambda t: t)
    if strip(tokens(src)) != strip(tokens(got)):
        errors.append((k, tokens(src), tokens(got)))
extra_plural = [k for k in tr if k not in flat_en and not PLURAL.match(k)]
print(f'{lang}: {len(tr)} translated, missing {len(missing)}, token mismatches {len(errors)}, unknown keys {len(extra_plural)}')
for k in missing[:15]:
    print('  MISSING', k)
for k, a, b in errors[:15]:
    print('  MISMATCH', k, a, b)
for k in extra_plural[:10]:
    print('  UNKNOWN', k)
if missing or errors or extra_plural:
    sys.exit(1)

out = {}
base = json.load(open(os.path.join(LOC, 'en.json'), encoding='utf8'))
for k, v in tr.items():
    ns, key = k.split('.', 1)
    out.setdefault(ns, {})[key] = v
with open(os.path.join(LOC, f'{lang}.json'), 'w', encoding='utf8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
    f.write('\n')
print('written', lang)
