"""
cs2_discord_rpc.py
------------------
Counter-Strike 2 oynarken Discord'da özel bir "Rich Presence" (oyun durumu)
gösterir: hangi haritada olduğun, kaçıncı roundda olduğun ve hangi oyun
modunda olduğun (Rekabetçi / Premier, Yoldaş (Wingman), Basit (Casual),
Deathmatch, Silah Yarışı, Yıkım, vb.).

Nasıl çalışır?
    1) CS2, Valve'ın "Game State Integration" (GSI) özelliği sayesinde
       oyun içi durumu bir HTTP isteğiyle yerel bilgisayarına gönderebilir.
       Bunun için `gamestate_integration_discordrpc.cfg` dosyasını CS2'nin
       config klasörüne kopyalaman gerekiyor (bkz. README.md).
    2) Bu script, o isteği karşılamak için yerelde küçük bir HTTP sunucusu
       açar (varsayılan: http://127.0.0.1:3000).
    3) Gelen veriyi (harita, mod, round, skor, bomba durumu vb.) okuyup
       `pypresence` kütüphanesiyle Discord masaüstü uygulamasına iletir.

Kurulum:
    pip install -r requirements.txt

Kullanım:
    DISCORD_CLIENT_ID=xxxxxxxxxxxxxxxxxx python cs2_discord_rpc.py

Discord Client ID nasıl alınır, GSI dosyası nereye konur -> README.md
"""

from __future__ import annotations

import json
import logging
import os
import threading
import time
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Optional

try:
    from pypresence import Presence
    from pypresence.exceptions import DiscordNotFound, PipeClosed
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "pypresence kütüphanesi bulunamadı. Kurmak için:\n"
        "    pip install -r requirements.txt"
    ) from exc


# --------------------------------------------------------------------------
# Ayarlar
# --------------------------------------------------------------------------

# Discord Developer Portal'da oluşturduğun uygulamanın Client ID'si.
# https://discord.com/developers/applications -> New Application -> General
# Ortam değişkeni olarak vermek istersen: DISCORD_CLIENT_ID
DISCORD_CLIENT_ID = os.environ.get("DISCORD_CLIENT_ID", "PUT_YOUR_DISCORD_CLIENT_ID_HERE")

# CS2'nin GSI verisini göndereceği yerel adres/port.
# gamestate_integration_discordrpc.cfg dosyasındaki "uri" ile eşleşmeli.
GSI_HOST = "127.0.0.1"
GSI_PORT = 3000

# Aynı durum değişmediği sürece Discord'a en fazla bu sıklıkta güncelleme
# gönderilir (Discord IPC'yi gereksiz yere yormamak için).
MIN_UPDATE_INTERVAL_SECONDS = 4.0

# Oyuncudan hiç veri gelmezse bu süre sonunda durum temizlenir
# (oyun kapatıldı / CS2'den çıkıldı olarak yorumlanır).
STALE_TIMEOUT_SECONDS = 20.0

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("cs2-discord-rpc")


# --------------------------------------------------------------------------
# CS2 oyun modları
#
# CS2'nin GSI çıktısındaki "map.mode" alanı, oyuncunun içinde bulunduğu
# oyun moduna göre değişir. Aşağıdaki tablo, bilinen tüm mod anahtarlarını
# görünen isimlere ve moda özgü davranışlara (round sayılıp sayılmayacağı,
# varsayılan maksimum round) eşler.
#
# Not: "max_rounds" değerleri CS2'nin standart matchmaking ayarlarına göre
# varsayılan değerlerdir (ör. Rekabetçi/Premier MR12 -> 24 round, Yoldaş
# MR8 -> 16 round). Özel sunucularda (custom/community server) bu limitler
# farklı olabilir; bilinmiyorsa sadece geçerli round gösterilir.
# --------------------------------------------------------------------------

@dataclass
class ModeInfo:
    label: str          # Discord'da gösterilecek Türkçe mod adı
    has_rounds: bool     # Bu modda "round" kavramı var mı?
    max_rounds: Optional[int] = None  # Varsayılan maksimum round (varsa)


MODE_INFO: dict[str, ModeInfo] = {
    # Rekabetçi / Premier (ikisi de GSI'da "competitive" olarak gelebilir)
    "competitive":        ModeInfo("Rekabetçi", True, 24),
    "scrimcomp5v5":       ModeInfo("Premier", True, 24),
    # Yoldaş (Wingman) 2v2
    "scrimcomp2v2":       ModeInfo("Yoldaş (Wingman)", True, 16),
    # Basit / Gündelik
    "casual":             ModeInfo("Basit", True, None),
    # Deathmatch: round yok, sürekli respawn + skor tablosu var
    "deathmatch":         ModeInfo("Deathmatch", False),
    # Silah Yarışı (Arms Race)
    "gungameprogressive": ModeInfo("Silah Yarışı", False),
    # Yıkım (Demolition)
    "gungametrbomb":      ModeInfo("Yıkım", True, None),
    # Uçan Keşif Nişancısı / diğer "skirmish" tipi modlar
    "skirmish":           ModeInfo("Uçan Keşif Nişancısı", True, None),
    # Co-op Strike / Guardian gibi işbirlikçi modlar
    "cooperative":        ModeInfo("Ko-op Görev", False),
    # Antrenman
    "training":           ModeInfo("Antrenman", False),
    # Özel oyun / community sunucular
    "custom":             ModeInfo("Özel Oyun", True, None),
    # Tehlike Bölgesi (battle royale, eski CS:GO modu)
    "survival":           ModeInfo("Tehlike Bölgesi", False),
}

