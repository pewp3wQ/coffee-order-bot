import logging

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from psycopg.connection_async import AsyncConnection

from config.config import load_config, Config
from lexicon.lexicon import LEXICON_RU, ORDER_DATA, GROUP_BUTTONS
from keyboard.keyboards import create_inline_kb, split_dict, OrderCallBackData
from FSM.FSM import FSMOrderCoffee
from database.db import (
    add_user,
    change_user_alive_status,
    get_user_alive_status,
    get_order_id,
    update_user_order,
    add_price,
    get_price
)


router = Router()
logger = logging.getLogger(__name__)
config: Config = load_config()


@router.message(Command('price'))
async def add_pice_func(message: Message, conn: AsyncConnection):
    logger.exception('перешел в команду прайс')
    prices = [["chocolate", "toppings", "20", ]]

    for data_list in prices:
        await add_price(conn, product_name=data_list[0], category=data_list[1], volume=data_list[2], price=data_list[3])


@router.message(CommandStart(), F.chat.type != 'supergroup', StateFilter(default_state))
async def process_location_command(message: Message):
    await message.answer(text=LEXICON_RU.get("/start"))


@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы вышли из машины состояний\n\n'
             'Чтобы снова перейти к заполнению анкеты - '
             'отправьте команду /fillform'
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


@router.message(Command(commands="order"), F.chat.type != 'supergroup', StateFilter(default_state))
async def process_location_command(message: Message, conn: AsyncConnection, state: FSMContext):
    logger.info(f'Пользователь: {message.from_user.username} - ID: {message.from_user.id} - начал свой заказ')

    await add_user(conn, user_id=message.from_user.id)
    order_id = await get_order_id(conn, user_id=message.from_user.id)

    await message.answer(text=LEXICON_RU['inline_kb_text'].get('location'),
                         reply_markup=create_inline_kb(
                             button_data=ORDER_DATA.get('location'),
                             index=1,
                             number_order=order_id))

    await state.update_data(user_id=message.from_user.id, name=message.from_user.username)
    await state.set_state(FSMOrderCoffee.choose_volume)



@router.callback_query(OrderCallBackData.filter(
    F.user_choose.in_([location for location in ORDER_DATA.get('location').keys()])),
    StateFilter(FSMOrderCoffee.choose_volume))
async def show_volume_menu(callback: CallbackQuery, callback_data: OrderCallBackData, state: FSMContext):
    await state.update_data(location=callback_data.user_choose)

    await callback.answer()
    await callback.message.edit_text(text=LEXICON_RU['inline_kb_text'].get('volume'),
                                     reply_markup=create_inline_kb(
                                         button_data=ORDER_DATA.get('volume'),
                                         index=1,
                                         number_order=callback_data.number_order))

    await state.set_state(FSMOrderCoffee.choose_coffee)


@router.callback_query(OrderCallBackData.filter(
    F.user_choose.in_([volume for volume in ORDER_DATA.get('volume').keys()])),
    StateFilter(FSMOrderCoffee.choose_coffee))
async def show_coffee_menu(callback: CallbackQuery, callback_data: OrderCallBackData, state: FSMContext):
    await state.update_data(volume=callback_data.user_choose)

    await callback.answer()
    await callback.message.edit_text(text=LEXICON_RU['inline_kb_text'].get('coffee'),
                                     reply_markup=create_inline_kb(
                                         button_data=ORDER_DATA['coffee'].get(callback_data.user_choose),
                                         index=1,
                                         number_order=callback_data.number_order))

    await state.set_state(FSMOrderCoffee.rotate_coffee)


@router.callback_query(OrderCallBackData.filter(), StateFilter(FSMOrderCoffee.rotate_coffee))
async def show_milk_menu(callback: CallbackQuery, callback_data: OrderCallBackData, state: FSMContext):
    await state.update_data(coffee=callback_data.user_choose)

    if callback_data.user_choose == 'americano':
        await state.set_state(FSMOrderCoffee.choose_toppings)
        await callback.answer()
    else:
        await state.set_state(FSMOrderCoffee.choose_milks)
        await callback.answer()

    print(await state.get_state())


