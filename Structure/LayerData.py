class LayerData(list):


    def __init__(self, arg):
        super().__init__(arg)

        self._regression_result = None

    def get_layer_time(self):
        return self[0].get_time()

    def get_time(self):
        time_list = [node.get_time() for node in self]
        return time_list

    def get_state(self):
        state_list = [node.get_state() for node in self]
        return state_list

    def get_coord(self):
        coord_list = [node.get_coord() for node in self]
        return coord_list

    def get_continuation(self):
        continuation_list = [node.get_continuation() for node in self]
        return continuation_list

    # <Setters>
    def set_regression_result(self, arg):
        self._regression_result = arg
    # </Setters>

    # <Getters>
    def get_regression_result(self):
        return self._regression_result
    # </Getters>