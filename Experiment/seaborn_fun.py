import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

flights = sns.load_dataset("flights")
flights.head()

type(flights)

A = np.random.rand(1000)
B = np.random.rand(1000)
C = np.random.rand(1000)


my_array = np.array([A, B, C])
my_array = my_array.transpose()

df = pd.DataFrame(my_array, columns=['Column_A', 'Column_B', 'Column_C'])

sns.set_theme(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})
g = np.tile(list("ABC"), 50)

pal = sns.cubehelix_palette(3, rot=-.25, light=.7)
g = sns.FacetGrid(df, row="g", hue="g", aspect=15, height=.5, palette=pal)

# Draw the densities in a few steps
g.map(sns.kdeplot, "x",
      bw_adjust=.5, clip_on=False,
      fill=True, alpha=1, linewidth=1.5)
g.map(sns.kdeplot, "x", clip_on=False, color="w", lw=2, bw_adjust=.5)

# passing color=None to refline() uses the hue mapping
g.refline(y=0, linewidth=2, linestyle="-", color=None, clip_on=False)


# Define and use a simple function to label the plot in axes coordinates
def label(x, color, label):
    ax = plt.gca()
    ax.text(0, .2, label, fontweight="bold", color=color,
            ha="left", va="center", transform=ax.transAxes)


g.map(label, "x")

# Set the subplots to overlap
g.figure.subplots_adjust(hspace=-.25)

# Remove axes details that don't play well with overlap
g.set_titles("")
g.set(yticks=[], ylabel="")
g.despine(bottom=True, left=True)