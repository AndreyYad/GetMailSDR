from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import generic

storage = MemoryStorage()

dp = Dispatcher(storage=storage)

dp.include_routers(
    generic.router
)