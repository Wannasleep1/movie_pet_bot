import aiohttp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from config.config import HEADERS
from config.data import MONTHS
from handlers.user.premieres import _get_premieres_params
from loader import dp
from states.states import PremieresFilterState
from utils.data_parsers import movies_data_parser
from utils.paginator.paginator import pagination_call, get_reply_markup
from utils.url_generator import get_api_url


ALL_MOVIES_PREMIERES_DATA = ""


@dp.message_handler(Text("Премьеры по фильтру"))
async def get_premieres_state_start(message: types.Message):
    await PremieresFilterState.release_year.set()
    await message.answer(text="Введите год премьеры. Чтобы отменить ввод используйте команду '/отмена'")


@dp.message_handler(lambda message: message.text.lower() not in MONTHS,
                    state=PremieresFilterState.release_month)
async def invalid_month_passed(message: types.Message):
    await message.answer("Укажите корректный месяц")


def _validate_release_year(year):
    try:
        int(year)
    except ValueError:
        return False
    else:
        return True


@dp.message_handler(state=PremieresFilterState.release_year)
async def get_premieres_state_year(message: types.Message, state: FSMContext):
    if not _validate_release_year(message.text):
        await message.answer("Введён некорректный год")
    else:
        async with state.proxy() as data:
            data['year'] = message.text
        await PremieresFilterState.next()
        await message.answer("Введите месяц премьеры")


@dp.message_handler(state=PremieresFilterState.release_month)
async def get_premieres_state_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        year = data["year"]
        month = message.text
        await state.finish()

    params = _get_premieres_params(year, MONTHS[month.lower()])
    url = get_api_url("premieres")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=HEADERS) as resp:
            loaded_data = await resp.json()

    global ALL_MOVIES_PREMIERES_DATA
    ALL_MOVIES_PREMIERES_DATA = loaded_data["items"]

    total_pages = (len(ALL_MOVIES_PREMIERES_DATA) + 9) // 10
    markup = get_reply_markup(1, total_pages, "PREMIERES_FILTERED")
    movies_1st_page = ALL_MOVIES_PREMIERES_DATA[:10]
    parsed = movies_data_parser(movies_1st_page, 1)

    await message.answer(parsed, parse_mode=types.ParseMode.HTML, reply_markup=markup)


@dp.callback_query_handler(pagination_call.filter(key="PREMIERES_FILTERED"))
async def get_premieres_state_page(callback: types.CallbackQuery, callback_data: dict):
    page = int(callback_data.get("page"))
    total_pages = int(callback_data.get("total_pages"))
    start_elem, end_elem = (page - 1) * 10 + 1, page * 10 + 1
    global ALL_MOVIES_PREMIERES_DATA
    page_data = movies_data_parser(ALL_MOVIES_PREMIERES_DATA[start_elem:end_elem], page)
    markup = get_reply_markup(page, total_pages, key=callback_data.get("key"))
    await callback.message.answer(page_data, reply_markup=markup,
                                  parse_mode=types.ParseMode.HTML)
    await callback.message.delete()
    await callback.answer()
