# texture translation specs: file -> {texture name: [edits]}
def grid(cols, rowh, table, y0=0, **kw):
    """table: list of rows, each a list of texts (None = keep)"""
    out = []
    for r, row in enumerate(table):
        for c, txt in enumerate(row):
            if txt is None: continue
            x0, x1 = cols[c]
            out.append(dict(box=(x0, y0 + r * rowh + 1, x1, y0 + r * rowh + rowh - 1), text=txt, **kw))
    return out

STAT = dict(kind='g11b', align='l')
SPECS = {}
SPECS['AKI.DAT'] = {
    'menu_ps1': grid([(0, 47), (47, 95), (95, 128)], 16, [
        ['공격', '청력', '확률'],
        ['충격', '발소리', '한손'],
        ['치명', '미스릴', ''],
        ['방어', '길이', '양손'],
        ['내구', '종류', None],
        ['패링', '치저항', None],
        ['속도', '재생', None],
        ['마력', '무효', None],
    ], **STAT),
    'menu_pd1': grid([(0, 47), (47, 95), (95, 128)], 16, [
        ['치명', '내구', '마나'],
        ['저항', None, '확률'],
        ['공격', '무효', None],
        ['충격', '재생', '+지능'],
        ['길이', '+민첩', '한손'],
        ['속도', '패링', None],
        ['+힘', '마력', '양손'],
        ['방어', None, None],
    ], **STAT),
    'mnu_wnd5': [
        dict(box=(33, 79, 68, 94), text='힘', kind='g11b'),
        dict(box=(33, 96, 68, 111), text='민첩', kind='g11b'),
        dict(box=(33, 113, 68, 128), text='지능', kind='g11b'),
        dict(box=(194, 40, 238, 57), text='레벨', kind='g11b'),
        dict(box=(194, 59, 217, 76), text='경험', kind='g11b'),
    ],
    'cnf_wnd2': [
        dict(box=(132, 225, 194, 243), text='나가기', kind='serif', shadow=2, full=True, align='c'),
    ],
    'menu_pc1': [dict(box=(0, y, 112, y + 17), text=t, kind='serif', align='c', shadow=1) for y, t in
                 ((3, '없음'), (27, '작게'), (51, '크게'), (75, '자동 숨김'), (99, '표시'))],
    'menu_pc2': [dict(box=(0, y, 112, y + 18), text=t, kind='serif', align='c', shadow=1) for y, t in
                 ((3, '스테레오'), (27, '모노럴'), (51, '켜짐'), (75, '없음'))],
    'menu_tc1': [dict(box=(0, y, 112, y + 19), text=t, kind='serif', align='c', shadow=1) for y, t in
                 ((3, '스테레오'), (27, '모노럴'), (51, '켜짐'), (75, '없음'))],
    'menu_mg2': [dict(box=(34, 70, 104, 92), text='취소', kind='serif', align='c', opaque=True, full=True, shadow=1)],
    'm_common1': [dict(box=(0, 96, 64, 111), text='불가', kind='g11b')],
    'm_common5': [dict(box=(30, 2, 92, 17), text='저항', kind='sansh', align='c', opaque=True, full=True, shadow=1, color=(225, 225, 225))],
    'menu_sl01': [
        dict(box=(24, 124, 108, 172), text='저장', kind='serif', align='c', opaque=True, full=True, shadow=2),
        dict(box=(140, 124, 244, 176), text='로드', kind='serif', align='c', opaque=True, full=True, shadow=2),
    ],
    'game': 'TITLE',
}

