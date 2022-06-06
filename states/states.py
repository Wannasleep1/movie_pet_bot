from aiogram.dispatcher.filters.state import StatesGroup, State


class FilmByIDState(StatesGroup):
    movie_id = State()
