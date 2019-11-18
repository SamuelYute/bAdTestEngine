from modules.Server import Strategy
from modules.datastore.Indicators import SimpleMovingAverage, ExponentialMovingAverage, HullMovingAverage


class AlgorithmOne(Strategy):
    def initialize(self):
        self.instrument = 'EURUSD'
        self.start_date = '2018-01-01'
        self.end_date = '2018-12-31'
        self.time_frame = '15Min'
        self.precision = 5
        self.average_pip_spread = 0
        self.spread_range_percentage = 10

        data_series = self.store.create_market_data_series(
            self.instrument,
            self.start_date,
            self.end_date,
            self.time_frame,
            activate=True
        )

        self.store.create_indicator_data_series(data_series, 'IamFastSMA', SimpleMovingAverage(20))
        self.store.create_indicator_data_series(data_series, 'IamSloowSMA', SimpleMovingAverage(100))
        self.store.create_indicator_data_series(data_series, 'ExponentialHereEMA', ExponentialMovingAverage(20))
        self.store.create_indicator_data_series(data_series, 'HallucinationLolHMA', HullMovingAverage(100))

    def on_tick(self):
        # Manage Trades HERE if you want
        return self

    def on_bar(self):
        # You can run you entry strategy here and interact with the MARKET SERVER API
        return self

    def on_position_open(self):
        # Called when a new Position is Opened
        return self

    def on_position_close(self):
        # Called when a Position is Closed
        return self

    def on_position_update(self):
        # Called when ever a position is modified
        return self


AlgorithmOne().run()
