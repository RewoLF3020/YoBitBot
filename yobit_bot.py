import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from config import BOT_TOKEN, USER_ID
from main_public import get_ticker, get_depth, get_trades


bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

currency = None


@dp.message_handler(Text(equals="Выбрать валюту"))
@dp.message_handler(commands="start")
async def start(message: types.Message = 'start'):
    button_btc = types.InlineKeyboardButton('BTC', callback_data='btc')
    button_eth = types.InlineKeyboardButton('ETH', callback_data='eth')
    button_trx = types.InlineKeyboardButton('TRX', callback_data='trx')
    button_xrp = types.InlineKeyboardButton('XRP', callback_data='xrp')
    button_doge = types.InlineKeyboardButton('DOGE', callback_data='doge')
    button_usdt = types.InlineKeyboardButton('USDT', callback_data='usdt')

    keyboard_currencies = types.InlineKeyboardMarkup()
    keyboard_currencies.add(button_btc, button_eth, button_trx, button_xrp, button_doge, button_usdt)
    
    start_buttons = ['Выбрать валюту', 'dsewd', 'fefewf']
    keyboard_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_start.add(*start_buttons)
    await message.answer("Выберите валюту", reply_markup=keyboard_currencies)
    await message.answer("Вскоре будут доступны другие валюты", reply_markup=keyboard_start)
    return keyboard_currencies


""" @dp.message_handler(Text(equals="Данные по выбранной валюте"))
async def get_info(message: types.Message):
    # with open("ticker.txt") as file:
        # info_dict = json.load(file)["btc_usd"]
    
    await message.answer(get_ticker(coin1=currency))


@dp.message_handler(Text(equals="Сумма выставленных на закуп монет"))
async def get_purchase_sum(message: types.Message):
    await message.answer(f"Общая сумма выставленных на закуп монет в последних 150 ордерах:\n{get_depth(coin1=currency)}")


@dp.message_handler(Text(equals="Сумма проданных и купленных монет"))
async def get_sold_bought_data(message: types.Message):
    await message.answer(get_trades(coin1=currency)) """


@dp.callback_query_handler(lambda c: c.data in ['btc', 'eth', 'trx', 'xrp', 'doge', 'usdt'])
async def process_callback_currency(callback_query: types.CallbackQuery):
    global currency
    currency = callback_query.data
        
    # next_buttons = ["Данные по выбранной валюте", "Сумма выставленных на закуп монет", "Сумма проданных и купленных монет"]
    # keyboard_actions = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # keyboard_actions.add(*next_buttons)
    # await message.answer("Выберите действие", reply_markup=keyboard_actions)
    
    button_data = types.InlineKeyboardButton('Данные по выбранной валюте', callback_data='data')
    button_sum = types.InlineKeyboardButton('Сумма выставленных на закуп монет', callback_data='sum')
    button_stats = types.InlineKeyboardButton('Сумма проданных и купленных монет', callback_data='stats')
    keyboard_actions = types.InlineKeyboardMarkup(row_width=1)
    keyboard_actions.add(button_data, button_sum, button_stats)
    
    await bot.send_message(callback_query.from_user.id, 
                           f"Вы выбрали валюту {currency}. Что вы хотите сделать?", 
                           reply_markup=keyboard_actions)


@dp.callback_query_handler(lambda c: c.data in ['data', 'sum', 'stats'])
async def process_callback_action(callback_query: types.CallbackQuery):
    action = callback_query.data
    
    if action == 'data':
        try:
            await bot.send_message(callback_query.from_user.id, f"<b>Данные по валюте {currency}:</b>\n{get_ticker(coin1=currency)}")
        except:
            await bot.send_message(callback_query.from_user.id, "Выберите валюту", )
    elif action == 'sum':
        await bot.send_message(callback_query.from_user.id, f"Общая сумма выставленных на закуп монет в последних 150 ордерах:\n{get_depth(coin1=currency)}")
    elif action == 'stats':
        await bot.send_message(callback_query.from_user.id, f"{get_trades(coin1=currency)}")


async def info_every_time():
    while True:
        info = get_ticker(coin1=currency)
        
        # get your id @userinfobot
        await bot.send_message(USER_ID, info, disable_notification=True)
        await asyncio.sleep(3600)


if __name__ == '__main__':
    if currency:
        loop = asyncio.get_event_loop()
        loop.create_task(info_every_time())
    executor.start_polling(dp)