import numpy as np
import matplotlib.pyplot as plt

class Path(np.ndarray):
    """
    A path is at its core a numpy array.
    """
    def __new__(cls, arg):
        obj = np.asarray(arg).view(cls)
        return obj

    def __array_finalize__(self, obj):
        pass

class Paths(list):
    """
    Paths is just a list of paths
    """
    pass

class PPath(Path):
    """
    PPath is a path but plottable.
    """

    def __new__(cls, arg, color = "blue"):
        obj = np.asarray(arg).view(cls)
        obj.color = color
        return obj

    def __array_finalize__(self, obj):
        self.color = getattr(obj, "color", None)

    def plotter(self, ax):
        x = np.array([state.get_time() for state in self])
        y = np.array([state.get_coord() for state in self])
        ax.plot(x, y)

    def plot(self):
        # Perhaps implement some iterator interface? depends on plt I guess
        fig, ax = plt.subplots()
        self.plotter(ax)


class PPaths(Paths):
    def plot(self):
        fig, ax = plt.subplots()
        for ppath in self:
            PPath(ppath).plotter(ax)












