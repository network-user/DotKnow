# =============================================================================
# Тема: Qpdf и pikepdf
# Раздел: python/tools/pdf
# =============================================================================

# pikepdf — это удобная Python-обертка над C++ библиотекой qpdf.
# Все примеры используют pikepdf.

from pikepdf import Pdf, Encryption
from pathlib import Path
import subprocess

# --- Пример 1: Копирование PDF «как есть» ---
# Открывает PDF и сохраняет его копию. Полезно для нормализации структуры файла.
with Pdf.open("input.pdf") as pdf:
    pdf.save("output_copy.pdf")


# --- Пример 2: Создание пустого PDF файла ---
# Создает новый PDF-документ с одной пустой страницей.
pdf = Pdf.new()
pdf.add_blank_page()
pdf.save("blank_page.pdf")


# --- Пример 3: Разделение PDF на несколько файлов ---
def split_pdf(src: str, dst_first: str, dst_rest: str) -> None:
    """
    Разделяет PDF-файл на два: один с первой страницей, другой с остальными.
    """
    with Pdf.open(src) as pdf:
        # Первый файл — только первая страница
        first = Pdf.new()
        first.pages.append(pdf.pages[0])
        first.save(dst_first)

        # Второй файл — остальные страницы
        rest = Pdf.new()
        for page in pdf.pages[1:]:
            rest.pages.append(page)
        rest.save(dst_rest)

# Пример вызова функции:
# split_pdf("report.pdf", "report_title.pdf", "report_body.pdf")


# --- Пример 4: Прямой вызов qpdf через subprocess ---
# Демонстрирует, как можно вызывать утилиту qpdf напрямую из Python.
# Требуется, чтобы qpdf был установлен в системе и доступен в PATH.
# Команда для расшифровки файла:
try:
    subprocess.run(
        ["qpdf", "--decrypt", "encrypted_input.pdf", "decrypted_output.pdf"],
        check=True
    )
except FileNotFoundError:
    print("Ошибка: утилита qpdf не найдена. Убедитесь, что она установлена и доступна в PATH.")
except subprocess.CalledProcessError as e:
    print(f"Ошибка при выполнении qpdf: {e}")

# Пример 5
def merge_pdfs(sources: list[str | Path], dst: str | Path) -> None:
    """
    Склеить несколько PDF
    Слияние реализуется добавлением страниц разных документов в один Pdf.
    pages.extend принимает любую итерируемую коллекцию страниц, поэтому можно «влить» все страницы другого
    документа за один вызов.
    """
    result = Pdf.new()

    for src in sources:
        with Pdf.open(src) as pdf:
            result.pages.extend(pdf.pages)

    result.save(dst)


merge_pdfs(
    ["title.pdf", "chapter1.pdf", "chapter2.pdf"],
    "book.pdf",
)

# Пример 6
def rotate_all(src: str, dst: str, angle: int = 180) -> None:
    """ Поворот и перестановка страниц. """
    with pikepdf.Pdf.open(src) as pdf:
        for page in pdf.pages:
            page.rotate(angle, relative=True)
        pdf.save(dst)



rotate_all("scan.pdf", "scan_rotated.pdf", angle=90)



# Пример 7
def reorder_pages(src: str, dst: str, order: list[int]) -> None:
    """
    order — новый порядок индексов страниц, например [2, 0, 1]
    """
    with Pdf.open(src) as pdf:
        new_pdf = Pdf.new()
        for i in order:
            new_pdf.pages.append(pdf.pages[i])
        new_pdf.save(dst)


# Пример 8
def encrypt_pdf(src: str, dst: str, password: str) -> None:
    """
    Шифрование и снятие пароля через pikepdf (qpdf под капотом)
    pikepdf умеет шифровать PDF при сохранении, используя объект Encryption.
    Пример: зашифровать PDF паролем пользователя/владельца:
    """
    with Pdf.open(src) as pdf:
        enc = Encryption(
            user=password,
            owner=password,
            R=4,  # уровень шифрования, в примере используется 128‑битный режим
        )
        pdf.save(dst, encryption=enc)


encrypt_pdf("confidential.pdf", "confidential_encrypted.pdf", "s3cr3t")

# Пример 9
def remove_password(src: str, dst: str, password: str) -> None:
    """ Убрать пароль. """
    pdf = pikepdf.open(src, password=password)[web:16]
    pdf.save(dst)

# Часть 2. Взаимодейсвтие через субпроцессы

import subprocess
from pathlib import Path


def run_qpdf(args: list[str]) -> None:
    """Обёртка над qpdf, выбрасывает исключение при ошибке."""
    completed = subprocess.run(["qpdf", *args], check=True, text=True, capture_output=True)
    if completed.stdout:
        print(completed.stdout)
    if completed.stderr:
        print(completed.stderr, file=sys.stderr)




def extract_pages(src: str, dst: str, page_spec: str) -> None:
    """
    Разбить PDF по диапазонам страниц
    page_spec в синтаксисе qpdf: "1-5", "1,3,7", "1-3,7-9" и т.п.
    """
    run_qpdf([src, "--pages", ".", page_spec, "--", dst])

extract_pages("multipage.pdf", "first_five.pdf", "1-5")


# Склеить несколько PDF в один
def merge_with_qpdf(parts: list[str], dst: str) -> None:
    """qpdf позволяет создать «пустой» документ и наполнить его страницами других файлов"""
    run_qpdf(["--empty", "--pages", *parts, "--", dst])


merge_with_qpdf(["a.pdf", "b.pdf", "c.pdf"], "merged.pdf")

# Шифрование PDF через qpdf
def encrypt_with_qpdf(src: str, dst: str, password: str) -> None:
    run_qpdf([
        "--encrypt",
        password,
        password,
        "--modify=none",  # запретить изменения
        "256",  # длина ключа
        "--",
        src,
        dst,
    ])


# Оптимизация, сжатие файла
def compress_pdf(src: str, dst: str) -> None:
    run_qpdf([
        "--compress-streams=y",
        "--object-streams=generate",
        src,
        dst,
    ])
