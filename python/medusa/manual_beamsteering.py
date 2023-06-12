#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 Bailey Campbell.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from scipy.constants import speed_of_light
from gnuradio import gr
from gnuradio.gr import pmt

pi = np.pi
cos = np.cos
sin = np.sin


class manual_beamsteering(gr.basic_block):
    """
    docstring for block manual_beamsteering
    """

    def __init__(self, elems=None, freq=1.0):
        gr.basic_block.__init__(
            self,
            name="manual_beamsteering",
            in_sig=None,
            out_sig=None
        )

        self.theta = 0
        self.phi = 0
        self.elems = elems
        self.n_elems = None
        if elems is not None:
            self.n_elems = len(self.elems)
        self.freq = freq
        self.wavelen = speed_of_light / self.freq
        self.message_port_register_out(pmt.intern("weights"))
        self.message_port_register_in(pmt.intern("positions"))
        self.set_msg_handler(pmt.intern("positions"), self.set_posns)

    def k(self, theta, phi):
        return 2 * pi * np.array([
            sin(theta)*cos(phi),
            sin(theta)*sin(phi),
            cos(theta)
        ])

    def set_angle_degrees(self, theta, phi):
        self.theta = theta
        self.phi = phi
        k = self.k(theta, phi)

        w = np.zeros(self.n_elems, dtype=np.complex64)
        w = np.exp(1j * k @ self.elems.T)

        self.message_port_pub(pmt.intern("weights"), pmt.to_pmt(w))

    def set_posns(self, msg):
        data = pmt.to_python(msg)
        self.elems = data.reshape(-1, 3)
        self.set_angle_degrees(self.theta, self.phi)
