from datetime import timedelta

# elif raw_button[1] == 'note':
# t = InlineKeyboardButton(raw_button[0], callback_data='get_note_{}_{}'.format(chat_id, raw_button[2]))
# elif raw_button[1] == 'alert':
# t = InlineKeyboardButton(raw_button[0], callback_data='get_alert_{}_{}'.format(chat_id, raw_button[2]))
# elif raw_button[1] == 'deletemsg':
# t = InlineKeyboardButton(raw_button[0], callback_data='get_delete_msg_{}_{}'.format(chat_id, raw_button[2]))


class InvalidTimeUnit(Exception):
    pass


def get_arg(message):
    try:
        return message.get_args().split()[0]
    except IndexError:
        return ""


def get_args(message):
    args = message.get_args().split()
    if args is None:
        # getting args from non-command
        args = message.text.split()
    return args


def get_args_str(message):
    return " ".join(get_args(message))


def get_cmd(message):
    cmd = message.get_command().lower()[1:].split("@")[0]
    return cmd


def convert_time(time_val):
    if not any(time_val.endswith(unit) for unit in ("m", "h", "d")):
        raise TypeError

    time_num = int(time_val[:-1])
    unit = time_val[-1]
    kwargs = {}

    if unit == "m":
        kwargs["minutes"] = time_num
    elif unit == "h":
        kwargs["hours"] = time_num
    elif unit == "d":
        kwargs["days"] = time_num
    else:
        raise InvalidTimeUnit()

    val = timedelta(**kwargs)

    return val


def convert_timedelta(time):
    return {"days": time.days, "seconds": time.seconds}


def need_args_dec(num=1):
    def wrapped(func):
        async def wrapped_1(*args, **kwargs):
            message = args[0]
            if len(message.text.split(" ")) > num:
                return await func(*args, **kwargs)
            else:
                await message.reply("Give me args!")

        return wrapped_1

    return wrapped
