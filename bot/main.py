import asyncio
from aiogram import Bot, Dispatcher

from private_router import private

bot = Bot(token="")

dp = Dispatcher()

dp.include_router(private)

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
