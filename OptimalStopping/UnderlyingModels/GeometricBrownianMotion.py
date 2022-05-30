import numpy as np
import OptimalStopping.config as config

from OptimalStopping.Storage import *
from .UnderlyingModel import UnderlyingModel


class GeometricBrownianMotion(UnderlyingModel):
    """
  A concrete class of Underlying model.
  """

    def __init__(self, rate=None, sigma=None, dividend=None):
        super().__init__()
        self.name = "Geometric Brownian Motion"
        self.rng = np.random.default_rng()

        if rate is None: rate = config.gbm_default['rate']
        if sigma is None: sigma = config.gbm_default['sigma']
        if dividend is None: dividend = config.gbm_default['dividend']

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

        return State(forward_time, updated_coord)

    def genesis(self):
        # Returns a default state.
        return State(config.default["initial_time"], 1.0)

    def generate_lattice(self, node=None, schedule=None, n=None):

        # Setting defaults
        if node is None: node = self.get_default_node()
        if schedule is None: schedule = self.get_default_schedule()

        # Making sure the beginning of the schedule matches with the initial node
        assert node.get_time() == schedule[0]

        root = node
        layer_list = []

        # lattice is a list of list
        layer_list.append([node])

        for t in range(1, len(schedule)):

            # timestamps
            last_timestamp = schedule[t - 1]
            timestamp = schedule[t]
            dt = timestamp - last_timestamp

            # ups and downs
            u = np.exp(self.sigma * np.sqrt(dt))
            d = 1 / u

            current_layer = layer_list[-1]
            next_layer = []

            # Populating next layer
            next_lowest_node_coord = current_layer[0].get_state().get_coord() * d
            next_lowest_node = self.new_node(State(timestamp, next_lowest_node_coord))
            next_layer.append(next_lowest_node)

            for node in current_layer:
                next_higher_node_coord = node.get_coord() * u
                next_higher_node = self.new_node(State(timestamp, next_higher_node_coord))
                next_layer.append(next_higher_node)

            # Connecting current layer to next layer
            for i in range(len(current_layer)):
                lower_child = next_layer[i]
                higher_child = next_layer[i + 1]
                current_layer[i].set_children([lower_child, higher_child])

            layer_list.append(next_layer)

        layer_list.reverse()
        layer_list = [Layer(node_list) for node_list in layer_list]
        return Data(root, layer_list)
