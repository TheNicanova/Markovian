class Layer:

    def __init__(self, arg):
        self.node_list = arg
        self._regression_result = None

    def get_node(self):
        return self.node_list

    def get_layer_time(self):
        return self.get_node()[0].get_time()

    def get_time(self):
        time_list = [node.get_time() for node in self.node_list]
        return time_list

    def get_state(self):
        state_list = [node.get_state() for node in self.node_list]
        return state_list

    def get_coord(self):
        coord_list = [node.get_coord() for node in self.node_list]
        return coord_list

    def get_continuation(self):
        continuation_list = [node.get_continuation() for node in self.node_list]
        return continuation_list

    def get_stop(self):
        stop_list = [node.get_coord() for node in self.node_list if node.get_policy()]
        return stop_list

    def get_regression(self):
        regression_list = [node.get_regression() for node in self.node_list]
        return regression_list

    def get_stopped_node(self):
        node_list = self.get_node()
        stopped_node_list = []
        for node in node_list:
            stopped_node_list = stopped_node_list + node.get_stopped_node()

        return stopped_node_list

    def get_stopped_european(self):
        stopped_node_list = self.get_stopped_node()
        european_list = [stopped_node.get_european() for stopped_node in stopped_node_list]

        return european_list

    # <Setters>
    def set_regression_result(self, arg):
        self._regression_result = arg

    def update_each_node(self, node_op_list):
        for node_data in self.get_node():
            for node_op in node_op_list:
                node_op.update(node_data)


    # </Setters>

    # <Getters>
    def get_regression_result(self):
        return self._regression_result
    # </Getters>
