from Structure.LayerData import *
from Structure.NodeData import *
from config import *
import numpy as np
import math


class PricingModel:

    def __init__(self):
        self.name = self.__class__.__name__
        self.root = None
        self.option = None
        self.layer_data_list = None
        self._node_partition = None

    def get_layer_op_list(self):
        raise "not implemented"

    def pre_training(self, root, option):
        self.root = root
        self.option = option
        self._node_partition = root.bfs()
        self._node_partition.reverse()  # slow and in place
        self.layer_data_list = [LayerData(node_list) for node_list in self._node_partition]

        # initialize all the nodes
        for layer_data in self.layer_data_list:
            for node_data in layer_data.get_node():
                NodeData.init_node_data(node_data, option)

    def get_root_value(self):
        return self.root.get_value()

    def train(self, root, option):
        self.pre_training(root, option)
        layer_op_list = self.get_layer_op_list()
        layer_data_list = self.layer_data_list
        for (layer_op, layer_data) in zip(layer_op_list, layer_data_list):
            layer_op.update(layer_data)

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def plot(self):
        axs_width = default["axs_width"]
        axs_height = math.ceil(len(self.layer_data_list) // axs_width)
        fig, axs = plt.subplots(axs_width, axs_height)
        i = 0
        ax_list = list(axs.ravel())
        ax_list.reverse()

        for layer in self.layer_data_list:
            time = layer.get_layer_time()
            x_min = np.min(layer.get_coord())
            x_max = np.max(layer.get_coord())

            self.option.plot(time, ax=ax_list[i], x_min=x_min, x_max=x_max)
            stop_coord = layer.get_stop()
            stop_y = np.zeros(len(stop_coord))
            ax_list[i].scatter(stop_coord, stop_y, label="stopped", marker='H', c='red')
            ax_list[i].set_xlabel("Coord")
            ax_list[i].set_ylabel("Reward")
            ax_list[i].set_title("At time " + f'{time:.2f}')
            i += 1

        ax_list[-1].legend()  # Last / First ax
        return ax_list
