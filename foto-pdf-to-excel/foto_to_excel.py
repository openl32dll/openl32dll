#!/usr/bin/env python3
"""
Tek elle, tek komutla çalışan giriş betiği.

Fotoğraf (PNG/JPG) veya PDF dosyalarındaki tabloları OCR ile okuyup Excel'e
(.xlsx) aktarır.

İlk çalıştırmadan önce bu klasörde bağımlılıkları kurmanız gerekir:
    pip install -r requirements.txt
(Windows'ta birden fazla Python kuruluysa: py -m pip install -r requirements.txt)

Ayrıca Tesseract-OCR programının sisteme kurulu olması gerekir; bkz. README.md.

Kullanım
--------
    python foto_to_excel.py fatura.jpg
    python foto_to_excel.py fatura.jpg -o fatura.xlsx
    python foto_to_excel.py sayfa1.png sayfa2.png rapor.pdf -o hepsi.xlsx

Tüm seçenekler için:
    python foto_to_excel.py --help
"""

import sys

try:
    from foto_pdf_to_excel.cli import main
except ImportError as hata:
    print(
        f"[HATA] Gerekli bir Python paketi eksik ({hata.name}).\n"
        "Bu klasörde önce bağımlılıkları kurmanız gerekiyor:\n\n"
        "    pip install -r requirements.txt\n\n"
        "Windows'ta birden fazla Python sürümü kuruluysa şunu deneyin:\n\n"
        "    py -m pip install -r requirements.txt\n",
        file=sys.stderr,
    )
    sys.exit(1)

if __name__ == "__main__":
    sys.exit(main())
