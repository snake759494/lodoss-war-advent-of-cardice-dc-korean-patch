# Lodoss War: Advent of Cardice (DC) Korean patch builder
import json, os, re, sys, struct, collections, glob
sys.path.insert(0, os.path.dirname(__file__))
import kfont, dictfmt
from PIL import ImageFont

ROOT = kfont.ROOT
O = os.path.join(ROOT, 'work', 'orig')
TR = os.path.join(ROOT, 'work', 'tr', 'out')
BASE = 0x8c010000
HWTAB = 0x104654
ONEBYTE_CODES = list(range(0xA1, 0xDE))      # 61 codes (skip DE/DF dakuten)
FONT_TTF = os.path.join(ROOT, 'NanumSquareNeo-dEb.ttf'); FONT_SIZE = 19
DICT_WIDTH = 23
LOG = []

def log(*a):
    s = ' '.join(str(x) for x in a); LOG.append(s); print(s)

# ---------------------------------------------------------------- load
exe0 = open(os.path.join(O, '1NOSDC.BIN'), 'rb').read()
font0 = open(os.path.join(O, 'DATANOS.BIN'), 'rb').read()
kan0 = open(os.path.join(O, 'KANIMG.DAT'), 'rb').read()
cand = json.load(open(os.path.join(ROOT, 'work', 'cand.json'), encoding='utf-8'))
# one-kanji equipment slot names missed by the string scanner (pointer table at 0x130458)
SLOTNAMES = {0xdb5b8: ('胸', '목', 0x130464), 0xdb610: ('腰', '허리', 0x13047c), 0xdb62c: ('頭', '머리', 0x130484),
             0xdb644: ('耳', '귀', 0x13048c), 0xdb6cc: ('足', '발', 0x1304ac)}
for _o, (_j, _k, _r) in SLOTNAMES.items():
    cand['T'].append({'off': _o, 'len': 2, 'refs': [_r]})

def load_out(prefix):
    res = {}
    for fn in sorted(glob.glob(os.path.join(TR, prefix + '_*.json'))):
        for u in json.load(open(fn, encoding='utf-8')): res[u['id']] = u
    return res

def load_in(prefix):
    res = {}
    for fn in sorted(glob.glob(os.path.join(ROOT, 'work', 'tr', 'in', prefix + '_*.json'))):
        for u in json.load(open(fn, encoding='utf-8')): res[u['id']] = u
    return res

HW = exe0[HWTAB:HWTAB + 63 * 2]
HWMAP = {0xA1 + i: HW[i*2:i*2+2].decode('cp932') for i in range(63)}
def display(off):
    end = exe0.find(b'\0', off); b = exe0[off:end]; out = ''; i = 0
    while i < len(b):
        ch = b[i]
        if 0xA1 <= ch <= 0xDF: out += HWMAP[ch]; i += 1
        elif 0x81 <= ch <= 0x9f or 0xe0 <= ch <= 0xef: out += b[i:i+2].decode('cp932'); i += 2
        else: out += chr(ch); i += 1
    return out

# ---------------------------------------------------------------- collect exe strings -> korean
def norm_ko(s):
    return s.replace(' ', '　')

script_in, script_out = load_in('script'), load_out('script')
unit_by_key = {}
for i, u in script_in.items():
    if i in script_out: unit_by_key[tuple(u['jp'])] = script_out[i]['ko']

# rebuild message grouping identically to export.py
refs = []
for x in cand['S']:
    for r in x['refs']:
        if exe0[r-1] in (0x0f, 0x5e): refs.append((r, exe0[r-1], x['off']))
refs.sort()
msgs = []; cur = []
for r, op, off in refs:
    if op == 0x5e:
        if cur: msgs.append(('msg', cur)); cur = []
        msgs.append(('choice', [off])); continue
    cur.append(off)
    if not display(off).endswith('\\n'): msgs.append(('msg', cur)); cur = []
