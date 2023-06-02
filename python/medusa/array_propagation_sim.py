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

pi = np.pi
cos = np.cos
sin = np.sin


class array_propagation_sim(gr.sync_block):
    """
    docstring for block array_propagation_sim
    """

    def __init__(self, n_elems, signal_angle=(0, 0), frequency=0.0):
        gr.sync_block.__init__(
            self,
            name="array_propagation_sim",
            in_sig=[np.complex64],
            out_sig=[(np.complex64, n_elems)]
        )
        self.n_elems = n_elems
        self.freq = frequency
        self.signal_angle = signal_angle

        self.steering_vecs = np.zeros((361, 181, self.n_elems))

        self.message_port_register_in(pmt.intern("steering_vecs"))
        self.set_msg_handler(pmt.intern("steering_vecs"), self.handler)

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        v_s = self.steering_vecs[180 + self.signal_angle[0],
                                 self.signal_angle[1]].reshape(-1, 1)
        out[:] = (in0 * v_s).T

        return len(output_items[0])

    def handler(self, msg):
        data = pmt.to_python(msg)
        self.steering_vecs = data[1].reshape(data[0]['shape'])
