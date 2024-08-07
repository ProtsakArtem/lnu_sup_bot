import asyncio
import logging
from aiogram.types import BotCommand


import betterlogging as bl
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from tgbot.config import load_config
from tgbot.handlers import routers_list
from tgbot.middlewares.config import ConfigMiddleware

from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder

from tgbot.services.db import create_tables, set_text_variables, all_text
from tgbot.handlers.user import user_router


class UserKeyBuilder(DefaultKeyBuilder):
    def build(self, key, *parts) -> str:
        return ":".join(map(str, (key, *parts)))

def setup_logging():
    """
    Set up logging configuration for the application.

    This method initializes the logging configuration for the application.
    It sets the log level to INFO and configures a basic colorized log for
    output. The log format includes the filename, line number, log level,
    timestamp, logger name, and log message.

    Returns:
        None

    Example usage:
        setup_logging()
    """
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")


async def main():
    setup_logging()
    create_tables()
    set_text_variables()
    print(all_text)

    config = load_config(".env")

    bot = Bot(token=config.tg_bot.token)
    key_builder = UserKeyBuilder()
    storage = RedisStorage.from_url("redis://localhost:6379/0", key_builder=key_builder)
    dp = Dispatcher(storage=storage)

    dp.include_router(user_router)

    dp.message.outer_middleware(ConfigMiddleware(config))
    dp.callback_query.outer_middleware(ConfigMiddleware(config))

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот був вимкнений!")
