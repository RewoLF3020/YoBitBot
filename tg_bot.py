# import json
import asyncio

from aiogram import Bot, Dispatcher, executor, types
# from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from aiogram.dispatcher.filters import Text
from config import BOT_TOKEN, USER_ID
from main_public import get_ticker, get_depth, get_trades


bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Данные по выбранной валюте", "Сумма выставленных на закуп монет", "Сумма проданных и купленных монет"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("данные по крипте", reply_markup=keyboard)


@dp.message_handler(Text(equals="Данные по выбранной валюте"))
async def get_info(message: types.Message):
    # with open("ticker.txt") as file:
        # info_dict = json.load(file)["btc_usd"]
    
    await message.answer(get_ticker())


@dp.message_handler(Text(equals="Сумма выставленных на закуп монет"))
async def get_purchase_sum(message: types.Message):    
    await message.answer(f"Общая сумма выставленных на закуп монет в последних 150 ордерах:\n{get_depth()}")


@dp.message_handler(Text(equals="Сумма проданных и купленных монет"))
async def get_sold_bought_data(message: types.Message):
    await message.answer(get_trades())


async def info_every_minute():
    while True:
        info = get_ticker()
        
        # get your id @userinfobot
        await bot.send_message(USER_ID, info, disable_notification=True)
        await asyncio.sleep(3600)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(info_every_minute())
    executor.start_polling(dp)