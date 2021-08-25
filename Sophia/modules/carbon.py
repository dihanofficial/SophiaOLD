#import os

#from pyrogram import filters

#from Sophia import pbot
#from Sophia.core.decorators.errors import capture_err
#from Sophia.utils.functions import make_carbon


#__mod_name__ = "⚡️Carbon⚡️"

#__help__ = """
# *Help for Carbon Module:*

#Commands
# ❍ /carbon : Reply to a text message to make carbon.
#"""

#@app.on_message(filters.command("carbon"))
#@capture_err
#async def carbon_func(_, message):
#    if not message.reply_to_message:
#        return await message.reply_text(
#            "Reply to a text message to make carbon."
#        )
#    if not message.reply_to_message.text:
#        return await message.reply_text(
#            "Reply to a text message to make carbon."
#        )
#    m = await message.reply_text("Preparing Carbon")
#    carbon = await make_carbon(message.reply_to_message.text)
#    await m.edit("Uploading")
#    await app.send_document(message.chat.id, carbon)
#    await m.delete()
#    carbon.close()
