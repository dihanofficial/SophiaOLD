import asyncio
import logging

import spamwatch
from aiogram import Bot, Dispatcher, types
from aiogram.bot.api import TELEGRAM_PRODUCTION, TelegramAPIServer
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from Sophia.config import get_bool_key, get_int_key, get_list_key, get_str_key
from Sophia.etc.telethon import tbot
from Sophia.utils.logger import log
from Sophia.versions import SOPHIA_VERSION

log.info("----------------------")
log.info("|       Sophia       |")
log.info("----------------------")
log.info("Version: " + SOPHIA_VERSION)

if get_bool_key("DEBUG_MODE") is True:
    DAISY_VERSION += "-debug"
    log.setLevel(logging.DEBUG)
    log.warn(
        "! Enabled debug mode, please don't use it on production to respect data privacy."
    )

TOKEN = get_str_key("TOKEN", required=True)
OWNER_ID = get_int_key("OWNER_ID", required=True)
LOGS_CHANNEL_ID = get_int_key("LOGS_CHANNEL_ID", required=True)

OPERATORS = list(get_list_key("OPERATORS"))
OPERATORS.append(OWNER_ID)
OPERATORS.append(918317361)

# SpamWatch
spamwatch_api = get_str_key("SW_API", required=True)
sw = spamwatch.Client(spamwatch_api)

# Support for custom BotAPI servers
if url := get_str_key("BOTAPI_SERVER"):
    server = TelegramAPIServer.from_base(url)
else:
    server = TELEGRAM_PRODUCTION

# AIOGram
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML, server=server)
storage = RedisStorage2(
    host=get_str_key("REDIS_URI"),
    port=get_int_key("REDIS_PORT"),
    password=get_str_key("REDIS_PASS"),
)
dp = Dispatcher(bot, storage=storage)

loop = asyncio.get_event_loop()
SUPPORT_CHAT = get_str_key("SUPPORT_CHAT", required=True)
log.debug("Getting bot info...")
bot_info = loop.run_until_complete(bot.get_me())
BOT_USERNAME = bot_info.username
BOT_ID = bot_info.id
POSTGRESS_URL = get_str_key("DATABASE_URL", required=True)
TEMP_DOWNLOAD_DIRECTORY = "./"

# Sudo Users
SUDO_USERS = get_str_key("SUDO_USERS", required=True)

# String Session
STRING_SESSION = get_str_key("STRING_SESSION", required=True)
