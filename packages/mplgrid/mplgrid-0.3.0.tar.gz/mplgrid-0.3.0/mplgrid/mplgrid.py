""" Functions to plot a grid of matplotlib Axes."""

import matplotlib.pyplot as plt

__all__ = ['grid', 'grid_dimensions']


def _grid_dimensions(aspect=1,
                     figheight=9,
                     nrows=1,
                     ncols=1,
                     height=0.715,
                     width=0.95,
                     space=0.05,
                     left=None,
                     bottom=None,
                     ):
    """ A helper to calculate the grid dimensions.

    Parameters
    ----------
    aspect : float, default 1
        The aspect ratio of the grid's axis (height divided by width).
    figheight : float, default 9
        The figure height in inches.
    nrows, ncols : int, default 1
        Number of rows/columns of axes in the grid.
    height : float, default 0.715
        The height of the grid in fractions of the figure height.
        The default is the grid height is 71.5% of the figure height.
    width : float, default 0.95
        The width of the grid in fractions of the figure width.
        The default is the grid is 95% of the figure width.
    space : float, default 0.05
        The total amount of the grid height reserved for spacing between the grid axes.
        Expressed as a fraction of the height. The default is 5% of the grid height.
        The spacing across the grid width is automatically calculated to maintain even spacing.
    left : float, default None
        The location of the left-hand side of the axes in fractions of the figure width.
        The default of None places the axes in the middle of the figure.
    bottom : float, default None
        The location of the bottom axes in fractions of the figure height.
        The default of None places the axes grid in the middle of the figure.

    Returns
    -------
    dimensions : dict[dimension, value]
        A dictionary holding the axes and figure dimensions.
    """
    if left is None:
        left = (1 - width) / 2

    if bottom is None:
        bottom = (1 - height) / 2

    if bottom + height > 1:
        error_msg_height = ('The axes extends past the figure height. '
                            'Reduce one of the bottom, or height so the total is ≤ 1.')
        raise ValueError(error_msg_height)

    if left + width > 1:
        error_msg_width = ('The grid axes extends past the figure width. '
                           'Reduce one of the width or left so the total is ≤ 1.')
        raise ValueError(error_msg_width)

    if (nrows > 1) and (ncols > 1):
        figwidth = (figheight * height / width * (((1 - space) / aspect * ncols / nrows) +
                                                  (space * (ncols - 1) / (nrows - 1))))
        spaceheight = height * space / (nrows - 1)
        spacewidth = spaceheight * figheight / figwidth
        axheight = height * (1 - space) / nrows
        axwidth = (width - (spacewidth * (ncols - 1))) / ncols
        wspace = spacewidth / axwidth
        hspace = spaceheight / axheight

    elif (nrows > 1) and (ncols == 1):
        figwidth = figheight * height / width * (1 - space) / aspect / nrows
        axheight = height * (1 - space) / nrows
        spaceheight = height * space / (nrows - 1)
        wspace = 0
        hspace = spaceheight / axheight

    elif (nrows == 1) and (ncols > 1):
        figwidth = figheight * height / width * (space + ncols / aspect)
        spacewidth = height * space * figheight / figwidth / (ncols - 1)
        axwidth = (width - (spacewidth * (ncols - 1))) / ncols
        wspace = spacewidth / axwidth
        hspace = 0

    else:  # nrows=1, ncols=1
        figwidth = figheight * height / aspect / width
        wspace = 0
        hspace = 0

    return {'figheight': figheight,
            'figwidth': figwidth,
            'nrows': nrows,
            'ncols': ncols,
            'aspect': aspect,
            'left': left,
            'right': left + width,
            'bottom': bottom,
            'top': bottom + height,
            'hspace': hspace,
            'wspace': wspace,
            }


def grid(aspect=1,
         figheight=9,
         nrows=1,
         ncols=1,
         height=0.715,
         width=0.95,
         space=0.05,
         left=None,
         bottom=None,
         ):
    """ Create a grid of axes in a specified location

    Parameters
    ----------
    aspect : float, default 1
        The aspect ratio of the grid's axis (height divided by width).
    figheight : float, default 9
        The figure height in inches.
    nrows, ncols : int, default 1
        Number of rows/columns of axes in the grid.
    height : float, default 0.715
        The height of the grid in fractions of the figure height.
        The default is the grid height is 71.5% of the figure height.
    width : float, default 0.95
        The width of the grid in fractions of the figure width.
        The default is the grid is 95% of the figure width.
    space : float, default 0.05
        The total amount of the grid height reserved for spacing between the grid axes.
        Expressed as a fraction of the height. The default is 5% of the grid height.
        The spacing across the grid width is automatically calculated to maintain even spacing.
    left : float, default None
        The location of the left-hand side of the axes in fractions of the figure width.
        The default of None places the axes in the middle of the figure.
    bottom : float, default None
        The location of the bottom axes in fractions of the figure height.
        The default of None places the axes grid in the middle of the figure.

    Returns
    -------
    fig : matplotlib.figure.Figure
    axs : matplotlib Axes or array of Axes
    """
    dim = _grid_dimensions(aspect=aspect,
                           figheight=figheight,
                           width=width,
                           height=height,
                           nrows=nrows,
                           ncols=ncols,
                           space=space,
                           left=left,
                           bottom=bottom)
    fig, ax = plt.subplots(figsize=(dim['figwidth'], dim['figheight']),
                           nrows=dim['nrows'], ncols=dim['ncols'],
                           gridspec_kw={'left': dim['left'],
                                        'bottom': dim['bottom'],
                                        'right': dim['right'],
                                        'top': dim['top'],
                                        'wspace': dim['wspace'],
                                        'hspace': dim['hspace'],
                                        },
                           )
    return fig, ax


def grid_dimensions(aspect,
                    figwidth,
                    figheight,
                    nrows,
                    ncols,
                    max_side,
                    space,
                    ):
    """ Propose a grid_width and grid_height for grid based on the inputs.

    Parameters
    ----------
    aspect : float, default 1
        The aspect ratio of the grid's axis (height divided by width).
    figwidth, figheight : float
        The figure width/height in inches.
    nrows, ncols : int
        Number of rows/columns of axes in the grid.
    max_side : float
        The longest side of the grid in fractions of the figure width / height.
        Should be between zero and one.
    space : float
        The total amount of the grid height reserved for spacing between the grid axes.
        Expressed as a fraction of the grid_height.

    Returns
    -------
    grid_width, grid_height : the suggested grid_width and grid_height
    """
    # grid1 = calculate the width given the max_grid as height
    # grid2 = calculate height given the max_grid as width

    if ncols > 1 and nrows == 1:
        grid1 = max_side * figheight / figwidth * (space + ncols / aspect)
        grid2 = max_side / figheight * figwidth / (space + ncols / aspect)
    elif ncols > 1 or nrows > 1:
        extra = space * (ncols - 1) / (nrows - 1)
        grid1 = max_side * figheight / figwidth * (((1 - space) / aspect *
                                                    ncols / nrows) + extra)
        grid2 = max_side / figheight * figwidth / (((1 - space) / aspect *
                                                    ncols / nrows) + extra)
    else:  # nrows=1, ncols=1
        grid1 = max_side * figheight / figwidth / aspect
        grid2 = max_side / figheight * figwidth * aspect

    # decide whether the max_grid is the width or height and set the other value
    if (grid1 > 1) | ((grid2 >= grid1) & (grid2 <= 1)):
        return max_side, grid2
    return grid1, max_side
