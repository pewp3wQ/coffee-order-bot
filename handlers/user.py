import logging
from copy import deepcopy

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from config.config import load_config, Config
from lexicon.lexicon import LEXICON_RU, ORDER_DATA, GROUP_BUTTONS
from keyboard.keyboards import create_inline_kb, split_dict, OrderCallBackData
from FSM.FSM import FSMOrderCoffee

router = Router()
logger = logging.getLogger(__name__)
config: Config = load_config()


@router.message(CommandStart(),
                F.chat.type != 'supergroup',
                StateFilter(default_state))
async def process_location_command(message: Message, db: dict, state: FSMContext):
    if message.from_user.id not in db["users"]:
        db["users"][message.from_user.id] = deepcopy(db.get("user_template"))

    db["users"][message.from_user.id]["order_step"] = 'location'
    number_order = db["number_order"]

    logger.info(f'Пользователь: {message.from_user.username} - ID: {message.from_user.id} - начал свой заказ')
    await message.answer(text=LEXICON_RU['inline_kb_text'].get('location'),
                         reply_markup=create_inline_kb(
                             button_data=ORDER_DATA.get('location'),
                             index=db["users"][message.from_user.id]['page'],
                             number_order=number_order))

    db["number_order"] += 1
    await state.set_state(FSMOrderCoffee.choose_volume)


@router.callback_query(OrderCallBackData.filter(
    F.user_choose.in_([coffee_name for coffee_name in ORDER_DATA.get('location').keys()])),
    StateFilter(FSMOrderCoffee.choose_volume))
async def show_volume_menu(callback: CallbackQuery, db: dict, callback_data: OrderCallBackData, state: FSMContext):
    db["users"][callback.from_user.id]["current_order"].get('location', 'location')
    db["users"][callback.from_user.id]["current_order"]["location"] = ORDER_DATA["location"].get(callback_data.user_choose)

    x = await callback.answer()
    await callback.message.edit_text(text=LEXICON_RU['inline_kb_text'].get('volume'),
                                     reply_markup=create_inline_kb(
                                         button_data=ORDER_DATA.get('volume'),
                                         index=db["users"][callback.from_user.id]['page'],
                                         number_order=callback_data.number_order))

    db["users"][callback.from_user.id]["order_step"] = 'volume'
    await state.set_state(FSMOrderCoffee.choose_coffee)


@router.callback_query(OrderCallBackData.filter(
    F.user_choose.in_([coffee_name for coffee_name in ORDER_DATA.get('volume').keys()])),
    StateFilter(FSMOrderCoffee.choose_coffee))
async def show_coffee_menu(callback: CallbackQuery, db: dict, callback_data: OrderCallBackData, state: FSMContext):
    db["users"][callback.from_user.id]["current_order"].get('volume', 'volume')
    db["users"][callback.from_user.id]["current_order"]["volume"] = ORDER_DATA["volume"].get(callback_data.user_choose)

    await callback.answer()
    await callback.message.edit_text(text=LEXICON_RU['inline_kb_text'].get('coffee'),
                                     reply_markup=create_inline_kb(
                                         button_data=ORDER_DATA.get('coffee'),
                                         index=db["users"][callback.from_user.id]['page'],
                                     number_order=callback_data.number_order))

    db["users"][callback.from_user.id]["order_step"] = 'coffee'
    await state.set_state(FSMOrderCoffee.choose_toppings)


@router.callback_query(OrderCallBackData.filter(
    F.user_choose.in_([coffee_name for coffee_name in ORDER_DATA.get('coffee').keys()])),
    StateFilter(FSMOrderCoffee.choose_toppings))
async def show_volume_menu(callback: CallbackQuery, db: dict, callback_data: OrderCallBackData, state: FSMContext):
    db["users"][callback.from_user.id]["current_order"].get('coffee', 'coffee')
    db["users"][callback.from_user.id]["current_order"]["coffee"] = ORDER_DATA["coffee"].get(callback_data.user_choose)
    # Сброс паггинации
    db["users"][callback.from_user.id]['page'] = 1

    await callback.answer()
    await callback.message.edit_text(text=LEXICON_RU['inline_kb_text'].get('toppings'),
                                     reply_markup=create_inline_kb(
                                         button_data=ORDER_DATA.get('toppings'),
                                         index=db["users"][callback.from_user.id]['page'],
                                     number_order=callback_data.number_order))

    db["users"][callback.from_user.id]["order_step"] = 'toppings'
    await state.set_state(FSMOrderCoffee.finish_order)


