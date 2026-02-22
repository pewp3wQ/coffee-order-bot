from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from lexicon.lexicon import ORDER_DATA


async def send_order_to_group(bot: Bot, order_id: int, order_info: tuple) -> None:
    group_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Взял заказ', callback_data=f'queue:{order_id}')],
            [InlineKeyboardButton(text='Заказ готов', callback_data=f'ready:{order_id}')]
        ]
    )

    text = f'Номер заказа: {order_id}\n\n' \
           f'Имя: {order_info[1]}\n' \
           f'Локация: {ORDER_DATA["location"][order_info[2]]}\n' \
           f'Напиток: {ORDER_DATA["coffee"][order_info[3]].get(order_info[4])}\n' \
           f'Объем: {ORDER_DATA["volume"].get(order_info[5])}\n' \
           f'Мололо: {ORDER_DATA["coffee_base"].get(order_info[6], "Без молока")}\n' \
           f'Сахар: {ORDER_DATA["sugar"].get(order_info[7])}\n' \
           f'Сироп: {ORDER_DATA["toppings"].get(order_info[8])}\n' \
           f'Добавка: {ORDER_DATA["additional"].get(order_info[9])}\n' \
           f'Горячий кофе: {ORDER_DATA["temperature"].get(order_info[10])}\n' \
           f'Ожидание: {ORDER_DATA["wait_time"].get(order_info[11])}\n' \
           f'Цена: {order_info[12]}\n'

    if order_info[2] == "ordzhonikidze":
        await bot.send_message(chat_id=-1003293541701,
                               text=text,
                               reply_markup=group_keyboard,
                               message_thread_id=3
                               )
    elif order_info[2] == "microdistrict":
        await bot.send_message(chat_id=-1003293541701,
                               text=text,
                               reply_markup=group_keyboard,
                               message_thread_id=18)