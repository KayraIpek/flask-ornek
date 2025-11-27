from flask import Flask, url_for, request
import random

app = Flask(__name__)

# Nadirlik Seviyelerine Göre Renkler
RENKLER = {
    "Common": "gray",
    "Rare": "#007bff",
    "Epic": "#6f42c1",
    "Legendary": "#ffc107"
}

def sansli_soz_getir():
    # --- (Burası senin yazdığın fonksiyonun aynısı, değiştirmedim) ---
    try:
        with open("sozler.txt", "r", encoding="utf-8") as dosya:
            satirlar = dosya.readlines()
    except:
        return None 

    soz_havuzu = {"Common": [], "Rare": [], "Epic": [], "Legendary": []}
    
    for satir in satirlar:
        temiz_satir = satir.strip()
        if not temiz_satir: continue
        parcalar = temiz_satir.split("|")
        if len(parcalar) == 3:
            soz = parcalar[0].strip()
            yazar = parcalar[1].strip()
            nadirlik = parcalar[2].strip()
            if nadirlik in soz_havuzu:
                soz_havuzu[nadirlik].append({"soz": soz, "yazar": yazar, "tip": nadirlik})

    secilen_tip = random.choices(["Common", "Rare", "Epic", "Legendary"], weights=[50, 30, 15, 5], k=1)[0]

    if not soz_havuzu[secilen_tip]:
        secilen_tip = "Common"
        if not soz_havuzu["Common"]:
            return {"soz": "Listeniz boş görünüyor.", "yazar": "Sistem", "tip": "Common"}
        
    return random.choice(soz_havuzu[secilen_tip])

# DEĞİŞİKLİK 1: Methods ekledik. Hem sayfayı görmeye (GET) hem tıklamaya (POST) izin veriyoruz.
@app.route('/', methods=['GET', 'POST'])
def anasayfa():
    
    # Varsayılan değerler (Henüz sandık açılmadı)
    sandik_acildi_mi = False
    veri = None
    yazi_rengi = "white"
    konfeti_kodu = ""
    
    # DEĞİŞİKLİK 2: Eğer kullanıcı sandığa (butona) bastıysa bu blok çalışır
    if request.method == 'POST':
        sandik_acildi_mi = True
        veri = sansli_soz_getir()
        
        if veri:
            yazi_rengi = RENKLER[veri['tip']]
            # Konfeti sadece açılınca ve iyi bir şey çıkınca patlasın
            if veri['tip'] in ['Epic', 'Legendary']:
                konfeti_kodu = """
                <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
                <script>
                    setTimeout(() => {
                        confetti({ particleCount: 150, spread: 70, origin: { y: 0.6 } });
                    }, 300);
                </script>
                """

    # HTML Tasarımı (Dinamik hale getirdik)
    # Eğer sandık açıldıysa sonucu göster, açılmadıysa kapalı sandığı göster
    
    icerik_html = ""
    
    if sandik_acildi_mi and veri:
        # --- DURUM A: SANDIK AÇILDIKTAN SONRA GÖRÜNECEK KISIM ---
        icerik_html = f"""
            <div style="padding: 10px 30px; border: 2px solid {yazi_rengi}; border-radius: 50px; color: {yazi_rengi}; font-weight: 900; font-size: 24px; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 30px; box-shadow: 0 0 20px {yazi_rengi};">
                {veri['tip']}
            </div>
            <h1 style="max-width: 800px; line-height: 1.4;">"{veri['soz']}"</h1>
            <h3 style="color: #aaa; margin-bottom: 50px;">- {veri['yazar']}</h3>
            
            <a href="/" style="text-decoration: none; color: white; border: 1px solid white; padding: 10px 20px; border-radius: 5px;">
                🔄 Tekrar Dene
            </a>
            {konfeti_kodu}
        """
    else:
        # --- DURUM B: SANDIK HENÜZ AÇILMADI (İLK GİRİŞ) ---
        icerik_html = f"""
            <h1 style="margin-bottom: 30px;">Şanslı Sandık</h1>
            <p style="margin-bottom: 10px; color: #ccc;">Kutuyu açmak için sandığa tıkla!</p>
            
            <form method="POST">
                <button type="submit" style="background: none; border: none; cursor: pointer; padding: 0;">
                    <img src="{url_for('static', filename='sandik.png')}" 
                         width="150" 
                         style="transition: transform 0.2s;"
                         onmouseover="this.style.transform='scale(1.1)'" 
                         onmouseout="this.style.transform='scale(1.0)'"
                    >
                </button>
            </form>
        """

    # Ana İskelet HTML
    tam_sayfa = f"""
    <div style="font-family: 'Segoe UI', sans-serif; text-align: center; background-color: #222; color: white; height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; margin: 0; overflow: hidden;">
        {icerik_html}
    </div>
    """
    
    return tam_sayfa

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    
    # host='0.0.0.0' demek: "Ağdaki diğer cihazlar da beni görebilsin" demektir.