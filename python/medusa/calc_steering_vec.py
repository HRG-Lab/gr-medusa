#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 Bailey Campbell.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
import scipy
from scipy.constants import speed_of_light
from gnuradio import gr
from gnuradio.gr import pmt

pi = np.pi
sin = np.sin
cos = np.cos


class calc_steering_vec(gr.sync_block):
    """
    docstring for block calc_steering_vec
    """

    def __init__(self, thetas=None, phis=None, frequency=0.0):
        gr.sync_block.__init__(
            self,
            name="calc_steering_vec",
            in_sig=None,
            out_sig=None
        )
        self.thetas, self.phis = np.meshgrid(
            thetas, phis, indexing='ij'
        )
        self.freq = frequency
        wavelen = speed_of_light / self.freq
        self.ks = self.k(wavelen, self.thetas, self.phis)

        self.message_port_register_in(pmt.intern("positions"))
        self.set_msg_handler(pmt.intern("positions"), self.handler)
        self.message_port_register_out(pmt.intern("vecs"))

    def handler(self, msg):
        data = pmt.to_python(msg)
        elems = data.reshape(-1, 3)
        vs = self.v(self.ks, elems.T)
        self.message_port_pub(
            pmt.intern("vecs"),
            pmt.cons(pmt.to_pmt({'shape': vs.shape}), pmt.to_pmt(vs))
        )

    def k(self, wavelen, t, p):
        const = 2 * pi / wavelen
        return const * np.array([
            sin(t)*cos(p),
            sin(t)*sin(p),
            cos(t)
        ])

    def v(self, k, r):
        kern = np.einsum('ijk,il->jkl', k, r)
        return np.exp(-1j * kern)
