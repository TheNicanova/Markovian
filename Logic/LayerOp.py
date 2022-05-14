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


class Regression(LayerOp):

    def __init__(self, regression_model=None):
        if regression_model is None:
            regression_model = Utility.Regression.Polynomial()
        self.regression_model = regression_model

    def update(self, layer_data):

        coord_list = layer_data.get_coord()
        target_list = layer_data.get_continuation()

        if self.regression_model.is_fittable(coord_list, target_list):
            continuation_model = self.regression_model.fit(coord_list, target_list)
            layer_data.set_regression_result(continuation_model)
            for node in layer_data.get_node():
                continuation_model_evaluated = continuation_model(node.get_coord())
                node.set_regression(continuation_model_evaluated)
        else:
            for node in layer_data.get_node():
                layer_data.set_regression_result(None)
                node.set_regression(node.get_continuation())


class Rasmussen(LayerOp):

    def __init__(self, control=None, regression_model=None):

        if control is None: control = BM_European
        if regression_model is None: regression_model = Regressu()

        self.control = control
        self.regression_model = regression_model

    def update(self, layer_data):
        LayerOp.update_each_node([ContinuationOp()], layer_data)
        RegressionLayerOp(self.regression_model).update(layer_data)

        LayerOp.update_each_node([EuropeanOp()], layer_data)

        continuation_list = layer_data.get_continuation()
        european_list = layer_data.get_stopped_european()

        control_variate_coefficient = np.corrcoef(continuation_list, european_list)[0, 1]
        print(control_variate_coefficient)

        def get_corrected_value(node):
            stopped_node = node.get_stopping_node()
            stopped_european = stopped_node.get_european_continuation_value()
            stopped_offer = stopped_node.get_offer()

            corrected = node.get_regression() - control_variate_coefficient * (stopped_european - stopped_offer)

            return max(corrected, node.get_european_continuation_value())

        LayerOp.update_each_node([PolicyOp(get_test_value=get_corrected_value), ValueOp()], layer_data)


class LangStaffLayerOp(LayerOp):

    def __init__(self, regression_model=None):
        if regression_model is None:
            regression_model = Utility.Regression.Polynomial()

        self.regression_model = regression_model


    def update(self, layer_data):
        LayerOp.update_each_node(
            [ContinuationOp()],
            layer_data)

        Regression(self.regression_model).update(layer_data)

        def test(node):
            return node.get_offer() > node.get_regression()

        LayerOp.update_each_node(
            [PolicyOp(test),
             ValueOp()],
            layer_data)
