import json
import threading
from .Instrument import Instrument
from .DataSeries import DataSeries
from .IndicatorDataSeries import IndicatorDataSeries


class Store:
    instruments = []
    active_market_series = None
    all_indicator_data_series = []

    def __init__(self):
        self.load_instruments()

    def load_instruments(self):
        with open('Files/instruments.json') as file:
            data = json.load(file)
            for instrument_config in data:
                self.instruments.append(Instrument(instrument_config))

    def get_instrument(self, name):
        instrument = None

        for value in self.instruments:
            if name == value.name:
                instrument = value
                break

        return instrument

    def create_market_data_series(self,  instrument, start_date, end_date, time_frame, activate=True):
        instrument_obj = self.get_instrument(instrument)
        data_series = DataSeries(instrument_obj, start_date, end_date, time_frame)

        if activate:
            self.active_market_series = data_series

        return data_series

    def create_indicator_data_series(self,  market_data_series, name, indicator):
        self.all_indicator_data_series.append({
            'name': name,
            'series': IndicatorDataSeries(market_data_series, indicator)
        })

    def get_indicator(self, name):
        indicator_data_series = None
        for series in self.all_indicator_data_series:
            if series['name'] == name:
                indicator_data_series = series['series']
        return indicator_data_series

    def process_tick(self, data_series, tick, volume_count):
        data_series.process_tick(tick, volume_count)

        def update(sr):
            sr.market_data_series.process_tick(tick, volume_count)

        for series in self.all_indicator_data_series:
            update(series['series'])

    def process_bar(self, data_series):
        data_series.process_bar()

        def update(sr):
            sr.market_data_series.process_bar()
            sr.update_current_indicator_bar()

        for series in self.all_indicator_data_series:
            update(series['series'])

