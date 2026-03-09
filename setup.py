import asyncio
import json
import os
import sys
import platform

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE  = os.path.join(BASE_DIR, 'config.json')
SESSION_FILE = os.path.join(BASE_DIR, 'session')

# Detect correct python command for this OS
PYTHON_CMD = 'python3' if platform.system() in ('Darwin', 'Linux') else 'python'

# Default download path: 'downloads' folder next to the script
DEFAULT_DOWNLOAD_PATH = os.path.join(BASE_DIR, 'downloads')

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm, IntPrompt
    from rich.rule import Rule
    from telethon import TelegramClient
except ImportError:
    print("Missing dependencies. Please run:  pip3 install telethon rich")
    sys.exit(1)

console = Console()

# ─────────────────────────────────────────
#  STRINGS
# ─────────────────────────────────────────

WIZARD = {
    'en': {
        'welcome_title': '🚀 Telegram Media Downloader — Setup Wizard',
        'welcome_body': (
            "Welcome! This wizard will guide you through the one-time setup.\n\n"
            "[bold]What you'll need:[/bold]\n"
            "  • Telegram account\n"
            "  • API credentials from [link=https://my.telegram.org]my.telegram.org[/link]\n"
            "  • The channel ID you want to download from\n\n"
            "[dim]Your credentials are stored locally in config.json and never shared.[/dim]"
        ),
        'step1_title':  'Step 1 of 4 — Language',
        'step1_body':   'Choose your preferred language / Dil seçin:',
        'step2_title':  'Step 2 of 4 — Telegram API Credentials',
        'step2_body': (
            "Go to [bold cyan]https://my.telegram.org[/bold cyan]\n"
            "  1. Log in with your phone number\n"
            "  2. Click [bold]'API development tools'[/bold]\n"
            "  3. Create a new application (any name/platform)\n"
            "  4. Copy your [bold]App api_id[/bold] and [bold]App api_hash[/bold]"
        ),
        'enter_api_id':   'Enter your api_id (numbers only)',
        'enter_api_hash': 'Enter your api_hash',
        'step3_title':  'Step 3 of 4 — Channel',
        'step3_body_before_auth': (
            "You need the [bold]Channel ID[/bold] of the channel to download from.\n\n"
            "[bold]How to find it:[/bold]\n"
            "  1. Complete this setup first (authentication required)\n"
            "  2. Then run: [bold cyan]{python} find_channel.py[/bold cyan]\n"
            "     It will list all your channels with their IDs\n"
            "  3. Re-run [bold cyan]{python} setup.py[/bold cyan] and enter the ID\n\n"
            "[dim]For private channels the ID usually looks like: -1001234567890[/dim]\n"
            "[dim]Leave blank for now and update config.json later.[/dim]"
        ),
        'enter_channel':  'Enter the Channel ID (or press Enter to skip)',
        'step4_title':  'Step 4 of 4 — Download Settings',
        'step4_body':   'Configure download preferences.',
        'enter_path':     'Download folder path',
        'enter_parallel': 'Parallel downloads (2–8 recommended)',
        'verify_title': '✅ Configuration Summary',
        'confirm_save':   'Save and continue?',
        'saved':        '[bold green]✓ Config saved to config.json[/bold green]',
        'auth_title':   '🔐 Authenticating with Telegram...',
        'auth_body': (
            "Telegram will send a verification code to your app/SMS.\n"
            "[dim]This creates a session file so you won't need to log in again.[/dim]"
        ),
        'auth_ok':      '[bold green]✓ Authentication successful![/bold green]',
        'done_title':   '🎉 Setup Complete!',
        'done_body_with_channel': (
            "You're all set! To start downloading, run:\n\n"
            "  [bold cyan]{python} downloader.py[/bold cyan]\n\n"
            "To re-run this wizard at any time:\n"
            "  [bold cyan]{python} setup.py[/bold cyan]"
        ),
        'done_body_no_channel': (
            "Almost there! You skipped the channel ID.\n\n"
            "Run this to find your channel ID:\n"
            "  [bold cyan]{python} find_channel.py[/bold cyan]\n\n"
            "Then re-run setup to set it:\n"
            "  [bold cyan]{python} setup.py[/bold cyan]"
        ),
        'invalid_id':   '[red]Invalid channel ID. Must be a number (e.g. -1001234567890)[/red]',
        'invalid_api':  '[red]Invalid API credentials. Please check and try again.[/red]',
        'aborted':      '[yellow]Setup aborted.[/yellow]',
        'lang_prompt':  'Language [en/tr]',
        'path_hint':    'Default',
    },
    'tr': {
        'welcome_title': '🚀 Telegram Medya İndirici — Kurulum Sihirbazı',
        'welcome_body': (
            "Hoş geldiniz! Bu sihirbaz sizi tek seferlik kurulum sürecinde yönlendirecek.\n\n"
            "[bold]İhtiyacınız olanlar:[/bold]\n"
            "  • Telegram hesabı\n"
            "  • [link=https://my.telegram.org]my.telegram.org[/link] adresinden API bilgileri\n"
            "  • İndirmek istediğiniz kanalın ID'si\n\n"
            "[dim]Bilgileriniz yalnızca yerel config.json dosyasına kaydedilir, paylaşılmaz.[/dim]"
        ),
        'step1_title':  'Adım 1 / 4 — Dil',
        'step1_body':   'Dil seçin / Choose your language:',
        'step2_title':  'Adım 2 / 4 — Telegram API Bilgileri',
        'step2_body': (
            "[bold cyan]https://my.telegram.org[/bold cyan] adresine gidin\n"
            "  1. Telefon numaranızla giriş yapın\n"
            "  2. [bold]'API development tools'[/bold] bölümüne tıklayın\n"
            "  3. Yeni bir uygulama oluşturun (isim/platform önemli değil)\n"
            "  4. [bold]App api_id[/bold] ve [bold]App api_hash[/bold] değerlerini kopyalayın"
        ),
        'enter_api_id':   'api_id değerini girin (sadece rakam)',
        'enter_api_hash': 'api_hash değerini girin',
        'step3_title':  'Adım 3 / 4 — Kanal',
        'step3_body_before_auth': (
            "İndirmek istediğiniz kanalın [bold]ID[/bold] değeri gerekli.\n\n"
            "[bold]Nasıl bulunur:[/bold]\n"
            "  1. Önce bu kurulumu tamamlayın (kimlik doğrulama gerekli)\n"
            "  2. Ardından çalıştırın: [bold cyan]{python} find_channel.py[/bold cyan]\n"
            "     Tüm kanallarınız ID'leriyle listelenecektir\n"
            "  3. [bold cyan]{python} setup.py[/bold cyan] ile tekrar kurulum yapıp ID'yi girin\n\n"
            "[dim]Özel kanalların ID'si genellikle şöyle görünür: -1001234567890[/dim]\n"
            "[dim]Şimdilik boş bırakıp config.json üzerinden sonra güncelleyebilirsiniz.[/dim]"
        ),
        'enter_channel':  'Kanal ID\'sini girin (atlamak için Enter\'a basın)',
        'step4_title':  'Adım 4 / 4 — İndirme Ayarları',
        'step4_body':   'İndirme tercihlerini ayarlayın.',
        'enter_path':     'İndirme klasörü yolu',
        'enter_parallel': 'Paralel indirme sayısı (2–8 önerilir)',
        'verify_title': '✅ Yapılandırma Özeti',
        'confirm_save':   'Kaydedip devam edilsin mi?',
        'saved':        '[bold green]✓ Yapılandırma config.json dosyasına kaydedildi[/bold green]',
        'auth_title':   '🔐 Telegram ile kimlik doğrulanıyor...',
        'auth_body': (
            "Telegram, uygulamanıza/SMS'inize bir doğrulama kodu gönderecek.\n"
            "[dim]Bu, bir oturum dosyası oluşturur; bir daha giriş yapmanız gerekmez.[/dim]"
        ),
        'auth_ok':      '[bold green]✓ Kimlik doğrulama başarılı![/bold green]',
        'done_title':   '🎉 Kurulum Tamamlandı!',
        'done_body_with_channel': (
            "Hazırsınız! İndirmeye başlamak için çalıştırın:\n\n"
            "  [bold cyan]{python} downloader.py[/bold cyan]\n\n"
            "Bu sihirbazı istediğiniz zaman tekrar çalıştırabilirsiniz:\n"
            "  [bold cyan]{python} setup.py[/bold cyan]"
        ),
        'done_body_no_channel': (
            "Neredeyse bitti! Kanal ID'sini atladınız.\n\n"
            "Kanal ID'nizi bulmak için çalıştırın:\n"
            "  [bold cyan]{python} find_channel.py[/bold cyan]\n\n"
            "Ardından kurulumu tekrar yapıp ID'yi girin:\n"
            "  [bold cyan]{python} setup.py[/bold cyan]"
        ),
        'invalid_id':   "[red]Geçersiz kanal ID'si. Bir sayı olmalıdır (örn. -1001234567890)[/red]",
        'invalid_api':  '[red]Geçersiz API bilgileri. Lütfen kontrol edip tekrar deneyin.[/red]',
        'aborted':      '[yellow]Kurulum iptal edildi.[/yellow]',
        'lang_prompt':  'Dil [en/tr]',
        'path_hint':    'Varsayılan',
    }
}


