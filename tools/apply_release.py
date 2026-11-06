"""릴리즈 xdelta 를 해시 검사 후 적용.
사용: python tools/apply_release.py --xdelta xdelta3.exe --source "Record of Lodoss War - The Advent of Cardice (Japan) (Track 5).bin" --patch LodossWar_Cardice_DC_KO_v1.2.xdelta --output "Record of Lodoss War - The Advent of Cardice (Japan) (Track 5) [KR].bin"
트랙 1~4는 바뀌지 않으므로 원본 트랙 1~4를 그대로 가리키는 CUE를 만든다.
"""
import argparse, hashlib, json, os, subprocess, sys

MAN = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'release_manifest.json'), encoding='utf-8'))
ORIG = 'Record of Lodoss War - The Advent of Cardice (Japan) (Track %d).bin'

def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''): h.update(b)
    return h.hexdigest()

def check(p, size, digest, what):
    if os.path.getsize(p) != size: sys.exit('%s 크기 불일치: %d (기대 %d)' % (what, os.path.getsize(p), size))
    print(what, '해시 확인 중...', flush=True)
    if sha256(p) != digest: sys.exit('%s SHA-256 불일치' % what)

a = argparse.ArgumentParser()
a.add_argument('--xdelta', default='xdelta3')
a.add_argument('--source', required=True, help='원본 트랙 5 BIN')
a.add_argument('--patch', required=True)
a.add_argument('--output', required=True)
o = a.parse_args()
if os.path.exists(o.output): sys.exit('출력 파일이 이미 있습니다: ' + o.output)
check(o.source, MAN['source_bin_size'], MAN['source_bin_sha256'], '원본 트랙 5 BIN')
check(o.patch, MAN['asset_size'], MAN['asset_sha256'], 'xdelta')
subprocess.run([o.xdelta, '-d', '-s', o.source, o.patch, o.output], check=True)
check(o.output, MAN['output_bin_size'], MAN['output_bin_sha256'], '결과 트랙 5 BIN')
out_dir = os.path.dirname(os.path.abspath(o.output)); src_dir = os.path.dirname(os.path.abspath(o.source))
base = os.path.basename(o.output)
cue = os.path.join(out_dir, base.replace(' (Track 5)', '').rsplit('.', 1)[0] + '.cue')
if not os.path.exists(cue):
    t = lambda n: os.path.relpath(os.path.join(src_dir, ORIG % n), out_dir)
    NL = chr(10)
    lines = ['REM SINGLE-DENSITY AREA',
             'FILE "%s" BINARY' % t(1), '  TRACK 01 MODE1/2352', '    INDEX 01 00:00:00',
             'FILE "%s" BINARY' % t(2), '  TRACK 02 AUDIO', '    INDEX 00 00:00:00', '    INDEX 01 00:02:00',
             'REM HIGH-DENSITY AREA',
             'FILE "%s" BINARY' % t(3), '  TRACK 03 MODE1/2352', '    INDEX 01 00:00:00',
             'FILE "%s" BINARY' % t(4), '  TRACK 04 AUDIO', '    INDEX 00 00:00:00', '    INDEX 01 00:02:00',
             'FILE "%s" BINARY' % base, '  TRACK 05 MODE1/2352', '    INDEX 00 00:00:00', '    INDEX 01 00:03:00']
    open(cue, 'w', encoding='utf-8').write(NL.join(lines) + NL)
    print('CUE 생성:', cue)
print('완료:', o.output)
