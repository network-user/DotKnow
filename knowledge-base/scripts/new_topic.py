"""
Скрипт для создания новой темы в репозитории знаний.

Использование:
    python scripts/new_topic.py --lang python --section basics --topic closures

Создаёт:
    python/basics/closures/
        closures.md
        closures.py
        meta.json

И обновляет:
    _meta/topics_index.json
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent

MD_TEMPLATE = """---
title: "{title}"
difficulty: medium
tags: [{slug}]
added: "{today}"
last_reviewed: null
---

## Что это такое

TODO: описание темы

## Ключевые концепции

- TODO

## Частые ошибки

1. TODO

## Вопросы для самопроверки

- TODO
"""

PY_TEMPLATE = """# =============================================================================
# Тема: {title}
# Раздел: {lang}/{section}
# =============================================================================

# --- Пример 1: ---
# TODO: добавить примеры кода
"""


def create_topic(lang: str, section: str, slug: str) -> None:
    title = slug.replace("_", " ").title()
    today = date.today().isoformat()
    topic_path = ROOT / lang / section / slug

    if topic_path.exists():
        print(f"[!] Тема уже существует: {topic_path}")
        sys.exit(1)

    topic_path.mkdir(parents=True)

    (topic_path / f"{slug}.md").write_text(
        MD_TEMPLATE.format(title=title, slug=slug, today=today),
        encoding="utf-8"
    )

    (topic_path / f"{slug}.py").write_text(
        PY_TEMPLATE.format(title=title, lang=lang, section=section),
        encoding="utf-8"
    )

    meta = {
        "title": title,
        "slug": slug,
        "section": f"{lang}/{section}",
        "difficulty": "medium",
        "tags": [slug],
        "added": today,
        "last_reviewed": None,
        "quiz_types": ["theory", "code_writing"]
    }
    (topic_path / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    index_path = ROOT / "_meta" / "topics_index.json"
    index: list = json.loads(index_path.read_text(encoding="utf-8")) if index_path.exists() else []

    index.append({
        "slug": slug,
        "path": f"{lang}/{section}/{slug}",
        "title": title,
        "difficulty": "medium",
        "tags": [slug],
        "quiz_types": ["theory", "code_writing"]
    })

    index_path.parent.mkdir(exist_ok=True)
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[OK] Тема создана: {topic_path}")
    print(f"[OK] topics_index.json обновлён ({len(index)} тем)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Создать новую тему в Knowledge Base")
    parser.add_argument("--lang",    required=True, help="Язык: python, javascript, sql")
    parser.add_argument("--section", required=True, help="Раздел: basics, oop, async ...")
    parser.add_argument("--topic",   required=True, help="Slug темы: closures, generators ...")
    args = parser.parse_args()
    create_topic(args.lang, args.section, args.topic)


if __name__ == "__main__":
    main()