from UnderlyingModel.State import *
from UnderlyingModel.Path import *
from UnderlyingModel.Schedule import *
from config import *
import numpy as np


class UnderlyingGenerator:
    """
  The process governing the evolution of a state through time.

  forward_to(state,forward_time) : expects a state object and a future time; returns a state object sampled at the future time.

  """

    def __init__(self):
        pass

    def forward_to(self, state, forward_time):
        pass

    def genesis(self):
        pass

    def generate_path(self, initial_state=None, schedule=None):

        # Setting defaults
        if initial_state is None: initial_state = self.genesis()
        if schedule is None: schedule = np.linspace(default["initial_time"], default["terminal_time"], default["num_of_timestamps"])

        # Making sure the beginning of the schedule matches with the initial state
        assert initial_state.get_time() == schedule[0]

        acc = [initial_state]
        for i in range(1, len(schedule)):
            new_state = self.forward_to(acc[i - 1], schedule[i])
            acc.append(new_state)
        return Path(acc)

    def generate_paths(self, initial_state=None, schedules=None, n= default["num_of_paths"]):

        # Setting defaults
        if schedules is None:
          return Paths([self.generate_path(initial_state) for _ in range(n)])
        else:
          return Paths([self.generate_path(initial_state, schedule) for schedule in schedules])


class GeometricBrownianMotion(UnderlyingGenerator):
    """
  A concrete class of Underlying model.
  """

    def __init__(self, rate=0.06, sigma=0.2, dividend=0):
        # To be modularized ...
        self.name = "Geometric Brownian Motion"
        self.rate = rate
        self.sigma = sigma
        self.dividend = dividend
        self.rng = np.random.default_rng()

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
        return State(default["initial_time"], 1.0)