@router.callback_query(OrderCallBackData.filter(), StateFilter(FSMOrderCoffee.choose_toppings))
async def show_toppings_menu(callback: CallbackQuery, callback_data: OrderCallBackData, state: FSMContext):
    await state.update_data(milk=callback_data.user_choose)

    await callback.answer()
    await callback.message.edit_text(text=LEXICON_RU['inline_kb_text'].get('toppings'),
                                     reply_markup=create_inline_kb(
                                         button_data=ORDER_DATA.get('toppings'),
                                         index=1,
                                         number_order=callback_data.number_order))

    await state.set_state(FSMOrderCoffee.choose_additional)

# OrderCallBackData.filter(
#     F.user_choose.in_(list({coffee_keys for coffee_dict in ORDER_DATA['coffee'].values() for coffee_keys in coffee_dict.keys()}))),

@router.callback_query(OrderCallBackData.filter(), StateFilter(FSMOrderCoffee.choose_milks))
async def show_milk_menu(callback: CallbackQuery, callback_data: OrderCallBackData, state: FSMContext):
    await state.update_data(coffee=callback_data.user_choose)

    await callback.answer()
    await callback.message.edit_text(text=LEXICON_RU['inline_kb_text'].get('milk'),
                                     reply_markup=create_inline_kb(
                                         button_data=ORDER_DATA.get('milk'),
                                         index=1,
                                         number_order=callback_data.number_order))

    await state.set_state(FSMOrderCoffee.choose_toppings)


@router.callback_query(OrderCallBackData.filter(
    F.user_choose.in_([topping for topping in ORDER_DATA.get('toppings').keys()])),
    StateFilter(FSMOrderCoffee.choose_additional))
async def show_volume_menu(callback: CallbackQuery, callback_data: OrderCallBackData, state: FSMContext):
    await state.update_data(toppings=callback_data.user_choose)

    await callback.answer()
    await callback.message.edit_text(text=LEXICON_RU['inline_kb_text'].get('additional'),
                                     reply_markup=create_inline_kb(
                                         button_data=ORDER_DATA.get('additional'),
                                         index=1,
                                         number_order=callback_data.number_order))

    await state.set_state(FSMOrderCoffee.finish_order)


@router.callback_query(OrderCallBackData.filter(
    F.user_choose.in_([coffee_name for coffee_name in ORDER_DATA.get('additional').keys()])),
    StateFilter(FSMOrderCoffee.finish_order))
async def show_volume_menu(callback: CallbackQuery, bot: Bot, conn: AsyncConnection, callback_data: OrderCallBackData, state: FSMContext):
    await state.update_data(additional=callback_data.user_choose)

    print(await state.get_data())

    current_order_data = await state.get_data()
    order_price = await process_price_calculation(conn, current_order_data)

    await state.update_data(price=order_price)

    await callback.answer()
    await bot.send_message(chat_id=callback.from_user.id,
                           text=f'Принял Ваш заказ\n\n'
                                f'Локация: {ORDER_DATA["location"][current_order_data["location"]]}\n'
                                f'Объем: {ORDER_DATA["volume"][current_order_data["volume"]]}\n'
                                f'Напиток: {ORDER_DATA["coffee"][current_order_data["volume"]][current_order_data["coffee"]]}\n'
                                f'Молоко: {ORDER_DATA["milk"][current_order_data["milk"]]}\n'
                                f'Топпинг: {ORDER_DATA["toppings"][current_order_data["toppings"]]}\n'
                                f'Добавка: {ORDER_DATA["additional"][current_order_data["additional"]]}\n'
                                f'Цена: {order_price} руб.')

    logger.info(f'Пользователь: {callback.message.chat.username} - '
                f'ID: {callback.message.chat.id} - закончил свой заказ')
    logger.info(callback.model_dump_json(indent=4, exclude_none=True))

    await update_user_order(conn,
                            order_id=callback_data.number_order,
                            location=current_order_data["location"],
                            volume=current_order_data["volume"],
                            coffee=current_order_data["coffee"],
                            milk=current_order_data["milk"],
                            toppings=current_order_data["toppings"],
                            additional=current_order_data["additional"],
                            price=order_price
                            )

    await bot.delete_message(chat_id=callback.from_user.id,
                             message_id=callback.message.message_id)

    current_order_data = await state.get_data()

    await send_order_to_group(bot, current_order_data, callback_data.number_order)
    print(await state.get_data())
    await state.clear()


