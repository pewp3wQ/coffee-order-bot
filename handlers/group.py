import logging

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from psycopg.connection_async import AsyncConnection

from config.config import Config, load_config
from database.db import get_user_from_order

config: Config = load_config()
router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(F.data.split(':')[0] == 'queue')
async def took_order(callback: CallbackQuery, bot: Bot, conn: AsyncConnection):
    logger.info('Прошел в хендлер взятия заказа в работу')
    order_id = callback.data.split(':')[1]
    user_id = await get_user_from_order(conn, order_id=int(order_id))

    group_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Заказ готов', callback_data=f'ready:{order_id}')]
        ]
    )

    await callback.answer()
    await callback.message.edit_text(text=callback.message.text, reply_markup=group_keyboard)
    await bot.send_message(chat_id=user_id, text='Заказ взять в работу')


@router.callback_query(F.data.split(':')[0] == 'ready')
async def took_order(callback: CallbackQuery, bot: Bot, conn: AsyncConnection):
    logger.info('Прошел в хендлер готовоность заказа')

    order_id = callback.data.split(':')[1]
    user_id = await get_user_from_order(conn, order_id=int(order_id))

    await bot.send_message(chat_id=user_id, text='Заказ готов')
    await callback.answer()

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Заказ выполнен", callback_data="finish")]])

    await callback.message.edit_text(text=callback.message.text, reply_markup=keyboard)


@router.callback_query(F.data == 'finish', F.message.chat.id == config.group.group_id)
async def took_order(callback: CallbackQuery):
        await callback.answer()


# @router.callback_query()
# async def took_order(callback: CallbackQuery):
#         await callback.answer(text='asd')