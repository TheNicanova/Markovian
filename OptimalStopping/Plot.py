import matplotlib.pyplot as plt
import seaborn as sns
from pandas.core.frame import DataFrame


class RidgePlot(DataFrame):
    @classmethod
    def plot(cls, dataframe):
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
