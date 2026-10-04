# 커피 레시피 북 저장소

이 저장소는 나의 브루잉 레시피 북이다. GitHub Pages로 배포되어 휴대폰에서 열람한다.
대화는 한국어로 한다.

## 구조

- `recipes/<id>.json` — 레시피 1개 = 파일 1개. 스키마와 작성 규칙은
  `.claude/skills/coffee-brewing-recipe-builder/SKILL.md`의 Step 7을 따른다.
- `notes/notes.json` — 브루 노트 배열 `{id, recipeId, rating, memo, date}`.
- `scripts/build.py` — recipes/, notes/를 검증하고 `data.js`를 만든다.
- `data.js` — 자동 생성. 직접 고치지 않는다.
- `index.html` — 레시피 북 화면(검색·필터·타이머·노트). 외부 서버 없이 `data.js`만 읽는다.

## 작업 규칙

1. 레시피 요청(원두 사진/정보 + 로스트 일자)이 오면 `coffee-brewing-recipe-builder`
   스킬로 설계하고, 결과를 `recipes/`에 JSON으로 저장한다.
2. 레시피를 만들기 전에 관련 노트(`notes/notes.json`)와 기존 레시피를 읽고 반영한다.
3. 레시피나 노트를 바꾼 뒤에는 항상 `python3 scripts/build.py`를 실행하고,
   성공하면 커밋하고 바로 push한다(사용자가 "항상 push"로 지정 — 확인받지 않는다).
4. 사용자가 레시피 북의 "노트 복사" 내용을 붙여 넣으면 `notes/notes.json`에
   중복 id를 건너뛰며 추가한 뒤 build → 커밋 → push.
5. `index.html`을 고치면 휴대폰 폭(390px)에서 깨지지 않는지 확인한다.
