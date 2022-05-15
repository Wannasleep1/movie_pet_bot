import logging

from aiogram import Dispatcher

from config.config import ADMINS


async def notify_admins(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Бот запущен!")
        except Exception as err:
            logging.exception(err)
