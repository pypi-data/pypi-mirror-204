""" Tests for mplgrid."""

from math import isclose
from random import randint, uniform

import matplotlib.pyplot as plt

from mplgrid import grid, grid_dimensions


def test_figsize():
    """ Test that the right figure size is created."""
    for i in range(100):
        aspect = uniform(0.3, 3)
        nrows = randint(1, 6)
        ncols = randint(1, 6)
        figwidth = uniform(0.5, 10)
        figheight = uniform(0.5, 10)
        max_side = uniform(0.5, 1)
        space = uniform(0, 0.2)

        width, height = grid_dimensions(aspect=aspect,
                                        figwidth=figwidth,
                                        figheight=figheight,
                                        nrows=nrows,
                                        ncols=ncols,
                                        max_side=max_side,
                                        space=space,
                                        )
        assert (isclose(height - max_side, 0, abs_tol=1e-09) or
                isclose(width - max_side, 0, abs_tol=1e-09)
                )

        fig, ax = grid(aspect=aspect,
                       figheight=figheight,
                       nrows=nrows,
                       ncols=ncols,
                       height=height,
                       width=width,
                       space=space,
                       )
        check_figwidth, check_figheight = fig.get_size_inches()

        assert isclose(check_figwidth - figwidth, 0, abs_tol=1e-09)
        assert isclose(check_figheight - figheight, 0, abs_tol=1e-09)
        plt.close(fig)


def test_return_shape():
    """ Test that the return shape is the same as plt.subplots."""
    for nrows in range(1, 4):
        for ncols in range(1, 4):
            fig1, ax1 = plt.subplots(nrows=nrows, ncols=ncols)
            fig2, ax2 = grid(nrows=nrows, ncols=ncols)
            if nrows > 1 or ncols > 1:
                assert ax1.shape == ax2.shape
            plt.close(fig1)
            plt.close(fig2)
