class LayerPricingData(list):


    def __init__(self, arg):
        super().__init__(arg)
        self.regression_result = None

    def get_state(self):
        state_list = [node.get_state() for node in self]
        return state_list

    def get_coord(self):
        coord_list = [node.get_coord() for node in self]
        return coord_list

    def get_continuation(self):
        continuation_list = [node.pricing_data.get_continuation() for node in self]
        return continuation_list


