import warnings
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import seaborn as sns
from pandas.api.types import is_numeric_dtype


def import_style(filepath: str) -> None:
    """
    This function imports a style file for matplotlib plots.

    Args:
      filepath (str):   A string representing the file path of the style sheet to be imported. The style
                        sheet should be in the correct format for matplotlib to use.
    """
    plt.style.use(filepath)


def create_horizontal_barplot(
    data, x_var, y_var, x_label="", title="", ax=None
) -> plt.Axes:
    """
    This function creates a horizontal bar plot using the input data and variables, with options for
    customizing the x-axis label and plot title.

    Args:
      data:     The dataset containing the variables to be plotted.
      x_var:    The variable to be plotted on the x-axis of the horizontal barplot.
      y_var:    The variable used for the y-axis of the horizontal barplot.
      x_label:  The label for the x-axis of the horizontal barplot.
      title:    The title of the horizontal barplot.
      ax:       The ax parameter is an optional parameter that allows the user to specify a specific subplot
                to plot the horizontal barplot on. If ax is not specified, the function will create a new subplot.

    Returns:
      a matplotlib axis object.
    """
    with plt.rc_context(
        {"axes.labelcolor": "black", "ytick.labelleft": True, "xtick.labelbottom": True}
    ):
        if ax is None:
            fig = plt.figure(figsize=(10, 10))
            ax = fig.add_subplot(111)
        y_pos = np.arange(len(data[y_var]))
        _ = ax.barh(y_pos, data[x_var], align="center")
        ax.set_yticks(y_pos)
        ax.set_yticklabels(data[y_var])
        ax.invert_yaxis()
        ax.set_xlabel(x_label)
        ax.set_title(title)
        return ax


def create_scatterplot(data, x_var, y_var, title="", ax=None) -> plt.Axes:
    """
    This function creates a scatterplot with specified data, x and y variables, and title.

    Args:
      data:     The dataset containing the variables to be plotted.
      x_var:    The variable to be plotted on the x-axis of the scatterplot.
      y_var:    The variable to be plotted on the y-axis of the scatterplot.
      title:    The title of the scatterplot (optional)
      ax:       The ax parameter is an optional parameter that allows the user to specify a specific subplot
                to plot the scatterplot on. If ax is not specified, a new subplot will be created.

    Returns:
      a matplotlib Axes object.
    """
    with plt.rc_context(
        {"axes.labelcolor": "black", "ytick.labelleft": True, "xtick.labelbottom": True}
    ):
        if ax is None:
            fig = plt.figure(figsize=(10, 10))
            ax = fig.add_subplot(111)
        ax.scatter(data[x_var], data[y_var])
        ax.set_xlabel(x_var)
        ax.set_ylabel(y_var)
        ax.set_title(title)
        return ax


def create_heatmap(
    data,
    complete=True,
    figsize=(10, 10),
    figtitle="",
    ax=None,
) -> plt.Axes:
    """
    This function creates a heatmap with customizable options and the ability to save the figure.

    Args:
      data:         The data to be plotted in the heatmap. It should be a 2D array or a pandas DataFrame.
      complete:     A boolean parameter that determines whether to show the complete heatmap or only the
                    bottom half of it. If set to True, the complete heatmap will be shown. If set to False, only the
                    bottom half of the heatmap will be shown. Defaults to True
      figsize:      The size of the figure in inches (width, height).
      figtitle:     The title of the heatmap figure.
      ax:           The matplotlib Axes object to plot the heatmap on. If it is not provided, a new figure and
                    Axes object will be created.

    Returns:
      the axis object (ax) of the heatmap plot.
    """
    with plt.rc_context(
        {"axes.labelcolor": "black", "ytick.labelleft": True, "xtick.labelbottom": True}
    ):
        if complete:
            mask = None
        else:
            # only show the bottom half of the heatmap
            mask = np.triu(np.ones_like(data, dtype=bool))
        if ax is None:
            fig = plt.figure(figsize=figsize)
            ax = fig.add_subplot(111)
        sns.heatmap(
            data,
            ax=ax,
            mask=mask,
            vmax=1,
            vmin=-1,
            annot=True,
            xticklabels=1,
            yticklabels=1,
            center=0,
            square=True,
            linewidths=0.5,
            cbar_kws={"shrink": 0.5},
            cmap="coolwarm",
        )
        ax.set_title(figtitle, fontsize=12, y=1.0)
        return ax


