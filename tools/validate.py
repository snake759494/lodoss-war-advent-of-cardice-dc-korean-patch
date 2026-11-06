# Validate translation output files.  usage: python tools/validate.py work/tr/out/<file>.json
import json, re, sys, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
KS = set(bytes([h, l]).decode('cp949') for h in range(0xB0, 0xC9) for l in range(0xA1, 0xFF))
CODE = re.compile(r'\\c0x[0-9a-f]+|\\[a-z0-9]|@[A-Z]|%[0-9]*[sdx]|\{\{\d+\||\}\}')

def codes(s): return CODE.findall(s)

def strip(s):
    s = re.sub(r'\\s.*?\\a', lambda m: m.group(0), s)
    return CODE.sub('', s)

def bad_chars(s):
    bad = []
    for ch in strip(s):
        if ch in ' \n': continue
        if '가' <= ch <= '힣':
            if ch not in KS: bad.append(ch)
            continue
        try: b = ch.encode('cp932')
        except UnicodeEncodeError: bad.append(ch); continue
        if len(b) == 1 and ch not in '\n': bad.append(ch)   # ASCII / halfwidth not allowed
    return bad

def width(s):
    return len(strip(s).replace('\n', ''))

def check(inp, out):
    errs = []
    src = {u['id']: u for u in inp}
    got = {u['id']: u for u in out}
    for i, u in src.items():
        if i not in got: errs.append((i, 'missing')); continue
        g = got[i]
        kind = u['kind']
        if kind == 'script':
            lim = 22 if u['type'] == 'choice' else 16
            if len(g['ko']) != len(u['jp']): errs.append((i, 'line count %d != %d' % (len(g['ko']), len(u['jp'])))); continue
            for a, b in zip(u['jp'], g['ko']):
                if codes(a) != codes(b): errs.append((i, 'codes differ: %r -> %r' % (a, b)))
                body = re.sub(r'\\s.*?(\\a|$)', '', b)
                if width(body) > lim and not re.search(r'\\s', b): errs.append((i, 'too wide (%d>%d): %r' % (width(body), lim, b)))
                bc = bad_chars(re.sub(r'\\s.*?(\\a|$)', '', b))
                if bc: errs.append((i, 'bad chars %r in %r' % (bc, b)))
        elif kind == 'table':
            a, b = u['jp'], g['ko']
            if codes(a) != codes(b): errs.append((i, 'codes differ'))
            la, lb = a.split('\n'), b.split('\n')
            if len(la) != len(lb): errs.append((i, 'line count %d != %d' % (len(lb), len(la))))
            else:
                for x, y in zip(la, lb):
                    lim = max(len(strip(x)), 3)
                    if width(y) > lim: errs.append((i, 'too wide (%d>%d): %r' % (width(y), lim, y)))
            bc = bad_chars(b)
            if bc: errs.append((i, 'bad chars %r' % bc))
        elif kind == 'dict':
            if width(g['title']) > 12: errs.append((i, 'title too wide'))
            ia = sorted(re.findall(r'\{\{(\d+)\|', u['body'])); ib = sorted(re.findall(r'\{\{(\d+)\|', g['body']))
            if ia != ib: errs.append((i, 'link ids differ %s vs %s' % (ia, ib)))
            bc = bad_chars(g['body'] + g['title'])
            if bc: errs.append((i, 'bad chars %r' % bc))
    return errs

if __name__ == '__main__':
    fn = sys.argv[1]
    out = json.load(open(fn, encoding='utf-8'))
    inp = json.load(open(fn.replace(os.sep + 'out' + os.sep, os.sep + 'in' + os.sep).replace('/out/', '/in/'), encoding='utf-8'))
    errs = check(inp, out)
    for e in errs: print(e)
    print('ERRORS:', len(errs))
