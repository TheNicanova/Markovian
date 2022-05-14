from Utility.ControlVariates import *


class NodeOp:
    def update(self, node):
        pass


class ContinuationOp(NodeOp):
    def update(self, node):
        if node.get_children():
            continuation = np.average([child.get_value() for child in node.get_children()])
        else:
            continuation = 0

        node.set_continuation(continuation)


class ValueOp(NodeOp):
    def update(self, node):
        if node.get_policy() is True:
            value = node.get_offer()
        else:
            value = node.get_continuation()

        node.set_value(value)


class PolicyOp(NodeOp):

    def __init__(self, test=None):
        if test is None:
            def test(node):
                return node.get_offer() > node.get_continuation()
        self.test = test

    def update(self, node):

        if node.get_children():
            policy = self.test(node)
        else:
            policy = True

        node.set_policy(policy)


class EuropeanOp(NodeOp):

    def __init__(self, control=None):
        if control is None: control = BM_European
        self.control = control

    def update(self, node):
        european_value = self.control(node)
        node.set_european_continuation_value(european_value)


class LogLikelihoodOp(NodeOp):
    def __init__(self, p):
        self.p = p


class ControlVariateOp(NodeOp):

    def update(self, node):
        if node.get_children():
            pass
        else:
            node.set_control_variate(node.get_offer(node))
