
class Instrument:
    def __init__(self, data):
        self.name = data['name']
        self.precision = data['precision']
        self.market_type = data['marketType']
        self.start_date = data['startDate']
        self.end_date = data['endDate']

    def check_availability(self, start_date, end_date):
        # Check Logic Here
        return (self.start_date <= start_date) and (self.end_date >= end_date)
