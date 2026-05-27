# Asenkron Discord Müzik Botu

Asenkron ağ istekleri ile çalışan, kesintisiz müzik deneyimi sunan Python tabanlı Discord botu.

Bu proje, bir Discord sunucusundaki ses kanallarını yönetmek ve kullanıcıların müzik dinleme deneyimini otomatize etmek amacıyla geliştirilmiştir.

## Özellikler

* **Asenkron Mimari:** `aiohttp` kullanılarak ağ bağlantıları ve API istekleri asenkron olarak yönetilir, bu sayede bot diğer komutları bekletmeden çalışmaya devam eder.
* **Müzik Kuyruğu (Queue):** Kullanıcıların eklediği şarkılar otomatik olarak bir listeye alınır ve sırayla oynatılır.
* **Şarkı Atlama (Skip):** Mevcut çalan şarkı istenildiği an geçilebilir ve sistem sıradaki şarkıya kesintisiz geçiş yapar.
* **Hata Toleransı ve Debugging:** Ağ bağlantısı kopmalarına veya API kısıtlamalarına karşı hata ayıklama mekanizmaları entegre edilmiştir. Çökme durumlarında sistem kendini güvenli bir şekilde kapatır veya işlemi atlar.

## Kullanılan Teknolojiler

* **Dil:** Python 3.x
* **Kütüphaneler:** `discord.py` (veya kullandığın fork), `aiohttp`
* **Diğer:** Asenkron programlama (`asyncio`)

## Kurulum ve Çalıştırma

Projeyi kendi ortamınızda çalıştırmak için aşağıdaki adımları izleyebilirsiniz.

### 1. Depoyu Klonlayın
```bash
git clone [https://github.com/](https://github.com/)[kullanici-adiniz]/[depo-adiniz].git
cd [depo-adiniz]
pip install -r requirements.txt
echo "DISCORD_TOKEN=sizin_gizli_token_bilginiz_buraya" > .env
python3 main.py
