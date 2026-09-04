"""Tesseract OCR ve PDF -> görüntü dönüşümü için yardımcı fonksiyonlar.

Bu modüldeki içe aktarmalar (pytesseract, fitz) fonksiyon içinde yapılır;
böylece paket, bu opsiyonel bağımlılıklar kurulu olmadan da import edilebilir
(ör. ``tablo.py`` içindeki mantığı test ederken).
"""

from typing import List

from PIL import Image

from .tablo import Kelime


def gorselden_kelimeler_al(gorsel: Image.Image, dil: str = "tur+eng", min_guven: int = 30) -> List[Kelime]:
    """Tesseract OCR kullanarak görüntüdeki kelimeleri ve piksel konumlarını çıkarır.

    Sisteminizde Tesseract-OCR kurulu olmalıdır (bkz. proje README'si).
    """
    try:
        import pytesseract
        from pytesseract import Output
    except ImportError as hata:
        raise RuntimeError(
            "pytesseract kurulu değil. Kurmak için: pip install pytesseract"
        ) from hata

    try:
        veri = pytesseract.image_to_data(gorsel, lang=dil, output_type=Output.DICT)
    except pytesseract.TesseractNotFoundError as hata:
        raise RuntimeError(
            "Tesseract-OCR programı bulunamadı. Lütfen sisteminize Tesseract-OCR'ı "
            "kurun (Windows için: https://github.com/UB-Mannheim/tesseract/wiki) "
            "ve PATH'e ekleyin."
        ) from hata

    kelimeler: List[Kelime] = []
    for i in range(len(veri["text"])):
        metin = veri["text"][i].strip()
        if not metin:
            continue
        try:
            guven = float(veri["conf"][i])
        except (ValueError, TypeError):
            guven = -1
        if guven < min_guven:
            continue
        kelimeler.append(
            Kelime(
                metin=metin,
                sol=veri["left"][i],
                ust=veri["top"][i],
                genislik=veri["width"][i],
                yukseklik=veri["height"][i],
                guven=guven,
            )
        )
    return kelimeler


def pdf_sayfalarini_goruntuye_cevir(pdf_yolu: str, dpi: int = 300) -> List[Image.Image]:
    """PDF dosyasının her sayfasını yüksek çözünürlüklü bir PIL görüntüsüne çevirir.

    PyMuPDF (fitz) kullanır; bu sayede ayrıca poppler kurulumuna gerek kalmaz.
    """
    try:
        import pymupdf as fitz  # PyMuPDF
    except ImportError:
        try:
            import fitz  # eski pymupdf sürümleri (< 1.24) bu adla kurulur
        except ImportError as hata:
            raise RuntimeError(
                "PyMuPDF kurulu değil. Kurmak için: pip install pymupdf"
            ) from hata

    goruntuler: List[Image.Image] = []
    olcek = dpi / 72
    matris = fitz.Matrix(olcek, olcek)

    with fitz.open(pdf_yolu) as belge:
        for sayfa in belge:
            pixmap = sayfa.get_pixmap(matrix=matris)
            goruntu = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
            goruntuler.append(goruntu)

    return goruntuler
