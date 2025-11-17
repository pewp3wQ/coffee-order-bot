import logging

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from psycopg.connection_async import AsyncConnection

from keyboard.keyboards import OrderCallBackData, create_inline_kb
from database.db import get_user_from_order
from lexicon.lexicon import GROUP_BUTTONS

group_router = Router()
logger = logging.getLogger(__name__)


@group_router.callback_query(F.data.split(':')[0] == 'queue')
async def took_order(callback: CallbackQuery, bot: Bot, conn: AsyncConnection):
    logger.info('Прошел в хендлер взятия заказа в работу')
    order_id = callback.data.split(':')[1]
    user_id = await get_user_from_order(conn, order_id=int(order_id))

    await callback.answer()
    await bot.send_message(chat_id=user_id, text='Заказ взять в работу')


@group_router.callback_query(F.data.split(':')[0] == 'ready')
async def took_order(callback: CallbackQuery, bot: Bot, conn: AsyncConnection):
    logger.info('Прошел в хендлер готовоность заказа')

    order_id = callback.data.split(':')[1]
    user_id = await get_user_from_order(conn, order_id=int(order_id))

    await bot.send_message(chat_id=user_id, text='Заказ готов')
    await callback.answer()

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Заказ выполнен", callback_data="finish")]])

    await bot.edit_message_text(text=callback.message.text,
                                chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                reply_markup=keyboard)


@group_router.callback_query(F.data == 'finish', F.message.chat.id == -1003293541701)
async def took_order(callback: CallbackQuery):
        await callback.answer()