def title(img):
    import numpy as np, texpatch as tp
    tp.BINARY[0] = True
    gold = tp.sample_style(img, (2, 230, 127, 251), False)
    grey = tp.sample_style(img, (7, 357, 250, 378), False)
    white = tp.sample_style(img, (3, 392, 196, 409), False)
    for b in [(0, 195, 256, 220), (0, 228, 128, 253), (0, 260, 128, 285), (0, 292, 128, 317), (0, 323, 130, 348),
              (0, 355, 256, 380), (0, 390, 256, 411), (0, 421, 512, 443), (0, 454, 100, 475)]:
        tp.erase(img, b, False)
    tp.draw(img, (8, 197, 250, 219), 'START 버튼을 누르세요', kind='sansh', style=gold, align='c', shadow=1)
    for y, t in ((230, '새 게임'), (262, '로드 게임'), (294, '옵션'), (325, '사전')):
        tp.draw(img, (0, y, 128, y + 21), t, kind='sansh', style=gold, align='c', shadow=1)
    tp.draw(img, (7, 358, 250, 378), '로도스도 전기  사신강림', kind='sansb', style=grey, align='l')
    tp.draw(img, (3, 392, 190, 409), '© 2000 카도카와 서점/ESP', kind='sansb', style=white, align='l')
    v = np.zeros((19, 603, 4), np.uint8)
    tp.draw(v, (3, 1, 603, 19), '© 1998 미즈노 료·그룹SNE·나츠모토 마사토/로도스도 전기 프로젝트/TV 도쿄', kind='sansb', style=white, align='l')
    img[423:442, 0:512] = v[:, :512]
    img[455:474, 0:91] = v[:, 512:603]
    return img
SPECS['AKI.DAT']['game'] = title

AREAS = {
    'm01_00': ('묘지 지하', '부활의 방'), 'm01_01': ('묘지 지하', '탈의 방'), 'm01_02': ('묘지 지하', '해의 방'),
    'm01_03': ('묘지 지하', '동굴'), 'm01_04': ('묘지 지하', '통로'), 'm01_05': ('묘지 지하', '독방'), 'm01_06': ('묘지 지하', '통로'),
    'm02_00': ('마모의 묘지', None), 'm04_00': ('고블린 요새', None),
    'm05_00': ('마모 남동', '구릉'), 'm05_01': ('마모 중앙', '사막'), 'm05_02': ('마모 북동', '습지'),
    'm05_03': ('마모 남서', '유적군'), 'm05_04': ('마모 북서', '산악'), 'm05_05': ('마모 북부', '호반'),
    'm06_00': ('피라미드', '１Ｆ'), 'm06_01': ('피라미드', '２Ｆ'), 'm06_02': ('피라미드', '３Ｆ'),
    'm06_03': ('다크엘프 마을', None), 'm07_00': ('마모 동단', '어둠의 숲'),
    'm08_00': ('고대 유적', None), 'm08_01': ('어둠의 숲', '지하 통로'), 'm08_03': ('지저 대협곡', None),
    'm08_04': ('지저 유적', '내부'), 'm08_11': ('고블린 대동굴', None),
    'm09_00': ('나스의 둥지', '동굴'), 'm09_01': ('나스의 둥지', '용의 방'), 'm10_00': ('팔라리스의 언덕', None),
    'm11_00': ('암흑 신전', 'Ｂ１'), 'm11_01': ('암흑 신전', 'Ｂ２'), 'm11_02': ('암흑 신전', 'Ｂ３'), 'm11_03': ('암흑 신전', 'Ｂ４'),
    'm11_04': ('팔라리스 대성당', None),
    'm12_00': ('얼음 동굴', 'Ｂ６'), 'm12_01': ('얼음 동굴', 'Ｂ７'), 'm12_02': ('얼음 동굴', 'Ｂ８'), 'm12_03': ('얼음 동굴', 'Ｂ９'),
    'm13_00': ('정복자의 성', '１Ｆ'), 'm13_01': ('정복자의 성', 'Ｂ１'), 'm13_02': ('정복자의 성', 'Ｂ２'),
    'm13_03': ('정복자의 성', '성문 아래'), 'm13_04': ('정복자의 성', 'Ｂ３'), 'm13_05': ('정복자의 성', 'Ｂ４'),
    'm13_06': ('정복자의 성', 'Ｂ５'), 'm14_00': ('카디스 신전', None), 'm16_30': ('용의 수호신', None),
}
for _i, _m in enumerate(['고블린 킹', '스켈레톤 킹', '좀비', '리자드맨', '사이클롭스', '아이언 골렘', '가고일', '엘더 나이트',
                         '타이탄 좀비', '고블린 로드', '리자드 킹', '암흑 신관', '타이탄', '메두사', '다크 샤먼', '레서 데몬',
                         '거대충', '팬텀', '기간데스 좀비', '퍼들 퀸', '샐러맨더', '그레이터 데몬', '플레임 데몬', '샌드 웜',
                         '기간데스', '키메라', '데몬 로드', '고블린 마스터', '미스릴 골렘', '헬 로드']):
    AREAS['m16_%02d' % _i] = ('요마의 둥지', _m)

