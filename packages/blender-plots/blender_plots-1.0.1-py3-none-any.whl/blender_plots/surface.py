import numpy as np

import bpy


"""Create a scatterplot.

Args:
    x,y,z:
        If y and z are not provided: expects x to be a Nx3 array with xyz positions for points to scatter, or TxNx3
            for sequence of scatter plots to animate
        if y and z are provided: expects x,y,z to be length N or TxN arrays for xyz coordinates respectively.
    color: Nx3 or Nx4 array or with RGB or RGBA values for each point, or a single RGB/RGBA-value
        (e.g. (1, 0, 0) for red) to apply to every point.
    name: name to use for blender object. Will delete any previous plot with the same name.
    marker_type: select appearance of points. Either MARKER_TYPE, "spheres", bpy_types.Mesh or bpy_types.Object
    marker_scale: xyz scale for markers
    marker_rotation: Nx3 (euler angles in radians) or Nx3x3 (rotation matrices) array specifying the rotation for
        each marker. Or "random" for applying a random rotation to each marker.
    randomize_rotation: If set to True randomize the rotation of each marker. Overrides marker_rotation.
    marker_kwargs: additional arguments for configuring markers
"""

class Surface:
    """Create a surface plot.
    Args:
        x, y, z:

    """

    def __init__(self, x, y, z, color=None, name="surface"):
        pass

    @property
    def points(self):
        return self._points
    
    @points.setter
    def points(self, points):
        self._points = points
        self.update_points()

    def update_points(self):
        pass

    

