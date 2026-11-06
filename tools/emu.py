# Background redream controller: python emu.py start <cue> | key <name> [ms] | shot <png> | stop
import ctypes, ctypes.wintypes as W, subprocess, sys, time, os, json
u32 = ctypes.windll.user32; g32 = ctypes.windll.gdi32
HERE = os.path.dirname(os.path.abspath(__file__)); EMU = os.path.join(HERE, '..', 'work', 'emu')
STATE = os.path.join(EMU, 'pid.json')
KEYS = {'a':'L','b':'P','x':'K','y':'O','start':' ','up':'T','down':'G','left':'F','right':'H','lt':0xDB,'rt':0xDD,
        'f5':0x74,'ju':'W','jd':'S','jl':'A','jr':'D'}
def vk(k):
    v = KEYS.get(k, k); return v if isinstance(v, int) else ord(v.upper())
def find_hwnd(pid):
    res = []
    @ctypes.WINFUNCTYPE(W.BOOL, W.HWND, W.LPARAM)
    def cb(h, l):
        p = W.DWORD(); u32.GetWindowThreadProcessId(h, ctypes.byref(p))
        if p.value == pid and u32.IsWindowVisible(h): res.append(h)
        return True
    u32.EnumWindows(cb, 0); return res[0] if res else None
def hwnd():
    return find_hwnd(json.load(open(STATE))['pid'])
def start(cue):
    p = subprocess.Popen([os.path.join(EMU, 'redream.exe'), os.path.abspath(cue)], cwd=EMU)
    json.dump({'pid': p.pid}, open(STATE, 'w'))
    for _ in range(100):
        time.sleep(0.1); h = find_hwnd(p.pid)
        if h: break
    # move off-screen without activating
    u32.SetWindowPos(h, 0, -3000, 50, 0, 0, 0x0001 | 0x0004 | 0x0010)
    print('started', p.pid, h)
def key(name, ms=80):
    h = hwnd(); v = vk(name); sc = u32.MapVirtualKeyW(v, 0)
    u32.PostMessageW(h, 0x100, v, 1 | (sc << 16)); time.sleep(ms / 1000)
    u32.PostMessageW(h, 0x101, v, 1 | (sc << 16) | (3 << 30)); time.sleep(0.05)
def shot(fn):
    import glob, shutil
    for f in glob.glob(os.path.join(EMU, 'screenshot*.png')): os.remove(f)
    key('f5'); 
    for _ in range(50):
        time.sleep(0.1); g = glob.glob(os.path.join(EMU, 'screenshot*.png'))
        if g: time.sleep(0.3); shutil.move(g[0], fn); print('saved', fn); return
    print('shot failed')
def shot_gdi(fn):
    from PIL import Image
    h = hwnd(); r = W.RECT(); u32.GetClientRect(h, ctypes.byref(r)); w, hh = r.right, r.bottom
    hdc = u32.GetDC(h); mdc = g32.CreateCompatibleDC(hdc); bmp = g32.CreateCompatibleBitmap(hdc, w, hh)
    g32.SelectObject(mdc, bmp); u32.PrintWindow(h, mdc, 3)
    buf = ctypes.create_string_buffer(w * hh * 4)
    class BI(ctypes.Structure): _fields_ = [('a', W.DWORD), ('w', W.LONG), ('h', W.LONG), ('p', W.WORD), ('b', W.WORD), ('c', W.DWORD), ('s', W.DWORD), ('x', W.LONG), ('y', W.LONG), ('u', W.DWORD), ('i', W.DWORD)]
    bi = BI(40, w, -hh, 1, 32, 0, 0, 0, 0, 0, 0)
    g32.GetDIBits(mdc, bmp, 0, hh, buf, ctypes.byref(bi), 0)
    Image.frombuffer('RGBA', (w, hh), buf, 'raw', 'BGRA', 0, 1).convert('RGB').save(fn)
    g32.DeleteObject(bmp); g32.DeleteDC(mdc); u32.ReleaseDC(h, hdc); print('saved', fn)
def stop():
    pid = json.load(open(STATE))['pid']; subprocess.call(['taskkill', '/F', '/PID', str(pid)], stdout=subprocess.DEVNULL); os.remove(STATE)
if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'start': start(sys.argv[2])
    elif c == 'stop': stop()
    elif c == 'shot': shot(sys.argv[2])
    elif c == 'wait': time.sleep(float(sys.argv[2]))
    elif c == 'seq':  # seq "start:200,wait:2,a"
        for it in sys.argv[2].split(','):
            n, _, v = it.partition(':')
            if n == 'wait': time.sleep(float(v))
            elif n == 'shot': shot(v)
            else: key(n, int(v) if v else 80)
    else: key(c, int(sys.argv[2]) if len(sys.argv) > 2 else 80)
