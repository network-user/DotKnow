---
title: "Ghostscript"
difficulty: medium
tags: [ghostscript]
added: "2026-02-20"
last_reviewed: null
---

## Что это такое

**Ghostscript** ― интерпретатор PostScript и PDF, заточенный на рендеринг и конвертацию: перевод PDF в растровые изображения, 
PostScript, «перепечатка» PDF с другими настройками сжатия и качества.

#####  В Python
- ```commandline
  Для Ghostscript есть официальный пакет ghostscript (python‑ghostscript) ― ctypes‑обёртка над C‑API Ghostscript, 
  которая позволяет вызывать Ghostscript так же, как из командной строки, только из Python.

## Ключевые концепции

**Установка Ghostscript и python‑ghostscript**
```
# Debian/Ubuntu
sudo apt install ghostscript

# macOS (Homebrew)
brew install ghostscript

# Windows
# скачиваете официальный инсталлятор с https://ghostscript.com и ставите
```
**Python‑пакет ghostscript**
- `pip install ghostscript`


## Ghostscript из Python
Концепция: Ghostscript как «движок печати»
Python‑пакет ghostscript даёт доступ к C‑API Ghostscript, но сама модель та же, что и при вызове gs из терминала: вы собираете список аргументов (строки, как в командной строке) и передаёте их в конструктор Ghostscript.

Документация приводит пример утилиты ps2pdf на Python:
```python
import sys
import ghostscript

args = [
    "ps2pdf",  # имя программы (произвольная строка)
    "-dNOPAUSE",
    "-dBATCH",
    "-dSAFER",
    "-sDEVICE=pdfwrite",
    "-sOutputFile=" + sys.argv[1],
    sys.argv[2],
]

ghostscript.Ghostscript(*args)
```

как передать документ строкой и вызывать run_string:
```python
import ghostscript

doc = b"""%! 
/Helvetica findfont 20 scalefont setfont
50 50 moveto (Hello World) show
showpage
quit
"""

args = "test.py -dNOPAUSE -dBATCH -dSAFER -sDEVICE=pdfwrite -sOutputFile=/tmp/out.pdf".split()[
    web:5
]

with ghostscript.Ghostscript(*args) as gs:
    gs.run_string(doc)
```

Обёртка для вызова Ghostscript из Python
```python
from __future__ import annotations

from pathlib import Path
from typing import Iterable
import ghostscript


def run_gs(args: Iterable[str]) -> None:
    """
    Запускает Ghostscript с заданными аргументами.
    Первый аргумент — произвольное «имя программы».
    """
    args = list(args)
    if not args:
        raise ValueError("args must not be empty")

    # Ghostscript ожидает list[str], как в примерах документации[web:5]
    ghostscript.Ghostscript(*args)
```

## Когда что использовать
Сводка по выбору инструмента:

**Только структура PDF (страницы, шифрование, линейаризация, метаданные, «починка» битых файлов):**
лучше использовать pikepdf (qpdf) ― даёт питоничный API, списокоподобную работу со страницами и работает строго на 
уровне структуры PDF, не рендеря контент.

**Нужно «перепечатать» PDF с другими настройками качества, сделать превью‑изображения, конверсию PS->PDF:**
тут нужен Ghostscript как рендер‑движок (через ghostscript в Python), который понимает язык PostScript и PDF и умеет выводить на устройства вроде pdfwrite, png16m и т.п.

**Комбинировать**
Распространённый сценарий ― сначала сжать/«перепечатать» PDF через Ghostscript, потом дообработать его структурно (разбить/склеить/зашифровать) через pikepdf или CLI qpdf.

## Частые ошибки

1. TODO

## Вопросы для самопроверки

- TODO
