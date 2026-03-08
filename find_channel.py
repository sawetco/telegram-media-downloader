"""
find_channel.py — Lists all your Telegram channels/groups with their IDs.
Run this to find the Channel ID needed during setup.
"""

import asyncio
import json
import os
import sys

CONFIG_FILE  = os.path.join(os.path.dirname(__file__), 'config.json')
SESSION_FILE = os.path.join(os.path.dirname(__file__), 'session')

try:
    from rich.console import Console
    from rich.table import Table
    from telethon import TelegramClient
    from telethon.tl.types import Channel, Chat
except ImportError:
    print("Missing dependencies. Please run:  pip install telethon rich")
    sys.exit(1)

console = Console()

LABELS = {
    'en': {
        'title':   'Your Telegram Channels & Groups',
        'col_id':  'Channel ID',
        'col_name':'Name',
        'col_type':'Type',
        'channel': 'Channel',
        'group':   'Group',
        'tip':     'Copy the ID of the channel you want to use in setup.',
        'no_sess': 'No session found. Run setup first:  python setup.py',
    },
    'tr': {
        'title':   'Telegram Kanallarınız ve Gruplarınız',
        'col_id':  'Kanal ID',
        'col_name':'İsim',
        'col_type':'Tür',
        'channel': 'Kanal',
        'group':   'Grup',
        'tip':     'Kurulumda kullanmak istediğiniz kanalın ID\'sini kopyalayın.',
        'no_sess': 'Oturum bulunamadı. Önce kurulumu çalıştırın:  python setup.py',
    }
}


def get_lang():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f).get('language', 'en')
    return 'en'


def get_credentials():
    if not os.path.exists(CONFIG_FILE):
        return None, None
    with open(CONFIG_FILE) as f:
        cfg = json.load(f)
    return cfg.get('api_id'), cfg.get('api_hash')


async def main():
    lang    = get_lang()
    L       = LABELS[lang]
    api_id, api_hash = get_credentials()

    if not os.path.exists(SESSION_FILE + '.session') and not os.path.exists(SESSION_FILE):
        console.print(f"[red]{L['no_sess']}[/red]")
        sys.exit(1)

    table = Table(title=L['title'], border_style="cyan", show_lines=True)
    table.add_column(L['col_id'],   style="bold yellow", no_wrap=True)
    table.add_column(L['col_name'], style="bold white")
    table.add_column(L['col_type'], style="dim")

    async with TelegramClient(SESSION_FILE, api_id, api_hash) as client:
        async for dialog in client.iter_dialogs():
            entity = dialog.entity
            if isinstance(entity, (Channel, Chat)):
                kind = L['channel'] if isinstance(entity, Channel) and entity.broadcast else L['group']
                table.add_row(str(dialog.id), dialog.name, kind)

    console.print()
    console.print(table)
    console.print(f"\n[dim]{L['tip']}[/dim]\n")


if __name__ == '__main__':
    asyncio.run(main())
