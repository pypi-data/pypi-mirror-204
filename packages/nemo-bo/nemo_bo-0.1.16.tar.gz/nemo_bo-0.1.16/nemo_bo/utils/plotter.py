import os
from typing import Any, List, Optional, Tuple, Union

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.animation import FuncAnimation
from matplotlib.axes import Axes


def scatter_plot(
    ax: Axes,
    data: Union[List[np.ndarray], np.ndarray],
    legend: Union[str, List[str]],
    error: Optional[Union[List[np.ndarray], np.ndarray]] = None,
) -> None:
    """

    Function to create the scatter plot Axes object

    Parameters
    ----------
    ax: Axes
        Matplotlib Axes object
    data: List[np.ndarray] | np.ndarray
        Can be a 2D (x, y) or 3D (x, y, z) array or a list of 2D or 3D arrays for drawing multiple plots on to the same
        set of axes
    legend: str | List[str]
        A string or a list of strings for labelling the plots
    error: List[np.ndarray] | np.ndarray, Default = None
        Can be an array or a list of arrays that contains the respective values to be used for error bars

    """
    # If the data provided is an array (i.e. not a list of arrays)
    # Starts the colour cycle for the plots from a different position (brown) to the default (blue)
    colorcycle = [
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf",
    ]
    if np.array(data)[0][0].ndim == 0:
        data_plot = np.array(data)
        # If the array provided is 2D
        if data_plot.shape[1] == 2:
            # If legend information was provided
            if error is None:
                if legend is not None:
                    ax.scatter(
                        data_plot[:, 0],
                        data_plot[:, 1],
                        label=legend,
                        marker="o",
                        s=40,
                        facecolors="none",
                        edgecolors=colorcycle[0],
                    )
                else:
                    ax.scatter(
                        data_plot[:, 0],
                        data_plot[:, 1],
                        label="Scatter plot",
                        marker="o",
                        s=40,
                        facecolors="none",
                        edgecolors=colorcycle[0],
                    )
            else:
                if legend is not None:
                    ax.errorbar(
                        data_plot[:, 0],
                        data_plot[:, 1],
                        yerr=error.flatten(),
                        fmt="o",
                        label=legend,
                        zorder=2,
                        fillstyle="none",
                    )
                else:
                    ax.errorbar(
                        data_plot[:, 0],
                        data_plot[:, 1],
                        yerr=error.flatten(),
                        fmt="o",
                        label="Scatter plot",
                        zorder=2,
                        fillstyle="none",
                    )
        # Else if the array provided is 3D
        elif data_plot.shape[1] == 3:
            # If legend information was provided
            if legend is not None:
                ax.scatter(
                    data_plot[:, 0],
                    data_plot[:, 1],
                    data_plot[:, 2],
                    label=legend,
                    marker="o",
                    s=40,
                )
            else:
                ax.scatter(
                    data_plot[:, 0],
                    data_plot[:, 1],
                    data_plot[:, 2],
                    label="Scatter plot",
                    marker="o",
                    s=40,
                )
    # Else the data provided is a list of arrays
    else:
        # Iterate through the list of arrays and plot each one
        for plotnum in range(len(data)):
            data_plot = np.array(data[plotnum])
            # If the array provided is 2D
            if data_plot.shape[1] == 2:
                # If legend information was provided
                if error is None:
                    if legend is not None:
                        ax.scatter(
                            data_plot[:, 0],
                            data_plot[:, 1],
                            label=legend[plotnum],
                            marker="o",
                            s=40,
                            facecolors="none",
                            edgecolors=colorcycle[plotnum],
                        )
                    else:
                        ax.scatter(
                            data_plot[:, 0],
                            data_plot[:, 1],
                            label=error_plot.flatten(),
                            marker="o",
                            s=40,
                            facecolors="none",
                            edgecolors=colorcycle[plotnum],
                        )
                else:
                    error_plot = np.array(error[plotnum])
                    if legend is not None:
                        ax.errorbar(
                            data_plot[:, 0],
                            data_plot[:, 1],
                            yerr=error_plot.flatten(),
                            fmt="o",
                            label=legend[plotnum],
                            zorder=2,
                            fillstyle="none",
                        )
                    else:
                        ax.errorbar(
                            data_plot[:, 0],
                            data_plot[:, 1],
                            yerr=error_plot.flatten(),
                            fmt="o",
                            label=f"Scatter plot {plotnum + 1}",
                            zorder=2,
                            fillstyle="none",
                        )
            # Else if the array provided is 3D
            elif data_plot.shape[1] == 3:
                # If legend information was provided
                if legend is not None:
                    ax.scatter(
                        data_plot[:, 0],
                        data_plot[:, 1],
                        data_plot[:, 2],
                        label=legend[plotnum],
                        marker="o",
                        s=40,
                    )
                else:
                    ax.scatter(
                        data_plot[:, 0],
                        data_plot[:, 1],
                        data_plot[:, 2],
                        label=f"Scatter plot {plotnum + 1}",
                        marker="o",
                        s=40,
                    )


