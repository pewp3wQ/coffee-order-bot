import asyncio
import logging

from psycopg_pool import AsyncConnectionPool
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram_dialog import setup_dialogs, BgManagerFactory
from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from redis.asyncio import Redis

from config.config import load_config, Config
from database.connection import get_pg_pool
from dialogs import main_menu, order
from handlers import group
from log_settings import log_config
from middleware.db_connection import DataBaseMiddleware
from menu.set_menu import set_user_menu, set_description
from payments.yookassa_payment import yookassa_webhook_handler

config: Config = load_config()
logger = logging.getLogger(__name__)

async def on_startup(bot: Bot) -> None:
    logger.info('Установлено меню и описание бота')
    await set_user_menu(bot)
    await set_description(bot)

    logger.info('Вебхук установлен')
    await bot.set_webhook(url=f"{config.webhook.base_url}{config.webhook.path}",
                          secret_token=config.webhook.secret,
                          drop_pending_updates=True)


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    db_pool = dispatcher.get("db_pool")
    await db_pool.close()
    await bot.session.close()


async def main():
    # log_config.setup_logging()

    storage = RedisStorage(
        redis=Redis(
            host=config.redis.host,
            port=config.redis.port,
            db=config.redis.db,
            password=config.redis.password,
            username=config.redis.username,
        ),
        key_builder=DefaultKeyBuilder(with_destiny=True)
    )

    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=storage)

    db_pool: AsyncConnectionPool = await get_pg_pool(
        db_name=config.db.name,
        host=config.db.host,
        port=config.db.port,
        user=config.db.user,
        password=config.db.password,
    )

    dp["db_pool"] = db_pool
    # await bot.delete_webhook()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    logger.info('Router including')
    dp.include_router(main_menu.router)
    dp.include_router(main_menu.main_menu_dialog)
    dp.include_router(order.router)
    dp.include_router(order.order_dialog)
    # dp.include_router(admin_menu.router)
    # dp.include_router(admin_menu.admin_dialog)
    dp.include_router(group.router)
    bg_factory = setup_dialogs(dp)

    logger.info("Including middlewares...")
    dp.update.middleware(DataBaseMiddleware())

    # await dp.start_polling(bot)
    app = web.Application()
    app['bot'] = bot
    app['dp'] = dp
    app['db_pool'] = db_pool
    app['bg_factory'] = bg_factory
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=config.webhook.secret
    )
    webhook_requests_handler.register(app, path=config.webhook.path)
    app.router.add_post(config.payment_webhook.path, yookassa_webhook_handler)
    setup_application(app, dp, bot=bot)
    return app


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.getLevelName(level=config.log.level),
        format=config.log.format
    )
    # asyncio.run(main())
    web.run_app(main(), host=config.webhook.server, port=int(config.webhook.port))