def w(lang, key, **kwargs):
    s = WIZARD.get(lang, WIZARD['en']).get(key, key)
    return s.format(**kwargs) if kwargs else s


# ─────────────────────────────────────────
#  WIZARD STEPS
# ─────────────────────────────────────────

def step_language():
    console.print(Rule())
    console.print(f"\n[bold]{w('en', 'step1_title')}[/bold]")
    console.print(w('en', 'step1_body'))
    console.print()
    return Prompt.ask(w('en', 'lang_prompt'), choices=['en', 'tr'], default='en')


def step_api(lang):
    console.print(f"\n[bold]{w(lang, 'step2_title')}[/bold]")
    console.print(Panel(w(lang, 'step2_body'), border_style="dim"))
    console.print()

    while True:
        try:
            api_id = IntPrompt.ask(w(lang, 'enter_api_id'))
            if api_id > 0:
                break
        except Exception:
            pass
        console.print(w(lang, 'invalid_api'))

    api_hash = Prompt.ask(w(lang, 'enter_api_hash'))
    return api_id, api_hash.strip()


def step_channel(lang):
    console.print(f"\n[bold]{w(lang, 'step3_title')}[/bold]")
    console.print(Panel(w(lang, 'step3_body_before_auth', python=PYTHON_CMD), border_style="dim"))
    console.print()

    raw = Prompt.ask(w(lang, 'enter_channel'), default='')
    if not raw.strip():
        return None

    while True:
        try:
            return int(raw.strip())
        except ValueError:
            console.print(w(lang, 'invalid_id'))
            raw = Prompt.ask(w(lang, 'enter_channel'), default='')
            if not raw.strip():
                return None