def line_plot(data: Union[List[np.ndarray], np.ndarray], legend: Union[str, List[str]]) -> None:
    """

    Function to create the line plot object

    Parameters
    ----------
    data: List[np.ndarray] | np.ndarray
        Can be a 2D (x, y) or 3D (x, y, z) array or a list of 2D or 3D arrays for drawing multiple plots on to the same
        set of axes
    legend: str | List[str]
        A string or a list of strings for labelling the plots

    """
    # Starts the colour cycle for the plots from a different position (brown) to the default (blue)
    colorcycle = [
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf",
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
    ]
    # If the data provided is a array (i.e. not a list of arrays)
    if np.array(data)[0][0].ndim == 0:
        data_plot = np.array(data)
        # If the array provided is 2D
        if data_plot.shape[1] == 2:
            # If legend information was provided
            if legend is not None:
                plt.plot(data_plot[:, 0], data_plot[:, 1], label=legend, color=colorcycle[0])
            else:
                plt.plot(
                    data_plot[:, 0],
                    data_plot[:, 1],
                    label="Line plot",
                    color=colorcycle[0],
                )
        # Else if the array provided is 3D
        elif data_plot.shape[1] == 3:
            # If legend information was provided
            if legend is not None:
                plt.plot(
                    data_plot[:, 0],
                    data_plot[:, 1],
                    data_plot[:, 2],
                    label=legend,
                    color=colorcycle[0],
                )
            else:
                plt.plot(
                    data_plot[:, 0],
                    data_plot[:, 1],
                    data_plot[:, 2],
                    label="Line plot",
                    color=colorcycle[0],
                )
    # Else the data provided is a list of arrays
    else:
        # Iterate through the list of arrays and plot each one
        for plotnum in range(len(data)):
            data_plot = np.array(data[plotnum])
            # If the array provided is 2D
            if data_plot.shape[1] == 2:
                # If legend information was provided
                if legend is not None:
                    plt.plot(
                        data_plot[:, 0],
                        data_plot[:, 1],
                        label=legend[plotnum],
                        color=colorcycle[plotnum],
                    )
                else:
                    plt.plot(
                        data_plot[:, 0],
                        data_plot[:, 1],
                        label=f"Line plot {plotnum + 1}",
                        color=colorcycle[plotnum],
                    )
            # Else if the array provided is 3D
            elif data_plot.shape[1] == 3:
                # If legend information was provided
                if legend is not None:
                    plt.plot(
                        data_plot[:, 0],
                        data_plot[:, 1],
                        data_plot[:, 2],
                        label=legend[plotnum],
                        color=colorcycle[0],
                    )
                else:
                    plt.plot(
                        data_plot[:, 0],
                        data_plot[:, 1],
                        data_plot[:, 2],
                        label=f"Line plot {plotnum + 1}",
                        color=colorcycle[0],
                    )


