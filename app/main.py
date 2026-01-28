import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.config import load_settings, summarize_optional_env
from app.handlers.common import router as common_router

async def main() -> None:
    settings = load_settings()
    optional_env = summarize_optional_env()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if not all(optional_env.values()):
        missing = [name for name, present in optional_env.items() if not present]
        logging.getLogger(__name__).warning(
            "Optional environment variables not set yet: %s",
            ", ".join(missing),
        )

    bot = Bot(token=settings.telegram_bot_token)
    dispatcher = Dispatcher()
    dispatcher.include_router(common_router)

    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
