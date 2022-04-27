from Structure.LayerData import *
from Structure.NodeData import *
from config import *
import numpy as np
import math


class PricingModel:

    def __init__(self, root, option):
        self.root = root
        self.option = option
        self.node_partition = root.bfs()
        self.node_partition.reverse()  # slow and in place
        self.layer_op_list = []

        # initialize all the layer_data
        self.layer_data_list = [LayerData(node_list) for node_list in self.node_partition]

        # initialize all the nodes
        for layer_data in self.layer_data_list:
            for node_data in layer_data.get_node():
                NodeData.init_node_data(node_data, option)

    def get_root_value(self):
        return self.root.get_value()

    def train(self):
        for i in range(len(self.layer_data_list)):
            self.layer_op_list[i].update(self.layer_data_list[i])

    def plot(self):
        axs_width = default["axs_width"]
        axs_height = math.ceil(len(self.layer_data_list)//axs_width)
        fig, axs = plt.subplots(axs_width, axs_height)
        i = 0
        ax_list = list(axs.ravel())
        ax_list.reverse()

        for layer in self.layer_data_list:
            time = layer.get_layer_time()
            self.option.plot(time, ax=ax_list[i])
            stop_coord = layer.get_stop()
            stop_y = np.zeros(len(stop_coord))
            ax_list[i].scatter(stop_coord, stop_y)
            ax_list[i].set_xlabel("Coord")
            ax_list[i].set_ylabel("Reward")
            ax_list[i].set_title("At time " + f'{time:.2f}')
            ax_list[i].legend()
            i += 1

        return ax_list