def area_fn(l1, l2):
    def f(img):
        import numpy as np, texpatch as tp
        tp.BINARY[0] = False
        a = img[..., 3] > 60
        def bb(y0, y1):
            ys, xs = np.where(a[y0:y1])
            return (xs.min(), y0 + ys.min(), xs.max() + 1, y0 + ys.max() + 1) if len(xs) else None
        b1 = bb(0, 72); b2 = bb(72, 150)
        st = tp.sample_style(img, b1, False)
        img[0:150] = 0
        tp.draw(img, (2, 6, 510, 66), l1, kind='sansh', style=st, align='l', outline=True, olw=3, shadow=0, ocol=(0, 75, 160))
        if l2:
            r = b2[2] if b2 else 300
            tp.draw(img, (max(0, r - 420), 78, r, 138), l2, kind='sansh', style=st, align='r', outline=True, olw=3, shadow=0, ocol=(0, 75, 160))
        return img
    return f
SPECS['TAKIMG.DAT'] = {k: area_fn(*v) for k, v in AREAS.items()}

def gameover(img):
    import numpy as np, cv2, texpatch as tp
    tp.BINARY[0] = False
    a = img[..., 3].astype(int); rgb = img[..., :3].astype(int)
    glyph = (a >= 170) & ~((rgb > 185).all(2))
    glyph = cv2.dilate(glyph.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool) & (a >= 100) & ~((rgb > 200).all(2))
    st = tp.sample_style(img, (80, 36, 256, 66), False)
    st0 = tp.sample_style(img, (0, 0, 256, 28), False)
    img[0:30] = 0
    for b in [(80, 34, 256, 70), (128, 74, 256, 110), (80, 114, 256, 150), (0, 156, 48, 188), (0, 194, 52, 226)]:
        tp.erase_mask(img, b, glyph)
    tp.draw(img, (0, 1, 256, 28), '당신은 죽었다...', kind='serif', style=st0, align='c', outline=True, olw=1)
    v = np.zeros((32, 176 + 48, 4), np.uint8); v[:, :176] = img[35:67, 80:256]; v[:, 176:] = img[157:189, 0:48]
    tp.draw(v, (4, 1, 220, 31), '새 게임', kind='sansh', style=st, color=(175, 190, 95), align='c', outline=True, olw=1)
    img[35:67, 80:256] = v[:, :176]; img[157:189, 0:48] = v[:, 176:]
    tp.draw(img, (130, 76, 252, 107), '타이틀', kind='sansh', style=st, color=(175, 190, 95), align='c', outline=True, olw=1)
    v = np.zeros((32, 176 + 52, 4), np.uint8); v[:, :176] = img[115:147, 80:256]; v[:, 176:] = img[195:227, 0:52]
    tp.draw(v, (4, 1, 224, 31), '로드 게임', kind='sansh', style=st, color=(175, 190, 95), align='c', outline=True, olw=1)
    img[115:147, 80:256] = v[:, :176]; img[195:227, 0:52] = v[:, 176:]
    return img