def step_settings(lang):
    console.print(f"\n[bold]{w(lang, 'step4_title')}[/bold]")
    console.print(w(lang, 'step4_body'))
    console.print(f"[dim]  {w(lang, 'path_hint')}: {DEFAULT_DOWNLOAD_PATH}[/dim]")
    console.print()

    download_path = Prompt.ask(w(lang, 'enter_path'), default=DEFAULT_DOWNLOAD_PATH)

    while True:
        try:
            parallel = IntPrompt.ask(w(lang, 'enter_parallel'), default=4)
            if 1 <= parallel <= 16:
                break
        except Exception:
            pass

    return download_path.strip(), parallel


async def step_auth(lang, api_id, api_hash):
    console.print(f"\n[bold]{w(lang, 'auth_title')}[/bold]")
    console.print(Panel(w(lang, 'auth_body'), border_style="yellow"))
    console.print()

    async with TelegramClient(SESSION_FILE, api_id, api_hash) as client:
        me = await client.get_me()
        name = f"{me.first_name or ''} {me.last_name or ''}".strip() or me.username or "Unknown"
        console.print(f"{w(lang, 'auth_ok')} [dim]({name})[/dim]")


# ─────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────

async def main():
    console.print()
    console.print(Panel.fit(
        "[bold cyan]Telegram Media Downloader[/bold cyan]\n"
        "[dim]github.com/your-username/telegram-media-downloader[/dim]",
        border_style="cyan"
    ))
    console.print()

    lang = step_language()

    console.print()
    console.print(Panel.fit(
        w(lang, 'welcome_body'),
        title=f"[bold cyan]{w(lang, 'welcome_title')}[/bold cyan]",
        border_style="cyan"
    ))

    api_id, api_hash   = step_api(lang)
    channel_id         = step_channel(lang)
    download_path, parallel = step_settings(lang)

    # Summary
    console.print(f"\n[bold]{w(lang, 'verify_title')}[/bold]\n")
    console.print(f"  [dim]Language:[/dim]      {lang}")
    console.print(f"  [dim]API ID:[/dim]        {api_id}")
    console.print(f"  [dim]API Hash:[/dim]      {api_hash[:8]}{'*' * (len(api_hash) - 8)}")
    console.print(f"  [dim]Channel ID:[/dim]    {channel_id if channel_id else '[yellow]not set[/yellow]'}")
    console.print(f"  [dim]Download path:[/dim] {download_path}")
    console.print(f"  [dim]Parallel:[/dim]      {parallel}")
    console.print()

    if not Confirm.ask(w(lang, 'confirm_save'), default=True):
        console.print(w(lang, 'aborted'))
        sys.exit(0)

    config = {
        'language':      lang,
        'api_id':        api_id,
        'api_hash':      api_hash,
        'channel_id':    channel_id,
        'download_path': download_path,
        'parallel':      parallel,
    }
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

    console.print(f"\n{w(lang, 'saved')}")

    await step_auth(lang, api_id, api_hash)

    console.print()
    if channel_id:
        done_body = w(lang, 'done_body_with_channel', python=PYTHON_CMD)
    else:
        done_body = w(lang, 'done_body_no_channel', python=PYTHON_CMD)

    console.print(Panel(
        done_body,
        title=f"[bold green]{w(lang, 'done_title')}[/bold green]",
        border_style="green"
    ))


if __name__ == '__main__':
    asyncio.run(main())
