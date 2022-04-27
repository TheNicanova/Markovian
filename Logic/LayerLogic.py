from Utility.Regression import *
from Logic.NodeLogic import *


class LayerOperation:

    def update(self, layer):
        pass

    @classmethod
    def update(cls, node_op_list, layer_data):
        for node_data in layer_data.get_node():
            for node_op in node_op_list:
                node_op.update(node_data)


class ContinuationLayerOp(LayerOperation):

    def update(self, layer_data):
        node_op_list = [ContinuationOp()]
        LayerOperation.update(node_op_list, layer_data)


class ValueLayerOp(LayerOperation):

    def update(self, layer_data):
        node_op_list = [ValueOp()]
        LayerOperation.update(node_op_list, layer_data)


class PolicyLayerOp(LayerOperation):

    def update(self, layer_data):
        node_op_list = [PolicyOp()]
        LayerOperation.update(node_op_list, layer_data)


class RegressionPolicyLayerOp(LayerOperation):

    def update(self, layer_data):
        node_op_list = [RegressionPolicyOp()]
        LayerOperation.update(node_op_list, layer_data)


class RegressionValueLayerOp(LayerOperation):

    def update(self, layer_data):
        node_op_list = [RegressionValueOp()]
        LayerOperation.update(node_op_list, layer_data)


class BasicLayerOp(LayerOperation):

    def update(self, layer_data):
        ContinuationLayerOp().update(layer_data)
        ValueLayerOp().update(layer_data)


class RegressionContinuationLayerOp(LayerOperation):

    def __init__(self, regression_model=None):
        if regression_model is None:
            regression_model = PolynomialRegression()
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


class LangStaffLayerOp(LayerOperation):

    def __init__(self, regression_model=None):
        if regression_model is None:
            regression_model = PolynomialRegression()
        self.regression_model = regression_model

    def update(self, layer):
        ContinuationLayerOp().update(layer)
        RegressionContinuationLayerOp(self.regression_model).update(layer)
        RegressionPolicyLayerOp().update(layer)
        RegressionValueLayerOp().update(layer)

