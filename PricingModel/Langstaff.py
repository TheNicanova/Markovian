from PricingModel.PricingModel import *
import Logic.LayerLogic as LayerLogic


class LangStaff(PricingModel):

    def __init__(self, root, offer):
        super().__init__(root, offer)
        self.layer_op_list = [LayerLogic.LangStaffLayerOp() for _ in self.layer_data_list]
