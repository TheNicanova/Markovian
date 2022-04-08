from LayerData import *
from LayerLogic import *


class PricingModel:

    def __init__(self, root, offer_fun):
        self.root = root
        self.node_partition = root.bfs()
        self.node_partition.reverse() # slow and in place
        self.layer_op_list = []

        # initialize all the layer_data
        self.layer_data_list = []
        for node_list in self.node_partition:
            self.layer_data_list.append(LayerData(node_list))

        # initialize all the nodes
        for layer in self.layer_data_list:
            for node in layer:
                NodeOperation.init_node(node, offer_fun)

    def get_root_value(self):
        return self.root.get_value()


    def train(self):
        for i in range(len(self.layer_data_list)):
            self.layer_op_list[i].update(self.layer_data_list[i])


class LangStaff(PricingModel):

    def __init__(self, root, offer):
        super().__init__(root, offer)
        self.layer_op_list = [LangStaffLayerOp() for _ in self.layer_data_list]

