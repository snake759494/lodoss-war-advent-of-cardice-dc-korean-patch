# Render Korean text into game textures (erase original lettering, redraw with sampled colours)
import os, sys, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(__file__))
import tex
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FONTS = {
    'serif': 'SeoulHangangEB.ttf', 'serifb': 'SeoulHangangB.ttf', 'serifm': 'SeoulHangangM.ttf',
    'sans': 'NanumSquareNeo-dEb.ttf', 'sansh': 'NanumSquareNeo-eHv.ttf', 'sansb': 'NanumSquareNeo-cBd.ttf',
    'sansr': 'NanumSquareNeo-bRg.ttf',
    'g11b': 'work/fonts/Galmuri11-Bold.ttf', 'g11': 'work/fonts/Galmuri11.ttf', 'g14': 'work/fonts/Galmuri14.ttf', 'g9': 'work/fonts/Galmuri9.ttf',
}
SS = 4   # supersampling

def font(kind, px):
    return ImageFont.truetype(os.path.join(ROOT, FONTS[kind]), px)

def glyph_mask(img, box, opaque):
    x0, y0, x1, y1 = box; r = img[y0:y1, x0:x1].astype(np.int32)
    if not opaque: return r[..., 3] > 60
    lum = r[..., :3].sum(2)
    bgl = np.median(lum)
    return np.abs(lum - bgl) > 150

def sample_style(img, box, opaque):
    x0, y0, x1, y1 = box
    m = glyph_mask(img, box, opaque); r = img[y0:y1, x0:x1].astype(np.float32)
    if m.sum() < 4: return None
    lum = r[..., :3].sum(2)
    bright = m & (lum >= np.percentile(lum[m], 75))
    dark = m & (lum < 150)
    rows = []
    for yy in range(y1 - y0):
        s = bright[yy]
        rows.append(r[yy][s][:, :3].mean(0) if s.any() else None)
    ys = [i for i, v in enumerate(rows) if v is not None]
    top, bot = min(ys), max(ys)
    grad = np.array([rows[i] for i in ys]); pos = (np.array(ys) - top) / max(1, bot - top)
    outline = dark.sum() > 0.18 * m.sum()
    lo = m & (lum <= np.percentile(lum[m], 25))
    ocol = r[lo][:, :3].mean(0) if lo.any() else np.zeros(3)
    return dict(grad=(pos, grad), outline=outline, top=top, bot=bot, ocol=ocol)

def erase(img, box, opaque, pad=1, full=False):
    x0, y0, x1, y1 = box
    if not opaque:
        img[y0:y1, x0:x1] = 0; return
    lum = img[..., :3].astype(np.float32).mean(2)
    med = cv2.medianBlur(np.clip(lum, 0, 255).astype(np.uint8), 15).astype(np.float32)
    gm = (np.abs(lum - med) > 28).astype(np.uint8)
    gm = cv2.dilate(gm, np.ones((3, 3), np.uint8))
    if full:   # row-wise resample of background pixels
        gm = cv2.dilate(gm, np.ones((3, 3), np.uint8))
        rng = np.random.default_rng(x0 * 7 + y0)
        for y in range(y0, y1):
            row = img[y, x0:x1]; mk = gm[y, x0:x1].astype(bool)
            ok = row[~mk]
            if len(ok) < 3:
                ok = img[y, max(0, x0 - 6):x0]
                if len(ok) == 0: continue
            # use the darker half of background (avoid frame highlights)
            l = ok[:, :3].astype(int).sum(1); lo_, hi_ = np.percentile(l, [20, 70]); ok = ok[(l >= lo_) & (l <= hi_)] if ((l >= lo_) & (l <= hi_)).any() else ok
            row[mk] = ok[rng.integers(0, len(ok), mk.sum())]
        return
    m = np.zeros(img.shape[:2], np.uint8)
    m[y0:y1, x0:x1] = gm[y0:y1, x0:x1]
    rgb = np.ascontiguousarray(img[..., :3])
    out = cv2.inpaint(rgb, m, 4, cv2.INPAINT_TELEA)
    img[..., :3] = out

def erase_mask(img, box, mk):
    """replace pixels where mk (full-image bool) inside box by random non-masked pixels of the same row"""
    x0, y0, x1, y1 = box
    rng = np.random.default_rng(x0 * 7 + y0)
    for y in range(y0, y1):
        row = img[y, x0:x1]; m = mk[y, x0:x1]
        if not m.any(): continue
        ok = row[~m]
        if len(ok) == 0: row[m] = 0; continue
        row[m] = ok[rng.integers(0, len(ok), m.sum())]

