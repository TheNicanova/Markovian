import numpy as np
import matplotlib.pyplot as plt

class Path(list):
    '''
    Path is a list of states.
    '''

    def __init__(self, args):
        super().__init__(args)
        self.length = len(self)

    def get_time(self):
        """
        Returns a numpy array created from the list of timestamps
        """
        return np.array([state.get_time() for state in self])

    def get_coord(self):
        """
        Returns a numpy array created from the list of coordinates
        """
        return np.array([state.get_coord() for state in self])

    def get_time_coord(self):
        """
        Returns an ordered pair
        """
        return (self.get_time(), self.get_coord())

    def plotter(self, ax):
        """ This is what you can override for personalization """
        x = self.get_time()
        y = self.get_coord()
        ax.plot(x, y)

    def plot(self, offer):
        fig, ax = plt.subplots()
        self.plotter(ax, offer)

    def plotter3D(self, ax, offer=None):

        x = self.get_time()
        y = self.get_coord()

        if offer is None:
            z = 0
        else:
            z = offer.payoff(x, y)

        ax.plot(x, y, z)

    def plot3D(self, offer):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        self.plotter3D(ax, offer)


    def get_length(self):
        return self.length


class Paths(list):
    """
    Paths is simply a list of paths
    """
    def __init__(self, args):
        super().__init__(args)
        self.memoed_schedules = None
        self.memoed_coords = None
        self.length = self[0].get_length()

    def get_coord(self): # returns a numpy matrix A where A_ij is the ith coord for the jth path
        if self.memoed_coords is None: # Compute and store an efficient representation
            matrix = np.array([path.get_coord() for path in self]).transpose() # This is the efficient representation
            self.memoed_coords = matrix.copy()  # So that we don't get a view
        return self.memoed_coords # Retrieve the result

    def get_time(self): # returns a numpy matrix A where A_ij is the ith timestamp for the jth path
        if self.memoed_schedules is None:
            matrix = np.array([path.get_time() for path in self]).transpose()
            self.memoed_schedules = matrix.copy()
        return self.memoed_schedules # So that we don't get a view

    def get_time_coord(self):
        return (self.get_time(), self.get_coord())

    def plot(self):
        fig, ax = plt.subplots()
        for path in self:
            path.plotter(ax)

    def plotter3D(self, ax, offer):
        for path in self:
            path.plotter3D(ax, offer)


    def plot3D(self, offer = None):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        self.plotter3D(ax, offer)

    def get_length(self):
        return self.length
