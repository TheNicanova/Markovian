import numpy as np
from PricingModel.Data.NodePricingData import NodePricingData


class NodeOperation:
    def update(self, node):
        pass

    # TODO: find a principled way to initialize the pricing_data and layer_data
    @classmethod
    def init_node(cls, node, offer_obj):
        offer_payoff = offer_obj.payoff_state(node.get_state())
        pricing_data = NodePricingData(offer=offer_payoff)
        node.pricing_data = pricing_data


class ContinuationOp(NodeOperation):
    def update(self, node):
        if node.children:
            continuation = np.average([child.pricing_data.get_value() for child in node.children])
        else:
            continuation = 0
        node.pricing_data.set_continuation(continuation)
        return continuation


class ValueOp(NodeOperation):
    def update(self, node):
        if node.children:
            # TODO: warning message
            value = np.maximum(node.pricing_data.get_continuation(), node.pricing_data.get_offer())
        else:
            value = node.pricing_data.get_offer()

        node.pricing_data.set_value(value)
        return value


class RegressionValueOp(NodeOperation):
    def update(self, node):
        if node.pricing_data.get_policy() is False:
            value = node.pricing_data.get_continuation()
            node.pricing_data.set_value(value)
        else:
            value = ValueOp().update(node)

        return value


class RegressionPolicyOp(NodeOperation):

    def update(self, node):
        if node.children:
            policy = node.pricing_data.get_offer() > node.pricing_data.regression
        else:
            policy = True

        node.pricing_data.set_policy(policy)
        return policy


class PolicyOp(NodeOperation):
    def update(self, node):
        if node.children:
            policy = node.pricing_data.get_offer() > node.pricing_data.get_continuation()
        else:
            policy = True

        node.pricing_data.set_policy(policy)
        return policy
