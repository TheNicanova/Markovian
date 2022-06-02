import OptimalStopping.Utility.Regressions as Regressions

from .PricingModel import *
from .Logic import *


class LongStaffLayerOp(LayerOp):

    def __init__(self, regression_layer=None, option=None):

        self.regression_layer = regression_layer
        self.option = option

    def update(self, layer):

        layer.update_each_node([OfferOp(option=self.option), ContinuationOp()])
        self.regression_layer.update(layer)

        def policy_test(node):
            return node.get_offer() > max(node.get_regression(), 0)

        layer.update_each_node([PolicyOp(test=policy_test), ValueOp()])


class LongStaff(PricingModel):

    def __init__(self, regression_layer=None):
        super().__init__()
        if regression_layer is None:
            regression_layer = Regression(regression_model=Regressions.Polynomial(),
                                          get_source="get_coord",
                                          get_target="get_continuation")
        self.regression_layer = regression_layer
        self.name = self.name + "_" + self.regression_layer.get_name()

        self.option = None

    def train(self, data, option):

        self.root = data.get_root()
        self.layer_list = data.get_layer_list()
        self.option = option

        for layer in self.layer_list:
            LongStaffLayerOp(regression_layer=self.regression_layer, option=self.option).update(layer)
