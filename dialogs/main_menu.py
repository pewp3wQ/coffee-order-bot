import logging

from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import User, CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, StartMode, Window
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button
from datetime import time, timezone, timedelta

from lexicon.lexicon import LEXICON_RU
from database.db import (
    add_user,
    get_order_id
)
from config.config import Config, load_config
from FSM.FSM import StartSG, OrderSG, AdminMenuSG

config: Config = load_config()
logger = logging.getLogger(__name__)
router = Router()


async def start_order_dialog(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    logger.info(f'Пользователь: {callback.from_user.username} - ID: {callback.from_user.id} - начал свой заказ')

    conn = dialog_manager.middleware_data['conn']
    await add_user(conn, user_id=callback.from_user.id)
    order_id = await get_order_id(conn, user_id=callback.from_user.id)

    await dialog_manager.start(state=OrderSG.set_location, data={'order_id': order_id})


async def start_admin_menu_dialog(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(state=AdminMenuSG.admin_menu_start)


async def get_username(event_from_user: User, **kwargs):
    return {'username': event_from_user.username if event_from_user.username is not None else event_from_user.full_name,
            'user_id': event_from_user.id}

def get_admin_id(data: dict, widget: Whenable, dialoga_manager: DialogManager):
    return data.get("user_id") in [config.bot.admin_ids]


main_menu_dialog = Dialog(
    Window(
        Format(text='Привет, <b>{username}</b>!\n'),
        Const(
            text=LEXICON_RU.get('/start')
        ),
        Button(text=Const('Сделать заказ'), id='get_order', on_click=start_order_dialog),
        Button(text=Const('Настройки'), id='admin_menu', on_click=start_admin_menu_dialog, when=get_admin_id),
        getter=get_username,
        state=StartSG.start,
    ),
)


@router.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    tz_utc9 = timezone(timedelta(hours=9))
    dt_local = message.date.astimezone(tz_utc9)

    start = time(7, 45)
    end = time(20, 00)

    is_allowed = start <= dt_local.time() <= end
    logger.info(f"Пользователь {message.from_user.username} -- {message.from_user.id} -- написал в {dt_local.time()}")

    if is_allowed:
        await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)
    else:
        await message.answer('Я принимаю заказы с 7-45 до 20-00')


@router.message()
async def delete_input_messages(message: Message, bot: Bot):
    if message.chat.type == 'private':
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    else:
        try:
            await bot.delete_message(chat_id=config.group.group_id, message_id=message.message_id)
        except Exception as e:
            logger.error(f'{message.message_id} -- {message.chat.id} -- {e}' )
