import numpy as np
import matplotlib.pyplot as plt
import math
import copy
import Logic.LayerOp
import Storage
import _config


class PricingModel:

    def __init__(self, layer_op):
        self.name = self.__class__.__name__
        self.root = None
        self.option = None
        self.layer_list = None
        self._node_partition = None
        self.layer_op = layer_op

    def pre_training(self, root, option):
        self.root = copy.deepcopy(root)
        self.option = option
        self._node_partition = self.root.bfs()
        self._node_partition.reverse()  # slow and in place

        # initialize all the storage layers
        self.layer_list = [Storage.Layer(node_list) for node_list in self._node_partition]

        # initialize all the storage nodes
        for layer in self.layer_list:
            for node in layer.get_node():
                node.init(option)

    def get_root_value(self):
        return self.root.get_value()

    def train(self, root, option):
        self.pre_training(root, option)

        for layer in self.layer_list:
            self.layer_op.update(layer)

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def plot(self):

        axs_width = _config.default["axs_width"]
        axs_height = math.ceil(len(self.layer_list) // axs_width)
        fig, axs = plt.subplots(axs_width, axs_height)
        fig.supxlabel(self.get_name())

        i = 0
        ax_list = list(axs.ravel())
        ax_list.reverse()

        for layer in self.layer_list:

            time = layer.get_layer_time()
            x_min = np.min(layer.get_coord())
            x_max = np.max(layer.get_coord())

            self.option.plot(time, ax=ax_list[i], x_min=x_min, x_max=x_max)
            stop_coord = layer.get_stop()
            stop_y = np.zeros(len(stop_coord))
            ax_list[i].scatter(stop_coord, stop_y, s=75, label="stopped", marker='H', c='red')

            if layer.get_continuation():
                ax_list[i].scatter(layer.get_coord(), layer.get_continuation(), label="continuation",
                                   c="green", marker=r'$\clubsuit$')
            if layer.get_regression_result():
                regression_function = layer.get_regression_result()

                x_res = _config.default["x_res"]
                x = np.linspace(x_min, x_max, x_res)

                y = [regression_function(el) for el in x]
                ax_list[i].plot(x, y, label="regression")

            ax_list[i].set_xlabel("Coord")
            ax_list[i].set_ylabel("Reward")
            ax_list[i].set_title("At time " + f'{time:.2f}')
            i += 1

        ax_list[-1].legend()  # Last / First ax
        return ax_list


class Basic(PricingModel):

    def __init__(self):
        prototypical_layer = Logic.LayerOp.Basic()

        super().__init__(prototypical_layer)


class LongStaff(PricingModel):

    def __init__(self, regression_model=None):
        prototypical_layer = Logic.LayerOp.LongStaffLayerOp(regression_model=regression_model)
        super().__init__(prototypical_layer)

        self.name = self.name + "_" + prototypical_layer.regression_model.get_name()


class Rasmussen(PricingModel):

    def __init__(self, control=None, regression=None):

        if control is None:
            control = Logic.LayerOp.Control()
        self.control = control

        if regression is None:
            regression = Logic.LayerOp.Regression()
        self.regression = control

        prototypical_layer = Logic.LayerOp.Rasmussen(control=self.control, regression=self.regression)
        super().__init__(prototypical_layer)

        self.name = self.name + "_" + prototypical_layer.get_name()
