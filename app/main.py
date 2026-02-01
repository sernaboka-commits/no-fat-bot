import asyncio
import uvicorn

from aiogram import Bot, Dispatcher
from app.config import BOT_TOKEN
from app.handlers.common import router as common_router
from app.web import app as web_app

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(common_router)


async def start_bot():
    await dp.start_polling(bot)


async def start_web():
    config = uvicorn.Config(
        web_app,
        host="0.0.0.0",
        port=8080,
        log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    await asyncio.gather(
        start_bot(),
        start_web()
    )


if __name__ == "__main__":
    asyncio.run(main())
