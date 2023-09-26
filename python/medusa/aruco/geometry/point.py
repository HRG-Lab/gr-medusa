"""Defines Point3D class."""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import List, Tuple, Union

from typing import overload
from collections.abc import Sequence
import numpy as np
from numpy.distutils.misc_util import is_sequence

from .transform import Se3


class Point:
    """A point in 3D Euclidean space.

    Internally, it is a 3-element ndarray representing x, y, and z coordinates.
    """

    __slots__ = ['_coords']
    _coords: np.ndarray

    def __init__(self, *args) -> None:
        """Create a point.

        Args:
            *args: Takes either 3 elements x, y, z or a single element that is
                numpy sequenceable e.g. Tuple, List, np.ndarry, Set, etc.
        """
        if len(args) == 1:
            if not is_sequence(args[0]):
                raise ValueError(
                    "Must pass a sequence, e.g. list, tuple, np.ndarray."
                )
            if isinstance(args[0], np.ndarray):
                try:
                    self._coords = args[0].reshape((3,))
                except ValueError:
                    raise ValueError(
                        "Couldn't broadcast Point argument to shape (3,)."
                    )
            else:
                if len(args[0]) != 3:
                    raise ValueError(
                        f"Must have length 3. Got {len(args[0])}")
                self._coords = np.array(args[0])
        elif len(args) == 3:
            self._coords = np.array([args[0], args[1], args[2]])
        else:
            raise ValueError(
                f"Point expects either 1 or 3 arguments. Got: {len(args)}"
            )

    @property
    def x(self) -> float:
        """X coordinate."""
        return self._coords[0]

    @property
    def y(self) -> float:
        """Y coordinate."""
        return self._coords[1]

    @property
    def z(self) -> float:
        """Z coordinate."""
        return self._coords[2]

    @property
    def coords(self) -> np.ndarray:
        """Point as ndarray with shape (3,)."""
        return self._coords

    def tolist(self) -> List:
        """Wrapper for np.ndarray.tolist."""
        return self._coords.tolist()

    @property
    def T(self) -> np.ndarray:
        """Transpose.

        Returns:
            ndarray (3,1) that is this point's coordinates transpose. First
            converts the internal array to a column vector (1,3) and transposes.
            Useful for mathematical calculations.
        """
        return self._coords.reshape((1, 3)).T

    def __add__(self, p: Point) -> Point:
        """Add two points together."""
        return Point(self.x + p.x, self.y + p.y, self.z + p.z)

    def __sub__(self, p: Point) -> Point:
        """Subtract a point from this point."""
        return Point(self.x - p.x, self.y - p.y, self.z - p.z)

    def __mul__(self, scalar: float) -> Point:
        """Multiply this point by a scalar."""
        return Point(self.x * scalar, self.y * scalar, self.z * scalar)

    def __neg__(self) -> Point:
        """Negate this point."""
        return Point(-self.x, -self.y, -self.z)

    def __eq__(self, other: object) -> bool:
        """Tests if two points are (approximately) equal."""
        if not isinstance(other, Point):
            raise NotImplementedError
        return np.allclose([self.x, self.y, self.z], [other.x, other.y, other.z])

    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__

    def __repr__(self) -> str:
        """Official string representation."""
        return f"Point({self.x}, {self.y}, {self.z})"

    def distance(self, p: Point) -> float:
        """Calculate distance this point and p."""
        return np.sqrt((self.x - p.x) ** 2 + (self.y - p.y) ** 2 + (self.z - p.z) ** 2)

    def to_cylindrical(self) -> Tuple[float, float, float]:
        """Find cylindrical coordinates."""
        r = np.sqrt(self.x ** 2 + self.y ** 2)
        phi = np.arctan(self.y / self.x)
        z = self.z
        return r, phi, z

    def to_spherical(self) -> Tuple[float, float, float]:
        """Find spherical coordinates."""
        r = np.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        theta = np.arctan(np.sqrt(self.x ** 2 + self.y ** 2) / self.z)
        phi = np.arctan(self.y / self.x)

        return r, theta, phi

    def transform(self, transform: Se3) -> Point:
        """Applies rigid transform to point.

        Args:
            transform: Rigid transformation SE(3)

        Returns:
            A new Point with the applied transformation.
        """
        temp = np.hstack((self._coords, 1)).reshape(1, -1)
        ret = np.einsum("ij,kj->ki", transform.mat, temp)[0]
        return Point(ret[0], ret[1], ret[2])


class Points(Sequence):
    """A collection of Point3Ds."""

    def __init__(self, points: Union[List[Point], np.ndarray]) -> None:
        """Creates the Points3D object."""
        if isinstance(points, list):
            self._points = np.array([p.coords for p in points])
        else:
            self._points = np.array(points)

    @overload
    def __getitem__(self, index: int) -> Point:  # noqa: D105
        ...

    @overload
    def __getitem__(self, index: slice) -> Points:  # noqa: D105
        ...

    def __getitem__(self, index: Union[slice, int]) -> Union[Point, Points]:
        """Implements indexing."""
        if isinstance(index, int):
            return Point(self._points[index])
        elif isinstance(index, slice):
            return Points(self._points[index.start: index.stop: index.step])
        else:
            raise TypeError(f"Expected int or slice, got {type(index)}")

    def __setitem__(self, index: int, item: Point) -> None:
        """Implement Points[idx] = Point."""
        self._points[index] = item.coords

    def __len__(self) -> int:
        """Number of points."""
        return len(self._points)

    def __str__(self) -> str:
        """String representation. If it's too long (>5) truncates with ...."""
        ret = ""
        if len(self._points) > 5:
            for i in range(5):
                ret += f"{self._points[i]}\n"
            ret += "..."
        else:
            for p in self._points:
                ret += f"{p}\n"
        return ret

    @property
    def array(self) -> np.ndarray:
        """Returns points array."""
        return self._points

    @property
    def points_list(self) -> List[Point]:
        """Converts internal array to list of Point."""
        return [self._points[i] for i in range(len(self._points))]

    @property
    def center(self) -> Point:
        """Find the geometric center of a collection of points."""
        xs = [p[0] for p in self._points]
        ys = [p[1] for p in self._points]
        zs = [p[2] for p in self._points]

        return Point(np.mean(xs), np.mean(ys), np.mean(zs))

    def dists(self, origin=Point(0, 0, 0)) -> np.ndarray:
        """Calculate distance of all points to origin."""
        temp = self._points.T - origin.T
        return np.sqrt(np.einsum("ij,ij->j", temp, temp))

    def transform(self, transform: Se3) -> Points:
        """Apply rigid transformation to all points.

        Args:
            transform: Rigid transformation SE(3)

        Returns:
            New Points object with all points after transformation.
        """
        temp = np.hstack((self._points, np.ones((len(self._points), 1))))
        return Points(np.einsum("ij,kj->ki", transform.mat, temp)[:, 0:3])