DEFAULT_MODE = ModeInfo("Bilinmeyen Mod", True, None)


def mode_info_for(mode_key: Optional[str]) -> ModeInfo:
    if not mode_key:
        return DEFAULT_MODE
    return MODE_INFO.get(mode_key, DEFAULT_MODE)


# --------------------------------------------------------------------------
# Harita isimleri
#
# GSI, harita adını "de_dust2" gibi teknik kodlarla gönderir. Bunları daha
# okunaklı isimlere çeviriyoruz; listede olmayan bir harita gelirse ön eki
# atıp baş harfleri büyültülmüş haliyle gösteriyoruz (ör. "de_newmap" ->
# "Newmap").
# --------------------------------------------------------------------------

MAP_DISPLAY_NAMES = {
    "de_dust2": "Dust II",
    "de_mirage": "Mirage",
    "de_inferno": "Inferno",
    "de_nuke": "Nuke",
    "de_overpass": "Overpass",
    "de_vertigo": "Vertigo",
    "de_ancient": "Ancient",
    "de_anubis": "Anubis",
    "de_train": "Train",
    "de_cache": "Cache",
    "cs_office": "Office",
    "cs_italy": "Italy",
    "cs_agency": "Agency",
    "de_shortdust": "Short Dust (Wingman)",
    "de_lake": "Lake (Wingman)",
    "de_stmarc": "St. Marc (Wingman)",
    "de_grail": "Grail (Wingman)",
    "aim_map": "Aim Map",
}


def display_map_name(raw_name: Optional[str]) -> str:
    if not raw_name:
        return "Bilinmeyen Harita"
    if raw_name in MAP_DISPLAY_NAMES:
        return MAP_DISPLAY_NAMES[raw_name]
    # "de_", "cs_", "aim_" gibi ön ekleri temizleyip düzgün göster.
    for prefix in ("de_", "cs_", "aim_", "gd_", "ar_"):
        if raw_name.startswith(prefix):
            return raw_name[len(prefix):].replace("_", " ").title()
    return raw_name.replace("_", " ").title()


# --------------------------------------------------------------------------
# Paylaşılan durum: GSI sunucusu bu nesneyi günceller, sunum (presence)
# döngüsü de buradan okuyarak Discord'a gönderir.
# --------------------------------------------------------------------------

@dataclass
class SharedState:
    lock: threading.Lock = field(default_factory=threading.Lock)
    payload: Optional[dict] = None
    last_seen: float = 0.0

    def update(self, payload: dict) -> None:
        with self.lock:
            self.payload = payload
            self.last_seen = time.monotonic()

    def snapshot(self) -> tuple[Optional[dict], float]:
        with self.lock:
            return self.payload, self.last_seen


state = SharedState()


# --------------------------------------------------------------------------
# GSI HTTP sunucusu: CS2'den gelen POST isteklerini karşılar.
# --------------------------------------------------------------------------

class GSIHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):  # noqa: A002 - BaseHTTPRequestHandler API
        # Varsayılan gürültülü erişim loglarını sustur.
        pass

    def do_POST(self) -> None:
        try:
            length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(length) if length else b""
            payload = json.loads(raw_body.decode("utf-8")) if raw_body else {}
        except (ValueError, json.JSONDecodeError) as exc:
            log.warning("Geçersiz GSI verisi alındı: %s", exc)
            self.send_response(400)
            self.end_headers()
            return

        state.update(payload)
        self.send_response(200)
        self.end_headers()


