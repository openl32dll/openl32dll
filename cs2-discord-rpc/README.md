# CS2 Discord Rich Presence

Counter-Strike 2 oynarken Discord profilinde sadece "Counter-Strike 2 oynuyor"
yazısı yerine; **hangi haritada**, **hangi modda** (Rekabetçi/Premier, Yoldaş
(Wingman), Basit (Casual), Deathmatch, Silah Yarışı, Yıkım, Ko-op, Antrenman,
Özel Oyun, vb.) ve **kaçıncı roundda** olduğunu gösteren bir araç.

Round kavramı olmayan modlarda (Deathmatch, Silah Yarışı gibi) round yerine
o anki frag/ölüm sayın gösterilir.

## Nasıl çalışır?

CS2, Valve'ın **Game State Integration (GSI)** özelliği sayesinde oyun içi
durumu (harita, mod, round, skor, bomba durumu...) belirli aralıklarla
bilgisayarındaki bir HTTP adresine gönderebilir. Bu script:

1. `http://127.0.0.1:3000` adresinde küçük bir yerel sunucu açar.
2. CS2'den gelen bu veriyi okur.
3. `pypresence` kütüphanesi ile Discord masaüstü uygulamasına iletir.

## Kurulum

### 1) Discord Uygulaması oluştur

Discord, üçüncü parti scriptlerin "Rich Presence" gösterebilmesi için bir
uygulama (Client ID) oluşturmanı ister:

1. https://discord.com/developers/applications adresine git.
2. **New Application** ile yeni bir uygulama oluştur, adını istersen
   `Counter-Strike 2` koy.
3. Sol menüden **OAuth2 / General** sayfasında görünen **Application ID**
   (Client ID) değerini kopyala.

Harita görselleri için Developer Portal'a ayrıca bir şey yüklemene gerek
yok: `assets/maps/` klasöründeki küçük harita ikonları bu repodan doğrudan
Discord'a "external image URL" olarak veriliyor (Discord Rich Presence,
yüklenmiş bir asset key kadar dışarıdan bir görsel URL'sini de kabul
ediyor). Yani script'i çalıştırır çalıştırmaz her harita için otomatik
olarak görsel görünür.

### 2) GSI config dosyasını CS2'ye tanıt

`gamestate_integration_discordrpc.cfg` dosyasını CS2'nin şu klasörüne kopyala:

```
<Steam kurulum dizini>\steamapps\common\Counter-Strike Global Offensive\game\csgo\cfg\
```

(CS2, CS:GO'nun devamı olduğu için klasör adı hâlâ `csgo`dur.)

Dosyayı kopyaladıktan sonra CS2'yi (açıksa) yeniden başlat.

### 3) Bağımlılıkları kur

```bash
cd cs2-discord-rpc
pip install -r requirements.txt
```

### 4) Script'i çalıştır

Discord masaüstü uygulamasının açık olduğundan emin ol, sonra:

```bash
# Windows (PowerShell)
$env:DISCORD_CLIENT_ID="BURAYA_CLIENT_ID"; python cs2_discord_rpc.py

# Linux / macOS
DISCORD_CLIENT_ID=BURAYA_CLIENT_ID python cs2_discord_rpc.py
```

CS2'ye girip bir maça başladığında Discord profilinde harita, mod ve round
bilgisi otomatik olarak görünmeye başlar. Ana menüdeyken veya oyundan
çıktığında durum otomatik olarak güncellenir/temizlenir.

## Harita görselleri

`assets/maps/` klasöründe her ana harita için (Dust II, Mirage, Inferno,
Nuke, Overpass, Vertigo, Ancient, Anubis, Train, Cache, Office, Italy,
Agency, Wingman haritaları, Aim Map) küçük birer PNG rozet + genel bir
`cs2_logo.png` bulunuyor. Bunlar Valve'ın oyun içi ekran görüntüleri değil,
bu repo için üretilmiş basit ikonlardır (telif sorunu yaşamamak için).

- Script, GSI'dan gelen harita adını bu klasördeki dosya adlarıyla
  eşleştirip şu adresten görseli çekiyor:
  `https://raw.githubusercontent.com/openl32dll/openl32dll/main/cs2-discord-rpc/assets/maps/<harita>.png`
  Bu adres, sadece bu değişiklik `main` dalına birleştikten (merge)
  sonra çalışır; PR henüz birleşmediyse test için
  `MAP_IMAGE_BASE_URL` ortam değişkenini kendi branch'ine
  (`.../<branch-adı>/cs2-discord-rpc/assets/maps`) göre ayarlayabilirsin.
- Elimizde ikonu olmayan bir harita gelirse (yeni çıkan bir harita ya da
  community server haritası) otomatik olarak `cs2_logo.png`'ye düşer.
- Kendi görsellerini (gerçek harita ekran görüntüsü gibi) kullanmak
  istersen: `assets/maps/<harita_kodu>.png` dosyasını kendi görselinle
  değiştirmen yeterli — kod tarafında hiçbir şey değiştirmene gerek yok.
- Yeni bir harita eklemek / ikonları yeniden üretmek istersen:
  `assets/generate_map_icons.py` script'ini (Pillow gerektirir) düzenleyip
  tekrar çalıştırabilirsin.

## Desteklenen modlar

| GSI mod anahtarı      | Discord'da görünen ad     | Round gösterimi |
|------------------------|----------------------------|------------------|
| `competitive`           | Rekabetçi                  | Round X/24       |
| `scrimcomp5v5`          | Premier                    | Round X/24       |
| `scrimcomp2v2`          | Yoldaş (Wingman)            | Round X/16       |
| `casual`                | Basit                      | Round X          |
| `deathmatch`            | Deathmatch                 | Frag / ölüm      |
| `gungameprogressive`    | Silah Yarışı (Arms Race)   | Frag / ölüm      |
| `gungametrbomb`         | Yıkım (Demolition)         | Round X          |
| `skirmish`              | Uçan Keşif Nişancısı        | Round X          |
| `cooperative`           | Ko-op Görev                | Frag / ölüm      |
| `training`              | Antrenman                  | Frag / ölüm      |
| `custom`                | Özel Oyun                  | Round X          |

Listede olmayan yeni bir mod eklenirse script "Bilinmeyen Mod" olarak
gösterir; `cs2_discord_rpc.py` içindeki `MODE_INFO` sözlüğüne yeni satır
ekleyerek kolayca genişletilebilir.

> **Not:** `competitive`/`scrimcomp5v5` için 24, `scrimcomp2v2` için 16
> round varsayılan matchmaking ayarlarına (MR12 / MR8) göre verilmiştir.
> Özel sunucularda (community server) bu limit farklıysa sadece geçerli
> round numarası gösterilir.
