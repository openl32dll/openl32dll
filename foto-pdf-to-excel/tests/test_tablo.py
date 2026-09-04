"""
tablo.py içindeki satır/sütun tespit mantığının birim testleri.

Bu testler Tesseract veya PyMuPDF gerektirmez; sentetik Kelime nesneleriyle
çalışır. Hem ``pytest`` ile hem de doğrudan ``python tests/test_tablo.py``
ile çalıştırılabilir.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from foto_pdf_to_excel.tablo import Kelime, satirlara_grupla, tablo_olustur


def _ornek_fatura_kelimeleri():
    """3 satır x 3 sütunluk basit bir fatura tablosunu simüle eder."""
    return [
        Kelime("Ürün", 10, 10, 60, 20),
        Kelime("Adet", 300, 12, 50, 20),
        Kelime("Fiyat", 500, 11, 60, 20),
        Kelime("Elma", 10, 42, 60, 20),
        Kelime("3", 310, 44, 15, 20),
        Kelime("12.50", 500, 43, 55, 20),
        Kelime("Armut", 10, 74, 65, 20),
        Kelime("5", 310, 75, 15, 20),
        Kelime("9.75", 500, 76, 50, 20),
    ]


def test_satirlara_grupla_uc_satir_olusturur():
    satirlar = satirlara_grupla(_ornek_fatura_kelimeleri())
    assert len(satirlar) == 3
    assert [k.metin for k in satirlar[0]] == ["Ürün", "Adet", "Fiyat"]


def test_hafif_egik_satirlar_yine_de_ayni_satirda_sayilir():
    # Elle çekilmiş fotoğraflarda satırlar birkaç piksel eğik olabilir.
    kelimeler = [
        Kelime("A", 10, 10, 20, 20),
        Kelime("B", 100, 13, 20, 20),  # 3px aşağıda, tolerans içinde
    ]
    satirlar = satirlara_grupla(kelimeler)
    assert len(satirlar) == 1


def test_tablo_olustur_uc_satir_uc_sutun_dogru_hizalar():
    tablo = tablo_olustur(_ornek_fatura_kelimeleri())
    assert len(tablo) == 3
    assert all(len(satir) == 3 for satir in tablo)
    assert tablo[0] == ["Ürün", "Adet", "Fiyat"]
    assert tablo[1] == ["Elma", "3", "12.50"]
    assert tablo[2] == ["Armut", "5", "9.75"]


def test_ayni_hucredeki_yakin_kelimeler_birlesir():
    kelimeler = [
        Kelime("Elma", 10, 10, 40, 20),
        Kelime("Suyu", 55, 10, 40, 20),  # "Elma" ile arada küçük boşluk -> aynı hücre
        Kelime("2", 400, 10, 15, 20),
    ]
    tablo = tablo_olustur(kelimeler)
    assert tablo == [["Elma Suyu", "2"]]


def test_serbest_metin_modu_her_satiri_tek_hucre_yapar():
    tablo = tablo_olustur(_ornek_fatura_kelimeleri(), serbest_metin=True)
    assert len(tablo) == 3
    assert tablo[0] == ["Ürün Adet Fiyat"]
    assert tablo[1] == ["Elma 3 12.50"]
    assert tablo[2] == ["Armut 5 9.75"]


def test_bos_kelime_listesi_bos_tablo_dondurur():
    assert tablo_olustur([]) == []


if __name__ == "__main__":
    hatalar = 0
    for ad, fonksiyon in list(globals().items()):
        if ad.startswith("test_") and callable(fonksiyon):
            try:
                fonksiyon()
                print(f"OK   {ad}")
            except AssertionError as e:
                hatalar += 1
                print(f"FAIL {ad}: {e}")
    if hatalar:
        print(f"\n{hatalar} test başarısız oldu.")
        sys.exit(1)
    print("\nTüm testler geçti.")
