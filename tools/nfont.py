import numpy as np
FONT_OFF = 0x80a0
def morton(x, y):
    r = 0
    for i in range(8):
        r |= ((y >> i) & 1) << (2 * i) | ((x >> i) & 1) << (2 * i + 1)
    return r
M16 = np.array([[morton(x, y) for x in range(16)] for y in range(16)])
def decode_glyph(b):  # 128 bytes -> 16x16 indices
    a = np.frombuffer(b, np.uint8)
    nib = np.stack([a & 15, a >> 4], -1).reshape(-1)
    return nib[M16]
def encode_glyph(px):
    nib = np.zeros(256, np.uint8); nib[M16] = px
    nib = nib.reshape(-1, 2); return (nib[:, 0] | (nib[:, 1] << 4)).astype(np.uint8).tobytes()
def load(raw):
    d = raw[FONT_OFF:]; n = len(d) // 128
    return [decode_glyph(d[i*128:(i+1)*128]) for i in range(n)]
def sheet(gl, start, cnt, fn, per=64, scale=2):
    from PIL import Image
    s = np.array(gl[start:start+cnt]); rows = (len(s) + per - 1) // per
    s = np.pad(s, ((0, rows*per - len(s)), (0, 0), (0, 0)))
    img = s.reshape(rows, per, 16, 16).transpose(0, 2, 1, 3).reshape(rows*16, per*16)
    pal = np.array([0, 90, 140, 255, 200, 220] + [255]*10, np.uint8)
    Image.fromarray(pal[img]).resize((per*16*scale, rows*16*scale), 0).save(fn)
if __name__ == '__main__':
    import sys
    gl = load(open(sys.argv[1], 'rb').read()); print(len(gl))
    sheet(gl, int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
