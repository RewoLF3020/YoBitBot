import binance
import pandas as pd
import numpy as np

client = binance.Client()

klines = client.get_historical_klines("BTCUSDT", binance.KLINE_INTERVAL_1DAY, "30 days ago")

df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])

df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Преобразуем столбцы в числовой формат
df[['open', 'high', 'low', 'close', 'volume', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume']] = df[['open', 'high', 'low', 'close', 'volume', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume']].apply(pd.to_numeric)

# Вычисляем скользящие средние за 20 и 50 дней
df['SMA20'] = df['close'].rolling(window=20).mean()
df['SMA50'] = df['close'].rolling(window=50).mean()

# Вычисляем RSI за 14 дней
delta = df['close'].diff()
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
min_value = df['low'].rolling(window=window).min()
max_value = df['high'].rolling(window=window).max()
df['stochastic_oscillator'] = (df['close'] - min_value) / (max_value - min_value) * 100

# Создаем сигнал на покупку/продажу
df['signal'] = np.where((df['SMA20'] > df['SMA50']) & (df['RSI'] < 30) & (df['stochastic_oscillator'] < 20), 'buy', np.where((df['SMA20'] < df['SMA50']) & (df['RSI'] > 70) & (df['stochastic_oscillator'] > 80), 'sell', ''))
