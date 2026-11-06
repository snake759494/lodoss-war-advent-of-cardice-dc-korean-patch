# Lodoss DC texture codec: 32-byte header (u32 size, u8 pixfmt, u8 datafmt, u16 0, u16 w, u16 h, 4 pad, name[16]) + PVR data
import struct, re
import numpy as np
from PIL import Image

def scan(d):
    res = []
    for o in range(0, len(d) - 32, 4):
        pf, df, z, w, h = struct.unpack_from('<BBHHH', d, o + 4)
        if pf <= 6 and 1 <= df <= 0x12 and z == 0 and w in (8,16,32,64,128,256,512,1024) and h in (8,16,32,64,128,256,512,1024):
            nm = d[o+16:o+32]
            if re.match(rb'^[\x21-\x7e]{1,16}\x00*$', nm):
                res.append(dict(off=o, pf=pf, df=df, w=w, h=h, name=nm.rstrip(b'\0').decode()))
    return res

_tw = {}
def twiddle_map(n):
    """n x n: returns array idx[y, x] -> linear twiddled index"""
    if n in _tw: return _tw[n]
    a = np.arange(n)
    def spread(v):
        r = np.zeros_like(v)
        for b in range(12): r |= ((v >> b) & 1) << (2 * b)
        return r
    m = (spread(a)[:, None] << 1) | spread(a)[None, :]   # y bit -> odd? PVR: x bits odd, y bits even
    m = (spread(a)[None, :] << 1) | spread(a)[:, None]
    _tw[n] = m; return m

def cb_size(df, w):
    if df == 3: return 256
    if df == 0x10: return 16 if w <= 16 else 32 if w == 32 else 128 if w == 64 else 256
    if df == 0x11: return 16 if w <= 16 else 64 if w == 32 else 256
    raise ValueError(df)

def to_rgba(px, pf):
    px = px.astype(np.uint32)
    if pf == 0:
        a = np.where(px & 0x8000, 255, 0); r = (px >> 10 & 31) * 255 // 31; g = (px >> 5 & 31) * 255 // 31; b = (px & 31) * 255 // 31
    elif pf == 1:
        a = np.full_like(px, 255); r = (px >> 11 & 31) * 255 // 31; g = (px >> 5 & 63) * 255 // 63; b = (px & 31) * 255 // 31
    elif pf == 2:
        a = (px >> 12 & 15) * 17; r = (px >> 8 & 15) * 17; g = (px >> 4 & 15) * 17; b = (px & 15) * 17
    return np.stack([r, g, b, a], -1).astype(np.uint8)

