# Adana Ocakbaşı — Restoran Web Sitesi

Adana Ocakbaşı restoranı için hazırlanmış, tek sayfa (single-page) tanıtım sitesi.
Sadece HTML, CSS ve vanilla JavaScript ile yazılmıştır — herhangi bir kurulum veya bağımlılık gerektirmez.

## İçerik / Bölümler

- **Anasayfa (Hero)** — restoran tanıtımı ve öne çıkan aksiyonlar
- **Hakkımızda** — restoranın hikayesi ve çalışma saatleri
- **Menü** — kategorilere ayrılmış (Başlangıçlar, Ana Yemekler, Izgaralar, İçecekler, Tatlılar) ve fiyatlandırılmış yemek listesi, sekme (tab) geçişli
- **Galeri** — yemek ve mekân fotoğrafları
- **Yorumlar** — müşteri değerlendirmeleri
- **Rezervasyon** — tarih/saat/kişi sayısı seçimli rezervasyon formu (istemci tarafı doğrulama ile)
- **İletişim** — adres, telefon, e-posta ve harita

## Nasıl çalıştırılır

Herhangi bir build aracı gerekmez, tarayıcıda doğrudan açılabilir:

```bash
open adana-ocakbasi/index.html
# veya basit bir local server ile:
cd adana-ocakbasi && python3 -m http.server 8000
```

## Dosya yapısı

```
adana-ocakbasi/
├── index.html      # Tüm sayfa içeriği
├── css/style.css   # Stiller (tema: köz/ateş renk paleti)
├── js/script.js    # Sekme geçişleri, mobil menü, form, sticky header
└── README.md
```

## Notlar

- İçerikteki adres, telefon ve fiyatlar örnek/demo amaçlıdır; gerçek işletme bilgileriyle güncellenmelidir.
- Galeri ve hero görselleri Unsplash üzerinden harici olarak yüklenmektedir; isterseniz `images/` klasörü açıp kendi fotoğraflarınızla değiştirebilirsiniz.
