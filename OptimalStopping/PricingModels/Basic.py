from .Logic import *
from .PricingModel import PricingModel


class BasicLayer(LayerOp):

    def update(self, layer):
        layer.update_each_node([
            ContinuationOp(),
            PolicyOp(),
            ValueOp()])


class Basic(PricingModel):

    def train(self, data, option):
        self.root = data.get_root()
        self.layer_list = data.get_layer_list()
        self.option = option

        for layer in self.layer_list:
            layer.update_each_node([OfferOp(option=self.option)])
            BasicLayer().update(layer)
