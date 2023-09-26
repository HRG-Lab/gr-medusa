#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 Bailey Campbell.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import itertools

from gnuradio import gr
import pmt

import numpy as np
import pyqtgraph as pg

from pyqtgraph import PlotWidget
from PyQt5.QtCore import pyqtSignal, QObject


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


class ContourPlot(PlotWidget):
    def __init__(
        self,
        title="",
        background="default",
        cmap="viridis",
        x_tick_spacing=15,
        y_tick_spacing=30,
        num_levels=10,
        auto_scale=False,
        draw_isos=True,
        signal_angle=(0, 0),
        parent=None,
        **kwargs,
    ):
        super().__init__(title=title, background=background, parent=parent, **kwargs)

        self.x_tick_spacing = x_tick_spacing
        self.y_tick_spacing = y_tick_spacing
        self.num_levels = num_levels
        self.isocurves = []
        self.autoScale = auto_scale
        self.drawIsolines = draw_isos
        self.z_min = 50
        self.z_max = 90

        self.signal_angle = (0, 0)
        self.intf_angles = [(0, 0)]

        self.x = np.linspace(-180, 180, 361)
        self.y = np.linspace(0, 180, 180)
        self.z = np.array([])

        self.img_item = pg.ImageItem()
        self.addItem(self.img_item)
        self.cbar = self.addColorBar(self.img_item, colorMap=cmap, interactive=False)
        self.setMouseEnabled(x=False, y=False)
        self.disableAutoRange()
        self.hideButtons()
        self.showAxes(True, showValues=(True, False, False, True))

        x_step = round(
            len(self.x)
            / ((np.nanmax(self.x) - np.nanmin(self.x)) / self.x_tick_spacing)
        )
        y_step = round(
            len(self.y)
            / ((np.nanmax(self.y) - np.nanmin(self.y)) / self.y_tick_spacing)
        )
        x_ticks = {
            k + 0.5: str(round(v))
            for k, v in itertools.islice(enumerate(self.x), 0, None, x_step)
        }
        y_ticks = {
            k + 0.5: str(round(v))
            for k, v in itertools.islice(enumerate(self.y), 0, None, y_step)
        }

        self.getPlotItem().getAxis("bottom").setTicks([x_ticks.items()])
        self.getPlotItem().getAxis("left").setTicks([y_ticks.items()])

        self.sig_point_item = pg.ScatterPlotItem(
            size=10,
            pen=pg.mkPen("green"),
            brush=pg.mkBrush("green"),
            pos=[(self.signal_angle[0] + 180, self.signal_angle[1])],
        )
        self.addItem(self.sig_point_item)

        self.intf_point_items = []
        for intf in self.intf_angles:
            intf_item = pg.ScatterPlotItem(
                size=10,
                pen=pg.mkPen("red"),
                brush=pg.mkBrush("red"),
                pos=[(intf[0] + 180, intf[1])],
            )
            self.intf_point_items.append(intf_item)
            self.addItem(intf_item)

    def setCmap(self, cmap):
        self.img_item.setColorMap(cmap)
        self.cbar.setColorMap(cmap)

    def setAutoScale(self, state):
        self.autoScale = state
        self.redraw()

    def setTitle(self, text: str) -> None:
        self.getPlotItem().setTitle(text)

    def setZMin(self, z):
        self.z_min = z
        self.redraw()

    def setZMax(self, z):
        self.z_max = z
        self.redraw()

    def setDrawIsolines(self, state: bool):
        self.drawIsolines = state
        if state:
            self.draw_isos()
            return

        for c in self.isocurves:
            self.removeItem(c)
        self.isocurves = []

    def setXLabel(self, text: str = "", units: str = "") -> None:
        self.getPlotItem().getAxis("bottom").setLabel(text=text, units=units)

    def setYLabel(self, text: str = "", units: str = "") -> None:
        self.getPlotItem().getAxis("left").setLabel(text=text, units=units)

    def setData(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        self.redraw()

    def setSignalAngle(self, signal_angle):
        self.signal_angle = signal_angle
        self.sig_point_item.setData(pos=[(signal_angle[0] + 180, signal_angle[1])])

    def setIntfAngles(self, intf_angles):
        self.intf_angles = intf_angles
        for intf, item in zip(self.intf_angles, self.intf_point_items):
            item.setData(pos=[(intf[0] + 180, intf[1])])

    def draw_isos(self):
        levels = np.linspace(self.z_min, self.z_max, self.num_levels)
        self.isocurves = []
        for i in range(len(levels)):
            v = levels[i]
            c = pg.IsocurveItem(level=v, pen=(i, len(levels) * 1.5))
            self.addItem(c)
            c.setZValue(10)
            self.isocurves.append(c)
            c.setData(self.z)

    def redraw(self):
        x = self.x
        y = self.y
        z = self.z
        if any((x is None, y is None, z is None)) or any(
            (len(x) == 0, len(y) == 0, len(z) == 0)
        ):
            return

        self.setRange(xRange=(0, len(x)), yRange=(0, len(y)), padding=0.05)

        for c in self.isocurves:
            self.removeItem(c)

        if self.drawIsolines:
            self.draw_isos()

        if self.autoScale:
            self.z_min = np.clip(np.nanmin(z), -100, None)
            self.z_max = np.nanmax(z)
            # self.newZBounds.emit(self.z_min, self.z_max)

        self.img_item.setImage(z)

        self.cbar.setLevels((self.z_min, self.z_max))


class plot_array_factor_contour(gr.sync_block, QObject):
    """
    docstring for block plot_array_factor_contour
    """

    newData = pyqtSignal(object, object, object)
    newAngle = pyqtSignal(object)
    newIntfAngle = pyqtSignal(object)

    def __init__(self):
        gr.sync_block.__init__(
            self, name="plot_array_factor_contour", in_sig=None, out_sig=None
        )
        QObject.__init__(self)

        self.message_port_register_in(pmt.intern("plot"))
        self.set_msg_handler(pmt.intern("plot"), self.handle_new_data)

    def set_signal_angle(self, theta, phi):
        self.newAngle.emit((theta, phi))

    def set_intf_angle(self, theta, phi):
        self.newIntfAngle.emit([(theta, phi)])

    def handle_new_data(self, msg):
        data = pmt.to_python(msg)

        r = data["r"]["data"].reshape(data["r"]["shape"])
        # theta = data["theta"]["data"].reshape(data["theta"]["shape"])
        # phi = data["phi"]["data"].reshape(data["phi"]["shape"])
        theta = np.linspace(-180, 180, 361)
        phi = np.linspace(0, 180, 181)

        r = clean_complex_to_db(r)

        self.newData.emit(np.rad2deg(theta), np.rad2deg(phi), r)
