import talib
import math
from ta.volume import chaikin_money_flow
from ta.volatility import keltner_channel_central, keltner_channel_hband, keltner_channel_lband


class Indicator:
    period = 1
    params = []

    def __init__(self, period, params=None):
        self.period = period
        self.params = params


class SimpleMovingAverage(Indicator):
    period = 20
    fields = ['value']
    source_preference = 'bid'

    def __init__(self, period):
        self.period = period

        super().__init__(self.period)

    def on_bar(self, bars):
        close = self.source_preference + '_close'

        bars['value'] = talib.SMA(bars[close].values, self.period)
        return bars


class ExponentialMovingAverage(Indicator):
    period = 20
    fields = ['value']
    source_preference = 'bid'

    def __init__(self, period):
        self.period = period

        super().__init__(self.period)

    def on_bar(self, bars):
        close = self.source_preference + '_close'

        bars['value'] = talib.EMA(bars[close].values, self.period)
        return bars


class HullMovingAverage(Indicator):
    period = 20
    fields = ['value']
    source_preference = 'bid'

    def __init__(self, period):
        self.period = period
        super().__init__(self.period)

    def on_bar(self, bars):
        close = self.source_preference + '_close'

        wma_1 = talib.WMA(bars[close].values, self.period / 2)
        wma_2 = talib.WMA(bars[close].values, self.period)

        bars['value'] = talib.WMA((2 * wma_1) - wma_2, math.sqrt(self.period))
        return bars


class VolumeWeightedMovingAverage(Indicator):
    period = 20
    fields = ['value']
    source_preference = 'bid'

    def __init__(self, period):
        self.period = period

        super().__init__(self.period)

    def on_bar(self, bars):
        close = self.source_preference + '_close'

        def calculate(df):
            volume_price = df.eval(close + ' * volume').values
            volume_sum = df["volume"].rolling(window=self.period).mean()
            volume_ratio = volume_price / volume_sum
            cumulative_sum = (volume_ratio * df[close]).rolling(window=self.period).sum()
            cumulative_div = volume_ratio.rolling(window=self.period).sum()
            return df.assign(value=cumulative_sum / cumulative_div)

        bars['value'] = calculate(bars)['value']
        return bars


class VolumeWeightedAveragePrice(Indicator):
    period = 20
    fields = ['value']
    source_preference = 'bid'

    def __init__(self, period):
        self.period = period

        super().__init__(self.period)

    def on_bar(self, bars):
        high = self.source_preference+'_high'
        low = self.source_preference+'_low'
        close = self.source_preference+'_close'

        def calculate(df):
            volume = df['volume'].values
            typical_price = df.eval('('+high+' + '+low+' + '+close+')/3').values
            return df.assign(value=(typical_price * volume).cumsum() / volume.cumsum())

        bars['value'] = bars.groupby(bars.index.date, group_keys=False).apply(calculate)['value']
        return bars


class AroonUpDown(Indicator):
    period = 14
    fields = ['up', 'down']
    source_preference = 'bid'

    def __init__(self, period):
        self.period = period

        super().__init__(self.period)

    def on_bar(self, bars):
        high = self.source_preference + '_high'
        low = self.source_preference + '_low'

        bars['up'], bars['down'] = talib.AROON(bars[high].values, bars[low].values, self.period)
        return bars


class AverageTrueRange(Indicator):
    period = 14
    fields = ['value']
    source_preference = 'bid'

    def __init__(self, period):
        self.period = period

        super().__init__(self.period)

    def on_bar(self, bars):
        high = self.source_preference + '_high'
        low = self.source_preference + '_low'
        close = self.source_preference + '_close'

        bars['value'] = talib.ATR(bars[high].values, bars[low].values, bars[close].values, self.period)
        return bars


class KeltnerChannels(Indicator):
    period = 20
    multiplier = 1
    average_true_range_period = 14
    fields = ['low_band', 'middle_band', 'high_bad']
    source_preference = 'bid'

    def __init__(self, period, multiplier, average_true_range_period):
        self.period = 20
        self.multiplier = multiplier
        self.average_true_range_period = average_true_range_period

        super().__init__(period, [{"multiplier": multiplier}, {"average_true_range_period", average_true_range_period}])

    def on_bar(self, bars):
        high = self.source_preference + '_high'
        low = self.source_preference + '_low'
        close = self.source_preference + '_close'

        true_range = talib.ATR(bars[high].values, bars[low].values, bars[close].values, self.average_true_range_period)
        bars['middle_band'] = middle_band = keltner_channel_central(bars[high], bars[low], bars[close], self.period)

        bars['high_band'] = middle_band + (self.multiplier * true_range)
        bars['low_band'] = middle_band - (self.multiplier * true_range)

        return bars


class WilliamsPercentR(Indicator):
    period = 20
    fields = ['value']

    def __init__(self, period):
        self.period = period

        super().__init__(period, [])

    def on_bar(self):
        # Check Logic Here
        return self


class TrendDirectionForceIndex(Indicator):
    period = 20
    fields = ['value']

    def __init__(self, period):
        self.period = period

        super().__init__(period, [])

    def on_bar(self):
        # Check Logic Here
        return self
