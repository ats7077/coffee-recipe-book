#!/usr/bin/env python3
"""recipes/*.json + notes/notes.json -> data.js (index.html이 읽는 파일)

사용법:  python3 scripts/build.py
- 필수 필드가 빠진 레시피가 있으면 어떤 파일의 어떤 필드인지 알려주고 실패한다.
- 표준 라이브러리만 사용한다.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECIPES = ROOT / "recipes"
NOTES = ROOT / "notes" / "notes.json"
OUT = ROOT / "data.js"

REQUIRED = ["id", "beanId", "beanName", "roastLevel", "rank", "intent", "title",
            "drippers", "settings", "steps"]
LEVELS = {"ultralight", "light", "medium", "dark"}
INTENTS = {"tea-like", "clarity", "sweetness", "aroma"}
POSITIONS = {"bright", "mid", "dark", ""}


def load_recipes():
    recipes, errors = [], []
    for path in sorted(RECIPES.glob("*.json")):
        try:
            r = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{path.name}: JSON 형식 오류 ({e})")
            continue
        if r.get("id") != path.stem:
            errors.append(f"{path.name}: id가 파일명과 달라요 (id={r.get('id')!r}, 파일명={path.stem!r})")
        missing = [k for k in REQUIRED if r.get(k) in (None, "", [])]
        if missing:
            errors.append(f"{path.name}: 필수 필드 누락 {missing}")
        if r.get("roastLevel") not in LEVELS:
            errors.append(f"{path.name}: roastLevel은 {sorted(LEVELS)} 중 하나여야 해요")
        if r.get("intent") not in INTENTS:
            errors.append(f"{path.name}: intent는 {sorted(INTENTS)} 중 하나여야 해요")
        if r.get("roastPosition", "") not in POSITIONS:
            errors.append(f"{path.name}: roastPosition은 bright/mid/dark 중 하나여야 해요")
        cv = r.get("colorValue")
        if cv is not None and not isinstance(cv, (int, float)):
            errors.append(f"{path.name}: colorValue는 숫자 또는 null이어야 해요")
        recipes.append(r)
    return recipes, errors


def load_notes(recipe_ids):
    if not NOTES.exists():
        return [], []
    try:
        notes = json.loads(NOTES.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [], [f"notes/notes.json: JSON 형식 오류 ({e})"]
    warnings = [f"notes.json: 레시피 {n.get('recipeId')!r}를 찾을 수 없어요 (노트는 유지)"
                for n in notes if n.get("recipeId") not in recipe_ids]
    return notes, warnings


def main():
    recipes, errors = load_recipes()
    if errors:
        print("빌드 실패:\n  " + "\n  ".join(errors), file=sys.stderr)
        sys.exit(1)
    notes, warnings = load_notes({r["id"] for r in recipes})
    for w in warnings:
        print("경고: " + w, file=sys.stderr)
    payload = (
        "// 자동 생성 파일 — 직접 고치지 말고 recipes/, notes/를 고친 뒤 build.py를 실행하세요.\n"
        f"window.RECIPES = {json.dumps(recipes, ensure_ascii=False)};\n"
        f"window.NOTES = {json.dumps(notes, ensure_ascii=False)};\n"
    )
    OUT.write_text(payload, encoding="utf-8")
    beans = len({r["beanId"] for r in recipes})
    print(f"data.js 생성: 레시피 {len(recipes)}개 · 원두 {beans}종 · 노트 {len(notes)}개")


if __name__ == "__main__":
    main()
