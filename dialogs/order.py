import logging
from typing import Any
from psycopg.connection_async import AsyncConnection

from aiogram import Bot, Router
from aiogram.types import CallbackQuery, Message, User, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.api.entities import Context
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Column, ScrollingGroup, Select

from lexicon.lexicon import LEXICON_RU, ORDER_DATA
from FSM.FSM import OrderSG
from database.db import (
    update_user_order,
    get_price
)

router = Router()

logger = logging.getLogger(__name__)


async def location_callback_click(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data['username'] = callback.from_user.username if callback.from_user.username is not None else callback.from_user.first_name
    dialog_manager.dialog_data['location'] = callback.data
    await dialog_manager.next()


async def drink_category(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data['category'] = callback.data
    await dialog_manager.next()


async def coffee_callback_click(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: Any):
    dialog_manager.dialog_data['coffee'] = item_id
    await dialog_manager.next()


async def volume_callback_click(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: Any):
    dialog_manager.dialog_data['volume'] = item_id
    if dialog_manager.dialog_data['coffee'] in ['americano', 'espresso_x2']:
        dialog_manager.dialog_data['coffee_base'] = 'nothing'
        await dialog_manager.switch_to(state=OrderSG.set_sugar)
    else:
        await dialog_manager.next()


async def base_callback_click(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: Any):
    dialog_manager.dialog_data['coffee_base'] = item_id
    await dialog_manager.next()


async def sugar_callback_click(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: Any):
    dialog_manager.dialog_data['sugar'] = item_id
    await dialog_manager.next()


async def toppings_callback_click(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: Any):
    dialog_manager.dialog_data['toppings'] = item_id
    await dialog_manager.next()


async def additional_callback_click(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: Any):
    dialog_manager.dialog_data['additional'] = item_id
    await dialog_manager.next()


async def get_order(dialog_manager: DialogManager, bot: Bot, **kwargs):
    order_info = dialog_manager.dialog_data
    order_id = dialog_manager.start_data
    logger.info(f'Данные по заказу >>>> {order_id} >>> {order_info}')

    order_price = await calculating_price(dialog_manager.middleware_data['conn'], order_info)
    order_info['price'] = order_price

    await send_order_to_group(bot, order_id['order_id'], order_info)
    await update_user_order(dialog_manager.middleware_data['conn'],
                            order_id=order_id['order_id'],
                            location=order_info["location"],
                            category=order_info["category"],
                            coffee=order_info["coffee"],
                            volume=order_info["volume"],
                            coffee_base=order_info["coffee_base"],
                            sugar=order_info["sugar"],
                            toppings=order_info["toppings"],
                            additional=order_info["additional"],
                            price=order_price
                            )

    return {
        'location': ORDER_DATA['location'].get(order_info.get('location')),
        'volume': ORDER_DATA['volume'].get(order_info.get('volume')),
        'coffee': ORDER_DATA['coffee'][order_info.get('category')].get(dialog_manager.dialog_data.get('coffee')),
        'coffee_base': ORDER_DATA['coffee_base'].get(order_info.get('coffee_base'), 'Ничего'),
        'sugar': ORDER_DATA['sugar'].get(order_info.get('sugar')),
        'toppings': ORDER_DATA['toppings'].get(order_info.get('toppings')),
        'additional': ORDER_DATA['additional'].get(order_info.get('additional')),
        'price': order_info.get('price')
    }

async def send_order_to_group(bot: Bot, order_id: int, order_info: dict) -> None:
    group_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Взял заказ', callback_data=f'queue:{order_id}')],
            [InlineKeyboardButton(text='Заказ готов', callback_data=f'ready:{order_id}')]
        ]
    )

    await bot.send_message(chat_id=-1003293541701,
                           text=f'Номер заказа: {order_id}\n\n'
                                f'Имя: {order_info["username"]}\n'
                                f'Локация: {ORDER_DATA["location"][order_info.get("location")]}\n'
                                f'Объем: {ORDER_DATA["volume"].get(order_info.get("volume"))}\n'
                                f'Напиток: {ORDER_DATA["coffee"][order_info.get("category")].get(order_info.get("coffee"))}\n'
                                f'Основа кофе: {ORDER_DATA["coffee_base"].get(order_info.get("coffee_base"), "Ничего")}\n'
                                f'Сахар: {ORDER_DATA["sugar"].get(order_info.get("sugar"))}\n'
                                f'Топпинг: {ORDER_DATA["toppings"].get(order_info.get("toppings"))}\n'
                                f'Добавка: {ORDER_DATA["additional"].get(order_info.get("additional"))}\n'
                                f'Цена: {order_info.get("price")}\n',
                           reply_markup=group_keyboard
                           )


async def calculating_price(conn: AsyncConnection, order_info: dict) -> int:
    coffee_price = await get_price(conn, product_name=order_info['coffee'], category=order_info['category'], volume=order_info['volume'])
    order_price = coffee_price

    if order_info['coffee_base'] != 'nothing':
        coffe_base_price = await get_price(conn, product_name=order_info['coffee_base'], category='additional')
        order_price += coffe_base_price

    if order_info['toppings'] != 'nothing':
        topping_price = await get_price(conn, product_name='syrup', category='additional')
        order_price += topping_price

    if order_info['additional'] != 'nothing':
        additional_price = await get_price(conn, product_name=order_info['additional'], category='additional')
        order_price += additional_price

    return order_price