def from_rgba(arr, pf):
    a = arr.astype(np.uint32); r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    if pf == 0: return (((al >= 128) << 15) | ((r * 31 + 127) // 255 << 10) | ((g * 31 + 127) // 255 << 5) | ((b * 31 + 127) // 255)).astype(np.uint16)
    if pf == 1: return (((r * 31 + 127) // 255 << 11) | ((g * 63 + 127) // 255 << 5) | ((b * 31 + 127) // 255)).astype(np.uint16)
    if pf == 2: return ((((al + 8) // 17) << 12) | (((r + 8) // 17) << 8) | (((g + 8) // 17) << 4) | ((b + 8) // 17)).astype(np.uint16)

def data_off(t):
    return t['off'] + 32

def decode(d, t):
    """returns (rgba array h x w x 4, raw16 array) for top mip level"""
    pf, df, w, h = t['pf'], t['df'], t['w'], t['h']; p = data_off(t)
    if df in (3, 0x10, 0x11, 4):
        n = cb_size(df if df != 4 else 3, w)
        cb = np.frombuffer(d, '<u2', n * 4, p).reshape(n, 4)
        p += n * 8
        if df in (4, 0x11):    # mipmaps: skip smaller levels (indices) - 1x1 level is 1 byte padded
            s = 1; q = 1
            while s < w // 2: q += s * s; s *= 2
            p += q
        m = twiddle_map(w // 2)
        idx = np.frombuffer(d, np.uint8, (w // 2) * (h // 2), p)[m]
        blk = cb[idx]           # (h/2, w/2, 4)  order: (0,0),(1,0)?,
        out = np.zeros((h, w), np.uint16)
        out[0::2, 0::2] = blk[..., 0]; out[1::2, 0::2] = blk[..., 1]; out[0::2, 1::2] = blk[..., 2]; out[1::2, 1::2] = blk[..., 3]
    elif df in (1, 2, 0xd):
        if df == 2:
            s = 1; q = 2           # 1x1 level padded to... (16-bit) PVR: 1 pixel(2 bytes) + ...
            q = 2
            s = 2
            while s < w: q += s * s * 2; s *= 2
            p += q
        n = min(w, h); m = twiddle_map(n)
        out = np.zeros((h, w), np.uint16)
        raw = np.frombuffer(d, '<u2', w * h, p)
        k = 0
        if w >= h:
            for bx in range(0, w, n): out[:, bx:bx+n] = raw[k:k+n*n][m]; k += n * n
        else:
            for by in range(0, h, n): out[by:by+n, :] = raw[k:k+n*n][m]; k += n * n
    elif df == 9:
        out = np.frombuffer(d, '<u2', w * h, p).reshape(h, w).copy()
    else:
        raise ValueError('df %x' % df)
    return to_rgba(out, pf), out

def png(d, t, fn):
    Image.fromarray(decode(d, t)[0], 'RGBA').save(fn)

# ---------------------------------------------------------------- encode (in place, same format)
def _kmeans(X, k, iters=12, seed=0, init=None):
    rng = np.random.default_rng(seed)
    if init is not None:
        C = init.astype(np.float32).copy()
        for _ in range(iters):
            lab = _assign(X, C)
            for j in range(k):
                s = X[lab == j]
                if len(s): C[j] = s.mean(0)
                else: C[j] = X[rng.integers(len(X))]
        return C
    uniq = np.unique(X, axis=0)
    if len(uniq) <= k:
        C = np.zeros((k, X.shape[1]), np.float32); C[:len(uniq)] = uniq
        return C
    C = uniq[rng.choice(len(uniq), k, replace=False)].astype(np.float32)
    for _ in range(iters):
        lab = _assign(X, C)
        for j in range(k):
            s = X[lab == j]
            if len(s): C[j] = s.mean(0)
            else: C[j] = X[rng.integers(len(X))]
    return C

def _assign(X, C):
    out = np.empty(len(X), np.int64)
    for i in range(0, len(X), 4096):
        x = X[i:i+4096]
        dd = (x * x).sum(1)[:, None] - 2 * x @ C.T + (C * C).sum(1)[None, :]
        out[i:i+4096] = dd.argmin(1)
    return out

def encode_into(d, t, rgba):
    """d: bytearray. rgba: h x w x 4 uint8. writes texture data in place (top level; mip levels regenerated)."""
    pf, df, w, h = t['pf'], t['df'], t['w'], t['h']; p = data_off(t)
    assert rgba.shape == (h, w, 4)
    if df in (3, 0x10):
        n = cb_size(df, w)
        px = from_rgba(rgba, pf)
        q = to_rgba(px, pf).astype(np.float32)      # quantized colour space
        # blocks: (h/2, w/2, 4 pixels, 4 ch) order matches decode
        bl = np.stack([q[0::2, 0::2], q[1::2, 0::2], q[0::2, 1::2], q[1::2, 1::2]], 2)
        X = bl.reshape(-1, 16)
        Xw = X.copy(); Xw[:, 3::4] *= 1.5
        cb0 = np.frombuffer(bytes(d[p:p + n * 8]), '<u2').reshape(n, 4)
        I = to_rgba(cb0, pf).astype(np.float32).reshape(n, 16); I[:, 3::4] *= 1.5
        C = _kmeans(Xw, n, 8, init=I)
        lab = _assign(Xw, C)
        C[:, 3::4] /= 1.5
        Cq = np.clip(np.rint(C), 0, 255).astype(np.uint8).reshape(n, 4, 4)
        cbw = from_rgba(Cq, pf)                      # n x 4
        d[p:p + n * 8] = cbw.astype('<u2').tobytes()
        idx = lab.reshape(h // 2, w // 2).astype(np.uint8)
        m = twiddle_map(w // 2)
        lin = np.zeros((w // 2) * (h // 2), np.uint8); lin[m.ravel()] = idx.ravel()
        d[p + n * 8:p + n * 8 + len(lin)] = lin.tobytes()
    elif df in (1, 0xd):
        px = from_rgba(rgba, pf); n = min(w, h); m = twiddle_map(n)
        raw = np.zeros(w * h, np.uint16); k = 0
        if w >= h:
            for bx in range(0, w, n): blk = np.zeros(n*n, np.uint16); blk[m.ravel()] = px[:, bx:bx+n].ravel(); raw[k:k+n*n] = blk; k += n*n
        else:
            for by in range(0, h, n): blk = np.zeros(n*n, np.uint16); blk[m.ravel()] = px[by:by+n].ravel(); raw[k:k+n*n] = blk; k += n*n
        d[p:p + w * h * 2] = raw.astype('<u2').tobytes()
    elif df == 9:
        d[p:p + w * h * 2] = from_rgba(rgba, pf).astype('<u2').tobytes()
    else:
        raise ValueError('encode df %x' % df)
