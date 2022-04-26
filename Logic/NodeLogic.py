import numpy as np


class NodeLogic:
    def update(self, node):
        pass


class ContinuationOp(NodeLogic):
    def update(self, node):
        if node.get_children():
            continuation = np.average([child.get_value() for child in node.get_children()])
        else:
            continuation = 0
        node.set_continuation(continuation)


class ValueOp(NodeLogic):
    def update(self, node):
        if node.get_children():
            # TODO: warning message
            value = np.maximum(node.get_continuation(), node.get_offer())
        else:
            value = node.get_offer()

        node.set_value(value)


class LogLikelihoodOp(NodeLogic):
    def __init__(self, p):
        self.p = p


class RegressionValueOp(NodeLogic):
    def update(self, node):
        if node.get_policy() is False:
            value = node.get_continuation()
            node.set_value(value)
        else:
            ValueOp().update(node)


class RegressionPolicyOp(NodeLogic):

    def update(self, node):
        if node.get_children():
            policy = node.get_offer() > node.get_regression()
        else:
            policy = True

        node.set_policy(policy)


class PolicyOp(NodeLogic):
    def update(self, node):
        if node.get_children():
            policy = node.get_offer() > node.get_continuation()
        else:
            policy = True

        node.set_policy(policy)
