"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
from math import pi, sin
import pmt
import numpy

class weights_to_plot(gr.basic_block):
    """
    docstring for block weights_to_plot
    """
    def __init__(self, num_elements=4, sep_lambda=0.5, log_response=True ):
        gr.basic_block.__init__(self,
            name="weights_to_plot",
            in_sig=None,
            out_sig=None)
        self.message_port_register_in(pmt.intern("weights"))
        self.set_msg_handler(pmt.intern("weights"), self.handle_weights)
        self.message_port_register_out(pmt.intern("plot"))

        self.num_elements = num_elements

        self.set_sep_lambda(sep_lambda)

        self.set_log_response(log_response)
        self.plot_depth=70.0


    def set_sep_lambda(self, sep_lambda):
        self.sep_lambda = sep_lambda

    def set_log_response(self, log_response):
         self.log_response = log_response
         print(f"{self.log_response=}")

    def handle_weights(self, msg):
        sizevec = pmt.to_python(pmt.car(msg))
        weights = pmt.to_python(pmt.cdr(msg))

        angles = np.array(np.linspace(-180.0,180.0,361), dtype=np.float32    )
        wr = self.weight_response(weights, angles, self.sep_lambda)

        self.message_port_pub(pmt.intern("plot"), pmt.to_pmt({"r":wr,"theta":angles}))

    def weight_response(self,weights,angles,lam):
        M = len(weights)
        theta = np.pi * angles/180.0
        sum_array = np.zeros(len(theta))
        for m in range(M):
            a = np.exp(-2.0*np.pi*m*lam*np.sin(theta)*1j)
            sum_array = sum_array + a*weights[m]
        
        wr = np.abs(sum_array)       
        wr = wr / np.max(wr)
        
        if self.log_response:
            wr = 20.0 * np.log10(wr)
            wr = 1 + wr / self.plot_depth
            wr = np.clip(wr,0.0,1.0)
        
        return wr
