#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 Bailey Campbell.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy as np
from gnuradio import gr
from math import pi, sin
import pmt


class manual_beamsteering(gr.basic_block):
    """
    Calculate weights for a calibrated ULA in a given direction
    """

    def __init__(self, num_elements=4, sep_lambda=0.5, angle_degrees=0.0):
        gr.basic_block.__init__(
            self, name="manual_beamsteering", in_sig=None, out_sig=None
        )

        self.num_elements = num_elements
        self.sep_lambda = sep_lambda
        self.message_port_register_out(pmt.intern("weights"))
        self.set_angle_degrees(angle_degrees)

    def set_angle_degrees(self, angle_degrees):
        self.angle_degrees = angle_degrees
        self.theta = self.angle_degrees * pi / 180.0
        # Calculate the weights
        w = [0.0 + 0.0j] * self.num_elements
        m = 0
        for m in range(self.num_elements):
            w[m] = np.exp(
                ((-2.0 * pi * float(m) * self.sep_lambda * sin(self.theta))) * 1.0j
            )

        vec = pmt.init_c32vector(len(w), w)
        sz = pmt.init_u32vector(2, [1, len(w)])
        self.message_port_pub(pmt.intern("weights"), pmt.cons(sz, vec))
