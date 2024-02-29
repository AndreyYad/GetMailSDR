from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import generic

dp = Dispatcher()

dp.include_routers(
    generic.router
)