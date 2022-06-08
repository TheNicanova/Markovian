import OptimalStopping.config as config
import OptimalStopping.Utility.Schedule as Schedule
import OptimalStopping.Storage as Storage


class UnderlyingModel:
    """
  The process governing the evolution of a state through time.

  forward_to(state,forward_time) : expects a state object and a future time; returns a state object sampled at the future time.

  """

    @classmethod
    def new_node(cls, state):
        return Storage.Node(state)

    @classmethod
    def new_layer(cls, node_list):
        return Storage.Layer(node_list)

    @classmethod
    def get_default_schedule(cls):
        return Schedule.Linear()

    def __init__(self):
        self.name = "No name given yet."
        pass

    def get_name(self):
        return self.name

    def forward_to(self, state, forward_time):
        pass

    def genesis(self):
        pass

    def get_default_node(self):
        return self.new_node(self.genesis())

    def generate_path(self, node=None, schedule=None):

        # Setting defaults
        if node is None: node = self.get_default_node()
        if schedule is None: schedule = self.get_default_schedule()

        # Making sure the beginning of the schedule matches with the initial state
        assert node.get_state().get_time() == schedule[0]

        acc = node
        for i in range(1, len(schedule)):
            acc.set_children([self.new_node(self.forward_to(acc.get_state(), schedule[i]))])
            acc = acc.get_children()[0]
        return node

    def generate_children(self, node, forward_time, n=config.default["num_of_paths"]):

        assert n > 0

        children = node.get_children()
        new_children = [self.new_node(self.forward_to(node.get_state(), forward_time)) for _ in range(n)]
        node.set_children(children + new_children)

        return node

    def generate_paths(self, node=None, schedule=None, n=config.default["num_of_paths"]):

        # Setting defaults
        if node is None: node = self.get_default_node()
        if schedule is None: schedule = self.get_default_schedule()

        # Making sure the beginning of the schedule matches with the initial state
        assert node.get_state().get_time() == schedule[0]
        assert n > 0

        self.generate_children(node, schedule[1], n)

        # Setting defaults
        for child in node.get_children():
            self.generate_path(child, schedule[1:])

        node_partition = node.bfs()
        node_partition.reverse()
        layer_list = [Storage.Layer(node_list) for node_list in node_partition]

        return Storage.Data(node, layer_list, schedule)
