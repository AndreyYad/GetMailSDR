from aiogram.fsm.state import StatesGroup, State

class FSMClient(StatesGroup):
    get_email = State()