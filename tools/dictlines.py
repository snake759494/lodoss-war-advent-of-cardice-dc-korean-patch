# check dictionary bodies fit the in-game page: <= 8 lines of 23 cells (auto-wrapped)
# usage: python tools/dictlines.py [file.json ...]   (default: all work/tr/out/dict_*.json)
import re, json, glob, sys, os
DICT_WIDTH = 23
MAX_LINES = 8
src = open(os.path.join(os.path.dirname(__file__), 'build.py'), encoding='utf-8').read()
i = src.index('def wrap_dict'); j = src.index('# ----', i)
exec(src[i:j])

def lines(body):
    b = body.replace(' ', '　')
    if '\n『팔리스 신관전사단』 ' in b:   # d265 holds two entries
        return max(len(wrap_dict(x).split('\n')) for x in b.split('\n『팔리스 신관전사단』　'))
    return len(wrap_dict(b).split('\n'))

if __name__ == '__main__':
    files = sys.argv[1:] or glob.glob('work/tr/out/dict_*.json')
    bad = 0
    for p in files:
        for u in json.load(open(p, encoding='utf-8')):
            n = lines(u['body'])
            if n > MAX_LINES:
                bad += 1; print('%s %s: %d lines' % (os.path.basename(p), u['id'], n))
    print('OVER:', bad)
