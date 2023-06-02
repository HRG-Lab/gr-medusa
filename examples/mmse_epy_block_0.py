"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from scipy.constants import speed_of_light
from gnuradio import gr
from gnuradio.gr import pmt


def sample_spherical(npoints, ndim=3):
    vec = np.random.randn(ndim, npoints)
    vec /= np.linalg.norm(vec, axis=0)
    return vec


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, n_elems=8, freq=1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Random Positions',
            in_sig=None,
            out_sig=None
        )
        self.n_elems = n_elems
        self.freq = freq
        self.wavelen = speed_of_light / self.freq
        self.elems = self.wavelen * sample_spherical(self.n_elems).T
        self.rng = np.random.default_rng()
        
        self.message_port_register_in(pmt.intern("trigger"))
        self.set_msg_handler(pmt.intern("trigger"), self.handler)
        
        self.message_port_register_out(pmt.intern("positions"))


    def handler(self, msg):
        perturbations = self.rng.standard_normal(size=self.elems.shape)
        self.elems += perturbations
        
        self.message_port_pub(
            pmt.intern("positions"), 
            pmt.to_pmt(self.elems)
        )