def draw(img, box, text, kind='serif', style=None, align='l', size=None, outline=None, color=None, shadow=False, vpad=0, spacing=0, olw=1, ocol=None):
    global SS
    pix = kind.startswith('g'); SS = 1 if pix else 4
    x0, y0, x1, y1 = box; W, H = (x1 - x0) * SS, (y1 - y0) * SS
    hpx = size or (y1 - y0 - 2 * vpad)
    px = int(hpx * SS * 1.12) if not pix else {'g11b': 12, 'g11': 12, 'g14': 15, 'g9': 10}[kind] * (size or 1) if size and size < 4 else {'g11b': 12, 'g11': 12, 'g14': 15, 'g9': 10}[kind]
    ol = outline if outline is not None else (style['outline'] if style else False)
    stw = SS if ol else 0
    while True:
        f = font(kind, px)
        bb = f.getbbox(text, stroke_width=stw)
        tw = bb[2] - bb[0] + spacing * SS * (len(text) - 1); th = bb[3] - bb[1]
        if (tw <= W and th <= H) or px < 6 * SS or pix: break
        px -= 1
    layer = Image.new('L', (W, H), 0)
    if align == 'l': ox = -bb[0]
    elif align == 'r': ox = W - tw - bb[0]
    else: ox = (W - tw) // 2 - bb[0]
    oy = (H - th) // 2 - bb[1]
    def put(dr, fill, sw):
        if spacing:
            x = ox
            for ch in text:
                dr.text((x, oy), ch, font=f, fill=fill, stroke_width=sw, stroke_fill=fill)
                x += f.getbbox(ch)[2] - f.getbbox(ch)[0] + spacing * SS + (f.getlength(ch) - (f.getbbox(ch)[2] - f.getbbox(ch)[0]))
        else:
            dr.text((ox, oy), text, font=f, fill=fill, stroke_width=sw, stroke_fill=fill)
    fill_m = Image.new('L', (W, H), 0); put(ImageDraw.Draw(fill_m), 255, 0)
    full_m = Image.new('L', (W, H), 0); put(ImageDraw.Draw(full_m), 255, stw)
    # colour gradient over text height
    fm = np.array(fill_m); ys = np.where(fm.any(1))[0]
    t0, t1 = (ys.min(), ys.max()) if len(ys) else (0, H)
    col = np.zeros((H, W, 3), np.float32)
    if color is not None:
        col[:] = color
    else:
        pos, grad = style['grad']
        yy = np.clip((np.arange(H) - t0) / max(1, t1 - t0), 0, 1)
        for c in range(3): col[:, :, c] = np.interp(yy, pos, grad[:, c])[:, None]
    fa = fm.astype(np.float32) / 255
    small = lambda z: cv2.resize(z, (x1 - x0, y1 - y0), interpolation=cv2.INTER_AREA)
    rgb_s = small(col * fa[..., None]); fa_s = small(fa)
    colr = rgb_s / np.maximum(fa_s[..., None], 1e-4)
    dst = img[y0:y1, x0:x1].astype(np.float32)
    binary = BINARY[0]
    if binary or pix:
        tm = (fa_s > 0.5).astype(np.float32)
    else:
        tm = np.clip(fa_s * 1.25, 0, 1)
    if ol:
        om = cv2.dilate(tm, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * olw + 1, 2 * olw + 1)))
    else:
        om = tm
    if shadow:
        sh = np.zeros_like(om); sh[1:, 1:] = om[:-1, :-1]
        if shadow == 2: sh2 = np.zeros_like(om); sh2[2:, 2:] = om[:-2, :-2]; sh = np.maximum(sh, sh2)
        om = np.maximum(om, sh * 0.85)
    a_s = np.maximum(tm, om)
    oc = np.array(ocol if ocol is not None else (style['ocol'] if (style and olw > 1) else (0, 0, 0)), np.float32)
    trgb = colr * tm[..., None] + oc * (a_s - tm)[..., None]
    da = dst[..., 3:4] / 255
    out_a = a_s[..., None] + da * (1 - a_s[..., None])
    out_rgb = (trgb + dst[..., :3] * da * (1 - a_s[..., None])) / np.maximum(out_a, 1e-4)
    img[y0:y1, x0:x1, :3] = np.clip(out_rgb, 0, 255)
    img[y0:y1, x0:x1, 3] = np.clip(out_a[..., 0] * 255, 0, 255)

BINARY = [False]

def apply_edits(img, edits, opaque=None):
    BINARY[0] = len(np.unique(img[..., 3])) <= 2
    if opaque is None: opaque = (img[..., 3] < 200).mean() < 0.2
    styles = []
    for e in edits:
        sb = e.get('sample', e['box'])
        styles.append(sample_style(img, sb, e.get('opaque', opaque)) if 'color' not in e else None)
    for e in edits:
        for b in [e.get('ebox', e['box'])] + e.get('erase', []): erase(img, b, e.get('opaque', opaque), full=e.get('full', False))
    for e, st in zip(edits, styles):
        if not e.get('text'): continue
        kw = {k: v for k, v in e.items() if k in ('kind', 'align', 'size', 'outline', 'color', 'shadow', 'vpad', 'spacing', 'olw', 'ocol')}
        draw(img, e.get('dbox', e['box']), e['text'], style=st, **kw)
    return img

def patch_file(data, specs, log=print):
    """data: bytearray of a .DAT; specs: {texname: [edits] or callable(img)->img}"""
    ts = {}
    for t in tex.scan(bytes(data)): ts.setdefault(t['name'], []).append(t)
    for name, edits in specs.items():
        if name.startswith('_'): continue
        for t in ts[name]:
            img, _ = tex.decode(bytes(data), t); img = img.copy()
            img = edits(img) if callable(edits) else apply_edits(img, edits)
            tex.encode_into(data, t, img)
        log('  tex %s x%d' % (name, len(ts[name])))
    return data
