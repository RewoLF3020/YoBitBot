import json

from aiogram import Bot, Dispatcher, executor, types
# from aiogram.utils.markdown import hbold, hunderline, hcode, hlink
from config import BOT_TOKEN
from main import get_depth, get_trades


bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


# @dp.message_handler(commands="start")
# async def start(message: types.Message):
#     await message.reply("Welcome to YoBit bot!")


@dp.message_handler(commands="chosen_pair_data")
async def get_info(message: types.Message):
    with open("ticker.txt") as file:
        info_dict = json.load(file)["btc_usd"]
    
    pair_data = f"High: {info_dict['high']} $\nLow: {info_dict['low']} $\n" \
                f"Buy: {info_dict['buy']} $\nSell: {info_dict['sell']} $\n" \

    await message.answer(pair_data)


@dp.message_handler(commands="total_summ_purchase_coins")
async def get_purchase_sum(message: types.Message):
    # with open("depth.txt") as file:
        # pass
    
    await message.answer(f"общая сумма выставленных на закуп монет в последних limit ордерах: {get_depth()}")


@dp.message_handler(commands="total_summ_sold_bought")
async def get_sold_bought_data(message: types.Message):
    await message.answer(get_trades())


if __name__ == '__main__':
    executor.start_polling(dp)