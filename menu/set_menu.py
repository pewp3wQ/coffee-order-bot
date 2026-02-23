import logging

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats

from lexicon.lexicon import LEXICON_RU


async def set_user_menu(bot: Bot):
    bot_command_for_user = [
        BotCommand(command='/start', description='Вызвать главное меню'),
    ]

    await bot.set_my_commands(
        commands=bot_command_for_user,
        scope=BotCommandScopeAllPrivateChats()
    )

    await bot.set_my_commands([],
        scope=BotCommandScopeAllGroupChats()
    )

    logging.info(msg='Команды доблавены')


async def delete_command_in_chat(bot: Bot):
    await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())
    logging.info(msg='Команды в чате удалены')


async def delete_command_in_group_chat(bot: Bot):
    await bot.delete_my_commands(scope=BotCommandScopeAllGroupChats())
    logging.info(msg='Команды в групповом чате удалены')


async def set_description(bot: Bot):
    await bot.set_my_description(LEXICON_RU.get('description'))