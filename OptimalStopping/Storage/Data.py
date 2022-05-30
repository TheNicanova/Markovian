class Data:

    def __init__(self, root, layer_list):
        self.root = root
        self.layer_list = layer_list

    def get_root(self):
        return self.root

    def get_layer_list(self):
        return self.layer_list

    def plot(self):
        self.get_root().plot()
