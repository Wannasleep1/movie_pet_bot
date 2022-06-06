from datetime import datetime

import aiohttp
from aiogram import types
from aiogram.dispatcher.filters import Text

from config.config import HEADERS
from keyboards.movie_kb import premieres_kb
from loader import dp
from utils.movie_data_parser import movie_data_parser
from utils.url_generator import get_api_url


@dp.message_handler(Text("Вывести кинопремьеры"))
async def get_premieres(message: types.Message):
    await message.answer("Выберите один из варинтов", reply_markup=premieres_kb)


@dp.message_handler(Text("Премьеры в этом месяце"))
async def get_curr_premieres(message: types.Message):
    curr_time = datetime.now()
    curr_month = curr_time.strftime('%B')
    curr_year = str(curr_time.year)
    url = get_api_url("premieres")
    params = {
        "year": curr_year,
        "month": curr_month,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=HEADERS) as resp:
            data = await resp.json()
            movies = movie_data_parser(data["items"], 1)
    await message.answer(movies)
