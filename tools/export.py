# Export translation units from 1NOSDC.BIN
import json, re, sys, os, struct
d = open('work/orig/1NOSDC.BIN', 'rb').read()
c = json.load(open('work/cand.json', encoding='utf-8'))
HW = d[0x104654:0x104654 + 63 * 2]
HWMAP = {0xA1 + i: HW[i*2:i*2+2].decode('cp932') for i in range(63)}

def display(off):
    """decode string at off to display form (halfwidth kana -> table glyph)"""
    end = d.find(b'\0', off); b = d[off:end]; out = ''; i = 0
    while i < len(b):
        ch = b[i]
        if 0xA1 <= ch <= 0xDF: out += HWMAP[ch]; i += 1
        elif (0x81 <= ch <= 0x9f or 0xe0 <= ch <= 0xef): out += b[i:i+2].decode('cp932'); i += 2
        else: out += chr(ch); i += 1
    return out

# ---------- script ----------
refs = []  # (refpos, op, off)
for x in c['S']:
    for r in x['refs']:
        op = d[r-1]
        if op in (0x0f, 0x5e): refs.append((r, op, x['off']))
refs.sort()
msgs = []; cur = []
for r, op, off in refs:
    if op == 0x5e:
        if cur: msgs.append({'type': 'msg', 'lines': cur}); cur = []
        msgs.append({'type': 'choice', 'lines': [off]})
        continue
    cur.append(off)
    if not display(off).endswith('\\n'):
        msgs.append({'type': 'msg', 'lines': cur}); cur = []
if cur: msgs.append({'type': 'msg', 'lines': cur})
# merge consecutive choices into one unit
units = []
for m in msgs:
    if m['type'] == 'choice' and units and units[-1]['type'] == 'choice' and len(units[-1]['lines']) < 8:
        units[-1]['lines'] += m['lines']
    else: units.append(m)
seen = set(); out = []
for u in units:
    key = tuple(display(o) for o in u['lines'])
    if key in seen: continue
    seen.add(key)
    out.append({'type': u['type'], 'jp': list(key)})
print('script units', len(out), 'lines', sum(len(u['jp']) for u in out))
json.dump(out, open('work/script_units.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ---------- table strings (items/menus) ----------
T = [x for x in c['T'] if 0xd0000 <= x['off'] < 0xe9000 or 0x129000 <= x['off'] < 0x13b000]
tu = []
for x in T:
    t = display(x['off'])
    if not re.search('[ぁ-んァ-ヶ一-龥]', t): continue
    tu.append({'off': x['off'], 'jp': t})
print('table strings', len(tu), len(set(u['jp'] for u in tu)))
json.dump(tu, open('work/table_units.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
