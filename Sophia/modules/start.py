from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton



@Client.on_message(
    filters.command("start")
    & filters.private
    & ~ filters.edited
)
async def start_(client: Client, message: Message):
    await message.reply_sticker("CAACAgIAAxkBAAEDF6Rgrcl1kZNSrAABqO7L-kVd4tWK48MAAi0BAAIw1J0REIYEuS-exNEeBA")
    await message.reply_text(
        f"""<b> Hey,👋 {message.from_user.first_name}!
\n Hello 👋 there! Hey there! My name is 𝗦𝗼𝗽𝗵𝗶𝗮.
I can help manage your groups with useful features, feel free to add me to your groups!.
 </b>""",
      
       
        reply_markup=InlineKeyboardMarkup(
                [
                    [
                          InlineKeyboardButton(
                               text="➕ Add Sophia to your Group ➕", url="t.me/SophiaSLBot?startgroup=true"),
                   ],
                   [
                         InlineKeyboardButton(text="Source Code 🗒️", callback_data="source_"),
                         InlineKeyboardButton(
                                 text="System Stats 💻", callback_data="stats_callback"
                       ),
                  ],
                  [
                        InlineKeyboardButton(text="🙋‍♀️ Sophia News", url=f"https://t.me/dihanofficial"),
                        InlineKeyboardButton(
                                text="💬 Support Group", url=f"https://t.me/dihan_official"
                       ),
                   ],
                   [
                        InlineKeyboardButton(text="❓ Commands Help ", callback_data="help_back"),
                   ],
          ]
       ]
      )
    )
