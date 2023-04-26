import numpy as np

from Utility.Regressions import Polynomial
import Utility.Oracle as Oracle
from .NodeOp import *


class LayerOp:

    def update(self, layer):
        pass


class Control(LayerOp):

    def __init__(self, to_control=None, control_estimate=None, control_expected=None):
        if to_control is None:
            def to_control(node):
                return node.get_continuation()

        if control_estimate is None:
            def control_estimate(node):
                stopped_node_list = node.get_stopped_node()
                european_list = [Oracle.European().put_price(stopped_node) for stopped_node in stopped_node_list]
                return np.average(european_list)

        if control_expected is None:
            def control_expected(node):
                return Oracle.European().put_price(node)

        self.to_control = to_control
        self.control_estimate = control_estimate
        self.control_expected = control_expected

        self.theta = None
        self.control_op = None  # To be initialized once we know theta

    def get_name(self):
        return "european_control"

    def update(self, layer):

        # Get theta
        control_estimate_list = [self.control_estimate(node) for node in layer.get_node()]
        to_control_list = [self.to_control(node) for node in layer.get_node()]
        # TODO: If layer.get_node() is 1: get the theta from the next layer
        if len(layer.get_node()) > 1:

            covariance_matrix = np.cov(control_estimate_list, to_control_list)

            if covariance_matrix[1, 1] > 0:
                self.theta = covariance_matrix[0, 1] / covariance_matrix[1, 1]
            else:
                self.theta = 0
        else:
            self.theta = 0

        # Set theta
        self.control_op = ControlOp(theta=self.theta,
                                    to_control=self.to_control,
                                    control_estimate=self.control_estimate,
                                    control_expected=self.control_expected)

        # Apply control node-wise
        layer.update_each_node([self.control_op])


class Regression(LayerOp):

    def __init__(self, regression_model=None, get_source=None, get_target=None, in_the_money_only=True):
        if regression_model is None:
            regression_model = Polynomial()

        if get_source is None:
            get_source = "get_coord"
        if get_target is None:
            get_target = "get_continuation"

        self.regression_model = regression_model
        self.in_the_money_only = in_the_money_only
        self.get_source = get_source
        self.get_target = get_target

    def get_name(self):
        return self.regression_model.get_name() + "_money=" + str(self.in_the_money_only)

    def update(self, layer):

        node_list = layer.get_node()
        if self.in_the_money_only:
            node_list = [node for node in node_list if node.get_offer() > 0]

        source_list = [node.__getattribute__(self.get_source)() for node in node_list]
        target_list = [node.__getattribute__(self.get_target)() for node in node_list]

        if self.regression_model.can_fit(source_list, target_list):
            continuation_model = self.regression_model.fit(source_list, target_list)
            layer.set_regression_result(continuation_model)
            for node in layer.get_node():
                continuation_model_evaluated = continuation_model(node.get_coord())
                node.set_regression(continuation_model_evaluated)
        else:
            for node in layer.get_node():
                layer.set_regression_result(None)
                node.set_regression(node.get_continuation())
