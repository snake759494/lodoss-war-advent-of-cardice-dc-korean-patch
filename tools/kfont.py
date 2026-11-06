# Korean font / encoding support for Lodoss War DC (nfont kanji table in DATANOS.BIN)
import os, numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
KANJI_BASE = 0x2a000          # file offset in DATANOS.BIN of JIS index 0 (0x2121)
GLYPH = 100                   # bytes per glyph, 20x20, 2 bits/px (MSB first)
FONT_FILE = os.path.join(ROOT, 'NanumSquareNeo-cBd.ttf')

HANGUL = [bytes([hi, lo]).decode('cp949') for hi in range(0xB0, 0xC9) for lo in range(0xA1, 0xFF)]
assert len(HANGUL) == 2350

def jis_index_to_sjis(idx):
    row, col = divmod(idx, 94)          # 0-based ku/ten
    j1, j2 = row + 0x21, col + 0x21
    s1 = (j1 + 1) // 2 + (0x70 if j1 <= 0x5e else 0xb0)
    if j1 & 1:
        s2 = j2 + (0x1f if j2 <= 0x5f else 0x20)
    else:
        s2 = j2 + 0x7e
    return (s1 << 8) | s2

def sjis_to_jis_index(code):
    s1, s2 = code >> 8, code & 0xff
    s1 -= 0x70 if s1 <= 0x9f else 0xb0
    j1 = s1 * 2 - 1
    if s2 >= 0x9f:
        j1 += 1; j2 = s2 - 0x7e
    else:
        j2 = s2 - (0x1f if s2 <= 0x7e else 0x20)
    return (j1 - 0x21) * 94 + (j2 - 0x21)

def build_slots():
    """hangul char -> sjis code (2 bytes), sequential from JIS row 16, skipping trail 0x5C."""
    m = {}; idx = 1410; i = 0
    while i < len(HANGUL):
        code = jis_index_to_sjis(idx); idx += 1
        if (code & 0xff) in (0x5c, 0x7f): continue
        m[HANGUL[i]] = code; i += 1
    return m

SLOTS = build_slots()

def render_glyph(ch, font, size=20, yoff=0, xoff=0):
    img = Image.new('L', (size * 2, size * 2), 0)
    dr = ImageDraw.Draw(img)
    bbox = font.getbbox(ch)
    dr.text((xoff + (size - (bbox[2] - bbox[0])) / 2 - bbox[0] + size / 2, yoff + size / 2), ch, font=font, fill=255)
    a = np.array(img)[size // 2: size // 2 + size, size // 2: size // 2 + size]
    return a

def levels(a, hi=120, lo=50):
    """grayscale 20x20 -> 2-bit values: 2 = bright core, 3 = dim edge, 0 = empty"""
    return np.where(a > hi, 2, np.where(a > lo, 3, 0)).astype(np.uint8)

def pack(px):  # px: 20x20 values (bool -> 2) -> 100 bytes
    if px.dtype == bool: px = np.where(px, 2, 0)
    v = px.astype(np.uint8).reshape(-1, 4)
    b = (v[:, 0] << 6) | (v[:, 1] << 4) | (v[:, 2] << 2) | v[:, 3]
    return b.astype(np.uint8).tobytes()

def unpack(b):
    a = np.frombuffer(b, np.uint8)
    return (np.stack([a >> 6, (a >> 4) & 3, (a >> 2) & 3, a & 3], -1).reshape(20, 20) > 0)
