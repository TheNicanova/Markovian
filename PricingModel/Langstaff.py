import numpy as np

from PricingModel.PricingModel import *
import Logic.LayerLogic as LayerLogic
from config import *

class LangStaff(PricingModel):

    def __init__(self, root, offer):
        super().__init__(root, offer)
        self.layer_op_list = [LayerLogic.LangStaffLayerOp() for _ in self.layer_data_list]

    def plot(self):
        ax_list = super().plot()
        i = 0
        for layer in self.layer_data_list:
            ax_list[i].scatter(layer.get_coord(), layer.get_continuation(), label="continuation",
                               c="green", marker=r'$\clubsuit$')
            x_min = default["x_min"]
            x_max = default["x_max"]
            x_res = default["x_res"]
            x = np.linspace(x_min, x_max, x_res)

            regression_function = layer.get_regression_result()
            if regression_function is not None:
                y = regression_function(x)
                ax_list[i].plot(x, y, label="regression")
            ax_list[i].legend()
            i += 1
        return ax_list
