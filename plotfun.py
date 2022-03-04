import matplotlib.pyplot as plt
import numpy as np

def addshit(ax):
    x = np.linspace(0,4,100)
    ax.plot(x, np.sin(2 * x))
    return ax

fig, ax = plt.subplots()

addshit(ax)

um = GeometricBrownianMotion()
mypath = um.generatepath()


class PPath(Path):
    def __new__(cls, arg, color="blue"):
        obj = np.asarray(arg).view(cls)
        obj.color = color
        return obj

    def __array_finalize__(self, obj):
        self.color = getattr(obj, "color", None)

    def plot(self):
        # Perhaps implement some iterator interface? depends on plt I guess
        x = np.array([state.get_time() for state in self])
        y = np.array([state.get_coord() for state in self])
        fig, ax = plt.subplots()
        ax.plot(x, y, linewidth=2.0)
        plt.show()
