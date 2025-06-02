# BoozeKing (지목왕)

BoozeKing은 술자리에서 즐길 수 있는 랜덤 지목 게임입니다. 참가자들의 이름을 등록하고, 랜덤으로 선택된 질문에 대답할 사람을 룰렛으로 정하는 방식으로 진행됩니다.

![BoozeKing Game](https://github.com/yourusername/boozeking/raw/main/screenshots/game.png)

## 게임 특징

- 참가자 이름 등록 및 관리
- 랜덤 질문 생성
- 시각적인 룰렛 애니메이션으로 참가자 선택
- 10초 타이머로 긴장감 조성
- 간단하고 직관적인 UI

## 게임 진행 방식

1. 메인 메뉴에서 '플레이어 등록' 버튼을 클릭하여 참가자 이름을 등록합니다.
2. 최소 2명 이상의 참가자가 등록되면 '게임 시작' 버튼이 활성화됩니다.
3. 게임이 시작되면 랜덤 질문이 표시됩니다.
4. '룰렛 돌리기' 버튼을 클릭하여 대답할 사람을 선택합니다.
5. 선택된 참가자는 10초 안에 질문에 답해야 합니다.
6. 시간 내에 답변을 완료하면 성공, 시간이 초과되면 벌칙을 받습니다.
7. '다음 라운드' 버튼을 클릭하여 게임을 계속 진행합니다.

## 설치 및 실행 방법

### 요구 사항

- Python 3.6 이상
- Pygame 2.0.0 이상

### 설치

1. 저장소를 클론합니다:

```bash
git clone https://github.com/yourusername/boozeking.git
cd boozeking
```

2. 가상 환경을 생성하고 활성화합니다:

```bash
# 가상 환경 생성
python -m venv venv

# 가상 환경 활성화
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. 필요한 패키지를 설치합니다:

```bash
pip install -r requirements.txt
```

### 실행

게임을 실행하려면 다음 명령어를 사용합니다:

```bash
python boozeking/main.py
```

## 개발 정보

### 프로젝트 구조

```
boozeking/
├── main.py              # 게임 메인 실행 파일
├── requirements.txt     # 필요한 패키지 목록
├── assets/              # 이미지, 사운드 등 리소스 파일
│   ├── images/
│   └── sounds/
├── data/                # 게임 데이터 파일
│   └── players.json     # 플레이어 정보 저장
└── game/                # 게임 모듈
    ├── __init__.py
    ├── ui.py            # UI 관련 기능
    ├── question.py      # 질문 관리
    ├── roulette.py      # 룰렛 기능
    └── manager.py       # 게임 상태 관리
```

### 커스터마이징

- `game/question.py` 파일에서 질문 목록을 수정하여 새로운 질문을 추가할 수 있습니다.
- `game/ui.py` 파일에서 UI 디자인을 수정할 수 있습니다.
- `game/manager.py` 파일에서 타이머 시간 등 게임 규칙을 조정할 수 있습니다.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

---

*이 프로젝트는 Amazon Q를 활용하여 개발되었습니다.*