async def send_order_to_group(bot: Bot, db: dict[str, str], number_order: int):
    match db["location"]:
        case 'microdistrict':
            x = await bot.send_message(
                                   text=f'Заказ № {number_order}\n\n'
                                        f'Имя: @{db["name"]}\n'
                                        f'Объем: {ORDER_DATA["volume"][db["volume"]]}\n'
                                        f'Напиток: {ORDER_DATA["coffee"][db["volume"]][db["coffee"]]}\n'
                                        f'Молоко: {ORDER_DATA["milk"][db["milk"]]}\n'
                                        f'Топпинг: {ORDER_DATA["toppings"][db["toppings"]]}\n'
                                        f'Добавка: {ORDER_DATA["additional"][db["additional"]]}\n'
                                        f'Цена: {db["price"]} руб',
                                   chat_id=config.group.group_id,
                                   reply_markup=create_inline_kb(GROUP_BUTTONS, 1, number_order))
            logger.info(x.message_id)

        case 'ordzhonikidze':
            x = await bot.send_message(
                                   text=f'Заказ № {number_order}\n\n'
                                        f'Имя: @{db["name"]}\n'
                                        f'Объем: {ORDER_DATA["volume"][db["volume"]]}\n'
                                        f'Напиток: {ORDER_DATA["coffee"][db["volume"]][db["coffee"]]}\n'
                                        f'Молоко: {ORDER_DATA["milk"][db["milk"]]}\n'
                                        f'Топпинг: {ORDER_DATA["toppings"][db["toppings"]]}\n'
                                        f'Добавка: {ORDER_DATA["additional"][db["additional"]]}\n'
                                        f'Цена: {db["price"]} руб',
                                   chat_id=config.group.group_id,
                                   message_thread_id=config.group.thread_id,
                                   reply_markup=create_inline_kb(GROUP_BUTTONS, 1, number_order))
            logger.info(x.message_id)


async def process_price_calculation(conn: AsyncConnection, order_data: dict) -> int:
    coffee_price = await get_price(conn, product_name=order_data['coffee'], category='coffee', volume=order_data['volume'])
    order_price = coffee_price

    if order_data['coffee_base'] is not None and order_data['coffee_base'] != 'nothing':
        coffee_base_price = await get_price(conn, product_name=order_data['coffee_base'], category='coffee_base')
        order_price += coffee_base_price

    if order_data['toppings'] != 'nothing':
        topping_price = await get_price(conn, product_name='syrup', category='additional')
        order_price += topping_price

    if order_data['additional'] != 'nothing':
        additional_price = await get_price(conn, product_name=order_data['additional'], category='additional')
        order_price += additional_price

    return order_price

@router.callback_query(OrderCallBackData.filter(F.user_choose.is_('forward')))
async def forward_page(callback: CallbackQuery, db: dict, callback_data: OrderCallBackData):
    current_order_page = db["users"][callback.from_user.id]['order_step']
    total_pages = split_dict(ORDER_DATA.get(current_order_page), 5)

    if db["users"][callback.from_user.id]['page'] < len(total_pages):
        db["users"][callback.from_user.id]['page'] += 1
        await callback.message.edit_text(text=LEXICON_RU['inline_kb_text'].get(current_order_page),
                                         reply_markup=create_inline_kb(
                                             button_data=ORDER_DATA.get(current_order_page),
                                             index=db["users"][callback.from_user.id]['page'],
                                             number_order=callback_data.number_order))
    await callback.answer()


@router.callback_query(OrderCallBackData.filter(F.user_choose.is_('backward')))
async def backward_page(callback: CallbackQuery, db: dict, callback_data: OrderCallBackData):
    current_order_page = db["users"][callback.from_user.id]['order_step']

    if db["users"][callback.from_user.id]['page'] > 1:
        db["users"][callback.from_user.id]['page'] -= 1
        await callback.message.edit_text(text=LEXICON_RU['inline_kb_text'].get(current_order_page),
                                         reply_markup=create_inline_kb(
                                             button_data=ORDER_DATA.get(current_order_page),
                                             index=db["users"][callback.from_user.id]['page'],
                                             number_order=callback_data.number_order))
    await callback.answer()


@router.message(Command('/settings'))
async def process_settings(message: Message):
    await message.answer('Вы нажали на настройки')