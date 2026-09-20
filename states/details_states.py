from aiogram.fsm.state import State, StatesGroup


class DetailsStates(StatesGroup):
    entering_card = State()