if cur: msgs.append(('msg', cur))
units = []
for t, lines in msgs:
    if t == 'choice' and units and units[-1][0] == 'choice' and len(units[-1][1]) < 8: units[-1][1].extend(lines)
    else: units.append((t, list(lines)))
trans = {}       # offset -> korean string
for t, lines in units:
    key = tuple(display(o) for o in lines)
    ko = unit_by_key.get(key)
    if ko is None: continue
    for o, k in zip(lines, ko):
        trans.setdefault(o, norm_ko(k))

table_in, table_out = load_in('table'), load_out('table')
tmap = {u['jp']: norm_ko(table_out[i]['ko']) for i, u in table_in.items() if i in table_out}
T = [x for x in cand['T'] if 0xd0000 <= x['off'] < 0xe9000 or 0x129000 <= x['off'] < 0x13b000]
for x in T:
    j = display(x['off'])
    if j in tmap: trans.setdefault(x['off'], tmap[j])
# float data misdetected as text (0.1f x3, used when equipping weapons) - never touch
for _o in (0xd8b80,): trans.pop(_o, None)
for _r in filter(None, os.environ.get('SKIP', '').split(';')):
    _a, _b = (int(v, 16) for v in _r.split('-'))
    for _o in [o for o in trans if _a <= o < _b]: del trans[_o]

# ---------------------------------------------------------------- name-entry grid: kana -> hangul syllables
def _syl(c, v, f=0):
    return chr(0xAC00 + (c * 21 + v) * 28 + f)
_C = dict(zip('ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ', range(19)))
_V = dict(zip('ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ', range(21)))
def _cols(cons, vows):
    return [[_syl(_C[c], _V[v]) for v in vows] for c in cons]
_P1 = _cols('ㄱㄴㄷㄹㅁㅂㅅㅋㅇㅈ', 'ㅏㅓㅗㅜㅣ')
_P2 = _cols('ㅊㅌㅍㅎ', 'ㅏㅓㅗㅜㅣ') + _cols('ㄱㄴㅁㄹㅅㅇ', 'ㅐㅔㅕㅡㅠ')
_R6 = ['한진민훈영준성현윤', '김정박철용석원혁은']
GRID = {}
for _pg, (_base, _cols_) in enumerate(((0xe5b2c, _P1), (0xe5c64, _P2))):
    for _r in range(6):
        _o = _base + _r * 0x34
        _s = display(_o); _body = _s.rstrip('\n'); _tail = _s[len(_body):]
        _cells = list(_body[0::2])          # cell k at char index 2k, separators are fullwidth spaces
        for _c in range(10 if _r < 5 else 9):
            if _cells[_c] == '　': continue
            _cells[_c] = _cols_[_c][_r] if _r < 5 else _R6[_pg][_c]
        GRID[_o] = '　'.join(_cells) + _tail
trans.update(GRID)
for _o, (_j, _k, _r) in SLOTNAMES.items(): trans[_o] = _k
log('exe strings translated:', len(trans))

# ---------------------------------------------------------------- dictionary
dict_in, dict_out = load_in('dict'), load_out('dict')
# entries were exported as 380 (d265 merged ファリス + ファリス神官戦士団); real file has 381
_d = {}
for _k, _v in dict_out.items():
    _i = int(_k[1:])
    if _i == 265:
        _p1, _p2 = _v['body'].split('\n『팔리스 신관전사단』 ', 1)
        _d['d265'] = {'title': _v['title'], 'body': _p1}
        _d['d266'] = {'title': '팔리스 신관전사단', 'body': _p2}
    else:
        _d['d%03d' % (_i + 1 if _i > 265 else _i)] = _v
dict_out = _d

