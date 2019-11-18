import time
import datetime
from modules.datastore.Store import Store
from modules.datastore.Tick import Tick
from modules.datastore.Indicators import SimpleMovingAverage, ExponentialMovingAverage, HullMovingAverage

instrument = 'EURUSD'
start_date = '2018-01-01'
end_date = '2018-12-31'
time_frame = '15Min'
columns = ['open', 'high', 'low', 'close']
precision = 5
average_pip_spread = 0
spread_range_percentage = 10

store = Store()
data_series = store.create_market_data_series(instrument, start_date, end_date, time_frame)
store.create_indicator_data_series(data_series, 'SMA', SimpleMovingAverage(20))
store.create_indicator_data_series(data_series, 'EMA', ExponentialMovingAverage(20))
store.create_indicator_data_series(data_series, 'HMA', HullMovingAverage(100))

volume_change_count = 0
for index_i in data_series.tick_series_index:

    if index_i in data_series.market_data.index:
        now = index_i
        volume = data_series.market_data.at[index_i, 'volume']

        for index_j in columns:
            price = data_series.market_data.at[index_i, index_j]
            volume = data_series.market_data.at[index_i, 'volume']

            tick = Tick(now, price, volume, precision, average_pip_spread, spread_range_percentage)
            store.process_tick(data_series, tick, volume_change_count)

            now += datetime.timedelta(seconds=15)

        if index_i in data_series.bars_data_frame.index:
            store.process_bar(data_series)

            simple_moving_average = store.get_indicator('SMA')

            last_bar = data_series.get_last_bar()
            last_indicator_bar = simple_moving_average.get_last_indicator_bar()

            print(index_i, last_bar.name, last_bar.bid_close, last_indicator_bar.name, last_indicator_bar.value)

        volume_change_count += 1


rounded_dt = data_series.bars_data_frame.round({"volume":2})
rounded_dt.dropna().to_csv(instrument+time_frame+'.csv')
