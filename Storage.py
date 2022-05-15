import matplotlib.pyplot as plt


class State:
    """
  The state object

  Attributes:
      time (float) : the total description of a situation includes the time.
      data : the data describing the state.

  """

    def __init__(self, time, data):
        self._time = time
        self._data = data

    def get_time(self):
        """
      Returns:
        the state's coordinate
      """
        return self._time

    def get_coord(self):
        """
    Returns:
        the state's coordinate
    """
        # could do some transformation of data
        return self._data


class Node:

    def __init__(self, state, children=[]):

        self._state = state
        self._children = children
        self._continuation = None
        self._policy = None
        self._value = None
        self._offer = None
        self._regression = None
        self._control_variate = None
        self._controlled = None
        self._european = None
        self._test_value = None

    def init(self, option):
        option_payoff = option.payoff_state(self.get_state())
        self.set_offer(option_payoff)

    # <Getters>

    # **********  <Reading from the "database"> *************

    def get_time(self):
        return self._state.get_time()

    def get_coord(self):
        return self._state.get_coord()

    def get_state(self):
        return self._state

    def get_children(self):
        return self._children

    def get_test_value(self):
        return self._test_value

    def get_european(self):
        return self._european

    def get_regression(self):
        return self._regression

    def get_continuation(self):
        return self._continuation

    def get_value(self):
        return self._value

    def get_policy(self):
        return self._policy

    def get_offer(self):
        return self._offer

    def get_control_variate(self):
        return self._control_variate

    def get_controlled(self):
        return self._controlled

    def get_stopped_node(self):

        # depth first search for stopped nodes
        stack = [self]
        stopped_node = []

        while stack:
            top_node = stack.pop()
            if top_node.get_policy():
                stopped_node.append(top_node)
            else:
                if top_node.get_children():
                    stack = stack + top_node.get_children()
                else:
                    # If there is no children, it must be a stopped node.
                    stopped_node.append(top_node)
        return stopped_node

        # **********  </Reading from the "database"> *************

        # **********  <Writing to the "database"> *************

    def set_children(self, children):
        self._children = children

    def set_test_value(self, arg):
        self._test_value = arg

    def set_continuation(self, arg):
        self._continuation = arg

    def set_value(self, arg):
        self._value = arg

    def set_policy(self, arg):
        self._policy = arg

    def set_offer(self, arg):
        self._offer = arg

    def set_regression(self, arg):
        self._regression = arg

    def set_control_variate(self, arg):
        self._control_variate = arg

    def set_european(self, arg):
        self._european = arg

    def set_controlled(self, arg):
        self._controlled = arg
        # **********  </Writing to the "database"> *************

        # ********* <Utility> *******

    def bfs(self):

        visited = set()

        layer_list = [[self]]
        queue = {self}
        next_generation = []

        while queue:
            for node in queue:
                next_generation += node.get_children()

            unique_next_generation = set(next_generation) - visited
            visited = visited.union(unique_next_generation)
            if unique_next_generation:
                layer_list.append(list(unique_next_generation))
                queue = unique_next_generation.copy()
            else:
                queue = {}

        return layer_list

        # ******* </Utility> *******

        # ******** <Observability> **********

    def plot_child(self, ax=None):
        if ax is None:
            fig, ax = plt.subplots()

        for child in self.get_children():
            parent_state = self.get_state()
            child_state = child.get_state()
            ax.plot([parent_state.get_time(), child_state.get_time()],
                    [parent_state.get_coord(), child_state.get_coord()])
        return ax

    def plot(self):
        self.plot_descendant()

    def plot_descendant(self):
        fig, ax = plt.subplots()
        fig.supxlabel('Time')
        fig.supylabel('Coordinates')
        layer_list = self.bfs()
        for list in layer_list:
            for node in list:
                node.plot_child(ax)

    def recursive_plot(self, ax):
        if self.get_children() is None:
            pass
        else:
            ax = self.plot_child(ax)
            for child in self.get_children():
                if child.children_drawn is False:
                    ax = child.recursive_plot(ax)
                    child.children_drawn = True
        return ax


# ******** </Observability> **********


##### LAYER #####

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

    # </Setters>

    # <Getters>
    def get_regression_result(self):
        return self._regression_result
    # </Getters>
