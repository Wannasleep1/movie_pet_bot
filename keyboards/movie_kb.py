from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
                          KeyboardButton, ReplyKeyboardMarkup


initial_kb = ReplyKeyboardMarkup(resize_keyboard=True)
initial_kb.add(
    KeyboardButton(text="Вывести топ фильмов"),
).add(
    KeyboardButton(text="Вывести кинопремьеры"),
).add(
    KeyboardButton(text="Найти фильм по фильтрам"),
)


movies_top_kb = ReplyKeyboardMarkup(resize_keyboard=True)
movies_top_kb.add(
    KeyboardButton(text="Топ 250 лучших фильмов"),
).add(
    KeyboardButton(text="Топ 100 популярных фильмов"),
).add(
    KeyboardButton(text="Топ ожидаемых фильмов")
).add(
    KeyboardButton(text="Вернуться в начало"),
)