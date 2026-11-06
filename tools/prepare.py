"""원본 디스크에서 빌드 입력을 만든다 (일본어 원문은 저장소에 없고 여기서 사용자 디스크로부터 생성).
사용: python tools/prepare.py   (저장소 폴더에서, 원본 Track 1~5 BIN과 CUE를 같은 폴더에 둔 상태)
1) GD 영역 파일을 work/orig/ 로 추출  2) work/cand_offsets.json + 실행파일 → work/cand.json
3) export.py · dictfmt.py · mkbatches.py 로 work/tr/in/ 생성 (번역 work/tr/out/ 과 id로 연결)
"""
import os, sys, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE); os.chdir(ROOT)
import gdfs
NEED = ['1NOSDC.BIN', 'DATANOS.BIN', 'KANIMG.DAT', 'AKI.DAT', 'TAKIMG.DAT']
os.makedirs('work/orig', exist_ok=True)
d = gdfs.Disc(); fs = d.files()
for name in NEED:
    lba, size, _, _ = fs[name]
    open('work/orig/' + name, 'wb').write(d.read(lba, size)); print('extract', name, size)
exe = open('work/orig/1NOSDC.BIN', 'rb').read()
c = json.load(open('work/cand_offsets.json', encoding='utf-8'))
for k in c:
    for x in c[k]:
        x['jp'] = exe[x['off']:x['off'] + x['len']].split(b'\0')[0].decode('cp932', 'replace')
json.dump(c, open('work/cand.json', 'w', encoding='utf-8'), ensure_ascii=False)
for s in ['export.py', 'dictfmt.py', 'mkbatches.py']:
    subprocess.run([sys.executable, os.path.join('tools', s)], check=True, stdout=subprocess.DEVNULL)
print('prepare done')
