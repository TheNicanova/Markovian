import numpy as np

import _config
import Storage


class UnderlyingGenerator:
    """
  The process governing the evolution of a state through time.

  forward_to(state,forward_time) : expects a state object and a future time; returns a state object sampled at the future time.

  """

    @classmethod
    def new_node(cls, state):
        return Storage.Node(state)

    @classmethod
    def get_default_schedule(self):
        return np.linspace(_config.default["initial_time"], _config.default["terminal_time"], _config.default["num_of_timestamps"])

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

    def generate_children(self, node, forward_time, n=_config.default["num_of_paths"]):

        assert n > 0

        children = node.get_children()
        new_children = [self.new_node(self.forward_to(node.get_state(), forward_time)) for _ in range(n)]
        node.set_children(children + new_children)

        return node

    def generate_paths(self, node=None, schedule=None, n=_config.default["num_of_paths"]):

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
        return node


class GeometricBrownianMotion(UnderlyingGenerator):
    """
  A concrete class of Underlying model.
  """

    def __init__(self, rate=None, sigma=None, dividend=None):
        super().__init__()
        # To be modularized ...
        self.name = "Geometric Brownian Motion"
        self.rng = np.random.default_rng()

        if rate is None: rate = _config.gbm_default['rate']
        if sigma is None: sigma = _config.gbm_default['sigma']
        if dividend is None: dividend = _config.gbm_default['dividend']

        self.rate = rate
        self.sigma = sigma
        self.dividend = dividend

    def forward_to(self, initial_state, forward_time):
        """
    Takes a state object (initial_state) and a time greater than the state's time (forward_time).
    Returns the state obtained from simulating the process starting in initial_state and stopping at forward_time.
    """
        dt = forward_time - initial_state.get_time()
        assert dt >= 0  # Making sure we are asked to generate a state at a later time than the initial state
        updated_coord = initial_state.get_coord() * np.exp((
                                                                   self.rate - self.dividend - self.sigma ** 2.0 / 2.0) * dt + self.sigma * dt ** 0.5 * self.rng.standard_normal())

        return Storage.State(forward_time, updated_coord)

    def genesis(self):
        # Returns a default state.
        return Storage.State(_config.default["initial_time"], 1.0)

    def generate_lattice(self, node=None, schedule=None, n=None):

        # Setting defaults
        if node is None: node = self.get_default_node()
        if schedule is None: schedule = self.get_default_schedule()

        # Making sure the beginning of the schedule matches with the initial node
        assert node.get_time() == schedule[0]

        root = node
        lattice = []

        # lattice is a list of list
        lattice.append([node])

        for t in range(1, len(schedule)):

            # timestamps
            last_timestamp = schedule[t - 1]
            timestamp = schedule[t]
            dt = timestamp - last_timestamp

            # ups and downs
            u = np.exp(self.sigma * np.sqrt(dt))
            d = 1 / u

            current_layer = lattice[-1]
            next_layer = []

            # Populating next layer
            next_lowest_node_coord = current_layer[0].get_state().get_coord() * d
            next_lowest_node = self.new_node(Storage.State(timestamp, next_lowest_node_coord))
            next_layer.append(next_lowest_node)

            for node in current_layer:
                next_higher_node_coord = node.get_coord() * u
                next_higher_node = self.new_node(Storage.State(timestamp, next_higher_node_coord))
                next_layer.append(next_higher_node)

            # Connecting current layer to next layerù
            for i in range(len(current_layer)):
                lower_child = next_layer[i]
                higher_child = next_layer[i + 1]
                current_layer[i].set_children([lower_child, higher_child])

            lattice.append(next_layer)
        return root


class BrownianMotion(UnderlyingGenerator):

    def forward_to(self, state, forward_time):
        pass

    def genesis(self):
        pass
