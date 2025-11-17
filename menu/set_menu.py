import logging

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats, \
    BotCommandScopeChatMember

from lexicon.lexicon import LEXICON_RU


async def set_user_menu(bot: Bot):
    bot_command_for_user = [
        BotCommand(command='/start', description=''),
    ]

    await bot.set_my_commands(
        commands=bot_command_for_user,
        scope=BotCommandScopeAllPrivateChats()
    )

    logging.info(msg='Команды доблавены')


async def set_admin_menu(bot: Bot):
    bot_command_for_admin = [
        BotCommand(command='/start', description='Сделать заказ'),
        BotCommand(command='/order', description='Заказы'),
        BotCommand(command='/settings', description='Узнать где мы находимся'),
        BotCommand(command='/price', description='Добавить цены')
    ]

    await bot.set_my_commands(
        commands=bot_command_for_admin,
        scope=BotCommandScopeChat(chat_id=699574032)
    )


async def delete_command_in_chat(bot: Bot):
    if await bot.delete_my_commands(
            scope=BotCommandScopeAllGroupChats()):
        logging.info(msg='Команды в чате удалены')


async def set_description(bot: Bot):
    await bot.set_my_description(LEXICON_RU.get('description'))