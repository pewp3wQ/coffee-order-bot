import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Update
from psycopg_pool import AsyncConnectionPool
from config.config import load_config
from database.connection import get_pg_pool

logger = logging.getLogger(__name__)
config = load_config()


class DataBaseMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: dict[str, Any],
    ) -> Any:
        logger.info('Get db pool')
        db_pool: AsyncConnectionPool = data.get("db_pool")

        if db_pool is None:
            logger.error("Database pool is not provided in middleware data.")
            raise RuntimeError("Missing db_pool in middleware context.")

        async with db_pool.connection() as connection:
            try:
                async with connection.transaction():
                    data["conn"] = connection
                    result = await handler(event, data)

                    logger.info('Внутри connection мидлвари database')
                    logger.info(f'{result}')

            except Exception as e:
                logger.exception("Transaction rolled back due to error: %s", e)
                raise

        logger.info(f'Прошел мидлварь по database {db_pool}')
        # Здесь может быть какой-то код, который выполнится в случае успешного завершения транзакции

        return result