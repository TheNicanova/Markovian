from PricingModel.PricingModel import PricingModel
import PricingModel.Logic as Logic


class LongStaff(PricingModel):

    def __init__(self, regression_model=None):
        prototypical_layer = Logic.LayerOp.LongStaffLayerOp(regression_model=regression_model)
        super().__init__(prototypical_layer)

        self.name = self.name + "_" + prototypical_layer.regression_model.get_name()