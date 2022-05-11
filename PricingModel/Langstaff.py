import numpy as np

from PricingModel.PricingModel import *
import Logic.LayerLogic as LayerLogic
from config import *
from Utility.Regression import *


class LangStaff(PricingModel):

    def __init__(self, regression_model=None):
        super().__init__()
        if regression_model is None: regression_model = PolynomialRegression()
        self.regression_model = regression_model
        self.name = self.name + "_" + self.regression_model.get_name()

    def get_layer_op_list(self):
        return [LayerLogic.LangStaffLayerOp(regression_model= self.regression_model) for _ in self.layer_data_list]

    def plot(self):
        ax_list = super().plot()
        i = 0
        for layer in self.layer_data_list:
            time = layer.get_layer_time()
            x_min = np.min(layer.get_coord())
            x_max = np.max(layer.get_coord())
            ax_list[i].scatter(layer.get_coord(), layer.get_continuation(), label="continuation",
                               c="green", marker=r'$\clubsuit$')

            x_res = default["x_res"]
            x = np.linspace(x_min, x_max, x_res)

            regression_function = layer.get_regression_result()
            if regression_function is not None:
                y = [regression_function(el) for el in x]
                ax_list[i].plot(x, y, label="regression")
            else:
                ax_list[i].plot(0, 0, label="regression")
            i += 1

        ax_list[-1].legend()
        return ax_list
