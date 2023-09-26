#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2023 gr-medusa author.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


from gnuradio import gr
import numpy as np

import pmt


class weights_to_matrix_a(gr.sync_block):
    """
    Converts calculated weights to Matrix A format expected by Multiply Matrix block
    """

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.basic_block.__init__(
            self,
            name="weights_to_matrix_a",  # will show up in GRC
            in_sig=None,
            out_sig=None,
        )

        self.message_port_register_in(pmt.intern("weights"))
        self.set_msg_handler(pmt.intern("weights"), self.handler)

        self.message_port_register_out(pmt.intern("A"))

    def handler(self, msg):
        # Check if msg is c32_vector
        if not pmt.is_pair(msg):
            print("Not expected c32 vector type")

        sizevec = pmt.to_python(pmt.car(msg))
        # print(sizevec)
        weights = pmt.to_python(pmt.cdr(msg))
        weights = np.reshape(weights, sizevec, order="C")
        # print(weights.shape)
        # print(weights)
        # print(weights.tolist())
        # print(weights[0])

        self.message_port_pub(pmt.intern("A"), pmt.to_pmt(weights.tolist()))

        # self.message_port_pub(pmt.intern("A"), pmt.to_pmt([[x.conjugate() for x in weights] ]))

        # message_port_pub(pdu_port_id, msg);
