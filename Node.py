import matplotlib.pyplot as plt


class Node:

    def __init__(self, state, children=None):

        self.children = []
        self.state = state

    def get_children(self):
        return self.children

    def set_children(self, children):
        self.children = children

    def get_state(self):
        return self.state

    def get_coord(self):
        return self.get_state().get_coord()

    def get_time(self):
        return self.get_state().get_time()

    def bfs(self):

        visited = set()

        layer_list = [[self]]
        queue = {self}
        next_generation = []

        while queue:
            for node in queue:
                next_generation += node.get_children()

            unique_next_generation = set(next_generation) - visited
            visited = visited.union(unique_next_generation)
            if unique_next_generation:
                layer_list.append(list(unique_next_generation))
                queue = unique_next_generation.copy()
            else:
                queue = {}

        return layer_list

    def plot_child(self, ax=None):
        if ax is None:
            fig, ax = plt.subplots()

        for child in self.get_children():
            parent_state = self.get_state()
            child_state = child.get_state()
            ax.plot([parent_state.get_time(), child_state.get_time()],
                    [parent_state.get_coord(), child_state.get_coord()])
        return ax

    def plot(self):
        self.plot_descendant()

    def plot_descendant(self):
        fig, ax = plt.subplots()
        layer_list = self.bfs()
        for list in layer_list:
            for node in list:
                node.plot_child(ax)

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
