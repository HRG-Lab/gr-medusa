#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 Bailey Campbell.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
import cv2 as cv
from cv2 import aruco

from gnuradio import gr


class draw_detected_markers(gr.sync_block):
    """
    docstring for block draw_detected_markers
    """

    def __init__(self):
        gr.sync_block.__init__(
            self, name="Draw Detected Markers", in_sig=None, out_sig=None
        )

        self.message_port_register_in(pmt.intern("frame"))
        self.set_msg_handler(pmt.intern("frame"), self.draw_markers)

        self.message_port_register_out(pmt.intern("frame"))

    def draw_markers(self, msg):
        frame_shape = pmt.to_python(pmt.car(msg))
        frame = pmt.to_python(pmt.cdr(msg))
        frame = frame.reshape(frame_shape)
