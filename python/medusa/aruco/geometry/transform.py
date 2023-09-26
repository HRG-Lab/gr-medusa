"""Defines the Se3 class."""
from __future__ import annotations

from dataclasses import dataclass, field

import cv2
import numpy as np


@dataclass
class Se3:
    r"""Rigid transformation.

    A class representing the 4x4 SE(3) rigid transformation matrix which
    represents all possible 3D rotation/translation transformations. More
    information can be found
    [here](http://motion.cs.illinois.edu/RoboticSystems/CoordinateTransformations.html).

    Briefly, an SE(3) transformation (for real world transformations
    specifically) is a `#!math 3 \times 3` rotation matrix, `#!math \textrm{R}`
    and a `#!math 3 \times 1` translation matrix, `#!math \textrm{T}` as this
    `#!math 4 \times 4` matrix:

    ```math
    \left(\begin{matrix}
    r_{11} & r_{12} & r_{13} & t_x \\
    r_{21} & r_{22} & r_{23} & t_y \\
    r_{31} & r_{32} & r_{33} & t_z \\
    0 & 0 & 0 & 1
    \end{matrix}\right)
    ```

    Or more compactly:

    ```math
    \left(\begin{matrix}
    \textrm{R}_{3 \times 3} & \textrm{t}_{3 \times 1} \\
    0_{1 \times 3} & 1
    \end{matrix}\right)
    ```

    Args:
        rvec: Rotation vector
        tvec: Translation vector

    Attributes:
        rvec: (3x1) rotation vector
        tvec: (3x1) translation vector
        mat: (4x4) transformation matrix of the form
    """

    rvec: np.ndarray
    tvec: np.ndarray
    mat: np.ndarray = field(init=False)

    def __post_init__(self) -> None:  # noqa: D105
        r, _ = cv2.Rodrigues(self.rvec)
        t = np.zeros((4, 4))
        t[0:3, 0:3] = r
        t[0:3, 3] = self.tvec.reshape((3,))
        t[3, 3] = 1
        self.mat = t

    def __matmul__(self, other: Se3) -> Se3:
        """Allow chaining transforms e.g. A@B@C."""
        return Se3.from_matrix(self.mat @ other.mat)

    @classmethod
    def from_matrix(cls, mat: np.ndarray) -> Se3:
        """Alternate constructor. Takes (4,4) np.ndarray."""
        try:
            mat = mat.reshape((4, 4))
        except ValueError:
            raise ValueError(f"Expected 4X4 matrix. Got {mat.shape}")

        rvec, _ = cv2.Rodrigues(mat[0:3, 0:3])
        tvec = mat[3, 0:3]
        return cls(rvec, tvec)

    @staticmethod
    def default() -> Se3:
        mat = np.zeros((4, 4))
        mat[0:3, 0:3] = np.eye((3, 3))
        mat[3, 3] = 1
        return Se3.from_matrix(mat)

    def inv(self) -> Se3:
        """Inverse transformation.

        Returns:
            Inverted Se3 object
        """
        inv = np.linalg.inv(self.mat)
        rinv = inv[0:3, 0:3]
        rinv, _ = cv2.Rodrigues(rinv)
        tinv = inv[:3, 3]
        return Se3(rinv, tinv)
