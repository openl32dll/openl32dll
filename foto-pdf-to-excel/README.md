# Foto/PDF → Excel

Elle telefonla çekilmiş **fotoğrafları (PNG/JPG)** ve **PDF** dosyalarını,
içindeki tabloyu OCR ile okuyup **tek komutla** bir Excel (`.xlsx`)
dosyasına aktaran basit bir araç.

- 📷 Fotoğraf ve 📄 PDF aynı komutla, tek elle kullanılır
- Her girdi dosyası (ve her PDF sayfası) çıktıda ayrı bir Excel sayfası olur
- Satır/sütun hizalaması, kelimelerin sayfadaki konumuna bakılarak otomatik tespit edilir
- Ek olarak bulut/ücretli bir servise ihtiyaç yoktur, tamamen bilgisayarınızda (offline) çalışır

## Kurulum

### 1. Tesseract-OCR'ı kurun

Bu araç metni okumak için [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract)
kullanır; bunun ayrıca sisteme kurulması gerekir (Python paketi tek başına yetmez).

- **Windows:** [UB-Mannheim Tesseract kurulum dosyası](https://github.com/UB-Mannheim/tesseract/wiki)
  ile kurun. Kurulum sırasında **"Turkish"** dil paketini de işaretleyin.
  Kurulumdan sonra Tesseract'ın klasörünü (ör. `C:\Program Files\Tesseract-OCR`)
  sistem `PATH` değişkenine eklediğinizden emin olun.
- **macOS:** `brew install tesseract tesseract-lang`
- **Linux (Debian/Ubuntu):** `sudo apt-get install tesseract-ocr tesseract-ocr-tur`

### 2. Python bağımlılıklarını kurun

```bash
cd foto-pdf-to-excel
pip install -r requirements.txt
```

## Kullanım

```bash
# Tek fotoğraf
python foto_to_excel.py fatura.jpg

# Çıktı dosyasını belirtmek
python foto_to_excel.py fatura.jpg -o fatura.xlsx

# PDF
python foto_to_excel.py rapor.pdf -o rapor.xlsx

# Birden fazla dosyayı (fotoğraf + PDF karışık) TEK komutla, tek Excel'e
python foto_to_excel.py sayfa1.png sayfa2.jpg rapor.pdf -o hepsi.xlsx
```

Her dosya (PDF ise her sayfası) çıktı Excel'inde ayrı bir sayfa (worksheet)
olarak yer alır; ilk satır otomatik olarak başlık gibi biçimlendirilir.

### Sık kullanılan seçenekler

| Seçenek | Açıklama |
|---|---|
| `-o, --output` | Çıktı Excel dosyasının adı (varsayılan: `sonuc.xlsx`) |
| `--dil` | OCR dili, Tesseract kodlarıyla (varsayılan: `tur+eng`) |
| `--serbest-metin` | Sütun tespiti yapmadan her satırı tek hücre olarak yazar (çizgisiz/karışık metinler için) |
| `--min-guven` | OCR güven eşiği 0-100 (varsayılan: `30`, gürültülü fotoğraflarda artırın) |
| `--dpi` | PDF sayfalarını görüntüye çevirirken kullanılacak çözünürlük (varsayılan: `300`) |
| `--baslik-yok` | İlk satırı başlık olarak biçimlendirme |
| `--on-isleme-yok` | Fotoğraf ön işleme (gri/kontrast/büyütme) adımlarını atla |
| `--debug-klasoru KLASOR` | OCR'ın hangi kelimeyi nerede bulduğunu gösteren kontrol görüntüsü kaydeder |

Tüm seçenekler için:

```bash
python foto_to_excel.py --help
```

## Daha iyi sonuç için fotoğraf çekme ipuçları

- Kağıdı düz bir zemine koyup **tam üstten**, gölgesiz ve net çekin.
- Yazı sayfaya göre çok küçük kalmasın; yakından çekin.
- Çok eğik/perspektifli fotoğraflarda sütun tespiti bozulabilir —
  bu durumda `--serbest-metin` ile satır satır çıktı alıp Excel'de
  elle sütunlara bölmek daha pratik olabilir.

## Nasıl çalışır?

1. **Girdi okuma** – PDF ise her sayfa `PyMuPDF` ile yüksek çözünürlüklü bir
   görüntüye çevrilir; fotoğraf ise doğrudan açılır.
2. **Ön işleme** – Griye çevirme, otomatik kontrast ve küçük görüntülerin
   büyütülmesiyle OCR doğruluğu artırılır (`--on-isleme-yok` ile kapatılabilir).
3. **OCR** – Tesseract, sayfadaki her kelimeyi metni ve piksel konumuyla
   (`sol, üst, genişlik, yükseklik`) birlikte döndürür.
4. **Tablo tespiti** – Kelimeler önce dikey konumuna göre **satırlara**,
   sonra aralarındaki boşluğa göre **hücrelere**, son olarak da tüm sayfadaki
   ortak hizalanma noktalarına göre **sütunlara** gruplanır
   (bkz. `foto_pdf_to_excel/tablo.py`).
5. **Excel'e yazma** – Elde edilen tablo, başlık satırı biçimlendirilmiş ve
   sütun genişlikleri otomatik ayarlanmış bir `.xlsx` dosyasına yazılır.

## Proje yapısı

```
foto-pdf-to-excel/
├── foto_to_excel.py           # Tek elle çalıştırılan giriş betiği
├── requirements.txt
├── foto_pdf_to_excel/
│   ├── cli.py                 # Komut satırı arayüzü
│   ├── ocr.py                 # Tesseract OCR + PDF->görüntü dönüşümü
│   ├── on_isleme.py           # Fotoğraf ön işleme (gri/kontrast/büyütme)
│   ├── tablo.py               # Kelimelerden satır/sütun tespiti (bağımsız, test edilebilir)
│   └── excel.py                # Tabloyu biçimlendirilmiş .xlsx dosyasına yazma
└── tests/
    └── test_tablo.py          # tablo.py için birim testleri (Tesseract gerektirmez)
```

## Testleri çalıştırma

`tablo.py` OCR/PDF kütüphanelerinden bağımsız olduğu için testler Tesseract
kurulu olmadan da çalışır:

```bash
python tests/test_tablo.py
# veya pytest kuruluysa:
pytest
```

## Bilinen sınırlamalar / gelecek geliştirmeler

- Sayfada **tek bir tablo** olduğu varsayılır; aynı sayfada birden fazla
  bağımsız tablo varsa sütunlar karışabilir.
- Eğik (perspektifli) fotoğraflarda otomatik düzeltme (deskew) yapılmaz;
  gerekirse fotoğrafı çekmeden önce düzeltin veya `--serbest-metin` kullanın.
- El yazısı desteklenmez (Tesseract yalnızca baskı/dijital yazıda güvenilirdir).
