import datetime
import random

def readme_hazirla():
    su_an = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # Her güncellemede değişecek rastgele bir söz (İstersen bunları değiştirebilirsin)
    sozler = [
        "Kod yazmak, sessizce şiir yazmaktır. 💻",
        "Hata ayıklamak (Debugging), bir dedektiflik hikayesidir. 🔍",
        "En iyi kod, henüz yazılmamış olandır. ✨",
        "Python ile dünyayı otomatize etmeye devam! 🚀",
        "openl32dll sistemi aktif ve stabil. ✅"
    ]
    secilen_soz = random.choice(sozler)

    icerik = f"""
# Selam! Ben openl32dll 👋

### 🤖 Otomatik Profil Durumu
Bu alan her saat başı GitHub Actions tarafından güncellenmektedir.

- 🕒 **Son Senkronizasyon:** {su_an}
- 🌍 **Konum:** Türkiye
- 🛠️ **Kullandığım Araçlar:** Python, GitHub Actions, VS Code
- 💬 **Günün Sözü:** {secilen_soz}

---
*Bu profil sayfası bir Python scripti tarafından otomatik olarak yönetilmektedir.*
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(icerik)

if __name__ == "__main__":
    readme_hazirla()
