import requests
import datetime
import pandas as pd


def get_info():
    response = requests.get(url="https://yobit.net/api/3/info")
    
    with open("info.txt", "w") as file:
        file.write(response.text)
        
    return response.text


def get_ticker(coin1='btc', coin2='usd'):
    response = requests.get(url=f"https://yobit.net/api/3/ticker/{coin1}_{coin2}?ignore_invalid=1")
    
    # with open("ticker.txt", 'w') as file:
        # file.write(response.text)
    
    data = response.json()[f"{coin1}_usd"]
    answer_message = f"<code>{datetime.datetime.fromtimestamp(data['updated'])}</code>\n" \
                     f"Максимальная цена: {data['high']} $\nМинимальная цена: {data['low']} $\n" \
                     f"Средняя цена: {data['avg']} $\nОбъем торгов: {data['vol']} $\n" \
                     f"Объем торгов в валюте: {data['vol_cur']} $\nЦена последней сделки: {data['last']} $\n" \
                     f"Цена покупки: {data['buy']} $\nЦена продажи: {data['sell']} $\n"
    
    return answer_message


def get_depth(coin1='btc', coin2='usd', limit=150):
    response = requests.get(url=f"https://yobit.net/api/3/depth/{coin1}_{coin2}?limit={limit}&ignore_invalid=1")
    
    # with open("depth.txt", 'w') as file:
        # file.write(response.text)
    
    #общая сумма выставленных на закуп монет в последних limit ордерах
    bids = response.json()[f"{coin1}_{coin2}"]["bids"]
    
    total_bids_amount = 0
    for item in bids:
        price = item[0]
        coin_amount = item[1]
        
        total_bids_amount += price * coin_amount
    
    return f"Total bids: {total_bids_amount} $"


def get_trades(coin1='btc', coin2='usd', limit=150):
    response = requests.get(url=f"https://yobit.net/api/3/trades/{coin1}_{coin2}?limit={limit}&ignore_invalid=1")
    
    # with open("trades.txt", 'w') as file:
        # file.write(response.text)
    
    #общая сумма проданных и купленных монет
    total_trade_ask = 0
    total_trade_bid = 0
    for item in response.json()[f"{coin1}_{coin2}"]:
        if item["type"] == 'ask':
            total_trade_ask += item['price'] * item['amount']
        else:
            total_trade_bid += item['price'] * item['amount']
        
    info = f"[-] TOTAL {coin1} SELL: {round(total_trade_ask, 2)} $\n[+] TOTAL {coin1} BUY: {round(total_trade_bid, 2)} $"
    
    return info


def sygnals():
    url = 'https://yobit.net/api/3/trades/eth_btc?limit=2000'
    response = requests.get(url=url)
    trades = response.json()['eth_btc']
    
    df = pd.DataFrame(trades)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df[['price', 'amount']] = df[['price', 'amount']].apply(pd.to_numeric)
    
    # Вычисляем скользящие средние за 20 и 50 дней
    df['SMA20'] = df['price'].rolling(window=20).mean()
    df['SMA50'] = df['price'].rolling(window=50).mean()
    
    # Вычисляем RSI за 14 дней
    delta = df['price'].diff()
    gain = delta.copy()
    loss = delta.copy()
    gain[gain < 0] = 0
    loss[loss > 0] = 0
    gain = gain.rolling(window=14).mean()
    loss = -loss.rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100.0 - (100.0 / (1.0 + rs))
    
    # Вычисляем стохастический осциллятор
    window = 14
    min_value = df['price'].rolling(window=window).min()
    max_value = df['price'].rolling(window=window).max()
    df['stochastic_oscillator'] = (df['price'] - min_value) / (max_value - min_value) * 100
    
    # Создаем сигнал на покупку/продажу
    df['signal'] = ''
    df.loc[(df['SMA20'] > df['SMA50']) & (df['RSI'] < 30) & (df['stochastic_oscillator'] < 20), 'signal'] = 'buy'
    df.loc[(df['SMA20'] < df['SMA50']) & (df['RSI'] > 70) & (df['stochastic_oscillator'] > 80), 'signal'] = 'sell'
    
    return df


def main():
    # print(get_info())
    print(get_ticker())
    # print(get_ticker(coin1='eth'))
    print(get_depth())
    # print(get_depth(coin1='doge', limit=2000))
    print(get_trades())
    print(sygnals())

if __name__ == '__main__':
    main()