def wrap_dict(body):
    """auto-wrap markup body to DICT_WIDTH cells; links unbreakable."""
    paras = body.replace('\r', '').split('\n')
    out_lines = []
    for p in paras:
        toks = re.findall(r'\{\{\d+\|[^}]*\}\}|[^\s{]+|\s+|\{', p)
        line = ''; w = 0
        def tw(t):
            m = re.match(r'\{\{\d+\|([^}]*)\}\}', t)
            return len(m.group(1)) if m else len(t)
        # split into words (spaces separate)
        words = re.findall(r'(?:\{\{\d+\|[^}]*\}\}|[^ 　{])+|\{', p)
        for wd in words:
            # break overly long words into link/char pieces
            pieces = re.findall(r'\{\{\d+\|[^}]*\}\}|.', wd)
            wlen = sum(tw(x) for x in pieces)
            if w and w + 1 + wlen <= DICT_WIDTH:
                line += '　' + wd; w += 1 + wlen
            elif not w and wlen <= DICT_WIDTH:
                line = wd; w = wlen
            else:
                if w: out_lines.append(line); line = ''; w = 0
                for pc in pieces:
                    pl = tw(pc)
                    if w + pl > DICT_WIDTH: out_lines.append(line); line = ''; w = 0
                    line += pc; w += pl
        out_lines.append(line)
    return '\n'.join(out_lines)

# ---------------------------------------------------------------- char frequency / 1-byte set
def all_ko_texts():
    for o, v in trans.items():
        if not (0xd0000 <= o < 0xe9000): yield v     # 1-byte codes only in script text
freq = collections.Counter()
CODE_RE = re.compile(r'\\s.*?\\a|\\c0x[0-9a-f]+|\\[a-z0-9]|@[A-Z]|%[0-9]*[sdx]|\{\{\d+\||\}\}|\[\[[0-9a-f]+\]\]')
for t in all_ko_texts():
    for ch in CODE_RE.sub('', t):
        if ch == '\n': continue
        freq[ch] += 1
cands = [c for c, n in freq.most_common() if c == '　' or ('가' <= c <= '힣')]
ONE = {c: ONEBYTE_CODES[i] for i, c in enumerate(cands[:len(ONEBYTE_CODES)])}
log('1-byte chars:', ''.join(ONE))

missing = set()
def enc(s, allow1=True):
    out = bytearray(); i = 0
    while i < len(s):
        m = CODE_RE.match(s, i)
        if m and m.start() == i and not m.group(0).startswith('{{') and m.group(0) != '}}':
            g = m.group(0)
            if g.startswith('\\s'):   # spell section: encode inner part normally (fullwidth latin)
                out += b'\\s' + enc(g[2:-2], allow1) + b'\\a'
            elif g.startswith('[['): out += bytes.fromhex(g[2:-2])
            else: out += g.encode('ascii')
            i = m.end(); continue
        ch = s[i]; i += 1
        if allow1 and ch in ONE: out.append(ONE[ch]); continue
        if ch in kfont.SLOTS: out += kfont.SLOTS[ch].to_bytes(2, 'big'); continue
        if ch == '\n': out += b'\n'; continue
        try:
            b = ch.encode('cp932')
        except UnicodeEncodeError:
            missing.add(ch); b = '？'.encode('cp932')
        if len(b) == 1 and ch not in '\r':
            missing.add(ch)
        out += b
    return bytes(out)

# ---------------------------------------------------------------- exe allocation
exe = bytearray(exe0)
# string ranges (orig)
allstr = {x['off']: x for x in cand['S'] + T}
ranges = sorted((o, o + allstr[o]['len'] + 1) for o in trans)
offs_sorted = sorted(allstr)
# detect overlapping / nested strings (substring refs) -> do not move
inner = set()
starts = sorted(o for o in allstr)
for o in trans:
    e = o + allstr[o]['len']
    for s2 in starts:
        if o < s2 <= e and s2 != o: inner.add(o); inner.add(s2)
log('overlapping strings (kept in place only):', len(inner))

def slot_end(o):
    e = o + allstr[o]['len'] + 1
    a = (e + 3) & ~3
    if a != e and a in allstr and all(b == 0 for b in exe0[e:a]): return a
    return e

