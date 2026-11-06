# 로도스도전기 사신강림 드림캐스트 한글패치

드림캐스트 일본판 **ロードス島戦記 -邪神降臨- (T-27903M V1.001)**용 비공식 한국어 패치입니다. **대사·나레이션·선택지 1,589개(5,150줄) 전체**와 **아이템·마법·메뉴·시스템 메시지 등 실행파일 문자열 1,172종**, **사전(총람) 380항목**을 한국어로 바꿨습니다. **타이틀 메뉴·옵션 화면·상태/장비 약자·마법 이름·고대 단어 창·이름 입력·저장/로드·지역 이름 79종·게임오버·로딩 화면** 같은 그림 글자도 한글로 다시 그렸습니다. 현재 배포판은 **v1.2 (2026-11-07)**입니다.

[패치 다운로드](https://github.com/snake759494/lodoss-war-advent-of-cardice-dc-korean-patch/releases/latest) · [기술 설명](docs/TECHNICAL.md) · [재빌드](docs/BUILD.md) · [변경 기록](CHANGELOG.md) · [권리 안내](RIGHTS.md)

릴리즈 첨부 파일은 한글패치 **LodossWar_Cardice_DC_KO_v1.2.xdelta**뿐입니다. 저장소에는 제작 소스와 한국어 번역만 공개합니다. 원본·완성 디스크 이미지, 추출한 게임 파일, 일본어 원문, 글꼴 파일, 외부 실행 파일은 포함하지 않습니다. GitHub가 자동으로 만드는 Source code ZIP/TAR는 저장소 소스를 압축한 것이며 게임 파일이 아닙니다.

## 게임 소개 및 대상 버전

『로도스도전기 사신강림』은 미즈노 료의 판타지 소설 『로도스도전기』를 바탕으로 2000년 카도카와 서점이 발매한 드림캐스트 액션 RPG입니다. 대현자 워트에게 되살아난 주인공이 마모의 땅을 돌아다니며 사신 카디스의 부활을 막는 이야기로, 무기에 고대 단어를 새겨 강화하는 시스템이 특징입니다.

이 패치는 **드림캐스트 일본판 T-27903M V1.001의 Redump 형식 BIN/CUE 이미지(트랙 5개)**의 **트랙 5**에만 적용합니다. 트랙 1~4는 바뀌지 않으므로 원본을 그대로 씁니다. 파일 이름보다 아래 표의 크기와 해시가 일치하는지가 중요합니다.

## 적용할 원본

| 항목 | 값 |
| --- | --- |
| 게임 ID | T-27903M V1.001 (2000-05-08) |
| 원본 형식 | 수정되지 않은 일본판 Redump BIN/CUE (트랙 5개) |
| 원본 트랙 5 BIN 크기 | 727,979,280 바이트 |
| **원본 트랙 5 BIN MD5** | `43882ab1e6d5c22388bc34f15ff315de` |
| 원본 트랙 5 BIN SHA-1 | `0e47ea419a791bcd87e7b648eb177b71048f8570` |
| 원본 트랙 5 BIN SHA-256 | `cc135e51e100b9ab748878fe7464093fc5e635a0bef577e3abe1aed27b750144` |
| 원본 트랙 3 BIN MD5 (변경 없음) | `7840754b56d7bf940c93012c05b99e62` |
| xdelta 파일 크기 | 1,905,516 바이트 |
| xdelta SHA-256 | `16025cf0a968f58cb0b0c0709a923d6ad3530a240ee2d6590b9cdb47ff6ea7bb` |
| 적용 결과 트랙 5 BIN 크기 | 727,979,280 바이트 (원본과 같음) |
| 적용 결과 트랙 5 BIN SHA-1 | `222196e07aa8ba911c38659c80eb592c2d5923a9` |
| 적용 결과 트랙 5 BIN SHA-256 | `d6f14713d5832e5349fa52c43d1be64b30e8fc936bcc5cb78240fa7e46599d40` |

원본 게임 파일은 사용자가 직접 준비해야 합니다.

## 패치 적용 방법

### Windows에서 원본 확인

```powershell
Get-FileHash -Algorithm MD5 -LiteralPath '.\Record of Lodoss War - The Advent of Cardice (Japan) (Track 5).bin'
```

위 표와 다르면 적용을 중단하세요. CHD, CDI, GDI 변환본 등 다른 형식에는 적용할 수 없습니다.

### xdelta UI 사용

1. 릴리즈에서 `LodossWar_Cardice_DC_KO_v1.2.xdelta`를 받습니다.
2. xdelta3 패치를 지원하는 도구에서 **Apply Patch** 기능을 엽니다.
3. **Patch**에는 xdelta 파일을, **Source File**에는 해시가 일치하는 원본 **트랙 5** `.bin`을 선택합니다.
4. **Output File**에는 `Record of Lodoss War - The Advent of Cardice (Japan) (Track 5) [KR].bin`을 지정합니다.
5. 원본 `.cue`를 복사해 `Record of Lodoss War - The Advent of Cardice (Japan) [KR].cue`로 이름을 바꾸고, 그 안의 `(Track 5).bin`을 `(Track 5) [KR].bin`으로 고칩니다. 트랙 1~4 파일은 원본 그대로 같은 폴더에 둡니다.

```
REM SINGLE-DENSITY AREA
FILE "Record of Lodoss War - The Advent of Cardice (Japan) (Track 1).bin" BINARY
  TRACK 01 MODE1/2352
    INDEX 01 00:00:00
FILE "Record of Lodoss War - The Advent of Cardice (Japan) (Track 2).bin" BINARY
  TRACK 02 AUDIO
    INDEX 00 00:00:00
    INDEX 01 00:02:00
REM HIGH-DENSITY AREA
FILE "Record of Lodoss War - The Advent of Cardice (Japan) (Track 3).bin" BINARY
  TRACK 03 MODE1/2352
    INDEX 01 00:00:00
FILE "Record of Lodoss War - The Advent of Cardice (Japan) (Track 4).bin" BINARY
  TRACK 04 AUDIO
    INDEX 00 00:00:00
    INDEX 01 00:02:00
FILE "Record of Lodoss War - The Advent of Cardice (Japan) (Track 5) [KR].bin" BINARY
  TRACK 05 MODE1/2352
    INDEX 00 00:00:00
    INDEX 01 00:03:00
```

xdelta는 호환성을 위해 압축·2차 압축·파일 경로 헤더 없이 만들었습니다. xdelta 자체는 [공식 프로젝트](https://github.com/jmacd/xdelta)를 참고하세요.

### 명령줄 사용

```powershell
.\xdelta3.exe -d -s '.\Record of Lodoss War - The Advent of Cardice (Japan) (Track 5).bin' '.\LodossWar_Cardice_DC_KO_v1.2.xdelta' '.\Record of Lodoss War - The Advent of Cardice (Japan) (Track 5) [KR].bin'
```

해시를 자동으로 검사하고 CUE까지 만들어 주는 도구도 있습니다(CUE의 트랙 1~4는 원본을 그대로 가리킵니다). Python 3과 xdelta3가 필요하며, 같은 이름의 출력 파일이 이미 있으면 덮어쓰지 않습니다.

```powershell
python tools/apply_release.py --xdelta '.\xdelta3.exe' --source '.\Record of Lodoss War - The Advent of Cardice (Japan) (Track 5).bin' --patch '.\LodossWar_Cardice_DC_KO_v1.2.xdelta' --output '.\Record of Lodoss War - The Advent of Cardice (Japan) (Track 5) [KR].bin'
```

### 실행

에뮬레이터(redream 등)에서 결과 `[KR].cue`를 여세요. 원본판의 세이브 스테이트는 불러오지 마세요(실행파일 내용이 다릅니다). VMU 세이브는 원본판과 같은 형식입니다.

## 작업 내용과 범위

| 구분 | 작업량 및 내용 |
| --- | --- |
| 대사 | 이벤트 대사·나레이션·선택지·화자 이름 1,589개(5,150줄) |
| 실행파일 문자열 | 아이템·무기·방어구·마법·고대 단어·메뉴·시스템 메시지·도움말 1,172종 |
| 사전(총람) | 인물·지리·생물·물품 380항목과 상호 링크 |
| 글꼴 | 게임 한자 글꼴 자리에 KS X 1001 한글 2,350자를 나눔스퀘어 네오로 그려 넣음 |
| 이름 입력 | 가나 입력판을 한글 음절표 2쪽으로 바꾸고, 「한글1」「한글2」「영숫자」「한자」·「한 글자 삭제」「공백」「결정」 버튼을 다시 그림 |
| 타이틀 | 「START 버튼을 누르세요」, 새 게임·로드 게임·옵션·사전, 로고 아래 「로도스도 전기 사신강림」 자막, 저작권 표기 |
| 옵션 화면 | 타이틀 옵션과 게임 안 옵션의 제목·항목 버튼(사운드·진동·배경음·효과음·화면 조정·맵·아이콘·불러오기), 설정값, 나가기 |
| 메뉴 그림 글자 | 상태·장비 능력치 약자(공격·방어·치명·내구·패링·힘·민첩·지능 등), 장비 부위, 마법 이름, 고대 단어·융합·정련 창, 저장/로드, 돌아가기, 버리기 |
| 지역 이름 | 지역 진입 때 나오는 이름 그림 79종 |
| 기타 화면 | 게임오버, 로딩, TV 설정 |

### 번역 원칙

- 기계 번역 없이 문맥을 보고 직접 번역했습니다(`docs/TRANSLATION_GUIDE.md`).
- 인명·지명은 국내에 알려진 『로도스도전기』 표기를 기준으로 했습니다(판, 디드리트, 슬레인, 카를라, 애슐럼, 카디스, 워트 등).
- 대사 상자는 한 줄 16칸이라 원문 길이를 넘지 않게 다듬었습니다.

### 번역하지 않은 것

- 타이틀 영문 로고(RECORD OF LODOSS WAR / THE ADVENT OF CARDICE) — 그림을 살리고 아래에 한글 자막을 넣었습니다.
- HP·MP 같은 일반 약어, 고대어 주문 구간의 영문 표기(원작 설정)
- 오프닝·엔딩 동영상

## 알려진 한계

- 타이틀·옵션·로드 화면, 이름 입력, 초반 대사, 상태 메뉴, 로딩 화면은 에뮬레이터로 확인했습니다. **게임오버, 지역 이름 표시, TV 설정, 아이템·고대 단어·마법 창, 게임 안 옵션 화면은 텍스처를 그린 결과만 확인했고 실제 게임 화면에서는 보지 못했습니다.**
- 게임을 끝까지 플레이해 보지는 않았습니다. 빌드는 모든 문자열이 원래 자리나 여유 공간에 들어가는지 검사합니다.
- 실기에서의 동작은 확인하지 못했습니다. 칸을 넘치거나 어긋난 문구가 있으면 이슈로 알려 주세요.

## 저장소 구성

| 경로 | 내용 |
| --- | --- |
| `tools/prepare.py` | 원본 디스크에서 빌드 입력 생성(파일 추출, 문자열 위치표에 원문 채우기, 번역 단위 분할) |
| `tools/build.py` | 전체 빌드(실행파일 문자열 재배치, 한글 글꼴, 사전, 그림 글자) 후 `--disc`로 트랙 5에 기록 |
| `tools/` | `gdfs.py`·`disc.py` GD-ROM 파일 읽기/제자리 쓰기(EDC/ECC), `kfont.py` 글꼴 칸 배정, `dictfmt.py` 사전 형식, `tex.py` 텍스처 코덱, `texpatch.py`·`texspec.py` 그림 글자, `export.py`·`exetext.py`·`mkbatches.py` 번역 단위 생성, `validate.py`·`dictlines.py` 번역 검사, `apply_release.py` 해시 검사 후 적용, `emu.py` 에뮬레이터 테스트 조작, `sh4dis.py` 분석용 SH-4 디스어셈블러 |
| `work/tr/out/*.json` | 번역. `script_*` 대사, `table_*` 실행파일 문자열, `dict_*` 사전(원문 없이 id로 연결) |
| `work/cand_offsets.json` | 실행파일 문자열 위치·길이·포인터 위치(원문 없음) |
| `work/fonts/` | (저장소에 없음) 갈무리 TTF를 두는 곳 |
| `docs/` | 기술 설명, 재빌드 방법, 글꼴 출처, 번역 지침 |

권리 관련 내용은 [RIGHTS.md](RIGHTS.md)를 참고하세요.
