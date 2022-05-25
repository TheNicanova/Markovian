import numpy as np

import Utility


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
                european_list = [European().put_price(stopped_node) for stopped_node in stopped_node_list]
                return np.average(european_list)

        if control_expected is None:
            def control_expected(node):
                return European().put_price(node)

        self.to_control = to_control
        self.control_estimate = control_estimate
        self.control_expected = control_expected

        self.control_op = ControlOp(to_control=self.to_control,
                                    control_estimate=self.control_estimate,
                                    control_expected=self.control_expected)

        self.theta = None

    def update(self, layer):

        # Get theta
        control_estimate_list = [self.control_estimate(node) for node in layer.get_node()]
        to_control_list = [self.to_control(node) for node in layer.get_node()]

        if len(layer.get_node()) > 1:

            covariance_matrix = np.cov(control_estimate_list, to_control_list)

            if covariance_matrix[1, 1] > 0:
                self.theta = covariance_matrix[0, 1] / covariance_matrix[1, 1]
            else:
                self.theta = 0
        else:
            self.theta = 0

        # Set theta
        self.control_op.theta = self.theta

        # Apply control node wise
        LayerOp.update_each_node([self.control_op], layer)


class Regression(LayerOp):
    # TODO: Make Regression layer independent of coord and continuation.

    def __init__(self, regression_model=None, in_the_money_only=True):
        if regression_model is None:
            regression_model = Utility.Regression.Polynomial()
        self.regression_model = regression_model
        self.in_the_money_only = in_the_money_only

    def get_name(self):
        return self.regression_model.get_name() + "_money=" + str(self.in_the_money_only)

    def update(self, layer):

        if self.in_the_money_only:
            node_list = layer.get_node()
            in_the_money_node_list = [node for node in node_list if node.get_offer() > 0]
            coord_list = [node.get_coord() for node in in_the_money_node_list]
            target_list = [node.get_continuation() for node in in_the_money_node_list]

        else:
            coord_list = layer.get_coord()
            target_list = layer.get_continuation()

        if self.regression_model.is_fittable(coord_list, target_list):
            continuation_model = self.regression_model.fit(coord_list, target_list)
            layer.set_regression_result(continuation_model)
            for node in layer.get_node():
                continuation_model_evaluated = continuation_model(node.get_coord())
                node.set_regression(continuation_model_evaluated)
        else:
            for node in layer.get_node():
                layer.set_regression_result(None)
                node.set_regression(node.get_continuation())


class LongStaffLayerOp(LayerOp):

    def __init__(self, regression_model=None):
        if regression_model is None:
            regression_model = Utility.Regression.Polynomial()

        self.regression_model = regression_model

        def policy_test(node):
            return node.get_offer() > node.get_regression()

        self.regression_model = regression_model
        self.policy_test = policy_test

    def update(self, layer):
        LayerOp.update_each_node(
            [ContinuationOp()],
            layer)

        Regression(self.regression_model).update(layer)

        LayerOp.update_each_node(
            [PolicyOp(test=self.policy_test),
             ValueOp()],
            layer)


class Rasmussen(LayerOp):

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
