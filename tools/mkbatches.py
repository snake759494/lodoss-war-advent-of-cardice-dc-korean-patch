import json, os, re
os.makedirs('work/tr/in', exist_ok=True); os.makedirs('work/tr/out', exist_ok=True)
su = json.load(open('work/script_units.json', encoding='utf-8'))
tu = json.load(open('work/table_units.json', encoding='utf-8'))
du = json.load(open('work/dict_units.json', encoding='utf-8'))
def garbage(t):
    s = re.sub(r'@[A-Z]|%[0-9]*[sd]', '', t)
    if '単漢字変換' in t or re.match(r'^(.　){5}', t): return True
    return bool(re.search(r'[A-Za-z*$#<>;{}|]', s))
def dump(name, items):
    json.dump(items, open('work/tr/in/%s.json' % name, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
# script: 8 batches
items = [{'id': 's%04d' % i, 'kind': 'script', 'type': u['type'], 'jp': u['jp']} for i, u in enumerate(su)]
n = 8; per = (len(items) + n - 1) // n
for k in range(n): dump('script_%d' % k, items[k*per:(k+1)*per])
# table: unique texts
uniq = []; seen = set()
for u in tu:
    if u['jp'] in seen or garbage(u['jp']): continue
    seen.add(u['jp']); uniq.append(u['jp'])
items = [{'id': 't%04d' % i, 'kind': 'table', 'jp': t} for i, t in enumerate(uniq)]
n = 3; per = (len(items) + n - 1) // n
for k in range(n): dump('table_%d' % k, items[k*per:(k+1)*per])
items = [{'id': 'd%03d' % u['i'], 'kind': 'dict', 'title': u['title'], 'body': u['body']} for u in du]
n = 4; per = (len(items) + n - 1) // n
for k in range(n): dump('dict_%d' % k, items[k*per:(k+1)*per])
for f in sorted(os.listdir('work/tr/in')):
    print(f, len(json.load(open('work/tr/in/' + f, encoding='utf-8'))))
