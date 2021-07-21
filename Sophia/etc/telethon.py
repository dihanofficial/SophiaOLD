from telethon import TelegramClient

from Sophia.config import get_int_key, get_str_key

TOKEN = get_str_key("TOKEN", required=True)
NAME = TOKEN.split(":")[0]

tbot = TelegramClient(
    NAME, get_int_key("APP_ID", required=True), get_str_key("APP_HASH", required=True)
)

# Telethon
tbot.start(bot_token=TOKEN)
