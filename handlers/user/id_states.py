from typing import Optional

import aiohttp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from config.config import HEADERS
from loader import dp
from states.states import FilmByIDState
from utils.url_generator import get_api_url


@dp.message_handler(Text("Выбрать фильм по ID"))
async def get_movie_by_id_state_start(message: types.Message):
    await FilmByIDState.movie_id.set()
    await message.answer(text="Введите ID фильма. Чтобы отменить ввод используйте команду '/отмена'")


@dp.message_handler(state='*', commands=['отмена'])
async def cancel_state(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Ввод ID отменён')


async def _get_movie_by_id(id_):
    url = get_api_url("base")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params={"id": id_}, headers=HEADERS) as resp:
            return resp


async def validate_id(id_):
    try:
        int(id_)
    except TypeError:
        pass
    else:
        resp = await _get_movie_by_id(id_)
        if resp.status == 404:
            return -1
        else:
            data = await resp.json()
            return data


@dp.message_handler(state=FilmByIDState.movie_id)
async def get_movie_by_id(message: types.Message, state: FSMContext):
    async with state.proxy():
        id_ = message.text
    result = await validate_id(id_)
    if result == -1:
        text = "Введён несуществующий или некорректный ID"
    else:
        text = result
    await message.answer(text)


