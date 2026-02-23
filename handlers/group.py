import logging

from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramForbiddenError
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
    try:
        await callback.answer()
        await callback.message.edit_text(text=callback.message.text, reply_markup=group_keyboard)
        await bot.send_message(chat_id=user_id, text='Заказ взят в работу')
    except TelegramForbiddenError as e:
        block_from_user_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Пользователь заблокировал бота', callback_data='user_block_bot')]
            ]
        )

        await callback.message.edit_text(text=callback.message.text, reply_markup=block_from_user_keyboard)
        logger.error(f'Пользователь {user_id} -- {callback.from_user.username} заблокировал бота {e}')
    except Exception as e:
        logger.error(f'Произошла ошибка: {e}')


@router.callback_query(F.data.split(':')[0] == 'ready')
async def took_order(callback: CallbackQuery, bot: Bot, conn: AsyncConnection):
    logger.info('Прошел в хендлер готовоность заказа')

    order_id = callback.data.split(':')[1]
    user_id = await get_user_from_order(conn, order_id=int(order_id))

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Заказ выполнен", callback_data="finish")]])

    try:
        await callback.answer()
        await bot.send_message(chat_id=user_id, text='Заказ готов')
        await callback.message.edit_text(text=callback.message.text, reply_markup=keyboard)
    except TelegramForbiddenError as e:
        block_from_user_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Пользователь заблокировал бота', callback_data='user_block_bot')]
            ]
        )

        await callback.message.edit_text(text=callback.message.text, reply_markup=block_from_user_keyboard)
        logger.error(f'Пользователь {user_id} -- {callback.from_user.username} заблокировал бота {e}')
    except Exception as e:
        logger.error(f'Произошла ошибка: {e}')


@router.callback_query(F.data.in_({'finish', 'user_block_bot'}))
async def answer_to_callback(callback: CallbackQuery):
        await callback.answer()