def surface_plot(ax: Axes, data: Union[List[np.ndarray], np.ndarray], legend: Union[str, List[str]]) -> None:
    """

    Function to create the scatter plot Axes object

    Parameters
    ----------
    ax: Axes
        Matplotlib Axes object
    data: List[np.ndarray] | np.ndarray
        Can be a 3D (x, y, z) array or a list of 3D arrays for drawing multiple plots on to the same set of axes
    legend: str | List[str]
        A string or a list of strings for labelling the plots

    """
    # Starts the colour cycle for the plots from a different position (brown) to the default (blue)
    colorcycle = [
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf",
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
    ]
    # If the data provided is a array (i.e. not a list of arrays)
    if np.array(data)[0][0].ndim == 0:
        data_plot = np.array(data)
        # plot_trisurf breaks the plot when there are fewer than 3 points
        if data_plot.shape[0] >= 3:
            # If legend information was provided
            if legend is not None:
                surf = ax.plot_trisurf(
                    data_plot[:, 0],
                    data_plot[:, 1],
                    data_plot[:, 2],
                    label=legend,
                    alpha=0.3,
                    color=colorcycle[0],
                    antialiased=False,
                )
                surf._facecolors2d = surf._facecolor3d
                surf._edgecolors2d = surf._edgecolor3d
            else:
                surf = ax.plot_trisurf(
                    data_plot[:, 0],
                    data_plot[:, 1],
                    data_plot[:, 2],
                    label=f"Surface plot",
                    alpha=0.3,
                    color=colorcycle[0],
                    antialiased=False,
                )
                surf._facecolors2d = surf._facecolor3d
                surf._edgecolors2d = surf._edgecolor3d
    # Else the data provided is a list of arrays
    else:
        # Iterate through the list of arrays and plot each one
        for plotnum in range(len(data)):
            data_plot = np.array(data[plotnum])
            # plot_trisurf breaks the plot when there are fewer than 3 points
            if data_plot.shape[0] >= 3:
                # If legend information was provided
                if legend is not None:
                    surf = ax.plot_trisurf(
                        data_plot[:, 0],
                        data_plot[:, 1],
                        data_plot[:, 2],
                        label=legend[plotnum],
                        alpha=0.3,
                        color=colorcycle[plotnum],
                        antialiased=False,
                    )
                    surf._facecolors2d = surf._facecolor3d
                    surf._edgecolors2d = surf._edgecolor3d
                else:
                    surf = ax.plot_trisurf(
                        data_plot[:, 0],
                        data_plot[:, 1],
                        data_plot[:, 2],
                        label=f"Surface plot {plotnum + 1}",
                        alpha=0.3,
                        color=colorcycle[plotnum],
                        antialiased=False,
                    )
                    surf._facecolors2d = surf._facecolor3d
                    surf._edgecolors2d = surf._edgecolor3d


def plot3d_video(ax: Axes, output_file: str) -> None:
    """

    Creates a .mp4 video file of a rotating 3D Matplotlib plot using a series of images

    Parameters
    ----------
    ax: Axes
        Matplotlib Axes object
    output_file: str
        String of the output video location and file name. Do not need the video file extension in this string

    """
    angles = np.linspace(0, 360, 91)[:-1]  # Generates a list of 90 angles between 0 and 360 degrees

    # Creates a series of images at different angles and a list of image file names
    imagefiles_list = []
    print(f"Creating temporary image files")
    for i, angle in enumerate(angles):
        ax.view_init(elev=None, azim=angle)  # elevation set to None
        fname = f"tmpimg_{i}.jpeg"
        ax.figure.savefig(fname, dpi=400)  # dpi set to 400
        imagefiles_list.append(fname)

    # Uses mencoder.exe in the home directory to produce a .mp4 movie from a list of image files.
    command = (
        f'mencoder "mf://{",".join(imagefiles_list)}" -mf fps={10} -o {output_file}.mp4 -ovc lavc -lavcopts '
        f"vcodec=msmpeg4v2:vbitrate={8000}"
    )  # fps=10, bitrate=8000
    os.system(command)

    # Deleted the temporary image files created above
    for f in imagefiles_list:
        os.remove(f)


