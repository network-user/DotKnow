# =============================================================================
# Тема: Ghostscript
# Раздел: python/tools/pdf
# =============================================================================

# --- Пример 1: ---
# Пример 1. PS → PDF (классический ps2pdf)
import ghostscript
from pathlib import Path


def ps2pdf(src: str | Path, dst: str | Path) -> None:
    args = [
        "ps2pdf",                 # любое имя
        "-dNOPAUSE",
        "-dBATCH",
        "-dSAFER",
        "-sDEVICE=pdfwrite",
        f"-sOutputFile={dst}",
        str(src),
    ]
    ghostscript.Ghostscript(*args)


# Пример 2. Оптимизация / «перепечатка» PDF
"""
Ghostscript часто используют для уменьшения размера PDF (напр. для веб‑отдачи). Для этого применяют устройство 
pdfwrite и разные параметры качества. Общая идея та же, что в примере выше: создать новый PDF через Ghostscript
"""

def optimize_pdf(src: str | Path, dst: str | Path) -> None:
    args = [
        "pdfopt",
        "-dNOPAUSE",
        "-dBATCH",
        "-dSAFER",
        "-sDEVICE=pdfwrite",
        # типичный набор опций качества (могут подбираться под задачу)
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/ebook",  # пример предустановки качества/сжатия
        f"-sOutputFile={dst}",
        str(src),
    ]
    ghostscript.Ghostscript(*args)


# Пример 3. PDF → растровые изображения (страница = PNG)
"""
Ghostscript умеет рендерить PDF в изображения, достаточно сменить -sDEVICE и шаблон выходного файла 
(например, page-%03d.png). Модель вызова остаётся той же, что в документации: список аргументов с -sDEVICE=... 
и -sOutputFile=....
"""
from pathlib import Path
import ghostscript


def pdf_to_png(
    src: str | Path,
    out_pattern: str | Path = "page-%03d.png",
    dpi: int = 300,
) -> None:
    """
    Конвертирует PDF в PNG: page-001.png, page-002.png, ...
    """
    args = [
        "pdf2png",
        "-dNOPAUSE",
        "-dBATCH",
        "-dSAFER",
        f"-r{dpi}",          # разрешение
        "-sDEVICE=png16m",   # цветной PNG
        f"-sOutputFile={out_pattern}",
        str(src),
    ]
    ghostscript.Ghostscript(*args)

# Пример 4. Склейка нескольких PDF через Ghostscript
"""
Ghostscript тоже умеет сливать несколько PDF в один, если задать -sDEVICE=pdfwrite, выходной файл и несколько входных 
PDF. Вызов остаётся тем же ― список аргументов, как если бы вы вызывали CLI‑утилиту.
"""
from pathlib import Path
from typing import Iterable
import ghostscript


def merge_pdfs_with_gs(sources: Iterable[str | Path], dst: str | Path) -> None:
    src_list = [str(Path(s)) for s in sources]
    if not src_list:
        raise ValueError("no sources")

    args = [
        "mergepdf",
        "-dNOPAUSE",
        "-dBATCH",
        "-dSAFER",
        "-sDEVICE=pdfwrite",
        f"-sOutputFile={dst}",
        *src_list,
    ]
    ghostscript.Ghostscript(*args)
