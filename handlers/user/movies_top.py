import aiohttp
from aiogram import types
from aiogram.dispatcher.filters import Text

from config.config import HEADERS
from keyboards.movie_kb import movies_top_kb, tops_kb
from loader import dp
from utils.url_generator import get_api_url
from utils.data_parsers import movies_top_data_parser
from utils.paginator.paginator import get_reply_markup, pagination_call


AVAILABLE_CMDS = {
    "Топ 250 лучших фильмов": "TOP_250_BEST_FILMS",
    "Топ 100 популярных фильмов": "TOP_100_POPULAR_FILMS",
    "Топ ожидаемых фильмов": "TOP_AWAIT_FILMS",
}
URL = get_api_url("movies_top")


def _get_movies_top_params(type_, page):
    return {
        "type": type_,
        "page": page,
    }


async def _get_data_for_paginating(callback_data: dict):
    page = int(callback_data.get("page"))
    param_type = callback_data.get("key")
    total_pages = int(callback_data.get("total_pages"))
    params = _get_movies_top_params(param_type, page)
    async with aiohttp.ClientSession() as session:
        async with session.get(URL, params=params, headers=HEADERS) as resp:
            data = await resp.json()
    movie_data = movies_top_data_parser(data["films"], page)
    reply_markup = get_reply_markup(page, total_pages, key=param_type)
    return movie_data, reply_markup


@dp.message_handler(Text("Вывести топ фильмов"))
async def movies_top(message: types.Message):
    await message.answer(text="Выберите один из вариантов", reply_markup=movies_top_kb)


@dp.message_handler(Text("Топы"))
async def movies_top(message: types.Message):
    await message.answer(text="Выберите один из топов", reply_markup=tops_kb)


@dp.message_handler(Text(["Топ 250 лучших фильмов",
                          "Топ 100 популярных фильмов",
                          "Топ ожидаемых фильмов",
                          ]))
async def get_movies_top(message: types.Message):
    params = _get_movies_top_params(AVAILABLE_CMDS[message.text], 1)
    async with aiohttp.ClientSession() as session:
        async with session.get(URL, params=params, headers=HEADERS) as resp:
            data_dict = await resp.json()
    total_pages = data_dict["pagesCount"]
    data = data_dict["films"]
    movie_data = movies_top_data_parser(data, 1)
    reply_markup = get_reply_markup(1, total_pages, key=AVAILABLE_CMDS[message.text])
    await message.answer(movie_data, reply_markup=reply_markup,
                         parse_mode=types.ParseMode.HTML)


@dp.callback_query_handler(pagination_call.filter(key="TOP_250_BEST_FILMS"))
async def get_movies_top_250_page(callback: types.CallbackQuery, callback_data: dict):
    movie_data, reply_markup = await _get_data_for_paginating(callback_data)
    await callback.message.answer(movie_data, reply_markup=reply_markup,
                                  parse_mode=types.ParseMode.HTML)
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(pagination_call.filter(key="TOP_100_POPULAR_FILMS"))
async def get_movies_top_100_popular_page(callback: types.CallbackQuery, callback_data: dict):
    movie_data, reply_markup = await _get_data_for_paginating(callback_data)
    await callback.message.answer(movie_data, reply_markup=reply_markup,
                                  parse_mode=types.ParseMode.HTML)
    await callback.message.delete()
    await callback.answer()


@dp.callback_query_handler(pagination_call.filter(key="TOP_AWAIT_FILMS"))
async def get_movies_top_100_popular_page(callback: types.CallbackQuery, callback_data: dict):
    movie_data, reply_markup = await _get_data_for_paginating(callback_data)
    await callback.message.answer(movie_data, reply_markup=reply_markup,
                                  parse_mode=types.ParseMode.HTML)
    await callback.message.delete()
    await callback.answer()
