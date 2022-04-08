from Node import *


class NodeData(Node):
    """
    Usage: this is an object that holds a node and the data needed for the node logic. It is important (for debugging)
    """

    def __init__(self, state):
        super().__init__(state)

        # Pricing Data
        self._continuation = None
        self._policy = None
        self._value = None
        self._offer = None
        self._regression = None

        # Generator Data



    # **********  <Reading from the "database"> *************
    def get_regression(self):
        return self._regression

    def get_continuation(self):
        return self._continuation

    def get_value(self):
        return self._value

    def get_policy(self):
        return self._policy

    def get_offer(self):
        return self._offer

    # **********  </Reading from the "database"> *************

    # **********  <Writing to the "database"> *************
    def set_continuation(self, arg):
        self._continuation = arg

    def set_value(self, arg):
        self._value = arg

    def set_policy(self, arg):
        self._policy = arg

    def set_offer(self, arg):
        self._offer = arg

    def set_regression(self, arg):
        self._regression = arg
    # **********  </Writing to the "database"> *************
