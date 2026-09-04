"""El ile çekilmiş fotoğrafların OCR başarısını artırmak için basit ön işleme adımları."""

from PIL import Image, ImageOps


def gorseli_hazirla(gorsel: Image.Image, min_genislik: int = 1600) -> Image.Image:
    """Griye çevirir, kontrastı otomatik ayarlar ve küçük görüntüleri büyütür.

    Telefonla çekilen fotoğraflarda ışık/kontrast dengesizliği ve düşük
    çözünürlük, OCR doğruluğunu ciddi şekilde düşürür. Bu fonksiyon ağır bir
    kütüphaneye (ör. OpenCV) ihtiyaç duymadan basit ama etkili düzeltmeler
    uygular.
    """
    gorsel = gorsel.convert("L")
    gorsel = ImageOps.autocontrast(gorsel, cutoff=1)

    if gorsel.width < min_genislik:
        oran = min_genislik / gorsel.width
        yeni_boyut = (min_genislik, int(gorsel.height * oran))
        gorsel = gorsel.resize(yeni_boyut, Image.LANCZOS)

    return gorsel