def ref_list(o):
    x = allstr[o]; good = []
    for r in x['refs']:
        if r % 4 == 0 and r < 0x13a000: good.append(r)           # aligned data/literal pool
        elif exe0[r-1] in (0x0f, 0x5e, 0x05, 0x40, 0x5f, 0x03, 0x01, 0x3f, 0x3e): good.append(r)
        else: log('  skip ref %x -> %x (op %02x)' % (r, o, exe0[r-1]))
    return good

NO1 = {0x13a8d9, 0x13a8e4, 0x13a8ed, 0x13a8f6, 0x13a8ff}   # default hero / magic sword, shield, armour, helm names: name-entry fields expect 2-byte SJIS
encoded = {o: enc(t, o not in NO1 and not (0xd0000 <= o < 0xe9000)) for o, t in trans.items()}
inplace = {}; move = {}
for o, b in encoded.items():
    cap = slot_end(o) - o
    if len(b) + 1 <= cap: inplace[o] = b
    elif o in inner:
        log('  OVERFLOW nested string %x %r' % (o, trans[o])); inplace[o] = b[:cap-1]
    else: move[o] = b
# free space: tails of in-place slots + whole slots of moved strings
free = []
for o, b in inplace.items():
    e = slot_end(o); s = o + len(b) + 1
    if e - s >= 4: free.append([s, e])
for o in move: free.append([o, slot_end(o)])
free.sort(); _m = []
for fr in free:
    if _m and fr[0] <= _m[-1][1]: _m[-1][1] = max(_m[-1][1], fr[1])
    else: _m.append(list(fr))
free = _m
need = sum(len(b) + 1 for b in move.values()); have = sum(e - s for s, e in free)
[log('  MOVED %x %d->%d %r' % (o, allstr[o]['len'], len(b), trans[o])) for o, b in move.items() if 0xd0000 <= o < 0xe9000]
log('in place: %d, to move: %d (%d bytes), free pool %d bytes' % (len(inplace), len(move), need, have))
# write in-place
for o, b in inplace.items():
    e = slot_end(o); exe[o:e] = b + bytes(e - o - len(b))
for o in move:
    e = slot_end(o); exe[o:e] = bytes(e - o)
# best-fit decreasing
free.sort(key=lambda x: x[1] - x[0])
unplaced = []
pool_strs = [(o2, b2) for o2, b2 in inplace.items()]
shared = 0
for o, b in sorted(move.items(), key=lambda kv: -len(kv[1])):
    n = len(b) + 1
    hit = next((o2 + len(b2) - len(b) for o2, b2 in pool_strs if b2.endswith(b)), None)
    if hit is not None:
        for r in ref_list(o): struct.pack_into('<I', exe, r, BASE + hit)
        shared += 1; continue
    for fr in free:
        if fr[1] - fr[0] >= n:
            pos = fr[0]; fr[0] += n
            exe[pos:pos + n] = b + b'\0'
            for r in ref_list(o): struct.pack_into('<I', exe, r, BASE + pos)
            pool_strs.append((pos, b))
            break
    else:
        unplaced.append(o); log('  unplaced %x len %d free-max %d %r' % (o, n, max(f[1]-f[0] for f in free), trans[o]))
    free.sort(key=lambda x: x[1] - x[0])
log('shared (dedup/suffix):', shared)
if unplaced:
    log('UNPLACED: %d strings, %d bytes' % (len(unplaced), sum(len(move[o]) + 1 for o in unplaced)))
    # fallback: keep original japanese (restore) -> they'd be garbled; store truncated placeholder
    for o in unplaced:
        cap = slot_end(o) - o
        exe[o:o + cap] = exe0[o:o + cap]

