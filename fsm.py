from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


class Buy_films(StatesGroup):
    films = State()


class Buy_adv(StatesGroup):
    adv = State()


class Out_money(StatesGroup):
    out = State()
