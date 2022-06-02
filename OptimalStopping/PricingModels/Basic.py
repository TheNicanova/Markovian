from .Logic import *
from .PricingModel import PricingModel


class Basic(PricingModel):

    def train(self, data, option):
        self.root = data.get_root()
        self.layer_list = data.get_layer_list()
        self.option = option

        for layer in self.layer_list:
            layer.update_each_node([
                OfferOp(option=self.option),
                ContinuationOp(),
                PolicyOp(),
                ValueOp()])
