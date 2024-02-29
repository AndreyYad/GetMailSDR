from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command

from modules.text import Text
from modules.bot_commands import send_msg, reply_msg, check_membering
from modules.database import save_email, get_email, delete_email

router = Router()

async def start_func(msg: types.Message):
    await send_msg(
        msg.chat.id, 
        Text.start_text
    )

    # print(await check_membering(msg.from_user.id))

    # from pprint import PrettyPrinter
    # pp = PrettyPrinter(indent=4)
    # pp.pprint(msg.__dict__)

async def save_email_func(msg: types.Message):
    if not await check_membering(msg.from_user.id):
        await reply_msg(msg, Text.not_chat_member)
        return
    user = msg.from_user
    await save_email(user, msg.text)
    await reply_msg(msg, Text.email_save)

async def get_saved_email_func(msg: types.Message):
    email = await get_email(msg.from_user.id)
    if email:
        await reply_msg(msg, Text.your_email.format(email))
    else:
        await reply_msg(msg, Text.email_is_none)

async def delete_email_func(msg: types.Message):
    if await delete_email(msg.from_user.id):
        await reply_msg(msg, Text.delete_email)
    else:
        await reply_msg(msg, Text.email_is_none)

async def register_generic_handlers():
    router.message.register(lambda msg: print(msg.chat.id), Command('id'))
    router.message.register(lambda msg: None, ~((F.chat.type == 'private') & (F.content_type == 'text')))
    router.message.register(start_func, CommandStart())
    router.message.register(get_saved_email_func, Command('my_email'))
    router.message.register(delete_email_func, Command('delete'))
    router.message.register(save_email_func)