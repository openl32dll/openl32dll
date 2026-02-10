import datetime
import random

def readme_hazirla():
    # Saat dilimini ayarlamak istersen +3 ekleyebilirsin, şu an UTC basıyor olabilir
    su_an = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    sozler = [
        "Kod yazmak, sessizce şiir yazmaktır. 💻",
        "Hata ayıklamak, bir dedektiflik hikayesidir. 🔍",
        "Python ile dünyayı otomatize etmeye devam! 🚀",
        "openl32dll sistemi aktif ve stabil. ✅"
    ]
    secilen_soz = random.choice(sozler)

    # Linkleri Markdown formatında (parantezli) değil, doğrudan HTML <img> olarak koyalım
    # Bu yöntem GitHub'da daha stabil çalışır
    icerik = f"""
# Selam! Ben openl32dll 👋

### 🤖 Otomatik Profil Durumu
- 🕒 **Son Senkronizasyon:** {su_an}
- 💬 **Günün Sözü:** {secilen_soz}

### 📊 GitHub İstatistiklerim
<img src="https://github-readme-stats.vercel.app/api?username=openl32dll&show_icons=true&theme=tokyonight" alt="Stats" />

### 🚀 Kullandığım Diller
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=openl32dll&layout=compact&theme=tokyonight" alt="Langs" />

---
*Bu profil sayfası bir Python scripti tarafından otomatik olarak yönetilmektedir.*
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(icerik)

if __name__ == "__main__":
    readme_hazirla()
