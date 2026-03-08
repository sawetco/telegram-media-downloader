# 📥 Telegram Media Downloader

> Bulk download all photos and videos from any Telegram channel — including private channels that restrict in-app saving.

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Telethon](https://img.shields.io/badge/powered%20by-Telethon-0088cc)](https://github.com/LonamiWebs/Telethon)

---

## ✨ Features

- 📂 Bulk download all photos and videos from any channel you're a member of
- 🔒 Works with **private channels** that block in-app media saving
- ⚡ Parallel downloads for maximum speed
- 📊 Beautiful real-time progress bar with speed, ETA, and file name
- 🔁 **Resume support** — stops and restarts without re-downloading already saved files
- 🧙 Interactive setup wizard (English & Turkish)
- 🌍 Bilingual UI — English & Turkish

---

## 📋 Requirements

- Python 3.10 or higher
- A Telegram account
- API credentials from [my.telegram.org](https://my.telegram.org)
- Membership in the target channel

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/telegram-media-downloader.git
cd telegram-media-downloader
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the setup wizard

```bash
python setup.py
```

The wizard will guide you through:
- Choosing your language (English / Turkish)
- Entering your Telegram API credentials
- Selecting the target channel
- Configuring download preferences
- Authenticating your Telegram account (one-time)

### 4. Start downloading

```bash
python downloader.py
```

---

## 🔑 Getting Your API Credentials

1. Go to [https://my.telegram.org](https://my.telegram.org)
2. Log in with your phone number
3. Click **"API development tools"**
4. Create a new application — name and platform don't matter
5. Copy your **`api_id`** (a number) and **`api_hash`** (a string)

> ⚠️ **Keep these private.** Never share your `api_id` or `api_hash` publicly.

---

## 🔍 Finding a Channel ID

If you're unsure of the channel ID, run:

```bash
python find_channel.py
```

This lists all your channels and groups with their numeric IDs.

Private channel IDs typically look like: `-1001234567890`

---

## ⚙️ Configuration

After setup, a `config.json` file is created in the project folder:

```json
{
  "language": "en",
  "api_id": 12345678,
  "api_hash": "your_api_hash_here",
  "channel_id": -1001234567890,
  "download_path": "~/Downloads/telegram_media",
  "parallel": 4
}
```

| Field | Description |
|---|---|
| `language` | UI language: `en` or `tr` |
| `api_id` | Your Telegram API ID |
| `api_hash` | Your Telegram API hash |
| `channel_id` | Numeric ID of the target channel |
| `download_path` | Where files will be saved |
| `parallel` | Number of simultaneous downloads (2–8 recommended) |

To change any setting, either edit `config.json` directly or re-run `python setup.py`.

---

## 📁 File Structure

```
telegram-media-downloader/
├── downloader.py       # Main download script
├── setup.py            # Interactive setup wizard
├── find_channel.py     # Helper to list channel IDs
├── requirements.txt    # Python dependencies
├── config.json         # Your config (auto-generated, git-ignored)
├── session.session     # Telegram session (auto-generated, git-ignored)
└── .gitignore
```

---

## 🛟 Troubleshooting

**`ValueError: Cannot find any entity`**
Run `find_channel.py` first — this caches channel info into your session.

**Downloads are slow**
Telegram rate-limits API downloads. Try increasing `parallel` to `6` or `8` in `config.json`. If you see `FloodWait` errors, reduce it back to `2–4`.

**`FileReferenceExpiredError`**
Some messages contain self-destructing media. These cannot be downloaded via the API and are automatically skipped.

**`Config file not found`**
Run `python setup.py` to complete the initial setup.

**Authentication issues**
Delete `session.session` and re-run `python setup.py` to create a fresh session.

---

## ⚖️ Legal & Ethical Use

This tool uses the **official Telegram API** (not a scraper or exploit).

- ✅ Only downloads media from channels you are a **member of**
- ✅ Uses your own Telegram account credentials
- ❌ Do not use this to download and redistribute copyrighted content
- ❌ Do not use this to scrape content without the creator's permission

By using this tool you agree to Telegram's [Terms of Service](https://telegram.org/tos).

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

---
---

# 📥 Telegram Medya İndirici

> Herhangi bir Telegram kanalındaki tüm fotoğraf ve videoları toplu indirin — uygulama içi kaydetmeyi kısıtlayan özel kanallar dahil.

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