# dictionary category tabs: fixed 6-byte slots without pointers (2 chars + NULs)
FIXED = {'総覧': '총람', '人物': '인물', '地理': '지리', '生物': '생물', '物品': '물품'}
for _o in range(0x129794, 0x1297d4, 6):
    _j = exe0[_o:_o + 4].decode('cp932', 'replace')
    if _j in FIXED: exe[_o:_o + 4] = enc(FIXED[_j], False)

# 1-byte table
for ch, code in ONE.items():
    if ch == '　': sj = 0x8140
    else: sj = kfont.SLOTS[ch]
    struct.pack_into('>H', exe, HWTAB + (code - 0xA1) * 2, sj)

# ---------------------------------------------------------------- dictionary rebuild
cnt, entries, endp = dictfmt.parse(kan0)
dbody = bytearray(kan0[:2])
for k, e in enumerate(entries):
    u = dict_out.get('d%03d' % k)
    if os.environ.get('NODICT') and k >= int(os.environ['NODICT']): u = None
    if u is None:
        title, body = e['title'], e['body']
    else:
        _d1 = False   # dictionary renderer can't take 1-byte codes
        title = enc(norm_ko(u['title']), _d1)
        mk = wrap_dict(norm_ko(u['body']))
        mk = re.sub(r'\{\{(\d+)\|', lambda m: '{{%d|' % (int(m.group(1)) & 0x7fff), mk)
        _de = (lambda x: b' '.join(enc(t, False) for t in x.split('　'))) if False else (lambda x: enc(x, _d1))
        body = dictfmt.markup_to_body(mk, _de)
    dbody += b'"' + title + b'"' + e['meta'] + b'"' + body + b'"' + e['tail'] + b'\n'
log('dictionary text %d bytes (orig %d, max %d)' % (len(dbody), endp, 0x1e800))
assert len(dbody) <= 0x1e800
kan = bytearray(kan0)
kan[:0x1e800] = bytes(dbody) + bytes(0x1e800 - len(dbody))
assert struct.unpack_from('<I', exe0, 0xe74c4)[0] == 0x0201e701
struct.pack_into('<I', exe, 0xe74c4, 0x02000000 | len(dbody))

# ---------------------------------------------------------------- font
font = bytearray(font0)
ttf = ImageFont.truetype(FONT_TTF, FONT_SIZE)
for ch, code in kfont.SLOTS.items():
    idx = kfont.sjis_to_jis_index(code)
    p = kfont.KANJI_BASE + idx * 100
    font[p:p + 100] = kfont.pack(kfont.levels(kfont.render_glyph(ch, ttf)))

if missing: log('MISSING chars:', ''.join(sorted(missing)))

# ---------------------------------------------------------------- textures (title, menus, area names)
import texpatch, texspec
TEXOUT = {}
if not os.environ.get('NOTEX'):
    for _f, _sp in texspec.SPECS.items():
        _d = bytearray(open(os.path.join(O, _f), 'rb').read())
        log('texture file', _f)
        texpatch.patch_file(_d, _sp, log=log)
        TEXOUT[_f] = _d

# ---------------------------------------------------------------- output
os.makedirs(os.path.join(ROOT, 'work', 'build'), exist_ok=True)
for name, data in (('1NOSDC.BIN', exe), ('DATANOS.BIN', font), ('KANIMG.DAT', kan)):
    open(os.path.join(ROOT, 'work', 'build', name), 'wb').write(data)
json.dump({'one': ONE}, open(os.path.join(ROOT, 'work', 'build', 'map.json'), 'w', encoding='utf-8'), ensure_ascii=False)
if '--disc' in sys.argv:
    import disc
    disc.fresh_copy(); d = disc.OutDisc()
    for name, data in [('1NOSDC.BIN', exe), ('DATANOS.BIN', font), ('KANIMG.DAT', kan)] + list(TEXOUT.items()):
        d.put(name, bytes(data))
    disc.write_cue()
    log('disc written')
open(os.path.join(ROOT, 'work', 'build', 'build.log'), 'w', encoding='utf-8').write('\n'.join(LOG))
