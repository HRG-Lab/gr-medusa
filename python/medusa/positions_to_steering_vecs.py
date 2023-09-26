#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 Bailey Campbell.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr
from .aruco import marker
import time

import pmt

pi = np.pi
sin = np.sin
cos = np.cos


def H(x):
    return x.T.conj()


def v(k, r):
    kern = np.einsum("ijk,il->jkl", k, r)
    return np.exp(-1j * kern)


def k(wavelen, t, p):
    const = 2 * pi / wavelen
    return const * np.array([sin(t) * cos(p), sin(t) * sin(p), cos(t)])


class positions_to_steering_vecs(gr.sync_block):
    """
    docstring for block positions_to_steering_vecs
    """

    def __init__(
        self, marker_length=0.1, origin_id=0, element_ids=None, update_rate=0.5
    ):
        gr.sync_block.__init__(
            self,
            name="positions_to_steering_vecs",
            in_sig=None,
            out_sig=None,
        )

        self.update_rate = int(update_rate * 1e9)
        self.last_update = time.time_ns()

        self.element_ids = element_ids
        self.origin = origin_id
        self.marker_length = marker_length

        self.theta, self.phi = np.meshgrid(
            np.linspace(-pi, pi, 361), np.linspace(0, pi, 181), indexing="ij"
        )

        self.all_k = k(1, self.theta, self.phi)
        self.positions = {k: np.array([0, 0, 0]) for k in self.element_ids}

        self.message_port_register_in(pmt.intern("frame_info"))
        # self.set_msg_handler(pmt.intern("frame_info"), self.handle_positions)
        self.set_msg_handler(pmt.intern("frame_info"), self.gen_sample_positions)

        self.message_port_register_out(pmt.intern("steering vecs"))
        self.message_port_register_out(pmt.intern("positions"))

        # TESTING
        ids = np.array(range(0, 33))
        rvecs = [np.array([2.56513577, -0.30890672, 0.53359262]) for _ in ids]
        tvecs = self.sample_spherical(32).T
        tvecs = [tvec for tvec in tvecs]

        markers = self.process(ids, rvecs, tvecs)
        if markers is None:
            return

        markers = [
            m for m in markers if (m.id != self.origin) and (m.id in self.element_ids)
        ]

        if len(markers) == 0:
            return

        for m in markers:
            self.positions[m.id] = m.se3_relative_to_origin.tvec

        self.all_v = v(self.all_k, self.positions_to_array().T)

        np.save("/home/gaylybailey/all_v_gr", self.all_v)
        np.save("/home/gaylybailey/positions", self.positions_to_array())

    def positions_to_array(self):
        return np.array([pos for pos in self.positions.values()])

    def sample_spherical(self, npoints, ndim=3):
        vec = np.random.randn(ndim, npoints)
        vec /= np.linalg.norm(vec, axis=0)
        return vec

    def gen_sample_positions(self, msg):
        now = time.time_ns()
        if (now - self.last_update) < self.update_rate:
            return
        self.last_update = now

        self.message_port_pub(
            pmt.intern("positions"),
            pmt.cons(
                pmt.to_pmt(self.positions_to_array().shape),
                pmt.to_pmt(self.positions_to_array().ravel()),
            ),
        )

        self.message_port_pub(
            pmt.intern("steering vecs"),
            pmt.cons(pmt.to_pmt(self.all_v.shape), pmt.to_pmt(self.all_v.ravel())),
        )

    def handle_positions(self, msg):
        now = time.time_ns()
        if (now - self.last_update) < self.update_rate:
            return
        self.last_update = now

        d = pmt.to_python(msg)
        ids = d["ids"]
        rvecs = d["rvecs"]
        tvecs = d["tvecs"]

        markers = self.process(ids, rvecs, tvecs)
        if markers is None:
            return

        markers = [
            m for m in markers if (m.id != self.origin) and (m.id in self.element_ids)
        ]

        if len(markers) == 0:
            return

        for m in markers:
            self.positions[m.id] = m.se3_relative_to_origin.tvec

        all_v = v(self.all_k, self.positions_to_array().T)

        self.message_port_pub(
            pmt.intern("positions"),
            pmt.cons(
                pmt.to_pmt(self.positions_to_array().shape),
                pmt.to_pmt(self.positions_to_array().ravel()),
            ),
        )

        self.message_port_pub(
            pmt.intern("steering vecs"),
            pmt.cons(pmt.to_pmt(all_v.shape), pmt.to_pmt(all_v.ravel())),
        )

    def process(self, ids, rvecs, tvecs):
        ids = ids.tolist()

        try:
            o_idx = ids.index(self.origin)
        except ValueError:
            return None
        else:
            o = marker.Marker(
                self.origin, self.marker_length, rvecs[o_idx], tvecs[o_idx], origin=None
            )
            ret = [
                marker.Marker(num, self.marker_length, rvec, tvec, o)
                for num, rvec, tvec in zip(ids, rvecs, tvecs)
            ]

        return ret
