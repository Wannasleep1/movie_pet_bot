from datetime import datetime

import aiohttp
from aiogram import types
from aiogram.dispatcher.filters import Text

from config.config import HEADERS
from keyboards.movie_kb import premieres_kb
from loader import dp
from utils.data_parsers import movies_data_parser
from utils.paginator.paginator import pagination_call, get_reply_markup
from utils.url_generator import get_api_url


ALL_MOVIES_DATA = ""


def _get_premieres_params(year, month):
    return {
        "year": year,
        "month": month,
    }


@dp.message_handler(Text("Вывести кинопремьеры"))
async def get_premieres(message: types.Message):
    await message.answer("Выберите один из варинтов", reply_markup=premieres_kb)


@dp.message_handler(Text("Премьеры в этом месяце"))
async def get_curr_premieres(message: types.Message):
    curr_time = datetime.now()
    curr_month = curr_time.strftime('%B')
    curr_year = str(curr_time.year)
    url = get_api_url("premieres")
    params = _get_premieres_params(curr_year, curr_month)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=HEADERS) as resp:
            data = await resp.json()
            global ALL_MOVIES_DATA
            ALL_MOVIES_DATA = data["items"]
            movies_1st_page = ALL_MOVIES_DATA[:10]
            parsed = movies_data_parser(movies_1st_page, 1)
            total_pages = (len(ALL_MOVIES_DATA) + 9) // 10
    markup = get_reply_markup(1, total_pages, "PREMIERES")
    await message.answer(parsed, parse_mode=types.ParseMode.HTML, reply_markup=markup)


@dp.callback_query_handler(pagination_call.filter(key="PREMIERES"))
async def get_movies_top_100_popular_page(callback: types.CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    total_pages = int(callback_data.get("total_pages"))
    start_elem, end_elem = (page - 1) * 10 + 1, page * 10 + 1
    global ALL_MOVIES_DATA
    page_data = movies_data_parser(ALL_MOVIES_DATA[start_elem:end_elem], page)
    markup = get_reply_markup(page, total_pages, key=callback_data.get("key"))
    await callback.message.answer(page_data, reply_markup=markup,
                                  parse_mode=types.ParseMode.HTML)
    await callback.message.delete()
    await callback.answer()
