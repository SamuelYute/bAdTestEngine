import pandas as pd


class DataSeries:
    open_time = None
    market_data = None
    tick_interval = '15s'
    path = 'Files/Data/'
    columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']
    columns_to_float = ['open', 'high', 'low', 'close', 'volume']

    tick_series_index = None
    bars_data_frame = None

    last_bar_datetime = None
    current_bar_datetime = None

    instrument = None
    start_date = None
    end_date = None
    time_frame = None

    volume_count = 0

    def __init__(self, instrument, start_date, end_date, time_frame):
        self.instrument = instrument
        self.start_date = start_date
        self.end_date = end_date
        self.time_frame = time_frame

        self.load_data()
        self.tick_series_index = pd.bdate_range(self.start_date, self.end_date, freq=self.tick_interval)
        self.initialize_bars()

        self.current_bar_datetime = self.last_bar_datetime = self.tick_series_index[0]

    def load_data(self):
        instrument_path = self.path+str(self.instrument.name+'.csv')
        data = pd.read_csv(instrument_path, usecols=self.columns, parse_dates=True)
        self.market_data = self.clean_data(data)

    def clean_data(self, data):
        for column in self.columns_to_float:
            data[column] = pd.to_numeric(data[column], errors='coerce')

        data['datetime'] = pd.to_datetime(data['datetime'])
        data = data.set_index('datetime')

        return data.dropna()

    def initialize_bars(self):
        all_columns = self.create_bar_columns()

        bar_series_index = pd.bdate_range(self.start_date, self.end_date, freq=self.time_frame)
        self.bars_data_frame = pd.DataFrame(index=bar_series_index, columns=all_columns)

        for column in all_columns:
            self.bars_data_frame[column] = pd.to_numeric(self.bars_data_frame[column], errors='coerce')

    def create_bar_columns(self):
        all_columns = []
        copy_columns = self.columns_to_float
        volume = copy_columns.pop()
        fields = ['bid', 'ask']

        for column in copy_columns:
            for field in fields:
                all_columns.append(field + '_' + column)

        all_columns.append(volume)

        return all_columns

    def get_bar(self, opening_time):
        # Check Logic Here
        return

    def get_current_bar(self):
        # Check Logic Here
        return self.bars_data_frame.loc[self.current_bar_datetime]

    def get_last_bar(self):
        # Check Logic Here
        return self.bars_data_frame.loc[self.last_bar_datetime]

    def get_previous_bars(self, bar_open_time, number = 10):
        # Check Logic Here
        return

    def process_tick(self, tick, count):
        if tick.timestamp not in self.tick_series_index:
            return

        opening_bar = False
        if tick.timestamp in self.bars_data_frame.index:
            opening_bar = True

        self.update_current_bar(tick, count, opening_bar)

        return opening_bar

    def process_bar(self):
        return self

    def update_current_bar(self, tick, count, is_open=False):
        if is_open:
            self.bars_data_frame.at[tick.timestamp, 'bid_open'] = \
                self.bars_data_frame.at[tick.timestamp, 'bid_high'] = \
                self.bars_data_frame.at[tick.timestamp, 'bid_low'] = \
                self.bars_data_frame.at[tick.timestamp, 'bid_close'] = tick.bid

            self.bars_data_frame.at[tick.timestamp, 'ask_open'] = \
                self.bars_data_frame.at[tick.timestamp, 'ask_high'] = \
                self.bars_data_frame.at[tick.timestamp, 'ask_low'] = \
                self.bars_data_frame.at[tick.timestamp, 'ask_close'] = tick.ask

            self.last_bar_datetime = self.current_bar_datetime
            self.current_bar_datetime = tick.timestamp
            self.bars_data_frame.at[tick.timestamp, 'volume'] = tick.volume
            self.volume_count = count
        else:
            if tick.bid > self.bars_data_frame.at[self.current_bar_datetime, 'bid_high']:
                self.bars_data_frame.at[self.current_bar_datetime, 'bid_high'] = tick.bid

            if tick.bid < self.bars_data_frame.at[self.current_bar_datetime, 'bid_low']:
                self.bars_data_frame.at[self.current_bar_datetime, 'bid_low'] = tick.bid

            if tick.ask > self.bars_data_frame.at[self.current_bar_datetime, 'ask_high']:
                self.bars_data_frame.at[self.current_bar_datetime, 'ask_high'] = tick.ask

            if tick.ask < self.bars_data_frame.at[self.current_bar_datetime, 'ask_low']:
                self.bars_data_frame.at[self.current_bar_datetime, 'ask_low'] = tick.ask

            self.bars_data_frame.at[self.current_bar_datetime, 'bid_close'] = tick.bid
            self.bars_data_frame.at[self.current_bar_datetime, 'ask_close'] = tick.ask

            if self.volume_count != count:
                self.bars_data_frame.at[self.current_bar_datetime, 'volume'] += tick.volume
                self.volume_count = count
