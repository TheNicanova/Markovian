from Structure.LayerData import *
from Structure.NodeData import *

class PricingModel:
    #TODO: Pricing model should be in charge of init the root with the data that it wants
    def __init__(self, root, option):
        self.root = root
        self.node_partition = root.bfs()
        self.node_partition.reverse()  # slow and in place
        self.layer_op_list = []

        # initialize all the layer_data
        self.layer_data_list = [LayerData(node_list) for node_list in self.node_partition]


        # initialize all the nodes
        for layer_data in self.layer_data_list:
            for node_data in layer_data:
                NodeData.init_node_data(node_data, option)

    def get_root_value(self):
        return self.root.get_value()

    def train(self):
        for i in range(len(self.layer_data_list)):
            self.layer_op_list[i].update(self.layer_data_list[i])
