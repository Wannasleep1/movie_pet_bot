from aiogram import types
from aiogram.dispatcher.filters import Command

from loader import dp


@dp.message_handler(Command("start"))
async def start(message: types.Message):
    text = "Поехали!"
    await message.answer(text)


@dp.message_handler(commands=["help"])
async def _help(message: types.Message):
    text = ("Небольшой бот, который поможет Вам выбрать фильм. "
           "Используйте команды, предлагаемые ботом, " 
           "для получения ожидаемого результата.")
    await message.answer(text)
