# 커피 레시피 북 저장소

이 저장소는 나의 브루잉 레시피 북이다. GitHub Pages로 배포되어 휴대폰에서 열람한다.
대화는 한국어로 한다.

## 구조

- `recipes/<id>.json` — 레시피 1개 = 파일 1개. 스키마와 작성 규칙은
  `.claude/skills/coffee-brewing-recipe-builder/SKILL.md`의 Step 7을 따른다.
- `notes/notes.json` — 브루 노트 배열 `{id, recipeId, rating, memo, date}`.
- `scripts/build.py` — recipes/, notes/를 검증하고 `data.js`를 만든다.
- `scripts/add_notes.py` — 표준 입력의 노트 JSON(추가·수정·삭제)을 `notes/notes.json`에 반영한다.
- `data.js` — 자동 생성. 직접 고치지 않는다.
- `index.html` — 레시피 북 화면(검색·필터·타이머·노트). 외부 서버 없이 `data.js`만 읽는다.

## 작업 규칙

1. 레시피 요청(원두 사진/정보 + 로스트 일자)이 오면 `coffee-brewing-recipe-builder`
   스킬로 설계하고, 결과를 `recipes/`에 JSON으로 저장한다.
2. 레시피를 만들기 전에 관련 노트(`notes/notes.json`)와 기존 레시피를 읽고 반영한다.
3. 레시피나 노트를 바꾼 뒤에는 항상 `python3 scripts/build.py`를 실행하고,
   성공하면 커밋하고 바로 push한다(사용자가 "항상 push"로 지정 — 확인받지 않는다).
4. 브루 노트는 레시피 북의 "GitHub로 보내기"로 이슈가 열리면
   `.github/workflows/brew-note.yml`이 `notes/notes.json`에 자동 반영·커밋한다.
   그래서 **작업을 시작할 때와 push 전에 `git pull --rebase`를 먼저 한다**
   (`data.js`가 충돌하면 `python3 scripts/build.py`로 다시 만든다).
   사용자가 "노트 복사" 내용을 직접 붙여 넣으면 `python3 scripts/add_notes.py`에
   넘겨 추가한 뒤 build → 커밋 → push.
5. 드리퍼·필터 정식 이름 목록은 `SKILL.md`, `scripts/build.py`(`FILTERS`),
   `index.html`(`OWNED_DRIPPERS`, `OWNED_FILTERS`) 세 곳에 있다. 장비가 늘면 함께 고친다.
6. `index.html`을 고치면 휴대폰 폭(390px)에서 깨지지 않는지 확인한다.