def loading(img):
    import numpy as np, texpatch as tp
    tp.BINARY[0] = False
    s1 = tp.sample_style(img, (0, 0, 128, 30), False); s2 = tp.sample_style(img, (0, 64, 128, 94), False)
    img[0:128, 0:128] = 0
    tp.draw(img, (2, 2, 128, 30), '다음 지역', kind='sansh', style=s1, align='l', outline=True, olw=1)
    tp.draw(img, (2, 66, 128, 94), '로딩 중...', kind='sansh', style=s2, align='l', outline=True, olw=1)
    return img

SPECS['TAKIMG.DAT'].update({
    'gameover': gameover, 'loading': loading,
    'pal00': [dict(box=(22, 58, 168, 96), text='TV 설정', kind='sansh', align='l', opaque=True, full=True, outline=True, olw=1)],
    'waku00': [dict(box=(118, 12, 172, 36), text='테스트', kind='sansh', align='c', opaque=True, full=True, shadow=1)],
})

_L = ['토네이도', '거스트', '볼텍스', '미러', '고스트', '인비저블', '타워', '월', '케이지', '리콜']
_R = ['본파이어', '파이어 월', '파이어케이지', '애니메이트', '원더 데드', '컨트롤 데드', '스톤 커스', '스피어', '애시드 포그']
_Y = [3, 27, 51, 75, 99, 123, 147, 171, 194, 218]
SPECS['AKI.DAT']['magic_wnd2'] = (
    [dict(box=(0, y, 86, y + 19), text=t, kind='sansb', align='c') for y, t in zip(_Y, _L)] +
    [dict(box=(86, y, 178, y + 19), text=t, kind='sansb', align='c') for y, t in zip(_Y, _R)])
SPECS['AKI.DAT']['menu_pa1'] = (
    [dict(box=(0, y, 120, y + 14), text=t, kind='g11b', align='l') for y, t in
     zip([2, 18, 34, 50, 66, 82, 98], ['하나 선택', '무기 변환', '고대 단어', '아이템 복제', '전체 목록', '정련', '나가기'])] +
    [dict(box=(0, y0, 256, y1), text=t, kind='serif', align='l') for (y0, y1), t in
     zip([(130, 158), (162, 188), (192, 223), (225, 255)], ['무기 변환', '아이템 복제', '고대 단어 융합', '새 고대 단어 진화'])])

_O = dict(opaque=True, full=True, shadow=1)
SPECS['AKI.DAT'].update({
    'itm_wnd1': [dict(box=(34, 164, 190, 184), text='고대 단어 슬롯', kind='sansh', align='l', **_O),
                 dict(box=(62, 222, 130, 244), text='융합', kind='sansh', align='r', **_O),
                 dict(box=(50, 246, 130, 256), text='', **_O)],
    'itm_wnd2': [dict(box=(50, 190, 130, 210), text='내용', kind='sansh', align='r', **_O),
                 dict(box=(50, 224, 130, 248), text='미스릴', kind='sansh', align='r', **_O)],
    'comp3_wnd1': [dict(box=(22, 22, 210, 46), text='고대 단어', kind='serif', align='l', **_O)],
    'mnu_wnd2': [dict(box=(110, 56, 166, 69), text='버리기', kind='g9', align='c', **_O)],
})

_CACHE = {}
def _orig_tex(f, name):
    import os, tex
    if (f, name) not in _CACHE:
        d = open(os.path.join(os.path.dirname(__file__), '..', 'work', 'orig', f), 'rb').read()
        t = [x for x in tex.scan(d) if x['name'] == name][0]
        _CACHE[(f, name)] = tex.decode(d, t)[0].copy()
    return _CACHE[(f, name)].copy()

def _content(part):
    """'Content' label spans itm_wnd1 rows 244-256 and itm_wnd2 rows 196-208"""
    def f(img):
        import numpy as np, texpatch as tp
        a = _orig_tex('AKI.DAT', 'itm_wnd1'); b = _orig_tex('AKI.DAT', 'itm_wnd2')
        v = np.concatenate([a[244:256, 40:132], b[196:209, 40:132]], 0).copy()
        st = tp.sample_style(v, (12, 2, 90, 24), True)
        tp.BINARY[0] = False
        tp.erase(v, (10, 0, 92, 25), True, full=True)
        tp.draw(v, (10, 2, 90, 24), '내용', kind='sansh', style=st, align='r', shadow=1)
        if part == 1:
            img = tp.apply_edits(img, SPECS['AKI.DAT']['_itm1'])
            img[244:256, 40:132] = v[:12]
        else:
            img = tp.apply_edits(img, SPECS['AKI.DAT']['_itm2'])
            img[196:209, 40:132] = v[12:]
        return img
    return f
