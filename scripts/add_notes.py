#!/usr/bin/env python3
"""표준 입력으로 받은 브루 노트를 notes/notes.json에 추가한다.

사용법:  python3 scripts/add_notes.py < notes.txt
- 입력은 JSON 배열(또는 객체 1개). 앞뒤에 다른 글이 있어도 ```json 블록 안이면 읽는다
  (레시피 북의 "GitHub로 보내기"가 만드는 이슈 본문, "노트 복사" 내용 모두 해당).
- 이미 있는 id는 건너뛴다. 형식이 틀리면 아무것도 쓰지 않고 실패한다.
- 추가한 뒤 scripts/build.py를 실행해야 data.js에 반영된다.
"""
import json
import re
import sys
from pathlib import Path

NOTES = Path(__file__).resolve().parent.parent / "notes" / "notes.json"


def parse(text):
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    data = json.loads(m.group(1) if m else text[text.index("["):] if "[" in text else text)
    if isinstance(data, dict):
        data = [data]
    notes = []
    for n in data:
        rating = n.get("rating") or 0
        if not (isinstance(n.get("id"), str) and n["id"] and isinstance(n.get("recipeId"), str)
                and n["recipeId"] and isinstance(rating, int) and 0 <= rating <= 5):
            raise ValueError(f"노트 형식이 틀려요: {n!r}")
        # 알려진 필드만 남긴다 (이슈 본문은 외부 입력)
        notes.append({"id": n["id"][:60], "recipeId": n["recipeId"][:120], "rating": rating,
                      "memo": str(n.get("memo") or "")[:2000], "date": str(n.get("date") or "")[:20]})
    return notes


def main():
    new = parse(sys.stdin.buffer.read().decode("utf-8"))
    notes = json.loads(NOTES.read_text(encoding="utf-8")) if NOTES.exists() else []
    seen = {n["id"] for n in notes}
    added = []
    for n in new:
        if n["id"] not in seen:
            seen.add(n["id"])
            added.append(n)
    NOTES.write_text(json.dumps(notes + added, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"노트 {len(added)}개 추가 · 중복 {len(new) - len(added)}개 건너뜀")


if __name__ == "__main__":
    main()
