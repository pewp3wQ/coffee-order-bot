from aiogram.fsm.state import State, StatesGroup


class FSMOrderCoffee(StatesGroup):
    choose_volume = State()
    choose_coffee = State()
    choose_toppings = State()
    rotate_coffee = State()
    choose_milks = State()
    choose_additional = State()
    finish_order = State()
    wait_order = State()