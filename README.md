# 📥 Telegram Media Downloader

> Bulk download all photos and videos from any Telegram channel — including private channels that restrict in-app saving.

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Telethon](https://img.shields.io/badge/powered%20by-Telethon-0088cc)](https://github.com/LonamiWebs/Telethon)

🇹🇷 [Türkçe dokümantasyon için tıklayın →](README.tr.md)

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
