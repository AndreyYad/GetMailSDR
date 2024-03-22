from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from re import fullmatch

from modules.text import Text
from modules.bot_commands import send_msg, reply_msg, check_membering
from modules.database import save_email, get_email, delete_email
from modules.states import FSMClient

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

async def set_get_email_func(msg: types.Message, state: FSMContext):
    await state.set_state(FSMClient.get_email)
    await send_msg(msg.chat.id, Text.enter_email)

async def cancel_func(msg: types.Message, state: FSMContext):
    await state.clear()
    await reply_msg(msg, Text.cancel)

async def save_email_func(msg: types.Message, state: FSMContext):
    # if not fullmatch(r'[A-Za-z0-9._%+-]+@proton(\.me|mail\.com)', msg.text):
    #     await reply_msg(msg, Text.not_correсt_email)
    #     return
    if not await check_membering(msg.from_user.id):
        await reply_msg(msg, Text.not_chat_member)
        return
    user = msg.from_user
    await save_email(user, msg.text)
    await reply_msg(msg, Text.email_save)
    await state.clear()
    print(f'@{user.username} - {msg.text}')

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
    router.message.register(cancel_func, Command('cancel'), ~StateFilter(default_state))
    router.message.register(save_email_func, StateFilter(FSMClient.get_email))
    router.message.register(start_func, CommandStart())
    router.message.register(get_saved_email_func, Command('my_email'))
    router.message.register(delete_email_func, Command('delete'))
    router.message.register(set_get_email_func, Command('email'))