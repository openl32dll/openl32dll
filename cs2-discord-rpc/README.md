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
4. (İsteğe bağlı ama önerilir) **Rich Presence → Art Assets** kısmına harita
   görselleri yükle. Görsellere haritanın GSI adıyla aynı anahtarı ver
   (ör. `de_dust2`, `de_mirage`, `de_inferno`...) ve varsayılan için bir de
   `cs2_logo` adında genel bir CS2 logosu ekle. Görsel eklemezsen Discord
   büyük resmi boş gösterir, metinler yine de çalışır.

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
