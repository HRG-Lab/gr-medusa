#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Perspecta Labs Inc. All rights reserved
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#


import numpy as np
from gnuradio import gr
from math import pi, sin
import pmt


class ula_sim(gr.sync_block):
    """
    Simulate reception through a Uniform Linear Array
    """
    def __init__(self, num_elements=4, sep_lambda=0.5, angle_degrees=0, log_response = False):
        gr.sync_block.__init__(self,
            name="uniform_linear_array",
            in_sig=[np.complex64],
            out_sig=[(np.complex64,num_elements)])

        self.num_elements = num_elements
        self.set_angle_degrees(angle_degrees)
        self.set_sep_lambda(sep_lambda)

        self.log_response = log_response
        self.plot_depth=70.0

        self.message_port_register_in(pmt.intern("weights"))
        self.set_msg_handler(pmt.intern("weights"), self.handle_weights)
        
        self.message_port_register_out(pmt.intern("plot"))

    def set_angle_degrees(self, angle_degrees):
        self.angle_degrees = angle_degrees
        self.theta = self.angle_degrees * pi / 180.0

    def set_sep_lambda(self, sep_lambda):
        self.sep_lambda = sep_lambda

    def set_log_response(self, log_response):
        self.log_response = log_response


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        
        m = 0
        for m in range(self.num_elements):

            out[:,m] = in0*np.exp(((-2.0*pi*float(m)*self.sep_lambda*sin(self.theta)))*1.0j)

        return len(output_items[0])

    def handle_weights(self, msg):
        weights = np.conj(pmt.c32vector_elements(msg))
        angles = np.array(np.linspace(-90.0,90.0,1801), dtype=np.float32)
        wr = self.weight_response(weights, angles, self.sep_lambda)
        # print(weights)
        self.message_port_pub(pmt.intern("plot"), pmt.to_pmt({"r":wr,"theta":angles}))


    def weight_response(self,weights,angles,lam):

        M = len(weights)
        theta = np.pi * angles/180.0
        sum_array = np.zeros(len(theta))
        for m in range(M):
            a = np.exp(-2.0*np.pi*m*lam*np.sin(theta)*1j)
            sum_array = sum_array + a*weights[m]
        #wr = 10.0 * np.log10(np.abs(sum_array))
        wr = np.abs(sum_array)       
        wr = wr / np.max(wr)
        
        if self.log_response:
            wr = 20.0 * np.log10(wr)
            wr = 1 + wr / self.plot_depth
            wr = np.clip(wr,0.0,1.0)
        
        return wr