def plot(
    plot_dim: str = "2D",
    scatter_data: Optional[Union[List[Union[np.ndarray, pd.DataFrame]], np.ndarray, pd.DataFrame]] = None,
    error: Optional[Union[List[np.ndarray], np.ndarray]] = None,
    line_data: Optional[Union[List[Union[np.ndarray, pd.DataFrame]], np.ndarray, pd.DataFrame]] = None,
    surface_data: Optional[Union[List[Union[np.ndarray, pd.DataFrame]], np.ndarray, pd.DataFrame]] = None,
    animation_scatter_data: Optional[Union[np.ndarray, pd.DataFrame]] = None,
    animated_scatter_fps: int = 2,
    scatter_legend: Optional[Union[str, List[str], Tuple[str]]] = None,
    line_legend: Optional[Union[str, List[str]]] = None,
    surface_legend: Optional[Union[str, List[str]]] = None,
    xlabel: str = "x",
    ylabel: str = "y",
    zlabel: str = "z",
    plottitle: str = "Title",
    output_file: str = "Plot",
    write_mp4: bool = False,
) -> None:
    """

    Function to start the plotting of a new 2D or 3D figure (including animated 2D scatter plots)

    Parameters
    ----------
    plot_dim: str, Default = '2D'
        Refers to the number of dimensions for the desired plot
    scatter_data: List[np.ndarray | pd.DataFrame] | np.ndarray | pd.DataFrame, Default is None
        The data used for the scatter plot can be either a 2D (x, y) or 3D (x, y, z) array or a list of 2D or 3D arrays
    line_data: List[np.ndarray | pd.DataFrame] | np.ndarray | pd.DataFrame, Default = None
        The data used for the line plot can be either a 2D (x, y) or 3D (x, y, z) array or a list of 2D or 3D arrays
    surface_data: List[np.ndarray | pd.DataFrame] | np.ndarray | pd.DataFrame, Default is None
        The data used for the surface plot can be either a 3D (x, y, z) array or a list of 3D arrays
    animated_scatter_data: np.ndarray | pd.DataFrame, Default = 2
        The 2D (x, y) data to be animated one point at a time
    animated_scatter_fps: int, Default is None
        The number of frames per second to animate at for the animated scatter data
    scatter_legend: str | List[str] | Tuple[str], Default is None
        The string or list of strings used to label the new scatter plot(s)
    line_legend: str | List[str], Default is None.
        The string or list of strings used to label the new line plot(s)
    surface_legend: str | List[str] | Tuple[str], Default is None
        The string or list of strings used to label the new surface plot(s)
    xlabel: str, Default is "x"
        Label of the x-axis
    ylabel: str, Default is "y"
        Label of the y-axis
    zlabel: str, Default is "z"
        Label of the z-axis
    plottitle: str, Default is "Title"
        The title of the figure
    output_file: str, Default is "Plot"
        The output file location of the .png and/or .mp4 of the new figure. Do not need the file extension
        (.png or .mp4)
    write_mp4: bool, Default is False
        When set to True, creates a .mp4 video file of a rotating 3D Matplotlib plot using a series of in-situ
        generated images

    """
    # Creates the Figure and Axes Matplotlib objects, with settings depending on if a 2D or 3D figure is requested
    if plot_dim == "2D":
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(1, 1, 1)
    elif plot_dim == "3D":
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")

    # Creates the scatter, line, or surface plot Axes objects respectively, depending on if the data for each type of
    # plot was provided
    if scatter_data is not None:
        scatter_data = data_to_np(scatter_data)
        scatter_plot(ax, scatter_data, scatter_legend, error)
    if line_data is not None:
        line_data = data_to_np(line_data)
        line_plot(line_data, line_legend)
    if surface_data is not None:
        surface_data = data_to_np(surface_data)
        surface_plot(ax, surface_data, surface_legend)

    # Modifies the style settings for the figure, with settings depending on if a 2D or 3D figure is requested
    if plot_dim == "2D":
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.set_title(plottitle, fontsize=12)
        plt.legend(loc="best", fontsize=10)
    elif plot_dim == "3D":
        ax.set_xlabel(xlabel, fontsize=6)
        ax.set_ylabel(ylabel, fontsize=6)
        ax.set_zlabel(zlabel, fontsize=6)
        ax.tick_params(axis="both", which="major", labelsize=6)
        ax.set_title(plottitle, pad=24, fontsize=6)
        plt.legend(loc="best", fontsize=6)

    # Additional style settings for the figure
    ax.set_axisbelow(True)
    plt.grid(b=True, which="major", c="whitesmoke")

    if animation_scatter_data is not None:
        if plot_dim != "2D":
            raise TypeError("Animated scatter plots are currently only supported for 2D scatter plots (plot_dim='2D')")

        animation_scatter_data = data_to_np(animation_scatter_data)
        (graph,) = plt.plot([], [], "o", color="red", markersize=10)

        def animate(i):
            graph.set_data(animation_scatter_data[: i + 1, 0], animation_scatter_data[: i + 1, 1])
            return graph

        ani = FuncAnimation(fig, animate, frames=animation_scatter_data.shape[0], repeat=False, interval=500)
        ani.save(f"{output_file}.mp4", writer=animation.FFMpegWriter(fps=animated_scatter_fps), dpi=400)

    # Writes a .png image file of the figure
    plt.savefig(f"{output_file}.png", dpi=400)

    # Writes a .mp4 video file of a rotating 3D Matplotlib plot
    if plot_dim == "3D":
        if write_mp4 == True:
            plot3d_video(ax, output_file)


