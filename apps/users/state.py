from aiogram.dispatcher.filters.state import State, StatesGroup


class IdentificationState(StatesGroup):
    code = State()