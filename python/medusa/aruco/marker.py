from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Optional, Tuple

import numpy as np
import cv2 as cv

from .geometry.axes import Axes
from .geometry.point import Point, Points
from .geometry.transform import Se3


class Marker:
    """Represents a single marker in a frame.

    This includes its rotation and translation vectors and metadata like the
    marker id. On initialization, it also initializes an
    `Se3` object represents an Se3 Lie group (more
    information in `Se3`).

    Attributes:
        id: Marker id
        center: Center coordinates of the marker
        axes: x, y, z unit vectors in global reference frame
        corners: Coordinates of the four corners (clockwise from top left)
        origin: Origin marker
        se3: Se3 transformation matrix from origin to position
    """

    def __init__(
        self,
        id: int,
        marker_length: float,
        rvec: np.ndarray,
        tvec: np.ndarray,
        origin: Optional[Marker],
    ):
        """Initalizes the Marker.

        Automatically creates the internal Se3 object and initializes objpoints
        to the points relative to origin. If `origin` is `None`, this marker
        **is** the origin.

        Args:
            id: Marker id
            marker_length: Side length of marker in meters
            rvec: Rotation vector (marker -> camera)
            tvec: Translation vector (marker -> camera)
            origin: The marker that defines the coordinate system for this marker
        """
        self._id = id
        self._origin = None
        self._se3 = Se3(rvec, tvec)
        self._se3_rel = None
        self._center = Point([0.0, 0.0, 0.0])
        self._axes = Axes.default().scale(marker_length)
        self._corners = Points(
            np.array(
                [
                    [-marker_length / 2.0, marker_length / 2.0, 0],  # top left
                    [marker_length / 2.0, marker_length / 2.0, 0],  # top right
                    [marker_length / 2.0, -marker_length / 2.0, 0],  # bottom right
                    [-marker_length / 2.0, -marker_length / 2.0, 0],  # bottom left
                ]
            )
        )

        if origin:
            self._origin = origin
            se3 = self._calc_rel_transform(self._origin)
            se3i = se3.inv()
            self._se3_rel = se3i
            self._center = self._center.transform(se3i)
            self._axes = self._axes.transform(se3i)
            self._corners = self._corners.transform(se3i)

    @property
    def origin(self) -> Optional[Marker]:
        """Returns the origin marker this marker is relative to.

        Returns:
            Origin marker if it exists
        """
        return self._origin

    @property
    def id(self) -> int:
        """Returns marker id.

        Returns:
            Marker id
        """
        return self._id

    @property
    def corners(self) -> Points:
        """Points of 4 corners of marker."""
        return self._corners

    @property
    def center(self) -> Point:
        """Center of marker."""
        return self._center

    @property
    def axes(self) -> Axes:
        """Returns origin and x, y, z axes.

        Returns:
            Numpy array of [origin, x-axis, y-axis, z-axis] coordinates
        """
        return self._axes

    @property
    def se3(self) -> Se3:
        """Returns this marker's transformation matrix.

        Returns:
            This marker's transformation matrix
        """
        return self._se3

    @property
    def se3_relative_to_origin(self) -> Se3:
        """Returns this marker's transformation matrix relative to its origin.

        Returns:
            This marker's transformation matrix relative to its origin
        """
        if self.is_origin():
            return Se3.default()

        return self._se3_rel

    def is_origin(self) -> bool:
        """If this marker is the origin marker."""
        return self._origin is None

    def _calc_rel_transform(self, origin: Marker) -> Se3:
        """Calculates transform from origin to this marker.

        Args:
            origin: Origin marker object
            markers: List of markers to calculate transforms for

        Returns:
            Transformation
        """
        r1 = origin.se3.rvec.reshape((3, 1))
        t1 = origin.se3.tvec.reshape((3, 1))

        r2 = self.se3.rvec.reshape((3, 1))
        t2 = self.se3.tvec.reshape((3, 1))
        r2inv, t2inv = self._inverse_perspective(r2, t2)
        r3, t3, *_ = cv.composeRT(r1, t1, r2inv, t2inv)

        return Se3(r3, t3)

    def _inverse_perspective(self, rvec, tvec) -> Tuple[np.ndarray, np.ndarray]:
        """Reverses transform. e.g. from Marker->Camera to Camera->Marker.

        Args:
            rvec: (3x1) rotation vector
            tvec: (3x1) translation vector

        Returns:
            Tuple (rvec, tvec) of inverted transforms
        """
        r, _ = cv.Rodrigues(rvec)
        tinv = np.dot(-r.T, tvec)
        rinv, _ = cv.Rodrigues(r.T)

        return rinv, tinv