def data_to_np(data: Union[List[Union[np.ndarray, pd.DataFrame]], np.ndarray, pd.DataFrame]) -> np.ndarray:
    """

    Function used to convert pd.DataFrames, np.ndarray or a list of pd.DataFrame or np.ndarray into 2D or 3D np.ndarray
    objects

    Parameters
    ----------
    data: List[np.ndarray | pd.DataFrame] | np.ndarray | pd.DataFrame
        Any 2D or 3D array or list of 2D or 3D array

    """
    inputdata = data
    if isinstance(data, list):
        if isinstance(data[0], pd.DataFrame) or isinstance(data[0], np.ndarray):
            inputdata = np.zeros(len(data), dtype=np.dtype("object"))
            for x in range(len(inputdata)):
                inputdata[x] = np.array(data[x])

    return inputdata


def plot_bar(
    names: Union[List[Any], Tuple[Any], np.ndarray],
    counts: Union[List[Any], Tuple[Any], np.ndarray],
    xlabel: str = "x",
    ylabel: str = "y",
    legend: str = "Legend",
    plottitle: str = "Title",
    output_file: str = "Plot",
) -> None:
    """

    Function to create a vertical bar plot

    Parameters
    ----------
    names: List[Any] | Tuple[Any] | np.ndarray
        The numbers or strings for each bar
    counts: List[Any] | Tuple[Any] | np.ndarray
        The height of the bars
    xlabel: str, Default is "x"
        Label of the x-axis
    ylabel: str, Default is "y"
        Label of the y-axis
    legend: str, Default is "Legend"
        Legend for the bar plot
    plottitle: str, Default is "Title"
        The title of the figure
    output_file: str, Default is "Plot"
        The output file location of the .png of the new figure. Do not need the file extension .png

    """

    fig, ax = plt.subplots(figsize=(8, 8))
    chart = ax.bar(names, counts, label=legend)
    ax.bar_label(chart, label_type="center")
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(plottitle, fontsize=12)

    plt.xticks(rotation=90)
    plt.legend()
    plt.tight_layout()

    plt.savefig(f"{output_file}", dpi=400)


def plot_stackedbar(
    names: Union[List[Any], Tuple[Any], np.ndarray],
    bottom_counts: Union[List[Any], Tuple[Any], np.ndarray],
    top_counts: Union[List[Any], Tuple[Any], np.ndarray],
    xlabel: str = "x",
    ylabel: str = "y",
    bottom_legend: str = "Bottom legend",
    top_legend: str = "Top legend",
    plottitle: str = "Title",
    output_file: str = "Plot",
) -> None:
    """

    Function to create a vertically stacked bar plot

    Parameters
    ----------
    names: List[Any] | Tuple[Any] | np.ndarray
        The numbers or strings for each stacked bar
    bottom_counts: List[Any] | Tuple[Any] | np.ndarray
        The height of the bottom bar in the stacked bar plot
    top_counts: List[Any] | Tuple[Any] | np.ndarray
        The height of the top bar in the stacked bar plot
    xlabel: str, Default is "x"
        Label of the x-axis
    ylabel: str, Default is "y"
        Label of the y-axis
    bottom_legend: str, Default is "Bottom legend"
        Legend for the bottom bar in the stacked bar plot
    top_legend: str, Default is "Top legend"
        Legend for the top bar in the stacked bar plot
    plottitle: str, Default is "Title"
        The title of the figure
    output_file: str, Default is "Plot"
        The output file location of the .png of the new figure. Do not need the file extension .png

    """
    fig, ax = plt.subplots(figsize=(8, 8))
    bar_bottom = ax.bar(names, bottom_counts, label=bottom_legend)
    bar_top = ax.bar(names, top_counts, bottom=bottom_counts, label=top_legend)
    ax.bar_label(bar_bottom, label_type="center")
    ax.bar_label(bar_top, label_type="center")
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(plottitle, fontsize=12)

    plt.xticks(rotation=90)
    plt.legend()
    plt.tight_layout()

    plt.savefig(f"{output_file}", dpi=400)


