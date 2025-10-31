import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config.config import load_config, Config
from handlers import other, user, group
from menu.set_menu import set_user_menu, delete_command_in_chat, set_admin_menu


async def main() -> None:
    db = {"user_template": {"page": 1,
                            'current_order': {},
                            'order_step': None
                            },
          "users": {},
          "number_order": 1,
          "history_order": {}
    }
    storage: MemoryStorage = MemoryStorage()

    config: Config = load_config()
    logging.basicConfig(
        level=logging.getLevelName(level=config.log.level),
        format=config.log.format
    )

    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=storage)
    dp.workflow_data.update(db=db)
    dp.include_router(user.router)
    dp.include_router(group.router)
    dp.include_router(other.router)

    # await set_user_menu(bot)
    await set_admin_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())