SPECS['AKI.DAT']['_itm1'] = SPECS['AKI.DAT']['itm_wnd1'][:2]
SPECS['AKI.DAT']['_itm2'] = SPECS['AKI.DAT']['itm_wnd2'][1:]
SPECS['AKI.DAT']['itm_wnd1'] = _content(1)
SPECS['AKI.DAT']['itm_wnd2'] = _content(2)

_N = dict(kind='sansh', align='c', opaque=True, full=True, outline=True)
SPECS['AKI.DAT'].update({
    'name_l_wnd1': [dict(box=(46, 83, 164, 101), text='한글１', **_N), dict(box=(188, 83, 256, 101), text='한글２', **_N)],
    'name_l_wnd3': [dict(box=(0, 83, 46, 101), text='', **_N)],
    'name_r_wnd1': [dict(box=(28, 83, 148, 101), text='영숫자', **_N), dict(box=(172, 83, 256, 101), text='한자', **_N)],
    'name_r_wnd4': [dict(box=(0, 83, 12, 99), text='', **_N)],
})

def cross_h(f, pieces, me, text, ebox, dbox, **kw):
    """label split horizontally across textures. pieces: [(tex, x0, y0, x1, y1)] same height, left->right"""
    def fn(img, _prev=None):
        import numpy as np, texpatch as tp
        if _prev: img = tp.apply_edits(img, _prev) if not callable(_prev) else _prev(img)
        parts = [_orig_tex(f, n)[y0:y1, x0:x1] for n, x0, y0, x1, y1 in pieces]
        v = np.concatenate(parts, 1).copy()
        st = tp.sample_style(v, ebox, kw.get('opaque', True))
        tp.BINARY[0] = False
        if kw.get('mask'): _rowfill(v, ebox, _textmask(v, ebox))
        else: tp.erase(v, ebox, kw.get('opaque', True), full=True)
        tp.draw(v, dbox, text, style=st, **{k: x for k, x in kw.items() if k not in ('opaque', 'mask')})
        x = 0
        for n, x0, y0, x1, y1 in pieces:
            if n == me: img[y0:y1, x0:x1] = v[:, x:x + x1 - x0]
            x += x1 - x0
        return img
    return fn
_RET = [('save_r_wnd2', 200, 118, 256, 166), ('save_r_wnd4', 80, 26, 118, 74)]
SPECS['AKI.DAT']['save_r_wnd2'] = cross_h('AKI.DAT', _RET, 'save_r_wnd2', '돌아가기', (4, 0, 92, 47), (10, 9, 88, 38), kind='sansh', align='c', shadow=1, mask=True)
SPECS['AKI.DAT']['save_r_wnd4'] = cross_h('AKI.DAT', _RET, 'save_r_wnd4', '돌아가기', (4, 0, 92, 47), (10, 9, 88, 38), kind='sansh', align='c', shadow=1, mask=True)

# ---------------------------------------------------------------- title option screen (labels split across atlas pieces)
_TC = {}
_TILES = [(0, 0, 256, 256, 'tcnf_l_wnd1', 0, 0), (256, 0, 304, 128, 'tcnf_l_wnd3', 256, 0), (256, 128, 304, 256, 'tcnf_l_wnd3', 208, 128),
          (304, 0, 560, 256, 'tcnf_r_wnd1', 304, 0), (0, 256, 256, 312, 'tcnf_l_wnd2', 0, 56), (256, 256, 288, 312, 'tcnf_l_wnd3', 160, 256),
          (288, 256, 304, 312, 'tcnf_l_wnd3', 192, 200), (304, 256, 560, 312, 'tcnf_r_wnd2', 304, 256)]
