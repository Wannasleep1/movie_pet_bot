from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


movie_inline_kb = InlineKeyboardMarkup(row_width=2)
movie_inline_kb.insert(
    InlineKeyboardButton("Прокат")
).insert(
    InlineKeyboardButton("Сборы")
).insert(
    InlineKeyboardButton("Факты")
).insert(
    InlineKeyboardButton("Изображения")
).insert(
    InlineKeyboardButton("Обзоры")
).insert(
    InlineKeyboardButton("Награды")
)


series_inline_kb = InlineKeyboardMarkup(row_width=2)
series_inline_kb.insert(
    InlineKeyboardButton("Сезоны")
).insert(
    InlineKeyboardButton("Факты")
).insert(
    InlineKeyboardButton("Изображения")
).insert(
    InlineKeyboardButton("Обзоры")
).insert(
    InlineKeyboardButton("Награды")
)
