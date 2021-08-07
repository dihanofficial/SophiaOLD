"""
XIT License 2021
Copyright (c) 2021 Dihan Official
"""
import asyncio
import os
import subprocess
import time

import psutil
from pyrogram import filters

from Sophia import (bot_start_time, DEV_USERS, pbot)
from Sophia.utils import formatter

__mod_name__ = "💞Sudoers💞"

__help__ = """
*Only for group owner:*
 - /stats - To Check System Status.
 - /gstats - Comming Soon 
 - /gban - Comming Soon 
 - /broadcast - Comming Soon 
 - /update - Comming Soon 
"""


# Stats Module


async def bot_sys_stats():
    bot_uptime = int(time.time() - bot_start_time)
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    process = psutil.Process(os.getpid())
    stats = f"""
root@DihanOfficial:~$ Sophia 
------------------
UPTIME: {formatter.get_readable_time((bot_uptime))}
BOT: {round(process.memory_info()[0] / 1024 ** 2)} MB
CPU: {cpu}%
RAM: {mem}%
DISK: {disk}%
"""
    return stats

#@pbot.on_message(
#    filters.command("broadcast") & filters.user(DEV_USERS) & ~filters.edited
#)
#@capture_err
#async def broadcast_message(_, message):
#    if len(message.command) < 2:
#        return await message.reply_text("**Usage**:\n/broadcast [MESSAGE]")
#    text = message.text.split(None, 1)[1]
#    sent = 0
#    chats = []
#    schats = await get_served_chats()
#    for chat in schats:
#        chats.append(int(chat["chat_id"]))
#    for i in chats:
#        try:
#            await app.send_message(i, text=text)
#            sent += 1
#        except Exception:
#            pass
#    await message.reply_text(f"**Broadcasted Message In {sent} Chats.**")



@app.on_message(filters.command("gban") & filters.user(SUDOERS))
@capture_err
async def ban_globally(_, message):
    user_id, reason = await extract_user_and_reason(message)
    user = await app.get_users(user_id)
    from_user = message.from_user

    if not user_id:
        return await message.reply_text("I can't find that user.")
    if not reason:
        return await message.reply("No reason provided.")

    if user_id in ([from_user.id, BOT_ID] + SUDOERS):
        return await message.reply_text("No")

    served_chats = await get_served_chats()
    m = await message.reply_text(
        f"**Banning {user.mention} Globally!**"
        + f" **This Action Should Take About {len(served_chats)} Seconds.**"
    )
    await add_gban_user(user_id)
    number_of_chats = 0
    for served_chat in served_chats:
        try:
            await app.kick_chat_member(
                served_chat["chat_id"], user.id
            )
            number_of_chats += 1
            await asyncio.sleep(1)
        except FloodWait as e:
            await asyncio.sleep(int(e.x))
        except Exception:
            pass
    try:
        await app.send_message(
            user.id,
            f"Hello, You have been globally banned by {from_user.mention},"
            + " You can appeal for this ban by talking to him.",
        )
    except Exception:
        pass
    await m.edit(f"Banned {user.mention} Globally!")
    ban_text = f"""
__**New Global Ban**__
**Origin:** {message.chat.title} [`{message.chat.id}`]
**Admin:** {from_user.mention}
**Banned User:** {user.mention}
**Banned User ID:** `{user_id}`
**Reason:** __{reason}__
**Chats:** `{number_of_chats}`"""
    try:
        m2 = await app.send_message(
            GBAN_LOG_GROUP_ID,
            text=ban_text,
            disable_web_page_preview=True,
        )
        await m.edit(
            f"Banned {user.mention} Globally!\nAction Log: {m2.link}",
            disable_web_page_preview=True,
        )
    except Exception:
        await message.reply_text(
            "User Gbanned, But This Gban Action Wasn't Logged, Add Me Bot In GBAN_LOG_GROUP"
        )


# Ungban


@app.on_message(filters.command("ungban") & filters.user(SUDOERS))
@capture_err
async def unban_globally(_, message):
    user_id = await extract_user(message)
    if not user_id:
        return await message.reply_text("I can't find that user.")
    user = await app.get_users(user_id)

    is_gbanned = await is_gbanned_user(user.id)
    if not is_gbanned:
        await message.reply_text("I don't remember Gbanning him.")
    else:
        await remove_gban_user(user.id)
        await message.reply_text(
            f"Lifted {user.mention}'s Global Ban.'"
        )


# Broadcast


@app.on_message(
    filters.command("broadcast")
    & filters.user(SUDOERS)
    & ~filters.edited
)
@capture_err
async def broadcast_message(_, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage**:\n/broadcast [MESSAGE]"
        )
    sleep_time = 0.1
    text = message.text.split(None, 1)[1]
    sent = 0
    schats = await get_served_chats()
    chats = [int(chat["chat_id"]) for chat in schats]
    m = await message.reply_text(
        f"Broadcast in progress, will take {len(chats) * sleep_time} seconds."
    )
    for i in chats:
        try:
            await app.send_message(i, text=text)
            await asyncio.sleep(sleep_time)
            sent += 1
        except FloodWait as e:
            await asyncio.sleep(int(e.x))
        except Exception:
            pass
    await m.edit(f"**Broadcasted Message In {sent} Chats.**")






# Update


@app.on_message(filters.command("update") & filters.user(SUDOERS))
async def update_restart(_, message):
    try:
        await message.reply_text(
            f'```{subprocess.check_output(["git", "pull"]).decode("UTF-8")}```'
        )
    except Exception as e:
        return await message.reply_text(str(e))
    m = await message.reply_text(
        "**Updated with default branch, restarting now.**"
    )
    await restart(m)