def _textmask(c, box, thr=22, sat_max=40):
    import numpy as np, cv2
    x0, y0, x1, y1 = box; r = c[y0:y1, x0:x1, :3].astype(np.float32)
    lum = r.mean(2); sat = r.max(2) - r.min(2)
    bg = np.median(lum[sat > np.percentile(sat, 60)])
    m = ((lum > bg + thr) & (sat < sat_max)) | (lum < bg * 0.62)
    m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    return cv2.dilate(m, np.ones((5, 5), np.uint8)).astype(bool)
def _rowfill(c, box, m, seed=1):
    import numpy as np, cv2
    x0, y0, x1, y1 = box; rng = np.random.default_rng(seed)
    reg = c[y0:y1, x0:x1].copy()
    for y in range(y1 - y0):
        ok = reg[y][~m[y]]
        if len(ok) < 4:
            yy = min(range(y1 - y0), key=lambda k: abs(k - y) if (~m[k]).sum() >= 4 else 999); ok = reg[yy][~m[yy]]
        reg[y][m[y]] = ok[rng.integers(0, len(ok), m[y].sum())]
    sm = cv2.blur(reg[..., :3], (3, 3)); reg[..., :3] = np.where(m[..., None], sm, reg[..., :3])
    c[y0:y1, x0:x1] = reg
