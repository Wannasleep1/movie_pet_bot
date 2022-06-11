from aiogram.utils.executor import start_polling

from loader import dp
import middlewares, handlers
from utils.notify_admins import notify_admins
from utils.set_default_commands import set_default_commands


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await notify_admins(dispatcher)


if __name__ == '__main__':
    start_polling(dp, skip_updates=True, on_startup=on_startup)
