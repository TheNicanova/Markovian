from .PricingModel import *
from .Logic import *


class RasmussenLayer(LayerOp):

    def __init__(self, control=None, regression=None, value_proxy=None,
                 policy_test=None):

        if control is None:
            control = Control()

        if regression is None:
            regression = Regression()

        if policy_test is None:
            def policy_test(node):
                return node.get_offer() > max(node.get_control(), European().put_price(node))

        if value_proxy is None:
            def value_proxy(node):
                return node.get_control()

        self.control = control
        self.regression = regression
        self.policy_test = policy_test
        self.value_proxy = value_proxy

    def get_name(self):
        return ""

    def update(self, layer):

        LayerOp.update_each_node([ContinuationOp()], layer)

        self.control.update(layer)

        for node in layer.get_node():
            node.set_continuation(node.get_control())

        LayerOp.update_each_node(
            [PolicyOp(test=self.policy_test),
             ValueOp(proxy=self.value_proxy)],
            layer)


class Rasmussen(PricingModel):

    def __init__(self, control=None, regression=None):

        if control is None:
            control = Control()
        self.control = control

        if regression is None:
            regression = Regression()
        self.regression = control

        prototypical_layer = RasmussenLayer(control=self.control, regression=self.regression)
        super().__init__(prototypical_layer)

        self.name = self.name + "_" + prototypical_layer.get_name()
