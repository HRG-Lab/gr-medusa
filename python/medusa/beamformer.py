#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 Bailey Campbell.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
from abc import ABC, abstractmethod

import numpy as np
from gnuradio import gr

import pmt

pi = np.pi
sin = np.sin
cos = np.cos


class BeamformingAlgorithm(ABC):
    @abstractmethod
    def calculate_weights(self, **kwargs):
        pass

    def H(self, x):
        return x.T.conj()

    def v(self, k, r):
        kern = np.einsum("ijk,il->jkl", k, r)
        return np.exp(-1j * kern)

    def k(self, wavelen, t, p):
        const = 2 * pi / wavelen
        return const * np.array([sin(t) * cos(p), sin(t) * sin(p), cos(t)])

    def y(self, w, a):
        return np.dot(a, self.H(w).T).squeeze()


class MMSE(BeamformingAlgorithm):
    def __init__(self, **kwargs):
        self.num_elems = kwargs.pop("num_elems")
        self.signal_power = kwargs.pop("signal_power")
        self.noise_power = kwargs.pop("noise_power")
        self.sig_angle = kwargs.pop("signal_angle")
        self.intf_angle = kwargs.pop("intf_angle")
        self.all_v = np.zeros((361, 181, self.num_elems))
        self.weights = None

    def set_steering_vecs(self, vecs):
        self.all_v = vecs

    def set_sig_angle(self, angle):
        self.sig_angle = angle

    def set_intf_angle(self, angle):
        self.intf_angle = angle

    def calculate_weights(self, **kwargs):
        v_s = self.all_v[180 + self.sig_angle[0], self.sig_angle[1]].reshape(-1, 1)
        r_ss = v_s @ self.H(v_s)

        v_i = np.hstack(
            (
                self.all_v[180 + self.intf_angle[0], self.intf_angle[1]].reshape(-1, 1),
                # all_v[180 + intf2[0], 0].reshape(-1, 1),
            )
        )

        r_ii = v_i @ self.H(v_i)
        r_nn = self.noise_power * np.eye(self.num_elems)
        r_uu = r_ii + r_nn
        r_xx = r_ss + r_uu

        weights = self.signal_power * np.linalg.inv(r_xx.T) @ v_s
        np.save("/home/gaylybailey/weights_gr", weights)
        return weights


class beamformer(gr.sync_block):
    """
    docstring for block beamformer
    """

    def __init__(self, nstreams=32, beamformer=MMSE, **kwargs):
        gr.sync_block.__init__(
            self, name="beamformer", in_sig=[(np.complex64, nstreams)], out_sig=None
        )

        self.nstreams = nstreams

        self.beamformer = beamformer(num_elems=nstreams, **kwargs)

        self.message_port_register_in(pmt.intern("steering vecs"))
        self.set_msg_handler(pmt.intern("steering vecs"), self.handle_steering_vecs)

        self.message_port_register_out(pmt.intern("weights"))

    def set_signal_angle(self, angle):
        self.beamformer.set_sig_angle(angle)

    def set_intf_angle(self, angle):
        self.beamformer.set_intf_angle(angle)

    def handle_steering_vecs(self, msg):
        vecs = pmt.to_python(pmt.cdr(msg)).reshape(pmt.to_python(pmt.car(msg)))
        self.beamformer.set_steering_vecs(vecs)
        weights = self.beamformer.calculate_weights()
        self.message_port_pub(pmt.intern("weights"), pmt.to_pmt(weights))

    def work(self, input_items, output_items):
        return len(input_items[0])
