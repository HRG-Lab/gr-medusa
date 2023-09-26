#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 Bailey Campbell.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr

import pmt

import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.opengl import GLViewWidget, GLSurfacePlotItem

import time

pi = np.pi
sin = np.sin
cos = np.cos


def spherical_to_cartesian(r, theta, phi):
    """Convert spherical coordinates to cartesian coordinates.

    Args:
        r (np.ndarray): r coordinates
        theta (np.ndarray): theta coordinates
        phi (np.ndarray): phi coordinates

    Returns:
        x (np.ndarray): x coordinates
        y (np.ndarray): y coordinates
        z (np.ndarray): z coordinates
    """
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)

    return x, y, z


def clean_complex_to_db(array: np.ndarray) -> np.ndarray:
    """Calculates dB from an array of complex values.

    Does some preprocessing of the input data to ensure no warnings are
    generated. Specifically, it replaces 0 magnitudes with a very small constant
    (1e-20).

    Args:
        array (np.ndarray): Array of complex values

    Returns:
        (np.ndarray): $20 log_{10}(array)$
    """
    mag = np.abs(array)
    clean_array = np.where(mag == 0, 1e-20, mag)
    return 20 * np.log10(clean_array)


class plot_3d_array_factor(gr.sync_block, GLViewWidget):
    """
    docstring for block plot_3d_array_factor
    """

    def __init__(self, parent=None):
        gr.sync_block.__init__(
            self, name="plot_3d_array_factor", in_sig=None, out_sig=None
        )

        GLViewWidget.__init__(self, parent=parent)
        self.surface = GLSurfacePlotItem(
            z=np.ones((361, 181)),
            computeNormals=False,
        )
        self.addItem(self.surface)

        self.r_max = 100
        self.r_min = 0
        self.cmap = pg.colormap.get("cividis")
        self.update_rate = 1000000
        self.past = time.time_ns()

        self.show()

        self.message_port_register_in(pmt.intern("plot"))
        self.set_msg_handler(pmt.intern("plot"), self.handle_data)

    def handle_data(self, msg):
        now = time.time_ns()
        if (now - self.past) < self.update_rate:
            return
        self.past = now
        data = pmt.to_python(msg)

        r = data["r"]["data"].reshape(data["r"]["shape"])
        r = clean_complex_to_db(r)
        # print(f"{np.amin(r)=} {np.amax(r)=}")
        r = np.clip(r, self.r_min, self.r_max)
        r_mapped = r + np.abs(self.r_min)
        r_range = np.abs(self.r_max - self.r_min)
        r_cmapped = (r - (self.r_min)) / r_range
        colors = self.cmap.map(r_cmapped, mode="float")

        r_range = np.abs(self.r_max - self.r_min)
        r_scale = 100 / r_range

        self.surface.resetTransform()
        self.surface.scale(1, 1, r_scale)
        self.surface.translate(0, 0, -self.r_min)

        theta = data["theta"]["data"].reshape(data["theta"]["shape"])
        phi = data["phi"]["data"].reshape(data["phi"]["shape"])

        self.surface.setData(theta, phi, r_mapped, colors=colors)
        # self.surface.setData(theta, phi, r)
