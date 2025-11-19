import asyncio
import logging

from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram_dialog import setup_dialogs
from aiohttp import web
from psycopg_pool import AsyncConnectionPool

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from config.config import load_config, Config
from dialogs import main_menu, order
from middleware.db_connection import DataBaseMiddleware
from handlers import user, group
from menu.set_menu import set_user_menu, delete_command_in_chat, set_admin_menu, set_description
from database.connection import get_pg_pool

config: Config = load_config()
logger = logging.getLogger(__name__)


async def on_startup(bot: Bot) -> None:
    logger.info('Установлено меню и описание бота')
    await set_user_menu(bot)
    # await set_admin_menu(bot)
    await set_description(bot)

    logger.info('Вебхук установлен')
    await bot.set_webhook(f"{config.webhook.base_url}{config.webhook.path}", secret_token=config.webhook.secret)


def main() -> None:
    storage = RedisStorage(
        redis=Redis(
            host=config.redis.host,
            port=config.redis.port,
            db=config.redis.db,
            password=config.redis.password,
            username=config.redis.username,
        )
    )

    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    dp.startup.register(on_startup)

    logger.info('Router including')
    dp.include_router(user.router)
    dp.include_router(group.router)
    dp.include_router(main_menu.router)
    dp.include_router(order.router)
    setup_dialogs(dp)

    logger.info("Including middlewares...")
    dp.update.middleware(DataBaseMiddleware())

    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=config.webhook.secret,
    )
    webhook_requests_handler.register(app, path=config.webhook.path)

    setup_application(app, dp, bot=bot)
    web.run_app(app, host=config.webhook.server, port=config.webhook.port)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.getLevelName(level=config.log.level),
        format=config.log.format
    )
    main()