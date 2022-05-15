from Logic.NodeOp import *
from Utility.ControlVariates import *
import Utility.Regression


class LayerOp:

    def update(self, layer):
        pass

    @classmethod
    def update_each_node(cls, node_op_list, layer):
        for node_data in layer.get_node():
            for node_op in node_op_list:
                node_op.update(node_data)


class Basic(LayerOp):

    def update(self, layer):
        LayerOp.update_each_node(
            [ContinuationOp(),
             PolicyOp(),
             ValueOp()],
            layer)


class ControlVariate(LayerOp):

    def __init__(self, control=None):
        if control is None: control = BM_European
        self.control = control

    def update(self, layer):
        modeled_continuation_list = layer.get_regression_result()
        european_list = layer.get_stopped_european()
        print("there are " + str(len(layer.get_node())))
        covariance_matrix = np.cov(modeled_continuation_list, european_list)
        control_variate_coefficient = covariance_matrix[0, 1] / covariance_matrix[1, 1]
        print(control_variate_coefficient)

        for node in layer.get_node():
            european = node.get_european()

            stopped_node = node.get_stopped_node()
            stopped_european = stopped_node.get_european()

            controlled = node.get_regression() - control_variate_coefficient * (stopped_european - european)
            node.set_controlled(controlled)


class Regression(LayerOp):
    # TODO: Make Regression layer independent of coord and continuation.

    def __init__(self, regression_model=None, in_the_money_only=True):
        if regression_model is None:
            regression_model = Utility.Regression.Polynomial()
        self.regression_model = regression_model
        self.in_the_money_only = in_the_money_only

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

        def test(node):
            return node.get_offer() > node.get_regression()

        self.test = test

    def update(self, layer_data):
        LayerOp.update_each_node(
            [ContinuationOp()],
            layer_data)

        Regression(self.regression_model).update(layer_data)
        LayerOp.update_each_node(
            [PolicyOp(self.test),
             ValueOp()],
            layer_data)


class Rasmussen(LayerOp):

    def __init__(self, control=None, regression_model=None):

        if control is None: control = BM_European
        if regression_model is None: regression_model = Utility.Regression.Polynomial()

        def test(node):
            return node.get_offer() > max(node.get_controlled(), node.get_european())

        self.control = control
        self.regression_model = regression_model
        self.test = test

    def update(self, layer):

        LayerOp.update_each_node([ContinuationOp()], layer)

        Regression(self.regression_model).update(layer)

        LayerOp.update_each_node([EuropeanOp()], layer)  # Setting all nodes to the european option

        ControlVariate().update(layer)

        LayerOp.update_each_node([PolicyOp(test=self.test), RasmussenValueOp()], layer)
