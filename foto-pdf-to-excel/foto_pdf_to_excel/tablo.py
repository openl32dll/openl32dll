"""
OCR ile bulunan tek tek kelimeleri; satır ve sütunlara ayırıp bir tabloya
(2 boyutlu string listesine) dönüştüren saf Python mantığı.

Bu modül hiçbir OCR/PDF kütüphanesine bağımlı değildir; bu sayede Tesseract
kurulu olmayan ortamlarda bile birim testleriyle doğrulanabilir.
"""

from dataclasses import dataclass
from statistics import median
from typing import List


@dataclass
class Kelime:
    """Tesseract OCR çıktısındaki tek bir kelime ve konumu (piksel cinsinden)."""

    metin: str
    sol: int
    ust: int
    genislik: int
    yukseklik: int
    guven: float = 100.0

    @property
    def sag(self) -> int:
        return self.sol + self.genislik

    @property
    def alt(self) -> int:
        return self.ust + self.yukseklik

    @property
    def x_merkez(self) -> float:
        return self.sol + self.genislik / 2

    @property
    def y_merkez(self) -> float:
        return self.ust + self.yukseklik / 2


@dataclass
class Hucre:
    """Aynı satırda birbirine yakın kelimelerin birleşmesiyle oluşan bir tablo hücresi."""

    metin: str
    sol: int
    sag: int
    x_merkez: float


def satirlara_grupla(kelimeler: List[Kelime], tolerans_orani: float = 0.6) -> List[List[Kelime]]:
    """Kelimeleri dikey konumuna (y ekseni) göre satırlara ayırır.

    Fotoğraflarda satırlar tam düz olmayabileceğinden, kelimenin y-merkezi ile
    satırın ortalama y-merkezi arasındaki fark, ortalama kelime yüksekliğinin
    ``tolerans_orani`` katından küçükse aynı satıra dahil edilir.
    """
    if not kelimeler:
        return []

    sirali = sorted(kelimeler, key=lambda k: k.y_merkez)
    ort_yukseklik = median(k.yukseklik for k in sirali) or 1
    tolerans = ort_yukseklik * tolerans_orani

    satirlar: List[List[Kelime]] = []
    for kelime in sirali:
        eklendi = False
        for satir in satirlar:
            satir_y = sum(k.y_merkez for k in satir) / len(satir)
            if abs(kelime.y_merkez - satir_y) <= tolerans:
                satir.append(kelime)
                eklendi = True
                break
        if not eklendi:
            satirlar.append([kelime])

    satirlar.sort(key=lambda s: sum(k.y_merkez for k in s) / len(s))
    for satir in satirlar:
        satir.sort(key=lambda k: k.sol)
    return satirlar


def satiri_hucrelere_ayir(satir: List[Kelime], bosluk_orani: float = 1.4) -> List[Hucre]:
    """Aynı satırdaki kelimeleri, aralarındaki yatay boşluğa göre hücrelere birleştirir.

    İki kelime arasındaki boşluk, ortalama kelime yüksekliğinin ``bosluk_orani``
    katından küçükse (ör. "Elma" ve "Suyu" gibi) aynı hücrede, büyükse
    (ör. bir sonraki sütuna geçildiyse) ayrı hücrelerde sayılır.
    """
    ort_yukseklik = median(k.yukseklik for k in satir) or 1
    esik = ort_yukseklik * bosluk_orani

    gruplar: List[List[Kelime]] = [[satir[0]]]
    for onceki, kelime in zip(satir, satir[1:]):
        bosluk = kelime.sol - onceki.sag
        if bosluk > esik:
            gruplar.append([kelime])
        else:
            gruplar[-1].append(kelime)

    hucreler = []
    for grup in gruplar:
        metin = " ".join(k.metin for k in grup).strip()
        sol = min(k.sol for k in grup)
        sag = max(k.sag for k in grup)
        hucreler.append(Hucre(metin=metin, sol=sol, sag=sag, x_merkez=(sol + sag) / 2))
    return hucreler


def sutun_merkezlerini_bul(
    tum_hucreler: List[Hucre], ort_yukseklik: float, esik_orani: float = 0.6
) -> List[float]:
    """Sayfadaki ortak sütun konumlarını bulur.

    Kümeleme, hücrenin x-merkezi yerine SOL kenarına göre yapılır: bir
    sütundaki hücreler (ör. "Adet" başlığı ile altındaki "3" değeri) farklı
    uzunlukta olsa da genelde aynı sol kenardan başlar; merkeze göre
    kümelemek kısa/uzun kelimeleri hatalı biçimde farklı sütunlara ayırabilir.
    """
    if not tum_hucreler:
        return []

    sol_kenarlar = sorted(h.sol for h in tum_hucreler)
    esik = max(ort_yukseklik * esik_orani, 10)

    kumeler: List[List[float]] = [[sol_kenarlar[0]]]
    for sol in sol_kenarlar[1:]:
        if sol - kumeler[-1][-1] <= esik:
            kumeler[-1].append(sol)
        else:
            kumeler.append([sol])

    return [sum(kume) / len(kume) for kume in kumeler]


def en_yakin_sutun(sol: float, sutun_konumlari: List[float]) -> int:
    return min(range(len(sutun_konumlari)), key=lambda i: abs(sutun_konumlari[i] - sol))


def tablo_olustur(kelimeler: List[Kelime], serbest_metin: bool = False) -> List[List[str]]:
    """OCR'dan gelen kelime listesini satır/sütun tablosuna (2 boyutlu string listesi) çevirir.

    Parametreler
    ------------
    kelimeler:
        :class:`Kelime` nesnelerinin listesi (konum bilgisiyle birlikte).
    serbest_metin:
        ``True`` verilirse sütun tespiti yapılmaz; her satır tek hücre olarak
        yazılır. Çizgisiz/düzensiz metinler (fiş yerine serbest not gibi) için
        kullanılır.
    """
    satirlar = satirlara_grupla(kelimeler)
    if not satirlar:
        return []

    if serbest_metin:
        return [[" ".join(k.metin for k in satir)] for satir in satirlar]

    satir_hucreleri = [satiri_hucrelere_ayir(satir) for satir in satirlar]
    tum_hucreler = [h for satir in satir_hucreleri for h in satir]

    ort_yukseklik = median(k.yukseklik for k in kelimeler) or 20
    sutun_merkezleri = sutun_merkezlerini_bul(tum_hucreler, ort_yukseklik=ort_yukseklik)

    tablo: List[List[str]] = []
    for satir in satir_hucreleri:
        satir_dizisi = [""] * len(sutun_merkezleri)
        for hucre in satir:
            idx = en_yakin_sutun(hucre.sol, sutun_merkezleri)
            if satir_dizisi[idx]:
                satir_dizisi[idx] += " " + hucre.metin
            else:
                satir_dizisi[idx] = hucre.metin
        tablo.append(satir_dizisi)

    return tablo
