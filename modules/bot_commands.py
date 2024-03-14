'''
Модуль с командами для бота
'''
from aiogram import types

from bot.bot import bot
from modules.config import CHAT_ID

empty_markups = types.InlineKeyboardMarkup(inline_keyboard=[[]])

async def send_msg(chat_id: int, text: str, markup: types.InlineKeyboardMarkup=empty_markups, **kwargs):
    '''Отправка сообщения'''
    return await bot.send_message(chat_id, text, reply_markup=markup, **kwargs)

async def reply_msg(msg: types.Message, text: str, markup: types.InlineKeyboardMarkup=empty_markups, **kwargs):
    '''Ответ на сообщение'''
    return await msg.reply(text, reply_markup=markup, **kwargs)
        
async def delete_msg(chat_id: int, msg_id: int):
    '''Удаление сообщения'''
    await bot.delete_message(chat_id, msg_id)

async def check_membering(user_id: int, debug: bool=False):
    if debug:
        print(await bot.get_chat_member(CHAT_ID, user_id))
    return (await bot.get_chat_member(CHAT_ID, user_id)).status._value_ not in ['left', 'kicked']