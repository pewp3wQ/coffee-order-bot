from aiogram.fsm.state import State, StatesGroup


class FSMOrderCoffee(StatesGroup):
    choose_volume = State()
    choose_coffee = State()
    choose_toppings = State()
    finish_order = State()
    wait_order = State()