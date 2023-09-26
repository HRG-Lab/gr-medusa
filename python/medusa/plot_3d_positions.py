#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 Bailey Campbell.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr
from pyqtgraph.opengl import GLScatterPlotItem, GLViewWidget, GLGridItem

import pmt


class plot_3d_positions(gr.sync_block, GLViewWidget):
    """
    docstring for block plot_3d_positions
    """

    def __init__(self, parent=None):
        gr.sync_block.__init__(
            self, name="plot_3d_positions", in_sig=None, out_sig=None
        )

        GLViewWidget.__init__(self, parent=parent)
        g = GLGridItem()
        self.scatter = GLScatterPlotItem(color=(0.0, 1.0, 0.0, 1.0))
        self.addItem(g)
        self.addItem(self.scatter)
        self.show()

        self.message_port_register_in(pmt.intern("positions"))
        self.set_msg_handler(pmt.intern("positions"), self.handle_positions)

    def handle_positions(self, msg):
        shape, positions = pmt.to_python(pmt.car(msg)), pmt.to_python(pmt.cdr(msg))
        positions = positions.reshape(shape)
        self.scatter.setData(pos=positions)
