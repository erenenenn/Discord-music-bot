# Python Tabanlı Discord Müzik Botu

Asenkron ağ istekleri ile çalışan, kesintisiz müzik deneyimi sağlayan Discord botu.

Projenin amacı, bir Discord sunucusundaki ses kanalları yönetmek ve kullanıcılara otomatik bir şekilde müzik deneyimi sağlamaktır.

## Özellikler

# Asenkron Mimari: 'aiohttp' kullanılarak ağ bağlantıları ve API istekleri asenkron olarak yönetilir, bu sayede bot diğer komutları bekletmeden çalışmaya devam eder.
# Kuyruk Yapısı (Queue): Kullanıcıdan eklediği şarkıları bir listeye alarak otomatik bir şekilde oynatılır.
# Şarkı Atlama (Skip): Mevcut çalan şarkı istenildiği an geçilebilir ve sistem sıradaki şarkıya kesintisiz geçiş yapar.
# Hata Toleransı ve Debugging: Ağ bağlantısı kopmalarına veya API kısıtlamalarına karşı hata ayıklama mekanizmaları entegre edilmiştir. Çökme durumlarında sistem kendini güvenli bir şekilde kapatır veya işlemi atlar.

## Kullanılan Teknolojiler

# Dil: Python 3.x
# Kütüphaneler: 'discord.py', 'aiohttp'
# Diğer: Asenkron programlama ('asyncio')

## Kurulum ve Çalıştırma

Projeyi kendi ortamınızda çalıştırmak için aşağıdaki adımları izleyebilirsiniz.

### 1.Depoyu Klonlayın