def make_barplot_labels(ax, rects) -> None:
    """
    The function adds labels to a barplot with the height of each bar.

    Args:
      ax:       The ax parameter is a matplotlib Axes object, which represents the plot on which the barplot
                is being drawn. It is used to add text labels to the bars in the plot.
      rects:    A list of Rectangle objects representing the bars in a bar plot.
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(
            rect.get_x() + rect.get_width() / 2.0,
            1.05 * height,
            "%d" % int(height),
            ha="center",
            va="bottom",
            color="blue",
            backgroundcolor="lightgrey",
        )


def make_boxplot_labels(ax, boxplot) -> None:
    """
    This function creates labels for a boxplot with information on the median, percentiles, caps, and
    fliers.

    Args:
      ax:       The matplotlib Axes object on which the boxplot is plotted.
      boxplot:  A dictionary containing the components of a boxplot (e.g. boxes, whiskers, medians, caps,
                fliers) as Line2D instances.
    """
    # Grab the relevant Line2D instances from the boxplot dictionary
    iqr = boxplot["boxes"][0]
    caps = boxplot["caps"]
    med = boxplot["medians"][0]
    fly = boxplot["fliers"][0]
    # The x position of the median line
    xpos = med.get_xdata()
    # Lets make the text have a horizontal offset which is some
    # fraction of the width of the box
    xoff = 0.10 * (xpos[1] - xpos[0])
    # The x position of the labels
    xlabel = xpos[1] + xoff
    # The median is the y-position of the median line
    median = med.get_ydata()[1]
    # The 25th and 75th percentiles are found from the
    # top and bottom (max and min) of the box
    pc25 = iqr.get_ydata().min()
    pc75 = iqr.get_ydata().max()
    # The caps give the vertical position of the ends of the whiskers
    capbottom = caps[0].get_ydata()[0]
    captop = caps[1].get_ydata()[0]
    # Make some labels on the figure using the values derived above
    ax.text(xlabel, median, "median: {:6.3g}".format(median), va="center")
    ax.text(xlabel, pc25, "25th percentile: {:6.3g}".format(pc25), va="center")
    ax.text(xlabel, pc75, "75th percentile: {:6.3g}".format(pc75), va="center")
    ax.text(xlabel, capbottom, "bottom cap: {:6.3g}".format(capbottom), va="center")
    ax.text(xlabel, captop, "top cap: {:6.3g}".format(captop), va="center")
    # Many fliers, so we loop over them and create a label for each one
    for flier in fly.get_ydata():
        ax.text(1 + xoff, flier, "{:6.3g}".format(flier), va="center")


def create_boxplot(
    data, x_var, y_var=None, color_by=None, ax=None, title=""
) -> plt.Axes:
    """
    This function creates a boxplot using seaborn library with optional parameters for color and title.

    Args:
      data:     The dataset to be used for creating the boxplot.
      x_var:    The variable to be plotted on the x-axis of the boxplot.
      y_var:    The variable to be plotted on the y-axis of the boxplot. It is optional and can be left as
                None if only one variable is being plotted.
      color_by: The parameter "color_by" is an optional parameter that allows the user to specify a
                categorical variable to color the boxplots by. If this parameter is not specified, the boxplots will
                not be colored by any variable.
      ax:       The ax parameter is an optional parameter that allows the user to specify the axes on which
                the boxplot will be plotted. If ax is not specified, a new figure and axes will be created.
      title:    The title of the boxplot.

    Returns:
      the axis object (ax) after creating a boxplot using the input data and parameters.
    """
    with plt.rc_context(
        {"axes.labelcolor": "black", "ytick.labelleft": True, "xtick.labelbottom": True}
    ):
        if ax is None:
            fig = plt.figure(figsize=(10, 10))
            ax = fig.add_subplot(111)
        sns.boxplot(x=x_var, y=y_var, hue=color_by, data=data, ax=ax)
        ax.set_title(title)
    return ax


def create_swarmplot(data, x_var, y_var=None, color_by=None, ax=None) -> plt.Axes:
    """
    This function creates a swarmplot using the Seaborn library in Python, with options to customize the
    plot's variables and appearance.

    Args:
      data:     The dataset that contains the variables to be plotted.
      x_var:    The variable to be plotted on the x-axis.
      y_var:    The variable to be plotted on the y-axis. It is optional and can be set to None if only the
                x-axis variable is to be plotted.
      color_by: The variable used to color the points in the swarmplot.
      ax:       The ax parameter is an optional parameter that specifies the matplotlib Axes object on which
                the swarmplot will be drawn. If it is not provided, a new figure and Axes object will be created.

    Returns:
      a matplotlib Axes object.
    """
    with plt.rc_context(
        {"axes.labelcolor": "black", "ytick.labelleft": True, "xtick.labelbottom": True}
    ):
        if ax is None:
            fig = plt.figure(figsize=(10, 10))
            ax = fig.add_subplot(111)
        with warnings.catch_warnings(record=True):
            sns.swarmplot(
                x=x_var,
                y=y_var,
                hue=color_by,
                dodge=True,
                data=data,
                alpha=0.8,
                s=4,
                ax=ax,
            )
    return ax


def create_histogram(
    data, var, color_by=None, bins=10, max_categories=50, ax=None, title=""
) -> plt.Axes:
    """
    This function creates a histogram plot for a given variable in a dataset, with the option to color
    by another variable.

    Args:
      data:             The dataset that contains the variable(s) to be plotted.
      var:              The variable/column in the dataset that we want to create a histogram for.
      color_by:         A variable to group the data by and display different colors for each group in the
                        histogram.
      bins:             The number of bins to use for the histogram. Defaults to 10
      max_categories:   The maximum number of categories allowed in a categorical variable before it is
                        replaced with an "OTHER" category. Defaults to 50
      ax:               The matplotlib axis object to plot the histogram on.
                        If it is None, a new figure and axis will be created.
      title:            The title of the histogram plot.

    Returns:
      a matplotlib axis object.
    """
    with plt.rc_context(
        {"axes.labelcolor": "black", "ytick.labelleft": True, "xtick.labelbottom": True}
    ):
        if ax is None:
            fig = plt.figure(figsize=(10, 10))
            ax = fig.add_subplot(111)

        if is_numeric_dtype(data[var]):
            if (color_by is None) | (color_by == var):
                plotdata = data[var]
                stacked = False
            else:
                plotdata = [
                    data[data[color_by] == x][var] for x in data[color_by].unique()
                ]
                stacked = True
            ax.hist(plotdata, bins=bins, stacked=stacked)
        else:
            nr_cats = data[var].nunique()
            if nr_cats > max_categories:
                pass
                # create an option here later on, by replacing the longtail into OTHER
            if (color_by is None) | (color_by == var):
                plotdata = (
                    data[var].value_counts(dropna=False).sort_index(ascending=True)
                )
                ax.bar(
                    x=plotdata.index.astype("str"),
                    height=plotdata,
                )
                highest_value = max(plotdata)
            else:
                plotdata = (
                    data.groupby([color_by, var])
                    .size()
                    .unstack(fill_value=0)
                    .transpose()
                )
                for ind, col in enumerate(plotdata.columns):
                    if ind == 0:
                        ax.bar(
                            x=plotdata[col].index.astype("str"), height=plotdata[col]
                        )
                        barheight = plotdata[col]
                    else:
                        ax.bar(
                            x=plotdata[col].index.astype("str"),
                            height=plotdata[col],
                            bottom=barheight,
                        )
                    barheight.add(plotdata[col], fill_value=0)
                highest_value = plotdata.sum(axis=1).max()
            ax.set_ylim([None, highest_value * 1.25])
            ax.tick_params(axis="x", labelrotation=45)
        ax.set_title(title)
        return ax


def create_confusion_matrix_heatmap(conf_matrix, model_accuracy=None, figsize=(9, 9), ax=None) -> plt.Axes:
    """
    This function creates a heatmap of a confusion matrix with optional model accuracy score.

    Args:
      conf_matrix:      The confusion matrix to be visualized as a heatmap.
      model_accuracy:   The accuracy score of a machine learning model, expressed as a percentage.
                        If not None, this value will be shown in the title of the heatmap
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(
        conf_matrix,
        annot=True,
        fmt=".0f",
        linewidths=0.5,
        square=True,
        cmap="Blues_r",
        ax=ax
    )
    plt.ylabel("Actual label")
    plt.xlabel("Predicted label")
    if model_accuracy is not None:
        all_sample_title = "Accuracy Score: {0} %".format(
            round(model_accuracy * 100, 2)
        )
        plt.title(all_sample_title, size=15)
    return ax


