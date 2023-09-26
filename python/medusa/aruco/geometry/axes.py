"""Coordinate Axis.

Simple dataclass containing the points representing x\u0302, y\u0302, z\u0302.
"""
from __future__ import annotations

from dataclasses import dataclass

from .transform import Se3
from .point import Point, Points


@dataclass
class Axes:
    """x\u0302, y\u0302, z\u0302."""

    x: Point
    y: Point
    z: Point

    @classmethod
    def default(cls) -> Axes:
        """Create the standard x\u0302, y\u0302, z\u0302 coordinate axis."""
        return Axes(
            x=Point(1.0, 0.0, 0.0),
            y=Point(0.0, 1.0, 0.0),
            z=Point(0.0, 0.0, 1.0),
        )

    def transform(self, transform: Se3) -> Axes:
        """Apply the transformation to the coordinate axes."""
        temp = Points([self.x, self.y, self.z])
        temp = temp.transform(transform)
        return Axes(temp[0], temp[1], temp[2])

    def scale(self, factor: float) -> Axes:
        """Scale the coordinate axis. Useful for normalization."""
        return Axes(self.x * factor, self.y * factor, self.z * factor)
