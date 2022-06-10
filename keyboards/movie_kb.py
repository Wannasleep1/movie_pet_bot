from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


initial_kb = ReplyKeyboardMarkup(resize_keyboard=True)
initial_kb.add(
    KeyboardButton(text="Вывести топ фильмов"),
).add(
    KeyboardButton(text="Вывести кинопремьеры"),
).add(
    KeyboardButton(text="Найти фильм по фильтрам"),
).add(
    KeyboardButton(text="Выбрать фильм по ID"),
)


movies_top_kb = ReplyKeyboardMarkup(resize_keyboard=True)
movies_top_kb.add(
    KeyboardButton(text="Топы")
).add(
    KeyboardButton(text="Выбрать фильм по ID"),
).add(
    KeyboardButton(text="Вернуться в начало"),
)


tops_kb = ReplyKeyboardMarkup(resize_keyboard=True)
tops_kb.add(
    KeyboardButton(text="Топ 250 лучших фильмов"),
).add(
    KeyboardButton(text="Топ популярных фильмов"),
).add(
    KeyboardButton(text="Топ ожидаемых фильмов"),
).add(
    KeyboardButton(text="Вернуться в начало"),
)


premieres_kb = ReplyKeyboardMarkup(resize_keyboard=True)
premieres_kb.add(
    KeyboardButton(text="Премьеры в этом месяце"),
).add(
    KeyboardButton(text="Премьеры по фильтру"),
).add(
    KeyboardButton(text="Выбрать фильм по ID"),
).add(
    KeyboardButton(text="Вернуться в начало"),
)
