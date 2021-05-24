class Company:

    companies = []

    def __init__(self, name, symbol, price):
        self.name = name
        self.symbol = symbol
        self.price = price
        self.companies.append(self)

    def get_name(self):
        return self.name

    def get_symbol(self):
        return self.symbol

    def get_price(self):
        return self.price

