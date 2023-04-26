from .PricingModel import *
from .Logic import *
from Utility.Regressions import Polynomial
import Utility.Oracle as Oracle
import numpy as np


class RasmussenLayerOp(LayerOp):

    def __init__(self, control_layer=None, regression_layer=None, value_proxy=None,
                 policy_test=None, option=None):
        self.control_layer = control_layer
        self.regression_layer = regression_layer
        self.value_proxy = value_proxy
        self.policy_test = policy_test
        self.option = option

    def update(self, layer):
        layer.update_each_node([OfferOp(option=self.option), ContinuationOp()])

        self.control_layer.update(layer)

        for node in layer.get_node():
            node.set_continuation(node.get_control())

        layer.update_each_node(
            [PolicyOp(test=self.policy_test),
             ValueOp(proxy=self.value_proxy)])


class Rasmussen(PricingModel):

    def __init__(self, control_layer=None, regression_layer=None, value_proxy=None,
                 policy_test=None):
        super().__init__()

        if control_layer is None:
            def to_control(node):
                return node.get_continuation()

            def control_estimate(node):
                stopped_node_list = node.get_stopped_node()
                european_list = [Oracle.European().put_price(stopped_node) for stopped_node in stopped_node_list]
                return np.average(european_list)

            def control_expected(node):
                return Oracle.European().put_price(node)

            control_layer = Control(to_control=to_control,
                                    control_estimate=control_estimate,
                                    control_expected=control_expected)

        if regression_layer is None:
            get_source = "get_coord"
            get_target = "get_continuation"
            regression_model = Polynomial()
            regression_layer = Regression(regression_model=regression_model,
                                          get_source=get_source,
                                          get_target=get_target)

        if value_proxy is None:
            def value_proxy(node):
                return node.get_control()
        if policy_test is None:
            def policy_test(node):
                return node.get_offer() > max(node.get_control(), Oracle.European().put_price(node))

        self.control_layer = control_layer
        self.regression_layer = regression_layer
        self.value_proxy = value_proxy
        self.policy_test = policy_test
        self.option = None
        self.name = self.name + "_" + self.regression_layer.get_name() + "_" + self.control_layer.get_name()

    def train(self, data, option):

        self.data = data
        self.option = option

        for layer in self.data.get_layer_list():
            RasmussenLayerOp(control_layer=self.control_layer,
                             regression_layer=self.regression_layer,
                             value_proxy=self.value_proxy,
                             policy_test=self.policy_test,
                             option=self.option
                             ).update(layer)

    def get_name(self):
        return "Rasmussen"
