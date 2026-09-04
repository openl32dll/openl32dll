"""Fotoğraf (PNG/JPG) ve PDF dosyalarını tek komutla Excel'e çeviren komut satırı aracı.

Örnekler
--------
    python foto_to_excel.py fatura.jpg
    python foto_to_excel.py fatura.jpg -o fatura.xlsx
    python foto_to_excel.py sayfa1.png sayfa2.png rapor.pdf -o hepsi.xlsx
"""

import argparse
import os
import sys
from typing import List, Tuple

from PIL import Image

from .excel import Tablo, tablolari_excele_yaz
from .ocr import gorselden_kelimeler_al, pdf_sayfalarini_goruntuye_cevir
from .on_isleme import gorseli_hazirla
from .tablo import tablo_olustur

DESTEKLENEN_GORSEL_UZANTILARI = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp"}


def _goruntuyu_tabloya_cevir(
    gorsel: Image.Image, dil: str, min_guven: int, on_isle: bool, serbest_metin: bool,
    debug_klasoru, ad: str,
) -> Tablo:
    islenmis = gorseli_hazirla(gorsel) if on_isle else gorsel
    kelimeler = gorselden_kelimeler_al(islenmis, dil=dil, min_guven=min_guven)

    if debug_klasoru:
        _debug_goruntusu_kaydet(islenmis, kelimeler, debug_klasoru, ad)

    tablo = tablo_olustur(kelimeler, serbest_metin=serbest_metin)
    print(f"  -> {len(kelimeler)} kelime bulundu, {len(tablo)} satır oluşturuldu.")
    return tablo


def _debug_goruntusu_kaydet(gorsel: Image.Image, kelimeler, klasor: str, ad: str) -> None:
    from PIL import ImageDraw

    os.makedirs(klasor, exist_ok=True)
    renkli = gorsel.convert("RGB")
    cizim = ImageDraw.Draw(renkli)
    for kelime in kelimeler:
        cizim.rectangle([kelime.sol, kelime.ust, kelime.sag, kelime.alt], outline="red", width=2)
    yol = os.path.join(klasor, f"{ad}_debug.png")
    renkli.save(yol)
    print(f"  -> Kontrol görüntüsü kaydedildi: {yol}")


def _dosyayi_isle(
    yol: str, dil: str, min_guven: int, dpi: int, on_isle: bool, serbest_metin: bool, debug_klasoru,
) -> List[Tuple[str, Tablo]]:
    uzanti = os.path.splitext(yol)[1].lower()
    ad = os.path.splitext(os.path.basename(yol))[0]
    sonuclar: List[Tuple[str, Tablo]] = []

    if uzanti == ".pdf":
        print(f"[PDF] {yol} okunuyor...")
        gorseller = pdf_sayfalarini_goruntuye_cevir(yol, dpi=dpi)
        for i, gorsel in enumerate(gorseller, start=1):
            sayfa_adi = f"{ad}_s{i}" if len(gorseller) > 1 else ad
            print(f" Sayfa {i}/{len(gorseller)}")
            tablo = _goruntuyu_tabloya_cevir(gorsel, dil, min_guven, on_isle, serbest_metin, debug_klasoru, sayfa_adi)
            sonuclar.append((sayfa_adi, tablo))
    elif uzanti in DESTEKLENEN_GORSEL_UZANTILARI:
        print(f"[Foto] {yol} okunuyor...")
        gorsel = Image.open(yol)
        tablo = _goruntuyu_tabloya_cevir(gorsel, dil, min_guven, on_isle, serbest_metin, debug_klasoru, ad)
        sonuclar.append((ad, tablo))
    else:
        print(f"[UYARI] Desteklenmeyen dosya türü, atlanıyor: {yol}", file=sys.stderr)

    return sonuclar


def olustur_ayristirici() -> argparse.ArgumentParser:
    ayristirici = argparse.ArgumentParser(
        prog="foto_to_excel",
        description=(
            "Fotoğraf (PNG/JPG) ve PDF dosyalarındaki tabloları OCR ile okuyup "
            "tek bir Excel (.xlsx) dosyasına aktarır."
        ),
    )
    ayristirici.add_argument("girdiler", nargs="+", help="Fotoğraf (.jpg/.png/...) ve/veya PDF dosya yolları")
    ayristirici.add_argument("-o", "--output", default="sonuc.xlsx", help="Çıktı Excel dosyası (varsayılan: sonuc.xlsx)")
    ayristirici.add_argument("--dil", default="tur+eng", help="Tesseract dil kodu (varsayılan: tur+eng)")
    ayristirici.add_argument("--min-guven", type=int, default=30, help="OCR güven eşiği, 0-100 (varsayılan: 30)")
    ayristirici.add_argument("--dpi", type=int, default=300, help="PDF sayfalarını görüntüye çevirirken kullanılacak çözünürlük (varsayılan: 300)")
    ayristirici.add_argument("--serbest-metin", action="store_true", help="Sütun tespiti yapma; her satırı tek hücre olarak yaz (çizgisiz/düzensiz metinler için)")
    ayristirici.add_argument("--baslik-yok", action="store_true", help="İlk satırı başlık olarak biçimlendirme")
    ayristirici.add_argument("--on-isleme-yok", action="store_true", help="Fotoğraf ön işleme adımlarını (gri/kontrast/büyütme) atla")
    ayristirici.add_argument("--debug-klasoru", help="Tespit edilen kelime kutucuklarını gösteren kontrol görüntülerinin kaydedileceği klasör")
    return ayristirici


def main(argv=None) -> int:
    ayristirici = olustur_ayristirici()
    args = ayristirici.parse_args(argv)

    sayfalar: dict = {}
    for yol in args.girdiler:
        if not os.path.isfile(yol):
            print(f"[HATA] Dosya bulunamadı: {yol}", file=sys.stderr)
            continue
        try:
            for sayfa_adi, tablo in _dosyayi_isle(
                yol, args.dil, args.min_guven, args.dpi,
                not args.on_isleme_yok, args.serbest_metin, args.debug_klasoru,
            ):
                sayfalar[sayfa_adi] = tablo
        except RuntimeError as hata:
            print(f"[HATA] {yol}: {hata}", file=sys.stderr)
            return 1

    if not sayfalar:
        print("[HATA] İşlenecek geçerli bir dosya bulunamadı.", file=sys.stderr)
        return 1

    tablolari_excele_yaz(sayfalar, args.output, ilk_satir_baslik=not args.baslik_yok)
    print(f"\nTamamlandı: {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
