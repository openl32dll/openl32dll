# Adana Ocakbaşı — Restoran Web Sitesi

Adana Ocakbaşı restoranı için hazırlanmış, canlı ve fotoğraf/GIF ağırlıklı bir tanıtım sitesi (Tavuk Dünyası, Günaydın gibi zincir restoran sitelerinden ilham alınarak tasarlandı). Sadece HTML, CSS ve vanilla JavaScript ile yazılmıştır — herhangi bir kurulum veya bağımlılık gerektirmez.

## İçerik / Bölümler

- **Üst bar + Header** — sipariş hattı, sticky navigasyon
- **Kayan promo şeridi (marquee)** — kampanya/duyuru anonsu
- **Anasayfa (Hero)** — büyük görsel kompozisyon, "Günün Fırsatı" rozet GIF'i, alev GIF'i, duman GIF'i
- **Kampanyalar** — indirimli menü kartları (eski/yeni fiyat, rozet)
- **Menü** — kategorilere ayrılmış (Başlangıçlar, Ana Yemekler, Izgaralar, İçecekler, Tatlılar), her kategoriye özel fotoğraflı banner + dönen şiş (kebap) GIF'i, fotoğraflı ürün kartları, sekme (tab) geçişli
- **Neden Biz** — ikon kartlar + çalışma saatleri şeridi
- **Galeri** — fotoğraf ızgarası + köz dumanı GIF'i
- **Yorumlar** — müşteri değerlendirmeleri
- **Rezervasyon** — form (istemci tarafı doğrulama ile, demo amaçlı — gerçek gönderim için kendi backend'inize bağlayın)
- **İletişim** — adres, telefon, e-posta, konum kartı
- **Mobilde sabit alt bar** — "Ara" / "Sipariş Ver" hızlı erişim

## GIF'ler

`images/` klasöründe, sitede kullanılan 4 adet özel üretilmiş (stok değil, bu proje için Python/Pillow ile çizilmiş) animasyonlu GIF bulunur:

| Dosya | Kullanım |
|---|---|
| `flame.gif` | Titreyen alev — hero ve rezervasyon bölümünde dekoratif |
| `smoke.gif` | Yükselen köz dumanı — hero arka planı ve galeri |
| `badge-firsat.gif` | Nabız gibi atan "Günün Fırsatı" rozeti — hero |
| `skewer-spin.gif` | Dönen şiş kebap — menü kategori banner'ları |

Bu GIF'ler harici bir servise bağımlı değildir, doğrudan repo içindedir; isterseniz `images/` klasöründeki dosyaları kendi GIF'lerinizle (aynı dosya adlarıyla) değiştirebilirsiniz.

## Fotoğraflar

Yemek/mekân fotoğrafları Unsplash üzerinden harici olarak yüklenir. Bir fotoğraf herhangi bir sebeple yüklenemezse (ağ engeli, silinen görsel vb.) `js/script.js` içindeki `imgFallback()` fonksiyonu otomatik olarak turuncu/kırmızı gradyanlı bir yer tutucu + ilgili emoji gösterir, böylece kırık görsel ikonu hiç görünmez.

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
├── index.html         # Tüm sayfa içeriği
├── css/style.css       # Stiller (tema: canlı kırmızı/altın sarısı, "Baloo 2" + "Nunito")
├── js/script.js        # Sekme geçişleri, mobil menü, form, görsel fallback, sticky header
├── images/              # Özel üretilmiş GIF'ler (flame, smoke, badge-firsat, skewer-spin)
└── README.md
```

## Notlar

- İçerikteki adres, telefon, fiyatlar ve kampanyalar örnek/demo amaçlıdır; gerçek işletme bilgileriyle güncellenmelidir.
- Rezervasyon formu şu an sadece bir "gönderildi" mesajı gösterir; gerçek gönderim için kendi backend/e-posta servisinize bağlamanız gerekir.
