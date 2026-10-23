from aiogram import Router,types
from aiogram.types import Message
from aiogram.filters import CommandStart
import aiohttp

private = Router()

API_URL = "http://127.0.0.1:8000"

@private.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Phones")
    phones = await get_data()
    for phone in phones:
        await message.answer(f"Title: {phone['title']}\nPrice: {phone['price']}\nUrl: {phone['url']}\nState: {phone['state']}\nLocation-date: {phone['location_date']}")

async def get_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/") as resp:
            data = await resp.json()

        return data["items"]
