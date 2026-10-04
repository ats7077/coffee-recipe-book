# 나의 브루잉 레시피 북

원두, 로스터, 나라, 농장, 품종, 프로세스, 드리퍼, 로스팅 단계, 색도(#숫자), 취향으로
레시피를 검색하고, 추출 타이머와 브루 노트를 쓰는 휴대폰용 레시피 북입니다.
레시피는 Claude Code가 만들어 `recipes/`에 쌓습니다.

## 처음 한 번: 설정

1. 이 폴더를 원하는 위치에 풀고 터미널에서 이동합니다.
2. GitHub에 새 저장소(Public)를 만들고 연결합니다.
   ```bash
   git init
   git add .
   git commit -m "init: coffee recipe book"
   git branch -M main
   git remote add origin https://github.com/<내 계정>/coffee-recipe-book.git
   git push -u origin main
   ```
3. GitHub 저장소 → Settings → Pages → Source: "Deploy from a branch",
   Branch: `main` / `/ (root)` → Save.
4. 잠시 뒤 표시되는 주소(`https://<내 계정>.github.io/coffee-recipe-book/`)를
   휴대폰 브라우저로 열고 "홈 화면에 추가"를 누릅니다.

## 스킬

`.claude/skills/coffee-brewing-recipe-builder/`에 스킬이 들어 있어서, 이 폴더에서
Claude Code를 실행하면 자동으로 인식됩니다. 다른 폴더에서도 쓰고 싶으면
`~/.claude/skills/`에 복사하세요.

## 평소 사용

- **새 원두**: 이 폴더에서 `claude` 실행 → 원두 사진/정보와 로스트 일자를 주고
  "레시피 만들어줘". Claude Code가 `recipes/`에 저장하고 빌드·커밋합니다.
  push하면 1~2분 뒤 휴대폰 레시피 북에 나타납니다.
- **브루 노트**: 레시피를 열고 별점·메모를 저장하면 GitHub 이슈 작성 화면이 열립니다.
  거기서 Submit을 누르면 GitHub Actions가 `notes/notes.json`에 반영하고, 1~2분 뒤
  모든 기기에서 보입니다(휴대폰 브라우저에 GitHub 로그인 필요). 저장소를 옮기면
  `index.html`의 `REPO`를 고치세요. 보내지 못한 노트는 그 기기에 남아 있고, 화면 위
  "GitHub로 보내기"로 다시 보내거나 "노트 복사"로 Claude Code에 붙여 넣을 수 있습니다.
- **직접 수정**: `recipes/*.json`을 고친 뒤 `python3 scripts/build.py` 실행.

## 로컬에서 보기

`python3 scripts/build.py` 후 `index.html`을 브라우저로 열면 됩니다(서버 불필요).
