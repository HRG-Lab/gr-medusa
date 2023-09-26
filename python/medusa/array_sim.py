#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 Bailey Campbell.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr

import pmt

pi = np.pi
sin = np.sin
cos = np.cos


def sph2cart(r, t, p):
    x = r * sin(t) * cos(p)
    y = r * sin(t) * sin(p)
    z = r * cos(t)

    return x, y, z


def H(x):
    return x.T.conj()


def v(k, r):
    kern = np.einsum("ijk,il->jkl", k, r)
    return np.exp(-1j * kern)


def k(wavelen, t, p):
    const = 2 * pi / wavelen
    return const * np.array([sin(t) * cos(p), sin(t) * sin(p), cos(t)])


def y(w, a):
    return np.dot(a, H(w).T).squeeze()


class array_sim(gr.sync_block):
    """
    docstring for block array_sim
    """

    def __init__(self, signal_angle=(0, 0), wavelen=1, num_elems=32):
        gr.sync_block.__init__(
            self,
            name="array_sim",
            in_sig=[np.complex64],
            out_sig=[np.complex64],
        )
        self.thetas = np.linspace(-180, 180, 361)
        self.phis = np.linspace(0, 180, 181)
        self.theta, self.phi = np.meshgrid(
            np.linspace(-pi, pi, 361), np.linspace(0, pi, 181), indexing="ij"
        )

        self.wavelen = wavelen
        self.num_elems = num_elems
        self.positions = np.zeros((num_elems, 3))

        self.all_k = k(wavelen, self.theta, self.phi)
        self.all_v = v(self.all_k, self.positions.T)
        self.weights = np.ones((self.num_elems, 1))
        self.sig = signal_angle
        self.noise = 0.001
        self.v_s = self.all_v[180 + self.sig[0], self.sig[1]]

        self.message_port_register_in(pmt.intern("steering vecs"))
        self.set_msg_handler(pmt.intern("steering vecs"), self.handle_steering_vecs)

        self.message_port_register_in(pmt.intern("weights"))
        self.set_msg_handler(pmt.intern("weights"), self.handle_weights)

        self.message_port_register_out(pmt.intern("plot"))

        self.i = 0

    def set_signal_angle(self, theta, phi):
        self.sig = (theta, phi)
        self.v_s = self.all_v[180 + self.sig[0], self.sig[1]]

    def set_steering_vecs(self, vecs):
        self.all_v = vecs
        self.v_s = self.all_v[180 + self.sig[0], self.sig[1]]

    def handle_steering_vecs(self, msg):
        shape, vecs = pmt.to_python(pmt.car(msg)), pmt.to_python(pmt.cdr(msg))
        vecs = vecs.reshape(shape)
        self.set_steering_vecs(vecs)

    def handle_weights(self, msg):
        weights = pmt.to_python(msg)
        self.weights = weights
        self.send_plot()

    def send_plot(self):
        r = y(self.weights, self.all_v)
        plot_data = {
            "r": {"data": r, "shape": r.shape},
            "theta": {"data": self.thetas, "shape": self.thetas.shape},
            "phi": {"data": self.phis, "shape": self.phis.shape},
        }
        self.message_port_pub(pmt.intern("plot"), pmt.to_pmt(plot_data))

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        out[:] = in0 * y(self.weights, self.v_s)

        self.send_plot()

        return len(output_items[0])
