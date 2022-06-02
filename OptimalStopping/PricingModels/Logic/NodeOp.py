import numpy as np


class NodeOp:
    def update(self, node):
        pass


class ContinuationOp(NodeOp):
    def update(self, node):
        if node.get_children():
            children = node.get_children()
            stopped_node_of_children = []
            for child in children:
                stopped_node_of_children = stopped_node_of_children + child.get_stopped_node()
            stopped_offer_list = [stopped_node.get_offer() for stopped_node in stopped_node_of_children]
            continuation = np.average(stopped_offer_list)

        else:
            continuation = 0

        node.set_continuation(continuation)


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


class ValueOp(NodeOp):

    def __init__(self, proxy=None):
        if proxy is None:
            def proxy(node):
                return node.get_continuation()
        self.proxy = proxy

    def update(self, node):
        if node.get_policy() is True:
            value = node.get_offer()
        else:
            value = self.proxy(node)

        node.set_value(value)


class OfferOp(NodeOp):

    def __init__(self, option=None):
        self.option = option

    def update(self, node):
        offer = self.option.payoff_state(node.get_state())
        node.set_offer(offer)


class ControlOp(NodeOp):

    def __init__(self, theta=None, to_control=None, control_estimate=None, control_expected=None):

        self.theta = theta
        self.to_control = to_control
        self.control_estimate = control_estimate
        self.control_expected = control_expected

    def update(self, node):

        controlled = self.to_control(node) - self.theta * (self.control_estimate(node) - self.control_expected(node))

        node.set_control(controlled)
