# KANIMG.DAT dictionary text parse / build
import re, struct

def parse(d):
    cnt = struct.unpack_from('<H', d, 0)[0]
    p = 2; entries = []
    for k in range(cnt):
        if p >= len(d) or d[p] != 0x22: break
        assert d[p] == 0x22, (k, hex(p), d[p:p+16])
        e = d.index(b'"', p + 1)
        title = d[p+1:e]
        meta = d[e+1:e+8]           # 00 00 00 00 00 xx 00 ?
        q = e + 1
        # find body start: next '"'
        b0 = d.index(b'"', q)
        meta = d[e+1:b0]
        # body until '"\0\n'
        m = re.compile(rb'"(\x00[^"\n\r]{0,7})\n(?="[^"\n]{1,40}"\x00|\x00{16})').search(d, b0 + 1)
        b1 = m.start()
        body = d[b0+1:b1]
        entries.append({'title': title, 'meta': meta, 'body': body, 'tail': m.group(1)})
        p = m.end()
    return cnt, entries, p

def body_to_markup(body):
    """bytes -> str; links as {{id|word}}, line break as '\n'"""
    out = ''; i = 0
    while i < len(body):
        if body[i] == 0 and body[i+1:i+3] == b'\x06i':
            lid = struct.unpack_from('<H', body, i + 3)[0]
            j = body.index(b'\0', i + 5)
            out += '{{%d|%s}}' % (lid, body[i+5:j].decode('cp932'))
            i = j + 1
            continue
        if body[i:i+2] == b'\r\n': out += '\n'; i += 2; continue
        ch = body[i]
        if (0x81 <= ch <= 0x9f or 0xe0 <= ch <= 0xef):
            try: out += body[i:i+2].decode('cp932')
            except UnicodeDecodeError: out += '[[%s]]' % body[i:i+2].hex()
            i += 2
        else:
            out += chr(ch); i += 1
    return out

def markup_to_body(s, enc):
    out = b''; pos = 0
    for m in re.finditer(r'\{\{(\d+)\|([^}]*)\}\}', s):
        out += enc(s[pos:m.start()].replace('\n', '\r\n'))
        out += b'\x00\x06i' + struct.pack('<H', int(m.group(1))) + enc(m.group(2)) + b'\x00'
        pos = m.end()
    out += enc(s[pos:].replace('\n', '\r\n'))
    return out

if __name__ == '__main__':
    import json, sys
    d = open('work/orig/KANIMG.DAT', 'rb').read()
    cnt, es, end = parse(d)
    print(cnt, len(es), hex(end))
    out = []
    widths = []
    for i, e in enumerate(es):
        body = body_to_markup(e['body'])
        plain = re.sub(r'\{\{\d+\|([^}]*)\}\}', r'\1', body)
        widths += [len(l) for l in plain.split('\n')]
        out.append({'i': i, 'title': e['title'].decode('cp932'), 'meta': e['meta'].hex(), 'body': body})
    import collections
    print(sorted(collections.Counter(widths).items())[-8:])
    print(collections.Counter(o['meta'] for o in out).most_common(10))
    json.dump(out, open('work/dict_units.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(sum(len(o['body']) for o in out))
