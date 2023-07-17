from aiogram import executor
from dispatcher import dp
import handlers

from db import BotDB
from config import host, user, password, db_name


BotDB = BotDB(host, user, password, db_name)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    