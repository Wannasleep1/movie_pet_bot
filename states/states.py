from aiogram.dispatcher.filters.state import StatesGroup, State


class FilmByIDState(StatesGroup):
    movie_id = State()


class PremieresFilterState(StatesGroup):
    release_year = State()
    release_month = State()
