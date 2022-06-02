from .Logic import *
from .PricingModel import PricingModel


class BasicLayerOp(LayerOp):
    def __init__(self, option=None):
        self.option = option

    def update(self, layer):
        layer.update_each_node([
            OfferOp(option=self.option),
            ContinuationOp(),
            PolicyOp(),
            ValueOp()])


class Basic(PricingModel):

    def train(self, data, option):
        self.root = data.get_root()
        self.layer_list = data.get_layer_list()
        self.option = option

        for layer in self.layer_list:
            BasicLayerOp(option=self.option).update(layer)
