import numpy as np
import matplotlib.pyplot as plt
from config import *


class Token:

    def __init__(self, paths, offer):
        self.paths = paths  # Storing the paths given
        self.offer = offer  # Storing the pay_off model used

        self.layer_payload = [None] * self.paths.get_length()

        self.schedules = paths.get_time()
        self.coords = paths.get_coord()
        self.offers = offer.payoff(self.schedules, self.coords)
        self.length = paths.get_length()

        self.min_coord = np.min(self.coords)
        self.max_coord = np.max(self.coords)

    def update_cursor(self):
        self.cursor = self.cursor - 1

    def get_precedent_cursor(self):
        return self.cursor + 1

    def set_cursor(self, i):
        self.cursor = i

    def plotter3D(self, ax):
        # Paths
        return self.paths.plotter3D(ax, self.offer)

        # Offer
        #self.schedules, np.meshgrid(self.schedules[:, 0], np.linspace(self.min_coord, self.max_coord, 101))
        #ax.plot_wireframe(self.schedules, np.meshgrid(self.schedules[:, 0], np.linspace(self.min_coord, self.max_coord, 101)), self.offers)

    def continuation_plotter3D(self, ax):

        # Plotting the continuation
        #assuming at least one path and assuming all schedules are the same
        x = self.schedules[1:, 0] # The 1:, = Not plotting the token at initial time
        y = np.linspace(self.min_coord,self.max_coord, default["time_resolution_continuation"])
        X, Y = np.meshgrid(x, y)
        Z = np.array([self.layer_payload[i](y) for i in range(1, self.length)]).transpose()
        ax.plot_wireframe(X, Y, Z, alpha=0.5, color='green')


    def plot3D(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.set_xlabel('time')
        ax.set_ylabel('coord')
        ax.set_zlim3d(0, np.max(self.offers))
        self.plotter3D(ax)


class LangStaffToken(Token):
    def __init__(self, paths, offer):
        super().__init__(paths, offer)

        self.policy = np.full(self.coords.shape, True)
        self.continuation = np.zeros(self.coords.shape)
        self.value = np.zeros(self.coords.shape)
        self.cursor = self.length - 1

    def policy_plotter3D(self, ax):# Can't be working..
        for i in range(self.length - 1, 0, -1):
            x = self.schedules[1:, 0]  # The 1:, = Not plotting the token at initial time
            ax.scatter(self.schedules, self.coords, self.policy,  label="stopped", marker='H', c='red')

        # The cursor keeps track of where the Data is during it's initialization
    def plotter3D(self, ax):
        super().plotter3D(ax) # Plotting the paths (at least)
        self.continuation_plotter3D(ax)


    def plotter(self, ax, i):
        # Preamble

        size_reference = plt.rcParams['lines.markersize'] ** 2. #some more default..
        ax.set_xlabel("coord")
        ax.set_ylabel("value")
        ax.set_title(f"Layer {i}. Time  {self.schedules[i][0]}")

        # Scatter plots

        # Plotting Stopped
        stopped_coord = self.coords[i][self.policy[i]]
        offer_at_stopped = self.offers[i][self.policy[i]]
        ax.scatter(stopped_coord, offer_at_stopped, s=size_reference * 2.0, label="stopped", marker='H', c='red')

        # Plotting Offers
        ax.scatter(self.coords[i], self.offers[i], s=size_reference * 2.0, label="offer", marker='*', c='grey')

        # Plotting the continuation value on the given path.
        ax.scatter(self.coords[i], self.continuation[i], label="continuation", c="green", marker=r'$\clubsuit$')


        # Continuous plots

        x = np.linspace(np.min(self.coords[i]), np.max(self.coords[i]), default["space_resolution_continuation"])
        # Plotting the regression

        ax.plot(x, self.layer_payload[i](x), linestyle='--', label="regression", c='green')



        ax.grid(visible = True, color='gray')
        ax.legend()

    def plot(self, i=None):

        if i is None:
            i = 0
            fig, axs = plt.subplots(1, self.length- 2) # not plotting the first and last time
            for i in range(0,self.length- 2):
                self.plotter(axs[i], i+1)
                i += 1

# Todo: Have path/data do the init for continuation, value, by means of "copy"
    class LatticeToken(Token):
        def __init__(self, paths, offer):
            super().__init__(paths, offer)
            self.layer_payload = [None] * self.paths.get_length()
            self.policy = [None] * self.paths.get_length()
            self.continuation = [None] * self.paths.get_length()
            self.value = [None] * self.paths.get_length()
            self.cursor = self.length - 1


