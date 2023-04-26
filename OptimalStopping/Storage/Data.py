class Data:
    """
    A Data object is just a container.

    Attributes:
        root : the node we want the price at.
        layer_list : a list of Layer object
        schedule : a list of timestamps
    """
    def __init__(self, root, layer_list, schedule):
        self.root = root
        self.layer_list = layer_list
        self.schedule = schedule


    def get_root(self):
        return self.root

    def get_layer_list(self):
        return self.layer_list

    def get_schedule(self):
        return self.schedule

    def plot(self):
        self.get_root().plot()