def plot_bar_horizontal(
    names: Union[List[Any], Tuple[Any], np.ndarray],
    counts: Union[List[Any], Tuple[Any], np.ndarray],
    xlabel: str = "x",
    ylabel: str = "y",
    legend: str = "Legend",
    plottitle: str = "Title",
    output_file: str = "Plot",
) -> None:
    """

    Function to create a bar plot

    Parameters
    ----------
    names: List[Any] | Tuple[Any] | np.ndarray
        The numbers or strings for each bar
    counts: List[Any] | Tuple[Any] | np.ndarray
        The width of the bars
    xlabel: str, Default is "x"
        Label of the x-axis
    ylabel: str, Default is "y"
        Label of the y-axis
    legend: str, Default is "Legend"
        Legend for the bar plot
    plottitle: str, Default is "Title"
        The title of the figure
    output_file: str, Default is "Plot"
        The output file location of the .png of the new figure. Do not need the file extension .png

    """
    fig, ax = plt.subplots(figsize=(8, 8))
    chart = ax.barh(names, counts, label=legend)
    ax.bar_label(chart, label_type="center")
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(plottitle, fontsize=12)

    plt.gca().invert_yaxis()
    plt.legend()
    plt.tight_layout()

    plt.savefig(f"{output_file}", dpi=400)


def plot_stackedbar_horizontal(
    names: Union[List[Any], Tuple[Any], np.ndarray],
    left_counts: Union[List[Any], Tuple[Any], np.ndarray],
    right_counts: Union[List[Any], Tuple[Any], np.ndarray],
    xlabel: str = "x",
    ylabel: str = "y",
    left_legend: str = "Left legend",
    right_legend: str = "Right legend",
    plottitle: str = "Title",
    output_file: str = "Plot",
) -> None:
    """

    Function to create a horizontally stacked bar plot

    Parameters
    ----------
    names: List[Any] | Tuple[Any] | np.ndarray
        The numbers or strings for each stacked bar
    left_counts: List[Any] | Tuple[Any] | np.ndarray
        The height of the left bar in the stacked bar plot
    right_counts: List[Any] | Tuple[Any] | np.ndarray
        The height of the right bar in the stacked bar plot
    xlabel: str, Default is "x"
        Label of the x-axis
    ylabel: str, Default is "y"
        Label of the y-axis
    left_legend: str, Default is "Left legend"
        Legend for the bottom bar in the stacked bar plot
    right_legend: str, Default is "Right legend"
        Legend for the top bar in the stacked bar plot
    plottitle: str, Default is "Title"
        The title of the figure
    output_file: str, Default is "Plot"
        The output file location of the .png of the new figure. Do not need the file extension .png

    """
    fig, ax = plt.subplots(figsize=(8, 8))
    bar_left = ax.barh(names, left_counts, label=left_legend)
    bar_right = ax.barh(names, right_counts, left=left_counts, label=right_legend)
    ax.bar_label(bar_left, label_type="center")
    ax.bar_label(bar_right, label_type="center")
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(plottitle, fontsize=12)

    plt.gca().invert_yaxis()
    plt.legend()
    plt.tight_layout()

    plt.savefig(f"{output_file}", dpi=400)
