#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 Bailey Campbell.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy as np
from gnuradio import gr
from gnuradio.gr import pmt
import pyqtgraph as pg
from pyqtgraph import PlotWidget
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.Qt.QtCore import QObject
import math


class PolarPlotWidget(PlotWidget):
    def __init__(self, autoscale, log_plot, plot_depth_db, *args):
        PlotWidget.__init__(self, enableMenu=False, axisItems={}, *args)
        self.curve = self.plot([], pen=(0, 200, 100), width=2.0, name="Polar Response")
        self.line = pg.InfiniteLine(QtCore.QPointF(0.0, 0.0), 0)
        self.addItem(self.line)

        self.circles = []
        self.autoscale = autoscale
        self.log_plot = log_plot
        self.plot_depth = plot_depth_db
        angles = np.array(np.linspace(-180.0, 180.0, 361), dtype=np.float32)
        for kk in range(0, int(10 * math.floor(self.plot_depth / 10.0)), 10):
            mag = 1 - float(kk) / self.plot_depth
            r = mag * np.ones(len(angles))
            x = self.pol_to_car_x(r, angles)
            y = self.pol_to_car_y(r, angles)
            self.circles.append(
                self.plot(x, y, pen=pg.mkPen((128, 128, 128), style=QtCore.Qt.DashLine))
            )

    # Polar to Cartesian
    def pol_to_car_x(self, r, theta):
        x = r * np.cos(theta * np.pi / 180.0)
        return x

    def pol_to_car_y(self, r, theta):
        y = r * np.sin(theta * np.pi / 180.0)
        return y

    def db_to_lin(x):
        return np.power(10, x / 20.0)

    def lin_to_db(x):
        return 20 * np.log10(x)

    def setLineAngle(self, theta):
        self.line.setAngle(90 + theta)

    def updateGraph(self, theta, r):
        y = self.pol_to_car_y(r, theta)
        x = self.pol_to_car_x(r, theta)

        self.curve.setData(y, x)


class polar_plot(gr.sync_block, QObject):
    """
    docstring for block test_gui
    """

    sigUpdateData = QtCore.Signal(object, object)
    sigUpdateAngle = QtCore.Signal(float)

    def __init__(self):
        gr.sync_block.__init__(self, name="polar_plot", in_sig=None, out_sig=None)
        QObject.__init__(self)

        self.message_port_register_in(pmt.intern("plot"))
        self.set_msg_handler(pmt.intern("plot"), self.handler)

    def set_angle_degrees(self, angle_degrees):
        self.angle_degrees = angle_degrees
        self.sigUpdateAngle.emit(self.angle_degrees)

    def handler(self, msg):
        d = pmt.to_python(msg)
        r = d["r"]
        theta = d["theta"]

        self.sigUpdateData.emit(theta, r)
