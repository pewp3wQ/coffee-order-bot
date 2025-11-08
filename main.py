import asyncio
import logging
import psycopg_pool

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from config.config import load_config, Config
from middleware.database import DataBaseMiddleware
from handlers import other, user, group
from menu.set_menu import set_user_menu, delete_command_in_chat, set_admin_menu
from database.connection import get_pg_pool


async def main() -> None:
    config: Config = load_config()

    storage = RedisStorage(
        redis=Redis(
            host=config.redis.host,
            port=config.redis.port,
            db=config.redis.db,
            password=config.redis.password,
            username=config.redis.username,
        )
    )

    logging.basicConfig(
        level=logging.getLevelName(level=config.log.level),
        format=config.log.format
    )

    logger = logging.getLogger(__name__)

    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=storage)

    logger.info('Get db pool')
    db_pool: psycopg_pool.AsyncConnectionPool = await get_pg_pool(
        db_name=config.db.name,
        host=config.db.host,
        port=config.db.port,
        user=config.db.user,
        password=config.db.password,
    )

    logger.info('Router including')
    dp.include_router(user.router)
    dp.include_router(group.router)
    dp.include_router(other.router)

    logger.info("Including middlewares...")
    dp.update.middleware(DataBaseMiddleware())

    # await set_user_menu(bot)
    await set_admin_menu(bot)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(
            bot,
            db_pool=db_pool
        )
    except Exception as e:
        logger.exception(e)
    finally:
        await db_pool.close()
        logger.info("Connection to Postgres closed")

if __name__ == '__main__':
    asyncio.run(main())