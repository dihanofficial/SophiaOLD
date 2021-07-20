# Special Thanks For Daisy X

# This file is part of SophiaSLBot (Telegram Bot)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.


# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.



from pyrogram import filters

from Sophia.pyrogramee.pluginshelper import admins_only
from Sophia.pyrogramee.pyrogram import pbot as app


@app.on_message(filters.command("webss") & ~filters.private & ~filters.edited)
@admins_only
async def take_ss(_, message):
    if len(message.command) != 2:
        await message.reply_text("Give A Url To Fetch Screenshot.")
        return
    url = message.text.split(None, 1)[1]
    m = await message.reply_text("**Taking Screenshot**")
    await m.edit("**Uploading**")
    try:
        await app.send_photo(
            message.chat.id,
            photo=f"https://webshot.amanoteam.com/print?q={url}",
        )
    except TypeError:
        await m.edit("No Such Website.")
        return
    await m.delete()
