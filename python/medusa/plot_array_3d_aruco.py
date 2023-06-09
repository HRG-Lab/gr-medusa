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

import pyqtgraph.opengl as gl
from pyqtgraph.opengl import GLViewWidget
from pyqtgraph.Qt import QtCore


class plot_array_3d_aruco(gr.sync_block, GLViewWidget):
    """
    docstring for block plot_array_3d_aruco
    """

    sigUpdateData = QtCore.Signal(object)

    def __init__(self, origin, *args):
        gr.sync_block.__init__(
            self,
            name="plot_array_3d_aruco",
            in_sig=None,
            out_sig=None
        )

        GLViewWidget.__init__(self, *args)

        self.origin_id = origin
        self.axes = []
        self.elems = np.zeros((1, 3))
        self.elem_plot = gl.GLScatterPlotItem(
            pos=self.elems, color=(1.0, 0.0, 1.0, 1.0)
        )

        self.addItem(self.elem_plot)

        self.message_port_register_in(pmt.intern("positions"))
        self.set_msg_handler(pmt.intern("positions"), self.handler)

        self.sigUpdateData.connect(self.updatePlot)

    def updatePlot(self, elems):
        self.elems = elems
        self.elem_plot.setData(pos=self.elems)
        for axis in self.axes:
            self.removeItem(axis)
        self.axes = []
        for elem in elems:
            axis = gl.GLAxisItem()
            axis.translate(*elem)
            self.axes.append(axis)
            self.addItem(axis)

    def handler(self, msg):
        data = pmt.to_python(msg)
        origin = data.get(self.origin_id)
        if origin is None:
            return
        origin = origin['tvec']

        pts = np.array([f['tvec'].T for f in data.values()]).reshape(-1, 3)

        self.sigUpdateData.emit(pts)
