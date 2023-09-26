"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt

class calc_array_weights(gr.sync_block):
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, num_elements=4, modulated_preamble=[]):
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Calc. Array Weights',   # will show up in GRC
            in_sig=None,
            out_sig=None
        )
        
        self.num_elems = num_elements
        self.modulated_preamble = modulated_preamble
        self.training_sequence = np.array(modulated_preamble).copy()
        
        self.message_port_register_in(pmt.intern("pdus"))
        self.message_port_register_out(pmt.intern("weights"))
        
        self.set_msg_handler(pmt.intern("pdus"), self.handle_pdus)
        
        
    def handle_pdus(self, msg):
        meta = pmt.car(msg);
        data = pmt.cdr(msg);

        nsamps_in = pmt.length(data);
        
        samps_interleaved = pmt.to_python(data)
        
        X = samps_interleaved.reshape((self.num_elems, -1))
        R = X @ np.conj(X.T)
        R = R + np.eye(*R.shape) * 1e-02
        p = X @ np.conj(self.training_sequence)
        w = np.conj(np.linalg.solve(R, p))
        
        vecpmt = pmt.to_pmt(w)
        sizepmt = pmt.to_pmt(w.shape)
        
        self.message_port_pub(pmt.intern("weights"), pmt.cons(sizepmt, vecpmt))
