import logging

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from keyboard.keyboards import OrderCallBackData
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from FSM.FSM import FSMOrderCoffee


router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(OrderCallBackData.filter(F.user_choose == 'queue'))
async def took_order(callback: CallbackQuery, bot: Bot, db: dict, callback_data: OrderCallBackData):
    logger.info('Прошел в хендлер взятия заказа')

    await callback.answer()
    user_id = db["history_order"][callback_data.number_order].get("user_id")
    await bot.send_message(chat_id=user_id,
                           text='Заказ взять в работу')


@router.callback_query(OrderCallBackData.filter(F.user_choose == 'ready'))
async def took_order(callback: CallbackQuery, bot: Bot, db: dict, callback_data: OrderCallBackData):
    logger.info('Прошел в хендлер готовоность заказа')

    await callback.answer()
    user_id = db["history_order"][callback_data.number_order].get("user_id")
    await bot.send_message(chat_id=user_id,
                           text='Заказ готов')

    await bot.delete_message(chat_id=callback.message.chat.id,
                             message_id=callback.message.message_id)