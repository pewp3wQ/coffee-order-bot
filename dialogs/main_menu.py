import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import User, CallbackQuery, Message, Chat
from aiogram_dialog import Dialog, DialogManager, StartMode, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button

from lexicon.lexicon import LEXICON_RU
from FSM.FSM import StartSG, OrderSG
from database.db import (
    add_user,
    get_order_id
)

logger = logging.Logger(__name__)
router = Router()

async def start_order_dialog(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    logger.info(f'Пользователь: {callback.from_user.username} - ID: {callback.from_user.id} - начал свой заказ')

    conn = dialog_manager.middleware_data['conn']
    await add_user(conn, user_id=callback.from_user.id)
    order_id = await get_order_id(conn, user_id=callback.from_user.id)

    await dialog_manager.start(state=OrderSG.set_location, data={'order_id': order_id})


async def get_username(event_from_user: User, **kwargs):
    return {'username': event_from_user.username if event_from_user.username is not None else event_from_user.full_name}


main_menu_dialog = Dialog(
    Window(
        Format(text='Привет, <b>{username}</b>!\n'),
        Const(
            text=LEXICON_RU.get('/start')),
        Button(text=Const('Сделать заказ'), id='get_order', on_click=start_order_dialog),
        getter=get_username,
        state=StartSG.start,
    ),
)

@router.message(CommandStart(), )
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)