async def back_button_click(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.back()


async def get_volume_menu(aiogd_context: Context,**kwargs):
    data = aiogd_context.dialog_data

    items = [(key, ORDER_DATA["volume"].get(key)) for key in ORDER_DATA["coffee_items"][data.get("coffee")]['sizes']]
    return {"volumes": items}


async def get_coffee_menu(aiogd_context: Context,**kwargs):
    data = aiogd_context.dialog_data

    items = [{"id": key, "label": value} for key, value in ORDER_DATA['coffee'][data.get('category')].items()]
    return {"coffee": items}


async def get_coffee_base_menu(**kwargs):
    items = [(key, value) for key, value in ORDER_DATA.get('coffee_base').items()]
    return {'bases': items}

async def get_sugar_menu(**kwargs):
    items = [(key, value) for key, value in ORDER_DATA.get('sugar').items()]
    return {'sugars': items}


async def get_toppings_menu(dialog_manager: DialogManager, **kwargs):
    items = [(key, value) for key, value in ORDER_DATA.get('toppings').items()]
    return {'toppings': items}


async def get_additional_menu(**kwargs):
    items = [(key, value) for key, value in ORDER_DATA.get("additional").items()]
    return {"additional": items}


order_dialog = Dialog(
    Window(
        Const(text=LEXICON_RU['inline_kb_text']['location']),
        Column(*[Button(text=Format(value), id=key, on_click=location_callback_click) for key, value in ORDER_DATA['location'].items()]),
        state=OrderSG.set_location),

    Window(
        Const(text=LEXICON_RU['inline_kb_text']['category']),
        Column(*[Button(text=Format(value), id=key, on_click=drink_category) for key, value in
                 ORDER_DATA['category'].items()]),
        Button(text=Const('Назад'), id='category_back', on_click=back_button_click),
        state=OrderSG.set_category
    ),

    Window(
        Const(text=LEXICON_RU['inline_kb_text']['coffee']),
        ScrollingGroup(
            Select(
                Format("{item[label]}"),
                id="drink",
                item_id_getter=lambda item: item["id"],
                items="coffee",
                on_click=coffee_callback_click
            ),
            id="coffee_group",
            width=1,
            height=6,
        ),
        Button(text=Const(text='Назад'), id='coffee_back', on_click=back_button_click),
        getter=get_coffee_menu,
        state=OrderSG.set_coffee
    ),

    Window(
        Const(text=LEXICON_RU['inline_kb_text']['volume']),
        Column(
            Select(
                Format('{item[1]}'),
                id="volume",
                item_id_getter=lambda item: item[0],
                items="volumes",
                on_click=volume_callback_click
            )
        ),
        Button(text=Const('Назад'), id='volume_back', on_click=back_button_click),
        getter=get_volume_menu,
        state=OrderSG.set_volume
    ),

    Window(
        Const(text=LEXICON_RU['inline_kb_text']['coffee_base']),
        ScrollingGroup(
            Select(
                Format('{item[1]}'),
                id="coffee_base",
                item_id_getter=lambda item: item[0],
                items="bases",
                on_click=base_callback_click
            ),
            id="base_group",
            width=1,
            height=6
        ),
        Button(text=Const(text='Назад'), id='coffee_base_back', on_click=back_button_click),
        getter=get_coffee_base_menu,
        state=OrderSG.set_coffee_base
    ),

    Window(
        Const(text=LEXICON_RU['inline_kb_text']['sugar']),
        Column(
          Select(
              Format("{item[1]}"),
              id="sugar",
              item_id_getter=lambda item: item[0],
              items="sugars",
              on_click=sugar_callback_click
          ),
        id="sugar_group"
        ),
        Button(text=Const(text='Назад'), id='coffee_base_back', on_click=back_button_click),
        getter=get_sugar_menu,
        state=OrderSG.set_sugar
    ),

    Window(
        Const(text=LEXICON_RU['inline_kb_text']['toppings']),
        ScrollingGroup(
            Select(
                Format('{item[1]}'),
                id='topping',
                item_id_getter=lambda x: x[0],
                items='toppings',
                on_click=toppings_callback_click),
            id="topping_group",
            width=1,
            height=6,
        ),
        Button(text=Const(text='Назад'), id='toppings_back', on_click=back_button_click),
        getter=get_toppings_menu,
        state=OrderSG.set_toppings

    ),
    Window(
        Const(text=LEXICON_RU['inline_kb_text']['additional']),
        ScrollingGroup(
            Select(
                Format('{item[1]}'),
                id='additional',
                item_id_getter=lambda x: x[0],
                items='additional',
                on_click=additional_callback_click
            ),
            id="additional_group",
            width=1,
            height=6,
        ),
        Button(text=Const(text='Назад'), id='additional_back', on_click=back_button_click),
        getter=get_additional_menu,
        state=OrderSG.set_additional
    ),

    Window(
        Const(text='Ваш заказ:\n'),
        Format(text='Локация - {location}\n'
                    'Напиток - {coffee}\n'
                    'Объем - {volume}\n'
                    'Основа кофе - {coffee_base}\n'
                    'Сахар - {sugar}\n'
                    'Топпинг - {toppings}\n'
                    'Добавки - {additional}\n'
                    'Цена - {price} руб.'),
        getter=get_order,
        state=OrderSG.set_finish)
)


@router.message()
async def delete_input_messages(message: Message, bot: Bot):
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
