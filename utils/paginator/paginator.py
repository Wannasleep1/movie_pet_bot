from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


pagination_call = CallbackData("paginator", "key", "page")


def get_reply_markup(current_page, total_pages, key):
    markup = InlineKeyboardMarkup(row_width=5)

    first_page_text = "<< 1"
    max_page_text = f"{total_pages} >>"

    if current_page > 1:
        markup.insert(
            InlineKeyboardButton(
                text=first_page_text,
                callback_data=pagination_call.new(key=key,
                                                  page=1)
            )
        )

    previous_page = current_page - 1
    previous_page_text = f"< {current_page - 1}"
    if current_page > 2:
        markup.insert(
            InlineKeyboardButton(
                text=previous_page_text,
                callback_data=pagination_call.new(key=key,
                                                  page=previous_page)
            )
        )

    markup.insert(
        InlineKeyboardButton(
            text=f"- {current_page} -",
            callback_data=pagination_call.new(key=key,
                                              page=current_page)
        )
    )

    next_page = current_page + 1
    next_page_text = f"{current_page + 1} >"
    if total_pages > next_page > current_page:
        markup.insert(
            InlineKeyboardButton(
                text=next_page_text,
                callback_data=pagination_call.new(key=key,
                                                  page=next_page)
            )
        )

    if current_page < total_pages:
        markup.insert(
            InlineKeyboardButton(
                text=max_page_text,
                callback_data=pagination_call.new(key=key,
                                                  page=total_pages)
            )
        )

    return markup
