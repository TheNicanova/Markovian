from PricingModel.Regression import *
from PricingModel.Logic.NodeOperation import *


class LayerOperation:

    def update(self, layer):
        pass

    @classmethod
    def update(cls, node_op_list, layer):
        for node in layer:
            for node_op in node_op_list:
                node_op.update(node)


class ContinuationLayerOp(LayerOperation):

    def update(self, layer):
        node_op_list = [ContinuationOp()]
        LayerOperation.update(node_op_list, layer)


class ValueLayerOp(LayerOperation):

    def update(self, layer):
        node_op_list = [ValueOp()]
        LayerOperation.update(node_op_list, layer)


class PolicyLayerOp(LayerOperation):

    def update(self, layer):
        node_op_list = [PolicyOp()]
        LayerOperation.update(node_op_list, layer)


class RegressionPolicyLayerOp(LayerOperation):

    def update(self, layer):
        node_op_list = [RegressionPolicyOp()]
        LayerOperation.update(node_op_list, layer)


class RegressionValueLayerOp(LayerOperation):

    def update(self, layer):
        node_op_list = [RegressionValueOp()]
        LayerOperation.update(node_op_list, layer)



class BasicLayerOp(LayerOperation):
    def update(self, layer):
        ContinuationLayerOp().update(layer)
        ValueOp().update(layer)


class RegressionContinuationLayerOp(LayerOperation):

    def __init__(self, regression_model=None):
        if regression_model is None:
            regression_model = PolynomialRegression()
        self.regression_model = regression_model

    def update(self, layer):

        coord_list = layer.get_coord()
        target_list = layer.get_continuation()

        if self.regression_model.is_fittable(coord_list, target_list):
            continuation_model = self.regression_model.fit(coord_list, target_list)
            layer.regression_result = continuation_model
            for node in layer:
                continuation_model_evaluated = continuation_model(node.get_coord())
                node.pricing_data.regression = continuation_model_evaluated
        else:
            for node in layer:
                layer.regression_result = None
                node.pricing_data.regression = node.pricing_data.get_continuation()


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