def create_tableplot(data, colLabels=None, figsize=(9, 9), ax=None) -> plt.Axes:
    """
    The function creates a table plot with column labels and returns the plot object.

    Args:
      ax:           The matplotlib axis object on which the tableplot will be created.
      data:         a pandas DataFrame containing the data to be displayed in the tableplot
      colLabels:    A list of column labels for the tableplot. If not provided, the column labels will be
                    taken from the column names of the input data.

    Returns:
      a tableplot object.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    if colLabels is None:
        colLabels = data.columns
    tableplot = ax.table(cellText=data.values, colLabels=colLabels, loc="center")
    tableplot.scale(1, 2)
    ax.axis("off")
    return ax


def create_single_tableplot(data, colLabels=None):
    """
    The function creates a table plot with given data and column labels.

    Args:
      data:         a pandas DataFrame containing the data to be plotted in a table format
      colLabels:    A list of column labels for the table. If not provided, the column labels will be the
                    column names of the input data.
    """
    if colLabels is None:
        colLabels = data.columns
    if len(data) + 1 > len(colLabels):
        nrows, ncols = len(data) + 1, len(colLabels)
    else:
        ncols, nrows = len(data) + 1, len(colLabels)
    fig = plt.figure(figsize=(ncols, nrows))
    ax = fig.add_subplot(111)
    ax.axis("off")
    tableplot = ax.table(cellText=data.values, colLabels=colLabels, loc="center")
    tableplot.set_fontsize(14)
    tableplot.scale(2, 2)
    return fig


def create_pairplot(
    data, figtitle=""
):
    """
    The function creates a pairplot using seaborn library

    Args:
      data:     The data to be plotted in the pairplot.
      figsize:  The size of the figure in inches (width, height).
      figtitle: The title of the figure
    """
    with plt.rc_context(
        {
            "axes.labelcolor": "black",
            "ytick.labelleft": True,
            "xtick.labelbottom": True,
            "axes.linewidth": 1.0,
        }
    ):
        fig_pairplot = sns.pairplot(
            data,
            corner=True,
            plot_kws=dict(color="#003D7C"),
            diag_kws={"color": "#003D7C"},
        )
        fig = fig_pairplot.fig
        fig.suptitle(figtitle, fontsize=12, y=1.0)
        return fig

