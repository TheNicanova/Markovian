from PricingModel.PricingModel import *
import Logic.LayerLogic as LayerLogic


class LangStaff(PricingModel):

    def __init__(self, root, offer):
        super().__init__(root, offer)
        self.layer_op_list = [LayerLogic.LangStaffLayerOp() for _ in self.layer_data_list]

    def plot(self):
        ax_list = super().plot()
        i = 0

        for layer in self.layer_data_list:
            ax_list[i].scatter(layer.get_coord(), layer.get_continuation(), color="orange")
            i += 1
        return ax_list
