from aiogram.dispatcher.filters.state import StatesGroup, State


class FilmByIDState(StatesGroup):
    movie_id = State()


class PremieresFilterState(StatesGroup):
    release_year = State()
    release_month = State()


class FilmByFilters(StatesGroup):
    countries = State()
    genres = State()
    order = State()
    type_ = State()
    ratingFrom = State()
    ratingTo = State()
    yearFrom = State()
    yearTo = State()
    keyword = State()
