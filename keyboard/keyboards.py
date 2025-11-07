from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from lexicon.lexicon import ORDER_DATA


class OrderCallBackData(CallbackData, prefix='order'):
    user_choose: str
    number_order: int

def split_dict(d: dict, n: int) -> dict[int, dict]:
    items = list(d.items())
    length = len(items)

    result = {i + 1: dict(items[i * n:(i + 1) * n]) for i in range((length + n - 1) // n)}

    return result


def create_inline_kb(button_data: dict, index: int, number_order: int) -> InlineKeyboardMarkup:

    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    splited_dict = split_dict(button_data, 5)

    # Заполняем список кнопками из аргументов args и kwargs
    if splited_dict:
        for key, button in splited_dict.get(index).items():
            buttons.append(InlineKeyboardButton(
                text=button,
                callback_data=OrderCallBackData(user_choose=key, number_order=number_order).pack()
            ))

    kb_builder.row(*buttons, width=1)

    if len(splited_dict) > 1:
        forward = InlineKeyboardButton(text='>>', callback_data=OrderCallBackData(user_choose='forward', number_order=number_order).pack())
        pagination = InlineKeyboardButton(text=f'{str(index)}/{str(len(splited_dict))}', callback_data=OrderCallBackData(user_choose='pagination', number_order=number_order).pack())
        backward = InlineKeyboardButton(text='<<', callback_data=OrderCallBackData(user_choose='backward', number_order=number_order).pack())

        kb_builder.row(*[backward, pagination, forward], width=3)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()