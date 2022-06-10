import aiohttp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from config.config import HEADERS
from config.data import ORDER, TYPES
from loader import dp
from states.states import FilmByFilters
from utils.data_parsers import movies_data_parser
from utils.paginator.paginator import get_reply_markup, pagination_call
from utils.url_generator import get_api_url


COUNTRIES = []
GENRES = []
USERS_PARAMS = {}


async def _upload_additional_data():
    global COUNTRIES, GENRES
    url = get_api_url("countries_genres")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as resp:
            data = await resp.json()
    COUNTRIES = data["countries"]
    GENRES = data["genres"]


def _validate_country(text):
    country = [el["id"] for el in COUNTRIES if text.lower().strip() == el["country"].lower()]
    return country[0] if country else None


def _validate_genre(text):
    genre = [el["id"] for el in GENRES if text.lower().strip() == el["genre"].lower()]
    return genre[0] if genre else None


def _validate_order(text):
    is_possible_order_param = ORDER.get(text.lower().strip(), None)
    return True if is_possible_order_param else False


def _validate_type(text):
    is_possible_type_param = TYPES.get(text.lower().strip(), None)
    return True if is_possible_type_param else False


def _validate_rating_from(text):
    try:
        rating = int(text)
    except ValueError:
        return False

    is_valid = 0 <= rating <= 10
    return True if is_valid else False


def _validate_rating_to(text, rating_from):
    try:
        rating = int(text)
    except ValueError:
        return False

    is_valid = (0 <= rating <= 10 and rating >= int(rating_from))
    return True if is_valid else False


def _validate_year_from(text):
    try:
        year = int(text)
    except ValueError:
        return False

    is_valid = 1000 <= year <= 3000
    return True if is_valid else False


def _validate_year_to(text, year_from):
    try:
        year = int(text)
    except ValueError:
        return False

    is_valid = (1000 <= year <= 3000 and year >= int(year_from))
    return True if is_valid else False


@dp.message_handler(Text("Найти фильм по фильтрам"))
async def get_film_by_filters(message: types.Message):
    if not COUNTRIES and not GENRES:
        await _upload_additional_data()
    await FilmByFilters.countries.set()
    await message.answer(text=("Введите название страны. Чтобы отменить ввод используйте "
                               "команду '/отмена'"))


@dp.message_handler(state=FilmByFilters.countries)
async def get_film_countries(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        country = _validate_country(message.text)
        if country:
            data["countries"] = [country]
            gs = [el["genre"] for el in GENRES]
            await FilmByFilters.next()
            await message.answer(text=f"Введите название жанра ({', '.join(gs)})")
        else:
            await message.answer("Введено несуществующее значение страны")


@dp.message_handler(state=FilmByFilters.genres)
async def get_film_genres(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        genre = _validate_genre(message.text)
        if genre:
            data["genres"] = [genre]
            await FilmByFilters.next()
            await message.answer(text="Введите один параметр порядка сортировки результата: "
                                      "по рейтингу, по количеству голосов, по году")
        else:
            await message.answer("Введено неккоректное значение жанра")


@dp.message_handler(state=FilmByFilters.order)
async def get_film_order(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        is_valid = _validate_order(message.text)
        if is_valid:
            data["order"] = ORDER[message.text]
            await FilmByFilters.next()
            await message.answer(text="Введите один параметр типа результата: "
                                      "фильм, сериал, шоу")
        else:
            await message.answer("Введено некорректное значение параметра сортировки результата")


@dp.message_handler(state=FilmByFilters.type_)
async def get_film_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        is_valid = _validate_type(message.text)
        if is_valid:
            data["type"] = TYPES[message.text]
            await FilmByFilters.next()
            await message.answer(text="Введите минимальный рейтинг (от 0 до 10)")
        else:
            await message.answer("Введено некорректное значение параметра сортировки результата")


@dp.message_handler(state=FilmByFilters.ratingFrom)
async def get_film_rating_from(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        is_valid = _validate_rating_from(message.text)
        if is_valid:
            data["ratingFrom"] = message.text
            await FilmByFilters.next()
            await message.answer(text="Введите максимальный рейтинг (от 0 до 10, но меньше "
                                      "минимального рейтинга)")
        else:
            await message.answer("Введен некорректный рейтинг")


@dp.message_handler(state=FilmByFilters.ratingTo)
async def get_film_rating_to(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        is_valid = _validate_rating_to(message.text, data["ratingFrom"])
        if is_valid:
            data["ratingTo"] = message.text
            await FilmByFilters.next()
            await message.answer(text="Введите начальное значение года выхода фильма")
        else:
            await message.answer("Введен некорректный рейтинг")


@dp.message_handler(state=FilmByFilters.yearFrom)
async def get_film_year_from(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        is_valid = _validate_year_from(message.text)
        if is_valid:
            data["yearFrom"] = message.text
            await FilmByFilters.next()
            await message.answer(text="Введите конечное значение года выхода фильма")
        else:
            await message.answer("Введен некорректный год")


@dp.message_handler(state=FilmByFilters.yearTo)
async def get_film_year_to(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        is_valid = _validate_year_to(message.text, data["yearFrom"])
        if is_valid:
            data["yearTo"] = message.text
            await FilmByFilters.next()
            await message.answer(text="Введите ключевое слово, которое содержится "
                                      "в названии фильма.")
        else:
            await message.answer("Введен некорректный год")


@dp.message_handler(state=FilmByFilters.keyword)
async def get_film_keyword(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        is_valid = len(message.text.split()) == 1

        if is_valid:
            data["keyword"] = message.text
            url = get_api_url("base")
            params = {**data, "page": "1"}
            USERS_PARAMS[message.from_user.id] = params
            kok = USERS_PARAMS
            await state.finish()

            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers=HEADERS) as resp:
                    data_dict = await resp.json()

            total_pages = data_dict["totalPages"]
            markup = get_reply_markup(1, total_pages, "FILM_BY_FILTERS")
            parsed = movies_data_parser(data_dict["items"], 1)
            await message.answer(parsed, reply_markup=markup, parse_mode=types.ParseMode.HTML)
        else:
            await message.answer("Введено некорректное ключевое слово")


@dp.callback_query_handler(pagination_call.filter(key="FILM_BY_FILTERS"))
async def get_filtered_films_page(callback: types.CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    total_pages = int(callback_data.get("total_pages"))
    markup = get_reply_markup(page, total_pages, key=callback_data.get("key"))

    url = get_api_url("base")
    params = USERS_PARAMS[callback.from_user.id]
    params["page"] = page
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=HEADERS) as resp:
            data_dict = await resp.json()

    parsed = movies_data_parser(data_dict["items"], page, 20)
    await callback.message.answer(parsed, reply_markup=markup,
                                  parse_mode=types.ParseMode.HTML)
    await callback.message.delete()
    await callback.answer()
