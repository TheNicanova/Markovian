import Plot


class PricingModel:

    def __init__(self):
        self.name = self.__class__.__name__
        self.data = None
        self.option = None

    def get_price(self):
        return self.data.get_root().get_value()

    def train(self, data, option):
        pass

    def get_name(self):
        return self.name

    def plot(self):
        Plot.plot_model(self)
