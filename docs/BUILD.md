# 재빌드

## 준비물

빌드 스크립트는 저장소 폴더를 작업 폴더로 씁니다. 원본 디스크와 글꼴을 **저장소 폴더 안**에 둡니다(`.gitignore`로 제외됩니다).

```
<저장소>/
  Record of Lodoss War - The Advent of Cardice (Japan).cue
  Record of Lodoss War - The Advent of Cardice (Japan) (Track 1).bin ~ (Track 5).bin   ← README의 해시와 일치해야 함
  NanumSquareNeo-cBd.ttf  NanumSquareNeo-dEb.ttf  NanumSquareNeo-eHv.ttf  NanumSquareNeo-bRg.ttf
  SeoulHangangEB.ttf  SeoulHangangB.ttf  SeoulHangangM.ttf
  work/fonts/Galmuri9.ttf  Galmuri11.ttf  Galmuri11-Bold.ttf  Galmuri14.ttf
```

- Python 3.13, `numpy`, `Pillow`, `opencv-python`
- 글꼴 출처는 `docs/FONT_CREDITS.md`
- xdelta3 (배포 파일을 만들 때만)

## 빌드

저장소 폴더에서 실행합니다.

```powershell
python tools/prepare.py          # 원본 디스크 → work/orig/, work/cand.json, work/tr/in/ (원문은 여기서만 생성)
python tools/build.py --disc     # → "Record of Lodoss War - The Advent of Cardice (Japan) (Track 5) [KR].bin" 과 [KR].cue
```

`build.py`는 원본 트랙 5를 `[KR]` 파일로 복사한 뒤 바뀐 파일(`1NOSDC.BIN`, `DATANOS.BIN`, `KANIMG.DAT`, `AKI.DAT`, `TAKIMG.DAT`)만 같은 자리에 다시 씁니다. 로그는 `work/build/build.log`에 남고, `MISSING chars`가 없어야 합니다. 결과 BIN의 SHA-256이 `release_manifest.json`의 `output_bin_sha256`과 같아야 합니다. 트랙 1~4는 원본을 그대로 씁니다.

## 배포 파일

```powershell
xdelta3 -e -0 -S none -A -s "Record of Lodoss War - The Advent of Cardice (Japan) (Track 5).bin" "Record of Lodoss War - The Advent of Cardice (Japan) (Track 5) [KR].bin" LodossWar_Cardice_DC_KO_v1.1.xdelta
```

## 번역 수정

1. `work/tr/out/*.json`의 해당 id 항목을 고칩니다(`docs/TRANSLATION_GUIDE.md`).
2. `python tools/validate.py work/tr/out/script_3.json`처럼 검사해 `ERRORS: 0`을 확인합니다. 사전은 `python tools/dictlines.py`로 한 쪽(23칸×8줄)에 들어가는지 확인합니다.
3. `python tools/build.py --disc`를 다시 실행합니다.

## 그림 글자 수정

`tools/texspec.py`에 텍스처 이름별로 지울 영역·그릴 글자·글꼴이 적혀 있습니다. `tools/tex.py`로 원본 텍스처를 PNG로 뽑아 위치를 확인할 수 있습니다(`tex.scan`, `tex.png`).
