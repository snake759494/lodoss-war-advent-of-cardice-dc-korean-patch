# Find pointer-referenced SJIS strings in 1NOSDC.BIN
import struct, re, json, sys
BASE = 0x8c010000
def valid_text(b):
    if not b: return False
    i = 0; jp = 0
    while i < len(b):
        c = b[i]
        if c in (0x0a, 0x09): i += 1; continue
        if 0x20 <= c < 0x7f: i += 1; continue
        if 0xa1 <= c <= 0xdf: jp += 1; i += 1; continue
        if (0x81 <= c <= 0x9f or 0xe0 <= c <= 0xef) and i + 1 < len(b) and 0x40 <= b[i+1] <= 0xfc and b[i+1] != 0x7f:
            jp += 1; i += 2; continue
        return False
    return jp > 0
def scan(d):
    ptrs = {}
    for i in range(0, len(d) - 3):
        v = struct.unpack_from('<I', d, i)[0]
        if BASE <= v < BASE + len(d):
            ptrs.setdefault(v - BASE, []).append(i)
    out = []
    for off, refs in ptrs.items():
        if off > 0 and d[off-1] != 0 and not (off >= 1 and d[off-1] == 0): pass
        end = d.find(b'\0', off)
        if end < 0 or end - off > 2000: continue
        b = d[off:end]
        if valid_text(b):
            out.append({'off': off, 'len': len(b), 'refs': refs, 'jp': b.decode('cp932', 'replace')})
    out.sort(key=lambda x: x['off'])
    return out
if __name__ == '__main__':
    d = open(sys.argv[1], 'rb').read(); r = scan(d)
    json.dump(r, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(len(r), sum(x['len'] for x in r))
    al = sum(1 for x in r if all(p % 4 == 0 for p in x['refs']))
    print('aligned-only', al)
