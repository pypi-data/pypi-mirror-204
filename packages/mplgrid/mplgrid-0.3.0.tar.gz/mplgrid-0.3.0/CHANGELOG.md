:rocket: Version 0.3.0
----------------------

Fixes
- Fix the aspect argument as it was setting the aspect ratio, which produced the wrong size \
of chart when data was added.

:rocket: Version 0.2.1
----------------------

Fixes
- Fix docstrings for aspect (height / width)

:rocket: Version 0.2
--------------------

Changed
- removed the ability to create endnote and title axes.
- grid now returns axes and figure instead of a dictonary.
- grid uses matplotlib plt.subplots instead of manually adding the axes with fig.add_axes()
- aspect is flipped to match matplotlib (height / width) instead of the previous (width / height)
- arguments are now renamed: grid_height to height, grid_width to width, and max_grid to max_side.

:rocket: Version 0.1.0
----------------------

Changed
- renamed ax_key to grid_key and changed the default to 'grid'
- changed the defaults so there is no title or endnote
- changed the returned result so if there is no endnote or title \
it returns the axes (e.g. numpy array of axes) rather than a dictionary.

Added
- added a test for the figsize


:rocket: Version 0.0.0
----------------------

Initial version of mplgrid with functions for creating a grid of Matplotlib axes and calculating the
ideal grid dimensions.
