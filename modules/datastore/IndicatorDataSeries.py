import pandas as pd


class IndicatorDataSeries:
    market_data_series = None
    indicator = None

    indicator_bars_data_frame = None
    current_indicator_bar_data_datetime = None

    volume_count = 0

    def __init__(self, market_data_series, indicator):
        self.market_data_series = market_data_series
        self.indicator = indicator

        self.initialize_indicator_bars()

    def initialize_indicator_bars(self):
        market_bar_series_index = self.market_data_series.bars_data_frame.index
        self.indicator_bars_data_frame = pd.DataFrame(index=market_bar_series_index, columns=self.indicator.fields)

    def get_current_indicator_bar(self):
        # Check Logic Here
        return self.indicator_bars_data_frame.loc[self.market_data_series.current_bar_datetime]

    def get_last_indicator_bar(self):
        # Check Logic Here
        return self.indicator_bars_data_frame.loc[self.market_data_series.last_bar_datetime]

    def get_previous_indicator_bars(self, bar_open_time, number=10):
        # Check Logic Here
        return

    def update_current_indicator_bar(self):
        relevant_bars = self.market_data_series.bars_data_frame.loc[:self.market_data_series.last_bar_datetime, :].dropna().tail(self.indicator.period+5)

        if len(relevant_bars) < self.indicator.period:
            return

        new_indicator_bar = self.indicator.on_bar(relevant_bars)

        if self.market_data_series.last_bar_datetime not in new_indicator_bar.index:
            return

        for column in self.indicator.fields:
            self.indicator_bars_data_frame.at[self.market_data_series.last_bar_datetime, column] = new_indicator_bar.at[self.market_data_series.last_bar_datetime, column]
