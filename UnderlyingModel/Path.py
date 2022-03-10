import numpy as np
import matplotlib.pyplot as plt

class Path(list):
    '''
    Path is a list of states.
    '''

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

    def plot(self):
        fig, ax = plt.subplots()
        self.plotter(ax)

class Paths(list):
    """
    Paths is simply a list of paths
    """
    def get_coord(self): # returns a numpy matrix A where A_ij is the ith coord for the jth path
        matrix = np.array([path.get_coord() for path in self]).transpose()
        return matrix.copy() # So that we don't get a view

    def get_time(self): # returns a numpy matrix A where A_ij is the ith timestamp for the jth path
        matrix = np.array([path.get_time() for path in self]).transpose()
        return matrix.copy() # So that we don't get a view

    def get_time_coord(self):
        return (self.get_time(), self.get_coord())

    def plot(self):
        fig, ax = plt.subplots()
        for path in self:
            path.plotter(ax)
