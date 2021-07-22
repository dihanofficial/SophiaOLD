import importlib
import time
import re
from sys import argv
from typing import Optional
from pyrogram import filters, idle

from Sophia import (
    ALLOW_EXCL,
    CERT_PATH,
    DONATION_LINK,
    LOGGER,
    OWNER_ID,
    PORT,
    SUPPORT_CHAT,
    TOKEN,
    URL,
    WEBHOOK,
    SUPPORT_CHAT,
    dispatcher,
    StartTime,
    telethn,
    pbot,
    updater,
)

# needed to dynamically load modules
# NOTE: Module order is not guaranteed, specify that in the config file!
from Sophia.modules import ALL_MODULES
from Sophia.modules.helper_funcs.chat_status import is_user_admin
from Sophia.modules.helper_funcs.misc import paginate_modules
from Sophia.modules.sudoers import bot_sys_stats
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.error import (
    BadRequest,
    ChatMigrated,
    NetworkError,
    TelegramError,
    TimedOut,
    Unauthorized,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.ext.dispatcher import DispatcherHandlerStop, run_async
from telegram.utils.helpers import escape_markdown


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


PM_START_TEXT = f"""
Hey there! My name is Sophia.
I can help manage your groups with useful features, feel free to add me to your Groups!  *Hit /help 
Sophia Updates @dihanofficial 
"""

buttons = [
    [
        InlineKeyboardButton(
            text="❓ Help", callback_data="help_back"),
    ],
    [
        InlineKeyboardButton(text="🙋‍♀️ Sophia Updates", callback_data="t.me/dihanofficial"),
        InlineKeyboardButton(
            text="🙋‍♂️ Sophia Support", url=f"https://t.me/dihan_official"
        ),
    ],
    [
        InlineKeyboardButton(text="👨‍🔧 Sophia Logs", callback_data="t.me/SophiaX_Updates"),
        InlineKeyboardButton(
            text="🤴 Developer", url=f"https://t.me/dihanrandila"
        ),
    ],
    [
        InlineKeyboardButton(text="🛠 Source Code ", url=f"https://github.com/dihanrandila"),
        InlineKeyboardButton(
            text="💾 System Stats", callback_data="stats_callback"
        ),
    ],
    [
        InlineKeyboardButton(text="➕ Add Sophia to your Group ➕", url="t.me/SophiaSLBot?startgroup=true"),
    ],
]