@router.callback_query(OrderCallBackData.filter(
    F.user_choose.in_([coffee_name for coffee_name in ORDER_DATA.get('toppings').keys()])),
    StateFilter(FSMOrderCoffee.finish_order))
async def show_volume_menu(callback: CallbackQuery, bot: Bot, db: dict, callback_data: OrderCallBackData, state: FSMContext):
    db["users"][callback.from_user.id]["current_order"].get('toppings', 'toppings')
    db["users"][callback.from_user.id]["current_order"]["toppings"] = ORDER_DATA["toppings"].get(callback_data.user_choose)

    await callback.answer()
    await bot.send_message(chat_id=callback.from_user.id,
                           text=f'Ваш заказ будет готов на: '
                                f'{db["users"][callback.from_user.id]["current_order"]["location"]}\n'
                                f'Объем: {db["users"][callback.from_user.id]["current_order"]["volume"]}\n'
                                f'Напиток: {db["users"][callback.from_user.id]["current_order"]["coffee"]}\n'
                                f'Топпинг: {db["users"][callback.from_user.id]["current_order"]["toppings"]}\n')

    logger.info(f'Пользователь: '
                f'{callback.message.chat.username} - ID: {callback.message.chat.id} - закончил свой заказ')
    logger.info(callback.model_dump_json())

    db["users"][callback.from_user.id]["current_order"]["name"] = callback.message.chat.username
    db["users"][callback.from_user.id]["current_order"]["user_id"] = callback.message.chat.id

    db["history_order"].update({callback_data.number_order: db["users"][callback.from_user.id]["current_order"]})

    await bot.delete_message(chat_id=callback.from_user.id,
                             message_id=callback.message.message_id)

    await send_order_to_group(bot, callback.from_user.id, db["users"], callback_data.number_order)
    # await state.set_state(FSMOrderCoffee.wait_order)
    print(db)
    print(await state.get_state())
    await state.clear()


# @router.message()
# async def send_order_to_group(bot: Bot, user_id: int, db: dict[int, dict[str, dict]], number_order: int):
#     print('прошел в wait_order')
#     match db[user_id]["current_order"]["location"]:
#         case '202-микр':
#             print('прошел матч 202 микр')
#             x = await bot.send_message(text=f'Заказ № {number_order}\n\n'
#                                         f'Имя: {db[user_id]["current_order"]["name"]}\n'
#                                         f'Объем: {db[user_id]["current_order"]["volume"]}\n'
#                                         f'Напиток: {db[user_id]["current_order"]["coffee"]}\n'
#                                         f'Топпинг: {db[user_id]["current_order"]["toppings"]}\n',
#                                    chat_id=-1003293541701,
#                                    reply_markup=create_inline_kb(GROUP_BUTTONS, 1, number_order))
#             logger.info(x.message_id)

async def send_order_to_group(bot: Bot, user_id: int, db: dict[int, dict[str, dict]], number_order: int):
    match db[user_id]["current_order"]["location"]:
        case '202-микр':
            print('прошел матч 202 микр')
            x = await bot.send_message(text=f'Заказ № {number_order}\n\n'
                                        f'Имя: {db[user_id]["current_order"]["name"]}\n'
                                        f'Объем: {db[user_id]["current_order"]["volume"]}\n'
                                        f'Напиток: {db[user_id]["current_order"]["coffee"]}\n'
                                        f'Топпинг: {db[user_id]["current_order"]["toppings"]}\n',
                                   chat_id=config.group.group_id,
                                   reply_markup=create_inline_kb(GROUP_BUTTONS, 1, number_order))
            logger.info(x.message_id)

        case 'Орджоникидзе':
            print('прошел матч ордж')
            x = await bot.send_message(chat_id=config.group.group_id,
                                   text=f'Заказ № {number_order}\n\n'
                                        f'Имя: {db[user_id]["current_order"]["name"]}\n'
                                        f'Объем: {db[user_id]["current_order"]["volume"]}\n'
                                        f'Напиток: {db[user_id]["current_order"]["coffee"]}\n'
                                        f'Топпинг: {db[user_id]["current_order"]["toppings"]}\n',
                                   message_thread_id=config.group.thread_id,
                                   reply_markup=create_inline_kb(GROUP_BUTTONS, 1, number_order))
            logger.info(x.message_id)


@router.callback_query(OrderCallBackData.filter(F.user_choose == 'forward'))
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


@router.callback_query(OrderCallBackData.filter(F.user_choose == 'backward'))
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