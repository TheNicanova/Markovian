class NodeData:
    """
    Usage: this is an object that holds a node and the data needed for the node logic. It is important (for debugging)
    """

    def __init__(self, continuation=None, policy=None, value=None, offer=None):

        self.node =


        self.continuation = None
        self.policy = None
        self.value = None
        self.offer = None
        self.regression = None

    # **********  <Reading to the "database"> *************
    def get_regression(self):
        return self.regression

    def get_continuation(self):
        return self.continuation

    def get_value(self):
        return self.value

    def get_policy(self):
        return self.policy

    def get_offer(self):
        return self.offer

    # **********  </Reading to the "database"> *************

    # **********  <Writing to the "database"> *************
    def set_continuation(self, arg):
        self.continuation = arg

    def set_value(self, arg):
        self.value = arg

    def set_policy(self, arg):
        self.policy = arg

    def set_offer(self, arg):
        self.offer = arg

    def set_regression(self, arg):
        self.regression = arg
    # **********  </Writing to the "database"> *************
