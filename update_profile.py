import datetime
import random

def readme_hazirla():
    su_an = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    sozler = [
        "Kod yazmak, sessizce şiir yazmaktır. 💻",
        "Python ile dünyayı otomatize etmeye devam! 🚀",
        "openl32dll sistemi aktif ve stabil. ✅",
        "Sistemler uyur, kodlar asla! 🛠️"
    ]
    secilen_soz = random.choice(sozler)

    icerik = f"""
# Selam! Ben openl32dll 👋

<p align="left">
  <img src="https://komarev.com/ghpvc/?username=openl32dll&color=blue&style=flat-square" alt="Ziyaretçi Sayısı" />
</p>

### 🤖 Otomatik Profil Durumu
- 🕒 **Son Senkronizasyon:** {su_an}
- 💬 **Günün Sözü:** {secilen_soz}

### 🛠️ Kullandığım Teknolojiler
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![VS Code](https://img.shields.io/badge/Visual_Studio_Code-00788C?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)

### 📊 GitHub İstatistiklerim
<img src="https://github-readme-stats.vercel.app/api?username=openl32dll&show_icons=true&theme=tokyonight" alt="Stats" />

### 🚀 Kullandığım Diller
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=openl32dll&layout=compact&theme=tokyonight" alt="Langs" />

### 🎮 CS2 Discord Rich Presence
Counter-Strike 2 oynarken Discord'da sadece "oynuyor" değil; hangi haritada,
hangi modda (Rekabetçi/Premier, Yoldaş, Basit, Deathmatch, Silah Yarışı vb.)
ve kaçıncı roundda olduğunu gösteren araç: [`cs2-discord-rpc`](https://github.com/openl32dll/cs2-discord-rpc)

---
*Bu profil sayfası bir Python scripti tarafından otomatik olarak yönetilmektedir.*
"""
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(icerik)

if __name__ == "__main__":
    readme_hazirla()
