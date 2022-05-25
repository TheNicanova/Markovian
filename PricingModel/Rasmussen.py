from PricingModel.PricingModel import PricingModel
import PricingModel.Logic as Logic


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
