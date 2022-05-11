from PricingModel.PricingModel import *
import Logic.LayerLogic as LayerLogic


class Basic(PricingModel):

    def __init__(self):
        super().__init__()

    def get_layer_op_list(self):
        return [LayerLogic.BasicLayerOp() for _ in self.layer_data_list]

    def plot(self):
        ax_list = super().plot()
        i = 0
        for layer in self.layer_data_list:
            ax_list[i].scatter(layer.get_coord(), layer.get_continuation(), label="continuation",
                               c="green", marker=r'$\clubsuit$')
            i += 1

