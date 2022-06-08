import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import OptimalStopping.config as config
from pandas.core.frame import DataFrame
import math


def plot_node_descendant(self):
    fig, ax = plt.subplots()
    fig.supxlabel('Time')
    fig.supylabel('Coordinates')
    layer_list = self.bfs()

    for layer in layer_list:
        for node in layer:
            plot_node_child(node, ax)


def plot_node_child(node, ax=None):
    if ax is None:
        fig, ax = plt.subplots()

    for child in node.get_children():
        parent_state = node.get_state()
        child_state = child.get_state()
        ax.plot([parent_state.get_time(), child_state.get_time()],
                [parent_state.get_coord(), child_state.get_coord()])
    return ax


def plot_node_data(node, ax):
    coord = node.get_coord()

    # Mark the node as a vertical line at coord
    ax.axvline(coord, linewidth=1, alpha=0.5, color='grey', linestyle='-')

    # Plotting the policy
    if node.get_policy() is True:
        ax.scatter(coord, -0.1, s=15, label="stopped", marker='H', c='red')

    # Plotting the continuation
    if node.get_continuation() is not None:
        ax.scatter(coord, node.get_continuation(), label="continuation", c="green", marker=r'$\clubsuit$')

    # Plotting the control value
    if node.get_control() is not None:
        ax.scatter(coord, node.get_control(), label="control", c="purple", marker="*")


def plot_option(time=None, option=None, ax=None, x_list=None):
    x = x_list
    y = [option.payoff(time, x) for x in x_list]
    ax.plot(x, y, label=option.get_name())
    return ax


def plot_regression(regression_function=None, ax=None, x_list=None):
    x = x_list
    y = [regression_function(x) for x in x_list]
    ax.plot(x, y, label="regression")


def plot_layer(layer, ax=None, x_list=None):
    if ax is None:
        fig, ax = plt.subplots()

    if x_list is None:
        x_min = np.min(layer.get_coord())
        x_max = np.max(layer.get_coord())
        x_res = config.default["x_res"]
        x_list = np.linspace(x_min, x_max, x_res)

    # Plotting labels and title
    ax.set_xlabel("Coord")
    ax.set_ylabel("Reward")
    ax.set_title("At time " + f'{layer.get_layer_time():.2f}')

    # Plotting layer-wise information

    if layer.get_regression_result() is not None:
        regression_function = layer.get_regression_result()
        plot_regression(x_list=x_list, regression_function=regression_function, ax=ax)

    # Plotting node-wise information

    for node in layer.get_node():
        plot_node_data(node, ax)


def plot_model(model):
    # Getting a figure and a list of ax

    axs_width = config.default["axs_width"]
    axs_height = math.ceil(len(model.data.layer_list) // axs_width)
    fig, axs = plt.subplots(axs_width, axs_height)
    fig.supxlabel(model.get_name())
    ax_list = list(axs.ravel())
    ax_list.reverse()

    for layer, ax in zip(model.data.layer_list, ax_list):
        ax.set_ylim(bottom=-0.2)
        x_min = np.min(layer.get_coord())
        x_max = np.max(layer.get_coord())
        x_res = config.default["x_res"]
        x_list = np.linspace(x_min, x_max, x_res)

        # Plotting option
        plot_option(time=layer.get_layer_time(), option=model.option, ax=ax, x_list=x_list)

        # Plotting layer data
        plot_layer(layer, ax, x_list)

    # Plotting the legend on the first ax as it has minimal information on it
    ax_list[-1].legend()


def plot_benchmark_result(dataframe):
    pal = sns.cubehelix_palette()

    g = sns.FacetGrid(dataframe, row="Model Name", col="Number of Paths", hue="Model Name", margin_titles=True,
                      palette=pal)

    # Draw the densities in a few steps
    g.map(sns.kdeplot, "Price", bw_adjust=.5, clip_on=False, fill=True, alpha=1, linewidth=1.5)
    g.map(sns.kdeplot, "Price", clip_on=False, color="w", lw=2, bw_adjust=.5)

    # passing color=None to refline() uses the hue mapping
    g.refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False)

    # Define and use a simple function to label the plot in axes coordinates
    def my_label(x, color, label):
        ax = plt.gca()
        ax.text(0, .4, label, fontweight="bold", color=color,
                ha="left", va="center", transform=ax.transAxes)

    g.map(my_label, "Price")

    # Set the subplots to overlap
    g.figure.subplots_adjust(hspace=-.1)

    # Remove axes details that don't play well with overlap
    g.set_titles("")
    g.set(yticks=[], ylabel="")
    g.despine(bottom=True, left=True)
    plt.tight_layout()
