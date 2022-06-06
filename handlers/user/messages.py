from aiogram import types
from aiogram.dispatcher.filters import CommandHelp, CommandStart, Text

from keyboards.movie_kb import initial_kb, movies_top_kb
from loader import dp


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    text = "Поехали!"
    await message.answer(text, reply_markup=initial_kb)


@dp.message_handler(CommandHelp())
async def _help(message: types.Message):
    text = ("Небольшой бот, который поможет Вам выбрать фильм. "
           "Используйте команды, предлагаемые ботом, " 
           "для получения ожидаемого результата.")
    await message.answer(text)


@dp.message_handler(Text("Вернуться в начало"))
async def go_back_to_initial(message: types.Message):
    await message.answer(text="Возвращаемся...", reply_markup=initial_kb)
