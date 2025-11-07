import logging
from typing import Any, Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

logger = logging.getLogger(__name__)


class FirstOuterMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handlers: Callable[[TelegramObject, dict[str, Any]],  Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any]) -> Any:

        logger.debug(f"Вошли в {__class__.__name__}, {event.__class__.__name__}")
        result = await handlers(event, data)
        logger.debug(f"Data: == {data}")
        logger.debug(f"Event: == {event.model_dump_json(indent=4, exclude_none=True)}")

        logger.debug(f"Вышли из {__class__.__name__}")

        return result