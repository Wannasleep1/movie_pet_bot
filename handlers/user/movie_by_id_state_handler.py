import aiohttp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from config.config import HEADERS
from keyboards.movie_series_inline_kb import movie_inline_kb, series_inline_kb
from loader import dp
from states.states import FilmByIDState
from utils.data_parsers import parse_single_movie
from utils.url_generator import get_api_url


@dp.message_handler(Text("Выбрать фильм по ID"))
async def get_movie_by_id_state_start(message: types.Message):
    await FilmByIDState.movie_id.set()
    await message.answer(text="Введите ID фильма. Чтобы отменить ввод используйте команду '/отмена'")


@dp.message_handler(state='*', commands=['отмена'])
async def cancel_state(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Ввод отменён')


async def _get_movie_by_id(id_):
    url = get_api_url("base") + id_
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as resp:
            if resp.status == 200:
                return await resp.json()


async def validate_id(id_):
    data = await _get_movie_by_id(id_)
    if not data:
        return -1
    else:
        result = data
        return result


@dp.message_handler(state=FilmByIDState.movie_id)
async def get_movie_by_id(message: types.Message, state: FSMContext):
    async with state.proxy():
        id_ = message.text
    result = await validate_id(id_)
    if result == -1:
        msg = "Введён несуществующий или некорректный ID"
        await message.answer(msg)
    else:
        await state.finish()
        if result["type"] == "TV_SERIES":
            markup = series_inline_kb
        else:
            markup = movie_inline_kb
        photo = result["posterUrl"]
        caption = parse_single_movie(result)
        await dp.bot.send_photo(message.chat.id, photo, caption=caption,
                                parse_mode=types.ParseMode.HTML)