def _tcnf_build():
    import numpy as np, texpatch as tp
    c = np.zeros((312, 560, 4), np.uint8)
    for x0, y0, x1, y1, n, dx, dy in _TILES: c[y0:y1, x0:x1] = _orig_tex('AKI.DAT', n)[y0 - dy:y1 - dy, x0 - dx:x1 - dx]
    tp.BINARY[0] = False
    labels = [('사운드', 123), ('진동', 147), ('배경음', 171), ('효과음', 195), ('화면 조정', 219)]
    styles = [tp.sample_style(c, (219, y, 309, y + 19), True) for _, y in labels]
    st_ex = tp.sample_style(c, (285, 260, 356, 287), True); st_op = tp.sample_style(c, (256, 50, 380, 92), True)
    clean = c[195:214, 262:308].copy()                     # empty right part of the SE button
    tile = np.concatenate([clean, clean[:, ::-1]], 1)
    for (t, y), st in zip(labels, styles):
        w = 309 - 219; c[y:y + 19, 219:309] = np.tile(tile, (1, w // tile.shape[1] + 1, 1))[:, :w]
    _rowfill(c, (284, 259, 357, 288), _textmask(c, (284, 259, 357, 288), 18))
    _rowfill(c, (252, 48, 384, 94), _textmask(c, (252, 48, 384, 94)))
    for (t, y), st in zip(labels, styles):
        tp.draw(c, (222, y + 1, 306, y + 18), t, kind='serif', style=st, align='l', shadow=1, outline=True)
    tp.draw(c, (288, 261, 353, 286), '나가기', kind='serif', style=st_ex, align='c', shadow=1, outline=True)
    tp.draw(c, (268, 52, 372, 90), '옵션', kind='serif', style=st_op, align='c', shadow=2, outline=True)
    return c
def _tcnf(name):
    def f(img):
        if not _TC: _TC['c'] = _tcnf_build()
        c = _TC['c']
        for x0, y0, x1, y1, n, dx, dy in _TILES:
            if n == name: img[y0 - dy:y1 - dy, x0 - dx:x1 - dx] = c[y0:y1, x0:x1]
        return img
    return f
for _n in ['tcnf_l_wnd1', 'tcnf_l_wnd2', 'tcnf_l_wnd3', 'tcnf_r_wnd1', 'tcnf_r_wnd2']:
    SPECS['AKI.DAT'][_n] = _tcnf(_n)

_SP = [('name_l_wnd2', 96, 166, 144, 192), ('name_r_wnd2', 0, 118, 80, 144)]
_spkw = dict(kind='sansh', align='c', outline=True)
SPECS['AKI.DAT']['_nl2'] = [dict(box=(68, 66, 180, 86), text='한 글자 삭제', **_N)]
SPECS['AKI.DAT']['_nr2'] = [dict(box=(148, 123, 256, 141), text='결정', **_N)]
SPECS['AKI.DAT']['name_l_wnd2'] = cross_h('AKI.DAT', _SP, 'name_l_wnd2', '공백', (6, 4, 122, 22), (6, 5, 122, 21), **_spkw)
SPECS['AKI.DAT']['name_r_wnd2'] = cross_h('AKI.DAT', _SP, 'name_r_wnd2', '공백', (6, 4, 122, 22), (6, 5, 122, 21), **_spkw)
_f1, _f2 = SPECS['AKI.DAT']['name_l_wnd2'], SPECS['AKI.DAT']['name_r_wnd2']
SPECS['AKI.DAT']['name_l_wnd2'] = lambda img, _f=_f1: _f(__import__('texpatch').apply_edits(img, SPECS['AKI.DAT']['_nl2']))
SPECS['AKI.DAT']['name_r_wnd2'] = lambda img, _f=_f2: _f(__import__('texpatch').apply_edits(img, SPECS['AKI.DAT']['_nr2']))
_CN = {}
def _cnf_build():
    import numpy as np, texpatch as tp
    w1 = _orig_tex('AKI.DAT', 'cnf_wnd1'); w2 = _orig_tex('AKI.DAT', 'cnf_wnd2')
    c = np.concatenate([w1, w2[200:216]], 0).copy()
    tp.BINARY[0] = False
    labels = ['맵', '아이콘', '사운드', '진동', '배경음', '효과음', '불러오기', '화면 조정']
    tops = [72 + 24 * i for i in range(8)]
    styles = [tp.sample_style(c, (66, t + 2, 158, t + 21), True) for t in tops]
    clean = c[194:213, 100:157].copy(); tile = np.concatenate([clean, clean[:, ::-1]], 1)
    for t in tops:
        w = 158 - 66; c[t + 2:t + 21, 66:158] = np.tile(tile, (1, w // tile.shape[1] + 1, 1))[:, :w]
    st_op = tp.sample_style(c, (30, 32, 126, 64), True)
    _rowfill(c, (33, 35, 123, 61), _textmask(c, (33, 35, 123, 61)))
    for t, lab, st in zip(tops, labels, styles):
        tp.draw(c, (69, t + 3, 156, t + 20), lab, kind='serif', style=st, align='l', shadow=1, outline=True)
    tp.draw(c, (32, 33, 124, 63), '옵션', kind='serif', style=st_op, align='c', shadow=2, outline=True)
    return c
def _cnf1(img):
    if not _CN: _CN['c'] = _cnf_build()
    img[:256] = _CN['c'][:256]; return img
_cnf2_edits = SPECS['AKI.DAT']['cnf_wnd2']
def _cnf2(img):
    import texpatch as tp
    if not _CN: _CN['c'] = _cnf_build()
    img = tp.apply_edits(img, _cnf2_edits); img[200:216] = _CN['c'][256:272]; return img
SPECS['AKI.DAT']['cnf_wnd1'] = _cnf1
SPECS['AKI.DAT']['cnf_wnd2'] = _cnf2

def _sl01(img):
    import texpatch as tp
    tp.BINARY[0] = False
    jobs = [((24, 124, 108, 172), (22, 120, 121, 172), '저장'), ((140, 124, 244, 176), (138, 120, 244, 176), '로드')]
    sts = [tp.sample_style(img, b, True) for b, _, _ in jobs]
    for (b, e, t), st in zip(jobs, sts):
        _rowfill(img, e, _textmask(img, e, 30, 999))
        tp.draw(img, b, t, kind='serif', style=st, align='c', shadow=2, outline=True)
    return img
SPECS['AKI.DAT']['menu_sl01'] = _sl01