def run_gsi_server() -> ThreadingHTTPServer:
    server = ThreadingHTTPServer((GSI_HOST, GSI_PORT), GSIHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    log.info("GSI sunucusu dinliyor: http://%s:%d", GSI_HOST, GSI_PORT)
    return server


# --------------------------------------------------------------------------
# GSI verisinden Discord'a gösterilecek "details" / "state" metinlerini
# üreten mantık.
# --------------------------------------------------------------------------

def build_presence_fields(payload: dict) -> Optional[dict]:
    """GSI payload'ından Discord Rich Presence alanlarını üretir.

    Oyuncu ana menüdeyse ya da veri eksikse None döner (bu durumda
    presence temizlenir).
    """
    player = payload.get("player") or {}
    map_info = payload.get("map") or {}
    round_info = payload.get("round") or {}

    activity = player.get("activity")
    if activity is not None and activity != "playing":
        # Ana menüde / metin girişinde -> oyun içi bilgi gösterecek bir şey yok.
        return {
            "details": "Ana menüde geziniyor",
            "state": "Counter-Strike 2",
            "large_image": "cs2_logo",
            "large_text": "Counter-Strike 2",
        }

    map_name_raw = map_info.get("name")
    mode_key = map_info.get("mode")
    mode = mode_info_for(mode_key)
    map_name = display_map_name(map_name_raw)

    phase = map_info.get("phase")  # warmup / live / intermission / gameover
    if phase == "warmup":
        details = f"🗺️ {map_name} · {mode.label}"
        state_text = "Isınma turu"
    elif phase == "gameover":
        details = f"🗺️ {map_name} · {mode.label}"
        state_text = "Maç bitti"
    else:
        team_ct = map_info.get("team_ct") or {}
        team_t = map_info.get("team_t") or {}
        ct_score = team_ct.get("score", 0)
        t_score = team_t.get("score", 0)

        details = f"🗺️ {map_name} · {mode.label}"

        if mode.has_rounds:
            current_round = map_info.get("round")
            # GSI round bilgisi 0'dan başlar; insan tarafı için +1.
            round_display = (current_round + 1) if isinstance(current_round, int) else None
            round_text = f"Round {round_display}" if round_display else "Round -"
            if mode.max_rounds:
                round_text += f"/{mode.max_rounds}"
            state_text = f"{round_text} · CT {ct_score} - {t_score} T"
        else:
            # Round kavramı olmayan modlar (Deathmatch, Silah Yarışı, vb.):
            # round yerine kişisel skor/kill bilgisini gösteriyoruz.
            match_stats = player.get("match_stats") or {}
            kills = match_stats.get("kills", 0)
            deaths = match_stats.get("deaths", 0)
            state_text = f"{kills} frag / {deaths} ölüm"

        if round_info.get("bomb") == "planted":
            state_text += " · 💣 Bomba döşendi"

    large_image = map_name_raw if map_name_raw else "cs2_logo"

    return {
        "details": details,
        "state": state_text,
        "large_image": large_image,
        "large_text": map_name,
    }


def state_key(fields: Optional[dict]) -> tuple:
    if fields is None:
        return ()
    return (fields.get("details"), fields.get("state"), fields.get("large_image"))


# --------------------------------------------------------------------------
# Ana döngü: Discord IPC bağlantısını kurar/canlı tutar ve GSI durumundaki
# değişiklikleri Discord'a yansıtır.
# --------------------------------------------------------------------------

def connect_discord() -> Presence:
    if DISCORD_CLIENT_ID == "PUT_YOUR_DISCORD_CLIENT_ID_HERE":
        raise SystemExit(
            "DISCORD_CLIENT_ID ayarlanmamış. README.md içindeki adımları izleyerek\n"
            "kendi Discord uygulamanı oluştur ve Client ID'sini bu script'e ver\n"
            "(ortam değişkeni: DISCORD_CLIENT_ID)."
        )
    rpc = Presence(DISCORD_CLIENT_ID)
    rpc.connect()
    log.info("Discord'a bağlanıldı (client_id=%s).", DISCORD_CLIENT_ID)
    return rpc


def main() -> None:
    run_gsi_server()

    rpc: Optional[Presence] = None
    last_sent_key: tuple = ("__init__",)
    last_sent_time = 0.0
    cleared_for_stale = True
    start_time = time.time()

    while True:
        try:
            if rpc is None:
                rpc = connect_discord()

            payload, last_seen = state.snapshot()
            now = time.monotonic()
            is_stale = payload is None or (now - last_seen) > STALE_TIMEOUT_SECONDS

            if is_stale:
                if not cleared_for_stale:
                    rpc.clear()
                    log.info("CS2'den veri gelmiyor, Discord durumu temizlendi.")
                    cleared_for_stale = True
                    last_sent_key = ()
                time.sleep(1.0)
                continue

            cleared_for_stale = False
            fields = build_presence_fields(payload)
            key = state_key(fields)

            enough_time_passed = (time.time() - last_sent_time) >= MIN_UPDATE_INTERVAL_SECONDS
            if fields and key != last_sent_key and enough_time_passed:
                rpc.update(
                    details=fields["details"],
                    state=fields["state"],
                    large_image=fields.get("large_image") or "cs2_logo",
                    large_text=fields.get("large_text") or "Counter-Strike 2",
                    start=int(start_time),
                )
                log.info("Durum güncellendi: %s | %s", fields["details"], fields["state"])
                last_sent_key = key
                last_sent_time = time.time()

            time.sleep(1.0)

        except (DiscordNotFound, PipeClosed) as exc:
            log.warning("Discord'a bağlanılamadı (%s). Discord masaüstü uygulamasının "
                        "açık olduğundan emin ol. 5 sn sonra tekrar denenecek.", exc)
            rpc = None
            time.sleep(5.0)
        except KeyboardInterrupt:
            log.info("Kapatılıyor...")
            break
        except Exception as exc:  # noqa: BLE001 - script'in tek seferlik hatada ölmesini istemiyoruz
            log.exception("Beklenmeyen hata: %s", exc)
            time.sleep(3.0)

    if rpc is not None:
        try:
            rpc.clear()
            rpc.close()
        except Exception:  # noqa: BLE001
            pass


if __name__ == "__main__":
    main()
