from contextlib import suppress

from Sophia.modules.utils.user_details import is_user_admin
from Sophia.etc.mongo import db
from Sophia.utils.logger import log

DISABLABLE_COMMANDS = []


def disableable_dec(command):
    log.debug(f"Adding {command} to the disableable commands...")

    if command not in DISABLABLE_COMMANDS:
        DISABLABLE_COMMANDS.append(command)

    def wrapped(func):
        async def wrapped_1(*args, **kwargs):
            message = args[0]

            chat_id = message.chat.id
            user_id = message.from_user.id
            cmd = command

            with suppress(KeyError):
                if command in (aliases := message.conf["cmds"]):
                    cmd = aliases[0]

            check = await db.disabled.find_one(
                {"chat_id": chat_id, "cmds": {"$in": [cmd]}}
            )
            if check and not await is_user_admin(chat_id, user_id):
                return
            return await func(*args, **kwargs)

        return wrapped_1

    return wrapped
