from modules.datastore.Store import Store
from modules.datastore.Tick import Tick


class Server:
    def __init__(self):
        self.me = 1

    def run(self):
        return self


class Strategy:
    instrument = 'EURUSD'
    start_date = '2018-01-01'
    end_date = '2018-12-31'
    time_frame = '1H'
    columns = ['open', 'high', 'low', 'close']
    precision = 5
    average_pip_spread = 0
    spread_range_percentage = 10

    store = None
    server = Server()

    def __init__(self):
        self.store = Store

    def initialize(self):
        return self

    def on_tick(self):
        return self

    def on_bar(self):
        return self

    def on_position_open(self):
        return self

    def on_position_close(self):
        return self

    def on_position_update(self):
        return self

    def run(self):
        self.server.run()
