# 📥 Telegram Medya İndirici

> Herhangi bir Telegram kanalındaki tüm fotoğraf ve videoları toplu indirin — uygulama içi kaydetmeyi kısıtlayan özel kanallar dahil.

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Telethon](https://img.shields.io/badge/powered%20by-Telethon-0088cc)](https://github.com/LonamiWebs/Telethon)

🇬🇧 [English documentation →](README.md)

---

## ✨ Özellikler

- 📂 Üye olduğunuz her kanaldan toplu medya indirme
- 🔒 Uygulama içi medya kaydetmeyi **engelleyen özel kanallarla** çalışır
- ⚡ Maksimum hız için paralel indirme
- 📊 Hız, tahmini süre ve dosya adıyla gerçek zamanlı ilerleme çubuğu
- 🔁 **Kaldığı yerden devam** — yeniden başlatıldığında zaten indirilenleri atlar
- 🧙 İnteraktif kurulum sihirbazı (Türkçe & İngilizce)
- 🌍 İki dilli arayüz — Türkçe & İngilizce

---

## 📋 Gereksinimler

- Python 3.10 veya üstü
- Telegram hesabı
- [my.telegram.org](https://my.telegram.org) adresinden API bilgileri
- Hedef kanalda üyelik

---

## 🚀 Hızlı Başlangıç

### 1. Depoyu klonlayın

```bash
git clone https://github.com/your-username/telegram-media-downloader.git
cd telegram-media-downloader
```

### 2. Bağımlılıkları yükleyin

```bash
pip install -r requirements.txt
```

### 3. Kurulum sihirbazını çalıştırın

```bash
python setup.py
```

Sihirbaz şu adımlarda size yol gösterecek:
- Dil seçimi (Türkçe / İngilizce)
- Telegram API bilgilerinin girilmesi
- Hedef kanal seçimi
- İndirme tercihlerinin ayarlanması
- Telegram hesabı doğrulama (tek seferlik)

### 4. İndirmeye başlayın

```bash
python downloader.py
```

---

## 🔑 API Bilgilerini Alma

1. [https://my.telegram.org](https://my.telegram.org) adresine gidin
2. Telefon numaranızla giriş yapın
3. **"API development tools"** bölümüne tıklayın
4. Yeni bir uygulama oluşturun — isim ve platform önemli değil
5. **`api_id`** (sayı) ve **`api_hash`** (metin) değerlerini kopyalayın

> ⚠️ **Bu bilgileri gizli tutun.** `api_id` ve `api_hash` değerlerinizi asla herkese açık paylaşmayın.

---

## 🔍 Kanal ID'si Bulma

Kanal ID'sinden emin değilseniz şunu çalıştırın:

```bash
python find_channel.py
```

Bu komut, tüm kanallarınızı ve gruplarınızı sayısal ID'leriyle listeler.

Özel kanal ID'leri genellikle şöyle görünür: `-1001234567890`

---

## ⚙️ Yapılandırma

Kurulumdan sonra proje klasöründe bir `config.json` dosyası oluşturulur:

```json
{
  "language": "tr",
  "api_id": 12345678,
  "api_hash": "api_hash_buraya",
  "channel_id": -1001234567890,
  "download_path": "~/Downloads/telegram_media",
  "parallel": 4
}
```

| Alan | Açıklama |
|---|---|
| `language` | Arayüz dili: `en` veya `tr` |
| `api_id` | Telegram API ID'niz |
| `api_hash` | Telegram API hash'iniz |
| `channel_id` | Hedef kanalın sayısal ID'si |
| `download_path` | Dosyaların kaydedileceği yer |
| `parallel` | Eş zamanlı indirme sayısı (2–8 önerilir) |

Herhangi bir ayarı değiştirmek için `config.json` dosyasını doğrudan düzenleyebilir veya `python setup.py` komutunu yeniden çalıştırabilirsiniz.

---

## 📁 Dosya Yapısı

```
telegram-media-downloader/
├── downloader.py       # Ana indirme scripti
├── setup.py            # İnteraktif kurulum sihirbazı
├── find_channel.py     # Kanal ID'si bulucu
├── requirements.txt    # Python bağımlılıkları
├── config.json         # Yapılandırma (otomatik oluşturulur, commit edilmez)
└── session.session     # Telegram oturumu (otomatik oluşturulur, commit edilmez)
```

---

## 🛟 Sorun Giderme

**`ValueError: Cannot find any entity`**
Önce `find_channel.py` çalıştırın — bu komut kanal bilgilerini oturumunuza önbelleğe alır.

**İndirmeler yavaş**
Telegram, API indirmelerini hız sınırına tabi tutar. `config.json` dosyasındaki `parallel` değerini `6` veya `8`'e yükseltmeyi deneyin. `FloodWait` hatası alırsanız `2–4` arasına düşürün.

**`FileReferenceExpiredError`**
Bazı mesajlar kendini imha eden medya içerir. Bunlar API üzerinden indirilemez ve otomatik olarak atlanır.

**`Config file not found`**
İlk kurumu tamamlamak için `python setup.py` çalıştırın.

**Kimlik doğrulama sorunları**
`session.session` dosyasını silin ve yeni bir oturum oluşturmak için `python setup.py` komutunu yeniden çalıştırın.

---

## ⚖️ Yasal ve Etik Kullanım

Bu araç, resmi **Telegram API'sini** kullanır (scraper veya exploit değil).

- ✅ Yalnızca **üye olduğunuz** kanallardan medya indirir
- ✅ Kendi Telegram hesabı bilgilerinizi kullanır
- ❌ Telif hakkıyla korunan içerikleri indirip yeniden dağıtmak için kullanmayın
- ❌ İçerik oluşturucunun izni olmadan içerik toplamak için kullanmayın

Bu aracı kullanarak Telegram'ın [Kullanım Koşulları](https://telegram.org/tos)'nı kabul etmiş olursunuz.

---

## 📄 Lisans

MIT Lisansı — ayrıntılar için [LICENSE](LICENSE) dosyasına bakın.
