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


class array_plot_3d(gr.sync_block, GLViewWidget):
    """
    docstring for block array_plot_3d
    """

    sigUpdateData = QtCore.Signal(object)

    def __init__(self, *args):
        gr.sync_block.__init__(
            self,
            name="array_plot_3d",
            in_sig=None,
            out_sig=None
        )

        GLViewWidget.__init__(self, *args)

        self.elems = np.zeros((1, 3))
        self.elem_plot = gl.GLScatterPlotItem(
            pos=self.elems, color=(1.0, 0.0, 1.0, 1.0)
        )
        self.axes_plot = gl.GLAxisItem()

        self.addItem(self.elem_plot)
        self.addItem(self.axes_plot)

        self.message_port_register_in(pmt.intern("positions"))
        self.set_msg_handler(pmt.intern("positions"), self.handler)

        self.sigUpdateData.connect(self.updatePlot)

    def updatePlot(self, elems):
        self.elems = elems
        self.elem_plot.setData(pos=self.elems)

    def handler(self, msg):
        data = pmt.to_python(msg)
        data = data.reshape(-1, 3)

        self.sigUpdateData.emit(data)
