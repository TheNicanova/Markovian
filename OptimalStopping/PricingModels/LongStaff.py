import OptimalStopping.Utility.Regressions as Regressions

from .PricingModel import *
from .Logic import *


class LongStaffLayerOp(LayerOp):

    def __init__(self, regression_model=None):
        if regression_model is None:
            regression_model = Regressions.Polynomial()

        self.regression_model = regression_model

        def policy_test(node):
            return node.get_offer() > node.get_regression()

        self.regression_model = regression_model
        self.policy_test = policy_test

    def update(self, layer):

        layer.update_each_node([ContinuationOp()])

        Regression(self.regression_model).update(layer)

        layer.update_each_node([PolicyOp(test=self.policy_test), ValueOp()])


class LongStaff(PricingModel):

    def __init__(self, regression_model=None):
        super().__init__()
        if regression_model is None: regression_model = Regressions.Polynomial()
        self.regression_model = regression_model

        self.name = self.name + "_" + self.regression_model.get_name()

    def train(self, data, option):
        self.root = data.get_root()
        self.layer_list = data.get_layer_list()
        self.option = option

        for layer in self.layer_list:
            layer.update_each_node([OfferOp(option=self.option)])
            LongStaffLayerOp(regression_model=self.regression_model).update(layer)


