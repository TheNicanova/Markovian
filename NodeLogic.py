import numpy as np
from NodeData import *


class NodeOperation:
    def update(self, node):
        pass

    # TODO: find a principled way to initialize the NodeData and layer_data

    @classmethod
    def init_node(cls, node, offer_obj):
        offer_payoff = offer_obj.payoff_state(node.get_state())
        node.set_offer(offer_payoff)


class ContinuationOp(NodeOperation):
    def update(self, node):
        if node.get_children():
            continuation = np.average([child.get_value() for child in node.get_children()])
        else:
            continuation = 0
        node.set_continuation(continuation)


class ValueOp(NodeOperation):
    def update(self, node):
        if node.get_children():
            # TODO: warning message
            value = np.maximum(node.get_continuation(), node.get_offer())
        else:
            value = node.get_offer()

        node.set_value(value)


class LogLikelihoodOp(NodeOperation):
    def __init__(self, p):
        self.p = p


class RegressionValueOp(NodeOperation):
    def update(self, node):
        if node.get_policy() is False:
            value = node.get_continuation()
            node.set_value(value)
        else:
            ValueOp().update(node)


class RegressionPolicyOp(NodeOperation):

    def update(self, node):
        if node.get_children():
            policy = node.get_offer() > node.get_regression()
        else:
            policy = True

        node.set_policy(policy)


class PolicyOp(NodeOperation):
    def update(self, node):
        if node.get_children():
            policy = node.get_offer() > node.get_continuation()
        else:
            policy = True

        node.set_policy(policy)
