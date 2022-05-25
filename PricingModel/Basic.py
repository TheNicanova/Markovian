from PricingModel.Logic.LayerOp import *
from PricingModel.Logic.NodeOp import *
from PricingModel.PricingModel import *


class BasicLayer(LayerOp):

    def update(self, layer):
        layer.update_each_node([
             ContinuationOp(),
             PolicyOp(),
             ValueOp()])


class Basic(PricingModel):

    def train(self, data, option):
        self.pre_training(data, option)

        for layer in self.layer_list:
            BasicLayer().update(layer)







