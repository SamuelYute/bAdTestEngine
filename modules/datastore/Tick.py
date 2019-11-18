import random


class Tick:
    timestamp = None
    precision = None
    average_spread = 2.5
    spread_range = 10
    spread = 0
    bid = 0.0
    ask = 0.0
    volume = 0.0

    def __init__(self, timestamp, price, volume, precision, average_spread, spread_range_percentage):
        self.timestamp = timestamp
        self.precision = precision
        self.average_spread = average_spread
        self.spread = self.get_spread()
        self.spread_range = spread_range_percentage
        self.bid = round(price, precision)
        self.ask = round(self.bid+self.spread, precision)
        self.volume = volume

    def get_spread(self):
        if self.average_spread == 0:
            return 0

        if self.spread_range > 0:
            range_value = (self.spread_range/100)*self.average_spread
            variation = random.uniform(-range_value, range_value)
        else:
            variation = 0

        return round(((self.average_spread+variation)/pow(10, self.precision-1)), self.precision)


