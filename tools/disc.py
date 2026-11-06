# Output disc handling: copy original Track 5 to [KR] file, write files in place.
import os, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
import gdfs
ROOT = gdfs.BASE
ORIG5 = os.path.join(ROOT, gdfs.NAME % 5)
OUT5 = os.path.join(ROOT, 'Record of Lodoss War - The Advent of Cardice (Japan) (Track 5) [KR].bin')
OUTCUE = os.path.join(ROOT, 'Record of Lodoss War - The Advent of Cardice (Japan) [KR].cue')

class OutDisc(gdfs.Disc):
    def __init__(self):
        gdfs.Disc.__init__(self)          # read-only originals (for directory)
        self.files_map = self.files()
        self.f[5].close()
        self.f[5] = open(OUT5, 'r+b')
    def put(self, name, data):
        lba, size, _, _ = self.files_map[name]
        alloc = (size + 2047) // 2048 * 2048
        assert len(data) <= alloc, (name, len(data), alloc)
        if len(data) != size:
            assert len(data) == size, 'size change not supported: %s' % name
        pad = data + bytes((-len(data)) % 2048)
        self.write(lba, pad)

def fresh_copy():
    shutil.copyfile(ORIG5, OUT5)

def write_cue():
    src = open(os.path.join(ROOT, 'Record of Lodoss War - The Advent of Cardice (Japan).cue'), encoding='ascii').read()
    src = src.replace('(Track 5).bin', '(Track 5) [KR].bin')
    open(OUTCUE, 'w', encoding='ascii', newline='\r\n').write(src.replace('\r\n', '\n'))
