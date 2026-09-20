from aiogram.fsm.state import State, StatesGroup


class DealStates(StatesGroup):
    choosing_method = State()
    choosing_currency = State()
    entering_amount = State()
    entering_description = State()