#!/usr/bin/env python3
"""
Tek elle, tek komutla çalışan giriş betiği.

Fotoğraf (PNG/JPG) veya PDF dosyalarındaki tabloları OCR ile okuyup Excel'e
(.xlsx) aktarır — kurulum gerektirmeden doğrudan çalıştırılabilir.

Kullanım
--------
    python foto_to_excel.py fatura.jpg
    python foto_to_excel.py fatura.jpg -o fatura.xlsx
    python foto_to_excel.py sayfa1.png sayfa2.png rapor.pdf -o hepsi.xlsx

Tüm seçenekler için:
    python foto_to_excel.py --help
"""

import sys

from foto_pdf_to_excel.cli import main

if __name__ == "__main__":
    sys.exit(main())
