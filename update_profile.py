import datetime
import random

def readme_hazirla():
    su_an = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    sozler = [
        "Kod yazmak, sessizce şiir yazmaktır. 💻",
        "Python ile dünyayı otomatize etmeye devam! 🚀",
        "openl32dll sistemi aktif ve stabil. ✅"
    ]
    secilen_soz = random.choice(sozler)

    # İstatistik kartlarını buraya ekledik ki Python bunları silmesin!
    icerik = f"""
# Selam! Ben openl32dll 👋

### 🤖 Otomatik Profil Durumu
- 🕒 **Son Senkronizasyon:** {su_an}
- 💬 **Günün Sözü:** {secilen_soz}

### 📊 GitHub İstatistiklerim
![Stats](https://github-readme-stats.vercel.app/api?username=openl32dll&show_icons=true&theme=tokyonight)

### 🚀 Kullandığım Diller
![Langs](https://github-readme-stats.vercel.app/api/top-langs/?username=openl32dll&layout=compact&theme=tokyonight)

---
*Bu profil sayfası bir Python scripti tarafından otomatik olarak yönetilmektedir.*
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(icerik)

if __name__ == "__main__":
    readme_hazirla()
