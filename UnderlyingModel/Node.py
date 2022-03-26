import matplotlib.pyplot as plt


class Node:

    def __init__(self, state, children=None):
        self.children = children
        self.state = state

    def get_children(self):
        return self.children

    def set_children(self, children):
        self.children = children

    def get_state(self):
        return self.state

    def plot_child(self, ax):
        if self.get_children() is None:
            return ax

        for child in self.get_children():
            ax.plot([self.get_state().get_time(), child.get_state().get_time()], [self.get_state().get_coord(), child.get_state().get_coord()])
        return ax

    def plot(self):
        fig, ax = plt.subplots()
        ax.plot(self.get_state().get_time(), self.get_state().get_coord())

    def plot_descendant(self):
        fig, ax = plt.subplots()
        self.recursive_plot(ax)

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

