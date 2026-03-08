import asyncio
import os
import json
import sys
from telethon import TelegramClient
from telethon.tl.types import MessageMediaDocument, MessageMediaPhoto
from telethon.errors import FloodWaitError
from rich.progress import (
    Progress, BarColumn, DownloadColumn, TransferSpeedColumn,
    TimeRemainingColumn, TextColumn, TaskProgressColumn, SpinnerColumn
)
from rich.console import Console
from rich.panel import Panel

CONFIG_FILE  = os.path.join(os.path.dirname(__file__), 'config.json')
SESSION_FILE = os.path.join(os.path.dirname(__file__), 'session')
console      = Console()


# ─────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────

def load_config():
    if not os.path.exists(CONFIG_FILE):
        console.print("[red]Config file not found. Please run the wizard first:[/red]")
        console.print("  [bold cyan]python setup.py[/bold cyan]")
        sys.exit(1)
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)


# ─────────────────────────────────────────
#  STRINGS
# ─────────────────────────────────────────

STRINGS = {
    'en': {
        'title':        'Telegram Media Downloader',
        'folder':       'Download folder',
        'prev_done':    'Previously downloaded',
        'files':        'files',
        'scanning':     '🔍 Scanning channel messages...',
        'to_download':  '📥 New files to download',
        'all_done':     '🎉 All files already downloaded!',
        'total':        'Total progress',
        'downloaded':   '✅ Downloaded',
        'skipped':      '⏭  Skipped',
        'failed':       '✗  Failed',
        'summary':      'Summary',
        'rate_limit':   '⏳ Rate limit — waiting {s}s...',
        'skip_exists':  'Already exists',
        'ok':           '✓',
        'err':          '✗ Failed',
        'err_skip':     '✗ Skipped',
        'no_config':    'Config not found. Run: python setup.py',
    },
    'tr': {
        'title':        'Telegram Medya İndirici',
        'folder':       'İndirme klasörü',
        'prev_done':    'Daha önce tamamlanan',
        'files':        'dosya',
        'scanning':     '🔍 Kanal mesajları taranıyor...',
        'to_download':  '📥 İndirilecek yeni dosya',
        'all_done':     '🎉 Tüm dosyalar zaten indirilmiş!',
        'total':        'Toplam ilerleme',
        'downloaded':   '✅ İndirilen',
        'skipped':      '⏭  Atlanan',
        'failed':       '✗  Başarısız',
        'summary':      'Özet',
        'rate_limit':   '⏳ Rate limit — {s}s bekleniyor...',
        'skip_exists':  'Zaten var',
        'ok':           '✓',
        'err':          '✗ Başarısız',
        'err_skip':     '✗ Atlandı',
        'no_config':    'Config bulunamadı. Çalıştır: python setup.py',
    }
}


def t(cfg, key, **kwargs):
    lang = cfg.get('language', 'en')
    s = STRINGS.get(lang, STRINGS['en']).get(key, key)
    return s.format(**kwargs) if kwargs else s


# ─────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────

def load_downloaded(progress_file):
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            return set(line.strip() for line in f if line.strip())
    return set()


def mark_downloaded(progress_file, msg_id: int):
    with open(progress_file, 'a') as f:
        f.write(f"{msg_id}\n")


def get_original_filename(msg) -> str | None:
    if isinstance(msg.media, MessageMediaDocument):
        for attr in msg.media.document.attributes:
            if hasattr(attr, 'file_name') and attr.file_name:
                return attr.file_name
    return None


def get_file_size(msg) -> int | None:
    if isinstance(msg.media, MessageMediaDocument):
        return msg.media.document.size
    return None


# ─────────────────────────────────────────
#  DOWNLOAD
# ─────────────────────────────────────────

