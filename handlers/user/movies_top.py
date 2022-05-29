import requests
from aiogram import types
from aiogram.dispatcher.filters import Text

from config.config import HEADERS
from loader import dp
from utils.get_api_url import get_api_url
from utils.movie_data_parser import movie_data_parser
from utils.paginator.paginator import get_reply_markup, pagination_call


AVAILABLE_CMDS = {
    "Топ 250 лучших фильмов": "TOP_250_BEST_FILMS",
    "Топ 100 популярных фильмов": "TOP_100_POPULAR_FILMS",
    "Топ ожидаемых фильмов": "TOP_AWAIT_FILMS",
}
URL = get_api_url("movies_top")
TOTAL_PAGES = 0


@dp.message_handler(Text(["Топ 250 лучших фильмов",
                          "Топ 100 популярных фильмов",
                          "Топ ожидаемых фильмов",
                          ]))
async def get_movies_top(message: types.Message):
    params = {
        "type": AVAILABLE_CMDS[message.text],
        "page": 1,
    }

    data_dict = requests.get(URL, params=params, headers=HEADERS).json()
    global TOTAL_PAGES
    TOTAL_PAGES = data_dict["pagesCount"]

    data = data_dict["films"]
    movie_data = movie_data_parser(data, 1)
    reply_markup = get_reply_markup(1, TOTAL_PAGES, key=AVAILABLE_CMDS[message.text])
    await message.answer(movie_data, reply_markup=reply_markup)


@dp.callback_query_handler(pagination_call.filter(key="TOP_250_BEST_FILMS"))
async def get_movies_top_250_page(callback: types.CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    params = {
        "type": "TOP_250_BEST_FILMS",
        "page": page,
    }
    data = requests.get(URL, params=params, headers=HEADERS).json()["films"]
    movie_data = movie_data_parser(data, page)
    reply_markup = get_reply_markup(page, TOTAL_PAGES, key="TOP_250_BEST_FILMS")
    await callback.message.delete()
    await callback.message.answer(movie_data, reply_markup=reply_markup)
    await callback.answer()
