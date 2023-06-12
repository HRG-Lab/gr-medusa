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


class weights_to_a_matrix(gr.sync_block):
    """
    docstring for block weights_to_a_matrix
    """

    def __init__(self):
        gr.sync_block.__init__(
            self,
            name="weights_to_a_matrix",
            in_sig=None,
            out_sig=None
        )

        self.message_port_register_in(pmt.intern("weights"))
        self.set_msg_handler(pmt.intern("weights"), self.handle_weights)

        self.message_port_register_out(pmt.intern("A"))

    def handle_weights(self, msg):
        data = pmt.to_python(msg)
        weights = data.reshape(1, -1)
        self.message_port_pub(pmt.intern("A"), pmt.to_pmt(weights.tolist()))