async def download_message(client, msg, semaphore, stats, progress, overall_task, cfg, download_dir, progress_file):
    async with semaphore:
        original_name = get_original_filename(msg) or f"photo_{msg.id}.jpg"
        file_size     = get_file_size(msg)
        display_name  = original_name[:45] + "…" if len(original_name) > 45 else original_name

        target = os.path.join(download_dir, original_name)
        if os.path.exists(target):
            mark_downloaded(progress_file, msg.id)
            stats['skipped'] += 1
            progress.advance(overall_task)
            return

        file_task = progress.add_task(f"[cyan]{display_name}", total=file_size, visible=True)

        def progress_callback(received, total):
            progress.update(file_task, completed=received, total=total)

        try:
            path = await client.download_media(msg, file=download_dir, progress_callback=progress_callback)
            if path:
                mark_downloaded(progress_file, msg.id)
                stats['done'] += 1
                progress.update(file_task, visible=False)
                progress.advance(overall_task)
                console.log(f"[green]{t(cfg, 'ok')}[/green] {original_name}")

        except FloodWaitError as e:
            progress.update(file_task, visible=False)
            console.log(f"[yellow]{t(cfg, 'rate_limit', s=e.seconds)}[/yellow]")
            await asyncio.sleep(e.seconds)
            try:
                path = await client.download_media(msg, file=download_dir)
                if path:
                    mark_downloaded(progress_file, msg.id)
                    stats['done'] += 1
                    progress.advance(overall_task)
                    console.log(f"[green]{t(cfg, 'ok')}[/green] {original_name}")
            except Exception as e2:
                stats['failed'] += 1
                progress.advance(overall_task)
                console.log(f"[red]{t(cfg, 'err')}:[/red] {original_name} — {e2}")

        except Exception as e:
            stats['failed'] += 1
            progress.update(file_task, visible=False)
            progress.advance(overall_task)
            console.log(f"[red]{t(cfg, 'err_skip')}:[/red] {original_name} — {e}")


# ─────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────

async def main():
    cfg          = load_config()
    download_dir = os.path.expanduser(cfg['download_path'])
    progress_file = os.path.join(download_dir, '.downloaded_ids')
    os.makedirs(download_dir, exist_ok=True)

    downloaded = load_downloaded(progress_file)

    console.print(Panel.fit(
        f"[bold cyan]{t(cfg, 'title')}[/bold cyan]\n"
        f"[dim]{t(cfg, 'folder')}:[/dim] {download_dir}\n"
        f"[dim]{t(cfg, 'prev_done')}:[/dim] [green]{len(downloaded)}[/green] {t(cfg, 'files')}",
        border_style="cyan"
    ))

    semaphore = asyncio.Semaphore(cfg.get('parallel', 4))
    stats     = {'done': 0, 'skipped': 0, 'failed': 0}

    async with TelegramClient(SESSION_FILE, cfg['api_id'], cfg['api_hash']) as client:
        console.print(f"\n[bold]{t(cfg, 'scanning')}[/bold]")

        msgs_to_download = []
        async for msg in client.iter_messages(cfg['channel_id']):
            if not msg.media:
                continue
            if str(msg.id) in downloaded:
                continue
            if isinstance(msg.media, (MessageMediaPhoto, MessageMediaDocument)):
                msgs_to_download.append(msg)

        total = len(msgs_to_download)

        if total == 0:
            console.print(f"\n[bold green]{t(cfg, 'all_done')}[/bold green]")
            return

        console.print(f"\n[bold]{t(cfg, 'to_download')}: [cyan]{total}[/cyan][/bold]\n")

        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=30),
            TaskProgressColumn(),
            DownloadColumn(),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
            console=console,
            refresh_per_second=10,
        ) as progress:
            overall_task = progress.add_task(f"[bold white]{t(cfg, 'total')}", total=total)

            tasks = [
                download_message(client, msg, semaphore, stats, progress, overall_task, cfg, download_dir, progress_file)
                for msg in msgs_to_download
            ]
            await asyncio.gather(*tasks)

    console.print(Panel(
        f"[green]{t(cfg, 'downloaded')}  : {stats['done']}[/green]\n"
        f"[yellow]{t(cfg, 'skipped')}    : {stats['skipped']}[/yellow]\n"
        f"[red]{t(cfg, 'failed')}  : {stats['failed']}[/red]",
        title=f"[bold]{t(cfg, 'summary')}[/bold]",
        border_style="green"
    ))


if __name__ == '__main__':
    asyncio.run(main())
